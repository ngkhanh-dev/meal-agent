from services.api_client import MealAPI
from trace import trace_node

@trace_node("context")
def load_context(state):
    api = MealAPI()
    state["kitchen"] = api.default_kitchen()
    state["menu"] = api.menus("today")
    state["holidays"] = api.holidays()
    state["api"] = api
    return state
