import pika
from settings import settings
import os
import json
import sys

sys.path.append(os.path.abspath('../'))

if __name__ == '__main__':
    seeds = []
    with open('seeds.txt') as f:
        for line in f:
            if line.startswith('http'):
                seeds.append(line.rstrip())
    print(seeds)
    if not seeds:
        raise ValueError("Check the seeds.txt. The seeds are not in correct form or the file is empty")
    credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP,
                                                                   credentials=credentials
                                                                   ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

    channel.basic_publish(exchange="",
                          routing_key=settings.DOWNLOADABLE_QUEUE,
                          body=json.dumps(seeds),)
    connection.close()
    print("The following seeds have been published on the queue: {}".format(seeds))
