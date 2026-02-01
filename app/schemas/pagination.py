from pydantic import BaseModel
from typing import Generic, TypeVar, List

#declaring a variable for universality
T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    limit: int
    offset: int