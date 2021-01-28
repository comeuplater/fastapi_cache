from typing import Union, Optional, AnyStr

import aioredis
from aioredis import Redis

from .base import BaseCacheBackend

DEFAULT_ENCODING = 'utf-8'
DEFAULT_POOL_MIN_SIZE = 5
CACHE_KEY = 'REDIS'

# expected to be of bytearray, bytes, float, int, or str type

RedisKey = Union[AnyStr, float, int]
RedisValue = Union[AnyStr, float, int]


class RedisCacheBackend(BaseCacheBackend[RedisKey, RedisValue]):
    def __init__(
        self,
        address: str,
        pool_minsize: Optional[int] = DEFAULT_POOL_MIN_SIZE,
        encoding: Optional[str] = DEFAULT_ENCODING,
    ) -> None:
        self._redis_address = address
        self._redis_pool_minsize = pool_minsize
        self._encoding = encoding

        self._pool: Optional[Redis] = None

    @property
    async def _client(self) -> Redis:
        if self._pool is None:
            self._pool = await self._create_connection()

        return self._pool

    async def _create_connection(self) -> Redis:
        return await aioredis.create_redis_pool(
            self._redis_address,
            minsize=self._redis_pool_minsize,
        )

    async def add(
        self,
        key: RedisKey,
        value: RedisValue,
        **kwargs
    ) -> bool:
        """
        Bad temporary solution, this approach prone to
        race condition error.

        # TODO: Implement via Lua

        if redis.call("GET", KEYS[1]) then
            return 0
        else
            redis.call("SET", KEYS[1], ARGV[1])
            return 1
        end
        """

        client = await self._client
        in_cache = await client.get(key)

        if in_cache is not None:
            return False

        return await client.set(key, value, **kwargs)

    async def get(
        self,
        key: RedisKey,
        default: RedisValue = None,
        **kwargs,
    ) -> AnyStr:
        kwargs.setdefault('encoding', self._encoding)

        client = await self._client
        cached_value = await client.get(key, **kwargs)

        return cached_value if cached_value is not None else default

    async def set(
        self,
        key: RedisKey,
        value: RedisValue,
        **kwargs,
    ) -> bool:
        client = await self._client

        return await client.set(key, value, **kwargs)

    async def exists(self, *keys: RedisKey) -> bool:
        client = await self._client
        exists = await client.exists(*keys)

        return bool(exists)

    async def delete(self, key: RedisKey) -> bool:
        client = await self._client

        return await client.delete(key)

    async def flush(self) -> None:
        client = await self._client
        await client.flushdb()

    async def expire(
        self,
        key: RedisKey,
        ttl: int
    ) -> bool:
        client = await self._client

        return await client.expire(key, ttl)

    async def close(self) -> None:
        client = await self._client
        client.close()
        await client.wait_closed()
