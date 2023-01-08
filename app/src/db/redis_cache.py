"""Create redis db DI function."""
import asyncio
from functools import lru_cache
from time import sleep
from typing import Optional

from db.abstract_cashe import AsyncCacheStorage
from redis.asyncio import Redis

redis_cache: Optional[Redis] = None


class RedisCacher(AsyncCacheStorage):
    """Implements interface to redis db."""

    def __init__(self, rds: Redis):
        """Initialaze constructor redis db interface.

        Args:
            rds (Redis): Redis db object
        """
        self._redis = rds

    async def get(self, key, *args, **kwargs):
        """Get recods from db.

        Args:
            key (str): key_value of records to be returned.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Any : records asoccated with key
        """
        return await self._redis.get(key)

    async def set(
        self,
        key,
        records_value,
        expire=60 * 15,
        **kwargs,
    ):
        """Save records to db.

        Args:
            key (_type_): key of records to be seved.
            records_value (_type_): value to be saved.
            expire (_type_, optional): records keeping period.
            **kwargs: Arbitrary keyword arguments.
        """
        await self._redis.set(
            name=key,
            value=records_value,
            ex=expire,
            **kwargs,
        )

    async def isKeyExist(self, key_name):
        return await self._redis.exists(key_name)


async def get_redis() -> Redis:
    """Функция внедрении зависимостей.

    Returns:
        aioredis.Redis: redis db instance.
    """
    return redis_cache


@lru_cache
def get_redis_cacher() -> RedisCacher:
    """Функция внедрении зависимостей.

    Returns:
        RedisCacher: redis db interface.
    """
    return RedisCacher(redis_cache)
