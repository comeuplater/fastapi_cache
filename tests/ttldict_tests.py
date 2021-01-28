from typing import Hashable, Any, Tuple
from unittest import mock

import pytest

from fastapi_cache.backends.utils.ttldict import TTLDict

MOCKED_DICT = dict()


@pytest.fixture
def ttl_dict() -> TTLDict:
    global MOCKED_DICT
    MOCKED_DICT = dict()

    with mock.patch('fastapi_cache.backends.utils.ttldict.dict', return_value=MOCKED_DICT):
        return TTLDict()


@pytest.mark.parametrize('key,value', [
    ('hello', 'world'),
])
def test_set_value_to_dict(
    key: Hashable,
    value: Any,
    ttl_dict: TTLDict,
) -> None:
    assert ttl_dict.set(key, value) is True
    assert key in MOCKED_DICT
    assert MOCKED_DICT[key] == (None, value)


@pytest.mark.parametrize('key,value,rewrite_value', [
    ('hello', 'world', 'kitty'),
])
def test_ser_should_rewrite_value_if_exits(
    key: Hashable,
    value: Any,
    rewrite_value: Any,
    ttl_dict: TTLDict
) -> None:
    ttl_dict.set(key, value)

    assert ttl_dict.set(key, rewrite_value) is True
    assert MOCKED_DICT.get(key) == (None, rewrite_value)


@pytest.mark.parametrize('key,value', [
    ('hello', 'world'),
])
def test_add_value_to_dict(
    key: Hashable,
    value: Any,
    ttl_dict: TTLDict
):
    assert ttl_dict.add(key, value) is True
    assert key in MOCKED_DICT
    assert MOCKED_DICT.get(key) == (None, value)


@pytest.mark.parametrize('key,value,rewrite_value', [
    ('hello', 'world', 'kitty'),
])
def test_add_should_return_false_if_key_exists(
    key: Hashable,
    value: Any,
    rewrite_value: Any,
    ttl_dict: TTLDict
) -> None:
    ttl_dict.add(key, value)

    assert ttl_dict.add(key, rewrite_value) is False
    assert MOCKED_DICT.get(key) == (None, value)


@pytest.mark.parametrize('key,value', [
    ('hello', 'world'),
])
def test_get_should_return_value_if_exists(
    key: Hashable,
    value: Any,
    ttl_dict: TTLDict
) -> None:
    ttl_dict.set(key, value)

    assert ttl_dict.get(key) == value


@pytest.mark.parametrize('key,default', [
    ('hello', 'WOW'),
])
def test_get_should_return_default_if_key_not_exists(
    key: Hashable,
    default: Any,
    ttl_dict: TTLDict
) -> None:
    assert ttl_dict.get(key, default) == default


@pytest.mark.parametrize('key,value', [
    ('hello', 'world'),
])
def test_delete_should_remove_key(
    key: Hashable,
    value: Any,
    ttl_dict: TTLDict
) -> None:
    ttl_dict.set(key, value)
    ttl_dict.delete(key)

    assert key not in MOCKED_DICT


def test_flush_should_remove_all_keys(ttl_dict: TTLDict) -> None:
    for num in range(10):
        ttl_dict.set(str(num), num)

    ttl_dict.flush()
    assert MOCKED_DICT == {}


@pytest.mark.parametrize('key,value,default', [
    ('hello', 'world', 'WOW'),
])
def test_get_should_return_default_if_ttl_expired(
    key: Hashable,
    value: Any,
    default: Any,
    ttl_dict: TTLDict,
) -> None:
    ttl_dict.set(key, value, ttl=0)

    assert ttl_dict.get(key, default) == default


@pytest.mark.parametrize('key,value', [
    ('hello', 'world'),
])
def test_get_should_return_value_if_ttl_not_expired(
    key: Hashable,
    value: Any,
    ttl_dict: TTLDict,
) -> None:
    ttl_dict.set(key, value, ttl=100)
    assert ttl_dict.get(key, 'NO OOPS') == value


@pytest.mark.parametrize('keys', [
    ('hello', 'world'),
])
def test_key_should_check_for_exists(
    keys: Tuple[Hashable],
    ttl_dict: TTLDict
) -> None:
    for key in keys:
        ttl_dict.set(key, key)

    assert ttl_dict.exists(*keys) is True


@pytest.mark.parametrize('keys,ttl,exists', [
    [('hello', 'world'), 0, False],
    [('hello', 'world'), 100, True],
])
def test_key_should_check_for_exists_with_ttl(
    keys: Tuple[Hashable],
    ttl: int,
    exists: bool,
    ttl_dict: TTLDict
) -> None:
    for key in keys:
        ttl_dict.set(key, key, ttl=ttl)

    assert ttl_dict.exists(*keys) is exists


@pytest.mark.parametrize('keys', [
    ('hello', 'world'),
])
def test_should_return_false_if_keys_not_exist(
    keys: Tuple[Hashable],
    ttl_dict: TTLDict
) -> None:
    assert ttl_dict.exists(*keys) is False


@pytest.mark.parametrize('key,value,ttl,expected', [
    ['hello', 'world', 0, None],
    ['hello', 'world', 10, 'world'],
])
def test_expire_from_cache(
    key: Hashable,
    value: Any,
    ttl: int,
    expected: Any,
    ttl_dict: TTLDict
) -> None:
    ttl_dict.add(key, value)
    ttl_dict.expire(key, ttl)

    assert ttl_dict.get(key) == expected
