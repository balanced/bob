from __future__ import unicode_literals

from thed import api


@api.Resource.nest('hooks')
class HookResource(api.Resource):

    pass


@api.RestController.register('hooks', context=HookResource)
class HookController(api.RestController):

    @api.decorators.view_config(name='github', request_method='POST')
    def github(self):
        return api.Response('github.created')

    @api.decorators.view_config(name='travis', request_method='POST')
    def travis(self):
        return api.Response('travis.created')
