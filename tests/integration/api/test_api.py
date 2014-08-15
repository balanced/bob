from __future__ import unicode_literals

import pytest
from webtest import TestApp

from tests import fixtures


@pytest.fixture
def web_app():
    return TestApp(fixtures.create_integration_app())


@pytest.fixture
def travis_payload():
    return fixtures.load_json(
        fixtures.get_for_reals_path('travis_webhook.json')
    )


@pytest.fixture
def github_payload():
    return fixtures.load_json(
        fixtures.get_for_reals_path('github_webhook.json')
    )


def test_hooks(web_app):
    response = web_app.post('/hooks/github')
    assert response.body == 'github.created'
    response = web_app.post('/hooks/travis')
    assert response.body == 'travis.created'
