import subprocess
from time import sleep
import pytest
import trio
import os
import threading
from .flask_test_server import run_test_server
from .._http_util import *

test_server = None
host = "127.0.0.1"
port = "5000"
path = "/"
html = "Hello"
server_thread = None


@pytest.fixture
def start_server():
    global server_thread
    if not server_thread:
        server_thread = threading.Thread(target=run_test_server, args=(host, port, path, html), daemon=True)
        server_thread.start()
    sleep(1) # Give time for starting server


def test_connect(start_server):
    async def open_http_connection():
        async with open_http_socket(host, int(port), ssl=False) as http_socket:
            pass
    trio.run(open_http_connection)

def test_http_response(start_server):
    async def open_http_connection():
        async with open_http_socket(host, int(port), ssl=False) as http_socket:
            response = await http_socket.request(path=path)
            assert type(response) is HTTPResponse
            assert response.html == html
            assert response.code == "200"
    trio.run(open_http_connection)

