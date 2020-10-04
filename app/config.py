import os

USER = os.environ.get("USER", "Katya")
PASSWORD = os.environ.get("PASSWORD", "12345678")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "sOmE_sEcUrE_pAsS")
RETRY_COUNT = os.environ.get("RETRY_COUNT", 5)
