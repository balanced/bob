from __future__ import unicode_literals

import logging
import os
import subprocess

import boto
import boto.sqs
import boto.sqs.jsonmessage
import gevent
import gevent.queue

import github
import travis
from github import GithubForm
from travis import TravisForm

from bob.builders.ubuntu import UbuntuBuilder


logs = gevent.queue.Queue()


# the more i think about this the more i think a file based approach is best.
# if we stream to a file called balanced/balanced/commit_hash.log then it's
# easy to check for the existence of that file and return that data
# when queried for it later.


# same as UbuntuBuilder but emits log messages to a gevent queue
class ThugBuilder(UbuntuBuilder):

    def log(self, msg, level='info', **kwargs):
        super(ThugBuilder, self).log(msg, level, **kwargs)
        logs.put((level, msg))
        gevent.sleep(0)


# hacked up easy way out if we can't get this to work. returns an iterator with
# stdout from the shell command.
def build_subprocess(github_organization, github_repo, commit_hash_or_tag):
    command = ['bob build ubuntu {} {} {}'.format(
        github_organization, github_repo, commit_hash_or_tag
    )]
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    for line in process.stdout:
        yield line


def queue_build(github_organization, github_repo, commit_hash_or_tag):
    from bob import settings
    conn = boto.sqs.connect_to_region(settings['boto.region'])
    queue = conn.get_queue(settings['bobb.queue'])
    message = boto.sqs.jsonmessage.JSONMessage()
    message.update(**dict(
        github_organization=github_organization,
        github_repo=github_repo,
        commit_hash_or_tag=commit_hash_or_tag
    ))
    queue.write(message)
    return message.id


def queue_consume():
    from bob import settings
    conn = boto.sqs.connect_to_region(settings['boto.region'])
    queue = conn.get_queue(settings['bobb.queue'])
    for msg in queue.get_messages(num_messages=1):
        kwargs = json.loads(msg.get_body())
        background_build(**kwargs)


def build_threaded(github_organization, github_repo, commit_hash_or_tag):
    task = gevent.spawn(
        background_build, github_organization, github_repo, commit_hash_or_tag,
    )

    while not task.ready():
        while not logs.empty():
            yield logs.get()
            gevent.sleep(0)
        gevent.sleep(0)


def background_build(github_organization, github_repo, commit_hash_or_tag):
    from bob import settings

    # HACK: until we figure out settings.ini
    working_dir = os.path.expanduser(settings.get('working_dir', '~/work'))
    output_dir = os.path.expanduser(settings.get('output_dir', '/opt'))
    logger = create_logger(
        github_organization, github_repo, commit_hash_or_tag
    )

    builder = ThugBuilder(
        github_repo, working_dir, output_dir, log_stream=logger
    )
    builder.prepare_workspace(
        github_organization, github_repo, commit_hash_or_tag
    )
    builder.parse_options()
    try:
        builder.prepare_system()
        builder.build()
        package_name = builder.package(commit_hash_or_tag)
        builder.upload(package_name)
        builder.notify_success(commit_hash_or_tag)
    except Exception as ex:
        builder.notify_failure(commit_hash_or_tag, ex)
    finally:
        builder.log('***finished***')


def create_logger(github_organization, github_repo, commit_hash_or_tag):
    logger = logging.getLogger(__name__)
    log_path = os.path.expanduser(
        '~/logs/{0}/{1}/{0}-{1}-{2}.log'.format(
            github_organization, github_repo, commit_hash_or_tag
        )
    )
    directory, _ = os.path.split(log_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    log_file = logging.FileHandler(log_path)
    log_format = logging.Formatter(
        '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
    )
    log_file.setFormatter(log_format)

    logger.addHandler(log_file)
    logger.setLevel(logging.DEBUG)

    return logger
