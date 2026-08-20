from src.api.v1.agents.agents import run_search_agent_stream, run_search_agent
from src.core.guardrails import guard_input, guard_output


# method for non streaming response
def query_documents(query: str, user_id: str):
    print(query)
    # Input guardrail: toxicity
    guard_input(query)

    result = run_search_agent(query, user_id)

    if isinstance(result, dict) and result.get("response"):
        # output guardrails for PII
        result["response"] = guard_output(result["response"])

    return result


# method for streaming response
async def query_documents_stream(query: str, user_id: str):
    # Input guardrail: toxicity
    guard_input(query)

    result = await run_search_agent_stream(query, user_id)
    print("=============OUTPUT IS ABOUT TO BE SENT============")

    if isinstance(result, dict) and result.get("response"):
        print("INSIDE IF")
        result["response"] = guard_output(result["response"])

    return result