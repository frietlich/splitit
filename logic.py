"""Business rules for SplitIt: who paid, who owes, and how much each person's share is."""

import db

# The categories an expense can have. Fixed on purpose: see specs/feature-2-categories.md.
CATEGORIES = ["rent", "groceries", "fun", "transport", "other"]


def get_groups():
    """Return every group as a list of dicts."""
    return db.load_table("groups")


def get_group(group_id):
    """Return the group with this id, or None if there is no such group."""
    for group in db.load_table("groups"):
        if group["id"] == str(group_id):
            return group
    return None


def get_group_members(group_id):
    """Return the members (a list of dicts) that belong to one group."""
    members = []
    for member in db.load_table("members"):
        if member["group_id"] == str(group_id):
            members.append(member)
    return members


def get_group_expenses(group_id):
    """Return the expenses (a list of dicts) of one group, in the order they were added."""
    expenses = []
    for expense in db.load_table("expenses"):
        if expense["group_id"] == str(group_id):
            expenses.append(expense)
    return expenses


def group_title(group):
    """Return the text shown as the big heading at the top of a group page."""
    return group["name"]


def is_valid_name(name):
    """A member name is valid when it is not empty (spaces alone do not count)."""
    return name.strip() != ""


def add_member(group_id, name):
    """Save a new member in a group and return the id they were given."""
    member = {"id": db.next_id("members"), "group_id": group_id, "name": name.strip()}
    db.append_row("members", member)
    return member["id"]


def add_expense(group_id, payer_id, description, amount, date, category="other"):
    """Save a new expense, paid by one member for the whole group, and return its id."""
    expense = {
        "id": db.next_id("expenses"),
        "group_id": group_id,
        "payer_id": payer_id,
        "description": description.strip(),
        "amount": amount,
        "date": date,
        "category": category,
    }
    db.append_row("expenses", expense)
    return expense["id"]


def remove_member_expenses(member_id):
    """Delete every expense this member paid for."""
    kept = []
    for expense in db.load_table("expenses"):
        if expense["payer_id"] != str(member_id):
            kept.append(expense)
    db.save_table("expenses", kept)


def remove_member(member_id):
    """Delete one member, and the expenses they paid for with them.

    Without the expenses the group page would crash: they would keep pointing
    at a payer_id that no longer has a name (see issues/002).
    """
    remove_member_expenses(member_id)
    kept = []
    for member in db.load_table("members"):
        if member["id"] != str(member_id):
            kept.append(member)
    db.save_table("members", kept)


def compute_shares(amount, member_ids, payer_id):
    """Split one amount between members and return {member_id: share}."""
    shares = {}
    for member_id in member_ids:
        shares[member_id] = amount / len(member_ids)
    return shares


def compute_balances(group_id):
    """Return {member_id: net}: positive means the group owes them, negative means they owe."""
    members = get_group_members(group_id)
    balances = {}
    for member in members:
        balances[member["id"]] = 0.0
    for expense in get_group_expenses(group_id):
        amount = float(expense["amount"])
        payer_id = expense["payer_id"]
        # Everybody shares the bill, the payer included: they ate too.
        share = amount / len(members)
        for member in members:
            balances[member["id"]] -= share
        balances[payer_id] += amount
    return balances


def balance_lines(group_id):
    """Return one sentence per member of the group, in the order of the members list."""
    balances = compute_balances(group_id)
    lines = []
    for member in get_group_members(group_id):
        amount = round(balances[member["id"]], 2)
        if amount > 0:
            lines.append(member["name"] + " is owed €" + format(amount, ".2f"))
        elif amount < 0:
            # The word "owes" already carries the sign, so drop the minus.
            lines.append(member["name"] + " owes €" + format(-amount, ".2f"))
        else:
            lines.append(member["name"] + " is settled up")
    return lines


def category_totals(group_id):
    """Return {category: total spent} for one group. Categories with no expenses are left out."""
    totals = {}
    for expense in get_group_expenses(group_id):
        category = expense["category"]
        amount = float(expense["amount"])
        if category in totals:
            totals[category] = totals[category] + amount
        else:
            totals[category] = amount
    for category in totals:
        totals[category] = round(totals[category], 2)
    return totals


def expense_rows(group_id):
    """Build the rows of the expenses table on the group page (one dict per expense)."""
    members = get_group_members(group_id)
    names = {}
    for member in members:
        names[member["id"]] = member["name"]
    member_ids = list(names.keys())
    rows = []
    for expense in get_group_expenses(group_id):
        payer_name = names[expense["payer_id"]]
        amount = float(expense["amount"])
        shares = compute_shares(amount, member_ids, expense["payer_id"])
        # Show what a member other than the payer has to chip in.
        each = None
        for member_id in member_ids:
            if member_id != expense["payer_id"]:
                each = shares[member_id]
        rows.append({
            "Description": expense["description"],
            "Paid by": payer_name,
            "Amount": "€" + expense["amount"],
            "Each": "€" + str(each),
            "Date": expense["date"],
        })
    return rows


def settle_up(group_id):
    """Work out the smallest set of payments that clears every debt in the group and record them."""
    # TODO: compute who pays whom and mark expenses as settled
