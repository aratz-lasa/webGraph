import trio
from _downloader import downloader
from .flask_test_server import start_server_thread, host, port, path, html
from .._http_util import *


def test_downloader(start_server_thread):
    trio.run(run_async_test_downloader)


async def run_async_test_downloader():
    timeout = 5
    # open timeout
    with trio.move_on_after(timeout):
        timeout = True
        # open nursery
        with trio.open_nursery() as nursery:
            # create queue1
            q1_write, q1_read = trio.open_memory_channel(0)
            # create queue2
            q2_write, q2_read = trio.open_memory_channel(0)
            # start downloader fun
            nursery.start_soon(downloader_fun, q1_read, q2_write)
            # write url to queue1
            await q1_write.send_channel.send(host)
            # read response from
            response = await q2_read.receive()
            timeout = False

        assert not timeout
        assert type(response) is HTTPResponse
        assert response.data == html
        assert response.code == "200"
        assert response.data == html


async def producer(send_channel):
    # Producer sends 3 messages
    for i in range(3):
        # The producer sends using 'await send_channel.send(...)'

async def downloader_fun(receive_channel, write_channel):
    # The consumer uses an 'async for' loop to receive the values:
    url = await receive_channel.receive()
    downloader()