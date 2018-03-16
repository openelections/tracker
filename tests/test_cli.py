import pytest

from tracker import cli


def test_github_token_warning(capsys, monkeypatch):
    "Ensures Github access env var is set"
    monkeypatch.delenv('GITHUB_PERSONAL_ACCESS_TOKEN')
    with pytest.raises(SystemExit):
        cli.main()
    out, err = capsys.readouterr()
    assert 'You must create a Github personal access token' in out
