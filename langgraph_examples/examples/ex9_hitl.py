# Let's have a simple agent with human-in-the-loop review or revision

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5")


# State
class AgentState(TypedDict):
    query: str
    draft_answer: str
    is_approved: bool
    review_comments: str
    final_answer: str


def draft_node(state: AgentState):
    """Creating draft answer."""
    response = llm.invoke(f"""Answer the following question concisely:

{state['query']}
""")

    return {
        **state,
        "draft_answer": response.content,
    }


def human_review_node(state: AgentState):
    """Simulating human approval.

    In real applications:
    UI / API / CLI
    """

    print(f"\nReview this answer:\n{state['draft_answer']}")

    reviewer_input = input("\nApprove? (yes/no): ").strip().lower()
    is_approved = reviewer_input == "yes"

    if not is_approved:
        review_comments = input("Review Comments: ").strip()

        return {
            **state,
            "is_approved": is_approved,
            "review_comments": review_comments,
        }

    return {
        **state,
        "is_approved": is_approved,
        "review_comments": "",
    }


def finalize_node(state: AgentState):
    """Finalize approved answer."""
    print("\nApproved. Sending answer...")

    return {
        **state,
        "final_answer": state["draft_answer"],
    }


def revise_node(state: AgentState):
    """Revise answer based on review comments."""
    print("\nRevising answer...")

    response = llm.invoke(f"""Revise the answer for the following query:

Query:
{state['query']}

Here's the draft answer:
{state['draft_answer']}

Based on the following review comments:
{state['review_comments']}
""")

    return {
        **state,
        "draft_answer": response.content,
    }


def review_route(state: AgentState):
    if state["is_approved"]:
        return "FINALIZE"

    return "REVISE"


# build the graph
workflow = StateGraph(AgentState)
workflow.add_node("draft", draft_node)
workflow.add_node("review", human_review_node)
workflow.add_node("finalize", finalize_node)
workflow.add_node("revise", revise_node)


workflow.add_edge(START, "draft")
workflow.add_edge("draft", "review")


workflow.add_conditional_edges(
    "review", review_route, {"FINALIZE": "finalize", "REVISE": "revise"}
)


# loop until approved
workflow.add_edge("revise", "review")
workflow.add_edge("finalize", END)


app = workflow.compile()


# generating and saving the graph visualization
graph_image = app.get_graph().draw_mermaid_png()
with open("examples/ex9_hitl.png", "wb") as f:
    f.write(graph_image)


result = app.invoke(
    {
        "query": "Explain Langgraph in simpler terms",
        "draft_answer": "",
        "approval": False,
        "final_answer": "",
    }
)


print("Final Answer: ", result["final_answer"])
