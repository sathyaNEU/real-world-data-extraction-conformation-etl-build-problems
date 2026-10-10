# solver round: round 2, plain

**Proxy score 89.5 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 47.5 of 58). Main call LANDED. 10 of 11 ask items cracked (80 per cent of tokens).

## Main call

golden: Give Q4's sprint to the one-time-code sign-in, which removes the loss from existing account holders who arrive from the club app's Shop tab without signing in.

solver: Give Q4's sprint to fix 4, the one-time-code sign-in at checkout (Jaime Jesus). The cause it removes is CD Monteralto members who were already customers. Since the SOCIO website code ended on 30 August, they arrive from the club app's Shop tab signed out, in a cookie-less in-app browser, and convert at 1.3% against the 4.6% those same accounts converted at in 3-30 August. In the week of 21-27 September that cost 51 orders (about EUR 3,700). The next closest is fix 3, the card SDK upgrade for Bankora/Finvo saved-card challenges, at 18 orders a week (about EUR 1,200), a gap of 33 orders a week. Duarte's address check is down to 10 orders a week. The club landing page (2) and split dispatch (-1) cost next to nothing.

tokens matched 2 of 2 (Give, Shop)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| q4_sprint_call.html | 1 | 0 | 0 | 0% |
| q4_sprint_call.html | 2 | 2 | 2 | 100% |
| q4_sprint_call.html | 3 | 4 | 5 | 80% |
| q4_sprint_call.html | 4 | 4 | 4 | 100% |
| q4_sprint_call.html | 5 | 1 | 1 | 100% |
| q4_sprint_call.html | 6 | 12 | 14 | 86% |
| q4_sprint_call.html | 7 | 11 | 13 | 85% |
| q4_sprint_call.html | 8 | 12 | 14 | 86% |
| q4_sprint_call.html | 9 | 13 | 15 | 87% |
| q4_sprint_call.html | 10 | 5 | 6 | 83% |
| checkout_fall_workings.xlsx | 1 | 38 | 40 | 95% |

## Solver's path

1. Read prompt.md, the shortlist docx and the field reference. Method from the shortlist: for each cause, take its customers' sessions in a week, multiply by those same customers' conversion over 3-30 Aug, and subtract their actual orders. Value each lost order at those customers' pre-fall average order value. The fall began in the week of 31 Aug; the call rests on the latest complete week, 21-27 Sep.
2. basket_sessions parquet (214,465) minus edge_bot_verdicts (732 bot basket sessions: 304 club_app in the week of 31 Aug, 428 in the week of 14 Sep, all with no orders), giving 213,733. Weeks are Monday to Sunday. The dashboard still counts the bots in those two weeks.
3. Finance export: kept the latest export per order (the 17 Aug re-export changed 412 orders). Divided totals on rows exported before 10 Aug by 1.23 to make everything net of VAT. Took one total per order rather than per shipment row. Every session order matched.
4. Address check: default address from address_book_history (changed_at is UTC, so +1h). A postcode that is not nnnn-nnn counts as rejected. Flag status from the checkout_flags_export cohorts, with the assignment_moves walked back to the session time and checked against the enabled_at waves. Affected sessions numbered 1,132, 1,021, 392 and 218 over the four weeks; the week of 21-27 Sep had 0 orders. Baseline 4.60% from those accounts' sessions in 3-30 Aug. Lost: 43, 38, 15, 10, total 106.
5. Card SDK: default saved card at session time, from saved_cards with the 141 set_default events walked back (Bankora/Finvo holders moving to other banks). Issuer Bankora/Finvo, signed in: 1,460 sessions and 49 orders in the week of 21-27 Sep against a 4.59% baseline, so 18 lost. Four weeks: 59.
6. Club app: the mpt token goes to cdm_token_billing member_no, then to an account through the SOCIO+7-digit codes in promo_redemptions (leading zero stripped) and the loyalty club_member_no. 4,884 of 7,953 non-bot club_app sessions are existing accounts. All club_app sessions are signed out and marked new visitor. Week of 21-27 Sep: 1,568 sessions and 21 orders against those accounts' 4.61% pre-fall rate, so 51 lost (4 weeks: 161). This is the sign-in gap that the one-time-code sign-in removes. Unknown members (929 sessions, 11 orders) set against the 1.40% pre-fall new-visitor rate give 2 lost, which is real dilution for the landing page.
7. Split dispatch: pre-order status at session time from catalogue_status_history (K3 pre-order 31 Aug-20 Sep, JKT from 15 Sep, CE-ORION, VBX). Mixed baskets have a 1.90% baseline; week of 21-27 Sep: 1,950 sessions and 38 orders, so -1 (4 weeks: 9).
8. 3DS: tagus log deduplicated on attempt_ref (7,420 to 7,309, matching the Tagus PDF), joined to the cohorts by session_id. Challenge share in the week of 21-27 Sep, C+D over attempts, by cohort.
9. Workbook: signed-in non-bot sessions 31 Aug-27 Sep grouped by cohort at session time; orders over sessions.

