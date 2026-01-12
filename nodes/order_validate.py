import datetime
import json
import re
from tracing import trace_node
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

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

@trace_node("order_validate")
def order_validate(state):
    today = datetime.date.today().isoformat()

    prompt = f"""
    Today is {today}
    User message: {state['user_message']}

    Extract order information if exists.
    Convert relative dates like "hôm nay", "ngày mai" to YYYY-MM-DD.

    Output JSON:
    {{
      "date": null | "YYYY-MM-DD",
      "items": [
        {{
          "menu_id": "...",
          "quantity": "..."
        }}
      ]
    }}
    """

    raw = llm.invoke(prompt).content
    data = extract_json(raw)
    
    # Add slot
    if data.get("date"):
        state["selected_date"] = data["date"]

    if data.get("items"):
        state["selected_items"] = data["items"]

    # Check complete
    missing = []
    if not state.get("selected_date"):
        missing.append("ngày")
    if not state.get("selected_items"):
        missing.append("món")

    if missing:
        state["clarification_question"] = (
            f"Bạn chưa chọn {' và '.join(missing)}, vui lòng bổ sung."
        )
        return state

    # Summary
    items_text = []
    for i in state["selected_items"]:
        items_text.append(
            f"- {i.get('menu_id')} x {i.get('quantity', 1)}"
        )

    state["order_summary"] = (
        "Thông tin đơn hàng của bạn:\n"
        f"Ngày: {state['selected_date']}\n"
        "Món:\n"
        + "\n".join(items_text)
    )

    return state
