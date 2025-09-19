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
        if order.get("force_fail"):
            raise Exception("Simulated payment processing failure")

        payment = Payment(order_id=order["order_id"], authorized=True)
        db.add(payment)
        db.commit()
        print(f"[✓] Payment authorized for order {order['order_id']}")

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
        print(f"[→] Published payment.authorized for order: {order['order_id']}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"[!] Error in Payment Service: {e}")
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
        queue="q.payment",
        durable=True,
        arguments={
            "x-dead-letter-exchange": "orders.dlx",
            "x-dead-letter-routing-key": "payment.dead"
        }
    )
    channel.queue_bind(exchange="orders", queue="q.payment", routing_key="order.created")

    # Dead Letter Queue
    channel.queue_declare(queue="q.payment.dlq", durable=True)
    channel.queue_bind(exchange="orders.dlx", queue="q.payment.dlq", routing_key="payment.dead")

    channel.basic_consume(queue="q.payment", on_message_callback=callback)
    print("[*] Payment Service waiting for order.created messages...")
    channel.start_consuming()


if __name__ == "__main__":
    main()
