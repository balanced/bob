from __future__ import unicode_literals

import pilo


class TravisRepoForm(pilo.Form):

    name = pilo.fields.String()

    owner_name = pilo.fields.String()


class TravisForm(pilo.Form):

    repository = pilo.fields.SubForm(TravisRepoForm)
