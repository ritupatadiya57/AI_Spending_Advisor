import sqlite3

# ---------------- USER AUTH ----------------

def create_user_table():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    data = c.fetchone()
    conn.close()
    return data

def create_table():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    date TEXT,
    category TEXT,
    amount REAL
)
""")

    conn.commit()
    conn.close()

import sqlite3

def create_finance_table():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_finance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        month TEXT,
        salary REAL,
        loan REAL
    )
    """)

    conn.commit()
    conn.close()

def save_finance(username, month, salary, loan):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO user_finance (username, month, salary, loan)
    VALUES (?, ?, ?, ?)
    """, (username, month, salary, loan))

    conn.commit()
    conn.close()

def get_finance(username, month):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    SELECT salary, loan FROM user_finance
    WHERE username=? AND month=?
    """, (username, month))

    data = c.fetchone()

    conn.close()
    return data

def delete_expense(expense_id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("DELETE FROM expenses WHERE id=?", (expense_id,))

    conn.commit()
    conn.close()

def update_expense(expense_id, date, category, amount):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("""
    UPDATE expenses
    SET date=?, category=?, amount=?
    WHERE id=?
    """, (date, category, amount, expense_id))

    conn.commit()
    conn.close()

def connect():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    # ✅ NEW TABLE STRUCTURE (WITH USERNAME)
    c.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        date TEXT,
        category TEXT,
        amount REAL
    )
    """)

    # users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_expense(date, category, amount):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, amount) VALUES (?, ?, ?)",
              (date, category, amount))
    conn.commit()
    conn.close()

def view_expenses():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    data = c.fetchall()
    conn.close()
    return data