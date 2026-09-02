from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GarageService, Garage, Service


router = APIRouter(
    prefix="/api/garage-services",
    tags=["Garage Services"]
)


@router.get("/")
def get_garage_services(
    db: Session = Depends(get_db)
):
    garage_services = db.query(
        GarageService
    ).all()

    return garage_services


@router.get("/{garage_service_id}")
def get_garage_service(
    garage_service_id: int,
    db: Session = Depends(get_db)
):
    garage_service = db.query(
        GarageService
    ).filter(
        GarageService.id == garage_service_id
    ).first()

    if garage_service is None:
        raise HTTPException(
            status_code=404,
            detail="Garage service not found"
        )

    return garage_service


@router.get("/garage/{garage_id}")
def get_garage_services_by_garage(
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

    services = db.query(
        GarageService
    ).filter(
        GarageService.garage_id == garage_id
    ).all()

    return services


@router.get("/service/{service_id}")
def get_garages_by_service(
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

    garages = db.query(
        GarageService
    ).filter(
        GarageService.service_id == service_id
    ).all()

    return garages


@router.post("/")
def create_garage_service(
    garage_id: int,
    service_id: int,
    price_min: int | None = None,
    price_max: int | None = None,
    duration: str | None = None,
    db: Session = Depends(get_db)
):
    # Check garage
    garage = db.query(Garage).filter(
        Garage.id == garage_id
    ).first()

    if garage is None:
        raise HTTPException(
            status_code=404,
            detail="Garage not found"
        )

    # Check service
    service = db.query(Service).filter(
        Service.id == service_id
    ).first()

    if service is None:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )

    # Check duplicate relationship
    existing = db.query(
        GarageService
    ).filter(
        GarageService.garage_id == garage_id,
        GarageService.service_id == service_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="This service already exists for this garage"
        )

    garage_service = GarageService(
        garage_id=garage_id,
        service_id=service_id,
        price_min=price_min,
        price_max=price_max,
        duration=duration
    )

    db.add(garage_service)
    db.commit()
    db.refresh(garage_service)

    return {
        "message": "Garage service created successfully",
        "garage_service": garage_service
    }


@router.delete("/{garage_service_id}")
def delete_garage_service(
    garage_service_id: int,
    db: Session = Depends(get_db)
):
    garage_service = db.query(
        GarageService
    ).filter(
        GarageService.id == garage_service_id
    ).first()

    if garage_service is None:
        raise HTTPException(
            status_code=404,
            detail="Garage service not found"
        )

    db.delete(garage_service)
    db.commit()

    return {
        "message": "Garage service deleted successfully"
    }