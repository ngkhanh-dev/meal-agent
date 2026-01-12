from langgraph.graph import END
from state import OrderState

def route_after_validate(state: OrderState):
    # if state.get("clarification_question"):
    #     return END

    # if state.get("order_summary"):
    #     return "clarify"

    return END


def route_after_clarify(state: OrderState):
    decision = state.get("confirmation")

    if decision == "chỉnh sửa":
        return "understand"

    if decision == "đồng ý":
        return END

    return END

from typing import Literal

def intent_classification(state: dict):
    active_flow = state.get("active_flow")
    return active_flow


# from langgraph.graph import END

# def router_after_order(state: OrderState):
#     if state.get("intent_changed"):
#         return "reset_intent"
    
#     intent = state.get("intent")
#     if intent == "CREATE":
#         return "create_order"
#     elif intent == "DELETE":
#         return "delete_order"
#     elif intent == "READ":
#         return "read_order"
#     else:
#         return END
