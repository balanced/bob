from __future__ import unicode_literals
import logging

import click

from bob.api import forms


logger = logging.getLogger(__name__)


@click.group('consume')
def group():
    pass


@group.command('messages')
def consume_messages():
    forms.queue_consume()
