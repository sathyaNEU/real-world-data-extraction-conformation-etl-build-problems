# task122 · Q1 2027 home carousel test slot

## Tags

**Domain:** Product Analytics (experimentation measurement: offline screening of registered home carousel ranking policies from a randomised session logger).
**Analytical objective:** Experiment & Causal Analysis (each policy's lift over the test from logged sessions under the archive-certified estimator, read against the charter's launch conditions).

## 1. Final Recommendation

**The Q1 2027 home carousel test slot, 4 January to 28 March 2027, goes to the sequence ranker with fresh-listing interleave (HC-37), which gives us 5.7 extra orders per 1,000 carousel sessions.**

It leads the velocity boost (HC-33), the only other policy that clears all three launch conditions, by 2.4. Not the session-sequence model or the two-tower personaliser, which each break the guardrail in one cell once every order placed from an arm's tiles is counted. Not the local pickup boost, which misses the fresh-listing floor. Not the seller-diversity re-ranker, which is under the lift bar. Not the velocity boost on its in-session orders, most of whose gain is watched listings its buyers buy within days anyway.

## 2. Critical Components

1. The per-session propensity estimator reproduces **9 of 9** archived tests within 0.25
2. On every order placed from each arm's tiles, the carousel order rate is **3.8%** below Blend v7 for the session-sequence model in app 0-29 and **2.5%** below for the two-tower personaliser in web 730+
3. The local pickup boost serves **8.8** fresh tiles per 100 per served ranking, and the seller-diversity re-ranker's lift is **1.4**
4. The velocity boost's lift over the test is **3.3** extra orders per 1,000 carousel sessions, against **8.0** in session
5. The sequence ranker with fresh-listing interleave's lift over the test is **5.7**

## 3. Step-by-Step Solution

1. Collapsed `home_carousel_render_log_2026-06-22_2026-09-20.csv` to one row per session (the logger's draw unit), joined `home_carousel_served_rankings_2026-06-22_2026-09-20.parquet` on `session_id` and placed each session in the charter's eight platform-by-tenure cells.
2. Ran replay over the render rows, a propensity weight per render row and a propensity weight per session on every test in `carousel_experiment_archive.xlsx`: only the per-session weight returns all nine realised lifts within 0.25, as charter 5.2 requires.
3. Scored each session on its buyer's orders in every channel of `orders_enrolled_buyers_2026-06-01_2026-10-11.parquet` over the 21 days after it started (lift is orders during the test, charter 2.2): every policy's lift is flat from day 6, and the velocity boost falls from 8.0 to 3.3 because its pinned tiles sell watched listings the buyer buys within days anyway.
4. Counted the carousel order rate (charter 2.4) on every order placed from the tiles each arm served, joining the buyer's carousel orders to the session's six tiles by listing (a shown listing stays off that buyer's carousel for seven days, `carousel_logger_field_reference.md`), which adds the orders placed after the session closed: the session-sequence model is 3.8% below Blend v7 in app 0-29 and the two-tower personaliser 2.5% below in web 730+.
5. Applied the fresh-listing commitment per served ranking (the local pickup boost serves 8.8 per 100) and the 2.0 bar (the seller-diversity re-ranker is at 1.4), leaving HC-37 at 5.7 ahead of HC-33 at 3.3, a gap of 2.4.
6. Charged every 21-day order the terms cover (all but pickups paid to the seller in person, `buyer_protection_terms_2026-09.pdf` s.2, so purchases paid from a Vouwlijn balance count although `payments_buyer_protection_2026-06-01_2026-10-11.parquet` holds only card and iDEAL captures) at tariff KB-2026-02 in `kopersbescherming_tarieven.csv` (EUR 0.80 plus 5% of the price paid after any accepted offer; the January row was deferred in `pricing_committee_minutes_2026-10-06.docx`), net of the 21% VAT as `finance_buyer_protection_fee_income_2026Q3.xlsx` books fee income, and differenced each policy's cell mean against Blend v7: the 48 cells below.
7. Took 10% of 2026-W01 to W12 sessions per cell from `home_carousel_sessions_weekly_2025W01_2026W39.csv` with `home_carousel_sessions_weekly_R2_2026W01_2026W26.csv` replacing those weeks, app cells from W03 (first app release on 18 January 2027 in `app_release_calendar_2026-2027.ics`, per `slot_capacity_and_release_gating.md`), and multiplied by each cell's order and fee lift: the totals below.
8. Recommendation: the sequence ranker with fresh-listing interleave (HC-37) takes the Q1 2027 slot at 5.7 extra orders per 1,000 carousel sessions.

## 4. Deliverable Answers

### carousel_slot_q1_2027.ipynb

1. Sequence ranker with fresh-listing interleave (HC-37), 5.7 extra orders per 1,000 carousel sessions
2. Closest policy clearing the launch conditions: velocity boost (HC-33), 3.3; gap 2.4
3. Change in buyer-protection fee income per 1,000 carousel sessions while the slot runs, EUR, against Blend v7:
   - Two-tower personaliser (HC-31): app 0-29 9.1, app 30-179 8.9, app 180-729 8.1, app 730+ 7.2, web 0-29 10.6, web 30-179 6.8, web 180-729 9.9, web 730+ -1.9
   - Velocity boost (HC-33): app 0-29 4.6, app 30-179 9.6, app 180-729 3.7, app 730+ 3.1, web 0-29 1.4, web 30-179 5.7, web 180-729 0.7, web 730+ 2.0
   - Session-sequence model (HC-34): app 0-29 -0.9, app 30-179 13.7, app 180-729 14.1, app 730+ 14.8, web 0-29 7.5, web 30-179 12.9, web 180-729 9.3, web 730+ 13.8
   - Local pickup boost (HC-36): app 0-29 -7.3, app 30-179 -12.3, app 180-729 -11.9, app 730+ -14.6, web 0-29 -8.1, web 30-179 -11.1, web 180-729 -12.7, web 730+ -15.8
   - Sequence ranker with fresh-listing interleave (HC-37): app 0-29 7.3, app 30-179 9.1, app 180-729 8.2, app 730+ 5.0, web 0-29 6.7, web 30-179 10.0, web 180-729 7.6, web 730+ 4.4
   - Seller-diversity re-ranker (HC-39): app 0-29 5.0, app 30-179 1.5, app 180-729 1.5, app 730+ 0.9, web 0-29 1.5, web 30-179 -2.3, web 180-729 0.6, web 730+ 1.4
4. Totals over the twelve weeks, extra orders and extra fee income, nearest hundred:
   - Two-tower personaliser (HC-31): 16,900 orders, EUR 18,300
   - Velocity boost (HC-33): 8,800 orders, EUR 10,400
   - Session-sequence model (HC-34): 26,100 orders, EUR 32,100
   - Local pickup boost (HC-36): 13,200 orders, EUR -33,500
   - Sequence ranker with fresh-listing interleave (HC-37): 15,200 orders, EUR 18,800
   - Seller-diversity re-ranker (HC-39): 3,700 orders, EUR 3,100

### carousel_slot_q1_2027_cells.png

1. Heatmap of the fee grid, the six policies down and the eight cells across, each cell coloured on its EUR figure (red below zero, blue above) and labelled to one decimal
2. Hatched cells: two-tower personaliser in web 730+ and session-sequence model in app 0-29
3. Outlined row: sequence ranker with fresh-listing interleave (HC-37)
4. Title: Q1 2027 carousel slot: Sequence ranker with fresh-listing interleave (HC-37), +5.7 orders per 1,000 carousel sessions
