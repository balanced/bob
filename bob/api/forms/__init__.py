from __future__ import unicode_literals
import json
import logging
import os

import boto
import boto.sqs
import boto.sqs.jsonmessage
import time

import github
import travis

from bob import builders
from bob.builders.ubuntu import UbuntuBuilder


logger = logging.getLogger(__name__)


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
    while True:
        # 3600 means we have an hour to build, this should be plenty of time
        for msg in queue.get_messages(num_messages=1, visibility_timeout=3600):
            kwargs = json.loads(msg.get_body())
            logger.debug('got message %s', kwargs)
            build_logger = builders.create_logger(**kwargs)
            build(logger=build_logger, **kwargs)

            msg.delete()
        time.sleep(0)


def build(github_organization, github_repo, commit_hash_or_tag,
          source=None, logger=None
):
    from bob import settings

    working_dir = os.path.expanduser(settings['bobb.work_dir'])
    output_dir = os.path.expanduser(settings['bobb.out_dir'])

    builder = UbuntuBuilder(
        github_repo, working_dir, output_dir, log_stream=logger
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
    finally:
        builder.log('***finished***')
