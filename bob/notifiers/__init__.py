from __future__ import unicode_literals
import os

import hipchat
import hipchat.commands
import hipchat.room

from bob.builders.ubuntu import UbuntuBuilder


@UbuntuBuilder.register_notification('travis')
def notify(message, **options):
    payload = {
        'from': 'bob the builder',
        'room_id': 'dev',
        'color': 'purple',
        'message_format': 'html',
        'message': message
    }
    payload.update(options)

    hipchat.config.init_cfg(os.path.expanduser('~/.hipchat.cfg'))
    hipchat.room.Room.message(**payload)
