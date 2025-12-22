from fastapi import FastAPI
from pydantic import BaseModel
from graph import app as graph_app
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Optional

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

class ChatReq(BaseModel):
    user_id: Optional[str] = None
    message: str

@api.post("/chat")
def chat(req: ChatReq):
    state = {
        "user_id": req.user_id,
        "user_message": req.message,
        "need_clarification": False
    }
    result = graph_app.invoke(state)

    # if result.get("end"):
    #     return {"reply": result["reply"]}

    # return {
    #     "order_id": result["order_result"]["order_id"],
    #     "date": result["selected_date"],
    #     "items": result["selected_items"]
    # }
    # 1. Clarification
    if result.get("need_clarification"):
        return {
            "type": "clarification",
            "message": result.get("clarification_question")
        }

    # 2. Order created
    if "order_result" in result:
        return {
            "type": "order_success",
            "order_id": result["order_result"]["order_id"],
            "order": result["order_result"]
        }

    # 3. Fallback (defensive)
    return {
        "type": "error",
        "message": "Không thể xử lý yêu cầu."
    }
