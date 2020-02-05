import pika
import json
import time
from truck import Truck
from random import randint
from datetime import datetime

def stringify_position(position):
    template = 'POINT(%f %f)'
    return template % (position[0], position[1])

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
    print('trying close')
    connection.close()
    print('closed')


def emit_truck_info():
    print('new emit')
    id_truck = randint(0, 100)
    id_driver = randint(0, 100)
    id_itinerary = randint(0, 100)
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
                    "position": stringify_position(position),
                    "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                  }
        journey_ended = position == arrival
        emit_message(payload)
        print('emited')
        t += 1
        time.sleep(1)


while True:
    emit_truck_info()