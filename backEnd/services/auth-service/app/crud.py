import jwt
import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User
from app.schemas import LoginRequest, LogoutRequest, RegistrationRequest

from werkzeug.security import check_password_hash, generate_password_hash
import uuid
import requests  
import random

SECRET_KEY = "ed73c27f0152572f885e87d1435153c56865d7ee379ffa0c89c6242616effade"  
JWT_EXPIRATION_MINUTES = 60
DOMAIN = "http://auth-service:80"

def current_time_plus_minutes(minutes: int) -> datetime.time:
    now = datetime.datetime.utcnow()
    new_time = (now + datetime.timedelta(minutes=minutes)).time()
    return new_time

def login_user(db: Session, data: LoginRequest):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not check_password_hash(user.password, data.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email is not verified")

    exp_time = int((datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES)).timestamp())

    access_token = jwt.encode(
        {
            "user_id": str(user.id),
            "exp": exp_time,
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

def register_user(db: Session, data: RegistrationRequest):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    new_user = User(
        id=str(uuid.uuid4()),
        email=data.email,
        password=generate_password_hash(data.password),  
        createdat=datetime.datetime.utcnow().time(),
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
            "http://notification-service:80/verify-email",
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


def generate_reset_token():
    reset_token = f"{random.randint(100000, 999999)}"  # 6num token
    expiration = current_time_plus_minutes(15)  # 15-minutes
    return reset_token, expiration

def request_password_reset(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User with this email does not exist.")

    reset_token, expiration = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expiration = expiration
    db.commit()

    # reset_link = f"http://localhost:4444/reset-password/{reset_token}"
    
    try:
        response = requests.post(
            "http://notification-service:80/change-password",
            json={
                "recipient_email": user.email,
                "subject": "Reset your password",
                "message": f"Your password reset code is: {reset_token}"
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to send reset email.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with notification-service: {e}")

    return {"message": "Password reset link sent to your email."}

def reset_password(db: Session, reset_token: str, new_password: str):
    user = db.query(User).filter(User.reset_token == reset_token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token.")

    now = datetime.datetime.utcnow().time()
    if user.reset_token_expiration < now:
        raise HTTPException(status_code=400, detail="Reset token has expired.")

    user.password = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiration = None
    db.commit()


    try:
        response = requests.post(
            "http://notification-service:80/verify-email",
            json={
                "recipient_email": user.email,
                "subject": "Password changed successfully",
                "message": "Your password has been changed successfully.",
            },
            headers={"Content-Type": "application/json"}
        )

        if response.status_code != 200:
            print(f"Failed to send password change confirmation email. Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with notification-service: {e}")

    return {"message": "Password successfully reset and confirmation email sent."}


