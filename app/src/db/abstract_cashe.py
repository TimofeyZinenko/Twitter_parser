"""Difine abstract Cashe Storage."""
from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    """Storage abstract class."""

    @abstractmethod
    async def get(self, key: str, **kwargs):
        """_Abstract method to get recods from db.

        Args:
            key (str): key of records to be returned.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError:  Reaise in a case the method is not implemented
        """
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, record_value: str, expire: int, **kwargs):
        """Abstract method to save records to db.

        Args:
            key (str): key of records to be seved.
            record_value (str): value to be saved.
            expire (int): records keeping period.
            **kwargs: Arbitrary keyword arguments.

        Raises:
            NotImplementedError: Reaise in a case the method is not implemented
        """
        raise NotImplementedError
