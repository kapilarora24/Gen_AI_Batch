# high level create agent example
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv  # uv add packagename
from tavily import TavilyClient
import requests
import os

# load the env variable
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def weather_tool(latitude: str, longitude: str):
    """
    use this tool to get weather info for a valid city
    """
    print("Geocordinates are :" + latitude + " and " + longitude)

    weather_api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
    weather_output = requests.get(weather_api_url)
    current_weather = weather_output.json()
    return current_weather


@tool
def web_search_tool(query: str):
    """use this tool to search the web"""

    print("searching with the web:")
    print(query)
    search_result = tavily_client.search(query)
    return search_result


general_purpose_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    tools=[weather_tool, web_search_tool],
    system_prompt="""you are a helpful assistant caable of giving weather update,
    and real time  iformation from the web.
    you must provide accurate weather information for given city's latitude and longitude
    if teh city ininvalid 
    you are given access to right tool to get weather info and real time udpates from web.""",  # roles and goals
)

response = general_purpose_agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in London?"}]}
)

print(response["messages"][-1].text)

# Token count input, output and total
ai_message = response["messages"][-1]
usage = ai_message.response_metadata.get("token_usage", {})

print("Input Tokens:", usage.get("prompt_tokens"))
print("Output Tokens:", usage.get("completion_tokens"))
print("Total Tokens:", usage.get("total_tokens"))
