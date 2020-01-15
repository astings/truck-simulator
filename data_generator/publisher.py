import pika
import json

def emit_journey_info(truck):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq-server")
        )
    channel = connection.channel()

    exchange_name = 'journey'
    routing_key = 'journey.new'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type="topic",
        durable=True
    )
