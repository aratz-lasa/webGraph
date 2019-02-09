import re

from ._http_util import open_http_socket, HTTP_OK_STATUS_REGEX
from ._data_structures import WebPage


async def downloader(read_queue, write_queue):
    async with read_queue:
        for url in read_queue:
            host, path = url.split("//", 1)
            with open_http_socket(host) as http_socket:
                response = await http_socket.request(path=path)
                if re.match(HTTP_OK_STATUS_REGEX, response.code):
                    webpage = WebPage(host, path, response.data)
                    with write_queue:
                        write_queue.send(webpage)