# solver round: round 5, skeptic

**Proxy score 45.6 / 100** (recommendation 2.9 of 35, instruction 7.0 of 7, asks 35.7 of 58). Main call missed. 2 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-34 (Session-sequence model) takes the Q1 2027 home carousel slot (4 Jan to 28 Mar 2027). It is worth 9.9 extra orders per 1,000 carousel sessions on the slot's traffic, which comes to about 25,700 extra orders and EUR 31,600 extra buyer-protection fee income (excl. VAT) over the twelve weeks. It clears all three launch conditions: logged-window lift 9.8 (at least 2.0 needed), worst cell app 0-29 at -0.96% against the -1.5% floor, and 13.9% of tiles going to fresh listings against the 12% commitment. The closest policy that also clears them is HC-37, at 5.7 per 1,000, so the gap is 4.2.

tokens matched 4 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 2 | 4 | 50% |
| carousel_slot_q1_2027.ipynb | 3 | 94 | 134 | 70% |
| carousel_slot_q1_2027.ipynb | 4 | 15 | 24 | 62% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 3 | 3 | 100% |
| carousel_slot_q1_2027_cells.png | 3 | 1 | 2 | 50% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Read the charter (lift at least 2.0, no cell more than 1.5% below incumbent HC-24 on carousel order rate, seller commitments met), the register (six registered policies, HC-24 is production), the fresh-listing commitment (12 of every 100 tiles under 48h, counted per served ranking), the slot gating note, the release calendar (code freeze; first app release on or after 4 Jan 2027 is 27.1 on 18 Jan), the tariff register and the terms.
2. Validated the estimator against the archive's logged_sessions. Session-weighted IPS on in_session_orders, sum(orders/propensity) by arm over N sessions (equal to the cell-stratified difference of means), lands within 0.25 of realised lift for all nine tests (T1 7.73 vs 7.9 ... T7 2.62 vs 2.5, T9 3.35 vs 3.2). Render-weighted replay and naive pooled means miss T2, T7, T8 and T9.
3. Built one row per logged session from render_seq=1 of the render log (150,400 sessions; constant ranker, propensity and tenure within each session) and banded tenure into the 8 charter cells. Propensities are constant per cell and ranker and quotas are exact. Joined served_rankings. ordered_tiles reconciles 1:1 with orders channel=carousel and home_session_id (9,957 orders).
4. Per-cell in-session carousel order rates against HC-24 (session-weighted). HC-31 web 730+ is -2.74%, a breach. HC-34 worst is app 0-29 at -0.96%, which passes. Render weighting would wrongly push HC-34 app 0-29 to -2.57%.
5. Fresh share per served ranking (tile_age_h<48 over 6 tiles per session): HC-36 8.8% fails, though it is 15.6% if counted per render. All others are 13.0-21.4%.
6. HC-33 tiles 1-2 are listings already on the buyer's watch list (53% and 22%). The same buyers' orders of watch-list listings in the 7 days after the session fall by 4.65 per 1,000, against exactly 0 for every other policy. Net HC-33 lift is 3.30 (in-session 7.96), so the outcome used is in-session carousel orders plus post-session watch-list orders within 7 days.
7. Fee method checked against the Q3 finance statement and reproduced exactly (e.g. July app 54,698 orders, EUR 945,884, EUR 70,729.59). Covered = captured payment, or shipped (balance) with no capture; unpaid pickup is not covered. Price = offer_eur when the order falls in [accepted_at, expires_at], otherwise asking price. Fee = tariff + 5% of price; income excl. VAT = fee/1.21. Repriced at the slot tariff of 0.80 (KB-2027-01 starts 5 Apr 2027, after the slot).
8. Slot traffic: R2 restatement (account-service tenure) for the same ISO weeks a year earlier, at 10% per platform. Web is 2026-W01..W12 and app 2026-W03..W12 because app release gating starts the app arm on 18 Jan. That gives 2,604,489 arm sessions. Lift = sum of cell diffs x slot sessions / total: HC-34 9.874, HC-37 5.679, HC-31 6.325 (fails), HC-33 3.271. Totals = cell diffs x slot sessions / 1000.

confidence: Medium-high. The winner HC-34 and its 9.9 are robust. The runner-up (HC-37 rather than HC-33) depends on netting out HC-33's watch-list displacement; without that, HC-33 would be runner-up at 8.0 with a gap of 1.9.

notes: Fee figures are buyer-protection fee income excl. 21% VAT at the 0.80 + 5% tariff. Lift is reported on the slot's traffic mix (9.9); the logged-window screen figure is 9.8. The 'gap' is given as 4.2 per 1,000 sessions, and as about 10,900 orders over the slot.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Chosen policy and lift: HC-34 Session-sequence model; +9.9 extra orders per 1,000 carousel sessions on the slot's traffic mix (logged-window offline screen lift 9.8)
- Runner-up that clears the launch conditions, and the gap: HC-37 Sequence ranker with fresh-listing interleave, +5.7 per 1,000; gap 4.2 extra orders per 1,000 carousel sessions (about 10,900 fewer extra orders over the slot: 25,700 vs 14,800)
- Fee income change per 1,000 carousel sessions, EUR excl. VAT, cells app 0-29 / app 30-179 / app 180-729 / app 730+ / web 0-29 / web 30-179 / web 180-729 / web 730+: HC-31: 9.1 / 9.0 / 8.1 / 7.1 / 10.7 / 6.9 / 9.9 / -1.8; HC-33: 4.7 / 9.6 / 3.7 / 3.1 / 1.8 / 5.7 / 1.0 / 2.0; HC-34: -1.2 / 13.7 / 14.1 / 14.8 / 7.4 / 12.9 / 9.3 / 13.7; HC-36: -7.0 / -12.3 / -11.9 / -14.6 / -8.1 / -10.9 / -12.8 / -15.8; HC-37: 7.4 / 9.1 / 8.2 / 5.0 / 6.7 / 10.0 / 7.6 / 4.5; HC-39: 5.0 / 1.6 / 1.5 / 1.0 / 1.6 / -2.3 / 0.6 / 1.3
- Twelve-week totals per policy: extra orders and extra fee income (EUR), to nearest hundred: HC-31: 16,500 orders, EUR 17,800; HC-33: 8,500 orders, EUR 10,200; HC-34: 25,700 orders, EUR 31,600; HC-36: 12,900 orders, EUR -32,900; HC-37: 14,800 orders, EUR 18,300; HC-39: 3,600 orders, EUR 3,100
- Launch-condition screen: HC-31 fails (b): web 730+ carousel order rate -2.7% vs HC-24. HC-36 fails (c): 8.8% fresh tiles per served ranking, under 12%. HC-39 fails (a): lift 1.4, under 2.0. HC-33 clears all three at a net lift of 3.3 (7.96 in-session minus 4.65 displaced watch-list orders). HC-34 and HC-37 clear all three.

### carousel_slot_q1_2027_cells.png (solver's answers)
- Grid coloured by fee change per 1,000 sessions: Same 6x8 fee grid as the notebook (policies down, cells across). Range runs from -15.8 (HC-36 web 730+) to +14.8 (HC-34 app 730+)
- Hatched guardrail breaches: One cell: HC-31 web 730+ (carousel order rate -2.74% vs incumbent). HC-34 app 0-29 at -0.96% is not hatched.
- Outlined row and title call: HC-34 row outlined. Title: HC-34 Session-sequence model takes the Q1 2027 slot, +9.9 orders per 1,000 carousel sessions
