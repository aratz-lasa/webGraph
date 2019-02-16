from ..utils._db import DB, open_db
from ..utils._data_structures import WebPage, Url, remove_protocol_from_url, get_host_from_url

web_page_url = "aratz.eus/"
link_url = Url("https://ama.eus", )


def test_db_connection():
    DB()


def test_dump_links():
    with open_db() as db:
        web_page = WebPage(url=web_page_url, links=[link_url])
        db.dump_links(web_page)
        assert db.graph.exists_link_relationship(web_page, link_url)
        assert db.set_store.exists_short_uri_entry(web_page)

        db.graph.delete_short_uri_node(web_page)
        db.graph.delete_short_uri_node(link_url)
        db.set_store.delete_short_uri_entry(web_page)
        assert not db.graph.exists_short_uri_node(web_page)
        assert not db.graph.exists_short_uri_node(link_url)
        assert not db.set_store.exists_short_uri_entry(web_page)


def test_get_unstudied_urls():
    with open_db() as db:
        web_page = WebPage(url=web_page_url, links=[link_url])
        assert not db.set_store.exists_short_uri_entry(link_url)
        assert set([link_url]) == set(db.get_unstudied_urls(web_page.links))

        db.set_store.add_short_uri_entry(link_url)
        assert db.set_store.exists_short_uri_entry(link_url)
        assert set([]) == set(db.get_unstudied_urls(web_page.links))

        db.set_store.delete_short_uri_entry(link_url)
        assert not db.set_store.exists_short_uri_entry(link_url)

