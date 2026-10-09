# solver round: round 1, plain

**Proxy score 89.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 47.8 of 58). Main call LANDED. 6 of 8 ask items cracked (80 per cent of tokens).

## Main call

golden: The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.

solver: HC-37, the sequence ranker with the fresh-listing interleave, gets the Q1 2027 home-carousel slot (4 Jan to 28 Mar 2027). It adds 5.8 orders per 1,000 carousel sessions over the slot's traffic mix (5.7 on the logged-window mix). It is the only policy that clears all three launch conditions apart from HC-33 Velocity boost, whose real lift is 3.4 once the watch-list orders it only moves from another channel are netted out, so HC-37 leads it by 2.4.

tokens matched 5 of 7 (4, 28, 37, 5.7, 1,000, January, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| carousel_slot_q1_2027.ipynb | 1 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 2 | 4 | 4 | 100% |
| carousel_slot_q1_2027.ipynb | 3 | 133 | 134 | 99% |
| carousel_slot_q1_2027.ipynb | 4 | 24 | 24 | 100% |
| carousel_slot_q1_2027_cells.png | 1 | 0 | 1 | 0% |
| carousel_slot_q1_2027_cells.png | 2 | 3 | 3 | 100% |
| carousel_slot_q1_2027_cells.png | 3 | 2 | 2 | 100% |
| carousel_slot_q1_2027_cells.png | 4 | 3 | 5 | 60% |

## Solver's path

1. Read the charter, fresh-listing commitment, policy register, slot gating note, tariff register, pricing committee minutes and planning thread. The six candidates are HC-31/33/34/36/37/39 and the incumbent is HC-24. Launch conditions: (a) lift of at least 2.0, (b) carousel order rate no more than 1.5% below the incumbent in any of the 8 platform x tenure cells, (c) at least 12 of every 100 tiles per served ranking go to listings under 48 hours old
2. Checked estimators on carousel_experiment_archive.xlsx logged_sessions. A session-level IPS, sum(in_session_orders/propensity)/N, test minus control, comes within 0.25 of the realised lift for all nine tests (worst miss 0.17 on T1). Render-weighted replay misses by up to 3.8 (T7)
3. Collapsed the render log to 150,400 sessions (one ranker and propensity each; quotas filled exactly, so the per-cell IPS equals the per-cell mean). Assigned cells from buyer_tenure_days using bands 0-29/30-179/180-729/730+
4. Joined served_rankings tile ages. Fresh share per served ranking: HC-36 8.8%, which fails (c); it would show 15.6% if counted per render. All others are above 12%, with HC-37 at 21.4%
5. Carousel order rate (from ordered_tiles) by cell vs HC-24: HC-34 is -2.39% in app 0-29 and HC-31 is -2.74% in web 730+, so both break (b)
6. Lift outcome: all orders by the buyer (any channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days. HC-33 pins watch-list listings in tiles 1-2, which cannibalises favourites/alerts orders in the 180+ tenure cells, so its net log-mix lift is 3.30 against a gross carousel lift of 7.96. Other policies: HC-31 6.56, HC-34 9.78, HC-36 5.07, HC-37 5.70, HC-39 1.39, so HC-39 fails (a)
7. Fee per order: joined payments and recomputed at the 1 Sep 2026 tariff, EUR 0.80 + 5% of item price paid (amount - shipping - fee, which already reflects accepted offers), because KB-2027-01 was deferred by the 6 Oct pricing committee. Pickup orders paid directly carry no fee. Took per-cell differences vs HC-24 per 1,000 sessions
8. Slot traffic: R2 restatement 2026-W01..W12 (it matches the account-service tenure), app only from W03 because of the release 27.1 gate on 18 Jan 2027, times the 10% share = 2,639,219 sessions. Weighting the per-cell lift and fee by this traffic gives slot lifts of HC-37 5.79 and HC-33 3.38 (gap 2.42), and totals of HC-37 15,286 orders and EUR 22,778

confidence: Medium. The ranking, the screen outcomes, the fee grid and the totals hold up under alternative horizons and traffic bases. The headline rate depends on the weighting: 5.8 on the slot traffic mix versus 5.7 on the logged-window mix.

notes: The headline lift uses the slot traffic mix (5.8). On the logged-window mix it is 5.7, and the gap is 2.4 either way. Fees are at the EUR 0.80 + 5% tariff because KB-2027-01 (EUR 0.95) was deferred. All work was done in in-memory Python scripts; no scratch files were written.

### carousel_slot_q1_2027.ipynb (solver's answers)
- Opening answer: chosen policy and its lift: HC-37 (Sequence ranker with fresh-listing interleave): +5.8 extra orders per 1,000 carousel sessions over the Q1 2027 slot traffic mix (+5.7 on the logged-window mix, 22 Jun to 20 Sep 2026)
- Closest policy that also clears the launch conditions, and the gap: HC-33 Velocity boost: net lift +3.4 per 1,000 sessions (3.3 on the log mix); its gross in-session carousel lift of 8.0 drops to 3.4 because the pinned tiles 1 and 2 are watch-list items the buyer would have ordered within 7 days anyway. Gap: HC-37 leads by 2.4 extra orders per 1,000 carousel sessions
- Screen outcome for the other policies: HC-34 Session-sequence model (lift 9.6) breaks the guardrail in app 0-29, where its carousel order rate is 2.4% below the incumbent. HC-31 Two-tower personaliser (lift 6.5) breaks it in web 730+ (-2.7%). HC-36 Local pickup boost (lift 5.0) breaks the fresh-listing commitment: 8.8 fresh tiles per 100 per served ranking, below the minimum of 12 (15.6 if counted per render). HC-39 Seller-diversity re-ranker misses condition (a) with lift 1.4, below 2.0. HC-37 has 21.4 fresh tiles per 100 and HC-33 has 14.1; neither breaks the guardrail in any cell
- Change in buyer-protection fee income per 1,000 carousel sessions, EUR, one decimal, by policy (cells in order app 0-29 / app 30-179 / app 180-729 / app 730+ / web 0-29 / web 30-179 / web 180-729 / web 730+): HC-31: 11.0 / 10.8 / 9.8 / 8.5 / 12.7 / 8.3 / 11.9 / -2.2. HC-33: 5.6 / 11.6 / 4.5 / 3.7 / 1.9 / 6.8 / 1.0 / 2.4. HC-34: 1.4 / 16.5 / 17.0 / 17.9 / 9.0 / 15.7 / 11.3 / 16.7. HC-36: -8.7 / -14.9 / -14.4 / -17.7 / -9.8 / -13.1 / -15.6 / -19.2. HC-37: 8.9 / 11.0 / 9.8 / 6.1 / 7.6 / 12.1 / 9.1 / 5.4. HC-39: 6.0 / 1.9 / 1.8 / 1.1 / 1.5 / -2.8 / 0.7 / 1.7
- Twelve-week totals: extra orders, nearest hundred: HC-31 17,100; HC-33 8,900; HC-34 25,300; HC-36 13,200; HC-37 15,300; HC-39 3,800
- Twelve-week totals: extra buyer-protection fee income, EUR, nearest hundred: HC-31 EUR 22,600; HC-33 EUR 12,700; HC-34 EUR 38,300; HC-36 EUR -39,600; HC-37 EUR 22,800; HC-39 EUR 3,700
- Slot traffic basis: 2,639,219 test-arm carousel sessions (10% of R2 logged-in sessions; web 2026-W01 to W12, app 2026-W03 to W12 because the app arm starts with release 27.1 on 18 Jan 2027). By cell: app 0-29 216,093; app 30-179 370,206; app 180-729 475,592; app 730+ 514,023; web 0-29 155,100; web 30-179 256,385; web 180-729 320,701; web 730+ 331,120

### carousel_slot_q1_2027_cells.png (solver's answers)
- Title call: HC-37 takes the Q1 2027 home carousel slot: +5.8 orders per 1,000 carousel sessions, about 15,300 extra orders and EUR 22,800 extra buyer-protection fee income over 12 weeks
- Grid coloured by fee change per 1,000 sessions: Same 6x8 fee grid as the notebook (policies down, cells across), values from -19.2 (HC-36, web 730+) to +17.9 (HC-34, app 730+)
- Hatched guardrail-breach cells: Two cells: HC-34 x app 0-29 (carousel order rate -2.4% vs incumbent) and HC-31 x web 730+ (-2.7%)
- Outlined row: HC-37
