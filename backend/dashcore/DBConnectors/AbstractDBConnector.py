from abc import ABC, abstractmethod
from typing import List


class AbstractDBConnector(ABC):

    @abstractmethod
    def delete_keys(self, keys: List[str]) -> None:
        pass

    @abstractmethod
    def close_and_delete(self):
        pass

    @abstractmethod
    def expire(self, key: str, expire_time: int) -> None:
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    def blpop(self, queue: str, timeout: int) -> str:
        pass

    @abstractmethod
    def lpush(self, queue: str, data: dict) -> None:
        pass

    @abstractmethod
    def set(self, collection: str, data: dict, ex: int, xx: bool) -> None:
        pass

    @abstractmethod
    def list_keys(self, keys_filter: str) -> list:
        pass

    @abstractmethod
    def get_key(self, key: str) -> str:
        pass

    @abstractmethod
    def delete_key(self, key: str) -> None:
        pass

    @abstractmethod
    def get_queue_message(self, queue):
        pass

    def parse_url(self, url):
        splitted = url.split(':')
        return splitted[0], splitted[1]