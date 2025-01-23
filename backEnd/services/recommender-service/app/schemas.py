from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class UserActionCreate(BaseModel):
    club_id: int
    user_id: UUID
    action: str

    class Config:
        orm_mode = True

class UserActionResponse(BaseModel):
    click_id: int
    club_id: int
    user_id: UUID
    action: str
    timestamp: datetime

    class Config:
        orm_mode = True
