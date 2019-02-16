import attr
import re
from ._http_util import HTTP_URL_REGEX
from ._data_structures import Url

from bs4 import BeautifulSoup as bs

@attr.s(repr=False, hash=False, cmp=False)
class CrawlerUtil:
    absolute_urls = attr.ib(default=attr.Factory(list))
    buffer_urls = attr.ib(default=attr.Factory(list))
    web_page = attr.ib(default=None)
    soup = attr.ib(default=None)

    def fill_links(self, web_page):
        self.web_page = web_page
        self.create_soup()
        self.analyze_soup()
        self.prepare_put_links_to_web_page()
        self.reset()

    def create_soup(self):
        self.soup = bs(self.web_page.html, 'html.parser')

    def analyze_soup(self):
        self.extract_urls()

    def prepare_put_links_to_web_page(self):
        self.filter_urls()
        self.cast_urls()
        self.web_page.links = self.absolute_urls[:]

    def extract_urls(self):
        for link in self.soup.find_all('a'):
            self.buffer_urls.append(link.get('href'))

    def cast_urls(self):
        buffer_urls = []
        for url in self.absolute_urls:
            buffer_urls.append(Url(url))
        self.absolute_urls = buffer_urls

    def filter_urls(self):
        for url in self.buffer_urls:
            if url and re.match(HTTP_URL_REGEX, url):  # if it is None no append
                self.absolute_urls.append(url)

    def reset(self):
        self.absolute_urls.clear()
        self.buffer_urls.clear()
        self.web_page = None
        self.soup = None
