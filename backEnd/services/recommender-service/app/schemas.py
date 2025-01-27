from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum
from typing import Union

# Enum for action types
class ActionEnum(str, Enum):
    liked = "liked"
    disliked = "disliked"

# Feedback models
# class FeedbackBase(BaseModel):
#     user_id: UUID
#     news_id: UUID
#     action: str
#     rating: int | None = None

# class FeedbackCreate(FeedbackBase):
#     timestamp: datetime | None = None



class FeedbackBase(BaseModel):
    user_id: UUID
    news_id: UUID
    action: str
    rating: Union[int, None] = None  # Use Union[int, None] instead of int | None

class FeedbackCreate(FeedbackBase):
    timestamp: Union[datetime, None] = None  # Use Union[datetime, None] instead of datetime | None


class Feedback(FeedbackBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

# UserAction models
class UserActionCreate(BaseModel):
    club_id: int
    user_id: UUID
    action: ActionEnum

    class Config:
        orm_mode = True

class UserActionResponse(BaseModel):
    click_id: int
    club_id: int
    user_id: UUID
    action: ActionEnum
    timestamp: datetime

    class Config:
        orm_mode = True

# SportNews models
# class SportNewsBase(BaseModel):
#     team_id: int
#     news_id: str
#     title: str
#     image_url: str | None = None
#     published_time: datetime
#     source: str
#     url: str
#     content: str | None = None

class SportNewsBase(BaseModel):
    team_id: int
    news_id: str
    title: str
    image_url: Union[str, None] = None  
    published_time: datetime
    source: str
    url: str
    content: Union[str, None] = None  

class SportNewsCreate(SportNewsBase):
    pass

class SportNews(SportNewsBase):
    class Config:
        orm_mode = True
