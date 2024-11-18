from llama_index.core import SimpleDirectoryReader, SummaryIndex, VectorStoreIndex, SimpleKeywordTableIndex, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from src.storage import get_storage_context


def index_documents():
    documents = SimpleDirectoryReader(
        input_dir="nx/docs/shared/examples",
        recursive=True,
        required_exts=[".md", ".mdx"]
    ).load_data()

    nodes = SentenceSplitter().get_nodes_from_documents(documents)

    storage_context = get_storage_context("nx-docs")

    storage_context.docstore.add_documents(nodes)

    storage_context.persist(persist_dir="./storage")
