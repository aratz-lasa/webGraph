import trio
from ..utils._data_structures import WebPage, ShortUri, Url
from .._dumper import dumper
from ..utils._db import open_db


web_page_url = "aratz.eus"
link_url = Url("https://ama.eus")


def test_downloader():
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
            nursery.start_soon(dumper, q1_read, q2_write)
            # write HTTPRequest to queue1
            web_page = WebPage(url=web_page_url, links=[link_url])
            await q1_write.send(web_page)
            # read response from
            http_request = await q2_read.receive()
            timeout = False
            cancel.cancel()

    assert not timeout
    assert type(http_request) is Url
    assert http_request.host == link_url.host
    assert http_request.path == link_url.path

    clean_up_dbs([web_page, link_url], [web_page])


def clean_up_dbs(graph_nodes, set_store_entries):
    with open_db() as db:
        for node in graph_nodes:
            db.graph.delete_short_uri(node)
            assert not db.graph.exists_short_uri(node)
        for entry in set_store_entries:
            db.set_store.delete_short_uri(entry)
            assert not db.set_store.exists_short_uri(entry)
