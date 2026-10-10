# solver round: round 1, plain

**Proxy score 86.1 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 44.1 of 58). Main call LANDED. 6 of 11 ask items cracked (80 per cent of tokens).

## Main call

golden: Give Q4's sprint to the one-time-code sign-in, which removes the loss from existing account holders who arrive from the club app's Shop tab without signing in.

solver: Give Q4's sprint to fix 4, the one-time-code sign-in at checkout. The cause it removes is club members who already have store accounts arriving from the Monteralto+ Shop tab without being signed in: 1,568 basket sessions in the week of 21 Sep produced 21 orders, against the 4.61% those same accounts converted at in August. That costs about 51 orders a week (about €3,700). The closest fix is the card SDK upgrade, where Bankora and Finvo default-card holders lose about 18 orders a week, a gap of 33 orders a week. Duarte's postcode lookup is now down to about 10 orders a week.

tokens matched 2 of 2 (Give, Shop)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| q4_sprint_call.html | 1 | 0 | 0 | 0% |
| q4_sprint_call.html | 2 | 2 | 2 | 100% |
| q4_sprint_call.html | 3 | 4 | 5 | 80% |
| q4_sprint_call.html | 4 | 3 | 4 | 75% |
| q4_sprint_call.html | 5 | 1 | 1 | 100% |
| q4_sprint_call.html | 6 | 12 | 14 | 86% |
| q4_sprint_call.html | 7 | 10 | 13 | 77% |
| q4_sprint_call.html | 8 | 11 | 14 | 79% |
| q4_sprint_call.html | 9 | 13 | 15 | 87% |
| q4_sprint_call.html | 10 | 5 | 6 | 83% |
| checkout_fall_workings.xlsx | 1 | 28 | 40 | 70% |

## Solver's path

