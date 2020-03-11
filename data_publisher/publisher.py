import pika
import json
import time
from truck import Truck
from datetime import datetime
from threading import Thread
import os

amqp_url = 'amqp://rabbitmq'


class Publisher(Thread):

    def __init__(self, id_truck, id_driver, id_itinerary):
        Thread.__init__(self)
        self.id_truck = id_truck
        self.id_driver = id_driver
        self.id_itinerary = id_itinerary
        self.truck = Truck(self.id_truck)
        self.connection = None

    def emit_message(self, payload):
        #amqp_url = os.environ['AMQP_URL']
        print('URL: %s' % (amqp_url,))

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
        self.truck.drive()
        journey_ended = False
        t = 0
        while not journey_ended:
            position = self.truck.get_position_at_time(t)
            payload = {
                "iddriver": self.id_driver,
                "idtruck": self.id_truck,
                "status": 0,
                "iditinerary": self.id_itinerary,
                "position": position,
                "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            }
            self.emit_message(payload)
            t += 1
            time.sleep(1)
