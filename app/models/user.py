from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    password = Column(String(255))
    role_id = Column(Integer)

    # relationships
    orders = relationship(
        "Order",
        back_populates="customer"
    )