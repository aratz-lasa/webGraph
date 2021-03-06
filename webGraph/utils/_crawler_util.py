import attr
import re
from bs4 import BeautifulSoup as bs

from ._http_util import ABSOLUTE_URL_REGEX, RELATIVE_ROOT_URL_REGEX
from ._data_structures import Url
from ..log.log import main_logger as logger


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
            if not url: # if it is None no append
                continue
            if re.match(ABSOLUTE_URL_REGEX, url):
                self.absolute_urls.append(url)
            elif re.match(RELATIVE_ROOT_URL_REGEX, url):
                self.absolute_urls.append(self.web_page.host + url)
                logger.debug("Transformed {} to {}".format(url, self.absolute_urls[-1]))
            else:
                self.absolute_urls.append(self.web_page.short_uri + url)
                logger.debug("Transformed {} to {}".format(url, self.absolute_urls[-1]))

    def reset(self):
        self.absolute_urls.clear()
        self.buffer_urls.clear()
        self.web_page = None
        self.soup = None
