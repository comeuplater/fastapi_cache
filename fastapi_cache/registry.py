from typing import Dict, Tuple, Union

from .backends.base import BaseCacheBackend


class CacheRegistry:
    _caches: Dict[str, BaseCacheBackend] = {}

    @classmethod
    def get(cls, name: str) -> Union[BaseCacheBackend, None]:
        return cls._caches.get(name, None)

    @classmethod
    def set(cls, name: str, cache: BaseCacheBackend) -> None:
        if name in cls._caches:
            raise NameError('Cache with the same name already registered')

        cls._caches[name] = cache

    @classmethod
    def all(cls) -> Tuple[BaseCacheBackend]:
        return tuple(cls._caches.values())

    @classmethod
    def remove(cls, name: str) -> None:
        if name not in cls._caches:
            raise NameError('Cache with the same name not registered')

        del cls._caches[name]

    @classmethod
    def flush(cls) -> None:
        cls._caches = {}
