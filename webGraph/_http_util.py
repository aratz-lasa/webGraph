from urllib.parse import urlsplit
import urllib
from trio import open_ssl_over_tcp_stream, open_tcp_stream
from ._data_structures import HTTPResponse
from contextlib import asynccontextmanager
import re


# General constants
HTTP_OK_STATUS_REGEX = "2.."
HTTP_ONE_BLANK_LINE = "\r\n"
HTTP_TWO_BLANK_LINES = HTTP_ONE_BLANK_LINE * 2

# Response fields
STATUS_CODE = 0
HEADERS = 1
DATA = 2

# Response states
DONE = 0
READING_HEADERS = 1
READING_DATA = 2


class HTTPConnection:
    headers = {"Accept": "text/html,application/xhtml+xm…ml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "utf-8",
               "Accept-Language": "en-US,en;q=0.5",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Host": None,
               "TE": "Trailers",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/65.0"}
    method = "GET"
    path = "/"
    http_version = 'HTTP/1.1'
    encoding = "utf-8"

    def __init__(self, host=None, port=443, timeout=5,
                 source_address=None, blocksize=8192):
        self.timeout = timeout
        self.source_address = source_address
        self.blocksize = blocksize
        self.sock = None
        self._buffer_out = []
        self.buffer_in = ""
        self.response = None
        self.response_state = READING_HEADERS
        self.__response = None
        self._method = None

        self.host = host
        self.port = port

    async def connect(self, host, port=None, ssl=True):
        if self.sock:
            await self.close()
        if port is None:
            port = self.port

        if ssl:
            self.sock = await open_ssl_over_tcp_stream(host, port, https_compatible=True)
        else:
            self.sock = await open_tcp_stream(host, port)
        self.headers["Host"] = host

    async def close(self):
        try:
            sock = self.sock
            if sock:
                self.sock = None
                await sock.aclose()
        except:
            pass

    async def send(self, data):
        try:
            await self.sock.send_all(data)
        except TypeError:
            raise TypeError("data should be a bytes-like object ")

    def _output(self, s):
        self._buffer_out.append(s)

    async def _send_output(self):
        self._buffer_out.extend((b"", b""))
        msg = b"\r\n".join(self._buffer_out)
        del self._buffer_out[:]
        await self.send(msg)

    def putrequest(self, method, path):
        if not path:
            path = self.path
        request = '%s %s %s' % (method, path, self.http_version)
        self._output(request.encode(self.encoding))

    def putheader(self, header, *values):
        header = header.encode(self.encoding)
        values = list(values)
        for i, one_value in enumerate(values):
                values[i] = one_value.encode(self.encoding)

        value = b'\r\n\t'.join(values)
        header = header + b': ' + value
        self._output(header)

    async def endheaders(self):
        await self._send_output()

    async def request(self, method=None, path=None, headers=None):
        if not method:
            method = self.method
        if not path:
            path = self.path
        if not headers:
            headers = self.headers
        await self._send_request(path, headers)

        return await self.receive_response()

    async def _send_request(self, path, headers):
        self.putrequest(self.method, path)
        for hdr, value in headers.items():
            self.putheader(hdr, value)
        await self.endheaders()

    async def receive_response(self):
        self.initialize_response_receival()
        while self.response_state != DONE:
            await self.read_response()
        return self.response

    def initialize_response_receival(self):
        self.response = HTTPResponse()
        self.response_state = READING_HEADERS
        self.buffer_in = ""

    async def read_response(self):
        if self.response_state == READING_HEADERS:
            self.buffer_in = await self.sock.receive_some(self.blocksize)
            self.parse_set_headers_and_code()
        if self.response_state == READING_DATA:
            self.buffer_in = await self.sock.receive_some(int(self.response.headers["Content-Length"]) - len(self.buffer_in))
            self.parse_set_data()

    def parse_set_headers_and_code(self):
        buffer_in = self.buffer_in.decode(self.encoding)
        if not re.search(HTTP_TWO_BLANK_LINES, buffer_in):
            return
        code_headers, data = buffer_in.split(HTTP_TWO_BLANK_LINES)
        code, headers = code_headers.split(HTTP_ONE_BLANK_LINE, 1)
        self.parse_set_code(code)
        self.parse_set_headers(headers)
        new_start = len(code_headers) + len(HTTP_TWO_BLANK_LINES) - 1
        self.buffer_in = self.buffer_in[new_start:]
        self.response_state = READING_DATA

    def parse_set_data(self):
        buffer_in = self.buffer_in
        content_length = int(self.response.headers["Content-Length"])
        if len(buffer_in) < content_length:
            return
        self.response.data = self.buffer_in[:content_length].decode(self.encoding)
        self.response_state = DONE

    def parse_set_headers(self, raw_headers):
        raw_headers = raw_headers.split(HTTP_ONE_BLANK_LINE)
        headers = {}
        for raw_header in raw_headers:
            key, value = raw_header.split(':', 1)  # split each line by http field name and value
            headers[key] = value
        self.response.headers = headers

    def parse_set_code(self, code):
        self.response.code = code.split(" ")[1]  # extract code from HTTP/1.1 302 FOUND --> 302


@asynccontextmanager
async def open_http_socket(host, port=None, ssl=True):
    http_socket = HTTPConnection(host, port)
    await http_socket.connect(host, ssl=ssl)
    try:
        yield http_socket
    finally:
        await http_socket.close()

