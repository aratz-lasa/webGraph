import threading
import pytest
from flask import Flask, make_response
from time import sleep

host = "127.0.0.1"
port = 5000
path = "/"
ssl = False
html = "Hello"
status = "200"

server_thread = None
app = Flask(__name__)


def setup_handler(path, html):
    @app.route(path)
    def handle():
        response = make_response(html)
        return response, 200


def run_test_server(host, port, path, html):
    setup_handler(path, html)
    app.run(host, port)


@pytest.fixture
def start_server_thread():
    global server_thread
    if not server_thread:
        server_thread = threading.Thread(target=run_test_server, args=(host, port, path, html), daemon=True)
        server_thread.start()
    sleep(1) # Give time for starting server


