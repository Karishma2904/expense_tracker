import streamlit as st
import pandas as pd
import as plt  # <- Required for pie chart

# Modern, aesthetic CSS
st.markdown("""
    <style>
        [data-testid="stApp"] {
            background-color: #ffe4e1;
            font-family: 'Segoe UI', sans-serif;
            color: #333333;
        }
        .stNumberInput input, .stSelectbox div, .stTextInput input, .stTextArea textarea {
            background-color: #fffacd !important;
            color: #333 !important;
            border-radius: 10px;
            padding: 8px;
            border: 1px solid #ccc;
        }
        button[kind="primary"] {
            background-color: #ff69b4;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
            border: none;
            transition: 0.3s ease-in-out;
        }
        button[kind="primary"]:hover {
            background-color: #ff1493;
            transform: scale(1.05);
        }
        .stDataFrame {
            background-color: #fff0f5;
            border-radius: 10px;
        }
        .stMarkdown h1 {
            color: #d63384;
            font-weight: bold;
        }
        .stAlert {
            background-color: #ffe6f0;
            border-left: 5px solid #d63384;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

st.title("Simple Daily Expense Tracker")

# Input form
with st.form("expense_form"):
    amount = st.number_input("Enter Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Other"])
    submit = st.form_submit_button("Add Expense")

# Add to session state
if submit and amount > 0:
    st.session_state.expenses.append({"Amount": amount, "Category": category})

# Show table and summary
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    st.subheader("Today's Expenses")
    st.dataframe(df)

    total = df['Amount'].sum()
    st.success(f"Total Spent Today: ₹{total:.2f}")

    # --- Pie Chart ---
    st.subheader("Spending by Category")
    category_totals = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()
    ax.pie(
        category_totals,
        labels=category_totals.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#ff9999", "#ffcc99", "#99ff99", "#66b3ff"]
    )
    ax.axis("equal")  # Equal aspect ratio for perfect circle
    st.pyplot(fig)

    # Reset button
    if st.button("Reset Expenses"):
        st.session_state.expenses = []
        st.experimental_rerun()