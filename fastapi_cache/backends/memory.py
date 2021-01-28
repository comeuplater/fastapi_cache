from typing import Any, Hashable

from .base import BaseCacheBackend
from .utils.ttldict import TTLDict

CACHE_KEY = 'IN_MEMORY'


class InMemoryCacheBackend(BaseCacheBackend[Hashable, Any]):
    def __init__(self):
        self._cache = TTLDict()

    async def add(
        self,
        key: Hashable,
        value: Any,
        **kwargs,
    ) -> bool:
        return self._cache.add(key, value, **kwargs)

    async def get(
        self,
        key: Hashable,
        default: Any = None,
        **kwargs
    ) -> Any:
        return self._cache.get(key, default)

    async def set(
        self,
        key: Hashable,
        value: Any,
        **kwargs,
    ) -> bool:
        return self._cache.set(key, value, **kwargs)

    async def expire(
        self,
        key: Hashable,
        ttl: int
    ) -> bool:
        return self._cache.expire(key, ttl)

    async def exists(self, *keys: Hashable) -> bool:
        return self._cache.exists(*keys)

    async def delete(self, key: Hashable) -> bool:
        return self._cache.delete(key)

    async def flush(self) -> None:
        return self._cache.flush()

    async def close(self) -> None:  # pragma: no cover
        return None
