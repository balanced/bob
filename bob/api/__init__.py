from __future__ import unicode_literals

from thed import api

import bob

from . import hooks, health


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


class Dispatcher(object):

    def __init__(self, app=None):
        bob.configure_logging()
        bob.init()
        app_settings = bob.init_config()
        self.app = app or create_app(**app_settings)

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)
