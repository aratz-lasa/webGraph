from contextlib import contextmanager

from ._graph import Neo4jDB
from ._set_store import RedisDB
from ..log.log import db_logger as logger


class DB:

    def __init__(self):
        self._init_graph()
        self._init_set_store()

    def _init_graph(self):
        self.graph = Neo4jDB()

    def _init_set_store(self):
        self.set_store = RedisDB()

    def dump_links(self, web_page):
        for link in web_page.links:
            if self.graph.exists_link_relationship(web_page, link):
                continue
            if not self.graph.exists_short_uri_node(web_page):
                self.graph.create_short_uri_node(web_page)
            if not self.graph.exists_short_uri_node(link):
                self.graph.create_short_uri_node(link)
            self.graph.create_link_relationship(web_page, link)
        self.set_store.add_short_uri_entry(web_page)

    def get_unstudied_urls(self, urls):
        logger.debug("Filtering unstudied urls...")
        unstudied_urls = []
        for url in urls:
            if not self.set_store.exists_short_uri_entry(url):
                logger.debug("Added {} to unstudied urls".format(url.short_uri))
                unstudied_urls.append(url)
        return unstudied_urls

    def close(self):
        self.graph.close()
        self.set_store.close()


@contextmanager
def open_db():
    db = DB()
    try:
        yield db
    finally:
        db.close()
