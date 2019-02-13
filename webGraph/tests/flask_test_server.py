import threading
import pytest
from flask import Flask, make_response
from time import sleep

# data to know where to contact flask server
host = "127.0.0.1"
port = 8000
path = "/"
ssl = False
html = """
<!DOCTYPE html>
<html>
<body>

<h2>HTML Links</h2>
<p>HTML links are defined with the a tag:</p>

<a href="https://www.w3schools.com">This is a link</a>
<a href="www.w3schools.com">This is a link</a>
<a href="https://www.google.com/search">This is a link</a>
<a href="www.google.com">This is a link</a>

</body>
</html>"""
status_code = 200

# urls in the html
incorrect_urls = ["www.google.com", "www.w3schools.com"]
absolute_urls = ["https://www.google.com/search", "https://www.w3schools.com"]
urls = absolute_urls + incorrect_urls


_server_thread = None
_app = Flask(__name__)


@_app.route(path)
def _handle():
    response = make_response(html)
    return response, status_code


@pytest.fixture
def start_server_thread():
    global _server_thread
    if not _server_thread:
        _server_thread = threading.Thread(target=_app.run, args=(host, port), daemon=True)
        _server_thread.start()
    sleep(1) # Give time for starting server


