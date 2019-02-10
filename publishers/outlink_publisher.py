import pika
import sys
import os


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

    for link in outlinks:
        channel.basic_publish(exchange="",
                              routing_key=settings.OUTLINKS_QUEUE,
                              body=link,
                              )
    connection.close()
