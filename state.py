from typing import TypedDict, Optional, List

class OrderState(TypedDict, total=False):
    user_id: str
    user_message: str

    kitchen: Optional[dict]
    menu: Optional[list]
    holidays: Optional[list]

    selected_date: Optional[str]
    selected_items: Optional[List[dict]]

    need_clarification: bool
    clarification_question: Optional[str]


    validation_summary: str
    confirmation: str
    
    order_result: Optional[dict]
