from trio import open_ssl_over_tcp_stream, open_tcp_stream
from contextlib import asynccontextmanager
import re
import h11

from ._data_structures import HTTPResponse
from ._exceptions import *




# regex patterns
HTTP_OK_STATUS_REGEX = "2.."
HTTP_URL_REGEX = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
HTTP_HOST_INSIDE_URL_REGEX = "(?<=//)[^/]*(?=/)"

# General constants
HTTP_ONE_BLANK_LINE = "\r\n"
HTTP_TWO_BLANK_LINES = HTTP_ONE_BLANK_LINE * 2
CONTENT_LENGTH_HEADER = "Content-Length"

# Response fields
STATUS_CODE = 0
HEADERS = 1
DATA = 2

# Response states
DONE = 0
READING_HEADERS = 1
READING_DATA = 2


class HTTPConnection:
    headers = {"Accept": "text/html",
               "Accept-Encoding": "utf-8",
               "Accept-Language": "en-US,en;q=0.5",
               "Cache-Control": "max-age=0",
               "Connection": "keep-alive",
               "Host": None,
               "TE": "Trailers",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Gecko/20100101 Firefox/65.0"}
    method = "GET"
    path = "/"
    http_version = 'HTTP/1.1'
    encoding = "utf-8"
    port = 80
    ssl_port = 443


    def __init__(self, timeout=5,
                 blocksize=8192):
        self.timeout = timeout
        self.blocksize = blocksize
        self.conn = None
        self.sock = None
        self._buffer_out = []
        self.buffer_in = []
        self.response = None
        self.response_state = READING_HEADERS
        self.__response = None
        self._method = None

    async def connect(self, host, port, ssl=True):
        if self.sock:
            await self.close()
        if not port:
            if ssl:
                port = self.ssl_port
            else:
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

    async def send_request(self, method, path, headers):
        self.conn = h11.Connection(our_role=h11.CLIENT)
        request = h11.Request(method=method,
                              target=path,
                              headers=self.get_formatted_headers(headers))
        data = self.conn.send(request)
        await self.sock.send_all(data)
        eof = h11.EndOfMessage()
        data = self.conn.send(eof)
        await self.sock.send_all(data)

    async def request(self, method=None, path=None, headers=None):
        if not method:
            method = self.method
        if not path:
            path = self.path
        if not headers:
            headers = self.headers

        await self.send_request(method, path, headers)
        await self.receive_response()
        return self.response

    async def receive_response(self):
        self.initialize_response_receival()
        await self.read_response()
        self.parse_response()
        return self.response

    async def read_response(self):
        while True:
            response_part = await self.read_next_response_part()
            if type(response_part) is h11.EndOfMessage:
                break
            self.buffer_in.append(response_part)

    def initialize_response_receival(self):
        self.response = HTTPResponse()
        self.buffer_in.clear()

    async def read_next_response_part(self):
        while True:
            event = self.conn.next_event()
            if event is h11.NEED_DATA:
                data = await self.sock.receive_some(self.blocksize)
                self.conn.receive_data(data)
                continue
            return event

    def parse_response(self):
        for part in self.buffer_in:
            if type(part) is h11.Response:
                self.parse_status_and_headers(part)
            elif type(part) is h11.Data:
                self.parse_data(part)

    def parse_data(self, data):
        try:
            self.response.data += data.data.decode(self.encoding)
        except UnicodeDecodeError:
            self.response.data += data.data.decode("ISO-8859-1")


    def parse_status_and_headers(self, response):
        self.response.code = response.status_code
        headers = self.response.headers
        for header in response.headers:
            key, value = header
            headers[key.decode(self.encoding)] = value.decode(self.encoding)

    def get_formatted_headers(self, headers):
        formatted_headers = []
        for key, value in headers.items():
            formatted_headers.append((key, value))
        return formatted_headers


@asynccontextmanager
async def open_http_socket(host, port=None, ssl=True):
    http_socket = HTTPConnection()
    await http_socket.connect(host, port, ssl)
    try:
        yield http_socket
    finally:
        await http_socket.close()

