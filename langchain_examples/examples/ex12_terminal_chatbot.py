from dotenv import load_dotenv
from langchain.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import uuid

load_dotenv()


model = ChatOpenAI(model="gpt-5.5")


print("Chatbot started. Type 'exit' to quit.\n")

chat_id = str(uuid.uuid4())

messages = []


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(
        messages,
        config={
            "run_name": "terminal_chatbot",
            "metadata": {"user_id": "kapil"},
            "chat_id": chat_id,
        },
    )

    messages.append(AIMessage(content=response.content))

    print(f"Bot: {response.content}\n")
