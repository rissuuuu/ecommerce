from sqlalchemy import Table, Column, INTEGER, String, Date, ForeignKey, event
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)
