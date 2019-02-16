from ..utils._data_structures import Url, WebPage, get_name_from_host, \
    get_path_from_url, get_host_from_url, uses_ssl_url, remove_protocol_from_url
url_with_ssl = "https://www.google.com/search"
url_without_ssl = "http://www.google.com/search"
host = "www.google.com"
path = "/search"
name = "google"
short_uri = host + path


def test_get_host_from_url():
    assert get_host_from_url(url_with_ssl) == host


def test_get_path_from_url():
    assert get_path_from_url(url_with_ssl) == path


def test_get_name_from_host():
    assert get_name_from_host(host) == name


def test_remove_protocol_from_url():
    assert remove_protocol_from_url(url_with_ssl) == short_uri


def test_short_uri():
    web_page = WebPage(url_with_ssl)
    assert web_page.short_uri == host + path


def test_url():
    http_request = Url(url_with_ssl)
    assert http_request.url == "https://" + host + path
    http_request.ssl = False
    assert http_request.url == "http://" + host + path


def test_eq():
    url1 = Url(url=url_with_ssl)
    url2 = Url(url=url_with_ssl)
    assert url1 == url2
    url2.host = "yammi.com"
    assert not url1 == url2

    wb1 = WebPage(url=url_with_ssl)
    wb2 = WebPage(url=url_with_ssl)
    assert wb1 == wb2

    wb2.host = "yammi.com"
    assert not wb1 == wb2
