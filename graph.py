from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from state import OrderState
from nodes.dummy import load_context
from nodes.order_validate import order_validate
from nodes.clarify import ask_clarification
from nodes.menu_agent import menu_agent
from nodes.chatbot import chatbot
from nodes.reset_intent import reset_intent
# from nodes.intent_classification import intent_classification
from routes import route_after_validate, route_after_clarify, route_after_flow


graph = StateGraph(OrderState)
memory = MemorySaver()

graph.add_node("dummy", load_context)
graph.add_node("validate", order_validate)
graph.add_node("menu_node", menu_agent)
graph.add_node("clarify", ask_clarification)
graph.add_node("chatbot", chatbot)
# graph.add_node("intent_classification", intent_classification)
graph.add_node("reset_intent", reset_intent)

graph.set_entry_point("dummy")


# graph.add_edge("dummy", "validate")

# graph.add_edge("dummy", "intent_classification")
graph.add_edge("reset_intent", "dummy")
graph.add_edge("menu_node", "chatbot")
graph.add_edge("validate", "chatbot")
graph.add_edge("clarify", "chatbot")
graph.add_edge("chatbot", END)

graph.add_conditional_edges(
    "dummy",
    route_after_flow,
    {
        "reset": "reset_intent",
        "order": "validate",
        "menu": "menu_node"
    }
)


# graph.add_conditional_edges(
#     "validate",
#     route_after_validate,
#     {
#         "clarify": "clarify",
#         "chatbot": "chatbot",
#     },
# )

# graph.add_conditional_edges(
#     "clarify",
#     route_after_clarify,
#     {
#         "validate": "validate",
#         "chatbot": "chatbot",
#     },
# )

app = graph.compile(checkpointer=memory)

