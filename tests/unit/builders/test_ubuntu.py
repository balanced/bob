from __future__ import unicode_literals

import mock
import pytest

import bob
from bob.builders.ubuntu import UbuntuBuilder


@pytest.fixture
def ubuntu_builder():
    project_name = 'test'
    working_dir = '/test'
    output_dir = '/out'
    tmp_dir = '/tmp'
    return UbuntuBuilder(project_name, working_dir, output_dir, tmp_dir)


@pytest.yield_fixture
def ubuntu_builder_with_valid_settings(ubuntu_builder):
    valid_settings = dict(
        version=1,
        targets=dict(
            ubuntu=dict(
                exclude=['*pyc'],
                build_dependencies=['libpq-dev'],
                dependencies=['libpq'],
                before_install=[],
                after_install=[],
                before_remove=[],
                after_remove=[],
                destinations=dict(
                    s3=dict(

                    ),
                    depot=dict(

                    )
                ),
                notifications=dict(
                    hipchat=dict(
                        room_id='dev',
                        on=['success', 'failure']
                    )
                ),
            )
        )
    )
    with mock.patch.object(UbuntuBuilder, 'settings') as settings:
        settings.__get__ = mock.Mock(return_value=valid_settings)
        yield ubuntu_builder


@pytest.yield_fixture
def ubuntu_builder_with_invalid_settings(ubuntu_builder):
    with mock.patch.object(UbuntuBuilder, 'settings') as settings:
        settings.__get__ = mock.Mock(return_value=dict(
            version='2'
        ))
        yield ubuntu_builder


class TestUbuntuBuilder(object):

    def test_version_loading(self, ubuntu_builder_with_valid_settings):
        ub = ubuntu_builder_with_valid_settings
        ub.parse_options()
        assert all(key in ub.transports for key in ub.destinations.iterkeys())

    def test_invalid_version_loading(
            self, ubuntu_builder_with_invalid_settings
    ):
        with pytest.raises(bob.builders.InvalidSettingsVersion):
            ubuntu_builder_with_invalid_settings.parse_options()
