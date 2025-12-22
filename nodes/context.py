from services.api_client import MealAPI

def load_context(state):
    api = MealAPI()
    state["kitchen"] = api.default_kitchen()
    state["menu"] = api.menus("today")
    state["holidays"] = api.holidays()
    state["api"] = api
    return state
