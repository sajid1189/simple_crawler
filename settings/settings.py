from enum import Enum
import os


class StorageOptions(Enum):
    local_db = "Each worker stores the content in the DB which lies on the same machine as the worker."
    central_db = "Every worker stores the content in the same, central database"
    local_files = "Each worker writes the content in its local file system"


STORAGE = StorageOptions.local_files

FETCH_EXTERNAL = False

DOWNLOADABLE_QUEUE_IP = os.getenv("DOWNLOADABLE_QUEUE_IP", "localhost")
OUTLINKS_QUEUE_IP = os.getenv("OUTLINKS_QUEUE_IP", "localhost")
LOCAL_OUTLINKS_QUEUE_IP = "localhost"

DOWNLOADABLE_QUEUE = "downloadable"
OUTLINKS_QUEUE = "outlinks"
LOCAL_OUTLINKS_QUEUE = 'local_outlinks'

USE_TOR = False

RMQ_USERNAME = "test"
RMQ_PASSWORD = "test"

OUTLINKS_CHUNK_SIZE = 5
LOCAL_CHUNK_SIZE = 2

LOCAL_STRATEGY = True

MAX_ACTIVE_WORKERS = 5
