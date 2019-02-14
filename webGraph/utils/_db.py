from ._data_structures import get_host_from_url, remove_protocol_from_url
from ._graph import GraphDB
from ._set_store import SetStoreDB
from contextlib import contextmanager

class DB:
    graph = None
    set_store = None

    def __init__(self):
        self._init_graph()
        self._init_set_store()

    def _init_graph(self):
        self.graph = GraphDB()

    def _init_set_store(self):
        self.set_store = SetStoreDB()

    def dump_links(self, web_page):
        if not self.graph.exists_web_page_by_host(web_page.host):
            self.graph.create_web_page_by_host(web_page.host)
        for link in web_page.links:
            link_host = get_host_from_url(link)
            if not self.graph.exists_web_page_by_host(link_host):
                self.graph.create_web_page_by_host(link_host)
            if not self.graph.exists_link_relationship(web_page.host, link_host):
                self.graph.create_link_relationship(web_page.host, link_host)
        self.set_store.add_url(web_page.url_without_protocol)

    def get_unstudied_urls(self, urls):
        unstudied_urls = []
        for url in urls:
            if not self.has_url_studied(url):
                unstudied_urls.append(url)
        return unstudied_urls

    def has_url_studied(self, url):
        clean_url = remove_protocol_from_url(url)
        return self.set_store.exists_url(clean_url)

    def close(self):
        self.graph.close()


@contextmanager
def open_db():
    db = DB()
    try:
        yield db
    finally:
        db.close()
