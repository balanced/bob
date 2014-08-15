from __future__ import unicode_literals

import pilo


class GithubRepoForm(pilo.Form):

    name = pilo.fields.String()

    organization = pilo.fields.String()


class GithubForm(pilo.Form):

    ref = pilo.fields.String()

    @ref.filter
    def ref(self, value):
        if 'refs/tags' not in value:
            return pilo.NONE
        return value

    repository = pilo.fields.SubForm(GithubRepoForm)
