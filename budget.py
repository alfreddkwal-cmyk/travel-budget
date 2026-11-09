"""Travel budget model and budget calculations."""


class TravelBudget:
    def __init__(self, name, currency, total_budget):
        if not name.strip():
            raise ValueError("Trip name cannot be empty.")
        if total_budget < 0:
            raise ValueError("Budget cannot be negative.")
        self.name = name
        self.currency = currency.upper()
        self.total_budget = float(total_budget)
        self.expenses = []

    @property
    def total_spent(self):
        return sum(item["amount"] for item in self.expenses)

    @property
    def remaining(self):
        return self.total_budget - self.total_spent

    @property
    def is_over_budget(self):
        return self.total_spent > self.total_budget

    def to_dict(self):
        return {
            "name": self.name,
            "currency": self.currency,
            "total_budget": self.total_budget,
            "expenses": self.expenses,
        }

    @classmethod
    def from_dict(cls, data):
        trip = cls(data["name"], data["currency"], data["total_budget"])
        trip.expenses = list(data.get("expenses", []))
        return trip
