import os
import requests

from .response import Response as GraphqlResponse


class BaseQuery:

    api_url = 'https://api.github.com/graphql'
    gql_initial_qry = None
    gql_next_qry = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['Authorization'] = 'Bearer {}'.format(self.gh_access_token)

    def run(self):
        raw_response = self.post(self.gql_initial_qry)
        raw_response.raise_for_status()
        current_response = GraphqlResponse(raw_response.json())
        repos = []
        repos.extend(current_response.repos)
        while current_response.repos.has_next_page:
            variables = {
                'reposCursor': current_response.repos.end_cursor
            }
            raw_response = self.post(self.gql_next_qry, variables)
            current_response = GraphqlResponse(raw_response.json())
            for repo in current_response.repos:
                repos.append(repo)
        return repos

    def post(self, query_type, variables={}):
        payload = self.prepare_qry(query_type, variables)
        return self.session.post(self.api_url, json=payload)

    def prepare_qry(self, query_type, variables={}):
        payload = {
            'query': self.get_query(query_type),
            'variables': {}
        }
        payload['variables'].update(variables)
        return payload

    @property
    def gh_access_token(self):
        return os.environ['OPENELEX_GITHUB_ACCESS_TOKEN']

    @property
    def default_vars(self):
        return {
            "reposCursor": "",
            "issuesCursor": "",
            "withIssues": True
        }

    def get_query(self, name):
        dir_path = os.path.dirname(__file__)
        qry_path = os.path.join(dir_path, "queries/{}.qry".format(name))
        with open(qry_path, 'r') as f:
            return f.read()
