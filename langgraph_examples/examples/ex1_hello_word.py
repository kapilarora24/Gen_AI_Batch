from langgraph.graph import StateGraph, MessagesState, START, END


def mock_llm(state: MessagesState):
    print("mock_llm called")
    print(state)
    return {"messages": [{"role": "ai", "content": "Hello World"}]}


graph = StateGraph(MessagesState)

graph.add_node("mock_llm", mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)

graph = graph.compile()

result = graph.invoke({"messages": [{"role": "user", "content": "Hey!"}]})
print("*" * 50)

print(result)
