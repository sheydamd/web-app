from fastapi import FastAPI
from app.routes import services
from app.database import engine, Base
from app import models
from app.routes import garages


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CarFix API",
    description="API for finding and comparing car repair shops",
    version="1.0.0",
)


app.include_router(garages.router)
app.include_router(services.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CarFix API"
    }