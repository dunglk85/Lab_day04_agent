from pathlib import Path
from typing import Annotated
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.agent.tools import search_flights, search_hotels, calculate_budget

load_dotenv()

# 1. Đọc System Prompt
BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT = (BASE_DIR / "system_prompt.txt").read_text(encoding="utf-8")


# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    step: str  # "searching", "done"


# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    step = state.get("step", "searching")
    
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # == LOGGING ==
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"Gọi tool: {tc['name']} ({tc['args']})")
    else:
        print("Trả lời trực tiếp")

    # Nếu đã xong rồi thì không gọi tool nữa
    if step == "done":
        return {
            "messages": [response],
            "step": "done"
        }

    return {
        "messages": [response]
    }

    return {"messages": [response]}


# 5. Xây dựng Graph
builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Khai báo edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge("agent", END)

graph = builder.compile()


# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh")
    print("Gõ 'quit' để thoát")
    print("=" * 60)

    messages = []  # Accumulate conversation history

    while True:
        user_input = input("\nBạn: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            break

        print("\nTravelBuddy đang suy nghĩ...")

        # Add user input to history
        messages.append(("human", user_input))

        result = graph.invoke({"messages": messages})
        final = result["messages"][-1]

        # Add assistant response to history
        messages.append(("assistant", final.content))

        # Ensure we only print the final response content once
        if hasattr(final, 'content') and final.content:
            print(f"\nTravelBuddy: {final.content}")
        else:
            print("\nTravelBuddy: (Không có phản hồi)")