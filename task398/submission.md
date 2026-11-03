## Tags

**Domain:** Quantitative finance (factor and return attribution).
**Analytical objective:** Root-cause analysis.

## 1. Final Recommendation

**Run the value sleeve as a tracker of the benchmark: replayed on 2025-26 it removes 830 bp of the B Accumulation shares' 970 bp shortfall against the Larkspur UK All-Share, 310 bp more than the runner-up, raising the overlay's trigger to 12% (520 bp).** Not the higher trigger, which the year's attribution and any replay that keeps the overlay's recorded exposure put first: Penrose Bank's collapse in the value sleeve is what took the B Accumulation price more than 8% below its 63-day high on 2026-03-20, and with the sleeve tracking the benchmark the price's deepest fall below its high is 6.2%, short of the 8% line, so the overlay never cuts exposure and the fund keeps the April to June rebound.

## 2. Critical Components

1. Over the accounting year (from the noon valuation point on 2025-09-30 to the one on 2026-09-30) the B Accumulation shares returned **2.4%** and the benchmark at the valuation point **12.1%**: a shortfall of **970 bp**.
2. As the year ran, the B Accumulation price closed **8.7%** below its 63-day high on 2026-03-20 and the overlay held equity exposure at 40% from 2026-03-23 to 2026-06-08.
3. Each change replayed with the overlay rule run on that fund's own price removes: value sleeve as a tracker **830 bp**, higher trigger **520 bp**, earlier restoration **80 bp**, growth sleeve as a tracker **-30 bp**, equitised liquidity sleeve **-50 bp**.
4. With the value sleeve as a tracker the price's deepest fall below its high is **6.2%** (2026-04-02) and exposure is never reduced; the gap to the runner-up is **310 bp**.

## 3. Step-by-Step Solution

1. Took each sleeve's daily return from thornbury_mruke_valuation_summary.csv (each valuation over the previous one plus its quarter-end transfer), the benchmark's noon total return from larkspur_index_levels_2025-26.csv, the liquidity fund's yield, and the contracts and noon futures marks from merrow_overlay_daily_monitor_2025-26.xlsx.
2. Rebuilt the fund at each valuation point as the prospectus runs it (dealing, charges by class, distributions and futures margin through the liquidity sleeve; the 47/47/6 rebalance at each quarter-end), reproducing the published B Accumulation price.
3. For each change on the review terms' list, swapped the sleeve's return for the benchmark's or changed the rule's line, and ran the overlay rule on that fund's own B Accumulation price from 2025-09-30 (63 valuation points, more than 8% below to reduce, within 4% to restore, both from the next dealing day, 40% exposure in whole contracts).
4. Priced each change as its replayed B Accumulation return less the return as it ran, and ranked them.
5. Dividend income: holloway_income_entitlements_2025-26.csv for ex-dates to 2026-03-31 without Penrose Bank's March final (never paid after its resolution), plus the scrip-alternative dividends that report omits; Northcote receipts and scrip shares dated by their ex-dates in corporate_actions_feed_20261016.csv; dividends unpaid at the extract's end (2026-10-16) from the settled holding on the record date.
6. Dealing costs: commission plus stamp duty, each trade dated two UK dealing days before settlement (trades of 2025-12-31 settled on 2026-01-05), with the trades open at the change of custodian taken once from holloway_open_trades_31mar2026.csv.
7. AIM holdings: the growth sleeve's settled holdings at each quarter-end at the custodian's close prices, with each company's market as at that date (two moved from AIM to the Main Market, on 2026-05-18 and 2026-09-07).

## 4. Deliverable Answers

### change_pricing_2025-26.xlsx

1. Shortfall removed by each change (bp): value sleeve as a tracker 830; higher trigger 520; earlier restoration 80; growth sleeve as a tracker -30; equitised liquidity sleeve -50. Shortfall 970 bp.
2. Dividend income by ex-dividend date (GBP):
   - Value sleeve: October to December 2025 4,951,000; January to March 2026 3,032,000; April to June 2026 4,860,000; July to September 2026 3,196,000
   - Growth sleeve: October to December 2025 2,234,000; January to March 2026 2,027,000; April to June 2026 2,859,000; July to September 2026 1,512,000
3. Commission and stamp duty by quarter of trade (GBP):
   - Value sleeve: October to December 2025 245,500; January to March 2026 331,300; April to June 2026 398,100; July to September 2026 226,000
   - Growth sleeve: October to December 2025 360,300; January to March 2026 405,800; April to June 2026 211,200; July to September 2026 325,700
4. Growth sleeve holdings quoted on AIM: 2025-12-31 10 holdings, 11.9%; 2026-03-31 10 holdings, 12.3%; 2026-06-30 9 holdings, 9.2%; 2026-09-30 8 holdings, 7.5%.

### board_review_2025-26.pptx

1. The change: run the value sleeve as a tracker of the benchmark, 830 bp of the shortfall removed.
2. Runner-up: raise the overlay's trigger to 12%, 520 bp; difference 310 bp.
3. Bar chart of every change's figure in basis points on slide 2.
