from fastapi import FastAPI

from app.routes import garages


app = FastAPI(
    title="CarFix API",
    description="API for finding and comparing car repair shops",
    version="1.0.0",
)


app.include_router(garages.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to CarFix API"
    }