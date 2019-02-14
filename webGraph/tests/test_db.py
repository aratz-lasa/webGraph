from ..utils._db import DB, open_db
from ..utils._data_structures import WebPage, remove_protocol_from_url, get_host_from_url

web_page_host = "aratz.eus"
web_page_path = "/"
link_url = "https://ama.eus"


def test_db_connection():
    DB()


def test_dump_links():
    link_host = get_host_from_url(link_url)
    with open_db() as db:
        web_page = WebPage(host=web_page_host, path=web_page_path, links=[link_url])
        db.dump_links(web_page)
        assert db.graph.exists_link_relationship(web_page.host, link_host)
        assert db.set_store.exists_url(web_page.url_without_protocol)

        db.graph.delete_web_page_by_host(web_page.host)
        db.graph.delete_web_page_by_host(link_host)
        db.set_store.delete_url(web_page.url_without_protocol)
        assert not db.graph.exists_web_page_by_host(web_page.host)
        assert not db.graph.exists_web_page_by_host(link_host)
        assert not db.set_store.exists_url(web_page.url_without_protocol)


def test_get_unstudied_urls():
    link_clean_url = remove_protocol_from_url(link_url)
    with open_db() as db:
        web_page = WebPage(host=web_page_host, path=web_page_path, links=[link_url])
        assert not db.set_store.exists_url(link_clean_url)
        assert set([link_url]) == set(db.get_unstudied_urls(web_page.links))

        db.set_store.add_url(link_clean_url)
        assert db.set_store.exists_url(link_clean_url)
        assert set([]) == set(db.get_unstudied_urls(web_page.links))

        db.set_store.delete_url(link_clean_url)
        assert not db.set_store.exists_url(link_clean_url)

