# ET06 — Complaint surge or taxonomy seam? Sizing a post-event staffing plan on the CFPB database

| Field | Value |
|---|---|
| Domain | Consumer finance compliance / complaint-operations workforce planning |
| Objective family | Anomaly Detection & Diagnostics (with taxonomy conformance) |
| Task shape | 17 · Periods around a change point |
| Core technique | Harmonizing a categorical taxonomy across a documented version change at sub-category grain; committed baseline + run-length excess test |
| Trap family (honest data) | Real schedule/definition change inside the baseline window; filtering on product names that only exist in one era |
| Primary sources | CFPB Consumer Complaint Database (full CSV/JSON export + field reference) |

## 1. The real-world project

A complaint-handling operations team (in-house at a lender, or a BPO serving one) sizes analyst headcount from the
CFPB's public complaint feed for its client's product family. After a high-profile industry event, leadership asks
whether the jump is **sustained** (hire permanent staff) or a **surge** (use overtime). The analyst filtered on the
product name, computed a 12-month baseline, and declared a sustained shift.

The baseline window straddled **24 April 2017**, the date the CFPB re-cut its product and issue taxonomy (e.g. "Credit
reporting" → "Credit reporting, credit repair services, or other personal consumer reports"; "Bank account or service" →
"Checking or savings account"; "Payday loan" folded into "Payday loan, title loan, or personal loan"; "Prepaid card"
folded into "Credit card or prepaid card"; mobile wallets moved to "Money transfer, virtual currency, or money service").

## 2. The business decision (one deterministic recommendation)

**Go / no-go on a permanent staffing increase for the client's product family, and, if go, the monthly complaint volume
the plan must absorb (median monthly excess over baseline during the longest excess run).**

Rules (operations planning standard):

* Product family is defined at **sub-product grain** in both eras via the CFPB field reference (the task folder includes
  the family definition as a list of old-era and new-era product/sub-product pairs).
* Period = calendar month of `Date received` (not `Date sent to company`).
* Baseline = mean and standard deviation of harmonized monthly counts over the 12 months before the event month.
* A post-event month is "in excess" if its count > baseline mean + 2 SD.
* Go if the longest run of consecutive excess months within the 16 months after the event is ≥ 6; the planning volume is
  the median of (count − baseline mean) over that run, rounded to the nearest 10 complaints.
* Snapshot: the export dated in the folder; complaints published later are out of scope.

## 3. Why this gets overlooked in real projects

* Product-name filters are written once and silently return zero rows for the other era; monthly charts show a cliff or
  a step that looks like behaviour.
* The 2017 change was not a pure rename: some old sub-products moved to *different* new products, so a product-level
  rename table is wrong in both directions.
* Field-level changes accompanied it (e.g. the `Consumer disputed?` field stops being populated after April 2017), which
  analysts notice and then wrongly assume is the only change.
* A real event coincides with the window, so any step is "explained" and nobody checks the definition.

## 4. Input package

| # | File | Format | Approx. rows | Source | License | Role |
|---|---|---|---|---|---|---|
| 1 | `complaints_snapshot.csv` | CSV | ~4–5M | CFPB Consumer Complaint Database | U.S. Gov public domain | All complaints |
| 2 | `complaints_2016_2018.json` (API extract for the window) | JSON | ~0.6M | CFPB API | Public domain | Cross-check slice |
| 3 | `cfpb_field_reference.pdf` | PDF | — | CFPB (data use / field reference pages) | Public domain | Product/sub-product lists, change notes |
| 4 | `product_family_definition.xlsx` | XLSX | ~40 pairs | Task author (from field reference) | — | Family at sub-product grain, both eras |
| 5 | `operations_planning_standard.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `event_timeline.csv` | CSV | ~10 | Public press releases (dates only) | Public | Event date |
| 7–10 | `monthly_published_counts_2016.csv` … `2019.csv` (CFPB trends export) | CSV | ~1k each | CFPB complaint trends | Public domain | Reconciliation targets |
| 11 | `us_state_fips.csv` | CSV | 56 | Census | Public domain | Optional state cut |

## 5. Deterministic solution path

1. Load snapshot; parse `Date received`; restrict to the 12 months before and 16 months after the event month.
2. Map each complaint to the family using the (product, sub-product) pairs for its era; complaints in the family's old
   sub-products that moved elsewhere in the new taxonomy are mapped by the pair list, not the product name.
3. Count per month; reconcile two months against the CFPB trends export.
4. Compute baseline mean/SD; flag excess months; find the longest run; apply go/no-go; compute planning volume.
5. Produce the comparison series under the naive product-name filter for the chart.

## 6. The traps

**Trap A — product-name filter, one era.** Baseline built on the old name only covers ~7 of 12 months (or reads zero for
May–Aug 2017) → baseline collapses → every post-event month is "excess" → false go.

**Trap B — product-level rename table.** Moves sub-products that did not move, inflating the new-era family by
categories the client does not handle; the run length changes.

**Trap C — wrong date field.** `Date sent to company` shifts months near the boundaries; the run can start or end one
month differently, which changes the go decision when the run is 5–7 months long.

**Trap D — baseline including the event month.** Inflates SD and shortens the run.

## 7. Why the data is honest

Every complaint is published as categorized at the time it was submitted; the taxonomy change is a documented,
dated product decision. Both the event and the seam are real; the analysis must separate them.

## 8. Draft task prompt (prose)

> Leadership wants a yes or no on permanent headcount for the client's complaint family after the event in the timeline
> file. Use the complaint snapshot, the family definition and our planning standard to line up the twelve months
> before the event and the sixteen after, test each later month against the committed baseline, and tell me whether the
> longest run of excess months clears the six-month bar and what monthly volume we should plan for. Deliver
> `complaint_change_point.png`, a monthly bar chart with the baseline band drawn, excess months highlighted, the longest
> run bracketed, and the April 2017 taxonomy change marked; and `staffing_decision.pdf`, one page leading with the
> decision and the planning volume, then a table of all 28 months with count, excess and flag, and one paragraph on how
> the answer would differ under a product-name filter.

## 9. Deliverables

* `complaint_change_point.png`, `staffing_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 28 monthly counts / excess flags (each a criterion), baseline mean and SD, run start/end, decision, planning volume.

## 11. Golden-output checklist

* Family mapped at sub-product grain across both eras; `Date received`; baseline excludes event month; decision follows
  the stated rule.

## 12. Build notes (scope tuning)

* Pick the product family and company (or industry total) where the harmonized run is < 6 months but the naive filter
  gives ≥ 6 (or vice versa). Test several families; credit-reporting-related families around September 2017 are a
  natural candidate, but confirm the flip on the actual snapshot.
* Freeze the snapshot file and record its download date — the database is live and counts change.
