from fastapi_cache.version import __author__, __version__
from setuptools import find_packages, setup

setup(
    name='FastAPI Cache',
    version=__version__,
    description='FastAPI simple cache',
    author=__author__,
    url='https://github.com/comeuplater/fastapi_cache',
    packages=find_packages(),
    license='MIT License',
    keywords=[
        'redis', 'aioredis', 'asyncio', 'fastapi', 'starlette', 'cache'
    ],
    install_requires=[
        'aioredis==1.3.1',
    ],
)
