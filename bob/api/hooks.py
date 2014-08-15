from __future__ import unicode_literals

from thed import api

from . import forms


@api.Resource.nest('hooks')
class HookResource(api.Resource):

    pass


@api.RestController.register('hooks', context=HookResource)
class HookController(api.RestController):

    @api.decorators.view_config(name='github', request_method='POST')
    def github(self):
        result = forms.GithubForm(self.request.json)
        return api.Response('github.created')

    @api.decorators.view_config(name='travis', request_method='POST')
    def travis(self):
        result = forms.TravisForm(self.request.json)
        if result['build']:
            forms.build(
                result['organization'], result['name'], result['commit']
            )
        return api.Response('travis.created')
