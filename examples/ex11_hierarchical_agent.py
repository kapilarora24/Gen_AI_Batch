from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv  # uv add packagename
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List
import requests
import os

# load the env variable
load_dotenv()


# initializing model for all agents
model = ChatOpenAI(model="gpt-5.5")

# researcher agent
reseracher_agent = create_agent(
    model=model,
    system_prompt="""
        you are a researcher. Provide well researched content with correct detailed.
""",
)


def researcher_tool(query: str):
    """call the research agent to gather necessary information"""
    print("Calling researcher_tool")
    print(query)
    print("========")
    researcher_output = reseracher_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return researcher_output["messages"][-1].content


# writer agent
writer_agent = create_agent(
    model=model,
    system_prompt="""
        you are a writer. Provide details on topic with summarized details.
""",
)


def writer_tool(query: str):
    """call the writer agent to write summary on the topic"""
    print("Calling writer_tool")
    print(query)
    print("========")
    writer_output = writer_agent.invoke(
        {"messages": [{"role": "user", "content": query}]}
    )
    return writer_output["messages"][-1].content


# supervisor agent
supervisor_agent = create_agent(
    model=model,
    tools=[writer_tool, researcher_tool],
    system_prompt="""
      you are a supervisor agent. You cordinate  task between special agents:
      Analyse the task clearly and decide which agent should work on what. 
        First ask to researcher agent to gather necessary infirmation       
        - use researcher tool if yuo feel like more research to be done on the query. 
        - use writer tool for writing,  editing and summarizing.
        Delegate task to  the appropriate agent and combine their outputs to 
        answer the user.
""",
)

my_task = "Reserach the benefits of protien and summarize 3 paragrah summary"

supervisors_output = supervisor_agent.invoke(
    {"messages": [{"role": "user", "content": my_task}]}
)

print(supervisors_output["messages"][-1].text)
