# Feature 3 — Unequal split

For groups that finished features 1 and 2 early.

## Why

As the person who ordered the salad while everybody else had the steak, I want an expense to be split by percentages instead of equally, so that the balances reflect who actually consumed what.

## What

An expense can carry an optional split. Without one, the expense is split equally, as today. With one, each member is charged their percentage of the amount.

- [ ] `expenses.csv` has a new column `split`. It is empty for an equal split; every existing expense (seed included) has it empty.
- [ ] The split is stored as text of the form `member_id:percent;member_id:percent;...`, e.g. `8:50;9:25;10:25`. A new function `parse_split(text)` in `logic.py` turns that text into a dict `{member_id: percent}` with the percentages as floats.
- [ ] A new function `split_is_valid(percentages)` returns `True` when the percentages add up to exactly 100 and `False` otherwise.
- [ ] `add_expense(...)` accepts a `split` argument (default: empty) and saves it.
- [ ] `compute_balances(group_id)` respects the split: for an expense with a split, each member's share is their percentage of the amount; the payer's net is still amount minus their own share. Expenses without a split are still split equally.

The Add expense form should offer a percentage per member (all empty = equal split) and refuse to save when the percentages do not add up to 100. That is checked in the UI, not by a test.

## Out of scope

- Splitting by fixed amounts instead of percentages.
- Leaving a member out of an expense (give them 0% instead).
- Editing the split of an existing expense.

## Done when

- `pytest tests/test_feature_3.py` is green.
- The form refuses a split that does not add up to 100, with a clear message.
- `uv run python seed.py` runs cleanly and the app still works after it.
- The work is on a branch called `feature-3-unequal-split` and pushed.
