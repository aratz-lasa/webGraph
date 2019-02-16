import trio
from _downloader import downloader
from _crawler import crawler
from _dumper import dumper


async def set_up_workers(init_url, downloaders_num=1, crawlers_num=1, dumpers_num=1):
    # ensure at least one of each
    downloaders_num = max(1, downloaders_num)
    crawlers_num = max(1, crawlers_num)
    dumpers_num = max(1, dumpers_num)
    # create queue1
    q1_write, q1_read = trio.open_memory_channel(0)
    # create queue2
    q2_write, q2_read = trio.open_memory_channel(0)
    # create queue3
    q3_write, q3_read = trio.open_memory_channel(0)

    async with trio.open_nursery() as nursery:
        for _ in range(downloaders_num):
            await nursery.start_soon(downloader, q1_read, q2_write)
        for _ in range(crawlers_num):
            await nursery.start_soon(crawler, q2_read, q3_write)
        for _ in range(dumpers_num):
            await nursery.start_soon(dumper, q3_read, q1_write)
        await nursery.start_soon(q1_write.send, init_url)

