import random
import requests
import pika
import time
import sys
import os

sys.path.append(os.path.abspath('../'))


from simple_parsers.parser import Soup
from publishers.outlink_publisher import publish_outlinks
from uuid import uuid4
from settings.user_agents import USER_AGENTS
from settings import settings


""" This is a simple worker. It listens to the DOWNLOADABLE_QUEUE, stores the content and pushes the out-links to the 
    OUTLINKS_QUEUE.
"""


def _write(response):
    if settings.STORAGE == settings.STORAGE_OPTIONS.local_files:
        with open(os.path.join("content", "{}.html".format(uuid4())), 'w+') as f:
            try:
                content = "{}\n\n {}".format(response.url, response.content)
                f.write(content)
            except Exception as e:
                print("Exception at _write: {}".format(e))


def _request(url):

    if settings.USE_TOR:

        session = requests.session()
        session.headers = {'User-Agent': USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]}
        session.proxies = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
        response = session.get(url)

    else:
        response = requests.get(url)
    return response


def worker(ch, method, properties, body):
    """
    A callback function that is called when a message is received by the worker. It downloads the passed url,
    parses the content for the outgoing links (urls) and stores the content in file or DB based on the storage settings
    :param ch: RabbitMQ channel
    :param method:
    :param properties:
    :param body: message body. Typically, it the url that the worker is going to download and process
    :return: None
    """

    print("received url {} by worker".format(body))
    response = _request(body)
    soup = Soup(response)
    internal_outlinks = soup.get_absolute_internal_links()
    external_outlinks = set()
    if settings.FETCH_EXTERNAL:
        external_outlinks = soup.get_external_links()
    outlinks = internal_outlinks.union(external_outlinks)
    publish_outlinks(outlinks)
    _write(response)


if __name__ == "__main__":
    credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP,
                                                                   credentials=credentials
                                                                   ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

    channel.basic_consume(worker, queue=settings.DOWNLOADABLE_QUEUE)
    channel.start_consuming()
