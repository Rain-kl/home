from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CacheItem(Generic[T]):
    value: T
    expires_at: float


class TimedCache:
    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self._items: dict[str, CacheItem] = {}

    def get_or_set(self, key: str, loader: Callable[[], T]) -> T:
        now = monotonic()
        item = self._items.get(key)
        if item and item.expires_at > now:
            return item.value

        value = loader()
        self._items[key] = CacheItem(value=value, expires_at=now + self.ttl_seconds)
        return value

    def clear(self) -> None:
        self._items.clear()
