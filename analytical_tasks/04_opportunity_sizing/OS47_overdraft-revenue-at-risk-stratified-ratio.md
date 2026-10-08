# OS47 — Fee revenue at risk under a cap: only large banks report it, and small banks are not small large banks

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Extrapolating revenue or usage from the subset of units that report it (large customers with telemetry, enterprise accounts with detailed billing) to the whole population |
| Domain | Banking / regulatory impact |
| Task shape | 03 · Bridge between two totals (reported overdraft revenue at reporting banks → industry-wide estimate via stratified ratio estimation; the revenue-at-risk figure for a fee-cap impact assessment) |
| Core method | Ratio estimator stratified by asset size class: within strata where both overdraft revenue and deposit service charges are reported, ratio r_h = Σ overdraft ÷ Σ total service charges on deposit accounts; apply r_h to non-reporting banks' total service charges in the same or nearest stratum per memo; revenue at risk = revenue × (1 − capped fee ÷ current average fee) |
| Analytical stump | Only banks above $1 billion in assets report overdraft-related service charges separately. Scaling their total by deposit share assumes small banks earn overdraft revenue in the same proportion to deposits; the ratio of overdraft revenue to deposit service charges differs by size. A stratified ratio estimator respects that |
| Primary sources | FFIEC Call Reports bulk data (Schedule RI and RI-E, including consumer overdraft-related service charges for reporting institutions) |

## 1. The real-world situation

An industry association must estimate revenue at risk from a proposed overdraft-fee cap for all banks. The draft took reporting banks' overdraft
revenue and grossed it up by total industry deposits ÷ reporting banks' deposits. Community bankers argued that their overdraft revenue relative
to deposits differs from large banks'.

## 2. The decision (one deterministic recommendation)

**Industry overdraft revenue (USD billions, annual) estimated by the stratified ratio method, and revenue at risk under the proposed cap.**

Rules (association memo):

* Data: Call Reports for the four quarters of the year in memo (year-to-date income items converted to annual by taking Q4 YTD).
* Reporting banks: those reporting the consumer overdraft-related service charges item (RIADH032 per memo) with non-missing values.
* Strata: assets $1–3B, $3–10B, $10–50B, > $50B; non-reporting banks: < $1B (single stratum) estimated using the $1–3B stratum ratio adjusted
  by the memo's factor (from published small-bank survey evidence).
* r_h = Σ overdraft ÷ Σ service charges on deposit accounts (RIAD4080) within stratum.
* Estimated overdraft revenue = reported + Σ non-reporting RIAD4080 × r_adjusted.
* Revenue at risk = estimate × (1 − $5 ÷ current average fee $27) (memo assumptions).
* Report the deposit-share gross-up for contrast.

## 3. Why capable analysts get it wrong

* Deposit-share scaling is common for extrapolation.
* The relationship between overdraft revenue and deposits varies by bank size and business model.
* Ratio estimators use a closely related auxiliary variable reported by all banks.
* YTD income must be annualised consistently.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `FFIEC CDR Call Bulk All Schedules <MMDDYYYY>.zip` (4 quarters) | Tab-delimited text inside ZIP | ~4.5k banks × schedules | FFIEC Central Data Repository | U.S. Gov public domain | Call Report data |
| 5 | `call_report_mdrm_dictionary.csv` | CSV | ~30k | Federal Reserve MDRM | Public domain | Item definitions |
| 6 | `association_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `draft_deposit_grossup.xlsx` | XLSX | — | Task author | — | Naive estimate |
| 8 | `small_bank_adjustment_citation.pdf` | PDF | — | Cite (public survey evidence) | Cite | Adjustment factor |
| 9 | `bank_assets_strata.parquet` | Parquet | ~4.5k | Derived | Public domain | Strata assignment |

## 5. Deterministic solution path

1. Extract Q4 YTD items; total assets; strata; reporting flags.
2. Stratum ratios; estimates for non-reporters; industry total.
3. Revenue at risk; bridge; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — deposit-share gross-up.** Wrong auxiliary relationship.

**B — single pooled ratio.** Size differences ignored.

**C — summing quarterly YTD values.** Double counting.

**D — ignoring the small-bank adjustment.** Not the memo's estimator.

## 7. Why the stump is analytical, not semantic

Items, strata and estimator are specified. The trap is extrapolating from a non-representative reporting subset.

## 8. Draft task prompt (prose)

> How much overdraft revenue is at risk industry-wide under the proposed cap? Extrapolate from reporting banks with the stratified ratio method in
> the association memo. Provide `stratum_estimates.csv` (stratum: banks, reporters, ratio, estimated revenue), `estimate_bridge.png`, and a
> one-page `revenue_at_risk.pdf`.

## 9. Deliverables

* `stratum_estimates.csv`, `estimate_bridge.png`, `revenue_at_risk.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 strata × (banks, ratio, estimate) = 15; totals; at-risk; contrast; annualisation check.

## 11. Golden-output checklist

* Q4 YTD; strata; reporter flags; ratios; adjustment; totals.

## 12. Build notes (scope tuning)

* Confirm the stratified estimate differs from the deposit gross-up by ≥ 15%.
