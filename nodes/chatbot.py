import os
from langchain_google_genai import ChatGoogleGenerativeAI
from tracing import trace_node
import re
import json
from dotenv import load_dotenv
load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)
    return json.loads(raw)

@trace_node("chatbot")
def chatbot(state: dict):
    flow = state["active_flow"]

    missing = []
    if flow == "order":
        if not state.get("selected_date"):
            missing.append("ngày")
        if not state.get("selected_items"):
            missing.append("món")

    context = {
        "flow": flow,
        "user_message": state.get("user_message"),
        "selected_date": state.get("selected_date"),
        "selected_items": state.get("selected_items"),
        "menu_results": state.get("menu_results"),
        "missing": missing
    }

    prompt = f"""
    Bạn là chatbot nhà ăn, nói tiếng Việt tự nhiên, lịch sự.

    === CONTEXT ===
    {context}

    === HƯỚNG DẪN ===
    - flow = menu:
        + Trình bày thực đơn từ menu_results
        + Nếu rỗng, nói rõ không có dữ liệu
    - flow = order:
        + Nếu missing không rỗng → hỏi bổ sung
        + Nếu đủ → xác nhận đơn, đưa ra một câu hỏi xác thực xem khách có đồng ý hay chỉnh sửa gì không
    - KHÔNG đổi flow
    - KHÔNG giải thích nội bộ

    === OUTPUT ===
    Chỉ trả về nội dung nói với người dùng
    """

    state["chatbot_message"] = llm.invoke(prompt).content.strip()
    
    return state
