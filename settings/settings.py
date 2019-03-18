from enum import Enum


class StorageOptions(Enum):
    local_db = "Each worker stores the content in the DB which lies on the same machine as the worker."
    central_db = "Every worker stores the content in the same, central database"
    local_files = "Each worker writes the content in its local file system"


STORAGE = StorageOptions.local_files

FETCH_EXTERNAL = False

DOWNLOADABLE_QUEUE_IP = "134.209.226.34"
OUTLINKS_QUEUE_IP = "134.209.226.34"
LOCAL_OUTLINKS_QUEUE_IP = "localhost"

DOWNLOADABLE_QUEUE = "download_test_211"
OUTLINKS_QUEUE = "outlinks_test_211"
LOCAL_OUTLINKS_QUEUE = 'outlinks_local_211'

USE_TOR = False

RMQ_USERNAME = "test"
RMQ_PASSWORD = "test"

OUTLINKS_CHUNK_SIZE = 20
LOCAL_CHUNK_SIZE = 20

LOCAL_STRATEGY = True

MAX_ACTIVE_WORKERS = 10
