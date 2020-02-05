import pika
import json
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

routing_key = 'journey.new'
channel.queue_declare(queue='exchange', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    content = json.loads(body)['position']
    print(" [x] Received %r" % json.loads(body))
    template = 'Truck %i with driver ID %i currently at:\n  -%f\n   -%f\non itinerary %i'
    print(template % (content['id_truck'],
                      content['id_driver'],
                      content['position'][0],
                      content['position'][1],
                      content['id_itinerary']))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # time.sleep(1)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='exchange',
                      on_message_callback=callback
                      )

channel.start_consuming()
