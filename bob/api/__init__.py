from __future__ import unicode_literals

from . import hooks


def includeme(config):
    hooks.HookController.scan(config)
