import pytest
from betamax import Betamax

from tracker.github.graphql import ReposQuery


def test_repos_query_basic():
    query = ReposQuery()
    with Betamax(query.session).use_cassette('repos-query'):
        repos = query.run()
        assert len(repos) == 119
