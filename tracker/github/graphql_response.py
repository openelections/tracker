class Repo:

    def __init__(self, data):
        self.data = data['node']
        self.name = self.data['name']
        self.url = self.data['url']
        self.open_issues = self.data['issues']['totalCount']

    def __repr__(self):
        return '<Repo: {}>'.format(self.name)

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


class GraphqlResponse:

    def __init__(self, data):
        self.raw_data = data['data']
        self.repos = Repositories(self.raw_data['organization']['repositories'])

    # TODO: create an iterable method that lets you page through the
    # data, using recursion/generator to make calls, as necessary?

    @property
    def org(self):
        return self.raw_data['organization']['name']

    @property
    def rate_limit(self):
        return self.raw_data['rateLimit']
