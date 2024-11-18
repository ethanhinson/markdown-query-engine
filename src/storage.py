import os
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
OPENSEARCH_ENDPOINT = os.getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")
OPENSEARCH_VECTOR_INDEX = os.getenv("OPENSEARCH_INDEX", "nx-docs")
VECTOR_EMBEDDING_FIELD = "embedding"
VECTOR_TEXT_FIELD = "content"

def vector_store() -> VectorStore:
    client = OpensearchVectorClient(OPENSEARCH_ENDPOINT, OPENSEARCH_VECTOR_INDEX, 768, 
                                    embedding_field=VECTOR_EMBEDDING_FIELD, 
                                    text_field=VECTOR_TEXT_FIELD)
    return OpensearchVectorStore(client)

def vector_index() -> VectorStoreIndex:
    return VectorStoreIndex.from_vector_store(vector_store())

def get_storage_context(namespace: str) -> StorageContext:
    storage_context = StorageContext.from_defaults(
        docstore=RedisDocumentStore.from_host_and_port(
        host=REDIS_HOST, port=REDIS_PORT, namespace=namespace
        ),
        index_store=RedisIndexStore.from_host_and_port(
            host=REDIS_HOST, port=REDIS_PORT, namespace=namespace
        ),
        vector_store=vector_store(),
    )

    return storage_context
