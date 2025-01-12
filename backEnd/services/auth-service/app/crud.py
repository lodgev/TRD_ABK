import jwt
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.schemas import LoginRequest, LogoutRequest, RegistrationRequest

# login
from werkzeug.security import check_password_hash

# user registration
from werkzeug.security import generate_password_hash
import uuid

SECRET_KEY = "ed73c27f0152572f885e87d1435153c56865d7ee379ffa0c89c6242616effade"  
JWT_EXPIRATION_MINUTES = 60
DOMAIN = "http://auth-service:80"

def login_user(db: Session, data: LoginRequest):

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # access token
    access_token = jwt.encode(
        {
            "user_id": str(user.id), 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    # refresh token
    refresh_token = jwt.encode(
        {"user_id": str(user.id), "type": "refresh"}, 
        SECRET_KEY,
        algorithm="HS256",
    )

    
    user.refreshtoken = refresh_token
    user.lastsignedinat = datetime.datetime.utcnow()
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token}

def logout_user(db: Session, data: LogoutRequest):
    user = db.query(User).filter(User.id == data.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.refreshtoken = None
    db.commit()

    return {"message": "Successfully logged out"}

def register_user_simple(db: Session, data: RegistrationRequest):
    
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")


    new_user = User(
        id=str(uuid.uuid4()),
        email=data.email,
        password=generate_password_hash(data.password),  
        createdat=datetime.datetime.utcnow(),
        firstname=data.firstname,
        lastname=data.lastname,
        is_verified=True,  
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User successfully created"}