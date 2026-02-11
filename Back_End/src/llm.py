from .config import api_key
from langchain_groq import ChatGroq

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)