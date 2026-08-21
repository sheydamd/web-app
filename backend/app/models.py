from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Garage(Base):
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    rating = Column(Float, default=0)