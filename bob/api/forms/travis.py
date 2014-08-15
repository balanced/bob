from __future__ import unicode_literals
from hashlib import sha256

import pilo


user_tokens = {
    'mjallday': 'irgy9pphBTydWzVYskRq'
}


class TravisRepoForm(pilo.Form):

    name = pilo.fields.String()

    organization = pilo.fields.String('owner_name')


class TravisForm(pilo.Form):

    commit = pilo.fields.String()

    repository = pilo.fields.SubForm(TravisRepoForm)

    success = pilo.fields.String('result_message')

    @success.munge
    def success(self, value):
        return value in ('Passed', 'Fixed')

    build = pilo.fields.Boolean(default=False)


def compute_travis_security(headers, form):
    auth_header = headers['Authorization']
    organization = form['repository']['organization']
    repo_name = form['repository']['name']
    is_secure = any(
        sha256(
            '{}/{}{}'.format(organization, repo_name, token)
        ).hexdigest() == auth_header
        for token in user_tokens.itervalues()
    )
    return is_secure
