from __future__ import unicode_literals

import github
import travis
from github import GithubForm
from travis import TravisForm

from bob.builders.ubuntu import UbuntuBuilder


def build(github_organization, github_repo, commit_hash_or_tag):
    from bob.api import settings

    # HACK: until we figure out settings.ini
    settings = settings or {}
    working_dir = settings.get('working_dir', '~/work')
    output_dir = settings.get('output_dir', '~/out')
    builder = UbuntuBuilder(
        github_repo, working_dir, output_dir
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
