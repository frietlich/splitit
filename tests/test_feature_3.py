"""Feature 3: an expense can be split by percentages instead of equally.

RED until the feature is built. The split is stored in a new "split" column of expenses.csv
(empty = equal split), written as member_id:percent pairs separated by semicolons, e.g. "8:50;9:25;10:25".
"""

import db
import logic

# Seed group "Jantar de Curso" (id 3): João (8) paid €30 for himself, Carolina (9) and Mariana (10).
JANTAR = "3"
JOAO = "8"
CAROLINA = "9"
MARIANA = "10"


def test_expenses_have_a_split_column(fresh_data):
    """Every existing expense has an empty split, meaning equal shares."""
    for expense in db.load_table("expenses"):
        assert expense["split"] == ""


def test_parse_split_reads_the_percentages():
    """parse_split turns the stored text into a dict of percentages."""
    assert logic.parse_split("8:50;9:25;10:25") == {"8": 50.0, "9": 25.0, "10": 25.0}


def test_a_split_must_add_up_to_100():
    """split_is_valid accepts 100 in total and rejects anything else."""
    assert logic.split_is_valid({"8": 50.0, "9": 25.0, "10": 25.0}) is True
    assert logic.split_is_valid({"8": 60.0, "9": 25.0, "10": 25.0}) is False


def test_balances_respect_the_split(fresh_data):
    """An expense with a split charges each member their percentage."""
    # João pays €30 of wine; Carolina drinks most of it: 20% / 60% / 20%.
    logic.add_expense(JANTAR, JOAO, "Vinho", 30.0, "2026-08-26", split="8:20;9:60;10:20")
    balances = logic.compute_balances(JANTAR)
    # Dinner (equal): João +20, Carolina -10, Mariana -10.  Wine: João +24, Carolina -18, Mariana -6.
    assert round(balances[JOAO], 2) == 44.0
    assert round(balances[CAROLINA], 2) == -28.0
    assert round(balances[MARIANA], 2) == -16.0
