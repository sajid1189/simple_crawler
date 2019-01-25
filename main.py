import pika
from settings import settings
import os
import sys

sys.path.append(os.path.abspath('../'))

if __name__ == '__main__':
    seeds = []
    with open('seeds.txt') as f:
        for line in f:
            seeds.append(line)
    print(seeds)
    for seed in seeds:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP))
        channel = connection.channel()
        channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

        channel.basic_publish(exchange="",
                              routing_key=settings.DOWNLOADABLE_QUEUE,
                              body=seed,)
        connection.close()
