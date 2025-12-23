import json
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
import re
from tracing import trace_node
import datetime
from dotenv import load_dotenv
load_dotenv()

# llm = (model="gpt-4o-mini", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=os.getenv("GEMINI_API_KEY")
)

def extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM:\n{raw}") from e

@trace_node("slot_detect")
def slot_detect(state):
    today = datetime.date.today().isoformat()
    msg = state["user_message"].lower()

    if msg in ["đồng ý", "ok", "xác nhận"]:
        state["confirmation"] = "yes"
        return state

    if msg in ["sửa", "chỉnh", "thay đổi"]:
        state["confirmation"] = "edit"
        return state
    
    prompt = f"""
    Today is {today}
    User message: {state['user_message']}

    Extract info if exists.
    If the user mentions relative time like "hôm nay", "ngày mai",
    convert it to YYYY-MM-DD.
    Output JSON:
    {{
      "date": "{state['selected_date']}",
      "items": [{{
        "menu_id": "...",
        "quantity": "..."
      }}]
    }}
    
    """
    raw = llm.invoke(prompt).content
    print("RAW LLM OUTPUT:", repr(raw))
    # data = json.loads(raw)
    data = extract_json(raw)

    state["selected_date"] = data["date"]
    state["selected_items"] = (
        data["items"]
        if data["menu_name"] else None
    )
    return state
