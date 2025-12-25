from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import OrderState
from nodes.dummy import load_context
from nodes.order_validate import order_validate
from nodes.clarify import ask_clarification
from routes import route_after_understand, route_after_clarify


graph = StateGraph(OrderState)
memory = MemorySaver()

graph.add_node("dummy", load_context)
graph.add_node("validate", order_validate)
graph.add_node("clarify", ask_clarification)

graph.set_entry_point("dummy")

graph.add_edge("dummy", "validate")

graph.add_conditional_edges(
    "understand",
    route_after_understand,
    {
        "clarify": "clarify",
        END: END,
    },
)

graph.add_conditional_edges(
    "clarify",
    route_after_clarify,
    {
        "validate": "validate",
        END: END,
    },
)

app = graph.compile(checkpointer=memory)
