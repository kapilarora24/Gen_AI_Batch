# multi level agent without any tool
from langchain.agents import create_agent
from dotenv import load_dotenv  # uv add packagename

# load the env variable
load_dotenv()


writer_agent = create_agent(
    model="openai:gpt-5.5",
    system_prompt="""
    you are a creative content writer, working in a top media company. 
    your taks is to wirte engaging content and privide insightful updates on various topics with limited 100 words only.
    """,
)


editor_agent = create_agent(
    model="openai:gpt-5.5",
    system_prompt="""
    you are an editor, working in a same top media company. 
    your task is to review the draft content wirtten by writer and provide constructive 
    feedback to enhance the quality and egagement of the content insightful, you rewrite if necessary,
    under with the word limits only
    """,
)


# function
def sequential_pipeline(topic: str):
    # sequential execution pipeline
    writer_result = writer_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "write engainig cotent on the topic :{topic}}",
                }
            ]
        }
    )

    print(writer_result["messages"][-1].content)

    # sending writer content to editor
    editer_result = editor_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                Review the following content:
                {writer_result["messages"][-1].content}

                enhance it is needed to make more egaging, clear and insightful while keeping 
                the originial meaning intact. 

                also provide a short feedback session covering:
                -what has improved
                -why the improvements help
                -any remining suggestions

                Focus on:
                clarity
                readability
                grammer
                flow
                engagement

                you must provide 3 tites to this written content and with yuor recommendation  out of 3.

            """,
                }
            ]
        }
    )
    print(editer_result["messages"][-1].content)


sequential_pipeline("How AI Agnet will transform the way business run")
