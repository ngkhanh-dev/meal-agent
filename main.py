from fastapi import FastAPI
from graph import app as graph_app
from models import ChatReq, User
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Optional
from langgraph.errors import GraphRecursionError
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from dotenv import load_dotenv
import re
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



api = FastAPI()


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


api.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@api.get("/")
def ui():
    return FileResponse("templates/index.html")

@api.get("/auth")
def authUI():
    return FileResponse("templates/auth.html")

@api.get("/gateway")
def gatewayUI():
    return FileResponse("templates/gateway.html")

@api.post("/chat")
def chat(req: ChatReq):
    try:
        config = {
            "configurable": {"thread_id": "1"},
            "recursion_limit": 5
            }
        state = {
            "user_id": req.user_id,
            # "user_id": "1",
            "user_message": req.message,
            # "need_clarification": False
        }
        result = graph_app.invoke(state, config=config)
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        if result.get("menu_message"):
            return {
                "type": "menu",
                "message": result["menu_message"]
            }

        if result.get("clarification_question"):
            return {
                "type": "clarification",
                "message": result["clarification_question"]
            }

        if result.get("order_summary"):
            return {
                "type": "summary",
                "message": result["order_summary"]
            }

    except GraphRecursionError as e:
        print(f"GraphRecursionError occurred: {e}")
    # print(f"Execution succeeded: {result}")

@api.post("/auth")
def auth(user: User):
    headers = {
    "Content-Type": "application/json"
    }

    response = requests.post(
        f"http://10.255.63.198:8001/api/v1/auth/login-sso",
        headers=headers,
        json={
            "username": user.username,
            "password": user.password
        })
    # print(response.json())

    return response.json()["data"]["payload"]["token"]
    




