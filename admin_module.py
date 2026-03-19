from database import view_expenses

def get_all_data():
    return view_expenses()

def total_transactions():
    data = view_expenses()
    return len(data)