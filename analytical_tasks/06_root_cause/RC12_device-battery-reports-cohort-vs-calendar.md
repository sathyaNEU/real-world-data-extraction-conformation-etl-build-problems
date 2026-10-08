# RC12 — Battery complaints tripled after a firmware update: calendar time or manufacture cohort?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Consumer and enterprise hardware field-failure spikes (phone batteries, laptop displays, network-gear clock components) where a software release coincides with a bad component lot reaching its failure age |
| Domain | Medical devices / hardware reliability |
| Task shape | 17 · Periods around a change point (a Lexis table of reports by manufacture month × months in service; is the break along calendar time, at the firmware date, or along manufacture cohort, at a component change?) |
| Core method | Battery-problem reports from MAUDE device problem codes; Lexis table of event counts by manufacture month (cohort) × age in months at event; keep only cells fully observed after a reporting-delay buffer; Poisson log-linear models: cohort + age (null), + calendar step at the firmware month (period model), + early-age excess for cohorts ≥ C (cohort model, C scanned); choose by AIC; locate C* by profile likelihood |
| Analytical stump | A calendar-time chart of report counts shows a step right after the firmware release, so the firmware is blamed. Calendar time = cohort + age, so the same step appears when cohorts built after a cell-supplier change start failing at 3–9 months in service. Separating the clocks needs the age–cohort table. Without restricting to fully observed cells, young cohorts look healthy simply because they have not been in service long enough |
| Primary sources | U.S. FDA MAUDE (Manufacturer and User Facility Device Experience) bulk files — master, device and device-problem files; FDA medical device recalls database (validation only) |

## 1. The real-world situation

A home-use medical device maker saw battery-related adverse-event reports roughly triple within two quarters of a firmware release that changed
power management. Software engineering prepared a rollback. Supplier quality pointed out that the battery-cell supplier had also changed at about
the same time. A field action is expensive either way: a firmware rollback touches every unit, a cohort-scoped battery replacement touches only
some.

## 2. The decision (one deterministic recommendation)

**The root-cause axis (calendar/firmware or manufacture cohort) and the field-action scope: a firmware rollback, or a battery replacement for units
manufactured from boundary month C\* onward, with the model evidence.**

Rules (quality memo):

* Data: MAUDE reports for the memo's product code and manufacturer, event dates in the memo's window; join device and device-problem files on
  MDR report key.
* Battery reports: any report with a device problem code in the memo's battery code set (e.g., battery problem, premature discharge, failure to
  charge). Deduplicate on MDR report key.
* Required fields: event date and device manufacture date; age = whole months from manufacture to event. Drop ages < 0 or > 60. Report the share of
  battery reports dropped for missing manufacture date, before and after the firmware month.
* Reporting delay: exclude events in the last 6 months of the window (median received-minus-event delay plus margin, per memo).
* Observable cells: cohort c, age a kept only if c + a ≤ last usable event month, and a ≤ 36.
* Models (Poisson, log link, counts by c × a): M0 = cohort + age factor; MP = M0 + I(c + a ≥ firmware month); MC(C) = M0 + I(c ≥ C) × I(a ≤ 12),
  for C over the 24 months around the firmware month.
* Choose the lowest AIC among M0, MP and the best MC(C). C\* = argmax likelihood of MC(C).
* Action: cohort model → battery replacement for cohorts ≥ C\*; period model → firmware rollback; null → no field action.

## 3. Why capable analysts get it wrong

* The firmware date is a vivid, plausible cause that lines up with the calendar spike.
* Three time axes (manufacture, age, calendar) are linked; only two are free.
* Right truncation makes the newest cohorts look reliable.
* Report filing lags make the most recent months look quiet.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `mdrfoi_<years>.txt` | TXT (pipe-delimited) | ~2M | FDA MAUDE downloads | U.S. Government work (public domain) | Report master: event and received dates |
| 2 | `foidev_<years>.txt` | TXT | ~2M | FDA MAUDE | Public domain | Device: product code, manufacturer, manufacture date |
| 3 | `foidevproblem_<years>.txt` | TXT | ~3M | FDA MAUDE | Public domain | Device problem codes per report |
| 4 | `deviceproblemcodes.csv` | CSV | ~1,200 | FDA | Public domain | Problem code descriptions |
| 5 | `device_recalls_<product_code>.json` | JSON | ~50 | openFDA device recall endpoint | Public domain | Validation only |
| 6 | `quality_memo.pdf` | PDF | — | Task author | — | Rules in §2, product code, firmware month, battery code set |
| 7 | `firmware_rollback_proposal.xlsx` | XLSX | — | Task author | — | Software team's calendar-time chart |

## 5. Deterministic solution path

1. Filter product code and manufacturer; join problem codes; keep battery reports; deduplicate.
2. Compute age; report missing-manufacture-date shares by period; apply the delay buffer and observability rule.
3. Build the Lexis table; fit M0, MP and the MC(C) scan; compare AIC; find C\*.
4. Map the winning model to the action; validate C\* against the recall record's manufacture-date range.

## 6. Wrong paths (method errors, not misreadings)

**A — before/after counts around the firmware month.** Calendar step attributed to firmware; the cohort explanation is never tested.

**B — no observability restriction.** Young cohorts have only early ages observed, so their cumulative report counts look low and C\* moves late
or disappears.

**C — dating by received date.** Filing lags smear the step and shift it by months.

**D — pooled age-at-failure fit.** A Weibull on all reports finds an early-failure mode but cannot say which units have it.

## 7. Why the stump is analytical, not semantic

Reports are selected by coded problem fields, not free text, and every model is specified. The trap is the age–period–cohort identity and the
truncation of young cohorts.

## 8. Draft task prompt (prose)

> Battery complaints tripled after our firmware release and software wants to roll it back. Supplier quality thinks it is the new cell supplier.
> Use the quality memo's age–cohort method on the MAUDE data to decide which it is and what the field action should cover. Provide
> `lexis_model_comparison.csv` (model: deviance, AIC, key coefficients, C\*), `lexis_heatmap.png`, and a one-page `field_action_decision.pdf`.

## 9. Deliverables

* `lexis_model_comparison.csv` — M0, MP and MC(C) for every scanned C.
* `lexis_heatmap.png` — reports by cohort × age, with the firmware diagonal and C\* marked.
* `field_action_decision.pdf` — winning model, scope, validation against the recall record, and why the calendar chart misled.

## 10. Where 25+ rubric criteria come from

* Filter counts (product reports, battery reports, dropped for missing manufacture date by period, dropped for delay): 6.
* Observable-cell rule applied; table dimensions: 2.
* Coefficients and AIC for M0, MP and best MC: 6.
* C\* and its profile-likelihood interval: 3.
* Winning axis and action: 2.
* Validation against recall dates; contrast with the rollback proposal: 3.
* Heatmap elements (diagonal, C\*): 3+.

## 11. Golden-output checklist

* Problem-code filter and deduplication by report key.
* Age in whole months; delay buffer of 6 months; observability rule.
* Three model families exactly as specified; AIC comparison; C\* scan window.
* Action follows the winning model.

## 12. Build notes (scope tuning)

* Pick a product code and manufacturer with an FDA recall that cites a battery issue limited to a manufacture-date range, and a documented software
  release within ±3 months of the start of that range. Confirm that the calendar step is visible and that MC(C\*) beats MP on AIC.
