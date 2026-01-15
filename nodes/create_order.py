from tracing import trace_node

@trace_node("create_order")
def create_order(state):
    state["order_result"] = state["api"].create_order({
        "date": state["selected_date"],
        "items": state["selected_items"]
    })
    return state

