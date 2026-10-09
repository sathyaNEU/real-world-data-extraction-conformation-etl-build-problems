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

1. Collapsed `home_carousel_render_log_2026-06-22_2026-09-20.csv` to one row per session (the logger's draw unit), joined `home_carousel_served_rankings_2026-06-22_2026-09-20.parquet` on `session_id`, placed each session in the charter's eight platform-by-tenure cells and back-tested the estimators on `carousel_experiment_archive.xlsx`: only a propensity weight per session returns all nine realised lifts within 0.25, as charter 5.2 requires.
2. Scored each session on its buyer's orders in every channel of `orders_enrolled_buyers_2026-06-01_2026-10-11.parquet` over the 21 days after it started (lift is orders during the test, charter 2.2): every policy's lift is flat from day 6, and the velocity boost falls from 8.0 to 3.3 because its pinned tiles sell watched listings the buyer buys within days anyway.
3. Counted the carousel order rate (charter 2.4) on every order placed from the tiles each arm served, joining the buyer's carousel orders to the session's six tiles by listing (a shown listing stays off that buyer's carousel for seven days, `carousel_logger_field_reference.md`), which adds the orders placed after the session closed: the session-sequence model is 3.8% below Blend v7 in app 0-29 and the two-tower personaliser 2.5% below in web 730+.
4. Applied the fresh-listing commitment per served ranking (the local pickup boost serves 8.8 per 100) and the 2.0 bar (the seller-diversity re-ranker is at 1.4), leaving HC-37 at 5.7 ahead of HC-33 at 3.3, a gap of 2.4.
5. Planned each cell's arm sessions as 10% of its 2026-W01 to W12 sessions in `home_carousel_sessions_weekly_2025W01_2026W39.csv`, with `home_carousel_sessions_weekly_R2_2026W01_2026W26.csv` replacing those weeks and app cells from W03 (first app release on 18 January 2027 in `app_release_calendar_2026-2027.ics`, per `slot_capacity_and_release_gating.md`), and split them at the checkout change of 1 March 2027 in the same note: six of the app arm's ten weeks and eight of the web arm's twelve fall before it.
6. Priced every 21-day order at tariff KB-2026-02 in `kopersbescherming_tarieven.csv` (EUR 0.80 plus 5% of the price paid after any accepted offer; the January row was deferred in `pricing_committee_minutes_2026-10-06.docx`), net of the 21% VAT as `finance_buyer_protection_fee_income_2026Q3.xlsx` books it, with the balance-paid purchases `payments_buyer_protection_2026-06-01_2026-10-11.parquet` does not capture: leaving pickups paid to the seller in person uncharged reproduces Finance's Q3 statement to the cent, and as pickups are paid at checkout and covered from 1 March (`buyer_protection_terms_2026-09.pdf` s.2), each cell's difference against Blend v7 weights the two covers by its planned sessions either side, the 48 cells below.
7. Multiplied each cell's order and fee lift by its planned arm sessions and summed the eight cells: the twelve-week totals below.
8. Recommendation: the sequence ranker with fresh-listing interleave (HC-37) takes the Q1 2027 slot at 5.7 extra orders per 1,000 carousel sessions.

## 4. Deliverable Answers

### carousel_slot_q1_2027.ipynb

1. Sequence ranker with fresh-listing interleave (HC-37), 5.7 extra orders per 1,000 carousel sessions
2. Closest policy clearing the launch conditions: velocity boost (HC-33), 3.3; gap 2.4
3. Change in buyer-protection fee income per 1,000 carousel sessions while the slot runs, EUR, against Blend v7:
   - Two-tower personaliser (HC-31): app 0-29 9.4, app 30-179 9.7, app 180-729 9.1, app 730+ 8.3, web 0-29 10.8, web 30-179 7.7, web 180-729 10.3, web 730+ -1.6
   - Velocity boost (HC-33): app 0-29 4.5, app 30-179 9.4, app 180-729 3.2, app 730+ 3.2, web 0-29 1.9, web 30-179 6.6, web 180-729 1.2, web 730+ 2.1
   - Session-sequence model (HC-34): app 0-29 -0.8, app 30-179 14.2, app 180-729 14.6, app 730+ 15.2, web 0-29 8.1, web 30-179 13.1, web 180-729 10.5, web 730+ 14.5
   - Local pickup boost (HC-36): app 0-29 -1.6, app 30-179 -3.9, app 180-729 -4.1, app 730+ -5.8, web 0-29 -4.6, web 30-179 -4.8, web 180-729 -6.5, web 730+ -9.0
   - Sequence ranker with fresh-listing interleave (HC-37): app 0-29 7.8, app 30-179 9.3, app 180-729 7.8, app 730+ 6.0, web 0-29 6.6, web 30-179 9.9, web 180-729 7.7, web 730+ 5.2
   - Seller-diversity re-ranker (HC-39): app 0-29 4.6, app 30-179 1.9, app 180-729 1.9, app 730+ 0.7, web 0-29 0.8, web 30-179 -1.4, web 180-729 1.0, web 730+ 1.8
4. Totals over the twelve weeks, extra orders and extra fee income, nearest hundred:
   - Two-tower personaliser (HC-31): 16,600 orders, EUR 19,800
   - Velocity boost (HC-33): 8,600 orders, EUR 10,300
   - Session-sequence model (HC-34): 25,800 orders, EUR 33,200
   - Local pickup boost (HC-36): 13,000 orders, EUR -14,000
   - Sequence ranker with fresh-listing interleave (HC-37): 14,900 orders, EUR 19,200
   - Seller-diversity re-ranker (HC-39): 3,600 orders, EUR 3,500

### carousel_slot_q1_2027_cells.png

1. Heatmap of the fee grid, the six policies down and the eight cells across, each cell coloured on its EUR figure (red below zero, blue above) and labelled to one decimal
2. Hatched cells: two-tower personaliser in web 730+ and session-sequence model in app 0-29
3. Outlined row: sequence ranker with fresh-listing interleave (HC-37)
4. Title: Q1 2027 carousel slot: Sequence ranker with fresh-listing interleave (HC-37), +5.7 orders per 1,000 carousel sessions
