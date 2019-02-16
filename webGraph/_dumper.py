from .utils._db import open_db
import trio


async def dumper(read_queue, write_queue):
    with open_db() as db:
        async with read_queue, write_queue:
            async for web_page in read_queue:
                await trio.run_sync_in_worker_thread(db.dump_links, web_page) # use a thread because there are sync DB accesses
                unstudied_urls = await trio.run_sync_in_worker_thread(db.get_unstudied_urls, web_page.links)
                for unstudied_url in unstudied_urls:
                    await write_queue.send(unstudied_url)

