from enum import Enum


class STORAGE_OPTIONS(Enum):
    local_db = "Each worker stores the content in the DB which lies on the same machine as the worker."
    central_db = "Every worker stores the content in the same, central database"
    local_files = "Each worker writes the content in its local file system"


STORAGE = STORAGE_OPTIONS.local_files

FETCH_EXTERNAL = False

DOWNLOADABLE_QUEUE_IP = "139.59.13.201"
OUTLINKS_QUEUE_IP = "139.59.13.201"

DOWNLOADABLE_QUEUE = "download_test_1"
OUTLINKS_QUEUE = "outlinks_test_1"

USE_TOR = False
