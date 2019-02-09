from flask import Flask, make_response

app = Flask(__name__)


def setup_handler(path, html):
    @app.route(path)
    def handle():
        response = make_response(html)
        return response


def run_test_server(host, port, path, html):
    setup_handler(path, html)
    app.run(host, int(port))


