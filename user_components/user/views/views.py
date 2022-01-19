from sanic import Sanic

from lib.db_connection import DbConnection
from lib.paginator import Paginator
from user_components.user.adapters import orm

app = Sanic.get_app()


async def get_user_by_email(email: str, db: DbConnection):
    result = await db.fetch_one(orm.user.select().where(orm.user.c.email == email))
    return result


async def get_user_by_uuid(id: str, db: DbConnection):
    result = await db.fetch_one(orm.user.select().where(orm.user.c.id == id))
    return result


async def check_user_by_username(username: str, db: DbConnection):
    result = await db.fetch_one(
        orm.user.select().where(orm.user.c.user_name == username)
    )
    return result


async def get_users(db: DbConnection, page: int):
    query = orm.user.select()
    paginated_query = await Paginator().paginate(query=query, page=page)
    return await db.fetch_all(query=paginated_query)


async def get_user(user_id: str, db: DbConnection):
    query = orm.user.select().where(orm.user.c.user_name == user_id)
    result = await db.fetch_one(query=query)
    return result
