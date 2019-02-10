import re

from .utils._http_util import open_http_socket, HTTP_OK_STATUS_REGEX
from .utils._data_structures import WebPage


async def downloader(read_queue, write_queue):
    async with read_queue, write_queue:
        async for request in read_queue:
            async with open_http_socket(request.host, request.port, request.ssl) as http_socket:
                response = await http_socket.request(path=request.path)
                if re.match(HTTP_OK_STATUS_REGEX, response.code):
                    webpage = WebPage(host=request.host, path=request.path, html=response.data)
                    await write_queue.send(webpage)
