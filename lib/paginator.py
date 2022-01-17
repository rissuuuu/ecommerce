import sqlalchemy

from entrypoint.settings import settings_factory

size = settings_factory().page_size


class Paginator:
    def __init__(self):
        self.size = size

    async def paginate(self, query: sqlalchemy.select, page: int):
        offset = (page - 1) * self.size
        return query.limit(self.size).offset(offset)
