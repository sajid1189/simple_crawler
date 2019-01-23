from settings import settings
import requests
import pika
from simple_parsers.parser import Soup
from publishers.outlink_publisher import publish_outlinks
from uuid import uuid4
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP))
channel = connection.channel()
channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

""" This is a simple worker. It listens to the DOWNLOADABLE_QUEUE, stores the content and pushes the out-links to the 
    OUTLINKS_QUEUE.
"""


def _write(response):
    if settings.STORAGE == settings.STORAGE_OPTIONS.local_files:
        print("writing {}".format(response))
        with open("{}.html".format(uuid4()), 'w+') as f:
            f.write(response.url)


def worker(ch, method, properties, body):
    """
    A callback function that is called when a message is received by the worker. It downloads the passed url,
    parses the content for the outgoing links (urls), stores the content
    :param ch: RabbitMQ channel
    :param method:
    :param properties:
    :param body: message body. Typically, it the url that the worker is going to download and process
    :return: None
    """
    try:
        print("received url {}".format(body))
        response = requests.get(body)
        soup = Soup(response)
        internal_outlinks = soup.get_absolute_internal_links()
        external_outlinks = set()
        if settings.FETCH_EXTERNAL:
            external_outlinks = soup.get_external_links()
        outlinks = internal_outlinks.union(external_outlinks)
        publish_outlinks(outlinks)
        try:
            _write(response)
        except Exception as e:
            print(e)
            print(" ------ Could not write {}".format(body))
    except Exception as e:
        print("erro {}".format(e))


channel.basic_consume(worker, queue=settings.DOWNLOADABLE_QUEUE)
channel.start_consuming()
