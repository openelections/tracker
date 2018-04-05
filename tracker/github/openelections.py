import re

from github3 import GitHub
from .graphql_query import GraphqlQuery


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
                'open_issues': repo.open_issues_count,
                'url': repo.url,
            }
            match = re.search(r'openelections-(sources|data|results)-(\w{2})$', repo.name)
            if match:
                repo_type, state = match.groups()
                payload.update({'repo_type': repo_type, 'state': state.upper()})
            repos.append(payload)
        return repos

    def issues_report(self):
        issues = []
        for repo in self.repos():
            for issue in repo.issues:
                issues.append({
                    'repo': repo.name,
                    'number': issue.number,
                    'title': issue.title,
                    'assignee': ','.join(issue.assignees),
                    'url': issue.url,
                    'created_date': issue.created_at.strftime("%Y-%m-%d"),
                    'created_by': issue.author,
                    'labels': ','.join(issue.labels),
                })
        return issues

    def repos(self):
        query = GraphqlQuery()
        repos = query.run()
        return repos
