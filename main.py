from fastmcp import FastMCP

from tools.tool import register_expense_tools
from tools.analytics_tools import register_analytics_tools


# Initialize MCP server
mcp = FastMCP(
    name="Expense Tracker MCP",
    instructions="""
    You are an Expense Tracker assistant.

    You can help users:
    - Add new expenses.
    - View all expenses.
    - Find expenses using their IDs.
    - Calculate total spending.
    - Analyze category-wise expenses.
    - Calculate monthly expenses.
    - Find their highest expense.

    All monetary amounts provided by users are in Indian Rupees (INR).
    """
)


# Register expense tools
register_expense_tools(mcp)

# Register analytics tools
register_analytics_tools(mcp)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)