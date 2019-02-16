import attr
import re


class ShortUri:
    def __init__(self, url):
        self.host = get_host_from_url(url)
        self.path = get_path_from_url(url)

    @property
    def short_uri(self):
        return self.host + self.path

    def __eq__(self, other):
        if type(self) == type(other) and self.short_uri == other.short_uri:
            return True
        return False

    def __hash__(self):
        return hash((self.host, self.path))


class WebPage(ShortUri):

    def __init__(self, url, html=None, links=None):
        super().__init__(url)
        self.html = html
        self.links = links
        if not links:
            self.links = []

    def __hash__(self):
        return super().__hash__()


class Url(ShortUri):
    def __init__(self, url, port=None):
        super().__init__(url)
        self.ssl = uses_ssl_url(url)
        self.port = port

    @property
    def url(self):
        if self.ssl:
            return "https://" + self.host + self.path
        return "http://" + self.host + self.path

    def __eq__(self, other):
        if super().__eq__(other) and self.port==other.port and self.ssl == other.ssl:
            return True
        return False

    def __hash__(self):
        return hash((super().__hash__(), self.port, self.ssl))


@attr.s(cmp=False, hash=False, repr=False)
class HTTPResponse:
    code = attr.ib(default=None)
    headers = attr.ib(default=attr.Factory(dict))
    data = attr.ib(default="")


def get_host_from_url(url):
    return url.split("://")[-1].split("/")[0]


def get_path_from_url(url):
    host = url.split("://")[-1]
    host_and_path = host.split("/", 1)
    path = "/"
    if len(host_and_path) == 2:
        path += host_and_path[1]
    return path


def get_name_from_host(host):
    if not re.search("\.", host):
        return host
    return "".join(host.split(".")[-2])


def uses_ssl_url(url):
    return not re.match("http:.*", url)


def remove_protocol_from_url(url):
    return url.split("://")[-1]
