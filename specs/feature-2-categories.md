# Feature 2 — Expense categories

## Why

As a flatmate, I want each expense tagged with a category, so that at the end of the month I can see how much of our money went on rent, on groceries and on fun, instead of scrolling through thirty lines.

## What

Every expense gets a `category`, chosen from a fixed list when the expense is created. The group page shows a total per category.

- [ ] `logic.CATEGORIES` is exactly the list `["rent", "groceries", "fun", "transport", "other"]`, in that order.
- [ ] `expenses.csv` has a new column `category`, and every expense (including the seed data) has a value from that list. In the seed, the dinner at Zé dos Cornos (group Jantar de Curso) is `fun`.
- [ ] `add_expense(...)` accepts a `category` argument and saves it with the expense.
- [ ] A new function `category_totals(group_id)` returns a dict `{category: total}` with the total amount spent per category in that group. Categories with no expenses do not appear.

Adding a column means touching three places: `COLUMNS` in `db.py`, the CSVs in `seed/` (add the column and a category to every line), and then `uv run python seed.py` so that `data/` gets the new column too. Do not edit `data/` by hand.

## Out of scope

- Changing the category of an existing expense.
- Custom categories; the list is fixed.
- Charts. A short list of "category: total" lines is enough.

## Done when

- `pytest tests/test_feature_2.py` is green.
- The Add expense form has a category selectbox, and the group page shows a total per category.
- `uv run python seed.py` runs cleanly and the app still works after it.
- The work is on a branch called `feature-2-categories` and pushed.
