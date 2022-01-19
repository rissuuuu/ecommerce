import logging

import pytest

from entrypoint.messagebus import messagebus
from lib.repository import Repository

LOGGER = logging.getLogger("logger")


class FakeRepository(Repository):
    def __init__(self, first_name) -> None:
        self.repository = set(first_name)

    async def add(self, model):
        self.repository.add(model)

    async def get(self, ref):
        result = next(
            (p for p in self.repository if p.user_name == ref),
            None,
        )
        result1 = result.dict()
        result1["id"] = result1["id_"]
        result1["first_name"] = result1["first_name"]
        return result1

    async def get_(self, ref):
        result3 = next(
            (p for p in self.repository if p.user_name == ref),
            None,
        )

        return result3

    async def user_email_exists(self, email):
        result3 = next(
            (p for p in self.repository if p.email == email),
            None,
        )

        return result3 is not None

    async def update(self, model):
        self.repository.update(model)


class FakeUnitOfWork:
    def __init__(self):
        self.repository = FakeRepository([])
        self.events = set()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            LOGGER.exception(exc_val)

    def collect_new_events(self):
        for item in self.events.copy():
            yield self.events.pop()

    async def commit(self):
        pass


@pytest.mark.user
@pytest.mark.asyncio
async def test_add_new_user(add_user_command):
    uow = FakeUnitOfWork()
    await messagebus.handle(message=add_user_command, uow=uow)
    assert await uow.repository.get_("pbnthru") is not None
