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

    def issues_report(self):
        issues = []
        counter = 0
        for repo in self.repos():
            if counter == 3:
                break
            for issue in repo.issues():
                issues.append({
                    'repo': repo.name,
                    'title': issue.title,
                    'assignee': issue.assignee,
                    'url': issue.html_url,
                    'created_date': issue.created_at.strftime("%Y-%m-%d"),
                    'created_by': issue.user.login,
                    'creator_gh_page': issue.user.html_url,
                    'labels': ','.join([label.name for label in issue.labels()]),
                    #'body': issue.body,
                })
        return issues

    def repos(self,):
        return [repo for repo in self.openelex.repositories()]

