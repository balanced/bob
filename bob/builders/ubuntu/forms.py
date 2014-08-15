from __future__ import unicode_literals

import pilo


class Notification(pilo.Form):
    pass


class Destinations(pilo.Form):
    pass


class UbuntuForm(pilo.Form):

    dependencies = pilo.fields.List(pilo.fields.String(), default=[])

    build_dependencies = pilo.fields.List(pilo.fields.String(), default=[])

    before_install = pilo.fields.List(pilo.fields.String(), default=[])

    after_install = pilo.fields.List(pilo.fields.String(), default=[])

    before_remove = pilo.fields.List(pilo.fields.String(), default=[])

    after_remove = pilo.fields.List(pilo.fields.String(), default=[])

    exclude = pilo.fields.List(pilo.fields.String(), default=[])

    # TODO: how to map this? I tried
    # pilo.fields.Group(('hipchat', pilo.fields.SubForm(Notification)))
    # but did not work
    notifications = pilo.fields.SubForm(Notification, unmapped='capture')

    destinations = pilo.fields.SubForm(Destinations, unmapped='capture')


class Targets(pilo.Form):

    ubuntu = pilo.fields.SubForm(UbuntuForm)


class V1Settings(pilo.Form):

    version = pilo.Field(default='1')

    targets = pilo.fields.SubForm(Targets)
