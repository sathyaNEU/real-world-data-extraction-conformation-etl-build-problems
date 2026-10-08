# RC40 — Fleet capacity factor fell from 93% to 88%: a reliability problem, or just more refuelling outages this year?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Fleet uptime metrics distorted by scheduled maintenance calendars (data-centre availability in years with more planned upgrades, aircraft availability around heavy-check cycles) |
| Domain | Nuclear power generation |
| Task shape | 12 · Drill-down to one leaf (fleet capacity-factor change → loss category: refuelling outages, coastdown, forced outages, derates → reactor → the reactor-category leaf with the largest increase) |
| Core method | Daily percent-power by reactor; classify each day's lost power into refuelling outage (long zero-power runs aligned with the reactor's cycle), end-of-cycle coastdown (gradual decline preceding a refuelling outage), forced outage (other zero-power runs), and derate (other partial power); capacity-weighted lost MWh by category and reactor; year-over-year change drilled to the leaf; refuelling outage count by calendar year as the timing check |
| Analytical stump | Calendar-year capacity factors swing with how many refuelling outages fall in the year: on 18-month cycles some years carry two outages per reactor and others none. Comparing annual capacity factors attributes that scheduling effect to reliability. Coastdowns also look like derates unless linked to the following refuelling outage. Only categorised losses show whether forced outages or derates actually rose |
| Primary sources | U.S. NRC Power Reactor Status Reports (daily percent power for every operating reactor); NRC operating reactor list (capacities) |

## 1. The real-world situation

A nuclear operator's fleet capacity factor fell five points year over year. The board's risk committee asked whether reliability was deteriorating
and proposed an independent reliability review costing several million dollars. The fleet's performance team believed the drop was mostly
refuelling outage timing. The committee wants the losses categorised before commissioning the review.

## 2. The decision (one deterministic recommendation)

**Whether the reliability review is commissioned (commissioned if forced-outage plus derate losses rose by ≥ 1.5 points of fleet capacity factor),
with the loss-category drill-down and the leaf reactor and category.**

Rules (fleet memo):

* Data: NRC daily power reactor status reports for the operator's reactors (memo list), years Y1 and Y2; net capacities from the NRC reactor list.
* Lost fraction per reactor-day = (100 − percent power) ÷ 100; lost MWh = lost fraction × capacity × 24.
* Zero-power runs: consecutive days at 0%.
* Refuelling outage: a zero-power run of ≥ 15 days whose start is within ± 90 days of the expected date (previous refuelling start + the reactor's
  cycle length in the memo), or the first run of ≥ 15 days in the data if no previous outage is observed.
* Coastdown: days in the 120 days before a refuelling outage start where power is < 100% and the 14-day moving average is declining.
* Forced outage: other zero-power days. Derate: other days with 0 < power < 100%.
* Fleet capacity factor = 1 − Σ lost MWh ÷ Σ (capacity × hours).
* Change by category in capacity-factor points; drill to the reactor with the largest increase in the largest-increasing category.
* Report refuelling outages starting in each year.

## 3. Why capable analysts get it wrong

* Annual capacity factor is the headline reliability metric.
* Refuelling cycles of 18 or 24 months do not align with calendar years.
* Coastdowns look like partial-power problems.
* Capacity weighting matters across reactors of different sizes.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `powerreactorstatusforlast365days_<Y1>.txt` / `_<Y2>.txt` | TXT (pipe-delimited) | ~35k each | NRC Power Reactor Status Reports | U.S. Government work (public domain) | Daily percent power |
| 2 | `nrc_operating_reactors.xlsx` | XLSX | ~95 | NRC | Public domain | Capacities, licensees |
| 3 | `refuelling_cycle_lengths.csv` | CSV | ~20 | Task author (from NRC licensee reports; cite) | Cite | Expected cycle lengths |
| 4 | `fleet_memo.pdf` | PDF | — | Task author | — | Rules in §2, reactor list |
| 5 | `risk_committee_paper.xlsx` | XLSX | — | Task author | — | Annual capacity-factor comparison |

## 5. Deterministic solution path

1. Load daily status for the fleet; join capacities; compute lost MWh.
2. Identify zero-power runs; classify refuelling outages; coastdowns; forced outages; derates.
3. Fleet capacity factors and category losses by year; changes.
4. Drill to the leaf; refuelling counts; decision; contrast with the committee paper.

## 6. Wrong paths (method errors, not misreadings)

**A — annual capacity factor comparison.** Refuelling timing read as reliability.

**B — all zero-power days as outages of one kind.** Refuelling and forced outages merged.

**C — coastdowns as derates.** Inflates partial-power losses.

**D — unweighted reactor averages.** Small units distort fleet results.

## 7. Why the stump is analytical, not semantic

All classification rules use power levels, dates and cycle lengths. The trap is calendar aggregation of cyclic maintenance.

## 8. Draft task prompt (prose)

> The risk committee wants a reliability review because our capacity factor fell five points. Categorise the losses with the fleet memo's rules and
> tell me whether reliability actually worsened. Provide `capacity_factor_losses.csv` (reactor × category × year: points), `loss_drilldown.png`, and a
> one-page `reliability_review_decision.pdf`.

## 9. Deliverables

* `capacity_factor_losses.csv` — losses by reactor, category and year.
* `loss_drilldown.png` — stacked category losses by year with the leaf highlighted.
* `reliability_review_decision.pdf` — decision, category changes and refuelling counts.

## 10. Where 25+ rubric criteria come from

* Fleet capacity factors (2 years): 2.
* Category losses (4 × 2 years): 8.
* Refuelling outages identified and counts by year: 4.
* Coastdown days identified: 2.
* Category changes and the decision: 3.
* Leaf reactor and category: 2.
* Committee contrast: 2.
* Chart elements: 2+.

## 11. Golden-output checklist

* Capacity-weighted lost MWh.
* Refuelling rule with cycle alignment; coastdown window and trend rule.
* Changes in capacity-factor points.

## 12. Build notes (scope tuning)

* Choose an operator and year pair with more refuelling outages in Y2; confirm forced plus derate losses rose by < 1.5 points.
