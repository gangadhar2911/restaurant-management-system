from typing import Optional

from pydantic import BaseModel, ConfigDict


class NotificationBase(BaseModel):
    user_id: int
    title: str
    message: str
    is_read: bool = False


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)