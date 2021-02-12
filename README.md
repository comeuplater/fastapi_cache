# FastAPI Cache

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ec5c44e899943c8920d3c3e31616784)](https://app.codacy.com/manual/ivan.sushkov/fastapi_cache?utm_source=github.com&utm_medium=referral&utm_content=comeuplater/fastapi_cache&utm_campaign=Badge_Grade_Dashboard)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPi Version](https://img.shields.io/pypi/v/fastapi-cache.svg)](https://pypi.python.org/pypi/fastapi-cache/)
[![Downloads](https://pepy.tech/badge/fastapi-cache)](https://pepy.tech/project/fastapi-cache)
[![Build Status](https://travis-ci.com/comeuplater/fastapi_cache.svg?branch=master)](https://travis-ci.com/comeuplater/fastapi_cache)

Implements simple lightweight cache system as dependencies in FastAPI.

## Installation

```sh
pip install fastapi-cache
```

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
    in_cache = await cache.get('some_cached_key')
    if not in_cache:
        await cache.set('some_cached_key', 'new_value', 5)

    return {'response': in_cache or 'default'}


@app.on_event('startup')
async def on_startup() -> None:
    rc = RedisCacheBackend('redis://redis')
    caches.set(CACHE_KEY, rc)


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await close_caches()
```

## TODO

*  [X] Add tests
*  [ ] ~~Add registry decorator~~
*  [ ] Add dependency for requests caching

## Acknowledgments

* [Balburdia](https://github.com/Balburdia)
* [xobtoor](https://github.com/xobtoor)
* [jersobh](https://github.com/jersobh)


## Changelog

* 0.0.6 Added typings for backends. Specific arguments now need to be passed through **kwargs.
Set default encoding to utf-8 for redis backend, removed default TTL for redis keys.
  
* 0.1.0 Added TTL support for InMemoryCacheBackend. Added `expire()` method that update ttl value for key.