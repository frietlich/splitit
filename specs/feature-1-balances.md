# Feature 1 — Balances in plain words

**Blocked by issue 001.** The numbers are computed by `compute_balances`, which is wrong today. Fix the bug first, otherwise this feature will proudly show wrong balances.

## Why

As a member of a group, I want to see at a glance who is owed money and who owes, in words I can read out loud to my flatmates, so that we stop arguing over a spreadsheet.

Today the group page has a "Balances" box that shows raw numbers next to member ids. Nobody knows who "9" is.

## What

A new function `balance_lines(group_id)` in `logic.py` returns one sentence per member, in the same order as the members list. The group page shows those sentences instead of the raw numbers.

- [ ] `balance_lines(group_id)` returns exactly one line per member of the group.
- [ ] A member with a positive balance gets `"<Name> is owed €<amount>"`, e.g. `João is owed €20.00`.
- [ ] A member with a negative balance gets `"<Name> owes €<amount>"`, e.g. `Carolina owes €10.00` (no minus sign).
- [ ] A member whose balance is zero gets `"<Name> is settled up"`.
- [ ] Amounts always have two decimals (`€8.20`, not `€8.2`).

## Out of scope

- Who should pay whom to settle everything (that is the Settle up section, later).
- Rounding the balances themselves (issue 003 is about shares, not balances).
- Changing the way balances are stored.

## Done when

- `pytest tests/test_feature_1.py` is green (and the bug 001 test with it).
- The group page shows the sentences under the "Balances" heading, and the raw numbers are gone.
- The work is on a branch called `feature-1-balances` and pushed.
