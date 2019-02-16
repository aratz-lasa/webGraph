from bs4 import BeautifulSoup as bs
from ..utils._crawler_util import CrawlerUtil
from ..utils._data_structures import WebPage, Url
from .flask_test_server import *


def test_crawler_put_urls_to_link():
    crawler_util, web_page = CrawlerUtil(), WebPage(url=url)
    crawler_util.web_page = web_page
    crawler_util.absolute_urls = absolute_urls
    assert not web_page.links
    crawler_util.prepare_put_links_to_web_page()
    assert set(crawler_util.absolute_urls) == set(web_page.links)


def test_crawler_filter_urls():
    crawler_util = CrawlerUtil()
    crawler_util.buffer_urls = urls
    crawler_util.filter_urls()
    assert crawler_util.absolute_urls == absolute_urls


def test_analyze_soup():
    crawler_util = CrawlerUtil()
    crawler_util.soup = bs(html, "html.parser")
    crawler_util.analyze_soup()
    assert set(crawler_util.buffer_urls) == set(urls)


def test_create_soup():
    crawler_util, web_page = CrawlerUtil(), WebPage(url=url, html=html)
    crawler_util.web_page = web_page
    soup = bs(html, "html.parser")
    crawler_util.create_soup()
    assert crawler_util.soup == soup


def test_fill_with_links():
    crawler_util, web_page = CrawlerUtil(), WebPage(url=url, html=html)
    crawler_util.fill_links(web_page)
    assert set(web_page.links) == set(map(lambda x: Url(x), absolute_urls))
