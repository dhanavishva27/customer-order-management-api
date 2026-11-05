
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema for creating a customer
class CustomerCreate(BaseModel):

    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=15)


# Schema for updating a customer
class CustomerUpdate(BaseModel):

    name: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    phone: Optional[str] = Field(default=None, max_length=15)


# Schema for returning customer information
class CustomerOut(BaseModel):

    id: int
    name: str
    email: str
    phone: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# Standard response for one customer
class CustomerSingleResponse(BaseModel):

    success: bool
    message: str
    data: CustomerOut


# Standard response for multiple customers
class CustomerListResponse(BaseModel):

    success: bool
    message: str
    data: list[CustomerOut]


from decimal import Decimal


# Schema for creating an order
class OrderCreate(BaseModel):

    customer_id: int
    order_number: str = Field(min_length=1, max_length=50)
    amount: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    status: str = Field(min_length=1, max_length=30)


# Schema for returning order information
class OrderOut(BaseModel):

    id: int
    customer_id: int
    order_number: str
    amount: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# Response for one order
class OrderSingleResponse(BaseModel):

    success: bool
    message: str
    data: OrderOut


# Response for multiple orders
class OrderListResponse(BaseModel):

    success: bool
    message: str
    data: list[OrderOut]


# Login request schema
class LoginRequest(BaseModel):

    username: str
    password: str


# Login response schema
class TokenResponse(BaseModel):

    access_token: str
    token_type: str

class CustomerSummaryData(BaseModel):
    customer: dict
    order_count: int
    total_order_amount: Decimal
    completed_orders: int
    pending_orders: int


class CustomerSummaryResponse(BaseModel):
    success: bool
    data: CustomerSummaryData