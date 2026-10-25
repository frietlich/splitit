# Onboarding sheet — SplitIt

Group: individual work   Members: ____________________________

Answer in this file, inside your project folder. Use the AI as much as you like — then verify every answer in the code or by clicking. Write *where* you verified (file + line, or what you clicked).

## Ask the code

**1. In one sentence, what does SplitIt do for its user?**

SplitIt keeps track of the shared expenses of a group — flatmates or a trip — and works out who owes whom at the end.

*Verified:* `README.md:3`, and the subtitle in the code, `app.py:33`.

**2. Which file runs first when you start the app? How do you know?**

`app.py`. Four independent reasons:

- The start command is literally `streamlit run app.py` (`README.md:9`), so Streamlit executes that file top to bottom.
- `app.py:118` calls `main()` at the top level, unindented. Nothing else calls `main()`.
- The import chain runs `app.py:5` (`import logic`) → `logic.py:3` (`import db`). `logic.py` and `db.py` only run because `app.py` imports them.
- Visible without reading code: `app.py:7` sets `page_title="SplitIt"`, and the browser tab says "SplitIt".

**3. Where is the data stored? Name the file and the three tables.**

`db.py` is the only file that reads or writes data (`load_table`, `save_table`, `append_row`, `next_id`). `db.py:7` points it at the `data/` folder next to the code. The three tables are defined in `db.py:10-14`:

| Table | File | Columns |
|---|---|---|
| groups | `data/groups.csv` | id, name, created_on |
| members | `data/members.csv` | id, group_id, name |
| expenses | `data/expenses.csv` | id, group_id, payer_id, description, amount, date |

Not a database — three plain CSV files. CSV stores text only, which is why `logic.py:92` has to call `float(expense["amount"])` when reading an amount back.

**4. Click Add expense. Which function runs? Which function does that call to save it?**

`logic.add_expense` runs, and it calls `db.append_row` to save.

```
app.py:79    the "Add expense" button of the form at app.py:74 is pressed
app.py:80    member_id_for()  - turns the name "Rita" into the id "1"
app.py:81    logic.add_expense(group_id, payer_id, description, amount, date)
logic.py:54  add_expense() builds the dict
logic.py:57    db.next_id("expenses")  - next free id
logic.py:64    db.append_row("expenses", expense)   <- this is the save
db.py:42     append_row() opens data/expenses.csv in append mode
db.py:46     writer.writerow(row)
app.py:82    st.rerun() - redraw, the expense appears in the table
```

*Verified by clicking:* a test expense was added through the form and landed as line 30 of `data/expenses.csv`.

The pattern underneath, which repeats across the whole app: `app.py` = screen → `logic.py` = rule → `db.py` = file. The screen never calculates, the rule never writes.

**5. `get_group_members` is used in more than one place. Where? Why is it a function instead of copy-pasting the code?**

Defined at `logic.py:19`, used in five places:

| Where | For what |
|---|---|
| `app.py:35` | group list, to count "4 members" |
| `app.py:46` | the members list on the group page |
| `app.py:70` | fills the "Paid by" dropdown |
| `logic.py:87` | `compute_balances` — how many people to divide by |
| `logic.py:105` | `expense_rows` — id to name for the table |

The function is only four lines (`logic.py:21-25`), but line 23 contains a subtlety: `member["group_id"] == str(group_id)`. The `str()` is needed because CSV always returns text while callers pass sometimes `"1"` and sometimes `1`. Without it the comparison is `"1" == 1`, which is `False` in Python, and the group would appear empty.

Copy-pasted five times, that is five chances to drop the `str()`, and the bug would only show on one screen — which makes it miserable to find. As one function there is a single source of truth: fix line 23 and all five callers are fixed. And when the storage moves from CSV to a real database, one function changes instead of five call sites.

**6. Add an expense with amount `0` and one with `-20`. What happens? Find the line that should have stopped you.**

Both are saved silently. No error, no warning. Straight from `data/expenses.csv`:

```
30,1,1,TEST amount zero,0.0,2026-09-08
31,1,1,TEST amount negative,-20.0,2026-09-08
```

The `-20` is the dangerous one: it inverts the balances. Computed with the app's own `compute_balances`:

| Member | without the tests | with `0` and `-20` | difference |
|---|---:|---:|---:|
| Rita (the payer) | 1612.15 | 1592.15 | **-20.00** |
| Tomás | -461.58 | -454.91 | +6.67 |
| Inês | -560.58 | -553.91 | +6.67 |
| Duarte | -589.99 | -583.33 | +6.67 |

Rita "paid" and is worse off for it, the other three are better off. Exactly backwards.

*The line that should have stopped it:* `app.py:79-81`.

```python
if st.form_submit_button("Add expense"):
    payer_id = member_id_for(members, payer_name)
    logic.add_expense(group_id, payer_id, description, amount, str(date))
```

It saves without any check. The comparison with the form right above makes it obvious — "Add member" at `app.py:54-59` does check:

```python
if st.form_submit_button("Add member"):
    if logic.is_valid_name(name):      # <- the check
        logic.add_member(group_id, name)
    else:
        st.error("Give the new member a name.")
```

There is `is_valid_name` at `logic.py:42`, but no `is_valid_amount`. The validation function was simply never written.

*Second, weaker candidate:* `app.py:76`, `st.number_input("Amount (€)", step=0.01, format="%.2f")` has no `min_value`. A `min_value=0.01` would block the input in the widget. But `app.py:79` is the real answer: the widget only guards the user interface, while `logic.add_expense` (`logic.py:54`) still accepts anything it is handed — including from tests or from a later CSV import.

## Verify the AI

