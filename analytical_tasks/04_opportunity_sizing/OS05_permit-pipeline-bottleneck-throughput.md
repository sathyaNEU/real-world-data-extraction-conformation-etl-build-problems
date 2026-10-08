# OS05 — Speeding up permits: adding staff anywhere but the bottleneck buys nothing

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Throughput improvement in multi-stage operations (manufacturing lines, fulfilment centres, hiring pipelines, code-review → CI → deploy) where only the constraint stage limits output |
| Domain | Government operations / construction permitting |
| Task shape | 09 · Funnel or chain of stages (filing → plan examination → approval → permit issuance; the stage where a fixed budget for staff buys the most additional permits issued per year) |
| Core method | Stage capacity from historical completions per staff-week (memo staffing table); utilisation and queue growth per stage; system throughput = min over stages of capacity × pass-through-adjusted demand; marginal throughput from adding capacity at each stage (theory of constraints) |
| Analytical stump | Sizing the gain from hiring by multiplying each stage's capacity increase by its own volume assumes every stage limits output. In a serial process only the bottleneck does; adding capacity upstream just lengthens the queue at the constraint. The bottleneck is identified from completion rates and growing queues, not from the slowest median duration |
| Primary sources | NYC Department of Buildings job application filings and permit issuance (NYC Open Data) |

## 1. The real-world situation

A building department has budget for 10 additional staff. The operations analyst sized the benefit of placing them in each stage as the
stage's current volume × the percentage capacity increase and recommended plan examination, which has the longest median time. Permits
issued per year did not move after a previous hiring round there.

## 2. The decision (one deterministic recommendation)

**The stage that receives the 10 staff and the additional permits issued per year that it yields.**

Rules (operations memo):

* Data: DOB job application filings and permit issuance for new-building and major-alteration jobs, 2022–2023; stage timestamps (pre-filing,
  filed, plan exam assigned, approved, permit issued) per the memo's field mapping.
* Stage completions per week and work in progress (WIP) at week end per stage.
* Capacity per stage = mean weekly completions in weeks where WIP at the stage start > 50 (busy weeks), ÷ staff (from `staffing_table.csv`)
  × staff.
* Pass-through: share of jobs completing a stage that proceed to the next within 180 days.
* System throughput (permits/year) = 52 × min_k [capacity_k ÷ Π_{j<k} pass-through_j adjusted per memo].
* Gain from 10 staff at stage k: recompute capacity_k with +10 staff; gain = new throughput − current.
* Choose the stage with maximum gain.

## 3. Why capable analysts get it wrong

* Long durations draw attention, but duration reflects queues created by downstream or upstream constraints.
* Local capacity increases don't propagate past the bottleneck.
* Pass-through losses mean upstream volume overstates downstream demand.
* Capacity must be measured when the stage is busy, not averaged over idle weeks.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `DOB_Job_Application_Filings.csv` | CSV | ~2.7M | NYC Open Data | NYC Open Data terms (open) | Jobs with stage dates |
| 2 | `DOB_NOW_Build_Job_Application_Filings.csv` | CSV | ~800k | NYC Open Data | Open | Newer system filings |
| 3 | `DOB_Permit_Issuance.csv` | CSV | ~3.8M | NYC Open Data | Open | Permits issued |
| 4 | `field_mapping.json` | JSON | ~20 | Task author | — | Stage timestamps across systems |
| 5 | `staffing_table.csv` | CSV | 4 | Task author (from public budget documents) | — | Staff per stage |
| 6 | `operations_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `analyst_volume_based_sizing.xlsx` | XLSX | 4 | Task author | — | Naive sizing |
| 8 | `goldratt_toc_citation.pdf` | PDF | — | Cite | Cite | Theory of constraints |
| 9 | `weekly_stage_flows.parquet` | Parquet | ~400 | Derived | Open | Completions and WIP by week |

## 5. Deterministic solution path

1. Harmonise stage timestamps across systems; filter job types and years.
2. Weekly completions and WIP per stage; busy-week capacity; pass-throughs.
3. System throughput; gains for each stage; choose.
4. Contrast with volume-based sizing.

## 6. Wrong paths (method errors, not misreadings)

**A — volume × % capacity increase per stage.** Ignores the constraint.

**B — bottleneck = longest median duration.** Confuses waiting with capacity.

**C — capacity from all weeks.** Underestimates capacity of non-binding stages.

**D — ignoring pass-through losses.** Wrong downstream demand.

## 7. Why the stump is analytical, not semantic

Stages, capacity and throughput are defined. The trap is local versus system optimisation in serial processes.

## 8. Draft task prompt (prose)

> Where should the 10 new staff go to issue the most additional permits? Model the pipeline as the operations memo specifies, find the bottleneck,
> and size each option. Provide `stage_capacity.csv` (stage: staff, capacity, pass-through, WIP trend, gain from +10), `wip_by_stage.png`, and a
> one-page `staffing_decision.pdf`.

## 9. Deliverables

* `stage_capacity.csv`, `wip_by_stage.png`, `staffing_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 stages × (capacity, pass-through, WIP trend, gain) = 16; throughput; chosen stage; contrast; busy-week counts.

## 11. Golden-output checklist

* Timestamp harmonisation; busy-week capacity; pass-through; min-throughput; gains; choice.

## 12. Build notes (scope tuning)

* Confirm the longest-duration stage is not the capacity bottleneck.
