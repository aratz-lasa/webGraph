import trio
from .._http_util import *
from .flask_test_server import start_server_thread, host, port, path, ssl, html, status, status_version



headers_dictionary = {'Content-Type': ' text/html; charset=utf-8', 'Content-Length': str(len(html)), 'Server': ' Werkzeug/0.14.1 Python/3.7.2', 'Date': ' Sun, 10 Feb 2019 10:54:32 GMT'}
data = html


def test_connect(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host, port, ssl=ssl) as http_socket:
            pass
    trio.run(open_http_connection)


def test_http_response(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host, port, ssl=False) as http_socket:
            response = await http_socket.request(path=path)
            assert type(response) is HTTPResponse
            assert response.data == html
            assert response.code == status
    trio.run(open_http_connection)


def test_parse_status_headers(start_server_thread):
    connection = HTTPConnection(host)

    prepare_connection(connection, status_version=status_version, headers=headers_dictionary)
    assert connection.response_state == READING_HEADERS
    assert not connection.response.code
    assert not connection.response.headers
    assert not connection.response.data

    prepare_connection(connection, status_version=status_version, headers=headers_dictionary, data=data)
    assert connection.response_state == DONE
    assert connection.response
    assert connection.response.headers == headers_dictionary
    assert connection.response.code == status_version.split(" ")[1]
    assert connection.response.data== data

    prepare_connection(connection, status_version=status_version, data=data)
    assert connection.response_state == DONE
    assert connection.response
    assert connection.response.headers != headers_dictionary
    assert connection.response.code == status_version.split(" ")[1]
    assert connection.response.data == ""


def prepare_connection(connection, **args):
    raw_response = prepare_raw_buffer_in(**args)
    connection.response_state = READING_HEADERS
    connection.initialize_response_receival()
    connection.buffer_in = raw_response
    connection.parse_response()


def prepare_raw_buffer_in(status_version=None, headers=None, data=None):
    raw_buffer_in = b""
    if status_version:
        raw_buffer_in = (status_version + HTTP_ONE_BLANK_LINE).encode(HTTPConnection.encoding)
    if headers:
        headers_string = ""
        for key, value in headers.items():
            headers_string += key + ":" + value + HTTP_ONE_BLANK_LINE
        raw_buffer_in += headers_string.encode(HTTPConnection.encoding)
    if data:
        if status_version or headers:
            raw_buffer_in += HTTP_ONE_BLANK_LINE.encode(HTTPConnection.encoding)
        raw_buffer_in += data.encode(HTTPConnection.encoding)
    return raw_buffer_in
