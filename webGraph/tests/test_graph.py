from ..utils._graph import Neo4jDB, open_graph
from ..utils._data_structures import WebPage, Url


web_page_url = WebPage(url="aratz.eus")
link_url = Url("ama.eus")


def test_graph_connection():
    with open_graph() as graph:
        pass


def test_create_web_page():
    with open_graph() as graph:
        graph.create_short_uri_node(web_page_url)
        assert graph.exists_short_uri_node(web_page_url)
        clean_web_pages(graph, [web_page_url])


def test_create_link_relationship():
    with open_graph() as graph:
        graph.create_short_uri_node(web_page_url)
        graph.create_short_uri_node(link_url)
        graph.create_link_relationship(web_page_url, link_url)
        assert graph.exists_link_relationship(web_page_url, link_url)
        clean_web_pages(graph, [web_page_url, link_url])


def test_delete_web_page_by_host():
    with open_graph() as graph:
        graph.create_short_uri_node(web_page_url)
        assert graph.exists_short_uri_node(web_page_url)
        graph.delete_short_uri_node(web_page_url)
        assert not graph.exists_short_uri_node(web_page_url)


def clean_web_pages(graph, hosts):
    for host in hosts:
        graph.delete_short_uri_node(host)
