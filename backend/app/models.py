from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    reviews = relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    favorites = relationship(
        "FavoriteGarage",
        back_populates="user",
        cascade="all, delete-orphan"
    )


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

    services = relationship(
        "GarageService",
        back_populates="garage",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "Review",
        back_populates="garage",
        cascade="all, delete-orphan"
    )

    favorites = relationship(
        "FavoriteGarage",
        back_populates="garage",
        cascade="all, delete-orphan"
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

    garages = relationship(
        "GarageService",
        back_populates="service",
        cascade="all, delete-orphan"
    )


class GarageService(Base):
    __tablename__ = "garage_services"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    garage_id = Column(
        Integer,
        ForeignKey("garages.id"),
        nullable=False
    )

    service_id = Column(
        Integer,
        ForeignKey("services.id"),
        nullable=False
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

    garage = relationship(
        "Garage",
        back_populates="services"
    )

    service = relationship(
        "Service",
        back_populates="garages"
    )

    __table_args__ = (
        UniqueConstraint(
            "garage_id",
            "service_id",
            name="unique_garage_service"
        ),
    )


class Review(Base):
    __tablename__ = "reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    garage_id = Column(
        Integer,
        ForeignKey("garages.id"),
        nullable=False
    )

    rating = Column(Integer,
        nullable=False
    )

    comment = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User",
        back_populates="reviews"
    )

    garage = relationship(
        "Garage",
        back_populates="reviews"
    )


class FavoriteGarage(Base):
    __tablename__ = "favorite_garages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    garage_id = Column(
        Integer,
        ForeignKey("garages.id"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="favorites"
    )

    garage = relationship(
        "Garage",
        back_populates="favorites"
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "garage_id",
            name="unique_user_garage_favorite"
        ),
    )