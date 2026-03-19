import sqlite3

# ✅ Get expenses for specific user
def get_user_expenses(username):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute("SELECT * FROM expenses WHERE username=?", (username,))
    data = c.fetchall()

    conn.close()
    return data


# ✅ Add expense for user
def add_user_expense(username, date, category, amount):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO expenses (username, date, category, amount) VALUES (?, ?, ?, ?)",
        (username, date, category, amount)
    )

    conn.commit()
    conn.close()