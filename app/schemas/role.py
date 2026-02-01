from pydantic import BaseModel
from typing import List, Optional

class RoleRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    permissions: List[str]

    class Config:
        from_attributes = True