confidence: medium-high: the ranking (51 vs 18 vs 10 a week) holds under every baseline variant I tried. Some cells could move by one depending on the convention: the address four-week figure is 106 or 107 depending on whether the baseline customer set is the four-week cohort or the 21-27 Sep cohort.

notes: Split dispatch comes out slightly negative in the week of 21-27 Sep (-1 order, -EUR 100); I reported it as computed rather than floored at zero. The challenge shares are within each cohort's own attempts. Euros are net of VAT.

### q4_sprint_call.html (solver's answers)
- Chosen fix, cause removed, orders a week it costs now: Fix 4, one-time-code sign-in at checkout. Cause: existing customers who are club members land signed out from the Monteralto+ Shop tab (in-app browser, no store cookie, so no saved address or card). Their tokens map through the member number to existing accounts via the 2025/26 SOCIO codes and the loyalty club_member_no. Cost: 51 orders a week in the week of 21-27 Sep 2026 (1,568 basket sessions, 21 orders, against a 4.61% baseline).
- Closest fix and gap: Fix 3, card SDK upgrade with in-page 3-D Secure: 18 orders lost in the week of 21-27 Sep. Gap to fix 4 is 33 orders a week (sales gap about EUR 2,500).
- Orders lost over the four weeks since the fall (31 Aug-27 Sep): Postcode lookup 106; club landing page 8; card SDK upgrade 59; one-time-code sign-in 161; split dispatch 9
- Orders lost in the fall's first week (31 Aug-6 Sep): Postcode lookup 43; club landing page 1; card SDK upgrade 5; one-time-code sign-in 24; split dispatch 5
- Sales lost in the week of the call (21-27 Sep), EUR to nearest 100, net of VAT: Postcode lookup EUR 600 (10 orders x EUR 59.95); club landing page EUR 100 (2 x EUR 46.50); card SDK upgrade EUR 1,200 (18 x EUR 66.53); one-time-code sign-in EUR 3,700 (51 x EUR 72.37); split dispatch -EUR 100 (-1 x EUR 93.40, so no loss)
- Share of the week's (21-27 Sep) card payment attempts that met a 3-D Secure challenge (C or D), 1 dp: Postcode lookup 85.7% (6 of 7); club landing page 72.1% (31 of 43); card SDK upgrade 90.9% (150 of 165); one-time-code sign-in 59.2% (45 of 76); split dispatch 34.9% (30 of 86). Whole store 42.7% (786 of 1,841), which matches the Tagus report.
- Chart: orders lost each week since the start of August, one line per cause: Weeks starting 3 Aug, 10 Aug, 17 Aug, 24 Aug, 31 Aug, 7 Sep, 14 Sep, 21 Sep. Address check (postcode lookup): 0,0,0,0,43,38,15,10. Club new fans (landing page): 0,0,0,0,1,3,2,2. Bankora/Finvo saved-card challenges (SDK): 0,0,0,0,5,19,17,18. Members signed out from the club app (one-time-code sign-in): 0,0,0,0,24,39,47,51. Mixed pre-order baskets (split dispatch): 0,0,0,0,5,9,-4,-1. The week of 21 Sep is marked and one-time-code sign-in is labelled. Title: 'One-time-code sign-in gets the Q4 sprint: signed-out club members cost 51 orders in the week of 21 Sep'.

### checkout_fall_workings.xlsx (solver's answers)
- Each address-check flag cohort: signed-in basket sessions 31 Aug-27 Sep (bots excluded, cohort as at the session after the assignment moves) and conversion to 2 dp: Cohort 1: 4,505 sessions, 195 orders, 4.33%. Cohort 2: 4,547, 195, 4.29%. Cohort 3: 4,722, 204, 4.32%. Cohort 4: 4,358, 187, 4.29%. Cohort 5: 4,721, 202, 4.28%. Cohort 6: 5,659, 240, 4.24%. Cohort 7: 4,433, 191, 4.31%. Cohort 8: 4,107, 179, 4.36%. Cohort 9: 4,643, 202, 4.35%. Cohort 10: 4,675, 201, 4.30%. Cohort 11: 4,637, 197, 4.25%. Cohort 12: 4,526, 200, 4.42%. Total 55,533 sessions, 2,393 orders.
