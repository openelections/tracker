import argparse
import csv
import os
import pathlib
import sys

from tracker.github.openelections import OpenElections
from tracker import reports


def main():
    parsed = get_parsed_args()
    publish_status = parsed.pop('publish')
    outdir = parsed.pop('outdir')
    openelex = OpenElections()
    for cmd, status in parsed.items():
        if is_report(cmd) and status == True:
            print("Running --{}...".format(cmd.replace('_','-')))
            data = getattr(openelex, cmd)()
            report_kls = get_report_kls(cmd)
            report = report_kls(outdir, data)
            report.write(publish_status)

def get_parsed_args():
    parser = argparse.ArgumentParser(
        description='Generate raw material for stats on OpenElections.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--repos-report',
        action='store_true',
        help='Generate CSV of all OpenElex repos'
    )
    parser.add_argument('--issues-report',
        action='store_true',
        help='Generate CSV of OpenElex issues'
    )
    parser.add_argument('--outdir',
        default='/tmp/openelections/tracker',
        help='Output directory where CSVs or reports will be written'
    )
    parser.add_argument('--publish',
        action='store_true',
        help='Publish report to S3'
    )
    return vars(parser.parse_args())

def is_report(cmd):
    return 'report' in cmd

def get_report_kls(cmd):
    report_name = cmd.split('_')[0].title()
    return getattr(reports, report_name)


if __name__ == '__main__':
    main()
