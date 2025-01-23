from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from datetime import datetime

class UserAction(Base):
    __tablename__ = "user_actions"

    click_id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, nullable=False)
    user_id = Column(UUID, nullable=False)
    action = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
