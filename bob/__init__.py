from __future__ import unicode_literals


__version__ = '0.0.8'


class BobError(Exception):
    pass


import api
import builders
import notifiers
import transports


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    return api.create_app()
