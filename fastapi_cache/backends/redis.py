from typing import Union, Any

import aioredis
from aioredis import Redis

from .base import BaseCacheBackend

DEFAULT_POOL_MIN_SIZE = 5
CACHE_KEY = 'REDIS'

RedisAcceptable = Union[str, int]


class RedisCacheBackend(BaseCacheBackend[RedisAcceptable, Any]):
    DEFAULT_ENCODING = 'utf-8'

    def __init__(self, address: str, pool_minsize: int = DEFAULT_POOL_MIN_SIZE) -> None:
        self._redis_address = address
        self._redis_pool_minsize = pool_minsize

    @property
    async def _client(self) -> Redis:
        if getattr(self, '_redis_pool', None) is None:
            self._redis_pool = await aioredis.create_redis_pool(
                self._redis_address,
                minsize=self._redis_pool_minsize,
            )

        return self._redis_pool

    async def add(
        self,
        key: RedisAcceptable,
        value: Any,
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
        key: RedisAcceptable,
        default: Any = None,
        **kwargs,
    ) -> Any:
        client = await self._client
        cached_value = await client.get(key, **kwargs)

        return cached_value if cached_value is not None else default

    async def set(
        self,
        key: RedisAcceptable,
        value: Any,
        **kwargs,
    ) -> bool:
        client = await self._client

        return await client.set(key, value, **kwargs)

    async def exists(self, *keys: Union[RedisAcceptable]) -> bool:
        client = await self._client
        exists = await client.exists(*keys)

        return bool(exists)

    async def delete(self, key: RedisAcceptable) -> bool:
        client = await self._client

        return await client.delete(key)

    async def flush(self) -> None:
        client = await self._client
        await client.flushdb()

    async def close(self) -> None:
        client = await self._client
        client.close()
        await client.wait_closed()
