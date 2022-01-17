import typing
import abc
from lib.db_connection import DbConnection


class Repository(typing.Protocol):
    async def add(self, model):
        raise NotImplementedError()

    async def get(self, ref):
        raise NotImplementedError()


class SqlAlchemyRepository(abc.ABC):
    db: DbConnection

    def __init__(self, db: DbConnection):
        self.db = db

    async def add(self, model):
        await self._add(model)

    @abc.abstractmethod
    async def _add(self, model):
        raise NotImplementedError

    async def get(self, ref):
        raise NotImplementedError
