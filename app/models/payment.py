from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    bill_id = Column(
        Integer,
        ForeignKey("bills.id", ondelete="CASCADE"),
        nullable=False
    )

    payment_method = Column(
        String(30),
        nullable=False
    )

    payment_status = Column(
        String(30),
        default="Success"
    )

    amount_paid = Column(
        Numeric(10, 2),
        nullable=False
    )

    transaction_id = Column(
        String(100),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Relationships
    bill = relationship(
        "Bill",
        back_populates="payments"
    )

    def __repr__(self):
        return f"<Payment(id={self.id}, amount={self.amount_paid})>"