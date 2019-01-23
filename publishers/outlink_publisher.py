import pika
from settings import settings


def publish_outlinks(outlinks):
    print("publishing {}".format(len(outlinks)))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP))
    channel = connection.channel()
    channel.queue_declare(queue=settings.OUTLINKS_QUEUE)

    for link in outlinks:
        channel.basic_publish(exchange="",
                              routing_key=settings.OUTLINKS_QUEUE,
                              body=link,
                              )
    connection.close()
