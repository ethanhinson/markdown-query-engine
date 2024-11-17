from os import getenv
from llama_index.core import VectorStoreIndex
from src.index import index
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

def get_llm():
    return Ollama(model="llama3", request_timeout=360.0)

def setup() -> VectorStoreIndex:
    Settings.llm = get_llm()
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    endpoint = getenv("OPENSEARCH_ENDPOINT", "http://localhost:9200")
    idx = getenv("OPENSEARCH_INDEX", "nx-docs")
    embedding_field = "embedding"
    text_field = "content"
    vectorStoreIndex = index(endpoint, idx, embedding_field, text_field)
    return vectorStoreIndex
