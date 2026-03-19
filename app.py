import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from datetime import date
from database import create_user_table, register_user, login_user
from database import connect
from user_module import add_user_expense, get_user_expenses
from ai_module import analyze_expenses
from admin_module import total_transactions
from database import create_finance_table, save_finance, get_finance
from database import delete_expense, update_expense
connect()

st.title("💰 AI Smart Spending Advisor")

menu = st.sidebar.selectbox(
    "Menu",
    ["Select Option", "User", "Admin"],
    index=0
)

# 🎨 COLOR CONTROL
if menu == "Select Option":
    title_color = "black"
else:
    title_color = "white"

# ✅ ALWAYS SHOW SIDEBAR
with st.sidebar:

    st.markdown(f"<h3 style='color:{title_color}'>👨‍💻 Developed by</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px; margin-bottom:10px;">
    Ritu Patadiya
    </div>

    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px; margin-bottom:10px;">
    Honey Sathwara
    </div>

    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px; margin-bottom:10px;">
    Prajapati Suhani
    </div>

    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px;">
    Yashasvi Vadukul
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<h3 style='color:{title_color}'>🎓 Mentored by</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px; margin-bottom:10px;">
    Mr. Praful Vinayak Bhoyar
    </div>

    <div style="background-color:#ffffff; color:black; padding:10px; border-radius:10px;">
    Mr. Ankit Dixit
    </div>
    """, unsafe_allow_html=True)

# 👉 MAIN PAGE CONTROL
if menu == "Select Option":
    st.warning("Please select an option 👈")
    st.stop()

# your other imports
from database import connect
from user_module import add_user_expense, get_user_expenses
from ai_module import analyze_expenses
from admin_module import total_transactions

# ---------------- ADMIN MODULE ----------------
ADMINS = {
    "ritu": "1234",
    "hony": "1111",
    "suhani": "2222",
    "yashvi": "3333"
}

# Initialize login admin
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if menu == "Admin":

    # If NOT logged in → show login form
    if not st.session_state.admin_logged_in:

        st.header(" Admin Login")

        admin_id = st.text_input("Enter Admin ID")
        admin_pass = st.text_input("Enter Password", type="password")

        if st.button("Login"):

            if admin_id in ADMINS and ADMINS[admin_id] == admin_pass:
                st.session_state.admin_logged_in = True
                st.session_state.admin_name = admin_id
                st.success(f"Welcome {admin_id} ✅")

            else:
                st.error("Invalid ID or Password ❌")

    # If logged in → show dashboard
    else:
        st.header("Admin Dashboard")

        st.write(f"Logged in as: {st.session_state.admin_name}")

        total = total_transactions()
        st.write(f"Total Transactions: {total}")

        # Logout button
        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.success("Logged out successfully")

# ---------------- USER MODULE ----------------
from database import connect, create_user_table, register_user, login_user

# Initialize DB
connect()
create_user_table()
create_finance_table()
# ✅ ADD THIS HERE
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if menu == "User":
    #  ----------login------------
    if not st.session_state.user_logged_in:

        choice = st.radio("Select Option", ["Login", "Register"])

        # -------- REGISTER --------
        if choice == "Register":
            st.subheader("Create Account")

            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type="password")

            if st.button("Register"):
                success = register_user(new_user, new_pass)
                if success:
                    st.success("Account created successfully.")
                else:
                    st.error("Username already exists.")

        # -------- LOGIN --------
        elif choice == "Login":
            st.subheader("Login")

            user = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                result = login_user(user, password)
                if result:
                    st.session_state.user_logged_in = True
                    st.session_state.username = user
                    st.success(f"Welcome {user}.")
                else:
                    st.error("Invalid credentials")

    # -------- AFTER LOGIN --------
    else:
        st.write(f"Logged in as: {st.session_state.username}")

        st.markdown("### 💼 Financial Details")
        current_month = datetime.datetime.now().strftime("%Y-%m")
        saved_data = get_finance(st.session_state.username, current_month)

        if saved_data:
            salary, loan_amount = saved_data
            st.success(f"Data already saved for {current_month}")
            st.write(f"Salary: ₹ {salary}")
            st.write(f"Loan: ₹ {loan_amount}")

        else:
            salary = st.number_input("Enter your Monthly Salary (₹)", min_value=00)

            loan_option = st.radio("Do you have any loan?", ["No", "Yes"])

            loan_amount = 0
            if loan_option == "Yes":
                loan_amount = st.number_input("Enter Monthly Loan Payment (₹)", min_value=0.0)

                if loan_amount > salary:
                    st.error("Loan cannot be greater than salary!")
                    st.stop()

            if st.button("Save Financial Data"):
                save_finance(st.session_state.username, current_month, salary, loan_amount)
                st.success("Data saved successfully ✅")

        # 💰 CALCULATION (KEEP THIS)
        remaining_after_loan = salary - loan_amount
        st.markdown("### 💰 After Loan Calculation")
        st.info(f"Remaining after loan: ₹ {remaining_after_loan}")

        # ➕ Add Expense
        st.header("Add Expense")

        expense_date = st.date_input("Date",value=date.today(),max_value=date.today())
        category = st.selectbox("Category", ["--select--","Food", "Travel", "Shopping", "Bills", "Other"])
        amount = st.number_input("Amount", min_value=00)

        if st.button("Add"):
            current_month = datetime.datetime.now().strftime("%Y-%m")
            data = get_user_expenses(st.session_state.username)

            current_total = 0

            if data:
        # 🧠 Filter only current month data
                monthly_data = [row for row in data if row[2].startswith(current_month)]

                if monthly_data:
                    df_temp = pd.DataFrame(monthly_data, columns=["ID", "Username", "Date", "Category", "Amount"])
                    current_total = df_temp["Amount"].sum()

            # 💰 Max allowed spending
            if loan_amount > 0:
                max_allowed = salary - loan_amount
            else:
                max_allowed = salary

            # ❌ VALIDATION
            if category == "--select--":
                st.warning("⚠️ Please select a valid category")

            elif amount <= 0:
                st.warning("⚠️ Please enter a valid amount")

            elif current_total + amount > max_allowed:
                st.error("❌ Cannot add expense! Total expenses exceed your available balance.")

            else:
                add_user_expense(st.session_state.username, str(expense_date), category, amount)
                st.success("Expense added!")

        st.header("Your Expenses")
        data = get_user_expenses(st.session_state.username)

        if data:
            df = pd.DataFrame(data, columns=["ID", "Username", "Date", "Category", "Amount"])

            # 📋 SHOW TABLE WITH ACTIONS
            for index, row in df.iterrows():
                col1, col2, col3, col4, col5 = st.columns(5)

                col1.write(row["Date"])
                col2.write(row["Category"])
                col3.write(f"₹ {row['Amount']}")

                # ✏️ EDIT BUTTON
                if col4.button("✏️ Edit", key=f"edit_{row['ID']}"):
                    st.session_state.edit_id = row["ID"]

                # 🗑️ DELETE BUTTON
                if col5.button("🗑️ Delete", key=f"delete_{row['ID']}"):
                    delete_expense(row["ID"])
                    st.success("Deleted successfully")
                    st.rerun()

            # 💰 CALCULATION (KEEP THIS SAME)
            total_expense = df["Amount"].sum()
            remaining = salary - loan_amount - total_expense

            # ✏️ EDIT FORM
            if "edit_id" in st.session_state:

                st.subheader("✏️ Edit Expense")

                edit_id = st.session_state.edit_id

                # 👉 GET OLD DATA
                old_data = df[df["ID"] == edit_id].iloc[0]

                # 👉 AUTO-FILL VALUES
                new_date = st.date_input(
                    "New Date",
                    value=pd.to_datetime(old_data["Date"])
                )

                categories = ["Food", "Travel", "Shopping", "Bills", "Other"]

                new_category = st.selectbox(
                    "New Category",
                    categories,
                    index=categories.index(old_data["Category"])
                )

                new_amount = st.number_input(
                    "New Amount",
                    min_value=0.0,
                    value=float(old_data["Amount"])
                )

                # ✅ UPDATE BUTTON
                if st.button("Update"):
                    update_expense(edit_id, str(new_date), new_category, new_amount)
                    st.success("Updated successfully")
                    del st.session_state.edit_id
                    st.rerun()

                # ❌ CANCEL BUTTON (OPTIONAL BUT USEFUL)
                if st.button("Cancel"):
                    del st.session_state.edit_id
                    st.rerun()

            # 💼 SUMMARY
            st.markdown(f"""
            ### 💼 Financial Summary
            - Salary: ₹ {salary}
            - Loan: ₹ {loan_amount}
            - Expenses: ₹ {total_expense}
            - Remaining: ₹ {remaining}
            """)

            # 🥧 PIE + 📊 BAR IN ONE LINE
            df["Date"] = pd.to_datetime(df["Date"])
            from datetime import datetime
            current_month = datetime.now().month
            current_year = datetime.now().year

            monthly_df = df[
                (df["Date"].dt.month == current_month) &
                (df["Date"].dt.year == current_year)
            ]

            st.subheader(f"📊 Monthly Spending - {datetime.now().strftime('%B %Y')}")

            # 👉 CREATE 2 COLUMNS
            col1, col2 = st.columns(2)

            # 🥧 PIE CHART (LEFT)
            with col1:
                st.subheader("Distribution")
                fig, ax = plt.subplots(figsize=(3,3))  # smaller for fit

                monthly_df.groupby("Category")["Amount"].sum().plot.pie(
                    autopct='%1.1f%%',
                    ax=ax
                )
                ax.set_ylabel("")
                st.pyplot(fig)

            # 📊 BAR CHART (RIGHT)
            with col2:
                st.subheader("Category Spending")
                category_data = monthly_df.groupby("Category")["Amount"].sum()
                st.bar_chart(category_data)

            # 🤖 SMART AI ADVICE
            st.subheader("🤖 Smart Financial Advice")

            advice = []

            if remaining < 0:
                advice.append("🚨 You are overspending! Reduce expenses.")
            elif remaining < salary * 0.2:
                advice.append("⚠️ Savings are low. Try to save more.")
            else:
                advice.append("✅ Good job! You are managing well.")

            if loan_amount > salary * 0.4:
                advice.append("⚠️ High loan burden. Reduce EMI if possible.")
            elif loan_amount > 0:
                advice.append("💡 Manage your loan carefully.")

            saving_target = salary * 0.2

            if remaining > saving_target:
                advice.append(f"💰 You can save at least ₹ {int(saving_target)} this month.")
            else:
                advice.append("💡 Try to save at least 20% of your salary.")

            for a in advice:
                st.write(a)

        # Logout
        if st.button("Logout"):
            st.session_state.user_logged_in = False
            st.success("Logged out successfully")


st.markdown("""
<style>

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #00b2ec;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
    font-weight: 500;
}

/* Dropdown (selectbox) styling */
[data-testid="stSidebar"] .stSelectbox > div {
    background-color: white;
    color: black;
    border-radius: 8px;
}

/* Buttons */
.stButton>button {
    background-color: #00b2ec;
    color: white;
    border-radius: 10px;
    border: none;
}

/* Button hover */
.stButton>button:hover {
    background-color: #0095c8;
}

/* Cards (light theme) */
.card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)