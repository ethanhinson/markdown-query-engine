# Markdown Query Engine

Provides a sample LlamaIndex application that indexes markdown files and allows for semantic search queries. Simply provide a path to the markdown files you want to index.

## Prerequisites
- Python 3.10+
- Ollama
- Docker

## Setup

1. Copy the `.env.example` file to `.env` and supply the namespace and data file path. Optionally, you can set `OPENAI_API_KEY` if you want to use ChatGPT instead of local Ollama.
2. Run `pip install -r requirements.txt` to install the dependencies.

### Running

1. Run `docker compose up` to start the Redis and OpenSearch containers.
2. Run `python -m MarkdownQueryEngine.bin.index` to index the documents.
3. Run `python -m MarkdownQueryEngine.app.main` to start the FastAPI server.

### Querying

Send a POST request to `http://localhost:9898/query` with a JSON body containing the query string.

```
{
    "query": "Why did the chicken cross the road?"
}
```

## Architecture

                                 User Query
                                     ↓
                  "Summarize X, or give me details about Y."
                                     ↓
                            +------------------+
                            | RouterQueryEngine |
                            +------------------+
                                     ↓
                            +------------------+
                            |   LLM Selector   |
                            | (Decides Route)  |
                            +------------------+
                                     ↓
                        +--------------------------+
                        |                          |
                        ↓                          ↓
            +--------------------+      +--------------------+
            |   List Engine      |      |   Vector Engine   |
            | (Summary Store)    |      |  (Specific Info)  |
            +--------------------+      +--------------------+
            | "Summarize all    |      | "Find details     |
            |  documents..."    |      |  about X..."      |
            +--------------------+      +--------------------+
                        ↓                          ↓
                        +---------------------------+
                                     ↓
                              Final Response
