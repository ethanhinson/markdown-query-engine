from src.setup import setup

index = setup()
query_engine = index.as_query_engine()
response = query_engine.query("Write a script to setup powerpack-gcs-cache")
print(response)
