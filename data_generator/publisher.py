import pika
import json
import time
from truck import Truck
from random import randint


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
    id_truck = randint(0, 100)
    id_driver = randint(0, 100)
    id_itinerary = randint(0, 100)
    truck = Truck(id_truck)
    departure, arrival = truck.drive()
    journey_ended = False
    t = 0
    while not journey_ended:
        position = truck.get_position_at_time(t)
        payload = {"position":
                   {"id_driver": id_driver,
                        "id_truck": id_truck,
                        "status": 0,
                        "id_itinerary": id_itinerary,
                        "position": position
                   }
                  }
        journey_ended = position == arrival
        emit_message(payload)
        t += 1
        time.sleep(1)


while True:
    emit_truck_info()