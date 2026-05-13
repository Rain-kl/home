from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Result(BaseModel, Generic[T]):
    code: int
    msg: str
    data: T | None = None


def success(data: T | None = None) -> Result[T]:
    return Result(code=200, msg="success", data=data)


def error(msg: str, code: int = 500, data: T | None = None) -> Result[T]:
    return Result(code=code, msg=msg, data=data)
