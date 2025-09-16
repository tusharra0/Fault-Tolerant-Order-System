import pika
import json
import time
from db import SessionLocal
from models import Payment


def callback(ch, method, properties, body):
    order = json.loads(body.decode("utf-8"))
    print(f"[x] Payment Service received: {order}")

    db = SessionLocal()
    try:
        payment = Payment(order_id=order["order_id"], authorized=True)
        db.add(payment)
        db.commit()
    finally:
        db.close()

    event = {
        "type": "payment.authorized",
        "order_id": order["order_id"],
        "user_id": order["user_id"]
    }
    ch.basic_publish(
        exchange="orders",
        routing_key="payment.authorized",
        body=json.dumps(event).encode("utf-8")
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def connect_rabbitmq():
    """Retry RabbitMQ connection until it's available."""
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq")
            )
            print("[*] Connected to RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("[!] RabbitMQ not ready, retrying in 5 seconds...")
            time.sleep(5)


def main():
    connection = connect_rabbitmq()
    channel = connection.channel()

    channel.exchange_declare(exchange="orders", exchange_type="topic")
    channel.queue_declare(queue="q.payment", durable=True)
    channel.queue_bind(exchange="orders", queue="q.payment", routing_key="order.created")

    channel.basic_consume(queue="q.payment", on_message_callback=callback)
    print("[*] Payment Service waiting for messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
