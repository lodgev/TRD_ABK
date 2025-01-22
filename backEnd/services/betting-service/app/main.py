from fastapi import FastAPI
from app.managing_betts.routes import router as bets_router
# from app.managing_odds.routes import router as odds_router
# from app.managing_bonus.routes import router as bonus_router

app = FastAPI()

# Include routes
app.include_router(bets_router, prefix="/betts", tags=["Bets"])
# app.include_router(odds_router, prefix="/odds", tags=["Odds"])
# app.include_router(bonus_router, prefix="/bonus", tags=["Bonus"])

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Betting Service is running!"}
