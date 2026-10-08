# RC03 — Which incidents caused the bad month? Count the knock-on delay they created, not just where trains were late

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Incident blast-radius analysis (one service failure cascading through dependents; one late truck delaying a whole route) |
| Domain | Rail operations |
| Task shape | 12 · Drill-down to one leaf (route → incident category → responsible organisation → the single incident category whose primary plus reactionary delay explains most of the period's deterioration) |
| Core method | Delay attribution records: each delay minute is attributed to an incident; reactionary (knock-on) minutes are linked to the originating incident; compute total impact per incident = primary + reactionary minutes; compare periods by incident category and responsible manager; drill down by route |
| Analytical stump | Ranking causes by primary minutes or by where delays were recorded ignores that some incidents (infrastructure failures at junctions, early-morning fleet issues) generate large reactionary delays across the network. Counting reactionary minutes under their originating incident changes the ranking of causes and owners |
| Primary sources | Network Rail historic delay attribution data (transparency datasets, by four-weekly period) |

## 1. The real-world situation

A train operator's performance fell sharply in one four-weekly period. The performance team ranked causes by delay minutes recorded against each
incident category on its own trains and blamed fleet faults. The infrastructure manager countered that a few signalling failures at a busy junction
caused most of the knock-on delay.

## 2. The decision (one deterministic recommendation)

**The incident category (and responsible organisation) that accounts for the largest share of the increase in total delay minutes (primary +
reactionary) versus the same period last year, on the operator's services.**

Rules (performance memo):

* Data: Network Rail delay attribution files for the period and the same period last year (operator code in memo).
* Each record: incident number, incident reason code, responsible manager, delay minutes, event type (primary/reactionary per data fields).
* Total impact per incident = Σ minutes over all delay records linked to that incident (including reactionary minutes to the operator's trains).
* Categories: incident reason groups from `reason_code_groups.csv` (e.g., track, signalling, fleet, traincrew, external, weather).
* Drill: route → category → responsible organisation; choose the leaf with the largest increase in total impact.
* Contrast: ranking by primary minutes only.

## 3. Why capable analysts get it wrong

* Primary delay is visible and directly attributable.
* Reactionary delay often exceeds primary delay for network incidents.
* The same incident affects many trains and operators.
* Year-over-year comparisons by period require the same period definitions.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Transparency_<yy-yy>_P<nn>.csv` (current period) | CSV | ~400k delay records | Network Rail Data feeds / transparency | Open Government Licence (Network Rail) | Delay attribution |
| 2 | `Transparency_<yy-yy>_P<nn>.csv` (last year) | CSV | ~400k | Same | OGL | Comparison |
| 3 | `delay_attribution_guide.pdf` | PDF | — | Delay Attribution Board (DAPR) | Public | Codes, primary/reactionary rules |
| 4 | `reason_code_groups.csv` | CSV | ~300 | Task author (from DAPR codes) | — | Category mapping |
| 5 | `performance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `performance_team_ranking.xlsx` | XLSX | ~10 | Task author | — | Primary-minutes ranking |
| 7 | `route_codes.csv` | CSV | ~20 | Network Rail | OGL | Routes |

## 5. Deterministic solution path

1. Filter operator; link reactionary records to incidents; total impact per incident.
2. Aggregate by route, category and organisation for both periods.
3. Increases; drill-down; leaf; contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — primary minutes only.** Misses knock-on impact.

**B — counting incidents rather than minutes.** Wrong weighting.

**C — mixing operators.** Network-level minutes not on the operator's services.

**D — calendar months instead of four-weekly periods.** Misaligned comparison.

## 7. Why the stump is analytical, not semantic

The attribution rules and drill are specified. The trap is ignoring propagation when attributing impact.

## 8. Draft task prompt (prose)

> What really caused our bad period? Attribute primary and reactionary delay to originating incidents and drill down as the performance memo
> specifies. Provide `delay_drilldown.csv` (level: category, organisation, minutes this year and last, increase), `delay_waterfall.png`, and a one-page
> `period_rca.pdf`.

## 9. Deliverables

* `delay_drilldown.csv`, `delay_waterfall.png`, `period_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* Route-level increases; category increases (8); organisation split; top incidents (5); leaf; contrast.

## 11. Golden-output checklist

* Operator filter; incident linking; total impact; categories; drill path.

## 12. Build notes (scope tuning)

* Choose a period with a major infrastructure incident; confirm primary-only ranking points to fleet.
