from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditLogRead(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    details: Optional[str]
    ip_address: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True