from __future__ import annotations

import logging
import typing
from abc import abstractmethod

from lib import repository
from lib.db_connection import DbConnection

LOGGER = logging.getLogger("logger")


class UnitOfWork(typing.AsyncContextManager, typing.Protocol):
    repository: repository

    @abstractmethod
    async def __aenter__(self) -> UnitOfWork:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def subunit(self):
        raise NotImplementedError()


class SqlAlchemyUnitOfWork:
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[repository.SqlAlchemyRepository],
    ):
        self._transactions = []
        self.connection = connection
        self.repository = repository_class(self.connection)
        self.events = set()

    def subunit(self, klass):
        return klass(self.connection)

    async def commit(self):
        _transaction = self._transactions.pop()
        await _transaction.commit()
        pass

    async def rollback(self):
        pass
        _transaction = self._transactions.pop()
        await _transaction.rollback()

    def collect_new_events(self):
        for item in self.events.copy():
            yield self.events.pop()

    async def __aenter__(self):
        _transaction = self.connection.transaction()
        self._transactions.append(_transaction)
        await _transaction.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            LOGGER.exception(exc_val)
            await self.rollback()
        else:
            await self.commit()
