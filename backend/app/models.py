from sqlalchemy import Column, Integer, String, Float, Boolean, Text

from app.database import Base


class Garage(Base):
    __tablename__ = "garages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    city = Column(
        String,
        nullable=True
    )

    latitude = Column(
        Float,
        nullable=True
    )

    longitude = Column(
        Float,
        nullable=True
    )

    rating = Column(
        Float,
        default=0
    )

    review_count = Column(
        Integer,
        default=0
    )

    website = Column(
        String,
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    source = Column(
        String,
        nullable=True
    )

class Service(Base):
    __tablename__ = "services"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    price_min = Column(
        Integer,
        nullable=True
    )

    price_max = Column(
        Integer,
        nullable=True
    )

    duration = Column(
        String,
        nullable=True
    )