from .utils._data_structures import HTTPRequest
from .utils._db import DB
import trio


async def dumper(read_queue, write_queue):
    db = DB()
    async with read_queue, write_queue:
        async for web_page in read_queue:
            await trio.run_sync_in_worker_thread(db.dump_links, web_page) # use a thread because there are sync DB accesses
            unstudied_urls = await trio.run_sync_in_worker_thread(db.get_unstudied_urls, web_page.links)
            unstudied_http_requests = get_http_requests_from_urls(unstudied_urls)
            for http_request in unstudied_http_requests:
                await write_queue.send(http_request)


def get_http_requests_from_urls(urls):
    http_requests = []
    for url in urls:
        http_request = HTTPRequest()
        http_request.load_from_url(url)
        http_requests.append(http_request)
    return http_requests
