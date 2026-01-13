from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Literal, Tuple
import re
import os
import json
from dotenv import load_dotenv
from tracing import trace_node

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)

Flow = Literal["menu", "order", "other"]

EXPLICIT_MENU = [
    "menu", "thực đơn", "xem menu", "xem thực đơn"
]

EXPLICIT_ORDER = [
    "đặt", "order", "mua", "cho tôi", "thêm", "bớt", "xác nhận đơn"
]

CONFIDENCE_THRESHOLD = 0.75

def extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)
    return json.loads(raw)

def llm_classify_intent(user_message: str) -> Tuple[Flow, float]:
    INTENT_PROMPT = """
        Bạn là bộ phân loại intent cho chatbot đặt cơm.

        Phân loại tin nhắn người dùng vào ĐÚNG 1 trong 3 nhãn:

        - "menu": xem thực đơn, hỏi món, hỏi có gì
        - "order": đặt món, thêm/bớt món, xác nhận hoặc chỉnh sửa đơn
        - "other": câu xã giao, xác nhận ("ok", "ừ", "tiếp đi"),
                KHÔNG thể hiện ý định chuyển flow

        Yêu cầu:
        - Chỉ trả về JSON hợp lệ
        - confidence ∈ [0, 1]
        - KHÔNG giải thích

        User message:
        "{user_message}"
    """
    resp = llm.invoke(
        INTENT_PROMPT.format(user_message=user_message)
    )

    data = extract_json(resp.content)

    flow = data.get("flow")
    conf = data.get("confidence")

    if flow not in ("menu", "order", "other"):
        raise ValueError("Invalid flow")

    if not isinstance(conf, (int, float)):
        raise ValueError("Invalid confidence")

    conf = max(0.0, min(1.0, float(conf)))
    return flow, conf

@trace_node("intent_classification")
def intent_classification(state: dict) -> Flow:
    user_msg = state.get("user_message", "").lower().strip()
    active_flow = state.get("active_flow")

    if any(k in user_msg for k in EXPLICIT_MENU):
        state["active_flow"] = "menu"
        return "menu"

    if any(k in user_msg for k in EXPLICIT_ORDER):
        state["active_flow"] = "order"
        return "order"

    try:
        flow, conf = llm_classify_intent(user_msg)

        if flow == "other":
            return active_flow or "menu"

        if conf >= CONFIDENCE_THRESHOLD:
            state["active_flow"] = flow
            return flow

    except Exception:
        pass

    if active_flow in ("menu", "order"):
        return active_flow

    state["active_flow"] = "menu"
    return "menu"
