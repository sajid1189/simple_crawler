from enum import Enum


class STORAGE_OPTIONS(Enum):
    local_db = "Each worker stores the content in the DB which lies on the same machine as the worker."
    central_db = "Every worker stores the content in the same, central database"
    local_files = "Each worker writes the content in its local file system"


STORAGE = STORAGE_OPTIONS.local_files

FETCH_EXTERNAL = False

DOWNLOADABLE_QUEUE_IP = "157.230.237.143"
OUTLINKS_QUEUE_IP = "157.230.237.143"
LOCAL_OUTLINKS_QUEUE_IP = "localhost"

DOWNLOADABLE_QUEUE = "download_test_x"
OUTLINKS_QUEUE = "outlinks_test_x"
LOCAL_OUTLINKS_QUEUE = 'outlinks_local_x'

USE_TOR = False

RMQ_USERNAME = "test"
RMQ_PASSWORD = "test"

OUTLINKS_CHUNK_SIZE = 20
LOCAL_CHUNK_SIZE = 100

LOCAL_STRATEGY = True
