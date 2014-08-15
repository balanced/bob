from __future__ import unicode_literals

import pilo


class GithubRepoForm(pilo.Form):

    name = pilo.fields.String()

    organization = pilo.fields.String()


class GithubForm(pilo.Form):

    commit = pilo.fields.String('ref')

    @commit.filter
    def commit(self, value):
        if 'refs/tags' not in value:
            return pilo.NONE
        return value

    repository = pilo.fields.SubForm(GithubRepoForm)

    build = pilo.fields.Boolean(default=False)
