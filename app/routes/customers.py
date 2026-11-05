from app.models import Customer, Order
from app.schemas import CustomerSummaryResponse
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, case
from app.database import get_db
from app.models import Customer
from app.schemas import (
    CustomerCreate,
    CustomerSummaryResponse,
    CustomerUpdate,
    CustomerSingleResponse,
    CustomerListResponse
)


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"]
)


# 1. CREATE CUSTOMER
@router.post(
    "",
    response_model=CustomerSingleResponse,
    status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    new_customer = Customer(**customer.model_dump())

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "success": True,
        "message": "Customer created successfully",
        "data": new_customer
    }


# 2. GET ALL CUSTOMERS
@router.get(
    "",
    response_model=CustomerListResponse
)
def get_customers(db: Session = Depends(get_db)):

    customers = db.query(Customer).all()

    return {
        "success": True,
        "message": "Customers retrieved successfully",
        "data": customers
    }


# 3. GET CUSTOMER BY ID
@router.get(
    "/{customer_id}",
    response_model=CustomerSingleResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "success": True,
        "message": "Customer retrieved successfully",
        "data": customer
    }


# 4. UPDATE CUSTOMER
@router.put(
    "/{customer_id}",
    response_model=CustomerSingleResponse
)
def update_customer(
    customer_id: int,
    updated_data: CustomerUpdate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.name = updated_data.name
    customer.email = updated_data.email
    customer.phone = updated_data.phone

    db.commit()
    db.refresh(customer)

    return {
        "success": True,
        "message": "Customer updated successfully",
        "data": customer
    }


# 5. DELETE CUSTOMER
@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Cannot delete customer because orders exist"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/{customer_id}/summary", response_model=CustomerSummaryResponse)
def get_customer_summary(
    customer_id: int,
    db: Session = Depends(get_db)
):
    # Check whether the customer exists
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Calculate order summary
    summary = db.query(
        func.count(Order.id).label("order_count"),

        func.coalesce(
            func.sum(Order.amount), 0
        ).label("total_order_amount"),

        func.sum(
            case(
                (Order.status == "completed", 1),
                else_=0
            )
        ).label("completed_orders"),

        func.sum(
            case(
                (Order.status == "pending", 1),
                else_=0
            )
        ).label("pending_orders")

    ).filter(
        Order.customer_id == customer_id
    ).first()

    return {
        "success": True,
        "data": {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "phone": customer.phone
            },
            "order_count": summary.order_count,
            "total_order_amount": summary.total_order_amount,
            "completed_orders": summary.completed_orders or 0,
            "pending_orders": summary.pending_orders or 0
        }
    }