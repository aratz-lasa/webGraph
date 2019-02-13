from ._graph import GraphDB

class DB:
    graph = None
    set_store = None

    def __init__(self):
        self.init_graph()
        self.init_key_value_store()

    def init_graph(self):
        self.graph = GraphDB()

    def init_set_store(self):
        pass

    def dump_links(self, web_page):
        self.graph.dump_links(web_page)

    def filter_unstudied_urls(self, urls):