from fastapi import APIRouter, Request
import httpx

router = APIRouter()

@router.post("/auth/login")
async def auth_login(request: Request):
    data = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post("http://auth-service/auth/login", json=data)
    return response.json()


