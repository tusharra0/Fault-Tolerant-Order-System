import pika
import json
import time
import uuid
from datetime import datetime, timedelta
from db import SessionLocal
from models import Shipment


def callback(ch, method, properties, body):
    inventory_event = json.loads(body.decode("utf-8"))
    print(f"[x] Shipping Service received: {inventory_event}")

    db = SessionLocal()
    try:
        if inventory_event.get("force_fail"):
            raise Exception("Simulated shipping failure")

        tracking_number = f"SHIP-{uuid.uuid4().hex[:8].upper()}"
        estimated_delivery = datetime.utcnow() + timedelta(days=3)

        shipment = Shipment(
            order_id=inventory_event["order_id"],
            user_id=inventory_event["user_id"],
            tracking_number=tracking_number,
            status="READY",
            estimated_delivery=estimated_delivery
        )
        db.add(shipment)
        db.commit()
        print(f"[✓] Shipment created for order: {inventory_event['order_id']} | Tracking: {tracking_number}")

        event = {
            "type": "shipping.ready",
            "order_id": inventory_event["order_id"],
            "user_id": inventory_event["user_id"],
            "tracking_number": tracking_number,
            "estimated_delivery": estimated_delivery.isoformat()
        }
        ch.basic_publish(
            exchange="orders",
            routing_key="shipping.ready",
            body=json.dumps(event).encode("utf-8")
        )
        print(f"[→] Published shipping.ready for order: {inventory_event['order_id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[!] Error in Shipping Service: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()


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
    channel.exchange_declare(exchange="orders.dlx", exchange_type="topic")  # Dead Letter Exchange

    channel.queue_declare(
        queue="q.shipping",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "orders.dlx",
            "x-dead-letter-routing-key": "shipping.dead"
        }
    )
    channel.queue_bind(exchange="orders", queue="q.shipping", routing_key="inventory.reserved")

    # Dead Letter Queue
    channel.queue_declare(queue="q.shipping.dlq", durable=True)
    channel.queue_bind(exchange="orders.dlx", queue="q.shipping.dlq", routing_key="shipping.dead")

    channel.basic_consume(queue="q.shipping", on_message_callback=callback)
    print("[*] Shipping Service waiting for inventory.reserved messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
