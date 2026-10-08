# OS36 — Beds freed by fixing delayed discharges: bed-days ÷ 365 is not beds at the winter peak

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Capacity freed by removing waste (idle reserved instances, warehouse dwell time, gate occupancy) where the value depends on the peak period, not the annual average |
| Domain | Hospital operations / social care |
| Task shape | 02 · Forecast across many periods (beds freed per month if delayed transfers are halved; the number of escalation beds the trust can close in winter) |
| Core method | Monthly delayed bed-days per trust → average occupied beds by month (bed-days ÷ days in month); halving delays frees half of each month's average; escalation beds closable = beds freed in the peak months (Dec–Feb) adjusted for the occupancy target (beds needed at 92% target occupancy) |
| Analytical stump | Converting annual delayed bed-days to beds by dividing by 365 averages away the monthly pattern. Delays are not highest in the months when escalation beds are open — pre-Christmas discharge pushes and winter social-care surges move them around — and capacity can only be released if it exists in every winter month. The binding figure is the winter minimum of beds freed, adjusted for target occupancy |
| Primary sources | NHS England Delayed Transfers of Care (DToC) monthly statistics (trust-level delayed days) |

## 1. The real-world situation

An acute trust and its local authority plan a discharge-to-assess scheme expected to halve delayed transfers of care. The business case divided
annual delayed bed-days by 365 and promised to close 40 escalation beds every winter. Operations noted that delayed transfers fall sharply around Christmas and New Year, exactly when escalation beds are open.

## 2. The decision (one deterministic recommendation)

**The number of escalation beds the trust can close for December–February (the minimum over those months of beds freed, converted at the 92%
occupancy target), with monthly beds freed.**

Rules (operations memo):

* Data: DToC monthly delayed days by trust, financial year in memo (pre-2020 series; the trust's figures).
* Monthly average delayed beds = delayed days ÷ days in month.
* Beds freed = 0.5 × monthly average delayed beds.
* Beds closable in month m = floor(beds freed_m ÷ 0.92) (occupancy target conversion per memo).
* Winter closure = min over Dec, Jan, Feb of beds closable.
* Report annual ÷ 365 method for contrast.

## 3. Why capable analysts get it wrong

* Annual averages are standard in business cases.
* Escalation beds exist for the winter months; capacity freed must be available in each of those months.
* Occupancy targets mean a freed occupied bed-day does not equal a closable bed one-for-one.
* Monthly days differ; using 30 for all months introduces error.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `DTOC-Trust-<Month>-<Year>.xlsx` (12 months) | XLSX | ~150 trusts each | NHS England Statistical Work Areas | Open Government Licence v3 | Delayed days by trust |
| 13 | `dtoc_guidance.pdf` | PDF | — | NHS England | OGL | Definitions |
| 14 | `trust_in_scope.json` | JSON | 1 | Task author | — | Trust code |
| 15 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `business_case_annual.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 17 | `kh03_bed_availability.xlsx` | XLSX | ~150 trusts | NHS England KH03 | OGL | Context: beds and occupancy |

## 5. Deterministic solution path

1. Extract the trust's monthly delayed days; days per month.
2. Monthly beds freed and closable; winter minimum.
3. Contrast with annual ÷ 365.

## 6. Wrong paths (method errors, not misreadings)

**A — annual ÷ 365.** Seasonality averaged away.

**B — winter mean instead of minimum.** Cannot close beds needed in the worst month.

**C — no occupancy conversion.** Overstated closure.

**D — 30-day months.** Arithmetic error.

## 7. Why the stump is analytical, not semantic

The conversion rules are specified. The trap is sizing capacity on averages instead of the binding period.

## 8. Draft task prompt (prose)

> How many escalation beds can we close next winter if delayed transfers halve? Convert monthly delayed days as the operations memo specifies.
> Provide `beds_freed_by_month.csv` (month: delayed days, average delayed beds, freed, closable), `seasonal_delays.png`, and a one-page
> `winter_capacity.pdf`.

## 9. Deliverables

* `beds_freed_by_month.csv`, `seasonal_delays.png`, `winter_capacity.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 months × (average delayed beds, closable) = 24; winter minimum; contrast.

## 11. Golden-output checklist

* Trust extraction; days per month; halving; occupancy conversion; minimum.

## 12. Build notes (scope tuning)

* Choose a trust whose December–February delayed days are ≥ 20% below its annual monthly average, so the annual method overstates winter
  closures.
