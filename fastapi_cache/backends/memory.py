from typing import Any, Union, Hashable, Tuple

from .base import BaseCacheBackend

CACHE_KEY = 'IN_MEMORY'


class InMemoryCacheBackend(BaseCacheBackend[Hashable, Any]):
    def __init__(self):
        self._cache: dict = {}

    async def add(
        self,
        key: Hashable,
        value: Any,
        **kwargs,
    ) -> bool:
        if key in self._cache:
            return False
        self._cache[key] = value

        return True

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
        self._cache[key] = value

        return True

    async def exists(self, *keys: Tuple[Hashable]) -> bool:
        return any(
            map(lambda key: key in self._cache, keys)
        )

    async def delete(self, key: Hashable) -> bool:
        if key not in self._cache:
            return False
        del self._cache[key]

        return True

    async def flush(self) -> None:
        self._cache = {}

    async def close(self) -> None:  # pragma: no cover
        return None
