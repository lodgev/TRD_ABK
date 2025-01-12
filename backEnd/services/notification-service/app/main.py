from fastapi import FastAPI, HTTPException
from app.email_utils import send_email
from pydantic import BaseModel

app = FastAPI()

# schema Api
class EmailRequest(BaseModel):
    recipient_email: str
    subject: str
    message: str

@app.post("/verify-email")
async def send_email_endpoint(request: EmailRequest):
    try:
        send_email(
            recipient_email=request.recipient_email,
            subject=request.subject,
            message=request.message,
        )
        return {"message": "Email sent successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e}")
