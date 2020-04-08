import pika
import json
import time
import os
import sys
from datetime import datetime
from threading import Thread
from truck import Truck
from db_utilis.etl_sqlalchemy import driver_to_db, itinerary_to_db

class Publisher(Thread):

    def __init__(self, id_truck, id_driver, id_itinerary):
        Thread.__init__(self)
        self.id_truck = id_truck
        self.id_driver = id_driver
        new_driver = driver_to_db({'iddriver':id_driver})
        self.id_itinerary = id_itinerary
        self.truck = Truck(self.id_truck)
        self.connection = None
        self.departure, self.arrival = self.truck.drive()
        self.departure = [self.departure['lng'], self.departure['lat']]
        self.arrival = [self.arrival['lng'], self.arrival['lat']]
        new_itinerary = itinerary_to_db({'iditinerary':id_itinerary,
                         'mission':'Undefined',
                         'departure':self.departure,
                         'arrival':self.arrival})
        if new_driver == 0:
            print('Driver id #%i created' % (self.id_driver))
        elif new_driver == 1 :
            print('Driver id #%i already in DB' % (self.id_driver))
        if new_itinerary == 0:
            print('Itinerary id #%i created' % (self.id_itinerary))
        elif new_itinerary == 1 :
            print('Itinerary id #%i already in DB' % (self.id_itinerary))

    def emit_message(self, payload):
        amqp_url = os.environ['AMQP_URL']

        parameters = pika.URLParameters(amqp_url)
        self.connection = pika.BlockingConnection(parameters)
        channel = self.connection.channel()

        channel.queue_declare(queue='exchange', durable=True)
        channel.basic_publish(exchange='',
                              routing_key='exchange',
                              body=json.dumps(payload),
                              )
        print(" [x] Message publisher %r" % payload)
        self.connection.close()

    def run(self):
        journey_ended = False
        t = 0
        while not journey_ended:
            position = self.truck.get_position_at_time(t)
            status = self.truck.get_status_at_time(t)
            payload = {
                "iddriver": self.id_driver,
                "idtruck": self.id_truck,
                "status": status,
                "iditinerary": self.id_itinerary,
                "position": position,
                "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
                "departure": self.departure,
                "arrival": self.arrival,
                "mission": "Unregistred"
            }
            self.emit_message(payload)
            t += 1
            time.sleep(1)
