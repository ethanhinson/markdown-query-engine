from src.setup import setup
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.core import SimpleDirectoryReader, get_response_synthesizer
from llama_index.core import DocumentSummaryIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter

documents = SimpleDirectoryReader(
    input_dir="nx/docs/shared",
    recursive=True,
    required_exts=[".md", ".mdx"]
).load_data()

index = setup()

splitter = SentenceSplitter(chunk_size=1024)

for doc in documents:
    response_synthesizer = get_response_synthesizer(
        response_mode="tree_summarize", use_async=True
    )
    doc_summary_index = DocumentSummaryIndex.from_documents(
        [doc],
        transformations=[splitter],
        response_synthesizer=response_synthesizer,

    )
    doc_summary_index.insert(doc)
