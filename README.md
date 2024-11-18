# Markdown Query Engine

Provides a sample LlamaIndex application that indexes markdown files and allows for semantic search queries. Simply provide a path to the markdown files you want to index.

## Prerequisites
- Python 3.10+
- Ollama
- Docker

## Setup

1. Copy the `.env.example` file to `.env` and supply the namespace and data file path. Optionally, you can set `OPENAI_API_KEY` if you want to use ChatGPT instead of local Ollama.
2. Run `pip install -r requirements.txt` to install the dependencies.
