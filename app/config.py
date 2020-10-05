# internal modules
import os


# set variables to
USER = os.environ.get("USER", "Katya")
PASSWORD = os.environ.get("PASSWORD", "12345678")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "sOmE_sEcUrE_pAsS")

# set variables for message queues

# how many times queue will try to send message
try:
    RETRY_COUNT = int(os.environ.get("RETRY_COUNT", 5))
except ValueError:
    RETRY_COUNT = 5

try:
    RETRY_INTERVAL = int(os.environ.get("RETRY_INTERVAL", 60))
except ValueError:
    RETRY_INTERVAL = 60

# how long messages will stay in memory
try:
    DELETE_FINISHED_TIMEOUT = int(os.environ.get("DELETE_FINISHED_TIMEOUT", 300))
except ValueError:
    DELETE_FINISHED_TIMEOUT = 300

try:
    DELETE_FAILED_TIMEOUT = int(os.environ.get("DELETE_FAILED_TIMEOUT", 300))
except ValueError:
    DELETE_FAILED_TIMEOUT = 300
