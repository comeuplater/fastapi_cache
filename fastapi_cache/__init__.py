from .registry import CacheRegistry

caches = CacheRegistry


async def close_caches():
    for cache in caches.all():
        await cache.close()
