from groq import Groq
from .config import api_key
from langchain.tools import tool
from agent import SQL_Query_Generator


api_key = api_key

store_tool = Tool(
    name="SQL_Query_Generator",
    func=SQL_Query_Generator,
    description="Use this tool to generate a SQL query based on the user's question."
)


def Generate_Answer(user_query):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content":  user_query,
            }
        ],

        model="llama-3.3-70b-versatile"
    )

    return chat_completion.choices[0].message.content