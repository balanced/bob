from __future__ import unicode_literals

from thed import api

from . import hooks


def includeme(config):
    hooks.HookController.scan(config)


def create(**overrides):
    return api.Application.create(
        {},
        includes=['thed.api.resources', 'thed.api.controllers'],
        **overrides
    )


def create_app(**overrides):
    def hook(config):
        includeme(config)
        config.add_view_predicate('resource', api.predicates.ResourcePredicate)
        config.scan()

    return create(hook=hook, **overrides)
