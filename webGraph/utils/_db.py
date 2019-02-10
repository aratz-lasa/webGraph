from ._graph_util import GraphDB

class DB:
    graph = None
    key_value_store = None

    def __init__(self):
        self.init_graph()
        self.init_key_value_store()

    def init_graph(self):
        self.graph = GraphDB()

    def init_key_value_store(self):
        pass

    def dump_links(self, web_page):
        self.graph.dump_links(web_page)