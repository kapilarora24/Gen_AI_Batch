import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()


def agent_with_tools(query: str) -> str:
    """Runs a ReAct agent with custom tools and returns the final answer."""

    try:

        @tool
        def word_count(text: str) -> int:
            """Returns the number of words in a text."""
            return len(text.split())

        @tool
        def reverse_text(text: str) -> str:
            """Returns the text reversed word-by-word."""
            return " ".join(text.split()[::-1])

        tools = [word_count, reverse_text]

        llm = ChatOpenAI(model="gpt-4o-mini")

        agent = create_agent(model=llm, tools=tools)

        result = agent.invoke({"messages": [{"role": "user", "content": query}]})

        return result["messages"][-1].content

    except Exception as exception:
        return f"Error while running agent: {str(exception)}"


result = agent_with_tools(
    "How many words are in 'The quick brown fox'? Also reverse it."
)

print(result)
