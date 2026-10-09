# solver round: round 5, plain

**Proxy score 48.0 / 100** (recommendation 3.6 of 35, instruction 7.0 of 7, asks 37.5 of 58). Main call missed. 2 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-34 (Session-sequence model) should take the Q1 2027 home-carousel slot (4 Jan to 28 Mar 2027). It adds 9.9 orders per 1,000 carousel sessions over the incumbent HC-24 Blend v7, about 25,700 extra orders and €31,100 extra buyer-protection fee income excl. VAT across the slot. The runner-up that also clears all three launch conditions is HC-37 (Sequence ranker with fresh-listing interleave) at 5.7, so the gap is 4.2.

tokens matched 5 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 3 | 4 | 75% |
| carousel_slot_q1_2027.ipynb | 3 | 93 | 134 | 69% |
| carousel_slot_q1_2027.ipynb | 4 | 15 | 24 | 62% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 3 | 3 | 100% |
| carousel_slot_q1_2027_cells.png | 3 | 1 | 2 | 50% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Archive check (carousel_experiment_archive.xlsx logged_sessions vs tests). A session-weighted inverse-propensity estimate of in-session carousel orders reproduces the realised lift of all 9 tests within 0.25 (for example T7 2.62 vs 2.5, T9 3.35 vs 3.2). Render-weighted replay misses (T7 6.29). So I used sessions, not renders, as the unit.
2. Render log joined to served rankings on session_id: 150,400 sessions, one ranker and propensity per session. Cells come from buyer_tenure_days (the account service value) in charter bands x platform. Propensities are constant within each cell and quotas are exact, so a policy's cell rate is the mean over its sessions.
3. Condition (c), fresh-listing commitment: share of tiles under 48 h old, counted once per served ranking. HC-24 13.0%, HC-31 13.6%, HC-33 14.1%, HC-34 13.9%, HC-36 8.8% (fails; 15.6% if counted per render), HC-37 21.4%, HC-39 15.2%.
4. Condition (b), carousel order rate: in-session carousel orders from ordered_tiles, which match the carousel orders on home_session_id one for one. Compared with HC-24 per cell, HC-31 web 730+ is -2.74%, a breach; HC-34's worst cell is app 0-29 at -0.96%, which passes.
5. Lift as the charter defines it: all orders the buyer placed in [session start, +7 days), from the orders parquet, any channel. This equals in-session orders for every policy except HC-33. HC-33 pins watch-list listings in tiles 1-2 (53% and 22% of sessions), which pulls forward favourites/alerts orders, so its per-cell lift falls from carousel-only values (up to 11.3) to 1.7-6.5. The counts are stable from 7 to 21 days.
6. Slot traffic: slot_capacity rule (same ISO weeks one year earlier) applied to the R2 weekly table, which uses account-service tenure. Web takes 2026-W01..W12. App takes W03..W12, because the release freeze means app release 27.1 on 18 Jan 2027 is the first app build. Times 10% gives 2,604,489 sessions. The slot-weighted lift is HC-34 9.874, HC-37 5.679, HC-31 6.325, HC-36 4.962, HC-33 3.271, HC-39 1.376 (fails a).
7. Fee per order: reconciled the finance Q3 xlsx exactly. It equals captured payments plus shipped orders with no capture (balance-paid), with item price = accepted offer if ordered before expiry, else asking price. Unpaid pickup orders carry no fee. Applied the slot tariff KB-2026-02 (EUR 0.80 + 5%); KB-2027-01 is unapproved and starts after the slot. Removed 21% VAT. Per-cell fee change vs HC-24 uses the same 7-day buyer window.
8. Totals = sum over cells of per-1,000 delta x slot sessions / 1,000. HC-34 gives 25,716 orders and EUR 31,090, rounded to 25,700 and EUR 31,100. The runner-up that clears all conditions is HC-37 at 5.7, a gap of 4.2.

confidence: Medium-high on the call (HC-34) and the 9.9 lift. Medium on the per-cell fee figures: orders outside the session add about ±1-2 EUR of price noise, so the values depend somewhat on the follow-up window (I used 7 days).

