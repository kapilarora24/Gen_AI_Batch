from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict


# define custom state
class SimpleState(TypedDict):
    user_name: str
    message: str
    status: str


def greet_node(state: SimpleState):
    print("\n======== 1. Greet Node ========")
    print("Received State", state)

    # update the state
    my_message = "Hello, " + state["user_name"]
    return {"message": my_message}


def status_node(state: SimpleState):
    print("\n======== 2. Status Node ========")
    print("Received State", state)

    # update the state
    my_status = "Workflow completed for the user " + state["user_name"]
    return {"status": my_status}


# define the graph
workflow = StateGraph(SimpleState)

workflow.add_node("greet", greet_node)
workflow.add_node("status", status_node)

workflow.add_edge(START, "greet")
workflow.add_edge("greet", "status")
workflow.add_edge("greet", END)

workflow = workflow.compile()

# generating ans ave graph visulization

graph_image = workflow.get_graph().draw_mermaid_png()
with open("examples/ex2_greet.png", "wb") as f:
    f.write(graph_image)

result = workflow.invoke({"user_name": "Alice"})

print(result)
