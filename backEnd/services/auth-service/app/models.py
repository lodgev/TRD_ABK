from sqlalchemy import Column, String, Time, Boolean
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    refreshtoken = Column(String) 
    createdat = Column(Time)
    updatedat = Column(Time, nullable=True)
    lastsigninat = Column(Time, nullable=True)
    firstname = Column(String)
    lastname = Column(String)
    is_verified = Column(Boolean, default=False)
    reset_token = Column(String)
    reset_token_expiration = Column(Time)
    
