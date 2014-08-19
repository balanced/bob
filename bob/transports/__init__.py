from __future__ import unicode_literals
import os
import boto

from bob.builders.ubuntu import UbuntuBuilder


class Uploader(object):

    def __init__(self, builder):
        self.builder = builder

    def upload(self, path_to_file, **options):
        raise NotImplementedError()


@UbuntuBuilder.register_transport('s3')
class BotoS3Uploader(Uploader):

    def upload(self, path_to_file, destination=None, **_):
        conn = boto.connect_s3()
        bucket = conn.get_bucket(destination)
        file_name = os.path.basename(path_to_file)
        key = bucket.get_key(file_name)
        if not key:
            key = bucket.new_key(file_name)
        key.set_contents_from_file(path_to_file)


@UbuntuBuilder.register_transport('depot')
class DepotUploader(Uploader):

    def upload(self, path_to_file, **options):
        self.builder.run_command(
            '''
            depot -s {destination} -c {codename} -k {gpg_key} \
                --component={component} --no-public --force \
                {target}
            '''.format(
                target=path_to_file,
                **options
            )
        )
