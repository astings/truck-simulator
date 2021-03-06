"""Consumer script awaiting for db write orders"""

import pika
import json
from db_utilis.etl_sqlalchemy import truck_position_to_db, truck_position_to_db_missing_foreign
import os
from sqlalchemy import exc


amqp_url = os.environ['AMQP_URL']
print('URL: %s' % (amqp_url,))

# Actually connect
parameters = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

routing_key = 'journey.new'
channel.queue_declare(queue='exchange', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    content = json.loads(body)
    print(" [x] Received %r" % json.loads(body))
    try:
        truck_position_to_db(content)
    except:
        print('Trying to add missing foreign keys')
        truck_position_to_db_missing_foreign(content)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='exchange',
                      on_message_callback=callback
                      )

channel.start_consuming()
