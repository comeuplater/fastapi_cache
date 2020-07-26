from typing import Union

DEFAULT_TIMEOUT = 600


class BaseCacheBackend(object):
    async def add(
        self,
        key: Union[str, int],
        value: Union[str, int],
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        raise NotImplementedError

    async def get(
        self, key: Union[str, int],
        default: Union[str, int] = None
    ) -> None:
        raise NotImplementedError

    async def set(
        self, key: Union[str, int],
        value: Union[str, int],
        timeout: int = DEFAULT_TIMEOUT
    ) -> None:
        raise NotImplementedError

    async def delete(self, key: Union[str, int]) -> bool:
        raise NotImplementedError
