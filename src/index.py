from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.opensearch import (
    OpensearchVectorStore,
    OpensearchVectorClient,
)

def index(endpoint: str, idx: str, embedding_field: str, text_field: str) -> VectorStoreIndex:
    client = OpensearchVectorClient(endpoint, idx, 768, 
                                    embedding_field=embedding_field, 
                                    text_field=text_field)
    vector_store = OpensearchVectorStore(client)
    index = VectorStoreIndex.from_vector_store(vector_store)
    return index