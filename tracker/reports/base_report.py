import csv
import pathlib
import os

import boto3

from tracker.utils import camel_to_snakecase

class BaseReport:

    custom_name = None

    def __init__(self, outdir, data):
        self.outdir = outdir
        self.outfile = os.path.join(outdir, self.name)
        self.data = self._prepare_data(data)
        self.headers = self._headers(self.data)

    @property
    def name(self):
        base_name = self.custom_name or camel_to_snakecase(self.__class__.__name__)
        return "{}.csv".format(base_name)

    def write(self, publish=False):
        pathlib.Path(self.outdir).mkdir(parents=True, exist_ok=True)
        with open(self.outfile, 'w') as csvfile:
            print("Data written to {}".format(self.outfile))
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)
        if publish:
            self.publish(self.outfile)

    def publish(self, outfile):
        bucket = 'openelections-tracker'
        obj_key  = os.path.basename(outfile)
        print("Publishing to S3: {}".format(outfile))
        s3 = boto3.resource('s3')
        extra_args = {'ACL':'public-read'}
        data = open(outfile, 'rb')
        s3.Bucket(bucket).put_object(Key=obj_key, Body=data)
        object_acl = s3.ObjectAcl(bucket, obj_key)
        object_acl.put(ACL='public-read')

    def _prepare_data(self, data):
        "Customize data in subclasses as necessary"
        return data

    def _headers(self, data):
        "Customize headers in subclasss or default to keys from first data row"
        return data[0].keys()

