from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogBase(BaseModel):
    user_id: int
    action: str
    module: str
    description: str


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)