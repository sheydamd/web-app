from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Review, User, Garage


router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"]
)


@router.post("/")
def create_review(
    user_id: int,
    garage_id: int,
    rating: int,
    comment: str = "",
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

    # Create review
    review = Review(
        user_id=user_id,
        garage_id=garage_id,
        rating=rating,
        comment=comment
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    # Update garage rating
    reviews = db.query(Review).filter(
        Review.garage_id == garage_id
    ).all()

    total_rating = sum(
        review.rating
        for review in reviews
    )

    garage.review_count = len(reviews)
    garage.rating = total_rating / len(reviews)

    db.commit()

    return {
        "message": "Review created successfully",
        "review": {
            "id": review.id,
            "user_id": review.user_id,
            "garage_id": review.garage_id,
            "rating": review.rating,
            "comment": review.comment
        }
    }


@router.get("/garage/{garage_id}")
def get_garage_reviews(
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

    reviews = db.query(Review).filter(
        Review.garage_id == garage_id
    ).all()

    return reviews


@router.get("/{review_id}")
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    review = db.query(Review).filter(
        Review.id == review_id
    ).first()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review