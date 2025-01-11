from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

# class LogoutRequest(BaseModel):
#     user_id: str
    
# class LogoutResponse(BaseModel):
#     message: str
