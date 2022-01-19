from __future__ import annotations

import pytest

from entrypoint import messagebus, settings
from user_components.user.domain import command
from user_components.user.tests.unit.test_handlers import FakeUnitOfWork
from user_components.user.views import views

db = settings.settings_factory().pg_dsn


@pytest.mark.unit_test
@pytest.mark.asyncio
async def test_get_user_by_email():
    uow = FakeUnitOfWork()
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    assert views.get_user_by_email("p@gmail.com", db)


@pytest.mark.unit_test
@pytest.mark.asyncio
async def test_get_user_by_uuid():
    uow = FakeUnitOfWork()
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    assert views.get_user_by_uuid("d9369a07-74e5-4329-b1ee-9d2708bfdbd9", db)


@pytest.mark.unit_test
@pytest.mark.asyncio
async def test_get_user_by_user_name():
    uow = FakeUnitOfWork()
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    await messagebus.handle(
        message=command.AddUser(
            first_name="prabin",
            last_name="tharu",
            email="p@gmail.com",
            user_name="pbnthru",
            password="p12345",
            phone_number="987645055",
        ),
        uow=uow,
    )
    assert views.check_user_by_username("pbnthru", db)
