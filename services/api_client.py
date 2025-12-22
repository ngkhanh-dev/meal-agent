class MealAPI:
    def kitchens(self):
        return [{"id": "K1", "name": "Bếp A"}]

    def default_kitchen(self):
        return {"id": "K1", "name": "Bếp A"}

    def menus(self, date: str):
        return [
            {"menu_id": "M1", "name": "Cơm gà"},
            {"menu_id": "M2", "name": "Cơm cá"}
        ]

    def holidays(self):
        return [{"date": "2025-12-20", "reason": "Nghỉ lễ"}]

    def validate_order(self, payload):
        return {"valid": True}

    def create_order(self, payload):
        return {"order_id": "ORD-001"}
