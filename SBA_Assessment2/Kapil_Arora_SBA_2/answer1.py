import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def basic_lcel_chain(topic: str) -> str:
    """Returns a one-paragraph explanation of the given topic."""

    prompt = ChatPromptTemplate.from_template(
        "Explain the following topic in one simple paragraph: {topic}"
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    parser = StrOutputParser()

    chain = prompt | llm | parser

    try:
        result = chain.invoke({"topic": topic})
        return result
    except Exception as e:
        return f"Error while calling the LLM: {str(e)}"


result = basic_lcel_chain("quantum computing")
print(result)
