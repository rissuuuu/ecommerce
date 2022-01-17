import json
from user_components.user.tests.conftest import (
    insert_dummy_into_user,
)
from lib.db_connection import DbConnection
import pytest
from user_components.user.views import views
from lib.json_encoder import jsonable_encoder


@pytest.mark.user
@pytest.mark.asyncio
async def test_user_by_user_id(
    get_db_connection: DbConnection,
    user_id="ABCD",
):
    await insert_dummy_into_user(db=get_db_connection)
    c = await views.get_user(user_id=user_id, db=get_db_connection)
    p = jsonable_encoder(c)
    assert (
        json.dumps(
            {
                "id": p["id"],
                "first_name": "ABCD",
                "last_name": "ABCD",
                "email": "ABCD",
                "user_name": "ABCD",
                "password": "ABCD",
                "is_active": False,
                "phone_number": "8764356786",
                "is_admin": True,
                "is_customer": True,
                "is_seller": False,
                "created_at": "2021-08-06T18:15:00+00:00",
                "updated_at": "2021-08-06T18:15:00+00:00",
            }
        )
        in json.dumps(p)
    )
    await get_db_connection.disconnect()
