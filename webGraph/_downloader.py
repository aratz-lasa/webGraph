import re

from .utils._http_util import open_http_socket, HTTP_OK_STATUS_REGEX
from .utils._data_structures import WebPage
from .log.log import logger


async def downloader(read_queue, write_queue):
    async with read_queue, write_queue:
        async for request in read_queue:
            logger.debug("Downloading {}...".format(request.host))
            async with open_http_socket(host=request.host, ssl=request.ssl, port=request.port) as http_socket:
                response = await http_socket.request(path=request.path)
                if re.match(HTTP_OK_STATUS_REGEX, str(response.code)):
                    web_page = WebPage(url=request.url, html=response.data)
                    await write_queue.send(web_page)
