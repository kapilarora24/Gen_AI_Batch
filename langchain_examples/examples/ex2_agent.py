# high level create agent example
from langchain.agents import create_agent
from dotenv import load_dotenv  # uv add packagename

# load the env variable
load_dotenv()

my_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    system_prompt="""you are a helpful assistant. \
        " your answer should be simple and easy to undertsand. Don't talk much.""",  # roles and goals
)
response = my_agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in chennai?"}]}
)

print(response["messages"][-1].text)


# Token count input, output and total
ai_message = response["messages"][-1]
print(ai_message.usage_metadata)
