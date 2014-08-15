from __future__ import unicode_literals
import logging

import click

from bob.builders.ubuntu import UbuntuBuilder


logger = logging.getLogger(__name__)

# where we clone to while we're building
WORKING_DIR = '/tmp/bob-the-builder'
# where the outputted package will end up
OUTPUT_DIR = '/opt'


@click.group('build')
def group():
    pass


@group.command('ubuntu')
@click.argument('github-organization')
@click.argument('github-repo')
@click.argument('commit-hash-or-tag')
@click.option('--source', help='Existing folder within ' + WORKING_DIR)
def build_ubuntu(github_organization, github_repo, commit_hash_or_tag,
                 source=None):
    builder = UbuntuBuilder(
        github_repo, WORKING_DIR, OUTPUT_DIR
    )
    if not source:
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
