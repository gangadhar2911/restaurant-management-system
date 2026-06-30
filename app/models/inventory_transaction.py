from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.core.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id", ondelete="CASCADE"),
        nullable=False
    )

    transaction_type = Column(
        String(30),  # STOCK_IN / STOCK_OUT
        nullable=False
    )

    quantity = Column(
        Numeric(10, 2),
        nullable=False
    )

    note = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships
    ingredient = relationship(
        "Ingredient",
        back_populates="transactions"
    )

    def __repr__(self):
        return f"<InventoryTransaction(id={self.id}, type={self.transaction_type})>"