from openai import OpenAI
from src.config import openai_api_key
from .agent_executor import agent_executor

client = OpenAI(api_key=openai_api_key)


if __name__ == "__main__":
    response = agent_executor.invoke(
        {
            "messages": [
                {"role": "user", "content": "Can you give me the contact information of the mall?"}
            ]
        }
    )

    # response.messages is a list of LangChain message objects
    messages = response["messages"] if isinstance(response, dict) else response.messages

    # Find the final AI message
    final_message = None
    for msg in reversed(messages):
        # Use attributes, not dict-style access
        if hasattr(msg, "type") and msg.type == "ai":
            final_message = getattr(msg, "content", None)
            break

    print(final_message)
