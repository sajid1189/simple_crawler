import pika
import os
import sys
import redis
import hashlib
import base64
import json

sys.path.append(os.path.abspath('../'))

from settings import settings


def publish_to_global_form_local(ch, method, properties, url_chunk):
    """
    A callback function that is called when a message is received by the worker. It downloads the passed url,
    parses the content for the outgoing links (urls), stores the content
    :param ch: RabbitMQ channel
    :param method:
    :param properties:
    :param url_chunk: The message body of RabbitMQ message. It is
     a list of urls in json format
    :return: None
    """
    global rds, link_bucket
    # Check if the link is already downloaded i.e.,if it exists in the global set
    urls = json.loads(url_chunk)

    refined_links = []
    for url in urls:
        url_hash = _get_alphanumeric_hash(url)
        if url_hash not in rds:
            refined_links.append(url)
            rds.set(url_hash, 1)
    print('refined links', refined_links)
    print('-------------')
    print(link_bucket)
    link_bucket += refined_links
    if len(link_bucket) > settings.LOCAL_CHUNK_SIZE:

        print("local publisher is publishing", len(link_bucket))

        creds = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
        con = pika.BlockingConnection(pika.ConnectionParameters(host=settings.OUTLINKS_QUEUE_IP,
                                                                credentials=creds))
        ch = con.channel()
        ch.queue_declare(queue=settings.OUTLINKS_QUEUE)

        ch.basic_publish(exchange="",
                         routing_key=settings.OUTLINKS_QUEUE,
                         body=json.dumps(link_bucket),
                        )
        con.close()
        link_bucket = []
    else:
        print("link bucket is not big enough", len(link_bucket))


def _get_alphanumeric_hash(url):
    hs = hashlib.md5(url.encode()).digest()
    return base64.b64encode(hs)


if __name__ == '__main__':
    credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.LOCAL_OUTLINKS_QUEUE_IP))
    channel = connection.channel()
    channel.queue_declare(queue=settings.LOCAL_OUTLINKS_QUEUE)
    rds = redis.Redis(host='localhost', port=6379, db=0)
    link_bucket = []
    channel.basic_consume(publish_to_global_form_local, queue=settings.LOCAL_OUTLINKS_QUEUE)
    channel.start_consuming()
