
async def crawler(read_queue, write_queue):
    async with read_queue, write_queue:
        async for web_page in read_queue:
            # extract urls from web_page
            # transform relative urls to absolute
            # add related urls to web_page
            # write web_page to write queue
            await write_queue.send(web_page)


