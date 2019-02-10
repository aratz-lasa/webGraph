async def dumper(read_queue, write_queue):
    async with read_queue, write_queue:
        async for web_page in read_queue:
                # save in graph db

                # check if related links have been studied
                # create http_request's from un-studied links
                # write http_request's to write_queue
                for http_request in un_studied_http_requests:
                    await write_queue.send(http_request)