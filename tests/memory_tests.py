from typing import Hashable, Any, Tuple

import pytest

from fastapi_cache.backends.memory import InMemoryCacheBackend

TEST_KEY = 'constant'
TEST_VALUE = '0'


@pytest.fixture
def f_backend() -> InMemoryCacheBackend:
    return InMemoryCacheBackend()


@pytest.mark.asyncio
async def test_should_add_n_get_data(
    f_backend: InMemoryCacheBackend
) -> None:
    is_added = await f_backend.add(TEST_KEY, TEST_VALUE)

    assert is_added is True
    assert await f_backend.get(TEST_KEY) == TEST_VALUE


@pytest.mark.asyncio
async def test_add_should_return_false_if_key_exists(
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.add(TEST_KEY, TEST_VALUE)
    is_added = await f_backend.add(TEST_KEY, TEST_VALUE)

    assert is_added is False


@pytest.mark.asyncio
async def test_should_return_default_if_key_not_exists(
    f_backend: InMemoryCacheBackend
) -> None:
    default = '3.14159'
    fetched_value = await f_backend.get('not_exists', default)

    assert fetched_value == default


@pytest.mark.asyncio
async def test_set_should_rewrite_value(
    f_backend: InMemoryCacheBackend
) -> None:
    eulers_number = '2.71828'

    await f_backend.add(TEST_KEY, TEST_VALUE)
    await f_backend.set(TEST_KEY, eulers_number)

    fetched_value = await f_backend.get(TEST_KEY)

    assert fetched_value == eulers_number


@pytest.mark.asyncio
async def test_delete_should_remove_from_cache(
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.add(TEST_KEY, TEST_VALUE)
    await f_backend.delete(TEST_KEY)

    fetched_value = await f_backend.get(TEST_KEY)

    assert fetched_value is None


@pytest.mark.asyncio
async def test_flush_should_remove_all_objects_from_cache(
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.add('pi', '3.14159')
    await f_backend.add('golden_ratio', '1.61803')

    await f_backend.flush()

    assert await f_backend.get('pi') is None
    assert await f_backend.get('golden_ratio') is None


@pytest.mark.asyncio
@pytest.mark.parametrize('key,value,ttl,expected', [
    ['hello', 'world', 0, None],
    ['hello', 'world', 100, 'world'],
])
async def test_should_set_value_with_ttl(
    key: Hashable,
    value: Any,
    ttl: int,
    expected: Any,
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.set(key, value, ttl=ttl)
    fetched_value = await f_backend.get(key)

    assert fetched_value == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('key,value,ttl,expected', [
    ['hello', 'world', 0, None],
    ['hello', 'world', 100, 'world'],
])
async def test_should_add_value_with_ttl(
    key: Hashable,
    value: Any,
    ttl: int,
    expected: Any,
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.add(key, value, ttl=ttl)
    fetched_value = await f_backend.get(key)

    assert fetched_value == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('keys', [
    ('hello', 'world'),
])
async def test_key_should_check_for_exists(
    keys: Tuple[Hashable],
    f_backend: InMemoryCacheBackend
) -> None:
    for key in keys:
        await f_backend.set(key, key)

    assert await f_backend.exists(*keys) is True


@pytest.mark.asyncio
@pytest.mark.parametrize('keys,ttl,exists', [
    [('hello', 'world'), 0, False],
    [('hello', 'world'), 100, True],
])
async def test_key_should_check_for_exists_with_ttl(
    keys: Tuple[Hashable],
    ttl: int,
    exists: bool,
    f_backend: InMemoryCacheBackend
) -> None:
    for key in keys:
        await f_backend.set(key, key, ttl=ttl)

    assert await f_backend.exists(*keys) is exists


@pytest.mark.asyncio
@pytest.mark.parametrize('keys', [
    ('hello', 'world'),
])
async def test_should_return_false_if_keys_not_exist(
    keys: Tuple[Hashable],
    f_backend: InMemoryCacheBackend
) -> None:
    assert await f_backend.exists(*keys) is False


@pytest.mark.asyncio
@pytest.mark.parametrize('key,value,ttl,expected', [
    [TEST_KEY, TEST_VALUE, 0, None],
    [TEST_KEY, TEST_VALUE, 10, TEST_VALUE],
])
async def test_expire_from_cache(
    key: Hashable,
    value: Any,
    ttl: int,
    expected: Any,
    f_backend: InMemoryCacheBackend
) -> None:
    await f_backend.add(key, value)
    await f_backend.expire(key, ttl)
    fetched_value = await f_backend.get(key)

    assert fetched_value == expected
