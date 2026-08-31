from pydantic import BaseModel


class GarageCreate(BaseModel):
    name: str
    address: str
    phone: str | None = None
    rating: float = 0
    review_count: int = 0