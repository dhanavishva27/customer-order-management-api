
from fastapi import FastAPI, Depends

from app import auth
from app.routes import customers, orders


app = FastAPI(
    title="Customer & Order Management API",
    description="REST API for managing customers and orders",
    version="1.0.0"
)


# Root endpoint (public)
@app.get("/")
def home():

    return {
        "success": True,
        "message": "Customer & Order Management API is running"
    }


# Login endpoint (public)
app.include_router(auth.router)


# Customer endpoints (protected)
app.include_router(
    customers.router,
    dependencies=[Depends(auth.get_current_user)]
)


# Order endpoints (protected)
app.include_router(
    orders.router,
    dependencies=[Depends(auth.get_current_user)]
)


# Customer-specific order endpoints (protected)
app.include_router(
    orders.customer_orders_router,
    dependencies=[Depends(auth.get_current_user)]
)
