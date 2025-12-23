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
        errors = []

        date = payload.get("date")
        items = payload.get("items", [])

        if not date:
            errors.append("Thiếu ngày đặt")

        for h in self.holidays():
            if h["date"] == date:
                errors.append(f"Ngày {date} là ngày nghỉ: {h['reason']}")

        if not items:
            errors.append("Chưa chọn món")

        menu_ids = {m["menu_id"] for m in self.menus(date)}

        for idx, item in enumerate(items):
            menu_id = item.get("menu_id")
            quantity = item.get("quantity")

            if menu_id not in menu_ids:
                errors.append(f"Món {menu_id} không tồn tại trong menu")

            if not isinstance(quantity, int) or quantity <= 0:
                errors.append(
                    f"Số lượng không hợp lệ cho món {menu_id}"
                )

        if errors:
            return {
                "valid": False,
                "errors": errors
            }

        return {
            "valid": True
        }

    def create_order(self, payload):
        return {"order_id": "ORD-001"}
