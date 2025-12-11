from fastapi import FastAPI

app = FastAPI(title="Postgres + FastAPI Test App")

from routes.car import router as car_router
app.include_router(car_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Postgres + FastAPI Test App"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000,reload=True)
