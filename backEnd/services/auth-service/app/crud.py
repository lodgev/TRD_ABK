import jwt
import datetime
from werkzeug.security import check_password_hash
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.schemas import LoginRequest

SECRET_KEY = "ed73c27f0152572f885e87d1435153c56865d7ee379ffa0c89c6242616effade"  
JWT_EXPIRATION_MINUTES = 60

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

# def logout_user(db: Session, user_id: str):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Очистимо refresh token
#     user.refreshtoken = None
#     db.commit()

#     return {"message": "Successfully logged out"}