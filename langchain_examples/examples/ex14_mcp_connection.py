from langchain.agents import create_agent
import asyncio

# uv add langchain-mcp-adapters
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os

# load the env variables
load_dotenv()


async def main():
    client = MultiServerMCPClient(
        {
            "calc_weather": {
                "transport": "http",  # HTTP-based remote server
                "url": "http://localhost:9001/mcp",
            },
            "tavily": {
                "transport": "http",  # HTTP-based remote server
                "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={os.getenv('TAVILY_API_KEY')}",
            },
        }
    )

    tools = await client.get_tools()

    agent = create_agent(
        model="openai:gpt-5.5",
        tools=tools,  # loading all MCP server tools
        system_prompt="""You are a helpful assistant.
           You must use the given tools to get answer for add, subtract and also for weather information.
       """,
    )

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "what's the latest version chatgpt model?",
                }
            ]
        }
    )
    print(response["messages"][-1].text)


if __name__ == "__main__":
    asyncio.run(main())
