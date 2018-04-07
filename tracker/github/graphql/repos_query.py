from .base_query import BaseQuery


class ReposQuery(BaseQuery):

    gql_initial_qry = 'repos'
    gql_next_qry = 'repos_next_page'
