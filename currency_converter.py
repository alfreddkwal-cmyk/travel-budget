"""Currency conversion using editable sample offline rates.

Rates represent the value of one unit of each currency in NGN.
These are demonstration values, not live market quotes.
"""

RATES_TO_NGN = {
    "NGN": 1.0,
    "USD": 1500.0,
    "EUR": 1630.0,
    "GBP": 1900.0,
    "CAD": 1100.0,
    "GHS": 100.0,
    "KES": 11.5,
}
SUPPORTED_CURRENCIES = tuple(RATES_TO_NGN)


def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one supported currency to another."""
    if not isinstance(amount, (int, float)) or amount < 0:
        raise ValueError("Amount must be a non-negative number.")
    source = from_currency.upper()
    target = to_currency.upper()
    if source not in RATES_TO_NGN or target not in RATES_TO_NGN:
        raise ValueError("Unsupported currency. Check the supported currency list.")
    amount_in_ngn = amount * RATES_TO_NGN[source]
    return amount_in_ngn / RATES_TO_NGN[target]
