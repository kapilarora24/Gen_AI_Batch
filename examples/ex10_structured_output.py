# high level create agent example
from langchain.agents import create_agent
from langchain_core.tools import tool
from dotenv import load_dotenv  # uv add packagename
from tavily import TavilyClient
from pydantic import BaseModel, Field
from typing import List
import requests
import os

# load the env variable
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# 1.  Let us defined structure (output Schema)
class NewsArtcile(BaseModel):
    "A Single News Article"

    title: str = Field(description="A News Article")
    summary: str = Field(description="Brief summary of the aticle")
    artcle: str = Field(description="url of the news")
    source: str = Field(description="Publisher or source of the news")


# 2, let us make th list of article
class AINewsResponse(BaseModel):
    """Structured Output from AI"""

    topic: str = Field(description="The specific topic")
    artilcels: List[NewsArtcile] = Field(description="List of releavnt news found")
    overall_summary: str = Field(description="High level summary of the topic")


@tool
def web_search_tool(query: str):
    """use this tool to search the web"""

    print("searching with the web:")
    print(query)
    search_result = tavily_client.search(query)
    return search_result


general_purpose_agent = create_agent(
    model="openai:gpt-5.5",  # brain of the agent
    tools=[web_search_tool],
    response_format=AINewsResponse,  # it must output structured
    system_prompt="""you are a helpful assistant capable of
    getting real time  iformation from the web.
    use the websearch tool to answer query
    if not able to find relevant output tell the user that answer not found.""",  # roles and goals
)

response = general_purpose_agent.invoke(
    {"messages": [{"role": "user", "content": "Tell me about weather in india?"}]}
)

news: AINewsResponse = response["structured_response"]

print(news)  # pydantic format

# if you want only json format
print(news.model_dump_json(indent=2))
