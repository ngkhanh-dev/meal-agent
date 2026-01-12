import json
from state import OrderState
from langchain_google_genai import ChatGoogleGenerativeAI
import re
import os
from dotenv import load_dotenv
load_dotenv()
from tracing import trace_node

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)
    return json.loads(raw)

@trace_node("order_intent")
def order_intent(state: OrderState):
    user_msg = state.get("user_message", "")
    old_intent = state.get("intent")
    
    if not old_intent:
        old_intent = "NONE"

    prompt = f"""
    Bạn là bộ não điều hướng đơn hàng. 
    Intent hiện tại của hệ thống: {old_intent}
    Tin nhắn mới: "{user_msg}"

    NHIỆM VỤ:
    1. Xác định tin nhắn này là:
       - "NEW": Một yêu cầu mới hoàn toàn (VD: "Tôi muốn hủy đơn" khi đang đặt cơm).
       - "CONTINUE": Cung cấp thông tin bổ sung cho intent {old_intent} (VD: "Ngày mai nhé", "Lấy cho tôi đùi gà").
    2. Nếu là "NEW", hãy phân loại nó (CREATE, READ, DELETE, UPDATE).
    3. Nếu là "CONTINUE", intent mới sẽ giống intent cũ.

    TRẢ VỀ JSON:
    {{
       "type": "NEW" | "CONTINUE",
       "detected_intent": "CREATE" | "READ" | "DELETE" | "UPDATE" | "OTHERS"
    }}
    """
    
    raw = llm.invoke(prompt).content
    response_raw = extract_json(raw)

    try:
        data = json.loads(response_raw)
        msg_type = data.get("type", "CONTINUE")
        detected_intent = data.get("detected_intent", old_intent)
    except:
        msg_type = "CONTINUE"
        detected_intent = old_intent

    intent_changed = False
    if msg_type == "NEW" and old_intent != "NONE" and detected_intent != old_intent:
        intent_changed = True
    
    final_intent = detected_intent if msg_type == "NEW" else old_intent

    return {
        "intent": final_intent,
        "intent_changed": intent_changed
    }