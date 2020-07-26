from typing import Dict, Iterable

from .backends.base import BaseCacheBackend


class CacheRegistry(object):
    _caches: Dict[str, BaseCacheBackend] = {}

    def get(self, name: str) -> BaseCacheBackend:
        return self._caches[name]

    def set(self, name: str, cache_backend: BaseCacheBackend) -> None:
        self._caches[name] = cache_backend

    def all(self) -> Iterable[BaseCacheBackend]:
        return self._caches.values()


caches = CacheRegistry()


async def close_caches():
    for cache in caches.all():
        await cache.close()
