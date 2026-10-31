import sqlite3
from pathlib import Path

# Get the database directory
BASE_DIR = Path(__file__).resolve().parent

# Database file location
DB_PATH = BASE_DIR / "expenses.db"


# Establish database connection
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Create expenses table
def create_table():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        print("Expenses table created successfully!")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


# Initialize database
if __name__ == "__main__":
    create_table()