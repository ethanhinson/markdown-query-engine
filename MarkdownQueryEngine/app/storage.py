import os
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.vector_stores.types import VectorStore
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.storage.index_store.redis import RedisIndexStore
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)
from MarkdownQueryEngine.app.config import AppConfig


def vector_store(config: AppConfig) -> VectorStore:
    client = OpensearchVectorClient(config.opensearch_endpoint, config.opensearch_index, 768, 
                                    embedding_field=config.vector_embedding_field, 
                                    text_field=config.vector_text_field)
    return OpensearchVectorStore(client)

def vector_index(config: AppConfig) -> VectorStoreIndex:
    return VectorStoreIndex.from_vector_store(vector_store(config))

def get_storage_context(config: AppConfig) -> StorageContext:
    storage_context = StorageContext.from_defaults(
        docstore=RedisDocumentStore.from_host_and_port(
            host=config.redis_host, port=config.redis_port, namespace=config.namespace
        ),
        index_store=RedisIndexStore.from_host_and_port(
            host=config.redis_host, port=config.redis_port, namespace=config.namespace
        ),
        vector_store=vector_store(config),
    )

    return storage_context
