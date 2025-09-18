import pika
import json
import time
from db import SessionLocal
from models import InventoryReservation


def callback(ch, method, properties, body):
    payment_event = json.loads(body.decode("utf-8"))
    print(f"[x] Inventory Service received: {payment_event}")

    db = SessionLocal()
    try:
        # Simulate stock reservation (always successful in this implementation)
        reservation = InventoryReservation(
            order_id=payment_event["order_id"],
            user_id=payment_event["user_id"],
            reserved=True,
            stock_available=95  # Simulated stock reduction
        )
        db.add(reservation)
        db.commit()
        print(f"[✓] Stock reserved for order: {payment_event['order_id']}")
    finally:
        db.close()

    # Publish inventory.reserved event
    event = {
        "type": "inventory.reserved",
        "order_id": payment_event["order_id"],
        "user_id": payment_event["user_id"],
        "stock_reserved": True
    }
    ch.basic_publish(
        exchange="orders",
        routing_key="inventory.reserved",
        body=json.dumps(event).encode("utf-8")
    )
    print(f"[→] Published inventory.reserved for order: {payment_event['order_id']}")
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
    channel.queue_declare(queue="q.inventory", durable=True)
    channel.queue_bind(exchange="orders", queue="q.inventory", routing_key="payment.authorized")

    channel.basic_consume(queue="q.inventory", on_message_callback=callback)
    print("[*] Inventory Service waiting for payment.authorized messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()