import trio

from .flask_test_server import *
from .._downloader import downloader
from .._crawler import crawler
from ..utils._data_structures import WebPage, HTTPRequest

def test_downloader(start_server_thread):
    trio.run(run_async_test_downloader_crawler)


async def run_async_test_downloader_crawler():
    timeout = 5
    # open timeout
    with trio.move_on_after(timeout) as cancel:
        timeout = True
        # open nursery
        async with trio.open_nursery() as nursery:
            # create queue1
            q1_write, q1_read = trio.open_memory_channel(0)
            # create queue2
            q2_write, q2_read = trio.open_memory_channel(0)
            # create queue3
            q3_write, q3_read = trio.open_memory_channel(0)
            # start downloader fun
            nursery.start_soon(downloader, q1_read, q2_write)
            nursery.start_soon(crawler, q2_read, q3_write)
            # write HTTPRequest to queue1
            request = HTTPRequest(host=host, port=port, path=path, ssl=ssl)
            await q1_write.send(request)
            # read WebPage from q3_read
            web_page = await q3_read.receive()
            timeout = False
            cancel.cancel()

    assert not timeout
    assert type(web_page) is WebPage
    assert web_page.html == html
    assert web_page.host == host
    assert web_page.path == path
    assert web_page.links
    assert set(web_page.links) == set(absolute_urls)