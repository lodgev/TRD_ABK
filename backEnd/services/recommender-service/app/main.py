from fastapi import FastAPI
from app.database import RecommenderBase, UserBase, MatchBase, BettingBase, recommender_engine, betting_engine, match_engine, user_engine
from app.routes import router

app = FastAPI()

app.include_router(router)

RecommenderBase.metadata.create_all(bind=recommender_engine)
UserBase.metadata.create_all(bind=user_engine)
MatchBase.metadata.create_all(bind=match_engine)
BettingBase.metadata.create_all(bind=betting_engine)


# for db_name, db_engine in additional_engines.items():
#     pass

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Recommendation system is running!"}
