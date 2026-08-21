from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Garage


router = APIRouter(
    prefix="/api/garages",
    tags=["Garages"]
)


@router.get("/")
def get_garages(db: Session = Depends(get_db)):
    garages = db.query(Garage).all()

    return garages