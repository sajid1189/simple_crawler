import pika
import os
import sys
import redis
import hashlib
import base64
import json

from redis_namespace import StrictRedis


sys.path.append(os.path.abspath('../'))

from settings import settings


def check_and_publish(ch, method, properties, url_chunk):
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
    global namespaced_redis
    # Check if the link is already downloaded i.e.,if it exists in the global set
    outlinks = json.loads(url_chunk)
    outlinks_to_be_downloaded = []
    print("checking and publishing", len(outlinks))
    for url in outlinks:
        url_hash = _get_alphanumeric_hash(url)
        if url_hash not in namespaced_redis:
            outlinks_to_be_downloaded.append(url)
            namespaced_redis.set(url_hash, 1)

    chunks_count = len(outlinks_to_be_downloaded) // settings.OUTLINKS_CHUNK_SIZE
    first_index = 0
    last_index = settings.OUTLINKS_CHUNK_SIZE
    for i in range(chunks_count+1):
        outlinks_bag = outlinks_to_be_downloaded[first_index: last_index]
        first_index = last_index
        last_index = last_index + settings.OUTLINKS_CHUNK_SIZE
        print("index {}, bag size {}".format(i, len(outlinks_bag)))
        if len(outlinks_bag):
            con = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP,
                                                                    ))
            ch = con.channel()
            ch.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)

            channel.basic_publish(exchange="",
                                  routing_key=settings.DOWNLOADABLE_QUEUE,
                                  body=json.dumps(outlinks_bag),
                                  )
            con.close()


def _get_alphanumeric_hash(url):
    hs = hashlib.md5(url.encode()).digest()
    return base64.b64encode(hs)


if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP,
                                                                   ))
    channel = connection.channel()
    channel.queue_declare(queue=settings.OUTLINKS_QUEUE)
    redis_connection = redis.StrictRedis()
    namespaced_redis = StrictRedis(namespace='global:', host='localhost', port=6379, db=0)
    channel.basic_consume(settings.OUTLINKS_QUEUE, check_and_publish)
    channel.start_consuming()



