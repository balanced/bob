from __future__ import unicode_literals
import logging
import wsgiref.simple_server

import click

from bob import api


logger = logging.getLogger(__name__)


@click.command('serve')
@click.option('--port', default=6543)
@click.option('--host', default='0.0.0.0')
def serve(port, host):
    dispatcher = api.Dispatcher()
    server = wsgiref.simple_server.make_server(
        host, port, dispatcher,
    )
    logger.info('serving on %s:%s ...', *server.server_address)
    server.serve_forever()
