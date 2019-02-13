from ..utils._set_store import SetStoreDB


url = "google.com"


def test_connect_set_store():
    SetStoreDB()


def test_add_url():
    set_store = SetStoreDB()
    set_store.add_url(url)
    assert set_store.exists_url(url)
    clean_set_urls(set_store, [url])


def test_delete_url():
    set_store = SetStoreDB()
    set_store.add_url(url)
    assert set_store.exists_url(url)
    set_store.delete_url(url)
    assert not set_store.exists_url(url)


def clean_set_urls(set_store, urls):
    for url in urls:
        set_store.delete_url(url)
