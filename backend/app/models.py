from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Garage
from app.schemas import GarageCreate


router = APIRouter(
    prefix="/api/garages",
    tags=["Garages"]
)


@router.get("/")
def get_garages(db: Session = Depends(get_db)):
    garages = db.query(Garage).all()

    return garages


@router.get("/{garage_id}")
def get_garage(
    garage_id: int,
    db: Session = Depends(get_db)
):
    garage = db.query(Garage).filter(Garage.id == garage_id).first()

    return garage


@router.post("/")
def create_garage(
    garage: GarageCreate,
    db: Session = Depends(get_db)
):
    new_garage = Garage(
        name=garage.name,
        address=garage.address,
        phone=garage.phone,
        rating=garage.rating,
        review_count=garage.review_count
    )

    db.add(new_garage)
    db.commit()
    db.refresh(new_garage)

    return new_garage