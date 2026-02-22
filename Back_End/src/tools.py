# tools.py

from .config import *
from langchain.tools import tool
from pinecone import Pinecone
from groq import Groq  # your LLM client
import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")


# Initialize clients
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)
groq = Groq(api_key=groq_api_key)


@tool
def schema_retriever(user_query: str) -> str:
    """Retrieve relevant database schema information for the given user query."""

    query_embedding = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[user_query],
        parameters={"input_type": "passage"}
    ).data[0]["values"]

    results = index.query(
        vector=query_embedding,
        top_k=20,
        include_metadata=True
    )

    schema_context = ""
    for match in results.matches:
        table = match.metadata.get("table")
        columns = match.metadata.get("columns", [])
        schema_context += f"{table}({','.join(columns)})\n"

    return schema_context.strip()


import mysql.connector
from langchain.tools import tool

@tool
def sql_executor(sql_query: str) -> str:
    """Execute the given SQL query and return results as a string."""
    
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=host,      # your DB host
        user=user,           # your DB user
        password=password,   # your DB password
        database=database  # your DB name
    )
    
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        # Convert rows to string
        if not rows:
            return "No results found."
        else:
            return "\n".join([str(row) for row in rows])
    except Exception as e:
        return f"SQL execution error: {str(e)}"
    finally:
        cursor.close()
        conn.close()