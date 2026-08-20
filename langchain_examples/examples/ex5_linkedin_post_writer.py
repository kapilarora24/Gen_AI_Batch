from langchain.agents import create_agent
from dotenv import load_dotenv  # uv add packagename

# load the env variable
load_dotenv()

linkedin_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    system_prompt="""You are an expert linkedin post writing agent.
    If the user asks for anything other than writing a linkedIn post and 
    topic is unsuitable for linkedIn, refuse it. aswer with only 40 - 45 words only
    Do not answer any other questions or tasks.""",
)
response = linkedin_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "write a linked post about LG webos TV specifications?",
            }
        ]
    }
)

print(response["messages"][-1].text)
