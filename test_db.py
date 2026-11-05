from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT DATABASE()")
        )

        database_name = result.scalar()

        print("Database connected successfully!")
        print("Connected Database:", database_name)

except Exception as e:
    print("Database connection failed!")
    print("Error:", e)

from app.database import SessionLocal
from app.models import Customer, Order

db = SessionLocal()

try:

    customers = db.query(Customer).all()
    orders = db.query(Order).all()

    print("Models connected successfully!")

    print("Total customers:", len(customers))
    print("Total orders:", len(orders))

except Exception as e:

    print("Error:", e)

finally:

    db.close()