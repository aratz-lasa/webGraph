import trio

from .utils._db import open_db
from .log.log import main_logger


async def dumper(read_queue, write_queue):
    with open_db() as db:
        async with read_queue, write_queue:
            async for web_page in read_queue:
                main_logger.debug("{} - Dumping...".format(web_page.host))
                await trio.run_sync_in_worker_thread(db.dump_links, web_page) # use a thread because there are sync DB accesses
                unstudied_urls = await trio.run_sync_in_worker_thread(db.get_unstudied_urls, web_page.links)
                for unstudied_url in unstudied_urls:
                    main_logger.debug("{} - Sending to Downloader queue...".format(unstudied_url.short_uri))
                    await write_queue.send(unstudied_url)

