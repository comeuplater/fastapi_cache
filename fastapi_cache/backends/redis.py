from typing import Union

import aioredis
from aioredis import Redis

from .base import BaseCacheBackend, DEFAULT_TIMEOUT

DEFAULT_POOL_MIN_SIZE = 5
CACHE_KEY = 'REDIS'


class RedisCacheBackend(BaseCacheBackend):
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
        key: Union[str, int],
        value: Union[str, int],
        timeout: int = DEFAULT_TIMEOUT
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

        return await client.set(key, value, expire=timeout)

    async def get(
        self,
        key: Union[str, int],
        default: Union[str, int] = None
    ) -> Union[str, int]:
        client = await self._client
        cached_value = await client.get(key, encoding='utf8')

        return cached_value if cached_value is not None else default

    async def set(
        self,
        key: Union[str, int],
        value: Union[str, int],
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        client = await self._client

        return await client.set(key, value, expire=timeout)

    async def delete(self, key: Union[str, int]) -> bool:
        client = await self._client

        return await client.delete(key)

    async def flush(self) -> None:
        client = await self._client
        await client.flushdb()

    async def close(self) -> None:
        client = await self._client
        client.close()
        await client.wait_closed()
