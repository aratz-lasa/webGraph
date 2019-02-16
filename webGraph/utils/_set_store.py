from contextlib import contextmanager
import redis
import os

from ._abc import SetStoreABC
from ..settings import settings # used for executing load_dotenv()

SET_STORE_URL = os.getenv("REDIS_URL")
SET_STORE_PORT = os.getenv("REDIS_PORT")


class RedisDB(SetStoreABC):

    def __init__(self):
        self.init_db()

    def init_db(self):
        self._driver = redis.Redis(host=SET_STORE_URL, port=SET_STORE_PORT, db=0)
        self.set_name = "studied_urls"

    def add_short_uri_entry(self, short_uri):
        self._driver.sadd(self.set_name, short_uri.short_uri)

    def delete_short_uri_entry(self, short_uri):
        self._driver.srem(self.set_name, short_uri.short_uri)

    def exists_short_uri_entry(self, short_uri):

        return self._driver.sismember(self.set_name, short_uri.short_uri)

    def close(self):
        pass  # Redis does not need to exit


@contextmanager
def open_set_store(SetStoreClass=RedisDB):
    set_store = SetStoreClass()
    try:
        yield set_store
    finally:
        set_store.close()
