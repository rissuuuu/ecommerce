import pandas as pd
import pytest
import uuid
from user_components.user.domain import model
from user_components.user.domain import command
from user_components.user.adapters.orm import user
from databases import Database
from lib.db_connection import DbConnection
from entrypoint import settings


@pytest.fixture
async def get_db_connection():
    db_settings = settings.settings_factory()
    db = Database(db_settings.pg_dsn, force_rollback=True)
    await db.connect()
    return db


async def insert_dummy_into_user(db: DbConnection):

    query = user.insert()
    values = {
        "id": str(uuid.uuid4()),
        "first_name": "ABCD",
        "last_name": "ABCD",
        "email": "ABCD",
        "user_name": "ABCD",
        "password": "ABCD",
        "phone_number": "8764356786",
        "is_admin": True,
        "is_customer": True,
        "is_seller": False,
        "created_at": pd.to_datetime("2021-08-06T18:15:00+00:00"),
        "updated_at": pd.to_datetime("2021-08-06T18:15:00+00:00"),
    }
    await db.execute(query=query, values=values)


@pytest.fixture
async def model_factory():
    return await model.user_factory(
        first_name="rishav",
        last_name="paudel",
        email="rissuuuu@gmail.com",
        user_name="rissuuuu",
        password="abcd1234efgh",
        phone_number="8897065512",
        is_admin=True,
        is_customer=True,
        is_seller=False,
    )


@pytest.fixture
async def add_user_command():
    return command.AddUser(
        first_name="rishav",
        last_name="paudel",
        email="rissuuuu@gmail.com",
        user_name="rissuuuu",
        password="abcd1234efgh",
        phone_number="8897065512",
        is_admin=True,
        is_customer=True,
        is_seller=False,
    )
