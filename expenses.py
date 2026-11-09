"""Expense entry and reporting functions."""
from datetime import date

VALID_CATEGORIES = {
    "transport", "accommodation", "food", "activities", "other"
}


def add_expense(trip, category, description, amount, expense_date=None):
    category = category.strip().lower()
    if category not in VALID_CATEGORIES:
        raise ValueError(f"Category must be one of: {', '.join(sorted(VALID_CATEGORIES))}")
    if not description.strip():
        raise ValueError("Expense description cannot be empty.")
    if amount < 0:
        raise ValueError("Expense amount cannot be negative.")
    trip.expenses.append({
        "category": category,
        "description": description.strip(),
        "amount": float(amount),
        "date": expense_date or date.today().isoformat(),
    })


def expense_summary(trip):
    by_category = {}
    for item in trip.expenses:
        by_category[item["category"]] = (
            by_category.get(item["category"], 0.0) + item["amount"]
        )
    spent = trip.total_spent
    return {
        "spent": spent,
        "remaining": trip.total_budget - spent,
        "status": "Over budget" if spent > trip.total_budget else "Within budget",
        "by_category": by_category,
    }
