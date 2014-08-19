from __future__ import unicode_literals
import logging
import os
import subprocess

import yaml

from bob import BobError


logger = logging.getLogger(__name__)


class InvalidSettingsVersion(BobError):
    pass


class GithubMixin(object):

    def prepare_workspace(self, github_organization, github_repo,
                          commit_hash_or_tag, **_):
        # clone github repo into dir
        github_url = 'git@github.com:{}/{}'.format(
            github_organization, github_repo)
        clean_command = [
            'rm -rf {}'.format(self.source)
        ]
        clone_command = [
            'git clone {} {}'.format(github_url, self.source)
        ]
        checkout_command = [
            'git checkout {}'.format(commit_hash_or_tag)
        ]
        for command, kwargs in (
            (clean_command, {}), (clone_command, {}),
            (checkout_command, dict(cwd=self.source)),
        ):
            self.run_command(command, **kwargs)


class Builder(object):

    type = 'deb'

    settings_file_name = 'build.yml'

    flavor = None

    destinations = None

    notifications = None

    logger = None

    def __init__(self, project_name, working_dir, output_dir, tmp_dir=None,
                 log_stream=None):
        self.project_name = project_name
        self.working_dir = working_dir
        self.output_dir = output_dir
        self.tmp_dir = os.path.join(
            (tmp_dir or '/tmp'), project_name + '.build'
        )
        self.configured = False
        self.logger = log_stream or logger

    @property
    def source(self):
        return '{working_dir}/{project_name}'.format(
            working_dir=self.working_dir,
            project_name=self.project_name
        )

    @property
    def target(self):
        return '{output_dir}/{project_name}'.format(
            output_dir=self.output_dir,
            project_name=self.project_name
        )

    def log(self, msg, level='info', **kwargs):
        getattr(self.logger, level)(msg, **kwargs)

    def run_command(self, command, **kwargs):
        if not isinstance(command, list):
            command = [command]

        self.log(command, 'debug')
        self.log(kwargs, 'debug')

        result = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            shell=True, **kwargs
        )

        for line in result.stdout:
            self.log(line.decode('utf8').replace('\n', '', 1), 'info')

        if result.returncode:
            raise Exception(
                'Failed to run command, exited with {}'.format(
                    result.returncode
                )
            )

    def prepare_workspace(self, github_organization, github_repo,
                          commit_hash_or_tag):
        # clone github repo into dir
        github_url = 'git@github.com:{}/{}'.format(
            github_organization, github_repo)
        clean_command = [
            'rm -rf {}'.format(self.source)
        ]
        mkdir_command = [
            'mkdir -p {}'.format(self.source)
        ]
        clone_command = [
            'git clone {} {}'.format(github_url, self.source)
        ]
        checkout_command = [
            'git checkout {}'.format(commit_hash_or_tag)
        ]
        for command, kwargs in (
            (clean_command, {}), (mkdir_command, {}), (clone_command, {}),
            (checkout_command, dict(cwd=self.source)),
        ):
            self.run_command(command, **kwargs)

    @property
    def settings_file(self):
        return open(os.path.join(self.source, self.settings_file_name))

    @property
    def settings(self):
        return yaml.safe_load(self.settings_file)

    _options_parsers = {}

    def parse_options(self):
        settings = self.settings
        version = settings.get('version', '1')
        try:
            self._options_parsers[str(version)]()
        except KeyError as ex:
            raise InvalidSettingsVersion(ex)

    def prepare_system(self):
        pass

    def build(self):
        pass

    def package(self, version):
        pass

    def notify(self, message, event=None):
        for channel, options in self.notifications.iteritems():
            if event and options and event in options.get('events', []):
                self.notifiers[channel](message)

    def notify_success(self, version):
        self.notify(
            'built {} version {} and uploaded to unstable'.format(
                self.project_name, version
            ),
            event='success',
        )

    def notify_failure(self, version, ex):
        self.notify(
            '{} version {} failed to build.<br><br><pre>{}</pre>'.format(
                self.project_name, version, str(ex)
            ),
            event='failure'
        )

    def upload(self, path_to_file):
        for transport, kwargs in self.destinations.iteritems():
            self.transports[transport](self).upload(path_to_file, **kwargs)

    transports = {}

    @classmethod
    def register_transport(cls, key):
        def register(klass):
            cls.transports[key] = klass
            return klass
        return register

    notifiers = {}

    @classmethod
    def register_notification(cls, key):
        def register(fn):
            cls.notifiers[key] = fn
            return fn
        return register
