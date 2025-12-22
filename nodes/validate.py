def validate_order(state):
    summary = (
        f"Vui lòng xác nhận đơn hàng:\n"
        f"- Ngày: {state['selected_date']}\n"
        f"- Món: {', '.join(i['name'] for i in state['selected_items'])}\n\n"
        "Trả lời 'đồng ý' hoặc 'sửa'"
    )
    state["validation_summary"] = summary
    return state
