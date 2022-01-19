import typing

from lib import unit_of_work
from lib.db_connection import DbConnection
from lib.repository import SqlAlchemyRepository


class UserSQLAlchemyUnitofWork(unit_of_work.SqlAlchemyUnitOfWork):
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[SqlAlchemyRepository],
    ):
        super().__init__(connection, repository_class)


class OtpSQLAlchemyUnitofWork(unit_of_work.SqlAlchemyUnitOfWork):
    def __init__(
        self,
        connection: DbConnection,
        repository_class: typing.Type[SqlAlchemyRepository],
    ):
        super().__init__(connection, repository_class)
