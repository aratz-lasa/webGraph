import attr

@attr.s(cmp=False, hash=False, repr=False)
class WebPage():
    host = attr.ib(default=None)
    path = attr.ib(default=None)
    html = attr.ib(default=None)
    related_urls = attr.ib(default=attr.Factory(list))


@attr.s(cmp=False, hash=False, repr=False)
class HTTPResponse():
    code = attr.ib(default=None)
    headers = attr.ib(default=None)
    data = attr.ib(default=None)