from __future__ import unicode_literals

from . import build, serve


def add_commands(group):
    group.add_command(build.group)
    group.add_command(serve.serve)
