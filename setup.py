from os.path import dirname, join

from setuptools import find_packages, setup

from fastapi_cache.version import __author__, __version__

setup(
    name='fastapi-cache',
    version=__version__,
    description='FastAPI simple cache',
    author=__author__,
    url='https://github.com/comeuplater/fastapi_cache',
    packages=find_packages(exclude=('tests',)),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    license='MIT License',
    keywords=[
        'redis', 'aioredis', 'asyncio', 'fastapi', 'starlette', 'cache'
    ],
    install_requires=[
        'aioredis==1.3.1',
    ],
)
