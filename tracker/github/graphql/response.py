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
                issues = Issues(self.data['issues'])
                self._issues = issues
                return self._issues
            except KeyError:
                # Return an empty array
                return []


class Connection:
    """A paged iterable connection-like object intended to wrap the payload for working with edges for a GraphQL type.

    Intended to be subclassed and used as a wrapper for connection data containing
    edges and paging info, as returned by the GraphQL API.

    Subclasses must specify a node_type class variable that will wrap nodes in the list of edges.

    Parameters
    ----------
    data: dict
        Dictionary from a GraphQL connection type


    Example
    --------

    class Repositories(Connection):

        node_type = Repo

    """

    node_type = None

    def __init__(self, data):
        self.edges = data['edges']
        self.page_info = data['pageInfo']

    def __iter__(self):
        for item in self.edges:
            yield self.node_type(item)

    def __len__(self):
        return len(self.edges)

    def __getitem__(self, key):
        return self.node_type(self.edges[key])

    @property
    def count(self):
        return self.__len__()

    @property
    def has_next_page(self):
        return self.page_info['hasNextPage']

    @property
    def end_cursor(self):
        return self.page_info.get('endCursor')


class Repositories(Connection):

    node_type = Repo

class Issues(Connection):

    node_type = Issue
