# DA31 — Pay distributions with partial-year workers: annualise before you compare

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Compensation analytics at companies with mid-year hires, leavers and part-timers (pay-equity reviews, band placement); per-subscriber revenue with partial-month subscribers |
| Domain | Public-sector payroll / HR analytics |
| Task shape | 14 · Cuts of a distribution (P10, P50, P90 of annualised base pay and overtime share for 5 job titles; the title referred for an overtime-dependency review) |
| Core method | Annualised base pay = base salary rate for annual-rate employees, or regular hours × hourly rate × (2,080 ÷ regular hours) for others per memo; filter to full-time, active-at-year-end or annualised partial-year records; overtime share = overtime pay ÷ total gross pay; percentiles across employees |
| Analytical stump | Gross pay of employees who joined or left mid-year is small, dragging percentiles down and inflating apparent dispersion; overtime shares computed on partial-year gross are noisy. Comparing titles on gross pay mixes tenure-in-year with pay level |
| Primary sources | NYC Citywide Payroll Data (NYC Open Data) |

## 1. The real-world situation

A city's budget office reviews job titles whose staff depend heavily on overtime. The analyst ranked titles by median gross pay and by
overtime ÷ gross pay over all payroll records, and identified a title with a low median and huge dispersion as "under-paid and overtime-
reliant". HR noted that the title had high turnover, so many records covered only a few months.

## 2. The decision (one deterministic recommendation)

**The job title referred for an overtime-dependency review: the title (among 5 in scope) with the highest median overtime share among
full-year-equivalent employees, with annualised pay percentiles for all five titles.**

Rules (budget memo):

* Data: NYC Citywide Payroll for the fiscal year in the memo; 5 titles in scope; pay basis per record (`Pay Basis`: per Annum, per Hour, per
  Day).
* Full-time: `Regular Hours` ≥ 1,820 for annual and hourly employees, or as defined in the memo for per-day; partial-year employees retained
  only if regular hours ≥ 520 and then annualised.
* Annualised base: per Annum → `Base Salary`; per Hour → `Base Salary` (hourly rate) × 2,080; per Day → rate × 261.
* Overtime share = `Total OT Paid` ÷ (`Regular Gross Paid` + `Total OT Paid` + `Total Other Pay`), computed on the actual year (not
  annualised); employees with < 520 regular hours excluded.
* Multiple records per employee-year (agency transfers): combine by the memo's name+agency+start-date key.
* Referral: highest median overtime share.

## 3. Why capable analysts get it wrong

* Gross pay is the most complete field and seems like "pay".
* Partial-year records are numerous in high-turnover titles.
* Pay basis differences (hourly versus annual) must be harmonised before comparing.
* Overtime share is unstable for workers with little regular time.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Citywide_Payroll_Data__Fiscal_Year_.csv` | CSV | ~6M (all years) | NYC Open Data | NYC Open Data terms (open) | Payroll records |
| 2 | `payroll_data_dictionary.xlsx` | XLSX | — | NYC Open Data | Open | Field definitions |
| 3 | `titles_in_scope.json` | JSON | 5 | Task author | — | Titles |
| 4 | `budget_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `analyst_gross_pay_ranking.xlsx` | XLSX | 5 | Task author | — | Naive analysis |
| 6 | `pay_basis_rules.json` | JSON | 3 | Task author | — | Annualisation |
| 7 | `employee_year_records.parquet` | Parquet | ~600k | Derived | Open | Fiscal-year extract |
| 8 | `payroll_check_cases.json` | JSON | ~10 | Task author | — | Hand-checked employees |
| 9 | `agency_codes.csv` | CSV | ~150 | NYC Open Data | Open | Agencies |

## 5. Deterministic solution path

1. Filter fiscal year and titles; combine multi-record employees.
2. Apply full-time and partial-year rules; annualise base pay.
3. Percentiles of annualised base; overtime shares; medians.
4. Referral; contrast with gross-pay analysis.

## 6. Wrong paths (method errors, not misreadings)

**A — gross pay percentiles.** Partial-year records drag down.

**B — mixing pay bases.** Hourly rates compared to salaries.

**C — overtime share on all records.** Noise from tiny regular hours.

**D — not combining transfers.** Split employees.

## 7. Why the stump is analytical, not semantic

The annualisation and filters are specified. The trap is comparing exposure-varying totals as if they were rates.

## 8. Draft task prompt (prose)

> Which of the five titles should we review for overtime dependency? Annualise pay and compute overtime shares as the budget memo specifies.
> Provide `title_pay_distribution.csv` (title: employees, P10/P50/P90 annualised base, median OT share, gross-pay figures for contrast),
> `ot_share_boxplot.png`, and a one-page `overtime_review.pdf`.

## 9. Deliverables

* `title_pay_distribution.csv`, `ot_share_boxplot.png`, `overtime_review.pdf`.

## 10. Where 25+ rubric criteria come from

* 5 titles × (P10, P50, P90, median OT share) = 20; counts; referral; check cases; contrast.

## 11. Golden-output checklist

* Combining records; filters; annualisation by basis; OT share definition; referral.

## 12. Build notes (scope tuning)

* Include one high-turnover title so that the naive and annualised analyses disagree.
