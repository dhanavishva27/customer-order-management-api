
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, Customer
from app.schemas import (
    OrderCreate,
    OrderSingleResponse,
    OrderListResponse
)


# Router for order endpoints
router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)

# Router for customer-specific order endpoints
customer_orders_router = APIRouter(
    prefix="/api/customers",
    tags=["Orders"]
)


# 1. CREATE ORDER
@router.post(
    "",
    response_model=OrderSingleResponse,
    status_code=201
)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    # Check whether customer exists
    customer = db.query(Customer).filter(
        Customer.id == order.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Create order object
    new_order = Order(**order.model_dump())

    try:
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "message": "Order created successfully",
        "data": new_order
    }


# 2. GET ALL ORDERS
@router.get(
    "",
    response_model=OrderListResponse
)
def get_orders(
    db: Session = Depends(get_db)
):

    orders = db.query(Order).all()

    return {
        "success": True,
        "message": "Orders retrieved successfully",
        "data": orders
    }


# 3. GET CUSTOMER'S ORDERS
@customer_orders_router.get(
    "/{customer_id}/orders",
    response_model=OrderListResponse
)
def get_customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):

    # Check whether customer exists
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Retrieve orders belonging to this customer
    orders = db.query(Order).filter(
        Order.customer_id == customer_id
    ).all()

    return {
        "success": True,
        "message": "Customer orders retrieved successfully",
        "data": orders
    }
