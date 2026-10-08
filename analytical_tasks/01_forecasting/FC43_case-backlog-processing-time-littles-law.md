# FC43 — How long will a new application take? Today's backlog says more than last quarter's processing times

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Employers and service providers forecasting work-authorization and case wait times (tech-industry visa/EAD planning; any ticket backlog) |
| Domain | Government services / HR mobility planning |
| Task shape | 02 · Forecast across many periods (expected wait for applications filed in each of the next 4 quarters → one committed promise) |
| Core method | Stock–flow forecasting: queue simulation forward with receipts and completion capacity; expected wait for a new filing = backlog ahead ÷ completion rate (Little's law, FIFO approximation) |
| Analytical stump | Published processing times describe cases completed recently — they lag. When backlog grows faster than completions, a new filer will wait much longer than the historical median; the forward-looking estimate comes from the stock ahead of them and the throughput |
| Primary sources | USCIS quarterly data on receipts, completions and pending cases by form; USCIS historical processing times |

## 1. The real-world situation

A technology company's mobility team tells employees how long a work-permit renewal will take. They quote the latest published
median processing time. Over the past year, employees waited far longer than quoted, and several lost work authorization in the gap.

## 2. The decision (one deterministic recommendation)

**The wait time (months) the company quotes for applications filed next quarter, and the forecast for each of the next four quarters.**

Rules (mobility memo):

* Form in scope: the form in the folder (e.g. I-765 category). Quarterly receipts, completions (approved + denied) and pending at
  quarter end from USCIS quarterly reports, FY2019 Q1 – latest.
* Forward simulation (FIFO): receipts next quarters = same quarter last year × 1.03; completions per quarter = average of the last
  four quarters (capacity held flat).
* Expected wait for a case filed in quarter q (months) = (pending at start of q + half of receipts in q) ÷ completion rate per month
  in the following quarters (iterate quarter by quarter until the backlog ahead is cleared).
* Quote = the forecast for next quarter's filings, rounded up to the next half month.

## 3. Why capable analysts get it wrong

* Published processing times are the "official" number and feel authoritative.
* They measure completed cases — a lagging statistic that misses growth in the queue.
* Little's law links backlog, throughput and wait; when inflow exceeds throughput, waits grow every quarter.
* Using receipts instead of completions as the flow rate understates waits when the queue is growing.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–20 | `uscis_all_forms_fyXX_qY.xlsx` (FY2019 Q1 – latest) | XLSX | ~200 forms × measures each | USCIS (Immigration and Citizenship Data) | U.S. Gov public domain | Receipts, completions, pending |
| 21 | `uscis_quarterly_long.parquet` | Parquet | ~15k | Derived | Public domain | Long format |
| 22 | `historical_processing_times.csv` | CSV | ~2k | USCIS historic processing times | Public domain | Published medians |
| 23 | `uscis_data_definitions.pdf` | PDF | — | USCIS | Public domain | Definitions |
| 24 | `form_scope.json` | JSON | — | Task author | — | Form/category |
| 25 | `mobility_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 26 | `current_quote_method.xlsx` | XLSX | ~10 | Task author | — | Published-median quote |
| 27 | `littles_law_reference.pdf` (citation) | PDF | — | Cite | Cite | Queueing background |

## 5. Deterministic solution path

1. Extract the form's quarterly series; reconcile stock-flow identity (pending_t ≈ pending_{t−1} + receipts − completions; report gaps).
2. Simulate four quarters forward; compute expected waits by filing quarter.
3. Quote next quarter's figure; compare with the published median.

## 6. Wrong paths (method errors, not misreadings)

**A — published median.** Too short when the backlog is growing.

**B — pending ÷ receipts.** Wrong flow rate.

**C — ignoring the backlog ahead.** Treats every case as processed on arrival.

**D — annual averages.** Hide recent acceleration.

## 7. Why the stump is analytical, not semantic

Series and simulation rules are defined. The trap is using a lagging outcome statistic instead of a stock–flow forecast.

## 8. Draft task prompt (prose)

> What wait should we quote employees filing next quarter? Following the mobility memo, use the USCIS receipts, completions and
> pending counts to simulate the queue forward and forecast the wait for filings in each of the next four quarters. Provide
> `wait_forecast.csv` (quarter: pending ahead, receipts, completions, expected wait), `backlog_flow.png` (stock and flows with
> published processing times overlaid), and a one-page `quote_memo.pdf` with the quote and how far the published median understates it.

## 9. Deliverables

* `wait_forecast.csv`, `backlog_flow.png`, `quote_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Historical quarterly stocks/flows (spot-check 12); identity gaps; 4 forecast waits; quote; published-median contrast.

## 11. Golden-output checklist

* Correct form series; FIFO simulation; completion rate as throughput; rounding.

## 12. Build notes (scope tuning)

* Pick a form whose pending count grew ≥ 30% over the last year; confirm the forecast quote exceeds the published median by > 2 months.
* USCIS file layouts change across years; publish the extraction mapping.
