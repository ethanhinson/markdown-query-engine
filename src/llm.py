from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

def get_llm():
    # TODO: Load from env
    return Ollama(model="llama3", request_timeout=360.0)

def get_embed_model():
    # TODO: Load from env
    return HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
