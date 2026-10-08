# RC46 — Persistent absence doubled to one pupil in five: a collapse among a large group, or a modest shift that a threshold amplified?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Share-above-threshold KPIs (share of requests slower than 1 s, share of customers with NPS ≤ 6, share of accounts overdue 30+ days) that jump when the whole distribution shifts slightly |
| Domain | Education / public policy |
| Task shape | 03 · Bridge between two totals (persistent-absence rate, pre-pandemic year → current year, bridged into the part explained by each school's mean absence shift at unchanged distribution shape and the part from changes in shape and composition) |
| Core method | For each school, fit a beta distribution of pupil absence rates matching the school's reference-year overall absence rate (mean) and persistent-absence share (P(X ≥ 10%)); keep the school's shape and move its mean to the current year's absence rate; predicted persistent-absence share summed over schools with current enrolments; mean-shift component = predicted − reference; shape and composition component = actual − predicted |
| Analytical stump | Persistent absence is the share of pupils above a 10% cut-off. When the distribution's mean moves from about 4.7% toward 7.5%, a large mass of pupils just under the threshold crosses it, so the share roughly doubles without any change in the distribution's shape. Reading the doubling as a new, distinct group in crisis leads to targeted programmes when a whole-population shift is the cause |
| Primary sources | Department for Education (England) — pupil absence in schools, school-level data (overall absence rate, persistent absence rate, enrolments) via Explore Education Statistics |

## 1. The real-world situation

A government's education department reported that persistent absence had doubled to over one pupil in five since before the pandemic. Ministers
proposed a programme of intensive case-work aimed at "persistently absent pupils", as though a distinct group had emerged. Analysts argued that the
whole distribution had shifted and that a threshold metric was amplifying a modest mean change. The department must choose between a universal
attendance policy and targeted case-work.

## 2. The decision (one deterministic recommendation)

**The policy emphasis — universal (if the mean-shift component explains ≥ 70% of the rise) or targeted (otherwise) — with the bridge in percentage
points.**

Rules (analysis memo):

* Data: school-level absence statistics for the reference year (2018/19) and current year (memo); state-funded primary, secondary and special
  schools; schools present in both years with ≥ 30 enrolled pupils.
* Per school: m = overall absence rate (sessions missed ÷ possible), p = persistent-absence rate (share of enrolments missing ≥ 10% of sessions).
* Beta fit (reference year): find shape κ such that a Beta(m·κ, (1 − m)·κ) distribution has P(X ≥ 0.10) = p; schools with p = 0 or p = 1 or no
  solution in κ ∈ [1, 500] use the national median κ.
* Prediction: current-year p̂ = P(X ≥ 0.10) under Beta(m_cur·κ, (1 − m_cur)·κ).
* National rates weighted by current enrolments (predicted and actual) and by reference enrolments (reference rate).
* Bridge: reference PA → + mean shift (Σ predicted − reference) → + shape and composition (actual − predicted) → current PA.
* Universal if mean-shift ÷ total rise ≥ 70%.

## 3. Why capable analysts get it wrong

* "Doubling" of a threshold share reads as a doubling of a problem group.
* Threshold metrics respond nonlinearly to mean shifts.
* School-level heterogeneity matters; a national single distribution misleads.
* Enrolment changes alter weights.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `absence_school_level_<ref>.csv` | CSV | ~22k | DfE Explore Education Statistics (pupil absence in schools in England) | Open Government Licence v3.0 | Reference year by school |
| 2 | `absence_school_level_<cur>.csv` | CSV | ~22k | Same | OGL v3.0 | Current year by school |
| 3 | `absence_national_<years>.csv` | CSV | ~1k | Same | OGL v3.0 | Published national rates |
| 4 | `absence_methodology.html` | HTML | — | DfE | OGL v3.0 | Definitions |
| 5 | `analysis_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `ministerial_casework_proposal.pdf` | PDF | — | Task author | — | Targeted-programme rationale |

## 5. Deterministic solution path

1. Filter schools and phases; match across years; compute m and p.
2. Fit κ per school; fall-backs; national median κ.
3. Predict p̂; weighted national rates; bridge.
4. Decision; contrast with the proposal and with a single national distribution.

## 6. Wrong paths (method errors, not misreadings)

**A — doubling read as a new group.** Ignores the threshold mechanics.

**B — one national distribution.** Misses heterogeneity in school means and shapes.

**C — linear extrapolation of PA from the mean.** Understates the threshold amplification.

**D — unmatched schools.** Openings and closures enter as spurious shape changes.

## 7. Why the stump is analytical, not semantic

All definitions and fitting rules are explicit. The trap is reading a threshold share as a count of a distinct population.

## 8. Draft task prompt (prose)

> Ministers want targeted case-work because persistent absence doubled. Bridge the change with the analysis memo's school-level distribution method and
> tell me whether the rise is a broad shift or a distinct group. Provide `persistent_absence_bridge.csv` (component: points), `threshold_amplification.png`,
> and a one-page `attendance_policy_note.pdf`.

## 9. Deliverables

* `persistent_absence_bridge.csv` — reference, mean shift, shape and composition, current.
* `threshold_amplification.png` — reference and shifted distributions around the 10% threshold for a typical school, with the national bridge.
* `attendance_policy_note.pdf` — policy emphasis and why the doubling misleads.

## 10. Where 25+ rubric criteria come from

* School filtering and matching counts: 4.
* κ fits (median, fall-backs): 3.
* National reference, predicted and actual rates: 3.
* Bridge components and closure: 4.
* Phase breakdown (primary, secondary, special) of the bridge: 6.
* Decision and contrasts: 4.
* Chart elements: 2+.

## 11. Golden-output checklist

* Beta parameterisation by mean and κ; P(X ≥ 0.10) target.
* Fall-back κ rule; enrolment weights.
* Bridge closure.

## 12. Build notes (scope tuning)

* Confirm on the data that the mean-shift component exceeds 70% of the rise; if phase-level results differ, report them but keep the national rule.
