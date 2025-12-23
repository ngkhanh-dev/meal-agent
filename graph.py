from langgraph.graph import StateGraph, END
from state import OrderState

from nodes.context import load_context
from nodes.slot_detect import slot_detect
from nodes.check_complete import check_complete
from nodes.clarify import ask_clarification
from nodes.menu_agent import menu_agent
from nodes.validate import validate_order
from nodes.create_order import create_order


graph = StateGraph(OrderState)

# ===== Nodes =====
graph.add_node("context", load_context)
graph.add_node("slot", slot_detect)
graph.add_node("check", check_complete)
graph.add_node("clarify", ask_clarification)
graph.add_node("menuu", menu_agent)
graph.add_node("validate", validate_order)
graph.add_node("order", create_order)

# ===== Entry =====
graph.set_entry_point("context")

# ===== Linear start =====
graph.add_edge("context", "slot")
graph.add_edge("slot", "check")

# ===== Routing sau CHECK =====
def route_after_check(state: OrderState):
    decision = "clarify" if state.get("need_clarification") else "validate"
    print(f"[ROUTE] check → {decision}")
    return decision

graph.add_conditional_edges(
    "check",
    route_after_check,
    {
        "clarify": "clarify",
        "validate": "validate",
    },
)

# ===== Clarify flow =====
# clarify chỉ hỏi → user trả lời → slot detect lại
graph.add_edge("clarify", "slot")


# ===== Routing  VALIDATE =====
def route_after_validate(state: OrderState):
    decision = "order" if state.get("confirmation") else "slot"
    print(f"[ROUTE] validate → {decision}")
    return decision

graph.add_conditional_edges(
    "validate",
    route_after_validate,
    {
        "order": "order",
        "slot": "slot",
    },
)

# ===== Order là điểm cuối =====
graph.add_edge("order", END)

app = graph.compile()
