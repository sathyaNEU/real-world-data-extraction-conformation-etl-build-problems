# task121 · Q4 sprint call after the September checkout conversion fall

## Tags

**Domain:** Product Analytics (onboarding and activation: the checkout funnel of an online licensed-merchandise store).
**Analytical objective:** Root-Cause Analysis (attributing a correctly reported conversion fall to the customers it happened to, and naming the fix that removes the largest current cause).

## 1. Final Recommendation

**Give Q4's sprint to the one-time-code sign-in, which removes the loss from existing account holders who arrive from the club app's Shop tab without signing in.**

That cause cost 51 orders in the week of 21 to 27 September, 33 more than the card SDK upgrade's cause at 18. Not the postcode lookup, whose address-check loss drained to 10 as accounts re-saved their postcodes. Not the club landing page, whose genuinely new fans cost 2 when booked at the new-visitor rate both partner close-outs use. Not the card SDK upgrade, a real loss but the smaller one. Not split dispatch, whose mixed baskets converted at the same lower rate in August.

## 2. Critical Components

1. Club-app account holders lost **51** orders in the week of 21 to 27 September
2. Bankora and Finvo saved-card payments lost **18** orders that week
3. The address check's accounts lost **10** orders that week
4. Club-app new fans lost **2** orders that week

## 3. Step-by-Step Solution

1. Dropped the sessions in `edge_bot_verdicts_2026-07-27_2026-09-27.csv` from `basket_sessions_2026-07-27_2026-09-27.parquet` per `warehouse_field_reference.md` and cut Monday weeks: the call week is 21 to 27 September, the four weeks before the fall 3 to 30 August.
2. Followed each club-app session's `mpt` token through `cdm_token_billing_2026-08.csv` and `cdm_token_billing_2026-09.csv` to a member number and through `loyalty_profiles_2026-09-28.csv` to an account: most Shop-tab basket sessions belong to existing accounts.
3. Built each fix's customers as `q4_sprint_shortlist.docx` names them, with flag cohort, default saved address (UTC moved to Lisbon), default card and pre-order status each taken as of the session.
4. Sized each population against the same customers' August conversion per the shortlist's sizing line, new fans at the web new-visitor rate as both close-outs book them: sign-in 51 orders lost in the call week, card SDK 18, postcode lookup 10, club landing page 2.
5. Valued lost orders at the same customers' August net order value from `finance_order_export_2026-07-27_2026-09-27.csv` (latest export, one value per order, VAT out before 10 August) and counted challenges per `attempt_ref` with C and D in `tagus_3ds_log_2026-08-31_2026-09-27.csv`.
6. Recommendation: the one-time-code sign-in gets the sprint, 33 orders a week ahead of the card SDK upgrade.

## 4. Deliverable Answers

### q4_sprint_call.html
1. Fix: one-time-code sign-in at checkout
2. Cause it removes: existing account holders arriving from the club app's Shop tab without signing in
3. Orders a week that cause costs now (21 to 27 September): 51
4. Closest fix: card SDK upgrade with in-page 3-D Secure, 18 orders that week
5. Gap: 33 orders a week
6. Orders lost over the four weeks 31 August to 27 September:
   - Inline postcode lookup: 106
   - Club landing page: 8
   - Card SDK upgrade: 59
   - One-time-code sign-in: 161
   - Split dispatch: 9
7. Orders lost in the first week of the fall, 31 August to 6 September:
   - Inline postcode lookup: 43
   - Club landing page: 1
   - Card SDK upgrade: 5
   - One-time-code sign-in: 24
   - Split dispatch: 5
8. Sales lost in the week of 21 to 27 September, nearest €100:
   - Inline postcode lookup: €600
   - Club landing page: €100
   - Card SDK upgrade: €1,200
   - One-time-code sign-in: €3,600
   - Split dispatch: -€100
9. Share of card payment attempts that met a 3-D Secure challenge, 21 to 27 September:
   - Inline postcode lookup: 85.7%
   - Club landing page: 72.1%
   - Card SDK upgrade: 90.9%
   - One-time-code sign-in: 59.2%
   - Split dispatch: 34.9%
10. Chart below the grid: orders lost each week from the week of 3 August to the week of 21 September, one line per cause, the week of 21 September shaded and labelled as the week the call rests on, the one-time-code sign-in line labelled as the chosen fix at 51, and the call in the title.

### checkout_fall_workings.xlsx
1. Address check flag cohorts, signed-in basket sessions 31 August to 27 September and conversion:
   - Cohort 1: 4,472 sessions, 4.34%
   - Cohort 2: 4,583 sessions, 4.30%
   - Cohort 3: 4,710 sessions, 4.29%
   - Cohort 4: 4,361 sessions, 4.31%
   - Cohort 5: 4,723 sessions, 4.30%
   - Cohort 6: 5,655 sessions, 4.21%
   - Cohort 7: 4,461 sessions, 4.35%
   - Cohort 8: 4,080 sessions, 4.34%
   - Cohort 9: 4,621 sessions, 4.33%
   - Cohort 10: 4,688 sessions, 4.31%
   - Cohort 11: 4,641 sessions, 4.31%
   - Cohort 12: 4,530 sessions, 4.37%
