from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy.orm import relationship

from app.core.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )

    table_id = Column(
        Integer,
        ForeignKey("restaurant_tables.id", ondelete="CASCADE"),
        nullable=False
    )

    reservation_date = Column(
        Date,
        nullable=False
    )

    reservation_time = Column(
        Time,
        nullable=False
    )

    number_of_guests = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(30),
        default="Pending"
    )

    special_request = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    customer = relationship(
        "User",
        back_populates="reservations"
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="reservations"
    )

    table = relationship(
        "RestaurantTable",
        back_populates="reservations"
    )

    def __repr__(self):
        return f"<Reservation(id={self.id}, customer={self.customer_id})>"