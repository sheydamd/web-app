from fastapi import APIRouter

router = APIRouter(
    prefix="/api/garages",
    tags=["Garages"]
)


@router.get("/")
def get_garages():
    return [
        {
            "id": 1,
            "name": "تعمیرگاه علی",
            "address": "تهران، صادقیه",
            "rating": 4.5
        },
        {
            "id": 2,
            "name": "تعمیرگاه محمد",
            "address": "تهران، ستارخان",
            "rating": 4.2
        }
    ]