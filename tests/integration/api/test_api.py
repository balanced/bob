from __future__ import unicode_literals

import pytest
from webtest import TestApp

from tests import fixtures


@pytest.fixture
def web_app():
    return TestApp(fixtures.create_integration_app())


def test_hooks(web_app):
    response = web_app.post('/hooks/github')
    assert response.body == 'github.created'
    response = web_app.post('/hooks/travis')
    assert response.body == 'travis.created'
