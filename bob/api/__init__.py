from __future__ import unicode_literals

import pyramid.threadlocal

from thed import api

from . import hooks, health


registry = pyramid.threadlocal.get_current_registry()
settings = registry.settings


def includeme(config):
    api.RestController.scan(config)


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
