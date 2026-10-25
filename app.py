"""SplitIt: the Streamlit screens. Start the app with:  uv run streamlit run app.py"""

import streamlit as st

import logic

st.set_page_config(page_title="SplitIt", page_icon="💶")


def open_group(group_id):
    """Remember which group is open and redraw the app."""
    st.session_state["group_id"] = group_id
    st.rerun()


def close_group():
    """Forget the open group and go back to the list."""
    del st.session_state["group_id"]
    st.rerun()


def member_id_for(members, name):
    """Find the id of the member with this name (names are unique inside a group)."""
    for member in members:
        if member["name"] == name:
            return member["id"]
    return None


def show_groups_list():
    """Home screen: one card per group, with a button to open it."""
    st.title("SplitIt")
    st.caption("Split expenses with your flatmates and travel buddies.")
    for group in logic.get_groups():
        members = logic.get_group_members(group["id"])
        with st.container(border=True):
            st.subheader(group["name"])
            st.write(str(len(members)) + " members · since " + group["created_on"])
            if st.button("Open", key="open-" + group["id"]):
                open_group(group["id"])


def show_members(group_id):
    """List the members of the open group, each with a Remove button, plus the Add member form."""
    st.subheader("Members")
    for member in logic.get_group_members(group_id):
        name_column, button_column = st.columns([4, 1])
        name_column.write(member["name"])
        if button_column.button("Remove", key="remove-" + member["id"]):
            logic.remove_member(member["id"])
            st.rerun()
    with st.form("add_member", clear_on_submit=True):
        name = st.text_input("Name")
        if st.form_submit_button("Add member"):
            if logic.is_valid_name(name):
                logic.add_member(group_id, name)
                st.rerun()
            else:
                st.error("Give the new member a name.")


def show_expenses(group_id):
    """The expenses table, followed by the Add expense form."""
    st.subheader("Expenses")
    rows = logic.expense_rows(group_id)
    if len(rows) == 0:
        st.write("No expenses yet.")
    else:
        st.table(rows)
    members = logic.get_group_members(group_id)
    names = []
    for member in members:
        names.append(member["name"])
    with st.form("add_expense", clear_on_submit=True):
        description = st.text_input("Description")
        amount = st.number_input("Amount (€)", step=0.01, format="%.2f")
        payer_name = st.selectbox("Paid by", names)
        date = st.date_input("Date")
        if st.form_submit_button("Add expense"):
            payer_id = member_id_for(members, payer_name)
            logic.add_expense(group_id, payer_id, description, amount, str(date))
            st.rerun()


def show_balances(group_id):
    """Balances, work in progress: raw numbers keyed by member id."""
    st.subheader("Balances")
    st.caption("Work in progress: one number per member id. Positive means the group owes them.")
    st.write(logic.compute_balances(group_id))


def show_settle_up(group_id):
    """The settle up section. Not built yet."""
    st.subheader("Settle up")
    st.info("Coming soon")


def show_group_page(group_id):
    """The page of one group: title, members, expenses, balances, settle up."""
    group = logic.get_group(group_id)
    if st.button("← All groups"):
        close_group()
    st.title(logic.group_title(group))
    show_members(group_id)
    show_expenses(group_id)
    show_balances(group_id)
    show_settle_up(group_id)


def main():
    """Decide which screen to show: the group list, or the group that is open."""
    if "group_id" in st.session_state:
        show_group_page(st.session_state["group_id"])
    else:
        show_groups_list()


main()
