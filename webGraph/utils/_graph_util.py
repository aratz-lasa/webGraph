from contextlib import contextmanager
from neo4j import GraphDatabase

from ._data_structures import get_name_from_host


class GraphDB:

    def __init__(self):
        self.init_db()

    def init_db(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "neo4j"))
        # read from .env file the environment settings for neo4j
        # connect to neo4j

    def create_web_page_by_host(self, host):
        self._write_transaction(self._create_web_page_by_host, host)
        # write links

    def create_link_relationship(self, from_host, to_host):
        self._write_transaction(self._create_link_relationship, from_host, to_host)

    def delete_web_page_by_host(self, host):
        self._write_transaction(self._delete_web_page, host)

    def exists_web_page(self, host):
        return self._read_transaction(self._exists_web_page, host)

    def exists_link_relationship(self, from_host, to_host):
        return self._read_transaction(self._exists_link_relationship, from_host, to_host)

    def _create_web_page_by_host(self, tx, host):
        # parameter host instead of web_page because it is also used for links
        tx.run(
            "CREATE (a:WebPage {name:$name, host: $host}) ",
            host=host, name=get_name_from_host(host)
        )

    def _create_link_relationship(self, tx, from_host, to_host):
        tx.run(
            "MATCH(from), (to) where from.host=$from_host and to.host=$to_host CREATE (from)-[:LinksTo]->(to)",
            from_host=from_host, to_host=to_host
        )

    def _delete_web_page(self, tx, host):
        tx.run(
            "MATCH(web_page) WHERE web_page.host=$host DETACH DELETE web_page",
            host=host
        )

    def _exists_link_relationship(self, tx, from_host, to_host):
        record = tx.run("MATCH (from:WebPage), (to:WebPage) WHERE from.host=$from_host "
                        "AND to.host=$to_host AND (from)-[:LinksTo]->(to) RETURN from, to",
                        from_host=from_host, to_host=to_host)
        return bool(record.value())  # record.value() returns a list with all matched nodes

    def _exists_web_page(self, tx, host):
        record = tx.run("MATCH (web_page:WebPage) WHERE web_page.host = $host RETURN web_page", host=host)
        return bool(record.value()) # record.value() returns a list with all matched nodes

    def _write_transaction(self, function, *args):
        with self._driver.session() as session:
            # check if link host exists, if not, create
            session.write_transaction(function, *args)

    def _read_transaction(self, function, *args):
        with self._driver.session() as session:
            # check if link host exists, if not, create
            response = session.read_transaction(function, *args)
        return response

    def close(self):
        self._driver.close()

    def __del__(self):
        self.close()

@contextmanager
def open_graph():
    graph = GraphDB()
    try:
        yield graph
    finally:
        graph.close()