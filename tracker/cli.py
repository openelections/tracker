import argparse
import csv
import os
import pathlib
import sys

from tracker.github.openelections import OpenElections
from tracker import reports


def main():
    parser = get_parser()
    parsed = parser.parse_args()
    openelex = OpenElections()
    for cmd, status in vars(parsed).items():
        if is_report(cmd) and status == True:
            print("Running --{}...".format(cmd.replace('_','-')))
            data = getattr(openelex, cmd)()
            report_kls = get_report_kls(cmd)
            report = report_kls(parsed.outdir, data)
            report.write()

def get_parser():
    parser = argparse.ArgumentParser(
        description='Generate raw material for stats on OpenElections.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--repos-report',
        action='store_true',
        help='Generate CSV of all OpenElex repos'
    )
    parser.add_argument('--tickets-report',
        action='store_true',
        help='Generate CSV of OpenElex tickets'
    )
    parser.add_argument('--outdir',
        default='/tmp/openelections/tracker',
        help='Output directory where CSVs or reports will be written'
    )
    return parser

def is_report(cmd):
    return 'report' in cmd

def get_report_kls(cmd):
    report_name = cmd.split('_')[0].title()
    return getattr(reports, report_name)


if __name__ == '__main__':
    main()
