from redis import Redis
from rq import Worker, Queue

from tasks import process_image

redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)

worker = Worker(queues=[queue], connection=redis_conn)
worker.work()