import pytest

from lib.db_connection import DbConnection
from lib.json_encoder import jsonable_encoder
from user_components.user.tests.conftest import insert_dummy_into_user
from user_components.user.views import views


@pytest.mark.user
@pytest.mark.asyncio
async def test_get_all_users(get_db_connection: DbConnection):
    await insert_dummy_into_user(db=get_db_connection)
    c = await views.get_users(db=get_db_connection, page=1)
    p = jsonable_encoder(c)
    assert p is not None
    await get_db_connection.disconnect()
