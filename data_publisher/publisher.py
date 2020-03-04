import pika
import json
import time
from truck import Truck
from datetime import datetime
from threading import Thread


class Publisher(Thread):

    def __init__(self, id_truck, id_driver, id_itinerary):
        Thread.__init__(self)
        self.id_truck = id_truck
        self.id_driver = id_driver
        self.id_itinerary = id_itinerary
        self.truck = Truck(self.id_truck)

    @staticmethod
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

    def run(self):
        self.truck.drive()
        t = datetime.now()
        while self.truck.status != "arrived":
            position = self.truck.get_position_at_time(t)
            payload = {
                "iddriver": self.id_driver,
                "idtruck": self.id_truck,
                "status": self.truck.status,
                "iditinerary": self.id_itinerary,
                "position": position,
                "timestamp": datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            }
            self.emit_message(payload)
            time.sleep(1)
            t = datetime.now()

        self.run()

