import multiprocessing
import random
import requests
import pika
import json
import sys
import os

sys.path.append(os.path.abspath('../'))

from simple_parsers.parser import Soup
from publishers.outlink_publisher import publish_outlinks, publish_outlinks_to_local_queue
from uuid import uuid4
from settings.user_agents import USER_AGENTS
from settings import settings


class Worker():

    def run(self):
        """
        It is a consumer that consumes the DOWNLOADABLE_QUEUE and upon receiving a message delegates the work to the
        `task`. `task` downloads the pages, extracts links and publishes them with the help of `publish_outlinks`
        or `publish_outlinks_to_local_queue` based on the strategy.

        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP,
                                                                       ))
        channel = connection.channel()
        channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

        channel.basic_consume(settings.DOWNLOADABLE_QUEUE, self.task)
        channel.start_consuming()

    def task(self, ch, method, properties, body):
        """
            A callback function that is called when a message is received by the worker. It downloads the passed url,
            parses the content for the outgoing links (urls) and stores the content in file or DB based on the storage settings
            :param ch: RabbitMQ channel
            :param method:
            :param properties:
            :param body: message body. Typically, it the url that the worker is going to download and process
            :return: None
            """
        urls = json.loads(body)
        urls = list(filter(lambda x: x.startswith('http'), urls))
        print("received {} urls by worker".format(len(urls)))

        for url in urls:
            response = self._request(url)
            print("request ends")
            soup = Soup(response)
            internal_outlinks = soup.get_absolute_internal_links()
            external_outlinks = set()
            if settings.FETCH_EXTERNAL:
                external_outlinks = soup.get_external_links()
            outlinks = list(internal_outlinks.union(external_outlinks))
            self._write(response)
            if not settings.LOCAL_STRATEGY:
                publish_outlinks(outlinks)
            else:
                print("publishing to local")
                publish_outlinks_to_local_queue(outlinks)

    def _request(self, url):

        if settings.USE_TOR:

            session = requests.session()
            session.headers = {'User-Agent': USER_AGENTS[random.randint(0, len(USER_AGENTS) - 1)]}
            session.proxies = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }
            response = session.get(url)

        else:
            print("in request {}".format(url))
            response = requests.get(url)
            print('response ', response)
        return response

    def _write(self, response):
        if settings.STORAGE == settings.StorageOptions.local_files:
            this_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            with open(os.path.join(this_dir, "workers", "content", "{}.html".format(uuid4())), 'w+') as f:
                try:
                    content = "{}\n\n {}".format(response.url, response.content)
                    f.write(content)
                except Exception as e:
                    print("Exception at _write: {}".format(e))


if __name__ == '__main__':
    worker = Worker()
    worker.run()
