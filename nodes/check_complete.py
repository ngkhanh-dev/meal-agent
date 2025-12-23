from tracing import trace_node

@trace_node("check_complete")
def check_complete(state):
    missing = []

    if not state.get("selected_date"):
        missing.append("ngày")
    if not state.get("selected_items"):
        missing.append("món")

    if missing:
        state["need_clarification"] = True
        state["clarification_question"] = (
            f"Bạn chưa chọn {' và '.join(missing)}, vui lòng bổ sung."
        )
    else:
        state["need_clarification"] = False

    return state
