from .config import api_key

client = Groq(api_key=api_key)

def SQL_Query_Generator(user_query):
    
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