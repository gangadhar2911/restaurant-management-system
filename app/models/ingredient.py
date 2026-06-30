from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)

    restaurant_id = Column(
        Integer,
        ForeignKey("restaurants.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    unit = Column(
        String(20),
        nullable=False
    )

    current_stock = Column(
        Numeric(10, 2),
        default=0.00
    )

    min_stock_level = Column(
        Numeric(10, 2),
        default=0.00
    )

    cost_per_unit = Column(
        Numeric(10, 2),
        default=0.00
    )

    is_active = Column(
        Boolean,
        default=True
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

    # Relationships
    restaurant = relationship("Restaurant", back_populates="ingredients")

    transactions = relationship(
        "InventoryTransaction",
        back_populates="ingredient",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Ingredient(id={self.id}, name={self.name})>"