from __future__ import unicode_literals
import json
import os


def get_for_reals_path(file_name):
    return os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        file_name
    )


def load_json(path):
    with open(path) as f:
        return json.load(f)
