import trio
from .._http_util import *
from .flask_test_server import start_server_thread, host, port, path, html


def test_connect(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host, int(port), ssl=False) as http_socket:
            pass
    trio.run(open_http_connection)

def test_http_response(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host, int(port), ssl=False) as http_socket:
            response = await http_socket.request(path=path)
            assert type(response) is HTTPResponse
            assert response.data == html
            assert response.code == "200"
    trio.run(open_http_connection)

