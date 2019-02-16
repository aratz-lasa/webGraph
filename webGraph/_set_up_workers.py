import trio
from math import inf

from ._downloader import downloader
from ._crawler import crawler
from ._dumper import dumper
from .log.log import main_logger as logger

async def set_up_workers(init_url, downloaders_num=100, crawlers_num=2, dumpers_num=2):
    # ensure at least one of each
    downloaders_num = max(1, downloaders_num)
    crawlers_num = max(1, crawlers_num)
    dumpers_num = max(1, dumpers_num)
    # create queue1
    q1_write, q1_read = trio.open_memory_channel(inf)
    # create queue2
    q2_write, q2_read = trio.open_memory_channel(inf)
    # create queue3
    q3_write, q3_read = trio.open_memory_channel(inf)

    async with trio.open_nursery() as nursery:
        for i in range(downloaders_num):
            nursery.start_soon(downloader, q1_read, q2_write)
            logger.debug("Created Downloader {}/{}".format(i+1, downloaders_num))
        for i in range(crawlers_num):
            nursery.start_soon(crawler, q2_read, q3_write)
            logger.debug("Created Crawler {}/{}".format(i+1, crawlers_num))
        for i in range(dumpers_num):
            nursery.start_soon(dumper, q3_read, q1_write)
            logger.debug("Created Dumper {}/{}".format(i+1, dumpers_num))
        nursery.start_soon(q1_write.send, init_url)

