from typing import Optional

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
    city: Optional[str] = None,
    name: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Garage)

    # Filter by city
    if city:
        query = query.filter(
            Garage.city == city
        )

    # Search by garage name
    if name:
        query = query.filter(
            Garage.name.ilike(
                f"%{name}%"
            )
        )

    # Pagination
    skip = (page - 1) * limit

    garages = query.offset(skip).limit(limit).all()

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