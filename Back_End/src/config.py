import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
gemini_embedding_key = os.getenv("GEMINI_EMBEDDING_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")