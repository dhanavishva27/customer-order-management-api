
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    ForeignKey,
    func
)

from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    phone = Column(String(15), nullable=True)

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )

    orders = relationship(
        "Order",
        back_populates="customer"
    )


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    order_number = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp()
    )

    customer = relationship(
        "Customer",
        back_populates="orders"
    )
