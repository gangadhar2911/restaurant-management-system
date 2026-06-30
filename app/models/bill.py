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


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False
    )

    bill_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    subtotal = Column(
        Numeric(10, 2),
        default=0.00
    )

    tax_amount = Column(
        Numeric(10, 2),
        default=0.00
    )

    discount_amount = Column(
        Numeric(10, 2),
        default=0.00
    )

    total_amount = Column(
        Numeric(10, 2),
        default=0.00
    )

    is_paid = Column(
        Boolean,
        default=False
    )

    payment_status = Column(
        String(30),
        default="Pending"
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
    order = relationship("Order")
    payments = relationship(
        "Payment",
        back_populates="bill",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Bill(id={self.id}, bill_number={self.bill_number})>"