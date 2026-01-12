#models.py
from pydantic import BaseModel
from typing import Optional

class ChatReq(BaseModel):
    user_id: Optional[str] = None
    message: str

class User(BaseModel):
    username: str
    password: str