from .base import BaseCacheBackend

DEFAULT_TIMEOUT = 0


class InMemoryCacheBackend(BaseCacheBackend):
    _cache: dict = []

    async def add(self, key, value, timeout=DEFAULT_TIMEOUT):
        if key in self._cache:
            return False
        self._cache[key] = value

        return True

    async def get(self, key, default=None):
        return self._cache.get(key, default)

    async def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        self._cache[key] = value

        return True

    async def delete(self, key):
        if key not in self._cache:
            return False

        del self._cache[key]

        return True
