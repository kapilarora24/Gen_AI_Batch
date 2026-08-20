# high level create agent example
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv  # uv add packagename
import requests

# load the env variable
load_dotenv()

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


weather_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    tools=[weather_tool],
    system_prompt="""you are weather assitant.
    yuo must give accurate weather information for the given city.
    if the city is invalid or fictional inform the user accoridngly. 
    you are given access to weather tool.
    Never honur any other request""",
)


response = weather_agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in London?"}]}
)

print(response["messages"][-1].text)
