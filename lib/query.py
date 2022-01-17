from pydantic import BaseModel, fields, validator
import typing
import uuid
from datetime import date


class QueryParamModel(BaseModel):
    q: typing.Optional[str]
    id: typing.Optional[uuid.UUID]
    id_: typing.Optional[str]
    sort: typing.Optional[str]
    date: typing.Optional[date]
    columns: typing.Optional[str]
    order: typing.Literal["asc", "desc"] = fields.Field("asc")
    next: typing.Optional[str]
    prev: typing.Optional[str]
    num: int = fields.Field(10, ge=5, le=25)
    page: typing.Optional[int] = 1

    class Config:
        validate_assignment = True

    @validator("page")
    def set_page(cls, page):
        return page or 1
