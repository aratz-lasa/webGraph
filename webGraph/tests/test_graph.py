from ..utils._graph_util import GraphDB, open_graph
from ..utils._data_structures import WebPage



web_page_host = "google.com"
link_host = "yahoo.com"


def test_graph_connection():
    GraphDB()

def test_create_web_page():
    with open_graph() as graph:
        graph.create_web_page_by_host(web_page_host)
        assert graph.exists_web_page(web_page_host)
        clean_web_pages(graph, [web_page_host])

def test_create_link_relationship():
    with open_graph() as graph:
        graph.create_web_page_by_host(web_page_host)
        graph.create_web_page_by_host(link_host)
        graph.create_link_relationship(web_page_host, link_host)
        assert graph.exists_link_relationship(web_page_host, link_host)
        clean_web_pages(graph, [web_page_host, link_host])

def clean_web_pages(graph, hosts):
    for host in hosts:
        graph.delete_web_page_by_host(host)