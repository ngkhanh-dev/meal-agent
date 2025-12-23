# def validate_order(state):
#     summary = (
#         f"Vui lòng xác nhận đơn hàng:\n"
#         f"- Ngày: {state['selected_date']}\n"
#         f"- Món: {', '.join(i['name'] for i in state['selected_items'])}\n\n"
#         "Trả lời 'đồng ý' hoặc 'sửa'"
#     )
#     state["validation_summary"] = summary
#     return state
from tracing import trace_node

@trace_node("validate")
def validate_order(state):
    raw_items = state.get("selected_items")
    date = state.get("selected_date")

    if not raw_items or not date:
        state["need_clarification"] = True
        state["clarification_question"] = (
            "Thông tin đơn hàng chưa đầy đủ, vui lòng chọn lại ngày và món."
        )
        return state

    items = []
    for item in raw_items:
        items.append({
            "menu_id": item.get("menu_id") or item.get("id"),
            "quantity": item.get("quantity", 1)
        })

    result = state["api"].validate_order({
        "date": date,
        "items": items
    })

    state["validation_result"] = result

    if not result["valid"]:
        state["need_clarification"] = True
        state["clarification_question"] = (
            "Đơn hàng chưa hợp lệ:\n- "
            + "\n- ".join(result["errors"])
        )

    return state
