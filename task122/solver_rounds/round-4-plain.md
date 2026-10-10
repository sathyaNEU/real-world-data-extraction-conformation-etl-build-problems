# solver round: round 4, plain

**Proxy score 46.8 / 100** (recommendation 3.6 of 35, instruction 7.0 of 7, asks 36.2 of 58). Main call missed. 2 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-34 (Session-sequence model) should take the Q1 2027 home carousel slot (4 Jan to 28 Mar 2027). Against the incumbent HC-24 Blend v7 it adds 9.8 orders per 1,000 carousel sessions on the archive-validated session-weighted screen. It clears all three launch conditions: its worst cell is app 0-29 at -0.96% (inside the 1.5% guardrail) and 13.9% of its served tiles are fresh listings (the floor is 12%). The policy that comes closest while also clearing the conditions is HC-37 at 5.7, a gap of 4.1. Over the twelve weeks HC-34 gives about 25,700 extra orders and about €31,600 extra buyer-protection fee income (excluding VAT).

tokens matched 5 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 3 | 4 | 75% |
| carousel_slot_q1_2027.ipynb | 3 | 70 | 134 | 52% |
| carousel_slot_q1_2027.ipynb | 4 | 15 | 24 | 62% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 3 | 3 | 100% |
| carousel_slot_q1_2027_cells.png | 3 | 1 | 2 | 50% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Read the charter (lift and guardrail definitions, launch conditions a/b/c, estimator rule 5.2), the policy register (incumbent HC-24 in production, six registered challengers), the slot and gating notes, the release calendar, the tariff register and the fresh-listing commitment.
2. Checked candidate estimators against all nine tests in carousel_experiment_archive.xlsx logged_sessions. Session-weighted IPS (orders/propensity summed over sessions, compared with control) matched realised lift within 0.25 on every test (for example T7 2.62 vs 2.5, T9 3.35 vs 3.2). Render-weighted replay missed (T7 5.21, T2 5.1), and so did naive means (T8 7.71).
3. Built a session table from the first render of each session in the render log (150,400 sessions, one ranker and one propensity per session), joined to served_rankings. Cells are platform x buyer_tenure_days bands (0-29, 30-179, 180-729, 730+). The outcome is in-session carousel orders from ordered_tiles, which matches the orders file exactly (9,957 orders linked by home_session_id). Allocation quotas are exact, so IPS equals the cell-share-weighted difference of per-cell means.
4. Lift against HC-24: HC-34 9.845, HC-33 7.957, HC-31 6.563, HC-37 5.697, HC-36 5.074, HC-39 1.389. Condition (a) knocks out HC-39.
5. Condition (b), the per-cell carousel order rate against the incumbent: HC-31 fails in web 730+ (-2.74%). HC-34's worst cell is app 0-29 at -0.96%, which passes. Every other policy is above the incumbent in every cell.
6. Condition (c), share of fresh tiles (<48h old) counted once per served ranking (session): HC-24 13.0, HC-31 13.6, HC-33 14.1, HC-34 13.9, HC-36 8.8 (fails; counting per render would wrongly give 15.6), HC-37 21.4, HC-39 15.2.
7. HC-33 pins watchlist items on tiles 1-2. In every other arm exactly 62.5% of watchlisted items are bought anyway; for HC-33's pinned items the figure is 62.86%, so only 45 of its 120 in-session watchlist orders are incremental. Its net lift is 3.30 (an all-channel 7-day check also gives 3.3). It still clears the conditions but ranks below HC-37, so HC-37 is the runner-up and the gap is 9.845 - 5.697 = 4.1.
8. Fee per order: covered orders are all card/iDEAL captures plus unpaid shipped orders paid from balance. This reconciles exactly to the finance Q3 sheet (July app 51,036 + 3,662 = 54,698 orders; item value EUR 945,884; fee excl. VAT 70,729.59). Unpaid pickup orders are paid directly to the seller and carry no fee. Item price is the accepted offer price if the order falls between accepted_at and expires_at, otherwise the asking price. The Q1 tariff is KB-2026-02 (EUR 0.80 + 5%), because KB-2027-01 starts 5 Apr 2027 and has no decision recorded. The fee is divided by 1.21 to remove VAT, then I took the per-cell difference per 1,000 sessions against HC-24.
9. Q1 traffic: R2 restatement (account-service tenure) for 2026-W01 to W12, the same ISO weeks as 2027-W01 to W12. Web runs all 12 weeks; the app arm runs only W03 to W12, because the first app release on or after 4 Jan is 27.1 on 18 Jan after the code freeze. Each platform takes a 10% share. Totals are the sum over cells of the per-cell delta x test sessions / 1,000. HC-34 comes to 25,716 orders and EUR 31,611.

