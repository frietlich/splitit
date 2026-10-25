"""One test per planted bug. They are RED on purpose: each one describes the CORRECT behaviour.

Fix the bug in the app code (never in here) and the test turns green.
"""

import logic

# The seed group "Jantar de Curso" (id 3): three members, João (id 8) paid the €30 dinner.
JANTAR = "3"
JOAO = "8"
CAROLINA = "9"
MARIANA = "10"


def test_bug_000_group_title():
    """The heading of a group page is the group's name, not its id."""
    group = {"id": "2", "name": "Surf Trip Ericeira", "created_on": "2026-08-07"}
    assert logic.group_title(group) == "Surf Trip Ericeira"


def test_bug_001_balances_split_among_everyone(fresh_data):
    """€30 paid by João for three people: João is owed €20, the other two owe €10 each."""
    balances = logic.compute_balances(JANTAR)
    assert round(balances[JOAO], 2) == 20.0
    assert round(balances[CAROLINA], 2) == -10.0
    assert round(balances[MARIANA], 2) == -10.0


def test_bug_002_removing_a_member_removes_their_expenses(fresh_data):
    """Removing João also removes the expenses he paid, so the group page still renders."""
    assert hasattr(logic, "remove_member_expenses"), "remove_member should call a remove_member_expenses step"
    logic.remove_member(JOAO)
    rows = logic.expense_rows(JANTAR)  # this is the line that used to crash
    assert rows == []
    for expense in logic.get_group_expenses(JANTAR):
        assert expense["payer_id"] != JOAO


def test_bug_003_shares_add_up_to_the_total():
    """€10 between three people: shares have two decimals, add up to €10, and the payer gets the leftover cent."""
    shares = logic.compute_shares(10.0, ["5", "6", "7"], "6")
    for share in shares.values():
        assert share == round(share, 2)
    assert round(sum(shares.values()), 2) == 10.0
    assert shares["6"] == 3.34
    assert shares["5"] == 3.33
    assert shares["7"] == 3.33
