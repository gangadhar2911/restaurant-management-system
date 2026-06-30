from datetime import datetime
from sqlalchemy import (
    Column, Integer, ForeignKey,
    DateTime, String, Numeric, Boolean
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    table_id = Column(Integer, ForeignKey("restaurant_tables.id"))

    order_status = Column(String(30), default="Pending")
    total_amount = Column(Numeric(10, 2), default=0.00)
    is_paid = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    customer = relationship(
        "User",
        back_populates="orders"
    )

    restaurant = relationship(
        "Restaurant",
        back_populates="orders"
    )

    table = relationship(
        "RestaurantTable",
        back_populates="orders"
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )