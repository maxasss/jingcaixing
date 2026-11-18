from typing import Generic, TypeVar
from pydantic import BaseModel
T = TypeVar("T")
class ApiResponse(BaseModel, Generic[T]):
    code: int | str = 0
    message: str = "ok"
    data: T | None = None
