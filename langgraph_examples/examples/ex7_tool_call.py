# this example demonstrates how to have the LLM dynamically
# call multiple tools in a single response,
# and how to structure the graph and state for that use case.
# The agent_node will keep invoking the LLM until there are
# no more tool calls in the response, allowing for complex
# interactions where the LLM can decide to call multiple tools
# in sequence.

# REFER: tool calling explainer.md file in the same directory
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, START, END
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

# Bind the tools to LLM
llm_with_tools = llm.bind_tools(tools)


# Custom State
class AgentState(TypedDict):
    query: str
    messages: List
    result: str


def agent_node(state: AgentState):
    print("Agent is thinking...")
    messages = list(state["messages"])

    # dynamically call tools until LLM has no more tool_calls in its response
    while True:
        # human message will go
        response = llm_with_tools.invoke(messages)

        print("1. Agent Response", response)
        # ai response will get added to the messages
        messages.append(response)

        # loading all existing tools in tool map
        tool_map = {t.name: t for t in tools}
        print(tool_map)

        print("*************")
        print(f"""2. Do we have Response with Tool calls? {response.tool_calls} """)
        print("*************")

        if not response.tool_calls:
            break

        # executing all tool calls that we see in the response
        for tool_call in response.tool_calls:
            print("================ 3. INSIDE THE FOR IN LOOP ============")
            print(tool_call)
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]

            print(f"3.1. TOOL SELECTED: {tool_name}")
            tool_fn = tool_map[tool_name]  # getting executable tool function
            print("$$$$$$$ 3.2. Manually calling the tool $$$$$$$")
            tool_result = tool_fn.invoke(tool_args)
            print("^^^^^^^^^^^^^^^^^ 3.3. Tool Result ^^^^^^^^^^")
            print(tool_result)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": str(tool_result),
                }
            )

    return {**state, "messages": messages, "result": response.content}


# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

app = workflow.compile()

# generating and saving the graph visualization
graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex7_tool_call.png", "wb") as f:
    f.write(graph_image)


final_response = app.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Hey! tell me the weather in chennai and multiply that by 2 and add 100",
            }
        ]
    }
)


print(final_response["result"])
