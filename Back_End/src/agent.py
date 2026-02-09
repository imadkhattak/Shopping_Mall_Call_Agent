from .config import pinecone_api_key, pinecone_index_name, groq_api_key
from .prompts import SQL_Prompt
from pinecone import Pinecone
from groq import Groq  # your LLM client

# Initialize clients
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(pinecone_index_name)
groq = Groq(api_key=groq_api_key)

def SQL_Query_Generator(user_query, top_k=5):
 
    query_embedding = pc.inference.embed(
        model="llama-text-embed-v2",
        inputs=[user_query],
        parameters={"input_type": "passage"}
    ).data[0]["values"]


    results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    

    schema_context = ""
    for match in results.matches:
        table = match.metadata.get("table")
        columns = match.metadata.get("columns", [])
        schema_context += f"{table}({','.join(columns)})\n"
    
    system_prompt = SQL_Prompt.format(
        schema_context=schema_context.strip(),
        user_question=user_query
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
    
    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    
    sql_query = response.choices[0].message.content
    return sql_query

