import typing

from lib import unit_of_work
from lib.repository import SqlAlchemyRepository
from lib.db_connection import DbConnection


class UserSQLAlchemyUnitofWork(unit_of_work.SqlAlchemyUnitOfWork):
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[SqlAlchemyRepository],
    ):
        super().__init__(connection, repository_class)
