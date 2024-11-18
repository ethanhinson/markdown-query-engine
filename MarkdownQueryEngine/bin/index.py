#! /usr/bin/env python
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from MarkdownQueryEngine.app.storage import get_storage_context
from MarkdownQueryEngine.app.config import AppConfig

def index_documents(config: AppConfig):
    documents = SimpleDirectoryReader(
        input_dir=config.data_file_path,
        recursive=True,
        required_exts=[".md", ".mdx"]
    ).load_data()
    print(f"Indexing {len(documents)} documents from {config.data_file_path}")
    nodes = SentenceSplitter().get_nodes_from_documents(documents)
    storage_context = get_storage_context(config)
    storage_context.docstore.add_documents(nodes)
    storage_context.persist(persist_dir="./storage")

if __name__ == "__main__":
    config = AppConfig()
    index_documents(config)
