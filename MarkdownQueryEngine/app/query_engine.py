from MarkdownQueryEngine.app.config import AppConfig
from MarkdownQueryEngine.app.storage import get_storage_context
from llama_index.core import load_index_from_storage
from redis import Redis
import json

class QueryEngine:
    def __init__(self, type: str, config: AppConfig, redis_client: Redis):
        self.type = type
        self.config = config
        self.redis_client = redis_client
        self.storage_context = get_storage_context(config)

    def get_index_types(self):
        return self.redis_client.hgetall(f"{self.config.namespace}/index")

    def get_index_id(self):
        for index_id, index_type in self.get_index_types().items():
            unpacked_type = json.loads(index_type.decode('utf-8'))
            if unpacked_type['__type__'] == self.type:
                return index_id

        raise Exception("Invalid index type")


    def as_query_engine(self):
        return load_index_from_storage(
            storage_context=self.storage_context, index_id=self.get_index_id()
        ).as_query_engine(llm=self.config.get_llm())
