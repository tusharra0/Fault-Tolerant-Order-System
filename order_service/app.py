from fastapi import FastAPI
from pydantic import BaseModel
import pika
import json 
app = FastAPI()

class Order(BaseModel):
    order_id: str
    user_id:str
    items: list
    total:float


def publish_order(order: dict):
    
    # connection to RaabitMQ

    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

    channel = connection.channel()
    channel.exchange_declare(exchange="orders", exchange_type="topic")


    channel.basic_publish(

        exchange = "orders",
        routing_key = "order.created",
        body=json.dumps(order).encode("uft-8")
    )
    connection.close()

@app.post("/orders")
def create_order(order:Order):

    publish_order(order.model_dump())
    return {"status":"Order received", "order_id":order.order_id}