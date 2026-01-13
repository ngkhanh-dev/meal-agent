from typing import TypedDict, Optional, List

class OrderState(TypedDict, total=False):
    user_id: str
    user_message: str

    active_flow: str

    intent: Optional[str]

    kitchen: Optional[dict]
    menu: Optional[list]
    holidays: Optional[list]

    menu_results: Optional[list]

    selected_date: Optional[str]
    selected_items: Optional[List[dict]]

    chatbot_message: Optional[str]

    # order_summary: str
    # menu_message: str
