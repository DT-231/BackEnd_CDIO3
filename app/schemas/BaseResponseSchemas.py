from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: T

class ErrorResponse(BaseModel):
    code: int
    message: str
    data: str
