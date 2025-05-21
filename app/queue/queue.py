from redis import Redis
from rq import Queue

# connecting to docker image(valkey)
redis_connection = Redis(host="valkey", port=6379)

# creating a queue - internally uses redis
q = Queue(connection=redis_connection)