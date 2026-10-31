from fastmcp import FastMCP
from database.database import get_connection


def register_analytics_tools(mcp: FastMCP):

    @mcp.tool()
    def get_total_expenses() -> dict:
        """
        Calculate the total amount spent across all expenses.
        """

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_transactions,
                    COALESCE(SUM(amount), 0) AS total_amount
                FROM expenses
            """)

            result = cursor.fetchone()

            return {
                "total_transactions": result["total_transactions"],
                "total_amount_rupees": result["total_amount"] / 100
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_category_wise_expenses() -> list[dict]:
        """
        Calculate total spending for each expense category.
        """

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    category,
                    COUNT(*) AS transaction_count,
                    SUM(amount) AS total_amount
                FROM expenses
                GROUP BY category
                ORDER BY total_amount DESC
            """)

            results = cursor.fetchall()

            return [
                {
                    "category": row["category"],
                    "transaction_count": row["transaction_count"],
                    "total_amount_rupees": row["total_amount"] / 100
                }
                for row in results
            ]

        finally:
            conn.close()

    @mcp.tool()
    def get_monthly_expenses(year: int, month: int) -> dict:
        """
        Calculate total expenses for a particular month.

        Example: year=2026, month=10
        """

        if not 1 <= month <= 12:
            raise ValueError("Month must be between 1 and 12.")

        if year < 1:
            raise ValueError("Invalid year.")

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) AS total_transactions,
                    COALESCE(SUM(amount), 0) AS total_amount
                FROM expenses
                WHERE strftime('%Y', expense_date) = ?
                AND strftime('%m', expense_date) = ?
            """, (f"{year:04d}", f"{month:02d}"))

            result = cursor.fetchone()

            return {
                "year": year,
                "month": month,
                "total_transactions": result["total_transactions"],
                "total_amount_rupees": result["total_amount"] / 100
            }

        finally:
            conn.close()

    @mcp.tool()
    def get_highest_expense() -> dict | None:
        """
        Find the highest individual expense.
        """

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM expenses
                ORDER BY amount DESC, id DESC
                LIMIT 1
            """)

            result = cursor.fetchone()

            if result is None:
                return None

            expense = dict(result)
            expense["amount_rupees"] = expense["amount"] / 100

            return expense

        finally:
            conn.close()