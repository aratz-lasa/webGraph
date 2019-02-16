from ..utils._set_store import open_set_store
from ..utils._data_structures import Url


url = Url("google.com")


def test_connect_set_store():
    with open_set_store() as set_store:
        pass


def test_add_url():
    with open_set_store() as set_store:
        set_store.add_short_uri_entry(url)
        assert set_store.exists_short_uri_entry(url)
        clean_set_urls(set_store, [url])


def test_delete_url():
    with open_set_store() as set_store:
        set_store.add_short_uri_entry(url)
        assert set_store.exists_short_uri_entry(url)
        set_store.delete_short_uri_entry(url)
        assert not set_store.exists_short_uri_entry(url)


def clean_set_urls(set_store, urls):
    for url in urls:
        set_store.delete_short_uri_entry(url)
