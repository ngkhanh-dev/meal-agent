from typing import Literal

Flow = Literal["menu", "order"]

EXPLICIT_MENU = [
    "menu", "thực đơn", "xem menu", "xem thực đơn"
]

EXPLICIT_ORDER = [
    "đặt", "order", "mua", "cho tôi", "thêm", "bớt", "xác nhận đơn"
]


def intent_classification(state: dict) -> Flow:
    """
    Session-level intent routing.
    Quyết định FLOW hiện tại của hội thoại.
    """

    user_msg = state.get("user_message", "").lower().strip()
    active_flow = state.get("active_flow")

    if any(k in user_msg for k in EXPLICIT_MENU):
        state["active_flow"] = "menu"
        return "menu"

    if any(k in user_msg for k in EXPLICIT_ORDER):
        state["active_flow"] = "order"
        return "order"

    if active_flow in ("menu", "order"):
        return active_flow

    state["active_flow"] = "menu"
    return "menu"
