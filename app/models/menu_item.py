from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text,
    Numeric, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    item_name = Column(String(150))
    description = Column(Text)
    price = Column(Numeric(10, 2))
    image = Column(String(255))
    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    order_items = relationship(
        "OrderItem",
        back_populates="menu_item"
    )