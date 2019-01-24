import pika
from settings import settings
import os
import sys

sys.path.append(os.path.abspath('../'))

seeds = ["https://www.webscraper.io/test-sites"]

if __name__ == '__main__':
    for seed in seeds:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP))
        channel = connection.channel()
        channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

        channel.basic_publish(exchange="",
                              routing_key=settings.DOWNLOADABLE_QUEUE,
                              body=seed,
                             )
        connection.close()
