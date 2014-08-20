from __future__ import unicode_literals

import pytest
from webtest import TestApp

from bob import api, __version__


@pytest.fixture
def web_app():
    settings = {
        'working_dir': '~/work',
        'output_dir': '~/out',
    }
    return TestApp(api.create_app(**settings))


def test_health(web_app):
    response = web_app.get('/health')

    assert response.body == str(__version__)
