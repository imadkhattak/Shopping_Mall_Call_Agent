# agent_executor.py

from langchain.agents import create_agent
from .llm import llm
from .tools import sql_query_generator, sql_executor

tools = [sql_query_generator, sql_executor]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""
You are a shopping mall database assistant\n\nWhen needed:\n
1. Use sql_query_generator to get relevant schema.\n
2. Generate a SQL query.\n
3. Use sql_executor to run it.\n
4. Return a clear explanation of the results to the user.
"""
)

agent_executor = agent
