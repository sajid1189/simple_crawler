import pika
import sys
import os
import json

from settings import settings


sys.path.append(os.path.abspath('../'))


def publish_outlinks(outlinks):
    from settings import settings
    credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
    print("publishing {}".format(len(outlinks)))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP,
                                                                   credentials=credentials
                                                                   ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.OUTLINKS_QUEUE)

    channel.basic_publish(exchange="",
                          routing_key=settings.OUTLINKS_QUEUE,
                          body=json.dumps(list(outlinks)),
                          )

    connection.close()


def publish_outlinks_to_local_queue(outlinks):
    from settings import settings
    # credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
    print("publishing {}".format(len(outlinks)))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.LOCAL_PUBLISHER_QUEUE))
    channel = connection.channel()
    channel.queue_declare(queue=settings.LOCAL_PUBLISHER_QUEUE)

    channel.basic_publish(exchange="",
                          routing_key=settings.LOCAL_PUBLISHER_QUEUE,
                          body=json.dumps(list(outlinks)),
                          )

    connection.close()
