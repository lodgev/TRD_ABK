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
import requests  

SECRET_KEY = "ed73c27f0152572f885e87d1435153c56865d7ee379ffa0c89c6242616effade"  
JWT_EXPIRATION_MINUTES = 60
DOMAIN = "http://auth-service:80"

# def login_user(db: Session, data: LoginRequest):

#     user = db.query(User).filter(User.email == data.email).first()
#     if not user or not check_password_hash(user.password, data.password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     # access token
#     access_token = jwt.encode(
#         {
#             "user_id": str(user.id), 
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
#         },
#         SECRET_KEY,
#         algorithm="HS256",
#     )

#     # refresh token
#     refresh_token = jwt.encode(
#         {"user_id": str(user.id), "type": "refresh"}, 
#         SECRET_KEY,
#         algorithm="HS256",
#     )

    
#     user.refreshtoken = refresh_token
#     user.lastsignedinat = datetime.datetime.utcnow()
#     db.commit()

#     return {"access_token": access_token, "refresh_token": refresh_token}
def login_user(db: Session, data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Перевірка підтвердження email
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email is not verified")

    # Генерація токенів
    access_token = jwt.encode(
        {
            "user_id": str(user.id), 
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        },
        SECRET_KEY,
        algorithm="HS256",
    )
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

# def register_user_simple(db: Session, data: RegistrationRequest):
    
#     existing_user = db.query(User).filter(User.email == data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User with this email already exists")


#     new_user = User(
#         id=str(uuid.uuid4()),
#         email=data.email,
#         password=generate_password_hash(data.password),  
#         createdat=datetime.datetime.utcnow(),
#         firstname=data.firstname,
#         lastname=data.lastname,
#         is_verified=True,  
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User successfully created"}

def register_user(db: Session, data: RegistrationRequest):

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
        is_verified=False,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    verification_link = f"http://localhost:4444/auth/verify/{new_user.id}"
    try:
        response = requests.post(
            "http://notification-service:80/verify-email",  # URL notification-service
            json={
                "recipient_email": new_user.email,
                "subject": "Verify your email",
                "message": f"Please click the following link to verify your email: {verification_link}",
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            print("Verification email sent successfully")
        else:
            print(f"Failed to send email. Response: {response.text}")
            raise HTTPException(status_code=500, detail="Failed to send verification email")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with notification-service: {e}")
        raise HTTPException(status_code=500, detail="Could not connect to the notification service")

    return {"message": "User successfully created. Verification email sent."}