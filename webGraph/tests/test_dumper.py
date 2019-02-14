import trio
from ..utils._data_structures import WebPage, HTTPRequest, get_host_from_url, get_path_from_url
from .._dumper import dumper
from ..utils._db import open_db


web_page_host = "aratz.eus"
web_page_path = "/"
link_url = "https://ama.eus"


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
            web_page = WebPage(host=web_page_host, path=web_page_path, links=[link_url])
            await q1_write.send(web_page)
            # read response from
            http_request = await q2_read.receive()
            timeout = False
            cancel.cancel()

    assert not timeout
    assert type(http_request) is HTTPRequest
    assert http_request.host == get_host_from_url(link_url)
    assert http_request.path == get_path_from_url(link_url)

    clean_up_dbs(hosts=[web_page_host, get_host_from_url(link_url)], urls=[web_page.url_without_protocol])


def clean_up_dbs(hosts, urls):
    with open_db() as db:
        for host in hosts:
            db.graph.delete_web_page_by_host(host)
            assert not db.graph.exists_web_page_by_host(host)
        for url in urls:
            db.set_store.delete_url(url)
            assert not db.set_store.exists_url(url)
