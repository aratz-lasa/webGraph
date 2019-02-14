import attr
import re

@attr.s(cmp=False, hash=False, repr=False)
class WebPage:
    host = attr.ib(default=None)
    path = attr.ib(default=None)
    html = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))

    @property
    def url_without_protocol(self):
        return self.host+self.path


@attr.s(cmp=False, hash=False, repr=False)
class HTTPResponse:
    code = attr.ib(default=None)
    headers = attr.ib(default=attr.Factory(dict))
    data = attr.ib(default="")


@attr.s(cmp=False, hash=False, repr=False)
class HTTPRequest:
    host = attr.ib(default=None)
    path = attr.ib(default="/")
    ssl = attr.ib(default=True)
    port = attr.ib(default=None) # only used for tests. If None --> 443 if ssl, 80 if not ssl

    def load_from_url(self, url):
        self.host = get_host_from_url(url)
        self.path = get_path_from_url(url)
        self.ssl = uses_ssl_url(url)


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
