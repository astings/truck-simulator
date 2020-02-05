import pika
import json
import time
from truck import Truck
from datetime import datetime


def emit_message(payload):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost")
        )
    channel = connection.channel()

    channel.queue_declare(queue='exchange', durable=True)
    channel.basic_publish(exchange='',
                          routing_key='exchange',
                          body=json.dumps(payload),
                          )
    print(" [x] Message publisher %r" % payload)
    connection.close()


def emit_truck_info():
    id_truck = 1
    id_driver = 2
    id_itinerary = 2
    truck = Truck(id_truck)
    departure, arrival = truck.drive()
    journey_ended = False
    t = 0
    while not journey_ended:
        position = truck.get_position_at_time(t)
        payload = {
                   "iddriver": id_driver,
                    "idtruck": id_truck,
                    "status": 0,
                    "iditinerary": id_itinerary,
                    "position": position,
                    "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                  }
        journey_ended = position == arrival
        emit_message(payload)
        t += 1
        time.sleep(1)
