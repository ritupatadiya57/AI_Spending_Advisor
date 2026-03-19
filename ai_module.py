import pandas as pd

def analyze_expenses(data):
    if not data:
        return ["No data available"]

    # ✅ Updated columns (with Username)
    df = pd.DataFrame(data, columns=["ID", "Username", "Date", "Category", "Amount"])

    total = df["Amount"].sum()
    category_sum = df.groupby("Category")["Amount"].sum()

    advice = []

    if category_sum.get("Food", 0) > 3000:
        advice.append("⚠️ You are spending too much on Food!")

    if category_sum.get("Shopping", 0) > 5000:
        advice.append("⚠️ Reduce Shopping expenses!")

    if total > 20000:
        advice.append("⚠️ Overall spending is too high!")

    if not advice:
        advice.append("✅ Your spending is under control!")

    return advice