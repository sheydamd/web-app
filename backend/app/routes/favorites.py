from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FavoriteGarage, User, Garage


router = APIRouter(
    prefix="/api/favorites",
    tags=["Favorites"]
)


@router.post("/")
def add_favorite(
    user_id: int,
    garage_id: int,
    db: Session = Depends(get_db)
):
    # Check user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check garage
    garage = db.query(Garage).filter(
        Garage.id == garage_id
    ).first()

    if garage is None:
        raise HTTPException(
            status_code=404,
            detail="Garage not found"
        )

    # Check existing favorite
    existing_favorite = db.query(
        FavoriteGarage
    ).filter(
        FavoriteGarage.user_id == user_id,
        FavoriteGarage.garage_id == garage_id
    ).first()

    if existing_favorite:
        raise HTTPException(
            status_code=400,
            detail="Garage already in favorites"
        )

    favorite = FavoriteGarage(
        user_id=user_id,
        garage_id=garage_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)

    return {
        "message": "Garage added to favorites",
        "favorite": {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "garage_id": favorite.garage_id
        }
    }


@router.get("/user/{user_id}")
def get_user_favorites(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    favorites = db.query(
        FavoriteGarage
    ).filter(
        FavoriteGarage.user_id == user_id
    ).all()

    return favorites


@router.delete("/")
def remove_favorite(
    user_id: int,
    garage_id: int,
    db: Session = Depends(get_db)
):
    favorite = db.query(
        FavoriteGarage
    ).filter(
        FavoriteGarage.user_id == user_id,
        FavoriteGarage.garage_id == garage_id
    ).first()

    if favorite is None:
        raise HTTPException(
            status_code=404,
            detail="Favorite not found"
        )

    db.delete(favorite)
    db.commit()

    return {
        "message": "Garage removed from favorites"
    }