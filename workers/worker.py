import settings
import requests

from simple_parsers.parser import Soup


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

    print("received url {}".format(body))
    response = requests.get(body)
    soup = Soup(response)
    outlinks = soup.get_absolute_internal_links()