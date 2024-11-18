from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from MarkdownQueryEngine.app.query_engine import QueryEngine
from MarkdownQueryEngine.app.redis import get_redis_client
from MarkdownQueryEngine.app.config import AppConfig

config = AppConfig()
redis_client = get_redis_client(config)

list_query_engine = QueryEngine(type="list", config=config, redis_client=redis_client).as_query_engine()
vector_query_engine = QueryEngine(type="vector_store", config=config, redis_client=redis_client).as_query_engine()

list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Useful for summarization questions related to the data source",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context related to the data source",
)

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(llm=config.get_llm()),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
    llm=config.get_llm(),
)

def query(query: str):
    return query_engine.query(query)
