# def ask_clarification(state):
#     return {
#         "reply": state["clarification_question"],
#         "end": True
#     }

def ask_clarification(state):
    # Chỉ trả về câu hỏi, frontend sẽ gửi lại user_message
    return state
