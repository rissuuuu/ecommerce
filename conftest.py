import pytest
from databases import Database

from entrypoint.settings import settings_factory


@pytest.fixture
async def get_db_connection():
    db_settings = settings_factory()
    db = Database(db_settings.pg_dsn, force_rollback=True)
    await db.connect()
    return db
