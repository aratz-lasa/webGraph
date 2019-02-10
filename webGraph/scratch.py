import trio
from utils import _http_util as http

if __name__ == "__main__":
    webpage = "trio.readthedocs.io"

    conn = http.HTTPConnection(webpage)
    async def fun():
        await conn.connect(webpage)
        response = await conn.request("GET", "/en/latest/")
        print(response.html)
    trio.run(fun)

