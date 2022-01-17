import pytest
from entrypoint.settings import settings_factory
from databases import Database


@pytest.fixture
async def get_db_connection():
    db_settings = settings_factory()
    db = Database(db_settings.pg_dsn, force_rollback=True)
    await db.connect()
    return db
