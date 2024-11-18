import os
import dotenv
from llama_index.core.llms.function_calling import FunctionCallingLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

class AppConfig():

    def __init__(self):
        dotenv.load_dotenv()
        self._namespace = os.getenv("NAMESPACE")
        self._data_file_path = os.getenv("DATA_FILE_PATH")
        self._llm_model = os.getenv("LLM_MODEL")
        self._openai_api_key = os.getenv("OPENAI_API_KEY")
        self._redis_host = os.getenv("REDIS_HOST")
        self._redis_port = os.getenv("REDIS_PORT")
        self._opensearch_endpoint = os.getenv("OPENSEARCH_ENDPOINT")
        self._opensearch_index = os.getenv("OPENSEARCH_INDEX")
        self._vector_embedding_field = os.getenv("VECTOR_EMBEDDING_FIELD")
        self._vector_text_field = os.getenv("VECTOR_TEXT_FIELD")
        self._app_port = os.getenv("APP_PORT")

    @property
    def namespace(self):
        return self._namespace

    @property
    def data_file_path(self):
        return self._data_file_path

    @property
    def llm_model(self):
        return self._llm_model
    
    @property
    def openai_api_key(self):
        return self._openai_api_key
    
    @property
    def redis_host(self):
        return self._redis_host
    
    @property
    def redis_port(self):
        return self._redis_port
    
    @property
    def opensearch_endpoint(self):
        return self._opensearch_endpoint
    
    @property
    def opensearch_index(self):
        return self._opensearch_index
    
    @property
    def vector_embedding_field(self):
        return self._vector_embedding_field
    
    @property
    def vector_text_field(self):
        return self._vector_text_field
    
    @property
    def app_port(self):
        return int(self._app_port)

    def get_llm(self) -> FunctionCallingLLM:
        timeout = 360.0
        if not os.getenv("OPENAI_API_KEY"):
            return Ollama(model=self.llm_model, request_timeout=timeout)
        else:
            return OpenAI(model=self.llm_model, request_timeout=timeout)

    def get_embed_model(self) -> HuggingFaceEmbedding:
        # TODO: Load from env if needed
        return HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
