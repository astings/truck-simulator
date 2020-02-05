import pika
import json
import time
import sys
from etl_service.etl_sqlalchemy import truck_position_to_db

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

routing_key = 'journey.new'
channel.queue_declare(queue='exchange', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    content = json.loads(body)
    print(content)
    # content['iditinerary'] = int(content['iditinerary'])
    print(" [x] Received %r" % json.loads(body))
    template = '[WRITING] truck %i with driver ID %i currently at:\n  -%f\n   -%f\non itinerary %i'
    # print(template % (content['idtruck'],
    #                   content['iddriver'],
    #                   content['position'][0],
    #                   content['position'][1],
    #                   content['iditinerary']))

    truck_position_to_db(content)
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # time.sleep(1)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='exchange',
                      on_message_callback=callback
                      )

channel.start_consuming()
