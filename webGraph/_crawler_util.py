import attr
import re
from ._http_util import HTTP_URL_REGEX

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
        self.put_urls_to_web_page_related_links()

    def create_soup(self):
        self.soup = bs(self.web_page.html, 'html.parser')

    def analyze_soup(self):
        self.extract_urls()
        self.filter_urls()

    def put_urls_to_web_page_related_links(self):
        self.web_page.links = self.absolute_urls[:]

    def extract_urls(self):
        for link in self.soup.find_all('a'):
            self.buffer_urls.append(link.get('href'))

    def filter_urls(self):
        for url in self.buffer_urls:
            if re.match(HTTP_URL_REGEX, url):
                self.absolute_urls.append(url)