**7. "What happens to the balances when I delete a member who paid for an expense?" Was the AI right?**

*The AI's answer, written down before clicking:*

> `remove_member` (`logic.py:68`) only rewrites the `members` table and does not touch `expenses`. The expense keeps `payer_id = "8"` although member 8 no longer exists. On redraw, `show_expenses` (`app.py:105`) runs **before** `show_balances` (`app.py:106`), and `expense_rows` dies first at `logic.py:112` with a `KeyError`. So the balances are not wrong — they are never reached. The whole group page dies before that.

*What actually happened:* clicked **Remove** next to João in *Jantar de Curso*. The members list updated correctly (only Carolina and Mariana left), and below it the page went red:

```
KeyError: '8'
  app.py:118  main()
  app.py:113  show_group_page(...)
  app.py:105  show_expenses(group_id)
  app.py:65   rows = logic.expense_rows(group_id)
  logic.py:112  payer_name = names[expense["payer_id"]]
```

*Was the AI right?* Yes — but that is not the interesting part. The interesting part is that the obvious answer would have been wrong. Anyone answering without reading the code says "then the balances go wrong" or "the payer drops out of the calculation". Both are false: there are no balances any more. The question contains a hidden assumption ("the balances show something"), and the AI answer is only correct because it checked that assumption instead of adopting it.

Lesson for next time: don't ask "what happens", ask "show me the line where it happens". The traceback above is an answer nobody can argue with.

**8. Ask the AI to explain `compute_balances`. Find one thing it glossed over or got wrong.**

*How the function works* (`logic.py:85-100`): it opens an account at 0.00 for every member, walks through each expense of the group, works out what one person has to chip in (`share`), subtracts that from the members and credits the payer with the full amount. The result per member: positive means the group owes them, negative means they owe the group.

*The one thing that was glossed over:* the explanation treated the comment at `logic.py:94` as a specification instead of a claim. It read:

```python
# The payer already paid, so the bill is split between everybody else.
```

That sounds like a rule somebody decided on. It is actually the bug itself, written in prose. Anyone reading the comment reads the line below it as a correct implementation of a sensible rule — and an AI does this particularly reliably, because comments in its training data are usually true. **A comment is not a source. It is the opinion of somebody who is no longer here.**

The proof was visible on screen the whole time: in the same group the expenses table said **"Each €10.0"** and two centimetres below it the balances said **-15**. The app contradicted itself. The reason: `compute_shares` (`logic.py:77-82`) divides by `len(member_ids)` — it already contains the **correct** formula — while `compute_balances` divided by `len(members) - 1`. Two functions, same question, two answers.

*Two further things that were not mentioned, and that the fix does not solve either:*

- Past expenses are split among **today's** members. Verified: if a fourth person joins the group, they retroactively owe €7.50 for a dinner on 2026-08-25 they were not at (20/-10/-10 becomes 22.5/-7.5/-7.5/-7.5). This is none of the four reported bugs, but it is wrong.
- The cents still do not add up (`1613.1533333333339`). That is bug 003 and remains open.

**9. Bug #1 — reproduce, name the line, fix it.**

*Reproduced* in *Jantar de Curso* (3 members, João paid €30) — exactly the case from the issue:

| | João (8) | Carolina (9) | Mariana (10) |
|---|---:|---:|---:|
| **before** | 30 | -15 | -15 |
| **expected** | 20 | -10 | -10 |
| **after the fix** | 20 | -10 | -10 |

*The line:* `logic.py:95` — `share = amount / (len(members) - 1)`. Two accomplices belong to it: the `if` at `logic.py:97`, which excluded the payer from the split, and the misleading comment at `logic.py:94`.

*The fix:*

```python
# before
- # The payer already paid, so the bill is split between everybody else.
- share = amount / (len(members) - 1)
- for member in members:
-     if member["id"] != payer_id:
-         balances[member["id"]] -= share

# after
+ # Everybody shares the bill, the payer included: they ate too.
+ share = amount / len(members)
+ for member in members:
+     balances[member["id"]] -= share
```

The reasoning in one sentence: €30 divided by 3 is €10 each, **including João** — he ate too. He is credited his €30 but also pays his own €10, so he ends at +20. The sum of all accounts is now 0; before the fix it was not.

*Verified three ways:*

- `uv run pytest tests/test_bugs.py` → `test_bug_001` **green** (000, 002, 003 stay red on purpose, they are not part of this sheet)
- In the app, the balances now show `{"8": 20, "9": -10, "10": -10}`
- Side effect, checked separately: a group with **one** member used to crash with `ZeroDivisionError` (dividing by `1-1`). That crash is gone too.

**10. Three questions you'd ask the developer who left.**

1. **`compute_shares` divides by `len(members)`, `compute_balances` divided by `len(members) - 1`. Was that deliberate, or did one of them drift?** The most important question: two places meant to compute the same thing, doing it differently. Whichever was right, there should only ever have been one.
2. **What should happen when somebody who has already paid leaves the group?** The test at `tests/test_bugs.py:29` demands deleting their expenses too. But then €30 that was really paid disappears. Was that the decision, or is the test just the quickest way to stop the crash?
3. **Why does the "Add member" form validate its input and the "Add expense" form not at all?** There is `is_valid_name` (`logic.py:42`) but no `is_valid_amount`. Was it forgotten, or is there a reason to allow negative amounts (refunds)?

## Done when
- [x] All laptops run the app — individual work; the app runs with `uv run streamlit run app.py`
- [x] This file is answered (it lives in your folder — keep the folder, next week it becomes a repo)
- [ ] Bug #1 fixed and shown to the TA (before / after) — fixed and verified; still to be shown to the TA
