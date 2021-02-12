from typing import Tuple, List, Any

import aioredis
import pytest

from fastapi_cache.backends.redis import RedisCacheBackend, RedisKey

TEST_KEY = 'constant'
TEST_VALUE = '0'


@pytest.fixture
def f_backend() -> RedisCacheBackend:
    return RedisCacheBackend(
        'redis://localhost'
    )


@pytest.mark.asyncio
async def test_should_add_n_get_data(
    f_backend: RedisCacheBackend
) -> None:
    is_added = await f_backend.add(TEST_KEY, TEST_VALUE)

    assert is_added is True
    assert await f_backend.get(TEST_KEY) == TEST_VALUE


@pytest.mark.asyncio
async def test_should_add_n_get_data_no_encoding(
    f_backend: RedisCacheBackend
) -> None:
    NO_ENCODING_KEY = 'bytes'
    NO_ENCODING_VALUE = b'test'
    is_added = await f_backend.add(NO_ENCODING_KEY, NO_ENCODING_VALUE)

    assert is_added is True
    assert await f_backend.get(NO_ENCODING_KEY, encoding=None) == bytes(NO_ENCODING_VALUE)


@pytest.mark.asyncio
async def test_add_should_return_false_if_key_exists(
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.add(TEST_KEY, TEST_VALUE)
    is_added = await f_backend.add(TEST_KEY, TEST_VALUE)

    assert is_added is False


@pytest.mark.asyncio
async def test_should_return_default_if_key_not_exists(
    f_backend: RedisCacheBackend
) -> None:
    default = '3.14159'
    fetched_value = await f_backend.get('not_exists', default)

    assert fetched_value == default


@pytest.mark.parametrize('preset,keys,exists', (
    [
        [
            ('key1', 'value1'),
            ('key2', 'value2'),
        ],
        ['key1', 'key2'],
        True,
    ],
    [
        [
            ('key1', 'value1'),
        ],
        ['key1', 'key2'],
        True,
    ],
    [
        [
            ('key1', 'value1'),
            ('key2', 'value2'),
        ],
        ['key3', 'key4'],
        False,
    ],
    [
        [],
        ['key3', 'key4'],
        False,
    ],

))
@pytest.mark.asyncio
async def test_should_check_is_several_keys_exists(
    preset: List[Tuple[str, str]],
    keys: List[str],
    exists: bool,
    f_backend: RedisCacheBackend
) -> None:
    for key, value in preset:
        await f_backend.add(key, value)

    assert await f_backend.exists(*keys) == exists


@pytest.mark.asyncio
async def test_set_should_rewrite_value(
    f_backend: RedisCacheBackend
) -> None:
    eulers_number = '2.71828'

    await f_backend.add(TEST_KEY, TEST_VALUE)
    await f_backend.set(TEST_KEY, eulers_number)

    fetched_value = await f_backend.get(TEST_KEY)

    assert fetched_value == eulers_number


@pytest.mark.asyncio
async def test_delete_should_remove_from_cache(
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.add(TEST_KEY, TEST_VALUE)
    await f_backend.delete(TEST_KEY)

    fetched_value = await f_backend.get(TEST_KEY)

    assert fetched_value is None


@pytest.mark.asyncio
@pytest.mark.parametrize('key,value,ttl,expected', [
    [TEST_KEY, TEST_VALUE, 0, None],
    [TEST_KEY, TEST_VALUE, 10, TEST_VALUE],
])
async def test_expire_from_cache(
    key: RedisKey,
    value: Any,
    ttl: int,
    expected: Any,
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.add(key, value)
    await f_backend.expire(key, ttl)
    fetched_value = await f_backend.get(key)

    assert fetched_value == expected


@pytest.mark.asyncio
async def test_flush_should_remove_all_objects_from_cache(
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.add('pi', '3.14159')
    await f_backend.add('golden_ratio', '1.61803')

    await f_backend.flush()

    assert await f_backend.get('pi') is None
    assert await f_backend.get('golden_ratio') is None


@pytest.mark.asyncio
async def test_close_should_close_connection(
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.close()
    with pytest.raises(aioredis.errors.PoolClosedError):
        await f_backend.add(TEST_KEY, TEST_VALUE)


@pytest.mark.asyncio
@pytest.mark.parametrize('key,value,expected', [
    [1, 1, '1'],
    ['1', 1, '1'],
    [1.5, 1, '1'],
    [b'bytes', 1, '1'],
    ['2', 1.5, '1.5'],
    [3, b'bytes', 'bytes'],  # default encoding
    [3.5, '3.5', '3.5'],
])
async def test_scalar_types(
    key: RedisKey,
    value: Any,
    expected: Any,
    f_backend: RedisCacheBackend
) -> None:
    await f_backend.set(key, value)
    assert await f_backend.get(key) == expected
