import trio
from .._crawler import crawler
from .flask_test_server import *
from ..utils._data_structures import WebPage, Url

def test_downloader(start_server_thread):
    trio.run(run_async_test_crawler)


async def run_async_test_crawler():
    timeout = 5
    # open timeout
    with trio.move_on_after(timeout) as cancel:
        exited = True
        # open nursery
        async with trio.open_nursery() as nursery:
            # create queue1
            q1_write, q1_read = trio.open_memory_channel(0)
            # create queue2
            q2_write, q2_read = trio.open_memory_channel(0)
            # start downloader fun
            nursery.start_soon(crawler, q1_read, q2_write)
            # write HTTPRequest to queue1
            web_page = WebPage(url=url, html=html)
            await q1_write.send(web_page)
            # read response from
            web_page = await q2_read.receive()
            exited = False
            cancel.cancel()

    assert not exited
    assert type(web_page) is WebPage
    assert web_page.html == html
    assert web_page.host == host
    assert web_page.path == path
    assert web_page.links
    assert set(web_page.links) == set(map(lambda url: Url(url), absolute_urls))

