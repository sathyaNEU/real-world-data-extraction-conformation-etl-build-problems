# ET01 — Point-in-time fundamentals: the revenue-acceleration screen that only worked in the backtest

| Field | Value |
|---|---|
| Domain | Capital markets / quant research data platform |
| Objective family | Data Extraction & Conformation (ETL / Pipeline Build) |
| Task shape | 01 · Ranked list under a cap (top-N screen) |
| Core technique | Bitemporal (as-known-as-of) fact selection; YTD-to-discrete quarter derivation; XBRL tag-priority conformance |
| Trap family (honest data) | Look-ahead through restated comparatives; "latest value wins" dedup |
| Primary sources | SEC EDGAR Financial Statement Data Sets (FSDS) |

## 1. The real-world project

A systematic equity team is replacing a vendor fundamentals feed with an in-house warehouse built from the SEC
Financial Statement Data Sets (quarterly zips of `sub.txt`, `num.txt`, `tag.txt`, `pre.txt`). The first production
signal is a **revenue-acceleration screen**: at each rebalance date, take every eligible filer, compute
year-over-year growth of the most recent discrete quarter's revenue and subtract the same growth one quarter
earlier, and buy the top 10.

The data engineer built a `fact_latest` table: for every `(cik, tag, ddate, qtrs, uom)` keep the value from the
most recently accepted submission. It is clean, unique, and passes every row-count test. The backtest Sharpe was
excellent. Live performance was not.

## 2. The business decision (one deterministic recommendation)

**Which 10 companies does the screen select as of the rebalance date 2023-08-15 (close), and which company is the
first one left out?**

The methodology note (part of the task folder) fixes every choice:

* Knowledge time = `sub.accepted`. Only submissions accepted on or before 2023-08-15 23:59:59 ET are visible.
* For a given `(cik, ddate, qtrs)` fact, use the value from the **latest submission visible as of the rebalance
  date** — not the latest submission in the warehouse.
* Revenue tag priority: `RevenueFromContractWithCustomerExcludingAssessedTax` → `Revenues` →
  `SalesRevenueNet` → `RevenueFromContractWithCustomerIncludingAssessedTax`; first tag present for that period wins.
* Only non-dimensional facts: `coreg` empty, `uom = USD`, no segment qualifiers.
* Discrete quarter = `qtrs = 1` fact if present; otherwise derive: Q4 = FY (`qtrs = 4`) − 9-month YTD (`qtrs = 3`);
  Q2 = 6M (`qtrs = 2`) − Q1; Q3 = 9M − 6M. Align periods by `ddate` (period end), never by `fy`/`fp`.
* Eligibility: 8 consecutive discrete quarters available as of the rebalance date; latest quarter revenue ≥ $50m.
* Score = YoY growth(latest quarter) − YoY growth(prior quarter). Rank descending; ties broken by larger latest
  revenue.

## 3. Why this gets overlooked in real projects

* FSDS is published per quarter of *filing*, so the same economic fact (e.g. FY2021 revenue) appears in the
  FY2021 10-K, again as a comparative in the FY2022 10-K, and again in the FY2023 10-K. Deduplicating to "latest"
  feels like hygiene, not like a modelling decision.
* Comparatives are frequently **restated** (discontinued operations, segment re-casts, accounting-policy changes,
  error corrections). The restated number is *correct* — it simply was not known on the rebalance date.
* Unit tests check uniqueness and non-null; nothing checks that a value's `accepted` timestamp precedes its use.
* The derived-Q4 step multiplies the problem: FY from the 10-K (Feb) minus 9M YTD from the Q3 10-Q (Nov) can mix
  a restated FY with an unrestated 9M if the as-of filter is applied to one leg but not the other.

## 4. Input package (≥10 files, ≥3 formats, ≥1 file ≥10k rows)

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1–36 | `2021q1/ … 2023q3/` × `sub.txt`, `num.txt`, `tag.txt`, `pre.txt` | TSV (txt) | `num.txt` ≈ 2–3.5M rows per quarter | SEC EDGAR FSDS (sec.gov/dera/data/financial-statement-data-sets) | U.S. Government work, public domain; follow SEC fair-access rules | Facts, submissions, tag metadata |
| 37 | `fsds_readme.htm` / data-set documentation | HTML/PDF | — | SEC DERA | Public domain | Field definitions (`accepted`, `prevrpt`, `qtrs`, `coreg`) |
| 38 | `company_tickers_exchange.json` | JSON | ~10k | SEC | Public domain | CIK ↔ ticker/exchange universe |
| 39 | `screen_methodology.pdf` | PDF | — | Task author (written as an internal research memo) | — | Rules in §2 |
| 40 | `us-gaap-2023` taxonomy element list | XLSX | ~20k elements | FASB/XBRL US GAAP Taxonomy | FASB taxonomy terms (free use) | Deprecated tag lineage (`SalesRevenueNet`) |

