from __future__ import unicode_literals

import pytest
from webtest import TestApp

from bob import api


from tests import fixtures


@pytest.fixture
def web_app():
    return TestApp(api.create_app())


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


def test_github_payload_parsing(github_payload):
    result = api.hooks.forms.GithubForm(github_payload)
    assert result == {
        'commit': 'refs/tags/0.0.1',
        'repository': {
            'name': 'bob',
            'organization': u'balanced'
        }
    }


def test_travis_payload_parsing(travis_payload):
    result = api.hooks.forms.TravisForm(travis_payload)
    assert result == {
        'commit': '62aae5f70ceee39123ef',
        'repository': {
            'name': u'minimal', 'organization': u'svenfuchs'
        }
    }
