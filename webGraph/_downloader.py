import trio


async def downloader(read_queue, write_queue):
    async with read_queue:
        # Read WebPage from read_queue
        for webpage in read_queue:
            # Download Page

            # Add HTML to WebPage
            # Write WebPage to write_queue
