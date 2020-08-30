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
    fetched_value = await f_backend.get(TEST_KEY, default)

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
