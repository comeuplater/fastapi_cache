from typing import Any, Union

DEFAULT_TIMEOUT = 600


class BaseCacheBackend(object):
    async def add(
        self,
        key: Union[str, int],
        value: Any,
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        raise NotImplementedError

    async def get(
        self,
        key: Union[str, int],
        default: Any = None,
        **kwargs
    ) -> Any:
        raise NotImplementedError

    async def set(
        self,
        key: Union[str, int],
        value: Any,
        timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        raise NotImplementedError

    async def delete(self, key: Union[str, int]) -> bool:
        raise NotImplementedError

    async def flush(self) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError
