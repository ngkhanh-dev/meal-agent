from tracing import trace_node
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from tracing import trace_node
load_dotenv()


# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0, 
    api_key=os.getenv("GEMINI_API_KEY")
)

@trace_node("clarify")
def ask_clarification(state):
    msg = state.get("user_message", "").lower().strip()

    CONFIRM_PROMPT = """
    Bạn là bộ phân loại ý định xác nhận đơn hàng.

    Nhiệm vụ:
    - Đọc câu trả lời của người dùng.
    - Chỉ được trả về MỘT trong ba nhãn sau (viết thường, không dấu câu, không giải thích):
    - "đồng ý"
    - "chỉnh sửa"
    - "khác"

    Quy tắc:
    - Nếu người dùng thể hiện ý xác nhận, đồng thuận, ok, được, yes, đồng ý, chuẩn rồi → "đồng ý"
    - Nếu người dùng muốn thay đổi, sửa, chỉnh sửa, đổi món, thêm bớt → "chỉnh sửa"
    - Mọi trường hợp còn lại → "khác"

    Câu trả lời người dùng:
    "{user_message}"
    """

    prompt = CONFIRM_PROMPT.format(user_message=msg)

    resp = llm.invoke(prompt)
    
    if resp in ["đồng ý"]:
        state["confirmation"] = "yes"
        return state

    if resp in ["chỉnh sửa"]:
        state["confirmation"] = "edit"
        return state
    
    state["clarification_question"] = (
        "Vui lòng trả lời 'đồng ý' để xác nhận hoặc 'sửa' để chỉnh sửa đơn hàng."
    )

    return state