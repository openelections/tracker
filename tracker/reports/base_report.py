import csv
import pathlib
import os
import sys

import botocore
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
        try:
            session = boto3.Session(profile_name='openelex')
            s3 = session.resource('s3')
        except botocore.exceptions.ProfileNotFound:
            s3 = boto3.resource('s3')
        try:
            bucket = 'openelections-tracker'
            obj_key  = os.path.basename(outfile)
            s3_url = "https://s3.amazonaws.com/{}/{}".format(bucket, obj_key)
            obj = s3.Object(bucket, obj_key)
            obj.upload_file(outfile, ExtraArgs={'ACL':'public-read'})
            print("Published to {}".format(s3_url))
        except (botocore.exceptions.ClientError, boto3.exceptions.S3UploadFailedError):
            msg = "ERROR: Failed to upload file to S3 (access denied)!\nPlease ensure you do one of the following:\n" \
            "\t* Create an AWS credentials profile called 'openelex'\n" \
            "\t* Set your default credentials to those for OpenElections\n" \
            "\t* Supply AWS_PROFILE=<profile_name> env variable when involking --publish\n" \
            "For more details, see http://boto3.readthedocs.io/en/latest/guide/configuration.html#shared-credentials-file"
            sys.exit(msg)

    def _prepare_data(self, data):
        "Customize data in subclasses as necessary"
        return data

    def _headers(self, data):
        "Customize headers in subclasss or default to keys from first data row"
        return data[0].keys()

