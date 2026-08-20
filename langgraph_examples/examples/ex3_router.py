from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict


# define custom state
class NumberState(TypedDict):
    number: int
    result: str


def check_node(state: NumberState):
    """Decide number is even or odd"""
    print("\n======== 1. Check Node ========")
    print("Received State", state)
    print(f"checking number:{state['number']}")
    return state


def route(state: NumberState):
    print("I am router. Number is even or add")
    print("\n======== 2. Route Node ========")
    print("Received State", state)

    if state["number"] % 2 == 0:
        return "EVEN_NUMBER"

    return "ODD_NUMBER"


def even_node(state: NumberState):
    """Number is even"""
    return {"result": f"{state['number']} is even"}


def odd_node(state: NumberState):
    """Number is odd"""
    return {"result": f"{state['number']} is odd"}


workflow = StateGraph(NumberState)

workflow.add_node("check", check_node)
workflow.add_node("even", even_node)
workflow.add_node("odd", odd_node)


workflow.add_edge(START, "check")


# making check node is router
workflow.add_conditional_edges(
    "check",
    route,
    {"EVEN_NUMBER": "even", "ODD_NUMBER": "odd"},
)

workflow.add_edge("even", END)
workflow.add_edge("odd", END)

app = workflow.compile()

graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex3_router.png", "wb") as f:
    f.write(graph_image)

result = app.invoke({"number": 7})
print(result)
