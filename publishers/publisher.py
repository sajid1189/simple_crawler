import pika
from settings import settings

from settings.shared import DOWNLOADED_LINKS

if __name__ == '__main__':
    pass
connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP))
channel = connection.channel()
channel.queue_declare(queue=settings.OUTLINKS_QUEUE)


def check_and_publish(ch, method, properties, body):
    """
    A callback function that is called when a message is received by the worker. It downloads the passed url,
    parses the content for the outgoing links (urls), stores the content
    :param ch: RabbitMQ channel
    :param method:
    :param properties:
    :param body: message body. Typically, it the url that the worker is going to download and process
    :return: None
    """

    # Check if the link is already downloaded i.e.,if it exists in the global set
    if body not in DOWNLOADED_LINKS:
        print("DOWNLOADED_LINKS len {} ".format(len(DOWNLOADED_LINKS)))
        con = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP))
        ch = con.channel()
        ch.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

        ch.basic_publish(exchange="", routing_key=settings.DOWNLOADABLE_QUEUE, body=body)
        con.close()
        DOWNLOADED_LINKS.add(body)
    else:
        print("not in set")
    print("publishing {}".format(body))


channel.basic_consume(check_and_publish, queue=settings.OUTLINKS_QUEUE)

channel.start_consuming()
