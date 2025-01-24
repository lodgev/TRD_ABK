
from fastapi import FastAPI
from app.database import WalletBase, wallet_engine, BettsBase, betts_engine
from app.routes import router

app = FastAPI()

app.include_router(router)

# Base.metadata.create_all(bind=engine)

WalletBase.metadata.create_all(bind=wallet_engine)
BettsBase.metadata.create_all(bind=betts_engine)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Usage Service is running!"}


