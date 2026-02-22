import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
pinecone_api_key = os.getenv("PINE_CONE_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
pinecone_index_name = os.getenv("PINE_CONE_INDEX_NAME")
openai_api_key = os.getenv("OPENAI_API_KEY")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT") 
password = os.getenv("DB_PASSWORD")
user = os.getenv("DB_USER")
database = os.getenv("DB_NAME")
