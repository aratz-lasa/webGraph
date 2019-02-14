from ..utils._data_structures import HTTPRequest, WebPage, get_name_from_host, \
    get_path_from_url, get_host_from_url, uses_ssl_url, remove_protocol_from_url
url_with_ssl = "https://www.google.com/search"
url_without_ssl = "http://www.google.com/search"
host = "www.google.com"
path = "/search"
name = "google"
url = host+path


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


def test_get_name_from_host():
    assert get_name_from_host(host) == name


def test_remove_protocol_from_url():
    assert remove_protocol_from_url(url_with_ssl) == url


def test_url_without_protocol():
    web_page = WebPage()
    web_page.host = host
    web_page.path = path
    assert web_page.url_without_protocol == host + path


def test_url():
    http_request = HTTPRequest()
    http_request.host = host
    http_request.path = path
    http_request.ssl = True
    assert http_request.url == "https://" + host + path
    http_request.ssl = False
    assert http_request.url == "http://" + host + path
