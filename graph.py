from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import OrderState
from nodes.dummy import load_context
from nodes.order_validate import order_validate
from nodes.clarify import ask_clarification
from nodes.menu_agent import menu_agent
# from nodes.intent_classification import intent_classification
from routes import route_after_validate, route_after_clarify, intent_classification


graph = StateGraph(OrderState)
memory = MemorySaver()

graph.add_node("dummy", load_context)
graph.add_node("validate", order_validate)
graph.add_node("menu_node", menu_agent)
graph.add_node("clarify", ask_clarification)
# graph.add_node("intent_classification", intent_classification)

graph.set_entry_point("dummy")


# graph.add_edge("dummy", "validate")

# graph.add_edge("validate", END)
# graph.add_edge("clarify", END)
# graph.add_edge("dummy", "intent_classification")
graph.add_edge("menu_node", END)

graph.add_conditional_edges(
    "dummy",
    intent_classification,
    {
        "menu": "menu_node",
        "order": "validate"
    }
)

graph.add_conditional_edges(
    "validate",
    route_after_validate,
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

