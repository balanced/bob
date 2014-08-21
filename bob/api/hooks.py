from __future__ import unicode_literals
import json

from thed import api

from . import forms


@api.Resource.nest('hooks')
class Resource(api.Resource):

    pass


@api.RestController.register('hooks', context=Resource)
class Controller(api.RestController):

    @api.decorators.view_config(name='github', request_method='POST')
    def github(self):
        result = forms.GithubForm(self.request.json)
        return api.Response('github.created')

    @api.decorators.view_config(name='travis', request_method='POST')
    def travis(self):
        try:
            result = forms.TravisForm(self.request.json)
        except ValueError:
            # http://docs.travis-ci.com/user/notifications/
            # Webhooks are delivered with a application/x-www-form-urlencoded
            # content type using HTTP POST, with the body including a payload
            # parameter that contains the JSON webhook payload in a URL-encoded
            # format.
            result = forms.TravisForm(json.loads(self.request.POST['payload']))
        if result['build']:
            response = forms.build_threaded(
                result['organization'], result['name'], result['commit']
            )
        else:
            response = 'nope nope nope'

        def iterate_response():
            for lines in response:
                if isinstance(lines, tuple):
                    level, lines = lines
                if not isinstance(lines, list):
                    lines = [lines]
                for line in lines:
                    if not isinstance(line, basestring):
                        line = unicode(line)
                    yield str(line.encode('utf-8'))
                    yield str('\n')

        return api.Response(app_iter=iterate_response())
