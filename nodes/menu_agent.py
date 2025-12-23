import json
# from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import json
import re
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

def extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw)
    raw = re.sub(r"```$", "", raw)
    
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from LLM:\n{raw}") from e

@trace_node("menu_agent")
def menu_agent(state):
    prompt = f"""
    User request: {state['user_message']}
    Menu: {state['menu']}

    Return JSON:
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

    state["selected_items"] = data["items"]
    return state
