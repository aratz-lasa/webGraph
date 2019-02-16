from contextlib import contextmanager
from neo4j import GraphDatabase
import os

from ._abc import GraphABC
from ._data_structures import get_name_from_host
from ..settings import settings # used for executing load_dotenv()

GRAPH_USER = os.getenv("NEO4J_USER")
GRAPH_PASSWORD = os.getenv("NEO4J_PASSWORD")
GRAPH_URL = os.getenv("NEO4J_URL")


class Neo4jDB(GraphABC):

    def __init__(self):
        self._init_db()

    def _init_db(self):
        self._driver = GraphDatabase.driver(GRAPH_URL, auth=(GRAPH_USER, GRAPH_PASSWORD))

    def create_short_uri_node(self, short_uri):
        self._write_transaction(self._create_short_uri_by_host, short_uri.host)

    def create_link_relationship(self, from_short_uri, to_short_uri):
        self._write_transaction(self._create_link_relationship_by_host, from_short_uri.host, to_short_uri.host)

    def delete_short_uri_node(self, short_uri):
        self._write_transaction(self._delete_short_uri_by_host, short_uri.host)

    def exists_short_uri_node(self, short_uri):
        return self._read_transaction(self._exists_short_uri_by_host, short_uri.host)

    def exists_link_relationship(self, from_short_uri, to_short_uri):
        return self._read_transaction(self._exists_link_relationship_by_host, from_short_uri.host, to_short_uri.host)

    def _create_short_uri_by_host(self, tx, host):
        # parameter host instead of web_page because it is also used for links
        tx.run(
            "CREATE (a:WebPage {name:$name, host: $host}) ",
            host=host, name=get_name_from_host(host)
        )

    def _create_link_relationship_by_host(self, tx, from_host, to_host):
        tx.run(
            "MATCH(from), (to) where from.host=$from_host and to.host=$to_host CREATE (from)-[:LinksTo]->(to)",
            from_host=from_host, to_host=to_host
        )

    def _delete_short_uri_by_host(self, tx, host):
        tx.run(
            "MATCH(web_page) WHERE web_page.host=$host DETACH DELETE web_page",
            host=host
        )

    def _exists_link_relationship_by_host(self, tx, from_host, to_host):
        record = tx.run("MATCH (from:WebPage), (to:WebPage) WHERE from.host=$from_host "
                        "AND to.host=$to_host AND (from)-[:LinksTo]->(to) RETURN from, to",
                        from_host=from_host, to_host=to_host)
        return bool(record.value())  # record.value() returns a list with all matched nodes

    def _exists_short_uri_by_host(self, tx, host):
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
def open_graph(GraphClass=Neo4jDB):
    graph = GraphClass()
    try:
        yield graph
    finally:
        graph.close()
