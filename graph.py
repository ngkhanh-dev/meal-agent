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
graph.add_node("menu", menu_agent)
graph.add_node("validate", validate_order)
graph.add_node("order", create_order)

# ===== Entry =====
graph.set_entry_point("context")

# ===== Linear start =====
graph.add_edge("context", "slot")
graph.add_edge("slot", "check")

# ===== Routing sau CHECK =====
def route_after_check(state: OrderState):
    if state["need_clarification"]:
        return "clarify"
    return "menu"

graph.add_conditional_edges(
    "check",
    route_after_check,
    {
        "clarify": "clarify",
        "menu": "menu"
    }
)

# ===== Clarify kết thúc lượt hỏi =====
graph.add_edge("clarify", END)

# ===== Menu agent chỉ refine items, xong QUAY LẠI CHECK =====
graph.add_edge("menu", "check")

# ===== Routing sau VALIDATE =====
# validate_order PHẢI set:
# state["validation_decision"] = "confirm" | "edit"
def route_after_validate(state: OrderState):
    decision = state.get("validation_decision")
    if decision == "edit":
        return "slot"
    if decision == "confirm":
        return "order"
    # fallback an toàn
    return END

graph.add_conditional_edges(
    "validate",
    route_after_validate,
    {
        "slot": "slot",
        "order": "order",
        END: END
    }
)

# ===== Check → Validate =====
# CHỈ KHI ĐÃ ĐỦ SLOT
graph.add_edge("check", "validate")

# ===== Order là điểm cuối =====
graph.add_edge("order", END)

app = graph.compile()
