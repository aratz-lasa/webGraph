import attr


@attr.s(cmp=False, hash=False, repr=False)
class WebPage():
    url = attr.ib(default=None)
    html = attr.ib(default=None)
    related_urls = attr.ib(default=attr.Factory(list))