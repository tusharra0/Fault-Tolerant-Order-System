import pika, json

def publish_order(order: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    channel.exchange_declare(exchange="orders", exchange_type="topic")

    channel.basic_publish(
        exchange="orders",
        routing_key="order.created",
        body=json.dumps(order).encode("utf-8")
    )

    connection.close()
