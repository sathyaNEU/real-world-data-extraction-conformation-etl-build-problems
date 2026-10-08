# OS45 — What does auto-enrolment add? Plans that chose it were different to begin with

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing the effect of defaults (opt-out versus opt-in settings, pre-checked boxes, default plans) from observational data where adopters self-select |
| Domain | Retirement plans / HR benefits |
| Task shape | 11 · Before and after with a control (plans that adopted auto-enrolment versus matched plans that did not; the participation gain used to size a recordkeeper's auto-enrolment campaign) |
| Core method | Panel of plans across filing years; treated plans = first year reporting the auto-enrolment feature code; participation rate = active participants ÷ eligible employees (memo's proxy from Form 5500 fields); difference-in-differences against matched non-adopters (size band, industry, prior participation), with pre-trend check; projected gain for the campaign's target plans |
| Analytical stump | Comparing participation in plans with versus without auto-enrolment (cross-section) attributes to the default the fact that adopters are large, generous plans with already-high participation. Within-plan change against matched controls isolates the effect; the sized campaign value changes by a large factor |
| Primary sources | U.S. DOL EBSA Form 5500 datasets (Form 5500 and Schedule H/I, with pension feature codes) |

## 1. The real-world situation

A retirement-plan recordkeeper wants to size a campaign persuading small-business clients to adopt auto-enrolment. The analyst compared average
participation in plans with and without the feature and found a 30-point gap, implying large asset growth. Product leaders asked for an estimate
that separates the feature's effect from the type of employer that adopts it.

## 2. The decision (one deterministic recommendation)

**The participation gain (percentage points) attributable to adopting auto-enrolment, and the projected new participants and assets from the
campaign's 2,000 target plans.**

Rules (product memo):

* Data: Form 5500 filings 2015–2022 for 401(k) plans with 10–500 participants; feature codes (pension benefit codes) indicating automatic
  enrolment (codes per memo).
* Participation rate proxy = active participants with account balances ÷ total active participants (fields per memo).
* Treated: plans whose first year with the auto-enrolment code is 2018–2020, present every year 2015–2022.
* Controls: plans never reporting the code, matched 1:1 on size band, two-digit industry and participation in the year before adoption.
* Pre-trend check: treated − control difference stable (|slope| < 1 point/year) over the 3 pre years.
* DiD = mean change (2 years after vs 1 year before) treated − controls.
* Campaign: target plans' eligible non-participants × DiD gain; assets per new participant from the memo.
* Report the cross-sectional gap for contrast.

## 3. Why capable analysts get it wrong

* Cross-sectional differences are the most available comparison.
* Adopters differ systematically; selection inflates the gap.
* Matching on pre-adoption participation and checking pre-trends address it.
* The participation proxy must be consistent across years and plan sizes.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–8 | `f_5500_<yyyy>_latest.csv` (2015–2022) | CSV | ~800k each | DOL EBSA Form 5500 datasets | U.S. Gov public domain | Plan filings, participants, feature codes |
| 9–16 | `F_SCH_I_<yyyy>_latest.csv` | CSV | ~600k each | DOL EBSA | Public domain | Small-plan financials |
| 17 | `form5500_data_dictionary.pdf` | PDF | — | DOL EBSA | Public domain | Fields, codes |
| 18 | `product_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 19 | `analyst_cross_section.xlsx` | XLSX | — | Task author | — | Naive gap |
| 20 | `matching_spec.json` | JSON | — | Task author | — | Matching rules |
| 21 | `campaign_targets.json` | JSON | — | Task author | — | Target plan profile |

## 5. Deterministic solution path

1. Build the plan panel; identify adoption years; participation proxy.
2. Match controls; check pre-trends.
3. DiD gain; campaign projection.
4. Contrast with the cross-sectional gap.

## 6. Wrong paths (method errors, not misreadings)

**A — cross-sectional gap.** Selection bias.

**B — before/after without controls.** Secular trends.

**C — matching on post-adoption variables.** Bias.

**D — inconsistent participation proxy.** Noise and bias.

## 7. Why the stump is analytical, not semantic

The panel, matching and DiD are specified. The trap is selection into treatment when sizing a default's effect.

## 8. Draft task prompt (prose)

> How much does adopting auto-enrolment really raise participation, and what is our campaign worth? Estimate the effect with the matched
> before/after design in the product memo. Provide `did_results.csv` (group × year: participation), `event_study.png`, and a one-page
> `campaign_sizing.pdf`.

## 9. Deliverables

* `did_results.csv`, `event_study.png`, `campaign_sizing.pdf`.

## 10. Where 25+ rubric criteria come from

* Treated/control counts; yearly means (8 × 2); pre-trend slope; DiD; projection; contrast.

## 11. Golden-output checklist

* Feature codes; panel balance; proxy; matching; pre-trend; DiD; projection.

## 12. Build notes (scope tuning)

* Confirm the cross-sectional gap is ≥ 2× the DiD estimate.
