# routes.py
from langgraph.graph import END
from state import OrderState


def route_after_understand(state: OrderState):

    if state.get("clarification_question"):
        return END

    if state.get("order_summary"):
        return "clarify"

    return END


def route_after_clarify(state: OrderState):

    decision = state.get("confirmation")

    if decision == "edit":
        return "understand"

    if decision == "yes":
        return END

    return END
