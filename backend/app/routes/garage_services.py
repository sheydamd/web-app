from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GarageService


router = APIRouter(
    prefix="/api/garage-services",
    tags=["Garage Services"]
)


@router.get("/")
def get_garage_services(
    db: Session = Depends(get_db)
):
    services = db.query(GarageService).all()

    return services


@router.get("/{garage_service_id}")
def get_garage_service(
    garage_service_id: int,
    db: Session = Depends(get_db)
):
    garage_service = db.query(GarageService).filter(
        GarageService.id == garage_service_id
    ).first()

    if garage_service is None:
        raise HTTPException(
            status_code=404,
            detail="Garage service not found"
        )

    return garage_service