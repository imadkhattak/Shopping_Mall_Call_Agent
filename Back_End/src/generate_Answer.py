from groq import Groq
from .config import api_key
from langchain.tools import Tool
from agent import SQL_Query_Generator
# from database_schema_embedding import embed_and_store_schema


llm = Groq(api_key=api_key)


def Generate_Answer(user_query):
    
    chat_completion = llm.chat.completions.create(

        model="llama-3.3-70b-versatile",

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

        tools=[{"name": "SQL_Query_Generator", "func": SQL_Query_Generator, 
        "description": "Use this tool to generate a SQL query based on the user's question."}]
        
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    user_query = "what is your mall name?"
    result = Generate_Answer(user_query)
    print(result)