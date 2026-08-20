from src.api.v1.agents.agents import run_search_agent_stream, run_search_agent


# method for non streaming response
def query_documents(query: str, user_id: str):
    print(query)
    return run_search_agent(query, user_id)


# method for streaming response
async def query_documents_stream(query: str, user_id: str):
    # just return async generator
    return run_search_agent_stream(query, user_id)
