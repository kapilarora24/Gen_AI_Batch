# role based prompt
# chaining with langchain

from dotenv import load_dotenv  # uv add packagename
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

# load the env variable
load_dotenv()

# prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """you are a sesones sales person" 
        having experience in persuasive product description""",
        ),
        (
            "user",
            """
        write a product description from the {query} using the following details
        - Product Name
        - Category
        - Features
        - Price
        - release Date
        """,
        ),
    ]
)

# How to initialize the modell to create a chain/pipeline with prompt template

model = ChatOpenAI(model="gpt-5.5", api_key=os.getenv("OPENAI_API_KEY"))


# chainning with langchain

pipeline = prompt | model

# invoke the pipeline
response = pipeline.invoke(
    {"query": """LG webos TV, Electronics, 128 watt sound, magic remote, super quality
        100*80*20 (55 inch)
        120000rs
        Jun 2026
        """}
)

print(response.content)
