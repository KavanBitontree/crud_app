from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import engine
from models import Base
from routes.auth import router as auth_router
from routes.car import router as car_router
from routes.fuel import router as fuel_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="FastAPI Backend", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(car_router)
app.include_router(fuel_router)


@app.get("/", tags=["Home"])
def root():
    return {"message": "Welcome to the FastAPI Backend"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
