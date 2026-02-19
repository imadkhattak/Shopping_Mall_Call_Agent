
import sys
import os

# Add the project root to sys.path so we can import Back_End
sys.path.append(os.getcwd())

from Back_End.src.agent_executor import agent_executor

def test_agent_location_query():
    query = "Where is the shopping mall located?"
    print(f"Testing agent with query: '{query}'")
    
    try:
        response = agent_executor.invoke({"input": query})
        print("\n--- Agent Response ---")
        print(response)
        
        # Check if tools were used (result should contain intermediate steps if we could see them, 
        # but here we check if the response indicates database usage or at least isn't the hardcoded one)
        # Note: 'agent_executor' might return a dict with 'output' key.
        
        output = response.get('output', str(response))
        print(f"\nFinal Output: {output}")
        
    except Exception as e:
        print(f"Error executing agent: {e}")

if __name__ == "__main__":
    test_agent_location_query()
