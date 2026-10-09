# solver round: round 3, plain

**Proxy score 51.1 / 100** (recommendation 2.9 of 35, instruction 7.0 of 7, asks 41.3 of 58). Main call missed. 4 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-34 (Session-sequence model) should take the Q1 2027 home carousel slot. On the archive-validated session-weighted IPS screen it gives +9.8 extra orders per 1,000 carousel sessions against the incumbent HC-24 (Blend v7), and it clears all three launch conditions: its worst cell is app 0-29 at −0.96%, inside the −1.5% guardrail, and 13.9% of its tiles go to fresh listings. Over the twelve weeks it gives about 25,800 extra orders and €33,200 of extra buyer-protection fee income (excl. VAT). The closest compliant policy is HC-37 at 5.7, a gap of 4.1.

tokens matched 4 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 3 | 4 | 75% |
| carousel_slot_q1_2027.ipynb | 3 | 130 | 134 | 97% |
| carousel_slot_q1_2027.ipynb | 4 | 21 | 24 | 88% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 3 | 3 | 100% |
| carousel_slot_q1_2027_cells.png | 3 | 1 | 2 | 50% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Estimator check on carousel_experiment_archive.xlsx (logged_sessions): a session-weighted IPS rate per arm (Horvitz-Thompson, one count per session) lands within 0.25 of realised_lift for all nine tests T1-T9 (largest miss 0.17 on T1). The render-weighted replay misses badly (T7 5.15 vs 2.5), so session weights are the estimator the charter allows.
2. Logger window: the render log is cut to render_seq=1 (150,400 sessions, one ranker and propensity per session). Cells are platform by account-service buyer_tenure_days bands (0-29, 30-179, 180-729, 730+), and propensity is constant within each cell. Session orders come from ordered_tiles and match carousel orders by home_session_id exactly (9,957).
3. Lift on carousel orders against HC-24: HC-34 9.845, HC-33 7.957, HC-31 6.563, HC-37 5.697, HC-36 5.074, HC-39 1.389. Render-weighted, HC-31 would have led at 11.0.
4. Charter section 2.2 counts all orders by the arm's buyers. Joining all of each buyer's orders in the 7 days after session start (orders_enrolled_buyers) leaves every policy unchanged except HC-33. HC-33 pins watch-list listings on tiles 1 and 2 (53% and 22% of the time), so +45 favourites orders and −39 carousel orders net its lift down to 3.3.
5. Condition (b), each cell's carousel order rate against HC-24: HC-31 web 730+ is −2.74% and fails. All other policies' cells are within −1.5% (HC-34 app 0-29 −0.96%).
6. Condition (c), share of tiles under 48 hours old, counted once per served ranking (session), from the served_rankings tile ages: HC-24 13.0, HC-31 13.6, HC-33 14.1, HC-34 13.9, HC-36 8.84 (fails; 15.6 if counted by render), HC-37 21.4, HC-39 15.2.
7. Compliant policies: HC-34 9.8, HC-37 5.7, HC-33 3.3. Chosen policy HC-34; gap to HC-37 is 4.1.
8. Fee model checked against the payments file and finance_buyer_protection_fee_income_2026Q3.xlsx: covered orders are shipped orders plus pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee excl. VAT exactly. The fee is fixed + 5% of item price paid, where price paid is the accepted offer when the order falls in [accepted_at, expires_at], otherwise the asking price. Fee income = fee / 1.21. Tariff for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01 even though the tariff register lists it.
9. Slot traffic: 10% of R2-restated 2026-W01 to W12 sessions per cell. The app arm starts 18 Jan 2027 (release 27.1 after the code freeze), so app runs W03-W12 and web W01-W12, for 2,614,488 slot sessions. From 1 Mar 2027 (W09-W12) every pickup order is paid at checkout and carries the fee; before that a pickup carries it only if it was paid at checkout.
10. Per-cell fee change = session-weighted blend of the pre-March and post-March IPS differences against HC-24. Totals = per-cell differences × planned slot sessions / 1,000. HC-34: 25,810 orders and EUR 33,222, rounded to 25,800 and EUR 33,200.

confidence: medium-high

notes: Rates are weighted by the logged-window cell mix. Weighting by the slot's traffic mix instead gives HC-34 9.87 (9.9) and a gap of 4.18 (4.2); the call itself does not change. HC-33's displacement is netted with a 7-day all-channel order window; 7 and 14 days give the same result.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Opening answer: chosen policy and its lift: HC-34 Session-sequence model: +9.8 extra orders per 1,000 carousel sessions against the incumbent HC-24 (session-weighted IPS on the 22 Jun to 20 Sep 2026 logged window; unrounded 9.845).
- Closest policy that still clears the launch conditions, and the gap: HC-37 (Sequence ranker with fresh-listing interleave) at +5.7 per 1,000 sessions. Gap to HC-34: 4.1 orders per 1,000 carousel sessions. Screened out: HC-31 (lift 6.6, but its web 730+ carousel order rate is −2.7%, beyond the 1.5% guardrail). HC-33 (all-channel lift is only 3.3 once orders it takes from favourites are netted out; the carousel-only figure of 8.0 counts orders that would have happened anyway). HC-36 (8.8% fresh tiles per served ranking, below the 12% commitment; counting by render gives a misleading 15.6%). HC-39 (lift 1.4, below 2.0).
- Change in buyer-protection fee income per 1,000 carousel sessions while the slot runs, EUR excl. VAT, by policy and cell (app 0-29 / app 30-179 / app 180-729 / app 730+ / web 0-29 / web 30-179 / web 180-729 / web 730+): HC-31: 9.4 / 9.7 / 9.1 / 8.3 / 10.8 / 7.7 / 10.3 / -1.6. HC-33: 4.5 / 9.4 / 3.2 / 3.2 / 1.9 / 6.6 / 1.2 / 2.1. HC-34: -0.8 / 14.2 / 14.6 / 15.2 / 8.1 / 13.1 / 10.5 / 14.5. HC-36: -1.6 / -3.9 / -4.1 / -5.8 / -4.6 / -4.8 / -6.5 / -9.0. HC-37: 7.8 / 9.3 / 7.8 / 6.0 / 6.6 / 9.9 / 7.7 / 5.2. HC-39: 4.6 / 1.9 / 1.9 / 0.7 / 0.8 / -1.4 / 1.0 / 1.8.
- Twelve-week totals per policy: extra orders and extra fee income (EUR, nearest hundred): HC-34: 25,800 orders, EUR 33,200. HC-31: 16,600 orders, EUR 19,800. HC-33: 8,600 orders, EUR 10,300. HC-36: 13,000 orders, EUR -14,000. HC-37: 14,900 orders, EUR 19,200. HC-39: 3,600 orders, EUR 3,500.

### carousel_slot_q1_2027_cells.png (solver's answers)
- Grid: 6 policies down, 8 cells across, coloured by the fee figure: Same fee grid as the notebook, colour range about EUR -9.0 (HC-36 web 730+) to +15.2 (HC-34 app 730+) per 1,000 carousel sessions.
- Hatched guardrail-breach cells: One cell: HC-31 web 730+ (carousel order rate −2.74% against HC-24). HC-34 app 0-29 at −0.96% is within the limit and is not hatched.
- Outlined row and title call: HC-34 row outlined. Title: HC-34 Session-sequence model takes the Q1 2027 slot, +9.8 orders per 1,000 carousel sessions, about 25,800 extra orders and EUR 33,200 extra fee income over 12 weeks.
