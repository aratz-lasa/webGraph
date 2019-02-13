import trio
from ..utils._http_util import *
from .flask_test_server import *
from h11 import Data, Response



headers_dictionary = {'content-type': 'text/html; charset=utf-8', 'content-length': str(len(html)), 'server': 'Werkzeug/0.14.1 Python/3.7.2', 'date': 'Sun, 10 Feb 2019 10:54:32 GMT'}


def test_connect(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host, port, ssl=ssl) as http_socket:
            pass
    trio.run(open_http_connection)


def test_http_response(start_server_thread):
    async def open_http_connection():
        async with open_http_socket(host=host, ssl=False, port=port) as http_socket:
            response = await http_socket.request(path=path)
            assert type(response) is HTTPResponse
            assert response.data == html
            assert response.code == status_code
    trio.run(open_http_connection)


def test_parse_status_headers(start_server_thread):
    connection = HTTPConnection(host)

    prepare_connection(connection, status_code=status_code, headers=headers_dictionary, data=None)
    assert connection.response.code
    assert connection.response.headers
    assert connection.response.headers == headers_dictionary
    assert connection.response.code == status_code
    assert not connection.response.data

    prepare_connection(connection, status_code=status_code, headers=headers_dictionary, data=html)
    assert connection.response
    assert connection.response.headers == headers_dictionary
    assert connection.response.code == status_code
    assert connection.response.data == html


def prepare_connection(connection, status_code, headers, data):
    connection.initialize_response_receival()
    headers = connection.get_formatted_headers(headers)
    connection.buffer_in.append(Response(status_code=status_code, headers=headers))
    if data:
        connection.buffer_in.append(Data(data=data.encode(connection.encoding)))
    connection.parse_response()


