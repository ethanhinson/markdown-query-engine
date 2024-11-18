import logging
import sys
from llama_index.core import Settings
from src.llm import get_llm, get_embed_model

# Configure settings first
Settings.llm = get_llm()
Settings.embed_model = get_embed_model()

# Then import query module
from src.query import query

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

if __name__ == "__main__":
    print(query("Summarize how to use nx?"))
