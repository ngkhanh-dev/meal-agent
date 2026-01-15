from langgraph.graph import END
from state import OrderState

def route_after_validate(state: OrderState):
    # if state.get("clarification_question"):
    #     return END

    # if state.get("order_summary"):
    #     return "clarify"

    return "chatbot"


def route_after_clarify(state: OrderState):
    decision = state.get("confirmation")

    if decision == "chỉnh sửa":
        return "understand"

    if decision == "đồng ý":
        return "chatbot"

    return "chatbot"

from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Literal
import os
import json
import re

Flow = Literal["menu", "order", "other"]

EXPLICIT_MENU = [
    "menu", "thực đơn", "xem menu", "xem thực đơn"
]

EXPLICIT_ORDER = [
    "đặt", "order", "mua", "cho tôi", "thêm", "bớt", "xác nhận đơn"
]

CONFIDENCE_THRESHOLD = 0.75

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)
    return json.loads(raw)


def _llm_detect_flow(user_message: str) -> Flow:
    prompt = f"""
Bạn là bộ phân loại intent cho chatbot đặt cơm.

Chọn ĐÚNG 1 trong 3 nhãn:
- "menu"
- "order"
- "other"

Trả về JSON:
{{
  "flow": "...",
  "confidence": 0.x
}}

User message:
"{user_message}"
"""

    resp = llm.invoke(prompt)
    data = _extract_json(resp.content)

    flow = data.get("flow")
    conf = float(data.get("confidence", 0))

    if flow not in ("menu", "order", "other"):
        return "other"

    if conf < CONFIDENCE_THRESHOLD:
        return "other"

    return flow


def route_after_flow(state: dict) -> str:
    """
    ROUTE FUNCTION
    - gọi rule + LLM
    - KHÔNG mutate state
    - chỉ quyết định nhánh
    """

    user_msg = state.get("user_message", "").lower().strip()
    prev_flow = state.get("active_flow")

    # 1. Rule-based
    if any(k in user_msg for k in EXPLICIT_MENU):
        new_flow = "menu"

    elif any(k in user_msg for k in EXPLICIT_ORDER):
        new_flow = "order"

    # 2. LLM fallback
    else:
        new_flow = _llm_detect_flow(user_msg)

        if new_flow == "other":
            new_flow = prev_flow or "menu"

    if prev_flow is not None and new_flow != prev_flow:
        return "reset"

    # 4. Giữ flow → đi tiếp
    return new_flow



# from typing import Literal

# def intent_classification(state: dict):
#     active_flow = state.get("active_flow")
#     return active_flow


# from langgraph.graph import END

# def router_after_order(state: OrderState):
#     if state.get("intent_changed"):
#         return "reset_intent"
    
#     intent = state.get("intent")
#     if intent == "CREATE":
#         return "create_order"
#     elif intent == "DELETE":
#         return "delete_order"
#     elif intent == "READ":
#         return "read_order"
#     else:
#         return END
