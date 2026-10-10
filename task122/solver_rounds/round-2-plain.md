# solver round: round 2, plain

**Proxy score 48.7 / 100** (recommendation 2.9 of 35, instruction 7.0 of 7, asks 38.9 of 58). Main call missed. 3 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-34 (Session-sequence model) should take the home carousel's Q1 2027 test slot (4 Jan to 28 Mar 2027). It gives +9.8 extra orders per 1,000 carousel sessions against the incumbent HC-24 Blend v7. It is the only top candidate that clears all three launch conditions with the largest lift. The next eligible policy is HC-37, the sequence ranker with fresh-listing interleave, at +5.7, so the gap is 4.1 orders per 1,000 sessions. Over the slot's 2,661,486 arm sessions, HC-34 adds about 26,100 orders and about EUR 32,100 of buyer-protection fee income (excluding VAT).

tokens matched 4 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 3 | 4 | 75% |
| carousel_slot_q1_2027.ipynb | 3 | 130 | 134 | 97% |
| carousel_slot_q1_2027.ipynb | 4 | 21 | 24 | 88% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 2 | 3 | 67% |
| carousel_slot_q1_2027_cells.png | 3 | 1 | 2 | 50% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Read the charter's launch conditions: lift >= 2.0; no cell with a carousel order rate more than 1.5% below the incumbent; the seller commitments. HC-24 Blend v7 is production, so it is the incumbent and six registered policies are candidates.
2. Tested estimators on carousel_experiment_archive.xlsx. A session-weighted inverse-propensity estimate of in_session_orders lands within 0.25 of every realised lift (e.g. T7 2.62 vs 2.5, T9 3.35 vs 3.2). The render-weighted replay misses (T7 5.21).
3. Built one row per session from the render log (render_seq 1) joined to served_rankings, 150,400 sessions. Assigned the charter's 8 cells from buyer_tenure_days (account service). Each ranker fills its cell quota exactly, so cell-stratified IPS equals the per-cell mean.
4. Fresh-listing commitment, counted per served ranking (session): HC-36 has 8.8% of tiles under 48 hours, below 12%, so it fails. Render-weighting would wrongly show 15.6%. All other policies are at 13.6% or more.
5. Guardrail on the in-session carousel order rate: the only breach is HC-31 in web 730+ (54.95 vs 56.49 per 1,000, -2.7%).
6. Lift as defined (all orders by the arm's buyers): counted every order by each buyer in the 7 days from session start, all channels, from the orders parquet. This equals in-session carousel lift for every policy except HC-33. HC-33 pins watch-list listings on tiles 1-2, which pulls forward orders that would otherwise come through favourites. Its lift falls from 7.96 to 3.30. The 0-7 day and 0-14 day results are identical.
7. Fee per order: tariff of 1 Sep 2026 (EUR 0.80 + 5% of item price paid). KB-2027-01 was deferred by the 6 Oct pricing committee. Price paid is the accepted offer when the order falls inside the offer window. Covered orders are all shipped orders plus pickup orders captured in payments; uncaptured pickups were paid directly and carry no fee. Fee income is taken excl. 21% VAT. This reconciles exactly to the Finance Q3 sheet (the 6,147 July shipped orders missing from payments supply EUR 8,205.17).
8. Per-cell change in fee per 1,000 sessions: IPS difference of the 7-day fee income against HC-24.
9. Slot traffic: R2 restatement (merged-account tenure), 10% of sessions. Web uses 2026-W01 to W12; app uses W03 to W12 because the first app release on or after 4 Jan 2027 is 27.1 on 18 Jan. That gives 2,661,486 arm sessions. Totals are cell lift times sessions: HC-34 26,124 orders and EUR 32,114; HC-37 15,213 orders and EUR 18,788. Slot-mix lift is HC-34 9.82 vs HC-37 5.72, a gap of 4.1.

confidence: Medium-high: the choice of HC-34 holds under every basis I tested. The figures most open to interpretation are HC-33's lift (it depends on counting displaced favourites orders over 7 days) and the fee basis (excl. VAT).

notes: If the headline lift is read on the logged-window mix instead of slot traffic it is 9.84 vs 5.70, which still rounds to 9.8 and a 4.1 gap. If the fee is reported including VAT, every fee figure scales by 1.21. The HC-36 fee change is negative because its extra pickup orders are paid directly and carry no buyer-protection fee.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Opening answer: the winning policy and its lift: HC-34 Session-sequence model; lift +9.8 extra orders per 1,000 carousel sessions (slot traffic mix 9.82; logged-window mix 9.84)
- Closest policy that still clears the launch conditions, and the gap: HC-37 Sequence ranker with fresh-listing interleave, lift +5.7 per 1,000 sessions; gap to HC-34 = 4.1 extra orders per 1,000 carousel sessions
- Launch-condition screen (lift, guardrail, fresh-listing share): Lift per 1,000 (slot mix): HC-31 6.3, HC-33 3.3, HC-34 9.8, HC-36 5.0, HC-37 5.7, HC-39 1.4. Share of tiles under 48 hours, counted per served ranking: HC-31 13.6%, HC-33 14.1%, HC-34 13.9%, HC-36 8.8%, HC-37 21.4%, HC-39 15.2%. Fails: HC-31 breaks the guardrail in web 730+ (carousel order rate -2.7% vs the incumbent, worse than the -1.5% limit); HC-36 fails the 12% fresh-listing commitment (8.8%); HC-39 fails lift >= 2.0 (1.4). Eligible: HC-34, HC-37, HC-33
- Change in fee income per 1,000 carousel sessions, HC-31 (EUR, excl. VAT): app 0-29 9.1; app 30-179 8.9; app 180-729 8.1; app 730+ 7.2; web 0-29 10.6; web 30-179 6.8; web 180-729 9.9; web 730+ -1.9
- Change in fee income per 1,000 carousel sessions, HC-33 (EUR): app 0-29 4.6; app 30-179 9.6; app 180-729 3.7; app 730+ 3.1; web 0-29 1.4; web 30-179 5.7; web 180-729 0.7; web 730+ 2.0
- Change in fee income per 1,000 carousel sessions, HC-34 (EUR): app 0-29 -0.9; app 30-179 13.7; app 180-729 14.1; app 730+ 14.8; web 0-29 7.5; web 30-179 12.9; web 180-729 9.3; web 730+ 13.8
- Change in fee income per 1,000 carousel sessions, HC-36 (EUR): app 0-29 -7.3; app 30-179 -12.3; app 180-729 -11.9; app 730+ -14.6; web 0-29 -8.1; web 30-179 -11.1; web 180-729 -12.7; web 730+ -15.8
- Change in fee income per 1,000 carousel sessions, HC-37 (EUR): app 0-29 7.3; app 30-179 9.1; app 180-729 8.2; app 730+ 5.0; web 0-29 6.7; web 30-179 10.0; web 180-729 7.6; web 730+ 4.4
- Change in fee income per 1,000 carousel sessions, HC-39 (EUR): app 0-29 5.0; app 30-179 1.5; app 180-729 1.5; app 730+ 0.9; web 0-29 1.5; web 30-179 -2.3; web 180-729 0.6; web 730+ 1.4
- Twelve-week totals per policy: extra orders and extra fee income (nearest hundred): HC-31: 16,900 orders, EUR 18,300; HC-33: 8,800 orders, EUR 10,400; HC-34: 26,100 orders, EUR 32,100; HC-36: 13,200 orders, EUR -33,500; HC-37: 15,200 orders, EUR 18,800; HC-39: 3,700 orders, EUR 3,100
- Slot traffic basis: 10% of R2 restated weekly sessions on the same ISO weeks one year earlier: web 2026-W01 to W12, and app 2026-W03 to W12, because the app arm starts with release 27.1 on 18 Jan 2027. Total 2,661,486 arm sessions (app 1,586,295; web 1,075,193)

### carousel_slot_q1_2027_cells.png (solver's answers)
- Grid: policies down, eight cells across, coloured by fee change per 1,000 sessions: Same 6x8 EUR grid as the notebook (HC-31, HC-33, HC-34, HC-36, HC-37, HC-39 by app/web x 0-29, 30-179, 180-729, 730+). Range runs from -15.8 (HC-36 web 730+) to +14.8 (HC-34 app 730+)
- Hatched guardrail-breach cells: One cell: HC-31 x web 730+ (carousel order rate 54.9 vs 56.5 per 1,000, -2.7%)
- Outlined row and title: HC-34 row outlined. Title: 'HC-34 Session-sequence model takes the Q1 2027 home carousel slot: +9.8 orders per 1,000 carousel sessions'
