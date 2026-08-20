# high level create agent example
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv  # uv add packagename

# load the env variable
load_dotenv()

# what is a tool - tool is a function that an agent call. Tool must have a name and description


@tool
def weather_tool(city: str):
    """
    use this tool to get weather info for a valid city
    """
    print("City is:" + city)
    return "Temparature in" + city + "20 degree C"


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
    {"messages": [{"role": "user", "content": "what is the weather in Australia?"}]}
)

print(response["messages"][-1].text)


# Token count input, output and total
ai_message = response["messages"][-1]
print(ai_message.usage_metadata)