Record the download date for every zip; FSDS files are occasionally re-issued.

## 5. Deterministic solution path

1. Load `sub.txt` for all quarters; keep forms `10-K`, `10-K/A`, `10-Q`, `10-Q/A`; parse `accepted` as ET.
2. Filter `sub.accepted ≤ 2023-08-15 23:59:59`. **This filter is applied before any dedup.**
3. Join `num` → filtered `sub` on `adsh`; keep revenue tags, `uom = USD`, empty `coreg`, no segments.
4. For each `(cik, tag, ddate, qtrs)`, keep the value from the submission with the max `accepted` among the visible
   ones (this correctly picks up a 10-K/A that arrived *before* the rebalance date).
5. Apply tag priority per `(cik, ddate, qtrs)`.
6. Build discrete quarters by `ddate`; derive missing Q2/Q3/Q4 per the rules, each leg drawn from the as-of set.
7. Require 8 consecutive quarters (quarter ends ≈ 91 ± 7 days apart; 52/53-week filers allowed).
8. Compute YoY growth for latest and prior quarter, score, rank, cut at 10.
9. Repeat steps 3–8 **without** step 2 (the "latest" warehouse) to produce the comparison for the bridge chart.

## 6. The traps

**Trap A — latest-value dedup (look-ahead).** The solver deduplicates the whole FSDS history to the most recent
value and then filters by `ddate ≤ as-of`. Every period is "in the past", so the filter looks correct, but prior-year
comparatives now carry values restated in filings accepted after 2023-08-15. Growth rates change, several names
swap in/out of the top 10.

**Trap B — fiscal labels instead of period ends.** Joining periods on `fy`/`fp` from `sub.txt` misaligns 52/53-week
filers and companies whose fiscal year label differs from the calendar year of `ddate`; YoY pairs become
5-quarter or 3-quarter gaps.

**Trap C — Q4 from mixed vintages.** Deriving Q4 = FY − 9M where FY comes from a later restated 10-K and 9M from the
original 10-Q produces a "Q4" that absorbs the restatement of Q1–Q3.

**Trap D — tag switching mid-series.** Using only `Revenues` drops companies that report
`RevenueFromContractWithCustomerExcludingAssessedTax`, or splices two tags with different scopes; the priority list
must be applied per period.

## 7. Why the data is honest

Every value in FSDS is exactly what the filer reported in that submission. Restated comparatives are correct
restatements. The challenge is purely methodological: knowing *when* each number became knowable and enforcing that
in the pipeline.

## 8. Draft task prompt (prose)

> Our revenue-acceleration screen rebalances on 15 August 2023 and buys ten names. Using the SEC financial statement
> data sets in the folder and the screen methodology memo, tell me exactly which ten companies the screen would have
> bought on that date and which company was first in line behind them. Produce `screen_2023-08-15.csv` with every
> eligible company, its latest and prior discrete-quarter revenue, the two YoY growth rates, the acceleration score,
> its rank, and whether it is selected. Then give me `pit_vs_latest.png`: for every company that is in the top ten
> under either the point-in-time rule or our current latest-value warehouse, show its rank under both, and mark which
> names enter or leave. Finally, a one-page `screen_note.pdf` stating the selected list, the first name out and its
> score gap to #10, how many names change versus the warehouse view, and for the single largest rank mover, the
> restated filing (accession and accepted date) responsible.

## 9. Deliverables

* `screen_2023-08-15.csv` (data) — full eligible universe, ranked.
* `pit_vs_latest.png` (visual) — slope/dumbbell chart of rank under both rules.
* `screen_note.pdf` (text, 1 page) — decision, gap, mover attribution.

## 10. Where 25+ rubric criteria come from

* 10 selected names (each a criterion), the #11 name, and the score gap #10 vs #11.
* Acceleration score for 5–6 named companies (checks Q4 derivation and tag priority).
* Count of eligible universe; count of names that differ PIT vs latest.
* Identification of the largest mover and the accession/accepted date that causes it.
* Chart: both ranks shown, entrants/leavers marked; CSV column set and sort order.

## 11. Golden-output checklist

* Visible-submission filter applied before dedup; restated comparatives accepted after the as-of date excluded.
* Q4 derived from as-of-visible FY and 9M legs only.
* Periods aligned on `ddate`; 52/53-week filers handled.
* Selected list and #11 stated; differences vs latest-value warehouse quantified.

## 12. Build notes (scope tuning so the trap flips the answer)

* Pick the universe (e.g. SIC 7370–7379 + 3570–3579, revenue ≥ $50m) and the as-of date so that **at least two of
  the top ten change** between the PIT and latest views; compute both before freezing the prompt.
* Prefer an as-of date 1–3 months before a filing season in which several universe members restated comparatives
  (search `sub.txt` for `10-K/A` and for prior-period values that differ across `adsh`).
* Keep the universe to 150–400 eligible names so the CSV is checkable but not eyeball-able.
