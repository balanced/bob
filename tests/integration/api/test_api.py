from __future__ import unicode_literals
import json
import mock

import pytest
from webtest import TestApp

from bob import api


from tests import fixtures


@pytest.fixture
def web_app():
    settings = {
        'working_dir': '~/work',
        'output_dir': '~/out',
    }
    return TestApp(api.create_app(**settings))


@pytest.fixture
def travis_payload():
    return fixtures.load_json(
        fixtures.get_for_reals_path('travis_webhook.json')
    )


@pytest.fixture(params=['master', '0.0.1'])
def travis_payload_and_result(request, travis_payload):
    travis_payload['branch'] = request.param
    expected_payload = {
        'commit': 'd4d7cb7392a0b501a64c4d54645ca0aa2b9c9d2d',
        'name': 'bob',
        'organization': 'balanced',
        'success': True,
        'build': request.param == '0.0.1',
        'branch': request.param
    }
    return travis_payload, expected_payload


@pytest.fixture
def travis_auth_headers():
    return {
        'Travis-Repo-Slug': 'balanced/bob',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': (
            'f5191fd8903bcb2c8402d6b0f6b8a8482644b5a2f498437bea1ce12fcb15eea6'
        )
    }


@pytest.fixture
def github_payload():
    return fixtures.load_json(
        fixtures.get_for_reals_path('github_webhook.json')
    )


def post_json(web_app, url, payload, headers=None):
    default_headers = {

    }
    default_headers.update(headers or {})
    return web_app.post(
        url, params=json.dumps(payload),
        headers=dict(
            (str(k), str(v)) for k, v in default_headers.iteritems()
        )
    )


def test_github(web_app, github_payload):
    response = post_json(web_app, '/hooks/github', github_payload)
    assert response.body == 'github.created'


@mock.patch('bob.api.forms.build_threaded')
def test_travis(build, web_app, travis_payload, travis_auth_headers):
    build.return_value = 'travis.created'
    response = post_json(
        web_app, '/hooks/travis',
        travis_payload,
        headers=travis_auth_headers
    )
    assert response.body == 'travis.created'
    args, _ = build.call_args
    assert args == (
        'balanced', 'bob', 'd4d7cb7392a0b501a64c4d54645ca0aa2b9c9d2d'
    )


def test_github_payload_parsing(github_payload):
    result = api.hooks.forms.GithubForm(github_payload)
    assert result == {
        'commit': 'refs/tags/0.0.1',
        'name': 'bob',
        'organization': 'balanced',
        'build': False
    }


def test_travis_payload_parsing(travis_payload_and_result):
    travis_payload, expected_payload = travis_payload_and_result
    result = api.hooks.forms.TravisForm(travis_payload)
    assert result == expected_payload


def test_travis_authentication_siging(travis_payload, travis_auth_headers):
    result = api.hooks.forms.TravisForm(travis_payload)
    assert api.hooks.forms.travis.compute_travis_security(
        travis_auth_headers, result
    )
