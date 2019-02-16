import trio

from .flask_test_server import *
from .._dumper import dumper
from .._crawler import crawler
from ..utils._data_structures import WebPage, Url, get_host_from_url, remove_protocol_from_url
from ..utils._db import open_db

def test_downloader():
    trio.run(run_async_test_crawler_dumper)


async def run_async_test_crawler_dumper():
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
            # create queue3
            q3_write, q3_read = trio.open_memory_channel(0)
            # start downloader fun
            nursery.start_soon(crawler, q1_read, q2_write)
            nursery.start_soon(dumper, q2_read, q3_write)
            # write HTTPRequest to queue1
            web_page = WebPage(url=url, html=html)
            await q1_write.send(web_page)
            # read WebPage from q3_read
            http_request1 = await q3_read.receive()
            http_request2 = await q3_read.receive()
            exited = False
            cancel.cancel()

    assert not exited
    assert type(http_request1) is Url
    assert http_request1.url in set(absolute_urls)

    assert type(http_request2) is Url
    assert http_request2.url in set(absolute_urls)

    clean_databases_by_urls([http_request1, http_request2, web_page])

def clean_databases_by_urls(urls):
    with open_db() as db:
        for url in urls:
            db.graph.delete_short_uri_node(url)
            assert not db.graph.exists_short_uri_node(url)

            db.set_store.delete_short_uri_entry(url)
            assert  not db.set_store.exists_short_uri_entry(url)
