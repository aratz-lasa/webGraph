import attr

@attr.s(cmp=False, hash=False, repr=False)
class WebPage:
    host = attr.ib(default=None)
    path = attr.ib(default=None)
    html = attr.ib(default=None)
    links = attr.ib(default=attr.Factory(list))


@attr.s(cmp=False, hash=False, repr=False)
class HTTPResponse:
    code = attr.ib(default=None)
    headers = attr.ib(default=None)
    data = attr.ib(default=None)


@attr.s(cmp=False, hash=False, repr=False)
class HTTPRequest:
    host = attr.ib()
    port = attr.ib(default=443)
    path = attr.ib(default="/")
    ssl = attr.ib(default=True)
