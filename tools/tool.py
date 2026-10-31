from decimal import Decimal
from fastmcp import FastMCP

from database.operations import (
    add_expense,
    get_all_expenses,
    get_expense_by_id
)


def register_expense_tools(mcp: FastMCP):

    @mcp.tool()
    def add_new_expense(
        amount: float,
        category: str,
        description: str = "",
        expense_date: str | None = None
    ) -> dict:
        """
        Add a new expense to the expense tracker.

        Amount should be provided in Indian Rupees.
        Example: 250.50 means ₹250.50.
        """

        rupees = Decimal(str(amount))

        if not rupees.is_finite() or rupees <= 0:
            raise ValueError("Amount must be a positive number.")

        paise = rupees * 100

        if paise != paise.to_integral_value():
            raise ValueError("Amount cannot have more than 2 decimal places.")

        amount_in_paise = int(paise)

        return add_expense(
            amount=amount_in_paise,
            category=category,
            description=description,
            expense_date=expense_date
        )

    @mcp.tool()
    def list_all_expenses() -> list[dict]:
        """
        Retrieve all expenses stored in the database.
        """
        return get_all_expenses()

    @mcp.tool()
    def find_expense(expense_id: int) -> dict | None:
        """
        Find a particular expense using its expense ID.
        """
        return get_expense_by_id(expense_id)