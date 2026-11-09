"""Command-line entry point for the Currency & Travel Budget Planner."""
from budget import TravelBudget
from currency_converter import convert_currency, SUPPORTED_CURRENCIES
from expenses import add_expense, expense_summary
from storage import save_trip, load_trip
from ai_assistant import get_assistant


def ask_amount(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid non-negative number.")


def main():
    print("\n=== Currency & Travel Budget Planner ===")
    trip = None
    assistant = get_assistant()
    while True:
        print("\n1. Convert currency")
        print("2. Create a travel budget")
        print("3. Add an expense")
        print("4. View budget summary")
        print("5. Save trip")
        print("6. Load trip")
        print("7. Ask AI assistant (Gemini)")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("Supported currencies:", ", ".join(SUPPORTED_CURRENCIES))
            source = input("From currency: ").strip().upper()
            target = input("To currency: ").strip().upper()
            amount = ask_amount("Amount: ")
            try:
                result = convert_currency(amount, source, target)
                print(f"{amount:.2f} {source} = {result:.2f} {target}")
                print("Note: rates are sample offline rates; update them before real travel.")
            except ValueError as error:
                print(error)

        elif choice == "2":
            name = input("Trip name: ").strip() or "My Trip"
            currency = input("Budget currency (e.g. NGN, USD, EUR): ").strip().upper()
            if currency not in SUPPORTED_CURRENCIES:
                print("Unsupported currency.")
                continue
            amount = ask_amount("Total planned budget: ")
            trip = TravelBudget(name, currency, amount)
            print(f"Created '{name}' with a budget of {amount:.2f} {currency}.")

        elif choice == "3":
            if trip is None:
                print("Create or load a trip first.")
                continue
            category = input("Category (transport/accommodation/food/activities/other): ").strip()
            description = input("Description: ").strip()
            amount = ask_amount(f"Amount in {trip.currency}: ")
            add_expense(trip, category, description, amount)
            print("Expense added.")

        elif choice == "4":
            if trip is None:
                print("Create or load a trip first.")
                continue
            summary = expense_summary(trip)
            print(f"\nTrip: {trip.name}")
            print(f"Budget:   {trip.total_budget:.2f} {trip.currency}")
            print(f"Spent:    {summary['spent']:.2f} {trip.currency}")
            print(f"Remaining:{summary['remaining']:.2f} {trip.currency}")
            print(f"Status:   {summary['status']}")
            print("By category:")
            for category, total in summary["by_category"].items():
                print(f"  {category}: {total:.2f} {trip.currency}")

        elif choice == "5":
            if trip is None:
                print("Create or load a trip first.")
                continue
            filename = input("Filename [trip.json]: ").strip() or "trip.json"
            save_trip(trip, filename)
            print(f"Trip saved to {filename}.")

        elif choice == "6":
            filename = input("Filename [trip.json]: ").strip() or "trip.json"
            try:
                trip = load_trip(filename)
                print(f"Loaded trip: {trip.name}")
            except (OSError, ValueError, KeyError) as error:
                print(f"Could not load trip: {error}")

        elif choice == "7":
            print(f"\nAI status: {assistant.status_message}")
            if not assistant.is_ready:
                print("Set GEMINI_API_KEY and install google-genai to enable this feature.")
                continue
            question = input("Your question for the AI: ").strip()
            if question:
                print("\nGemini is thinking…")
                reply = assistant.ask(question, trip=trip)
                print("\n--- Gemini reply ---")
                print(reply)
                print("--------------------")

        elif choice == "0":
            print("Safe travels!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
