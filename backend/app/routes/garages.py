from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Garage


router = APIRouter(
    prefix="/api/garages",
    tags=["Garages"]
)


@router.get("/")
def get_garages(
    db: Session = Depends(get_db)
):
    garages = db.query(Garage).all()

    return garages


@router.get("/{garage_id}")
def get_garage(
    garage_id: int,
    db: Session = Depends(get_db)
):
    garage = db.query(Garage).filter(
        Garage.id == garage_id
    ).first()

    if garage is None:
        raise HTTPException(
            status_code=404,
            detail="Garage not found"
        )

    return garage