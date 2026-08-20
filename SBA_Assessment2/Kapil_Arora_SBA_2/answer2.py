import os
from dotenv import load_dotenv

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()


def conversation_with_memory() -> list:
    """Runs a 3-turn conversation and returns the full message history."""

    store = {}

    # Create the prompt for chat history
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant. Remember information from "
                "the conversation and use it when answering later questions.",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = prompt | llm

    # Function to retrieve or create session history
    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()

        return store[session_id]

    # Add message history functionality
    conversation_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    # Use session ID for all turns
    session_id = "alex_conversation"

    # Turn 1
    conversation_chain.invoke(
        {"input": "My name is Alex. What is machine learning?"},
        config={"configurable": {"session_id": session_id}},
    )

    # Turn 2
    conversation_chain.invoke(
        {"input": "Can you give me a real-world example?"},
        config={"configurable": {"session_id": session_id}},
    )

    # Turn 3
    conversation_chain.invoke(
        {"input": "What is my name?"},
        config={"configurable": {"session_id": session_id}},
    )

    # Get the complete conversation history
    history = store[session_id].messages

    result = []

    for message in history:
        if message.type == "human":
            role = "human"
        elif message.type == "ai":
            role = "ai"
        else:
            role = message.type

        result.append((role, message.content))

    return result


result = conversation_with_memory()

for role, content in result:
    print(f"{role}: {content}")
