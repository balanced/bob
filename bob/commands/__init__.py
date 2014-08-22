from __future__ import unicode_literals

import click

import bob
from . import build, serve, consume


@click.command('version')
def version():
    click.echo(bob.__version__)


def add_commands(group):
    group.add_command(version)
    group.add_command(build.group)
    group.add_command(serve.serve)
    group.add_command(consume.group)
