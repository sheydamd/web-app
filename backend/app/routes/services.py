from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Service


router = APIRouter(
    prefix="/api/services",
    tags=["Services"]
)


@router.get("/")
def get_services(
    db: Session = Depends(get_db)
):
    services = db.query(Service).all()

    return services


@router.get("/{service_id}")
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    return service