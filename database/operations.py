from database.database import get_connection
from datetime import date


# 1. Add a new expense
def add_expense(amount: int, category: str,
                description: str = "",
                expense_date: str = None):

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if not category.strip():
        raise ValueError("Category cannot be empty.")

    if expense_date is None:
        expense_date = date.today().isoformat()

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO expenses
            (amount, category, description, expense_date)
            VALUES (?, ?, ?, ?)
        """, (amount, category, description, expense_date))

        conn.commit()

        return {
            "success": True,
            "expense_id": cursor.lastrowid,
            "message": "Expense added successfully!"
        }

    finally:
        conn.close()


# 2. Retrieve all expenses
def get_all_expenses():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM expenses
            ORDER BY expense_date DESC, id DESC
        """)

        expenses = cursor.fetchall()

        return [dict(expense) for expense in expenses]

    finally:
        conn.close()


# 3. Retrieve expense by ID
def get_expense_by_id(expense_id: int):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM expenses
            WHERE id = ?
        """, (expense_id,))

        expense = cursor.fetchone()

        if expense is None:
            return None

        return dict(expense)

    finally:
        conn.close()