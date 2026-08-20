# this example demonstrates how to have the LLM dynamically
# call multiple tools in a single response,
# and how to structure the graph and state for that use case.
# The agent_node relying on should_continue will keep invoking the LLM until there are
# no more tool calls in the response, allowing for complex
# interactions where the LLM can decide to call multiple tools
# in sequence.
# REFER: tool calling explainer.md file in the same directory

from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI  # uv add langchain-openai python-dotenv
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests

load_dotenv()


llm = ChatOpenAI(model="gpt-5.5")


@tool
def calculator_tool(expression: str):
    """Evaluate Math expression. For all your calculations you must use this function"""
    print("Calling calculator_tool")
    try:
        return str(eval(expression))
    except:
        return "Error in Calculation"


@tool
def weather_tool(latitude: str, longitude: str):
    """
    use this tool to get weather info for a valid city's latitude and longitude
    """
    print("Calling weather_tool")
    print("Geocoordinates :" + latitude + " and  " + longitude)

    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_output = requests.get(weather_api_url)
    current_weather = weather_output.json()
    return current_weather


tools = [calculator_tool, weather_tool]

# bind the tool

llm_with_tools = llm.bind_tools(tools)


class AgentState(TypedDict):
    messages: Annotated[List, add_messages]


def agent_node(state: AgentState):

    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def should_conitnue(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "MORE TOOLS TO CALL"

    return "NO MORE TOOLS TO CALL"


tool_node = ToolNode(tools)

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges(
    "agent",
    should_conitnue,
    {"MORE TOOLS TO CALL": "tools", "NO MORE TOOLS TO CALL": END},
)

workflow.add_edge("tools", "agent")

app = workflow.compile()

# generating and saving the graph visualization
graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex6_tool_node.png", "wb") as f:
    f.write(graph_image)

result = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "what is the weather in chennai and multiple by 2 and add 10",
            }
        ]
    }
)

print(result["messages"][-1].content)