notes: The rounded lift depends on traffic weighting: logged-window cell mix gives 9.845 (9.8), slot mix gives 9.874 (9.9); I used the slot mix. Fee deltas include background-order price noise, so 14- or 21-day windows move cells by up to about 2 EUR. Order lifts do not move between 7 and 21 days.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Opening call: policy and lift: HC-34 Session-sequence model; lift 9.9 extra orders per 1,000 carousel sessions vs HC-24 (all buyer orders within 7 days of the session start, session-weighted per cell, weighted by Q1 slot traffic)
- Closest policy that clears the launch conditions, and the gap: HC-37 Sequence ranker with fresh-listing interleave, lift 5.7 per 1,000 carousel sessions; gap to HC-34 = 4.2 orders per 1,000 carousel sessions
- Launch-condition screen: HC-31 fails (b): web 730+ carousel order rate is -2.7% vs incumbent (54.95 vs 56.49 per 1,000). HC-36 fails (c): 8.8% fresh tiles per served ranking, below the 12% floor (it shows 15.6% if counted per render). HC-39 fails (a): lift 1.4 < 2.0. HC-33 passes but its true lift is 3.3, not the ~7.5 carousel-only figure, because its tiles 1-2 pull forward watch-list orders that would have happened anyway. HC-34 passes: fresh share 13.9%, worst cell app 0-29 at -1.0%, lift 9.9. HC-37 passes: fresh share 21.4%, lift 5.7.
- Fee income change per 1,000 carousel sessions, HC-31 (EUR, excl. VAT): app 0-29 8.9; app 30-179 8.7; app 180-729 8.0; app 730+ 6.5; web 0-29 10.7; web 30-179 7.1; web 180-729 8.1; web 730+ -3.0
- Fee income change per 1,000 carousel sessions, HC-33 (EUR): app 0-29 4.7; app 30-179 10.0; app 180-729 3.6; app 730+ 2.9; web 0-29 1.8; web 30-179 6.0; web 180-729 0.1; web 730+ 1.6
- Fee income change per 1,000 carousel sessions, HC-34 (EUR): app 0-29 -2.5; app 30-179 14.1; app 180-729 14.3; app 730+ 14.6; web 0-29 9.6; web 30-179 12.7; web 180-729 7.8; web 730+ 13.4
- Fee income change per 1,000 carousel sessions, HC-36 (EUR): app 0-29 -8.4; app 30-179 -12.6; app 180-729 -11.8; app 730+ -14.7; web 0-29 -8.1; web 30-179 -10.1; web 180-729 -14.0; web 730+ -15.7
- Fee income change per 1,000 carousel sessions, HC-37 (EUR): app 0-29 7.0; app 30-179 8.8; app 180-729 8.1; app 730+ 5.0; web 0-29 8.2; web 30-179 10.9; web 180-729 5.3; web 730+ 4.5
- Fee income change per 1,000 carousel sessions, HC-39 (EUR): app 0-29 4.4; app 30-179 2.3; app 180-729 1.7; app 730+ 1.7; web 0-29 1.6; web 30-179 -1.4; web 180-729 0.5; web 730+ 0.2
- Slot totals per policy: extra orders and extra fee income (EUR), nearest hundred: HC-31: 16,500 orders, EUR 16,400; HC-33: 8,500 orders, EUR 9,800; HC-34: 25,700 orders, EUR 31,100; HC-36: 12,900 orders, EUR -33,400; HC-37: 14,800 orders, EUR 17,700; HC-39: 3,600 orders, EUR 3,500
- Overall lift per 1,000 carousel sessions per policy (slot-weighted): HC-31 6.3; HC-33 3.3; HC-34 9.9; HC-36 5.0; HC-37 5.7; HC-39 1.4
- Slot traffic base (10% of R2-restated 2026-W01..W12 sessions; app from W03): 2,604,489 slot sessions: app 0-29 176,491; app 30-179 339,292; app 180-729 478,707; app 730+ 575,038; web 0-29 113,908; web 30-179 225,856; web 180-729 316,766; web 730+ 378,431

### carousel_slot_q1_2027_cells.png (solver's answers)
- Grid: policies down, cells across, coloured by fee change: Same 6x8 fee grid in EUR per 1,000 carousel sessions as the notebook; range -15.7 (HC-36 web 730+) to +14.6 (HC-34 app 730+)
- Hatched guardrail-breach cells: One cell: HC-31 x web 730+ (carousel order rate -2.7% vs incumbent, past the -1.5% limit). No other policy-cell breaches; HC-34 app 0-29 is -1.0%, so it is within the limit.
- Outlined row and title call: HC-34 row outlined; title: HC-34 Session-sequence model takes the Q1 2027 slot, +9.9 orders per 1,000 carousel sessions (about 25,700 orders and EUR 31,100 fee income over the slot)
