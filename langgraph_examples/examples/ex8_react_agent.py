from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI  # uv add langchain-openai python-dotenv
from langchain_core.tools import tool
from tavily import TavilyClient  # uv add tavily-python
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatOpenAI(model="gpt-5.5")


# setting up tavily search client
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class AgentState(TypedDict):
    query: str
    thought: str
    action: str
    observation: str
    final_answer: str


# Tool #1: websearch
def web_search_tool(query: str):
    print("Searching the web for the query: ", query)
    search_results = tavily_client.search(query)
    return search_results


# # Tool #2: calculator
def calculator_tool(query: str):
    print("Calling calculator_tool")
    try:
        expression = llm.invoke(f"""
           Extract ONLY the mathematical expression from the user's request.


           User:
           {query}


           Examples:
           What's 10+10? -> 10+10
           Calculate (15*8)+2 -> (15*8)+2
           What is 100/4? -> 100/4


           Return only the expression.
           """).content.strip()
        return str(eval(expression))
    except:
        return "Error in Calculation"


def think_node(state: AgentState):
    prompt = f"""
       You are an Agent. Decide the next step for the query:
       {state["query"]}.  
    
       Previous Observation: {state['observation']}


       Choose one:
       - search (if you feel like web search is required for the query)
       - calculate (for even simple math return this )
       - finish (if the model can answer directly)
      
     Respond with only one word.
   """

    action = llm.invoke(prompt).content

    return {**state, "action": action}


def act_node(state: AgentState):
    # let's call the tool from this node
    action = state["action"]

    if action == "search":
        result = web_search_tool(state["query"])
    elif action == "calculate":
        result = calculator_tool(state["query"])
    else:
        result = "No Tool Call Required"

    print("Action -->", action)

    print(result)

    return {**state, "observation": result}


def answer_node(state: AgentState):
    print("Preparing to generate an answer")
    print("Context", state["observation"])
    response = llm.invoke(f"""
       User Question:
       {state["query"]}


       Previous Tool Result:
       {state["observation"]}
   """)

    return {**state, "final_answer": response.content}


def route(state: AgentState):
    if state["action"] == "finish":
        return "LLM_CAN_ANSWER"

    return "ACTION_REQUIRED"


workflow = StateGraph(AgentState)


workflow.add_node("think", think_node)
workflow.add_node("act", act_node)
workflow.add_node("answer", answer_node)


workflow.add_edge(START, "think")
workflow.add_conditional_edges(
    "think", route, {"ACTION_REQUIRED": "act", "LLM_CAN_ANSWER": "answer"}
)


# Loop
workflow.add_edge("act", "think")
workflow.add_edge("answer", END)


app = workflow.compile()


# generating and saving the graph visualization
graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex8_simple_react_agent.png", "wb") as f:
    f.write(graph_image)


final_response = app.invoke(
    {
        "query": "what's 10+10 and who is winner for FIFA 2026",
        "thought": "",
        "action": "",
        "observation": "",
        "final_answer": "",
    }
)


print("Query: ", final_response["query"])
print("Thought: ", final_response["thought"])
print("Action: ", final_response["action"])
print("Observation: ", final_response["observation"])
print("Final Answer: ", final_response["final_answer"])
