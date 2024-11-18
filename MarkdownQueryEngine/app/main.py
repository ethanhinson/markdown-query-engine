import logging
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from llama_index.core import Settings
from MarkdownQueryEngine.app.config import AppConfig

config = AppConfig()

Settings.llm = config.get_llm()
Settings.embed_model = config.get_embed_model()

app = FastAPI()

class QueryRequest(BaseModel):
    query: str


from MarkdownQueryEngine.app.query import query

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    return query(request.query)

# Keep this for local testing if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.app_port)
