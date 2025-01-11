# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Gateway Service")

# Підключення маршрутів
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "OK", "message": "Gateway Service is running!"}
