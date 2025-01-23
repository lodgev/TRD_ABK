# from fastapi import FastAPI
# # from app.routes import router
#
# app = FastAPI(title="Deposit Service")
#
# # Підключення маршрутів
# # app.include_router(router)
#
# @app.get("/")
# def health_check():
#     return {"status": "OK", "message": "Deposit Service is running!"}

#
# from fastapi import FastAPI
# from app.managing_betts.routes import router as bets_router
#
# app = FastAPI()
#
# # Include routes
# app.include_router(bets_router, prefix="/betts", tags=["Bets"])
# # app.include_router(odds_router, prefix="/odds", tags=["Odds"])
# # app.include_router(bonus_router, prefix="/bonus", tags=["Bonus"])
#
# @app.get("/")
# def health_check():
#     return {"status": "OK", "message": "Betting Service is running!"}
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Withdrawal Service is running!"}
