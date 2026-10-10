# CRM extracts: field notes

Data platform, member programme marts. Maintained by Francis Amrein. Last edited 11 September 2026.

These notes cover the extracts the data platform hands to programme analytics. Every file is UTF-8.
Card numbers and membership numbers are identifiers, not quantities: keep them as text (older cards
start with a zero).

## card_week_sales_2026w15_w34.parquet

One row per card and ISO week in which the card was presented at a till (at least one basket).
Weeks run Monday to Sunday. A card with no purchase in a week has no row for that week.

| Field | Meaning |
|---|---|
| card_no | 13-digit card number |
| iso_week | ISO week, `YYYY-Www` |
| week_start | Monday of the ISO week |
| baskets | baskets paid with the card in the week |
| gross_sales_chf | sales paid with the card, after till discounts and before reward cost, excluding VAT |
| gross_margin_chf | gross sales less cost of goods, at the week's standard cost |
| reward_cost_chf | points issued (CHF 0.01 a point) plus programme-funded vouchers and coupons booked in the week |

Facts are final for weeks closed before the extract; nothing in 2026-W15 to 2026-W34 is still open.

## st26_offer_allocation.csv

The offer engine's allocation register for the summer 2026 test (ST26), one row per card allocated.
`cell` is K, A, B, C or D as in the test catalogue. `bucket` is the engine's 0-99 bucket for the card.
`allocated_at` is the engine's timestamp (Europe/Zurich).

## member_cards.csv

One row per member card. `card_type` is main or additional; a membership has one main card and up to
three additional cards. `issued_on` is the date the current card number was issued (a reissued card
gets a new date, not a new number). `app_linked` says whether the card is linked to the Talwerk app.

## memberships.csv

One row per membership. `home_branch` is the branch the membership is administered at. `postcode`
and `canton` are the correspondence address. `share_certificates` is the number of co-operative
shares held.

## branch_footfall_2026w15_w34.csv

Door-counter visits by branch and ISO week, from the store systems. `door_count` counts entries
through the main door, members and non-members alike. `counter_status` is partial where a counter
dropped out for part of the week. Closed branches have no rows after their last trading week.

## branches_2026-01.csv

The branch register as issued in January 2026: number, name, town, region, format (S, M, L) and
area manager.
