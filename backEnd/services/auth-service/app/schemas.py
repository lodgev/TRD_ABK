from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class LogoutRequest(BaseModel):
    id: str
    
class LogoutResponse(BaseModel):
    message: str

class RegistrationRequest(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

class RegisterUserResponse(BaseModel):
    message: str