import pytest

from tracker.github.graphql import ReposQuery


@pytest.mark.vcr(filter_headers=['authorization'])
def test_repos_query_basic():
    query = ReposQuery()
    repos = query.run()
    assert len(repos) == 119
