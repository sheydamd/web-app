from fastapi import FastAPI

from app.database import Base, engine
from app.routes import garages, services, garage_services
from app.routes import garages, services, garage_services, users
from app.routes import reviews

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CarFix API",
    description="API for finding and comparing car repair shops",
    version="1.0.0",
)


app.include_router(garages.router)
app.include_router(services.router)
app.include_router(garage_services.router)
app.include_router(users.router)
app.include_router(reviews.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to CarFix API"
    }