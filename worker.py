""" Executable module of message_sender worker listening queues """

# internal modules
import os

# external modules
import redis
from rq import Worker, Queue, Connection


conn = redis.Redis(host="redis", port="6379", password=os.environ.get("REDIS_PASSWORD", "sOmE_sEcUrE_pAsS"))
listen = ['medium', "check", "scheduled"]


if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work(with_scheduler=True)
