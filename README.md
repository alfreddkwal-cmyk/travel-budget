# Currency & Travel Budget Planner

A Python application that helps a traveller convert currencies, plan a trip budget, record expenses, save/load trip information, and get AI-powered travel advice via Google Gemini.

## Features
- Currency conversion using editable sample offline rates.
- Create a trip budget in a supported currency.
- Record expenses under transport, accommodation, food, activities, or other.
- View total spending, remaining funds, and category totals.
- Save and load trips as JSON files.
- **AI Assistant** (optional) – powered by Google Gemini. Ask for budget tips, day plans, expense ideas, etc. The assistant receives the current trip context automatically.

## Requirements
- Python 3.8 or later
- Core app: no third-party packages
- AI Assistant (optional): `pip install google-genai`

## Run the graphical application
From the project folder:

```bash
python gui.py
```

The GUI uses Tkinter, included with most standard Python installations. On some Linux systems, install the `python3-tk` package if Tkinter is missing.

### Enabling the AI Assistant (Gemini)
1. Install the official Google Gen AI SDK:
   ```bash
   pip install google-genai
   ```
2. Obtain a free API key from [Google AI Studio](https://aistudio.google.com/apikey).
3. Set the key in your environment:
   ```bash
   export GEMINI_API_KEY=your_key_here
   # (Windows PowerShell:  $env:GEMINI_API_KEY="your_key_here")
   ```
4. Restart the application. Open the **AI Assistant** tab and ask questions.  
   The assistant automatically sees the currently loaded trip (budget, remaining funds, recent expenses).

Quick prompts are provided for common requests (budget tips, day plan, expense ideas).

## Run the command-line version (optional)

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Important note about exchange rates
The application currently uses sample rates stored in `currency_converter.py`. They are included for demonstration and must not be treated as live exchange rates. Update the dictionary with verified rates before using the converter for an actual trip.

## Suggested team responsibilities

| Member | Main contribution | Files |
|---|---|---|
| 1 | GUI and application integration | `gui.py`, `main.py` |
| 2 | Currency conversion logic | `currency_converter.py`, `tests/test_currency_converter.py` |
| 3 | Budget model and calculations | `budget.py` |
| 4 | Expense recording and reports | `expenses.py`, `tests/test_budget_expenses.py` |
| 5 | JSON saving/loading | `storage.py`, `tests/test_storage.py` |
| (extra) | Gemini AI assistant | `ai_assistant.py` |

Each member should make their own changes, commit them from their own GitHub account, and open a pull request. Do not share one account or have one person make all commits on behalf of the group.

## Recommended GitHub contribution workflow

1. One member creates the repository and adds the starter files.
2. Add all five members as repository collaborators.
3. Each member creates a branch for their assigned task, for example `feature/currency-converter`.
4. The assigned member edits and tests their own module.
5. They commit and push using their own GitHub account.
6. They open a pull request and another member reviews it.
7. Merge the pull request into `main` after review.

Example commands:

```bash
git checkout -b feature/currency-converter
git add currency_converter.py tests/test_currency_converter.py
git commit -m "Add currency conversion module and tests"
git push -u origin feature/currency-converter
```

Use meaningful commits that show real work. Each member should personally understand and be able to explain their contribution during grading.

## Suggested project demonstration
1. Convert 100 USD to NGN.
2. Create a trip with a budget.
3. Add transport, accommodation, and food expenses.
4. Display the summary and remaining balance.
5. Save the trip, exit, and load it again.
6. Run the unit tests.
