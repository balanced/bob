from __future__ import unicode_literals

from thed import api

from bob import __version__


@api.Resource.nest('health')
class Resource(api.Resource):

    pass


@api.RestController.register('health', context=Resource)
class Controller(api.RestController):

    def index(self):
        return api.Response(__version__)
