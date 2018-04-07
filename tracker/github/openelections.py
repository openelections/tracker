import datetime
import re

from github3 import GitHub
from .graphql import ReposQuery, ReposWithIssuesQuery


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
                'repo_name': repo.name,
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
        for repo in self.repos_with_issues():
            for issue in repo.issues:
                payload = {
                    'state': '',
                    'repo_type': '',
                    'repo_name': repo.name,
                    'number': issue.number,
                    'title': issue.title,
                    'assignee': ','.join(issue.assignees),
                    'url': issue.url,
                    'created_date': self._simple_date(issue.created_at),
                    'created_by': issue.author,
                    'labels': ','.join(issue.labels),
                }
                match = re.search(r'openelections-(sources|data|results)-(\w{2})$', repo.name)
                if match:
                    repo_type, state = match.groups()
                    payload.update({'repo_type': repo_type, 'state': state.upper()})
                issues.append(payload)
        return issues

    def repos(self):
        query = ReposQuery()
        repos = query.run()
        return repos

    def repos_with_issues(self):
        query = ReposWithIssuesQuery()
        repos = query.run()
        return repos

    def _simple_date(self, date_str):
        return datetime.datetime\
                .strptime(date_str,"%Y-%m-%dT%H:%M:%SZ")\
                .strftime("%Y-%m-%d")
