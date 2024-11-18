from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector
from llama_index.core.tools import QueryEngineTool
from llama_index.core import load_index_from_storage
from src.storage import get_storage_context
from src.llm import get_llm
from src.redis import get_redis_client
import json

redis_client = get_redis_client()

index_types = redis_client.hgetall("nx-docs/index")

for index_id, index_type in index_types.items():
    unpacked_type = json.loads(index_type.decode('utf-8'))
    if unpacked_type['__type__'] == 'list':
        list_query_engine_id = index_id
    if unpacked_type['__type__'] == 'vector_store':
        vector_query_engine_id = index_id


if not list_query_engine_id or not vector_query_engine_id:
    raise Exception("No query engines found")

storage_context = get_storage_context("nx-docs")

list_query_engine = load_index_from_storage(
    storage_context=storage_context, index_id=list_query_engine_id
).as_query_engine(llm=get_llm())

vector_query_engine = load_index_from_storage(
    storage_context=storage_context, index_id=vector_query_engine_id
).as_query_engine(llm=get_llm())

list_tool = QueryEngineTool.from_defaults(
    query_engine=list_query_engine,
    description="Useful for summarization questions related to the data source",
)
vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description="Useful for retrieving specific context related to the data source",
)

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(llm=get_llm()),
    query_engine_tools=[
        list_tool,
        vector_tool,
    ],
    llm=get_llm(),
)

def query(query: str):
    return query_engine.query(query)
