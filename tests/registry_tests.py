import pytest

from fastapi_cache.backends.memory import BaseCacheBackend, CACHE_KEY
from fastapi_cache.registry import CacheRegistry


@pytest.fixture
def cache_registry() -> CacheRegistry:
    registry = CacheRegistry()
    yield registry
    registry.flush()


def test_get_from_registry_should_return_none_if_cache_not_registered(
    cache_registry: CacheRegistry
) -> None:
    assert cache_registry.get('') is None


def test_get_from_registry_should_return_cache_instance(
    cache_registry: CacheRegistry
) -> None:
    cache = BaseCacheBackend()
    cache_registry.set(CACHE_KEY, cache)

    assert cache_registry.get(CACHE_KEY) == cache


def test_retrieve_all_registered_caches_from_registry(
    cache_registry: CacheRegistry
) -> None:
    cache = BaseCacheBackend()

    cache_registry.set(CACHE_KEY, cache)
    cache_registry.set('OTHER_CACHE_KEY', cache)

    assert cache_registry.all() == (cache, cache)


def test_registry_should_raise_error_on_dublicate_cache_key(
    cache_registry: CacheRegistry
) -> None:
    cache = BaseCacheBackend()
    cache_registry.set(CACHE_KEY, cache)

    with pytest.raises(NameError, match='Cache with the same name already registered'):
        cache_registry.set(CACHE_KEY, cache)


def test_remove_cache_from_registry(
    cache_registry: CacheRegistry
) -> None:
    cache = BaseCacheBackend()
    cache_registry.set(CACHE_KEY, cache)
    cache_registry.remove(CACHE_KEY)

    assert cache_registry.get(CACHE_KEY) is None


def test_remove_cache_from_registry_should_raise_error_if_cache_not_register(
    cache_registry: CacheRegistry
) -> None:
    with pytest.raises(NameError, match='Cache with the same name not registered'):
        cache_registry.remove(CACHE_KEY)


def test_flush_should_remove_all_registered_cashes(
    cache_registry: CacheRegistry
) -> None:
    cache = BaseCacheBackend()

    cache_registry.set(CACHE_KEY, cache)
    cache_registry.set('OTHER_CACHE_KEY', cache)

    cache_registry.flush()

    assert cache_registry.get(CACHE_KEY) is None
    assert cache_registry.get('OTHER_CACHE_KEY') is None


@pytest.mark.backwards
def test_registry_can_be_imported_by_older_path() -> None:
    import importlib

    fastapi_cache = importlib.import_module("fastapi_cache")
    assert hasattr(fastapi_cache, 'caches')