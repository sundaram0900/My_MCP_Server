import sqlite3
import os
import shutil
from pathlib import Path


# Create a writable application data directory
APP_DATA_DIR = (
    Path(os.getenv("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    / "ExpenseTrackerMCP"
)

APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

# New database location
DB_PATH = APP_DATA_DIR / "expenses.db"

# Previous database location
OLD_DB_PATH = Path(__file__).resolve().parent / "expenses.db"

# Preserve existing database
if OLD_DB_PATH.exists() and not DB_PATH.exists():
    shutil.copy2(OLD_DB_PATH, DB_PATH)


def get_connection():
    conn = sqlite3.connect(str(DB_PATH), timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


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

        print("Database initialized successfully!")
        print(f"Database location: {DB_PATH}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    create_table()