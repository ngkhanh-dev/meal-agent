# def validate_order(state):
#     summary = (
#         f"Vui lòng xác nhận đơn hàng:\n"
#         f"- Ngày: {state['selected_date']}\n"
#         f"- Món: {', '.join(i['name'] for i in state['selected_items'])}\n\n"
#         "Trả lời 'đồng ý' hoặc 'sửa'"
#     )
#     state["validation_summary"] = summary
#     return state
from trace import trace_node

@trace_node("validate")
def validate_order(state):
    items = state.get("selected_items")
    date = state.get("selected_date")

    if not items or not date:
        state["need_clarification"] = True
        state["clarification_question"] = (
            "Thông tin đơn hàng chưa đầy đủ, vui lòng chọn lại ngày và món."
        )
        return state

    result = state["api"].validate_order({
        "date": date,
        "items": items
    })

    state["validation_result"] = result
    return state

