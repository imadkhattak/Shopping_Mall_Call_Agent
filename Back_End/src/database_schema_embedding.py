from google import genai
from .config import pinecone_api_key
from .config import gemini_embedding_key
from .fetching_schema import fetching_schema
from langchain_text_splitters import RecursiveCharacterTextSplitter


api_key = gemini_embedding_key

client = genai.Client(api_key=api_key)

result = client.models.embed_content(
        model="gemini-embedding-001",
        contents="What is the meaning of life?"
)

print(result.embeddings)