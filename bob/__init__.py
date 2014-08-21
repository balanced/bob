from __future__ import unicode_literals

import logging
import logging.config
import os
import sys


__version__ = '0.2.4'


class BobError(Exception):
    pass


import api
import builders
import notifiers
import transports


def configure_logging(log_config=None, log_level=logging.INFO):
    if log_config and os.path.exists(log_config):
        try:
            logging.config.dictConfig(eval(open(log_config, 'r').read()))
            logging.getLogger().setLevel(log_level)
        except Exception, ex:
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
