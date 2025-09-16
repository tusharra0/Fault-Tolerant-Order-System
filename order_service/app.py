from fastapi import FastAPI
from pydantic import BaseModel
from db import SessionLocal, init_db
from models import Order
from publisher import publish_order

app = FastAPI()

class OrderRequest(BaseModel):
    order_id: str
    user_id: str
    items: list
    total: float

@app.post("/orders")
def create_order(order: OrderRequest):
    db = SessionLocal()
    db_order = Order(
        id=order.order_id,
        user_id=order.user_id,
        items=",".join(order.items),  
        total=order.total,
        status="PENDING"
    )
    db.add(db_order)
    db.commit()
    db.close()

    publish_order(order.dict())

    return {"status": "Order received", "order_id": order.order_id}



@app.on_event("startup")
def on_startup():
    init_db()
