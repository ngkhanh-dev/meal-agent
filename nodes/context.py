from services.api_client import MealAPI
from tracing import trace_node

@trace_node("context")
def load_context(state):
    api = MealAPI()
    state["api"] = api
    state["kitchen"] = api.default_kitchen()
    state["menu"] = api.menus("today")
    state["holidays"] = api.holidays()
    return state
