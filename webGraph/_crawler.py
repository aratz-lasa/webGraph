from .utils._crawler_util import CrawlerUtil
from .log.log import main_logger as logger

async def crawler(read_queue, write_queue):
    crawler_util = CrawlerUtil()
    async with read_queue, write_queue:
        async for web_page in read_queue:
            logger.debug("{} - Crawling...".format(web_page.short_uri))
            crawler_util.fill_links(web_page)
            logger.debug("{} - Sending to Dumper queue...".format(web_page.short_uri))
            await write_queue.send(web_page)
