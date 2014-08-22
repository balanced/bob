from __future__ import unicode_literals
import logging

import click

from bob import builders
from bob.api.forms import build


logger = logging.getLogger(__name__)


@click.group('build')
def group():
    pass


@group.command('ubuntu')
@click.argument('github-organization')
@click.argument('github-repo')
@click.argument('commit-hash-or-tag')
@click.option('--source')
def build_ubuntu(github_organization, github_repo, commit_hash_or_tag,
                 source=None):
    logger = builders.create_logger(
        github_organization, github_repo, commit_hash_or_tag
    )
    build(
        github_organization,
        github_repo,
        commit_hash_or_tag,
        logger=logger,
        source=source
    )
