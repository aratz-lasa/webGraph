from .utils._db import DB

async def dumper(read_queue, write_queue):
    db = DB()
    async with read_queue, write_queue:
        async for web_page in read_queue:
                # save in graph db
                db.dump_links(web_page)
                # check if related links have been studied
                unstudied_urls = db.filter_unstudied_urls(web_page.links)
                # create http_request's from un-studied links
                unstudied_http_requests = get_http_requests_from_urls(unstudied_urls)
                # write http_request's to write_queue
                for http_request in unstudied_http_requests:
                    await write_queue.send(http_request)

def get_http_requests_from_urls(urls):
    pass