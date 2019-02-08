import pika
import os
import sys
import redis
import hashlib
import base64

sys.path.append(os.path.abspath('../'))

from settings import settings


def check_and_publish(ch, method, properties, url):
    """
    A callback function that is called when a message is received by the worker. It downloads the passed url,
    parses the content for the outgoing links (urls), stores the content
    :param ch: RabbitMQ channel
    :param method:
    :param properties:
    :param url: The message body of RabbitMQ message. Typically, it is
     the url that the worker is going to download and process
    :return: None
    """

    # Check if the link is already downloaded i.e.,if it exists in the global set
    url_hash = _get_alphanumeric_hash(url)
    if url_hash not in rds:
        con = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP))
        ch = con.channel()
        ch.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

        ch.basic_publish(exchange="", routing_key=settings.DOWNLOADABLE_QUEUE, body=url)
        con.close()
        rds.set(url_hash, 1)


def _get_alphanumeric_hash(url):
    hs = hashlib.md5(url.encode()).digest()
    return base64.b64encode(hs)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP))
    channel = connection.channel()
    channel.queue_declare(queue=settings.OUTLINKS_QUEUE)
    rds = redis.Redis(host='localhost', port=6379, db=0)
    channel.basic_consume(check_and_publish, queue=settings.OUTLINKS_QUEUE)
    channel.start_consuming()
