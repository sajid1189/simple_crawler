# import pika
# from settings import settings
# import os
# import json
# import sys
# import time
#
# sys.path.append(os.path.abspath('../'))
#
# from workers.worker import Worker
#
#
# if __name__ == '__main__':
#     seeds = []
#     with open('seeds.txt') as f:
#         for line in f:
#             if line.startswith('http'):
#                 seeds.append(line.rstrip())
#     if not seeds:
#         raise ValueError("Check the seeds.txt. The seeds are not in correct form or the file is empty")
#     credentials = pika.PlainCredentials(settings.RMQ_USERNAME, settings.RMQ_PASSWORD)
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.DOWNLOADABLE_QUEUE_IP,
#                                                                    credentials=credentials
#                                                                    ))
#     channel = connection.channel()
#     channel.queue_declare(queue=settings.DOWNLOADABLE_QUEUE)
#
#     channel.basic_publish(exchange="",
#                           routing_key=settings.DOWNLOADABLE_QUEUE,
#                           body=json.dumps(seeds),)
#     connection.close()
#     print("The following seeds have been published on the queue: {}".format(seeds))
#
#     worker_list = []
#     for url in seeds:
#         worker = Worker(url)
#         worker_list.append(worker)
#         worker.start()

    # while True:
    #     for worker in worker_list:
    #         if not worker.is_alive():
    #             print("a worker just died :(")
    #             worker_list.remove(worker)
    #     for i in range(settings.MAX_ACTIVE_WORKERS - len(worker_list)):
    #         worker = Worker()
    #         worker_list.append(worker)
    #         worker.start()
    #     time.sleep(10)
