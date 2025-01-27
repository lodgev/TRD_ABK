from fastapi import FastAPI
from app.database import Base, engine, additional_engines
from app.routes import router

app = FastAPI()

app.include_router(router)

Base.metadata.create_all(bind=engine)

for db_name, db_engine in additional_engines.items():
    pass

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Recommendation system is running!"}
