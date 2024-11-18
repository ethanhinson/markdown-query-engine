import os
from redis import Redis
from MarkdownQueryEngine.app.config import AppConfig

def get_redis_client(config: AppConfig):
    r = Redis(host=config.redis_host, port=config.redis_port, db=0)
    return r
