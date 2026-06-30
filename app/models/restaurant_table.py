from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id = Column(Integer, primary_key=True, index=True)

    table_number = Column(String(20))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))

    orders = relationship(
        "Order",
        back_populates="table"
    )