import attr
import redis
import os

from ..settings import settings # used for executing load_dotenv()

SET_STORE_URL = os.getenv("REDIS_URL")
SET_STORE_PORT = os.getenv("REDIS_PORT")


class SetStoreDB:

    def __init__(self):
        self.init_db()

    def init_db(self):
        self._driver = redis.Redis(host=SET_STORE_URL, port=SET_STORE_PORT, db=0)
        self.set_name = "studied_urls"

    def add_url(self, url):
        self._driver.sadd(self.set_name, url)

    def delete_url(self, url):
        self._driver.srem(self.set_name, url)

    def exists_url(self, url):
        return self._driver.sismember(self.set_name, url)
