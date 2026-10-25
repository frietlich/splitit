"""Feature 1: balances in plain words on the group page. RED until the feature is built.

Blocked by issue 001: the numbers only come out right once compute_balances is fixed.
"""

import logic

# Seed group "Jantar de Curso" (id 3): João (8) paid €30 for himself, Carolina (9) and Mariana (10).
JANTAR = "3"


def test_one_line_per_member(fresh_data):
    """There is one sentence for every member of the group."""
    lines = logic.balance_lines(JANTAR)
    assert len(lines) == 3


def test_someone_who_is_owed_money(fresh_data):
    """A positive balance reads '<Name> is owed €<amount>'."""
    assert "João is owed €20.00" in logic.balance_lines(JANTAR)


def test_someone_who_owes_money(fresh_data):
    """A negative balance reads '<Name> owes €<amount>', without a minus sign."""
    lines = logic.balance_lines(JANTAR)
    assert "Carolina owes €10.00" in lines
    assert "Mariana owes €10.00" in lines


def test_someone_who_is_settled(fresh_data):
    """A zero balance reads '<Name> is settled up'."""
    # If Carolina and Mariana each pay a €30 round as well, nobody owes anybody.
    logic.add_expense(JANTAR, "9", "Segunda rodada", 30.0, "2026-08-26")
    logic.add_expense(JANTAR, "10", "Terceira rodada", 30.0, "2026-08-27")
    lines = logic.balance_lines(JANTAR)
    assert lines == ["João is settled up", "Carolina is settled up", "Mariana is settled up"]
