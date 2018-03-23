import re

from github3 import GitHub


class OpenElections:

    def __init__(self):
        self.github = GitHub()
        self.openelex = self.github.organization('openelections')

    def repos_report(self):
        repos = []
        for repo in self.repos():
            payload = {
                'state': '',
                'repo_type': '',
                'name': repo.name,
                'url': repo.html_url,
            }
            match = re.search(r'openelections-(sources|data|results)-(\w{2})$', repo.name)
            if match:
                repo_type, state = match.groups()
                payload.update({'repo_type': repo_type, 'state': state.upper()})
            repos.append(payload)
        return repos

    def tickets_report(self):
        tickets = []
        for repo in self.repos():
            pass

    def repos(self,):
        return [repo for repo in self.openelex.repositories()]
