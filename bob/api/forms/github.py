from __future__ import unicode_literals

import pilo


class GithubForm(pilo.Form):

    commit = pilo.fields.String('ref')

    @commit.filter
    def commit(self, value):
        if 'refs/tags' not in value:
            return pilo.NONE
        return value

    name = pilo.fields.String('repository.name')

    organization = pilo.fields.String('repository.organization')

    build = pilo.fields.Boolean(default=False)
