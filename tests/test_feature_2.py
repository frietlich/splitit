"""Feature 2: every expense has a category, and the group page shows a total per category.

RED until the feature is built. Remember to add the column to the CSVs in seed/ and run uv run python seed.py.
"""

import db
import logic

# Seed group "Jantar de Curso" (id 3): one €30 dinner paid by João (8), to be tagged "fun" in the seed.
JANTAR = "3"
JOAO = "8"


def test_the_category_list_is_fixed():
    """The five categories, in this order, live in logic.CATEGORIES."""
    assert logic.CATEGORIES == ["rent", "groceries", "fun", "transport", "other"]


def test_expenses_have_a_category_column(fresh_data):
    """Every expense in the CSV has a category from the list."""
    for expense in db.load_table("expenses"):
        assert expense["category"] in logic.CATEGORIES


def test_add_expense_saves_the_category(fresh_data):
    """add_expense takes a category and writes it to the CSV."""
    new_id = logic.add_expense(JANTAR, JOAO, "Táxi para casa", 12.0, "2026-08-26", category="transport")
    saved = None
    for expense in db.load_table("expenses"):
        if expense["id"] == str(new_id):
            saved = expense
    assert saved["category"] == "transport"


def test_category_totals_for_a_group(fresh_data):
    """category_totals adds up the amounts per category, skipping empty categories."""
    logic.add_expense(JANTAR, JOAO, "Táxi para casa", 12.0, "2026-08-26", category="transport")
    logic.add_expense(JANTAR, JOAO, "Copos depois do jantar", 8.5, "2026-08-26", category="fun")
    assert logic.category_totals(JANTAR) == {"fun": 38.5, "transport": 12.0}
