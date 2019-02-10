import trio
from .._downloader import downloader
from .flask_test_server import start_server_thread, host, port, path, html, ssl
from .._data_structures import WebPage, HTTPRequest

def test_downloader(start_server_thread):
    trio.run(run_async_test_downloader)


async def run_async_test_downloader():
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
            # start downloader fun
            nursery.start_soon(downloader, q1_read, q2_write)
            # write HTTPRequest to queue1
            request = HTTPRequest(host=host, port=port, path=path, ssl=ssl)
            await q1_write.send(request)
            # read response from
            web_page = await q2_read.receive()
            timeout = False
            cancel.cancel()

    assert not timeout
    assert type(web_page) is WebPage
    assert web_page.html == html
    assert web_page.host == host
    assert web_page.path == path
    assert not web_page.links
