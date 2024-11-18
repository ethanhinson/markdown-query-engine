import os
from redis import Redis

def get_redis_host():
    return os.getenv("REDIS_HOST", "127.0.0.1")

def get_redis_port():
    return os.getenv("REDIS_PORT", 6379)

def get_redis_namespace():
    return os.getenv("REDIS_NAMESPACE", "nx-docs")

def get_redis_client():
    r = Redis(host=get_redis_host(), port=get_redis_port(), db=0)
    return r
