from .config import openai_api_key
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key=openai_api_key,
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=150
)
