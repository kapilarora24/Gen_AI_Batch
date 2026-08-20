from langchain.chat_models import init_chat_model
from dotenv import load_dotenv  # uv add packagename

import os

# load the env variable
load_dotenv()

# lets check whether API is available
# print(os.getenv("OPENAI_API_KEY"))

# model = init_chat_model("openai:gpt-5.5")

# response = model.invoke("write a story about lion")
# print(response.content)

model = init_chat_model("openai:gpt-5.5")

response = model.invoke("hey")
print(response.content)
