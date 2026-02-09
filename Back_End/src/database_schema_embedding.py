import re
from pinecone import Pinecone, ServerlessSpec
from .fetching_schema import fetching_schema
from google import genai
from .config import (
    pinecone_api_key,
    pinecone_index_name
)



pc = Pinecone(api_key=pinecone_api_key)


if pinecone_index_name not in [i['name'] for i in pc.list_indexes()]:
    pc.create_index(
        name=pinecone_index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

index = pc.Index(pinecone_index_name)

def embed_and_store_schema():
    schema = fetching_schema()
    vectors = []

    for table, columns in schema.items():
        text = f"Table {table} has columns: " + ", ".join(columns)

        embedding_response = pc.inference.embed(
                model="llama-text-embed-v2",
                inputs=[text],
                parameters={"input_type": 'passage'}
            )

        print("Embedding response:", embedding_response)
        embedding = embedding_response.data[0]['values']

        vectors.append({
            "id": table,
            "values": embedding,
            "metadata": {
                "table": table,
                "columns": columns
            }
        })

    index.upsert(vectors=vectors)
    print("✅ Database schema embedded and stored in Pinecone")

