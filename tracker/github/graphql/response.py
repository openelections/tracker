class Response:

    def __init__(self, data):
        self.raw_data = data['data']
        self.repos = Repositories(self.raw_data['organization']['repositories'])

    @property
    def org(self):
        return self.raw_data['organization']['name']

    @property
    def rate_limit(self):
        return self.raw_data['rateLimit']


class Repositories:

    def __init__(self, data):
        self.data = data['edges']
        self.page_info = data['pageInfo']

    def __iter__(self):
        for r in self.data:
            yield Repo(r)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return Repo(self.data[key])

    @property
    def count(self):
        return self.__len__()

    @property
    def has_next_page(self):
        return self.page_info['hasNextPage']

    @property
    def end_cursor(self):
        return self.page_info.get('endCursor')


class Repo:

    def __init__(self, data):
        self.data = data['node']
        self.name = self.data['name']
        self.url = self.data['url']
        self.open_issues_count = self.data['issues']['totalCount']

    def __repr__(self):
        return '<Repo: {}>'.format(self.name)

    @property
    def issues(self):
        # Return memoized issues if exists
        try:
            return self._issues
        except AttributeError:
            # Create issues attribute and memoize
            try:
                issues = Issues(self.data['issues']['nodes'])
                self._issues = issues
                return self._issues
            except KeyError:
                # Return an empty array
                return []


class Issues:

    def __init__(self, data):
        self.data = data['edges']
        self.page_info = data['pageInfo']

    def __iter__(self):
        for i in self.data:
            yield Issue(i)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        return Issue(self.data[key])

class Issue:

    def __init__(self, data):
        self.data = data['node']
        self.number = self.data['number']
        self.title = self.data['title']
        self.url = self.data['url']
        self.author = self.data['author']['login']
        self.comments_count = self.data['comments']['totalCount']

    def __repr__(self):
        return '<Issue {}>'.format(self.number)

    @property
    def created_at(self):
        return self.data['createdAt']

    @property
    def labels(self):
        return [node['name'] for node in self.data['labels']['nodes']]

    @property
    def assignees(self):
        return [node['login'] for node in self.data['assignees']['nodes']]
