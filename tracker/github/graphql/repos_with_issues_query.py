from .base_query import BaseQuery


class ReposWithIssuesQuery(BaseQuery):

    gql_initial_qry = 'repos_with_issues'
    gql_next_qry = 'repos_with_issues_next_page'
