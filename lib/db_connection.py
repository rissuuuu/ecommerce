from __future__ import annotations
import typing


class DbConnection(typing.Protocol):
    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()

    async def transaction(self):
        raise NotImplementedError()

    async def execute(self, query, values=None):
        raise NotImplementedError()

    async def execute_many(self, query, values):
        raise NotImplementedError()

    async def fetch_all(self, query):
        raise NotImplementedError()

    async def fetch_one(self, query):
        raise NotImplementedError()

    async def fetch_val(self, query):
        raise NotImplementedError()
