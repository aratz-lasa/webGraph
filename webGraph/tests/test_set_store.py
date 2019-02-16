from ..utils._set_store import SetStoreDB
from ..utils._data_structures import Url


url = Url("google.com")


def test_connect_set_store():
    SetStoreDB()


def test_add_url():
    set_store = SetStoreDB()
    set_store.add_short_uri(url)
    assert set_store.exists_short_uri(url)
    clean_set_urls(set_store, [url])


def test_delete_url():
    set_store = SetStoreDB()
    set_store.add_short_uri(url)
    assert set_store.exists_short_uri(url)
    set_store.delete_short_uri(url)
    assert not set_store.exists_short_uri(url)


def clean_set_urls(set_store, urls):
    for url in urls:
        set_store.delete_short_uri(url)