1. Followed the shortlist docx's rule. 'Now' is the week of 21-27 Sep 2026. The baseline is the same customers over 3-30 Aug, and lost orders are valued at those customers' August average order value. The fall starts in the week of 31 Aug (Tagus weeks 36-39, dashboard conversion 3.61% falling to 3.20%).
2. Basket sessions parquet minus the 732 basket sessions the edge bot file flags (304 club-app sessions on 31 Aug to 1 Sep, 428 gift-card sessions on 16-18 Sep). This reproduces the dashboard weekly sessions and orders exactly.
3. Finance export: kept the latest export per order (the 17 Aug re-export supersedes 412 orders), took one row per order rather than per shipment, and divided rows exported before 10 Aug by 1.23 to make them net. Joined on order_id to give order values.
4. Fix 1: took each account's default address at session start from address_book_history (UTC plus 1h converted to Lisbon). Cohort at session time comes from the flags JSON, using from_cohort before the 14 Sep moves, and the rollout times set when the flag was on. Sessions with the flag on and a 4-digit postcode: 1,132, 1,021, 392, 218 by week. Most accounts fixed their postcode in September, so 218 sessions with 0 orders in the latest week against a 4.62% baseline gives 10 lost.
5. Fix 4 and fix 2: took the mpt token from the club_app landing URLs and joined token to member_no (club token reports) to club_member_no (loyalty_profiles) to account. That maps 61% of club-app sessions to existing accounts, confirmed 290 of 290 by address_fp against the address book. The mapped members, not signed in, ran 1,568 sessions and 21 orders in the latest week against their August 4.605%, so 51.2 lost, valued at EUR 71.39 an order. The unmapped club-app sessions (the real new fans) convert at 1.18% against an August new-visitor rate of 1.40%, so about 2 lost.
6. Fix 3: rebuilt each account's default card at session time from the saved_cards snapshot plus 141 September set_default events that moved accounts off Bankora or Finvo. Bankora/Finvo default sessions: 1,460 sessions and 49 orders in the latest week against 4.60%, so 18.1 lost at EUR 66.47 an order.
7. Fix 5: took SKU status at session time from catalogue_status_history (Orion collector's edition, Lumen vinyl box, K3 from 31 Aug to 20 Sep, jacket from 15 Sep). Mixed baskets converted at 1.90% in August and 1.95% in the latest week (1,950 sessions, 38 orders), so -1. It is a steady structural slice, not a cause of the fall.
8. Challenge share: deduplicated the Tagus log to 7,309 attempts, which matches the PDF weekly totals. Took latest-week attempts by sent_at and counted C or D statuses per cohort via session_id: 7 attempts at 85.7%, 43 at 72.1%, 165 at 90.9%, 76 at 59.2%, 86 at 34.9%.
9. Workings: grouped signed-in non-bot sessions from 31 Aug to 27 Sep by cohort at session time. Conversion is flat across cohorts (4.21% to 4.37%) whatever their enable date, so the address check no longer separates them.

confidence: Medium-high on the call and the 51-against-18 ranking. Medium on the fix 2 and fix 5 cells, whose baselines are judgement calls (new visitors, and mixed baskets then against now).

notes: The files left open how to give fix 2 (genuinely new fans, who have no August history of their own) and fix 5 a 'same customers' baseline. I used the August new-visitor rate and the August mixed-basket rate, which gives near-zero and slightly negative losses. Sales were valued with unrounded lost orders: 51.2 x EUR 71.39 = EUR 3,655, which rounds to EUR 3,700. Using the rounded 51 orders would give EUR 3,600.

### q4_sprint_call.html (solver's answers)
- Chosen fix and the cause it removes: Fix 4, one-time-code sign-in at checkout. The cause is existing account holders (club members) who arrive through the club app's Shop tab not signed in and check out as guests.
- Orders a week the chosen cause costs now (week of 21-27 Sep 2026): 51 orders (1,568 sessions x 4.61% baseline = 72.2 expected, 21 actual, so 51.2 lost)
- Runner-up fix and gap: Fix 3, the card SDK upgrade with in-page 3-D Secure, at 18 orders a week. Gap: 33 orders a week.
- Fix 1 postcode lookup: orders lost over the four weeks from 31 Aug to 27 Sep / in the first week / sales lost in the week of 21 Sep / 3DS challenge share that week: 106 orders / 43 orders / EUR 600 / 85.7%
- Fix 2 club landing page (club-app fans with no account): four-week lost / first-week lost / sales lost in the week of 21 Sep / challenge share: 8 orders / 1 order / EUR 100 / 72.1%
- Fix 3 card SDK upgrade (Bankora/Finvo default card): four-week lost / first-week lost / sales lost in the week of 21 Sep / challenge share: 59 orders / 5 orders / EUR 1,200 / 90.9%
- Fix 4 one-time-code sign-in (club members not signed in): four-week lost / first-week lost / sales lost in the week of 21 Sep / challenge share: 161 orders / 24 orders / EUR 3,700 / 59.2%
- Fix 5 split dispatch (baskets mixing pre-order and in-stock lines): four-week lost / first-week lost / sales lost in the week of 21 Sep / challenge share: 9 orders / 5 orders / EUR -100 (-1 order, so effectively nothing lost) / 34.9%
- Chart: weekly orders lost by cause from 3 Aug: Sign-in (fix 4): 0,0,0,0 then 24, 39, 47, 51. Card (fix 3): about 0 through August, then 5, 19, 17, 18. Address (fix 1): 0 through August, then 43, 38, 15, 10. Club new fans (fix 2): 1, 3, 2, 2. Split dispatch (fix 5): 5, 9, -4, -1. The week of 21 Sep is marked, fix 4 is labelled, and the title carries the one-time-code sign-in call.

### checkout_fall_workings.xlsx (solver's answers)
- Each flag cohort's basket sessions over 31 Aug to 27 Sep and conversion (signed-in, bot-excluded, cohort as at the session): C1 4,472 sessions, 4.34%. C2 4,583, 4.30%. C3 4,710, 4.29%. C4 4,361, 4.31%. C5 4,723, 4.30%. C6 5,655, 4.21%. C7 4,461, 4.35%. C8 4,080, 4.34%. C9 4,621, 4.33%. C10 4,688, 4.31%. C11 4,641, 4.31%. C12 4,530, 4.37%. Total 55,525 sessions, 2,393 orders, 4.31%.
