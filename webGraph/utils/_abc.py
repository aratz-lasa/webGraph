from abc import ABCMeta, abstractmethod


class GraphABC(metaclass=ABCMeta):

    @abstractmethod
    def create_short_uri_node(self, short_uri):
        pass

    @abstractmethod
    def create_link_relationship(self, from_short_uri, to_short_uri):
        pass

    @abstractmethod
    def delete_short_uri_node(self, short_uri):
        pass

    @abstractmethod
    def exists_short_uri_node(self, short_uri):
        pass

    @abstractmethod
    def exists_link_relationship(self, from_short_uri, to_short_uri):
        pass

    @abstractmethod
    def close(self):
        pass


class SetStoreABC(metaclass=ABCMeta):

    @abstractmethod
    def add_short_uri_entry(self, short_uri):
        pass

    @abstractmethod
    def delete_short_uri_entry(self, short_uri):
        pass

    @abstractmethod
    def exists_short_uri_entry(self, short_uri):
        pass

    @abstractmethod
    def clean(self):
        pass

    @abstractmethod
    def close(self):
        pass