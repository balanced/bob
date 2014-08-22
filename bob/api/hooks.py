from __future__ import unicode_literals
import json
import logging
import os

from thed import api

from . import forms


logger = logging.getLogger(__name__)


@api.Resource.nest('hooks')
class Resource(api.Resource):

    pass


@api.RestController.register('hooks', context=Resource)
class Controller(api.RestController):

    @api.decorators.view_config(name='logs')
    def logs(self):
        from bob import settings

        def iterate_response():
            root = os.path.expanduser(settings['bobb.log_dir'])
            for file_name in list_logs(root):
                yield str(os.path.relpath(file_name, root))
                yield str('\n')
        return api.Response(app_iter=iterate_response())

    @api.decorators.view_config(name='github', request_method='POST')
    def github(self):
        forms.github.WebhookForm(self.request.json)
        return api.Response('github.created')

    @api.decorators.view_config(name='travis', request_method='POST')
    def travis(self):
        try:
            result = forms.travis.WebhookForm(self.request.json)
        except ValueError:
            # http://docs.travis-ci.com/user/notifications/
            # Webhooks are delivered with a application/x-www-form-urlencoded
            # content type using HTTP POST, with the body including a payload
            # parameter that contains the JSON webhook payload in a URL-encoded
            # format.
            result = forms.travis.WebhookForm(
                json.loads(self.request.POST['payload'])
            )

        logger.info(result)

        if result['build']:
            response = forms.queue_build(
                result['organization'], result['name'], result['branch']
            )
        else:
            response = 'nope nope nope'

        return api.Response(response)


def list_logs(path):
    for root_directory, directories, files in os.walk(path):
        for file_name in files:
            yield os.path.join(root_directory, file_name)
        for current_directory in directories:
            for file_name in list_logs(
                    os.path.join(root_directory, current_directory)
            ):
                yield file_name
