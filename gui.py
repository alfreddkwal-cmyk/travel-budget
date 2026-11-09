"""Tkinter GUI for the Currency & Travel Budget Planner. Run: python gui.py"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from budget import TravelBudget
from currency_converter import convert_currency, SUPPORTED_CURRENCIES
from expenses import add_expense, expense_summary, VALID_CATEGORIES
from storage import save_trip, load_trip
from ai_assistant import get_assistant


class TravelBudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency & Travel Budget Planner")
        self.geometry("920x680")
        self.minsize(760, 560)
        self.trip = None
        self._assistant = get_assistant()
        self._style()
        self._header()
        self._tabs()
        self.refresh()

    def _style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("Title.TLabel", font=("Segoe UI", 19, "bold"))
        style.configure("Metric.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("Treeview", rowheight=27)
        style.configure("TButton", padding=7)

    def _header(self):
        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="x")
        ttk.Label(frame, text="✈ Currency & Travel Budget Planner", style="Title.TLabel").pack(anchor="w")
        ttk.Label(frame, text="Convert money, plan your trip and track expenses.").pack(anchor="w", pady=(5, 0))
        ttk.Separator(self).pack(fill="x")

    def _tabs(self):
        book = ttk.Notebook(self)
        book.pack(fill="both", expand=True, padx=16, pady=14)
        self.converter = ttk.Frame(book, padding=20)
        self.trip_page = ttk.Frame(book, padding=20)
        self.expense_page = ttk.Frame(book, padding=20)
        self.summary_page = ttk.Frame(book, padding=20)
        self.ai_page = ttk.Frame(book, padding=16)
        for page, label in [
            (self.converter, "Currency Converter"),
            (self.trip_page, "Travel Budget"),
            (self.expense_page, "Expenses"),
            (self.summary_page, "Summary"),
            (self.ai_page, "AI Assistant"),
        ]:
            book.add(page, text=label)
        self._converter_ui()
        self._trip_ui()
        self._expense_ui()
        self._summary_ui()
        self._ai_ui()
        footer = ttk.Frame(self, padding=(16, 0, 16, 10))
        footer.pack(fill="x")
        ttk.Button(footer, text="Load Trip", command=self.load_trip).pack(side="left")
        ttk.Button(footer, text="Save Trip", command=self.save_trip).pack(side="left", padx=8)
        ttk.Label(footer, text="Sample offline exchange rates", foreground="#8a5a00").pack(side="right")

    def _converter_ui(self):
        ttk.Label(self.converter, text="Currency converter", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))
        form = ttk.Frame(self.converter); form.pack(anchor="w")
        self.amount = tk.StringVar(value="1")
        self.source = tk.StringVar(value="USD")
        self.target = tk.StringVar(value="NGN")
        ttk.Label(form, text="Amount").grid(row=0, column=0, sticky="w", padx=(0, 14), pady=8)
        ttk.Entry(form, textvariable=self.amount, width=25).grid(row=0, column=1)
        ttk.Label(form, text="From").grid(row=1, column=0, sticky="w", padx=(0, 14), pady=8)
        ttk.Combobox(form, textvariable=self.source, values=SUPPORTED_CURRENCIES, state="readonly", width=22).grid(row=1, column=1)
        ttk.Label(form, text="To").grid(row=2, column=0, sticky="w", padx=(0, 14), pady=8)
        ttk.Combobox(form, textvariable=self.target, values=SUPPORTED_CURRENCIES, state="readonly", width=22).grid(row=2, column=1)
        ttk.Button(form, text="Convert", command=self.convert).grid(row=3, column=1, sticky="w", pady=14)
        self.conversion_result = ttk.Label(self.converter, text="Enter an amount and select currencies.", font=("Segoe UI", 13, "bold"))
        self.conversion_result.pack(anchor="w", pady=18)
        ttk.Label(self.converter, text="Exchange rates are examples for demonstration, not live market rates.", wraplength=700).pack(anchor="w")

    def _trip_ui(self):
        ttk.Label(self.trip_page, text="Create a travel budget", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))
        form = ttk.Frame(self.trip_page); form.pack(anchor="w")
        self.trip_name = tk.StringVar(); self.trip_currency = tk.StringVar(value="NGN"); self.trip_amount = tk.StringVar()
        ttk.Label(form, text="Trip name").grid(row=0, column=0, sticky="w", padx=(0, 14), pady=9)
        ttk.Entry(form, textvariable=self.trip_name, width=30).grid(row=0, column=1)
        ttk.Label(form, text="Currency").grid(row=1, column=0, sticky="w", padx=(0, 14), pady=9)
        ttk.Combobox(form, textvariable=self.trip_currency, values=SUPPORTED_CURRENCIES, state="readonly", width=27).grid(row=1, column=1)
        ttk.Label(form, text="Total budget").grid(row=2, column=0, sticky="w", padx=(0, 14), pady=9)
        ttk.Entry(form, textvariable=self.trip_amount, width=30).grid(row=2, column=1)
        ttk.Button(form, text="Create Trip Budget", command=self.create_trip).grid(row=3, column=1, sticky="w", pady=14)
        self.trip_status = ttk.Label(self.trip_page, text="No trip created yet."); self.trip_status.pack(anchor="w", pady=16)

    def _expense_ui(self):
        ttk.Label(self.expense_page, text="Add a travel expense", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 14))
        form = ttk.Frame(self.expense_page); form.pack(anchor="w")
        self.category = tk.StringVar(value="food"); self.description = tk.StringVar(); self.expense_amount = tk.StringVar()
        fields = [("Category", ttk.Combobox(form, textvariable=self.category, values=sorted(VALID_CATEGORIES), state="readonly", width=27)),
                  ("Description", ttk.Entry(form, textvariable=self.description, width=30)),
                  ("Amount", ttk.Entry(form, textvariable=self.expense_amount, width=30))]
        for row, (label, widget) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", padx=(0, 14), pady=9)
            widget.grid(row=row, column=1, sticky="w")
        ttk.Button(form, text="Add Expense", command=self.add_expense).grid(row=3, column=1, sticky="w", pady=14)
        self.expense_hint = ttk.Label(self.expense_page, text="Create or load a trip before adding expenses.")
        self.expense_hint.pack(anchor="w", pady=10)

    def _summary_ui(self):
        ttk.Label(self.summary_page, text="Budget summary", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 12))
        self.budget_text = tk.StringVar(value="Budget: —"); self.spent_text = tk.StringVar(value="Spent: —"); self.remaining_text = tk.StringVar(value="Remaining: —")
        for var in (self.budget_text, self.spent_text, self.remaining_text):
            ttk.Label(self.summary_page, textvariable=var, style="Metric.TLabel").pack(anchor="w", pady=5)
        self.status_text = ttk.Label(self.summary_page, text="Create or load a trip to see its summary.")
        self.status_text.pack(anchor="w", pady=8)
        ttk.Label(self.summary_page, text="Spending by category", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(12, 5))
        self.category_table = ttk.Treeview(self.summary_page, columns=("category", "total"), show="headings", height=8)
        self.category_table.heading("category", text="Category"); self.category_table.heading("total", text="Total")
        self.category_table.column("category", width=220); self.category_table.column("total", width=220, anchor="e")
        self.category_table.pack(fill="x")

    def _ai_ui(self):
        """AI Assistant tab powered by Google Gemini."""
        header = ttk.Frame(self.ai_page)
        header.pack(fill="x", pady=(0, 8))
        ttk.Label(header, text="AI Travel Assistant (Gemini)", font=("Segoe UI", 16, "bold")).pack(side="left")
        self.ai_status = ttk.Label(header, text=self._assistant.status_message, foreground="#555")
        self.ai_status.pack(side="right")

        # Chat history
        self.ai_chat = scrolledtext.ScrolledText(
            self.ai_page, wrap=tk.WORD, height=18, font=("Segoe UI", 10), state="disabled"
        )
        self.ai_chat.pack(fill="both", expand=True, pady=(4, 8))
        self.ai_chat.tag_configure("user", foreground="#0b5cad", font=("Segoe UI", 10, "bold"))
        self.ai_chat.tag_configure("assistant", foreground="#1a1a1a")
        self.ai_chat.tag_configure("system", foreground="#8a5a00", font=("Segoe UI", 9, "italic"))

        # Input row
        input_row = ttk.Frame(self.ai_page)
        input_row.pack(fill="x")
        self.ai_prompt = tk.StringVar()
        entry = ttk.Entry(input_row, textvariable=self.ai_prompt, font=("Segoe UI", 11))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        entry.bind("<Return>", lambda _e: self.ask_ai())
        ttk.Button(input_row, text="Ask Gemini", command=self.ask_ai).pack(side="left")
        ttk.Button(input_row, text="Clear", command=self._clear_ai_chat).pack(side="left", padx=(6, 0))

        # Quick suggestion buttons
        tips = ttk.Frame(self.ai_page)
        tips.pack(fill="x", pady=(10, 0))
        ttk.Label(tips, text="Quick prompts:", font=("Segoe UI", 9)).pack(side="left", padx=(0, 6))
        for label, prompt in [
            ("Budget tips", "Give me 5 practical tips to stay within my current trip budget."),
            ("Suggest day plan", "Suggest a realistic one-day itinerary that fits my remaining budget."),
            ("Expense ideas", "Suggest typical expenses I should expect for this trip by category."),
        ]:
            ttk.Button(
                tips, text=label,
                command=lambda p=prompt: (self.ai_prompt.set(p), self.ask_ai())
            ).pack(side="left", padx=3)

        # Initial system message
        self._append_ai("system", self._assistant.status_message)
        if not self._assistant.is_ready:
            self._append_ai(
                "system",
                "To enable the AI assistant:\n"
                "1. pip install google-genai\n"
                "2. export GEMINI_API_KEY=your_key_here\n"
                "3. Restart the application."
            )

    def convert(self):
        try:
            value = convert_currency(float(self.amount.get()), self.source.get(), self.target.get())
            self.conversion_result.config(text=f"{float(self.amount.get()):,.2f} {self.source.get()} = {value:,.2f} {self.target.get()}")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Conversion error", str(error))

    # ── AI Assistant helpers ──────────────────────────────────────────────
    def _append_ai(self, role: str, text: str):
        self.ai_chat.configure(state="normal")
        if role == "user":
            self.ai_chat.insert(tk.END, "You: ", "user")
            self.ai_chat.insert(tk.END, text.strip() + "\n\n", "assistant")
        elif role == "assistant":
            self.ai_chat.insert(tk.END, "Gemini: ", "user")
            self.ai_chat.insert(tk.END, text.strip() + "\n\n", "assistant")
        else:
            self.ai_chat.insert(tk.END, text.strip() + "\n\n", "system")
        self.ai_chat.see(tk.END)
        self.ai_chat.configure(state="disabled")

    def _clear_ai_chat(self):
        self.ai_chat.configure(state="normal")
        self.ai_chat.delete("1.0", tk.END)
        self.ai_chat.configure(state="disabled")
        self._append_ai("system", self._assistant.status_message)

    def ask_ai(self):
        prompt = self.ai_prompt.get().strip()
        if not prompt:
            return
        self.ai_prompt.set("")
        self._append_ai("user", prompt)
        self.ai_status.config(text="Thinking…")
        self.update_idletasks()
        reply = self._assistant.ask(prompt, trip=self.trip)
        self._append_ai("assistant", reply)
        self.ai_status.config(text=self._assistant.status_message)

    def create_trip(self):
        try:
            self.trip = TravelBudget(self.trip_name.get().strip(), self.trip_currency.get(), float(self.trip_amount.get()))
            self.refresh()
            messagebox.showinfo("Trip created", "Your travel budget has been created.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid trip", str(error))

    def add_expense(self):
        if self.trip is None:
            messagebox.showwarning("No trip", "Create or load a trip first."); return
        try:
            add_expense(self.trip, self.category.get(), self.description.get(), float(self.expense_amount.get()))
            self.description.set(""); self.expense_amount.set(""); self.refresh()
            messagebox.showinfo("Expense added", "Expense recorded successfully.")
        except (ValueError, TypeError) as error:
            messagebox.showerror("Invalid expense", str(error))

    def refresh(self):
        if self.trip is None:
            self.trip_status.config(text="No trip created yet.")
            self.expense_hint.config(text="Create or load a trip before adding expenses.")
            self.budget_text.set("Budget: —"); self.spent_text.set("Spent: —"); self.remaining_text.set("Remaining: —")
            self.status_text.config(text="Create or load a trip to see its summary.")
            for row in self.category_table.get_children(): self.category_table.delete(row)
            return
        report = expense_summary(self.trip); cur = self.trip.currency
        self.trip_status.config(text=f"Current trip: {self.trip.name} | Budget: {self.trip.total_budget:,.2f} {cur}")
        self.expense_hint.config(text=f"Expenses are recorded in {cur}.")
        self.budget_text.set(f"Budget: {self.trip.total_budget:,.2f} {cur}")
        self.spent_text.set(f"Spent: {report['spent']:,.2f} {cur}")
        self.remaining_text.set(f"Remaining: {report['remaining']:,.2f} {cur}")
        self.status_text.config(text=f"Status: {report['status']}")
        for row in self.category_table.get_children(): self.category_table.delete(row)
        for category, total in sorted(report["by_category"].items()):
            self.category_table.insert("", "end", values=(category.title(), f"{total:,.2f} {cur}"))

    def save_trip(self):
        if self.trip is None:
            messagebox.showwarning("No trip", "Create or load a trip before saving."); return
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                save_trip(self.trip, filename); messagebox.showinfo("Saved", f"Trip saved to:\n{filename}")
            except OSError as error: messagebox.showerror("Save error", str(error))

    def load_trip(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            try:
                self.trip = load_trip(filename); self.refresh()
                messagebox.showinfo("Loaded", f"Loaded trip: {self.trip.name}")
            except (OSError, ValueError, KeyError) as error: messagebox.showerror("Load error", str(error))


if __name__ == "__main__":
    TravelBudgetApp().mainloop()