confidence: medium-high on the call (HC-34, 9.8) and on HC-37 as runner-up; medium on HC-33's net figures and on whether the headline should be the screen lift (9.8) or the Q1-mix-weighted rate (9.9)

notes: The headline is the logged-window screen lift, 9.8. Weighted to the Q1 traffic mix (app arm starting 18 Jan) it is 9.9. HC-33's grid row and totals are net of the watchlist orders that would have happened anyway (62.5% of them); without that adjustment its fee row would be 4.7, 9.6, 10.3, 13.2, 1.8, 5.7, 7.4, 14.3 and its totals 20,800 orders and EUR 25,800. Fee figures exclude VAT; including VAT they would be 1.21 times higher.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Chosen policy and extra orders per 1,000 carousel sessions: HC-34 Session-sequence model; lift 9.8 extra orders per 1,000 carousel sessions vs HC-24 (screen estimate 9.845; weighted to the Q1 traffic mix it is 9.874)
- Closest policy that still clears the launch conditions, and the gap: HC-37 Sequence ranker with fresh-listing interleave, lift 5.7 per 1,000 sessions; gap to HC-34 = 4.1 orders per 1,000 carousel sessions
- Policies that fail the launch conditions: HC-31 fails (b): web 730+ carousel order rate is 2.7% below incumbent (54.95 vs 56.49 per 1,000). HC-36 fails (c): 8.8% fresh tiles counted per served ranking (it looks like 15.6% only if counted per render). HC-39 fails (a): lift 1.4. HC-33 passes but its net lift is only 3.3 (raw 8.0), because 62.5% of its watchlist tiles on positions 1-2 would have been bought through favourites or alerts anyway
- Change in buyer-protection fee income per 1,000 carousel sessions, EUR excl. VAT, by policy x cell (app 0-29, app 30-179, app 180-729, app 730+, web 0-29, web 30-179, web 180-729, web 730+): HC-31: 9.1, 9.0, 8.1, 7.1, 10.7, 6.9, 9.9, -1.8 | HC-33 (net of displaced watchlist orders): 4.7, 9.6, 3.7, 3.1, 1.8, 5.7, 1.0, 2.0 | HC-34: -1.2, 13.7, 14.1, 14.8, 7.4, 12.9, 9.3, 13.7 | HC-36: -7.0, -12.3, -11.9, -14.6, -8.1, -10.9, -12.8, -15.8 | HC-37: 7.4, 9.1, 8.2, 5.0, 6.7, 10.0, 7.6, 4.5 | HC-39: 5.0, 1.6, 1.5, 1.0, 1.6, -2.3, 0.6, 1.3
- Twelve-week totals per policy: extra orders and extra fee income (EUR), nearest hundred: HC-34: 25,700 orders, EUR 31,600 | HC-31: 16,500 orders, EUR 17,800 | HC-33: 8,500 orders, EUR 10,200 (net; raw in-session 20,800 orders, EUR 25,800) | HC-36: 12,900 orders, EUR -32,900 | HC-37: 14,800 orders, EUR 18,300 | HC-39: 3,600 orders, EUR 3,100

### carousel_slot_q1_2027_cells.png (solver's answers)
- Grid: policies down, 8 cells across, coloured by fee change per 1,000 sessions: Same fee grid as in the notebook; scale runs from about -15.8 (HC-36 web 730+) to +14.8 (HC-34 app 730+)
- Hatched guardrail-breach cells: Only one cell: HC-31 x web 730+ (-2.7% vs incumbent carousel order rate). HC-34 app 0-29 is -0.96%, inside the 1.5% limit, so it is not hatched
- Outlined row and title call: HC-34 row outlined; title: HC-34 Session-sequence model takes the Q1 2027 slot, +9.8 orders per 1,000 carousel sessions
