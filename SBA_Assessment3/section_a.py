from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
import re

def graph_with_checkpointing() -> list:
    """Runs a 2-turn chat graph with memory. Returns [answer1, answer2]."""
    try:
        def chat_node(state: MessagesState):
            messages = state["messages"]
            favourite_number = None
            for message in messages:
                content = getattr(message, "content", "")
                if "favourite number is" in content.lower():
                    try:
                        number_text = content.lower().split(
                            "favourite number is", 1
                        )[1].strip()
                        number_text = number_text.split(".")[0].strip()
                        favourite_number = int(number_text)
                    except (ValueError, IndexError):
                        pass
            current_message = messages[-1]
            current_content = getattr(current_message, "content", "").lower()
            # Turn 1
            if "remember it" in current_content and favourite_number is not None:
                answer = (
                    f"Got it! I will remember that your favourite number "
                    f"is {favourite_number}."
                )
            # Turn 2
            elif "multiplied by 2" in current_content:
                if favourite_number is not None:
                    answer = str(favourite_number * 2)
                else:
                    answer = "I don't remember your favourite number."
            else:
                answer = "I don't have enough information to answer that."
            return {"messages": [AIMessage(content=answer)]}
        # Build graph
        builder = StateGraph(MessagesState)
        builder.add_node("chat", chat_node)
        builder.add_edge(START, "chat")
        builder.add_edge("chat", END)
        # MemorySaver = checkpointing
        memory = MemorySaver()
        graph = builder.compile(checkpointer=memory)
        config = {
            "configurable": {
                "thread_id": "session-1"
            }
        }
        # Turn 1
        turn1 = "My favourite number is 42. Remember it."
        result1 = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=turn1)
                ]
            },
            config,
        )
        answer1 = result1["messages"][-1].content
        # Turn 2
        turn2 = "What is my favourite number multiplied by 2?"
        result2 = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=turn2)
                ]
            },
            config,
        )
        answer2 = result2["messages"][-1].content
        return [answer1, answer2]
    except Exception as error:
        print(f"Checkpointing graph error: {error}")
        return [
            "Unable to process the first turn.",
            "Unable to process the second turn."
        ]
    
if __name__ == "__main__":
    result = graph_with_checkpointing()
    print(result)
