import attr


@attr.s(cmp=False, hash=False, repr=False)
class SetStoreDB:
    set_store = attr.ib(default=None)

    def __init__(self):
        self.init_db()


    def init_db(self):
        # TODO: connect to redis
        # read from .env file the environment settings for neo4j
        # connect to redis
        pass

    def add_url(self):
        pass

    def is_url_added(self, url):
        pass