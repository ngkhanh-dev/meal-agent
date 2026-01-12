from state import OrderState
from tracing import trace_node

@trace_node("reset_intent")
def reset_intent(state: OrderState):
    return {
        "intent": None, 
        "selected_date": None,            
        "clarification_question": None,
        "selected_items": [],  
        "order_summary": None,       
    }


