import streamlit as st
from collections import defaultdict

# At the top
st.title("🔐 Secure Splitwise App")

# Hardcoded simple login
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username != "Andy" or password != "2004":
    st.warning("Enter valid credentials to continue.")
    st.stop()
#for centre
st.set_page_config(layout="centered")



st.set_page_config(page_title="My Splitwise App", layout="centered")

st.title("💸 Personalized Splitwise App")

# Reset all session data
if st.button("🔁 Reset All Data"):
    st.session_state.people = []
    st.session_state.expenses = []
    st.success("All data has been reset!")

# Initialize session state
if "people" not in st.session_state:
    st.session_state.people = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

# Section: Add people
st.header("1. Add People")
new_person = st.text_input("Enter a name:")
if st.button("Add Person"):
    if new_person and new_person not in st.session_state.people:
        st.session_state.people.append(new_person)
        st.success(f"{new_person} added!")
    else:
        st.warning("Invalid or duplicate name.")

st.write("Current people:", ", ".join(st.session_state.people))

# Section: Add expense
st.header("2. Add Expense")
if len(st.session_state.people) >= 2:
    amount = st.number_input("Total Amount", min_value=0.0, step=0.5)
    payer = st.selectbox("Paid by", st.session_state.people)
    participants = st.multiselect("Split among", st.session_state.people, default=st.session_state.people)

    if st.button("Add Expense"):
        if amount > 0 and payer in st.session_state.people and participants:
            st.session_state.expenses.append({
                "amount": amount,
                "payer": payer,
                "participants": participants
            })
            st.success("Expense added!")
        else:
            st.error("Fill all fields properly.")

# Section: Show all expenses
st.header("3. All Expenses")
for i, exp in enumerate(st.session_state.expenses):
    st.markdown(f"- ₹{exp['amount']} paid by **{exp['payer']}** for {', '.join(exp['participants'])}")

# Section: Final settlement calculation
st.header("4. Final Settlement")

balances = defaultdict(float)

# Calculate balances
for exp in st.session_state.expenses:
    amt = exp["amount"]
    payer = exp["payer"]
    participants = exp["participants"]
    split_amt = amt / len(participants)

    for person in participants:
        balances[person] -= split_amt
    balances[payer] += amt

# Simplify debts
def simplify(bal):
    creditors = sorted([(p, a) for p, a in bal.items() if a > 0], key=lambda x: -x[1])
    debtors = sorted([(p, a) for p, a in bal.items() if a < 0], key=lambda x: x[1])

    transactions = []

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, d_amt = debtors[i]
        creditor, c_amt = creditors[j]

        settle = min(-d_amt, c_amt)
        transactions.append(f"{debtor} pays ₹{settle:.2f} to {creditor}")

        debtors[i] = (debtor, d_amt + settle)
        creditors[j] = (creditor, c_amt - settle)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transactions

settlements = simplify(balances)

if settlements:
    st.subheader("💰 Settlements")
    for t in settlements:
        st.write("➡️", t)
else:
    if st.session_state.expenses:
        st.success("🎉 All settled up!")
        
if st.checkbox("🛠 Show Internal Balances"):
    st.write("Balances:", dict(balances))
