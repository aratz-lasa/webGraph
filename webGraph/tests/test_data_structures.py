from ..utils._data_structures import HTTPRequest, get_name_from_host, \
    get_path_from_url, get_host_from_url, uses_ssl_url
url_with_ssl = "https://www.google.com/search"
url_without_ssl = "http://www.google.com/search"
host = "www.google.com"
path = "/search"
name = "google"


def test_load_from_url():
    ssl_request = HTTPRequest()
    ssl_request.load_from_url(url_with_ssl)
    assert ssl_request.host == host
    assert ssl_request.path == path
    assert ssl_request.ssl == True

    no_ssl_request = HTTPRequest()
    no_ssl_request.load_from_url(url_without_ssl)
    assert no_ssl_request.host == host
    assert no_ssl_request.path == path
    assert no_ssl_request.ssl == False

def test_get_host_from_url():
    assert get_host_from_url(url_with_ssl) == host

def test_get_path_from_url():
    assert get_path_from_url(url_with_ssl) == path

def test_uses_ssl_url():
    assert uses_ssl_url(url_with_ssl)
    assert not uses_ssl_url(url_without_ssl)

def test_get_name_from_host():
    assert get_name_from_host(host) == name