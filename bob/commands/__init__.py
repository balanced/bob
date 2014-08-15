from __future__ import unicode_literals

from . import build


def add_commands(group):
    group.add_command(build.group)
