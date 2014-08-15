from __future__ import unicode_literals

import pytest
from webtest import TestApp

from tests import fixtures


@pytest.fixture
def web_app():
    return TestApp(fixtures.create_integration_app())


@pytest.fixture
def travis_payload():
    return {
        "id": 1,
        "number": "1",
        "status": None,
        "started_at": None,
        "finished_at": None,
        "status_message": "Passed",
        "commit": "62aae5f70ceee39123ef",
        "branch": "master",
        "message": "the commit message",
        "committed_at": "2011-11-11T11: 11: 11Z",
        "committer_name": "Sven Fuchs",
        "committer_email": "svenfuchs@artweb-design.de",
        "author_name": "Sven Fuchs",
        "author_email": "svenfuchs@artweb-design.de",
        "type": "push",
        "build_url": "https://travis-ci.org/svenfuchs/minimal/builds/1",
        "repository": {
            "id": 1,
            "name": "minimal",
            "owner_name": "svenfuchs",
            "url": "http://github.com/svenfuchs/minimal"
        },
        "config": {
            "notifications": {
                "webhooks": ["http://evome.fr/notifications", "http://example.com/"]
            }
        }
    }


def test_hooks(web_app):
    response = web_app.post('/hooks/github')
    assert response.body == 'github.created'
    response = web_app.post('/hooks/travis')
    assert response.body == 'travis.created'
