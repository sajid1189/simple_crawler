from enum import Enum


class StorageOptions(Enum):
    local_db = "Each worker stores the content in the DB which lies on the same machine as the worker."
    central_db = "Every worker stores the content in the same, central database"
    local_files = "Each worker writes the content in its local file system"


STORAGE = StorageOptions.local_files

FETCH_EXTERNAL = False

DOWNLOADABLE_QUEUE_IP = "178.62.254.140"
OUTLINKS_QUEUE_IP = "178.62.254.140"
LOCAL_OUTLINKS_QUEUE_IP = "localhost"

DOWNLOADABLE_QUEUE = "downloadable"
OUTLINKS_QUEUE = "outlinks"
LOCAL_OUTLINKS_QUEUE = 'local_outlinks'

USE_TOR = False

RMQ_USERNAME = "test"
RMQ_PASSWORD = "test"

OUTLINKS_CHUNK_SIZE = 20
LOCAL_CHUNK_SIZE = 1

LOCAL_STRATEGY = True

MAX_ACTIVE_WORKERS = 10
