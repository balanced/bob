from __future__ import unicode_literals

import pilo


class TravisRepoForm(pilo.Form):

    name = pilo.fields.String()

    organization = pilo.fields.String('owner_name')


class TravisForm(pilo.Form):

    commit = pilo.fields.String()

    repository = pilo.fields.SubForm(TravisRepoForm)
