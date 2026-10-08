# RC38 — Elevator availability fell from 97% to 94%: are elevators breaking more often, or staying broken longer?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | SRE availability decompositions (incident frequency vs time to restore), fleet uptime (failure rate vs repair turnaround), where the lever — replacement vs process — depends on which factor moved |
| Domain | Transit infrastructure / asset maintenance |
| Task shape | 03 · Bridge between two totals (unplanned elevator downtime hours, reference year → current year, bridged by equipment count, outage frequency per unit and mean outage duration, with long outages separated) |
| Core method | Outage records clipped to each year; downtime = units × outages per unit × mean duration; LMDI decomposition of the change; separate class for long outages (> 30 days) whose durations are heavy-tailed; censored open outages clipped at year-end; planned outages excluded |
| Analytical stump | Outage counts are the visible maintenance metric and rose, so ageing equipment and capital replacement get the blame. Availability, however, depends on frequency times duration, and duration is dominated by a heavy tail of long outages waiting for parts or contractor work. Including planned outages, dropping outages still open at year-end, or summarising duration with a median all distort which factor moved |
| Primary sources | MTA Open Data (data.ny.gov) — NYC Transit elevator and escalator outage history and monthly availability |

## 1. The real-world situation

A transit agency's elevator availability fell from 97% to 94%, drawing complaints from disability advocates. The maintenance contractor said that
ageing units were failing more often and requested accelerated capital replacement. The agency's asset manager suspected repair times had grown
because of parts shortages and contractor staffing. Replacement and process fixes come from different budgets.

## 2. The decision (one deterministic recommendation)

**The programme funded — capital replacement (if the frequency effect is larger) or a parts-and-staffing repair programme (if the duration effect is
larger) — with the LMDI bridge in downtime hours by outage class.**

Rules (asset memo):

* Data: elevator outage records (equipment ID, start, end, outage type) for the reference and current years; equipment inventory by year.
* Outages: unplanned only (planned maintenance and capital-project outages excluded per the outage-type field); outages crossing year boundaries
  clipped; outages still open at the data extract date clipped at year-end.
* Classes: short (≤ 30 days of clipped duration) and long (> 30 days).
* Per class: units U (elevators in service during the year), frequency F = outages ÷ U, duration D = mean clipped duration in hours.
* Downtime_class = U × F × D; LMDI-I effects for U, F and D per class, summed.
* Availability check: 1 − downtime ÷ (U × 8,760) compared with the published monthly availability average (difference reported).
* Fund replacement if Σ frequency effects > Σ duration effects; otherwise the repair programme.

## 3. Why capable analysts get it wrong

* Outage counts are the reported maintenance KPI.
* Durations are heavy-tailed; a handful of long outages carry most downtime.
* Censored and planned outages must be handled consistently.
* Equipment count changes when new elevators open.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `nyct_elevator_escalator_outages_<years>.csv` | CSV | ~150k | MTA Open Data (data.ny.gov) | NY Open Data terms (public) | Outage records |
| 2 | `nyct_elevator_escalator_availability_monthly.csv` | CSV | ~40k (equipment × month) | MTA Open Data | Same | Published availability |
| 3 | `nyct_equipment_inventory.csv` | CSV | ~600 | MTA Open Data | Same | Equipment list and in-service dates |
| 4 | `asset_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `contractor_replacement_request.xlsx` | XLSX | — | Task author | — | Count-based argument |
| 6 | `ang_2004_lmdi_citation.pdf` | PDF | — | Cite | Cite | LMDI method |

## 5. Deterministic solution path

1. Filter elevators and unplanned outages; clip to years; classify short and long.
2. U, F, D per class and year; downtime; availability check.
3. LMDI effects; totals by factor.
4. Decision; duration distribution (share of downtime in the top 5% of outages); contrast with the contractor's request.

## 6. Wrong paths (method errors, not misreadings)

**A — outage counts only.** Frequency blamed by default.

**B — median duration.** Ignores the tail that carries downtime.

**C — planned outages included.** Capital-project closures inflate both frequency and duration.

**D — open outages dropped.** Long, unresolved outages vanish from the current year.

## 7. Why the stump is analytical, not semantic

The outage-type field and clipping rules are given; the decomposition is specified. The trap is a product identity with a heavy-tailed factor.

## 8. Draft task prompt (prose)

> Our contractor wants accelerated elevator replacement because outages are up. Decompose the change in unplanned downtime with the asset memo's
> method and tell me whether frequency or duration drove it. Provide `downtime_bridge.csv` (class × factor effects), `downtime_bridge.png`, and a
> one-page `elevator_programme_decision.pdf`.

## 9. Deliverables

* `downtime_bridge.csv` — U, F, D by class and year; LMDI effects.
* `downtime_bridge.png` — waterfall by factor with a duration-distribution inset.
* `elevator_programme_decision.pdf` — decision, bridge and tail statistics.

## 10. Where 25+ rubric criteria come from

* Filtering and clipping counts: 4.
* U, F, D for 2 classes × 2 years: 12.
* LMDI effects (6) and closure: 7.
* Availability check: 1.
* Decision and contrast: 3.

## 11. Golden-output checklist

* Unplanned outages only; clipping and censoring rules.
* 30-day class split.
* LMDI-I with exact closure.

## 12. Build notes (scope tuning)

* Choose a year pair in which outage counts rose modestly while long outages lengthened; confirm the duration effect exceeds the frequency effect.
