# Removing a member breaks the whole group page

## What I did

In **Surf Trip Ericeira**, Francisco dropped out of the trip, so I clicked **Remove** next to his name.

## What I expected

Francisco disappears from the members list and the page carries on as normal. I was not sure what would happen to the things he paid for (the boards, the pastéis de nata...), but at least a page.

## What actually happened

The page went red with a long error message. Something about a `KeyError: '7'`. I can't open that group at all any more, not even to add the rest of the members back. The only way I found to get it working again was to run `uv run python seed.py`, which of course wiped everything else I had typed in.
