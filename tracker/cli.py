import argparse
import csv
import os
import pathlib
import sys

from tracker.github.openelections import OpenElections
from tracker.reports.base_report  import BaseReport


def main():
    try:
        gh_token = os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']
    except KeyError:
        err_msg = "You must create a Github personal access token and "\
        "store it in the env variable GITHUB_PERSONAL_ACCESS_TOKEN"
        print(err_msg)
        sys.exit()

    parser = argparse.ArgumentParser(description='Generate raw material for stats on OpenElections.')
    parser.add_argument('--compile-repos',
        action='store_true',
        help='Generate CSV of all OpenElex repos'
    )
    #parser.add_argument('--compile-data-files',
    #    action='store_true',
    #    help='Generate CSV of all data files in soure|data repos'
    #)
    parsed = parser.parse_args()
    openelex = OpenElections(gh_token)
    for cmd, status in vars(parsed).items():
        if status == True:
            print("Running --{}...".format(cmd.replace('_','-')))
            data = getattr(openelex, cmd)()
            # TODO: lookup appropriate report
            outfile = '/tmp/openelex/tracker/repos.csv'
            report = BaseReport(outfile, data)
            report.write()

if __name__ == '__main__':
    main()
