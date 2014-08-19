from __future__ import unicode_literals
import logging
import wsgiref.simple_server

import click

from bob import api


logger = logging.getLogger(__name__)


class Dispatcher(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        return self.app(environ, start_response)


@click.command('serve')
@click.option('--port', default=6543)
@click.option('--host', default='0.0.0.0')
def serve(port, host):
    dispatcher = Dispatcher(api.create_app())
    server = wsgiref.simple_server.make_server(
        host, port, dispatcher,
    )
    logger.info('serving on %s:%s ...', *server.server_address)
    server.serve_forever()
