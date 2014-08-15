from __future__ import unicode_literals
import json
import os

from thed import api


def create(**overrides):
    return api.Application.create(
        {},
        includes=['thed.api.resources', 'thed.api.controllers', 'bob.api'],
        **overrides
    )


def create_integration_app(**overrides):
    def hook(config):
        config.add_view_predicate('resource', api.predicates.ResourcePredicate)
        config.scan()

    return create(hook=hook, **overrides)


def get_for_reals_path(file_name):
    return os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        file_name
    )


def load_json(path):
    with open(path) as f:
        return json.load(f)
