# fastapi_cache

## Usage example
```python
from fastapi import Depends, FastAPI

from fastapi_cache import caches, close_caches
from fastapi_cache.backends.redis import CACHE_KEY, RedisCacheBackend

app = FastAPI()


def redis_cache():
    return caches.get(CACHE_KEY)


@app.get('/')
async def hello(
    cache: RedisCacheBackend = Depends(redis_cache)
):
    in_cache = await cache.get('some_cached_key', 'default')
    if not in_cache:
        await cache.set('some_cached_key', 'new_value', 5)

    return {'response': in_cache}


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://redis')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
```