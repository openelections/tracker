import os

import pytest

from tracker import cli
import logging


@pytest.mark.vcr(filter_headers=['authorization'])
def test_repos_data(caplog, mocker, tmpdir):
    # Enable below to view vcrpy debug logging
    caplog.set_level(logging.INFO)
    outfile = os.path.join(tmpdir.strpath, 'repos.csv')
    parsed_args = {
        'repos_report': True,
        'outdir': tmpdir.strpath,
        'publish': False
    }
    mock = mocker.patch(
        'tracker.cli.get_parsed_args',
        return_value=parsed_args,
        autospec=True,
    )
    cli.main()
    with open(outfile) as f:
        # line count includes header
        assert len(f.readlines()) == 120
