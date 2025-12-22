# def ask_clarification(state):
#     return {
#         "reply": state["clarification_question"],
#         "end": True
#     }
from trace import trace_node

@trace_node("clarify")
def ask_clarification(state):
    # Chỉ trả về câu hỏi, frontend sẽ gửi lại user_message
    return state
