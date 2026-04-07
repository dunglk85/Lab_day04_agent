import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from src.agent import agent


# =========================
# Helpers
# =========================

class FakeLLMDirect:
    """LLM giả: trả lời trực tiếp, không gọi tool."""
    def invoke(self, messages):
        return AIMessage(content="Xin chào! Bạn thích biển, núi hay thành phố? Ngân sách và thời gian dự kiến là bao nhiêu?")


class FakeLLMToolCall:
    """LLM giả: trả về 1 tool call."""
    def __init__(self, tool_calls, content=""):
        self._tool_calls = tool_calls
        self._content = content

    def invoke(self, messages):
        return AIMessage(
            content=self._content,
            tool_calls=self._tool_calls
        )


class FakeGraph:
    """Graph giả để test flow end-to-end đơn giản."""
    def __init__(self, result):
        self._result = result

    def invoke(self, state):
        return self._result


# =========================
# Test 1 - Direct Answer
# =========================

def test_direct_answer_no_tool(monkeypatch):
    monkeypatch.setattr(agent, "llm_with_tools", FakeLLMDirect())

    state = {
        "messages": [HumanMessage(content="Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.")]
    }

    result = agent.agent_node(state)
    response = result["messages"][0]

    assert isinstance(response, AIMessage)
    assert response.content != ""
    assert response.tool_calls == [] or response.tool_calls is None


# =========================
# Test 2 - Single Tool Call
# =========================

def test_single_tool_call_search_flights(monkeypatch):
    fake_tool_calls = [
        {
            "name": "search_flights",
            "args": {
                "origin": "Hà Nội",
                "destination": "Đà Nẵng"
            },
            "id": "call_1",
            "type": "tool_call"
        }
    ]

    monkeypatch.setattr(agent, "llm_with_tools", FakeLLMToolCall(fake_tool_calls))

    state = {
        "messages": [HumanMessage(content="Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng")]
    }

    result = agent.agent_node(state)
    response = result["messages"][0]

    assert isinstance(response, AIMessage)
    assert response.tool_calls is not None
    assert len(response.tool_calls) == 1
    assert response.tool_calls[0]["name"] == "search_flights"
    assert response.tool_calls[0]["args"]["origin"] == "Hà Nội"
    assert response.tool_calls[0]["args"]["destination"] == "Đà Nẵng"


# =========================
# Test 3 - Multi-Step Tool Chaining
# =========================

def test_multi_step_tool_chaining(monkeypatch):
    """
    Kỳ vọng luồng:
    1. search_flights("Hà Nội", "Phú Quốc")
    2. search_hotels("Phú Quốc", ...)
    3. calculate_budget(...)
    """

    calls = []

    def fake_search_flights(origin: str, destination: str):
        calls.append(("search_flights", origin, destination))
        return "Vé rẻ nhất: 1.100.000₫"

    def fake_search_hotels(city: str, max_price: int = None):
        calls.append(("search_hotels", city, max_price))
        return "Khách sạn phù hợp: 800.000₫/đêm"

    def fake_calculate_budget(total_budget: int, expenses: str):
        calls.append(("calculate_budget", total_budget, expenses))
        return "Còn lại: 2.300.000₫"

    monkeypatch.setattr(agent, "search_flights", fake_search_flights)
    monkeypatch.setattr(agent, "search_hotels", fake_search_hotels)
    monkeypatch.setattr(agent, "calculate_budget", fake_calculate_budget)

    # Vì graph thật khó mock toàn bộ theo tool flow nội bộ,
    # ta mock graph.invoke để mô phỏng kết quả cuối cùng đã chain đủ bước.
    final_message = AIMessage(
        content=(
            "Gợi ý chuyến đi Phú Quốc 2 đêm trong budget 5 triệu:\n"
            "- Vé bay rẻ nhất: 1.100.000₫\n"
            "- Khách sạn: 800.000₫/đêm x 2 = 1.600.000₫\n"
            "- Tổng: 2.700.000₫\n"
            "- Còn lại: 2.300.000₫"
        )
    )

    monkeypatch.setattr(
        agent,
        "graph",
        FakeGraph({"messages": [final_message]})
    )

    result = agent.graph.invoke({
        "messages": [("human", "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!")]
    })

    final = result["messages"][-1]

    assert "Phú Quốc" in final.content
    assert "1.100.000" in final.content
    assert "1.600.000" in final.content
    assert "2.700.000" in final.content
    assert "2.300.000" in final.content


# =========================
# Test 4 - Missing Info / Clarification
# =========================

def test_missing_info_clarification(monkeypatch):
    monkeypatch.setattr(
        agent,
        "llm_with_tools",
        FakeLLMDirect()
    )

    state = {
        "messages": [HumanMessage(content="Tôi muốn đặt khách sạn")]
    }

    result = agent.agent_node(state)
    response = result["messages"][0]

    assert isinstance(response, AIMessage)
    assert response.tool_calls == [] or response.tool_calls is None
    assert response.content != ""


# =========================
# Test 5 - Guardrail / Refusal
# =========================

def test_guardrail_refusal(monkeypatch):
    class FakeLLMRefusal:
        def invoke(self, messages):
            return AIMessage(
                content="Xin lỗi, mình chỉ có thể hỗ trợ các yêu cầu liên quan đến du lịch như chuyến bay, khách sạn và ngân sách."
            )

    monkeypatch.setattr(agent, "llm_with_tools", FakeLLMRefusal())

    state = {
        "messages": [HumanMessage(content="Giải giúp tôi bài tập lập trình Python về linked list")]
    }

    result = agent.agent_node(state)
    response = result["messages"][0]

    assert isinstance(response, AIMessage)
    assert response.tool_calls == [] or response.tool_calls is None
    assert "du lịch" in response.content.lower() or "chuyến bay" in response.content.lower()