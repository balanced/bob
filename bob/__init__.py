from __future__ import unicode_literals

import logging
import logging.config
import os
import sys

import ConfigParser


__version__ = '0.2.6'

logger = logging.getLogger(__name__)


class BobError(Exception):
    pass


def configure_logging(log_config=None, log_level=logging.INFO):
    log_config = log_config or os.environ.get('BOB_LOGGING_CONF', None)
    if log_config and os.path.exists(log_config):
        try:
            logging.config.dictConfig(eval(open(log_config, 'r').read()))
            logging.getLogger().setLevel(log_level)
        except Exception as ex:
            print >> sys.stderr, 'unable to load "{}" - {}'.format(
                log_config, str(ex)
            )
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
                stream=sys.stderr,
            )
    else:
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s : %(levelname)s : %(name)s : %(message)s',
            stream=sys.stderr,
        )


def init_config(overrides=None):
    if overrides == '-':
        overrides = None
    overrides = overrides or os.environ.get('BOB_CONF', None)
    if isinstance(overrides, dict):
        return overrides
    if overrides:
        logger.info('loading config overrides from "%s"', overrides)
        if not os.path.exists(overrides):
            raise Exception('Config %s not found' % overrides)
        config = ConfigParser.RawConfigParser()
        config.read(overrides)
        return dict(config.items('bobb:main'))
    return {}


settings = None


def init():
    global settings
    settings = init_config()


import api
import builders
import notifiers
import transports
