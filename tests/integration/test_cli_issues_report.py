import os

import pytest

from tracker import cli
import logging


@pytest.mark.vcr(filter_headers=['authorization'])
def test_issues_data(caplog, mocker, tmpdir):
    # Enable below to view vcrpy debug logging
    caplog.set_level(logging.INFO)
    outfile = os.path.join(tmpdir.strpath, 'issues.csv')
    parsed_args = {
        'issues_report': True,
        'outdir': tmpdir.strpath,
        'publish': False
    }
    mocker.patch(
        'tracker.cli.get_parsed_args',
        return_value=parsed_args,
        autospec=True,
    )
    cli.main()
    with open(outfile) as f:
        assert len(f.readlines()) == 274
