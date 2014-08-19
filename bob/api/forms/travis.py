from __future__ import unicode_literals
from hashlib import sha256

import semantic_version
import pilo


user_tokens = {
    'mjallday': 'irgy9pphBTydWzVYskRq'
}


class TravisForm(pilo.Form):

    commit = pilo.fields.String()

    success = pilo.fields.String('result_message')

    name = pilo.fields.String('repository.name')

    organization = pilo.fields.String('repository.owner_name')

    branch = pilo.fields.String()

    @success.munge
    def success(self, value):
        return value in ('Passed', 'Fixed')

    build = pilo.fields.Boolean(default=False)

    @build.compute
    def build(self):
        # branch is the tag on travis. since the tag should look like 1.0.0
        # we can check if it is parseable as a semver to decide if this test
        # run was for a build (tag) or a commit. on tag we can say build = True
        # if the tests passed
        commit = self['branch']
        if commit and commit[0] == 'v':
            commit = commit[1:]
        try:
            semantic_version.Version(commit)
        except ValueError:
            return False
        else:
            return self['success']


def compute_travis_security(headers, form):
    auth_header = headers['Authorization']
    organization = form['organization']
    repo_name = form['name']
    is_secure = any(
        sha256(
            '{}/{}{}'.format(organization, repo_name, token)
        ).hexdigest() == auth_header
        for token in user_tokens.itervalues()
    )
    return is_secure
