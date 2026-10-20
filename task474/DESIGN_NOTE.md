# task474 design note: the Regional Opportunity Fund's FY2027 split across the new planning regions

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task474.json` (architecture v1), registered 2026-10-20 after a pull. Guard
  check WARN only: `three_rules.strategy_risk` (time_semantics; answered by the analyst test below, every field read
  right still files the wrong split), `repeat.gate_g` and `overuse.gate_g` (method_or_model_selection, as task271 v2's
  callback model and task468 v4's linkage-corrected mortality: the label is shared, the mechanism is not). The first
  check BLOCKed on `test.same_driver_older` (gap time, G13, method_or_model_selection, as task229 v2, task242, task461
  and task501 v4); the decisive generator is redrawn to G2, which is the honest label (the town data's grain is a
  five-year period, the estimand's a single year), with G13 kept under it. Nearest driver task58 v15 at 0.07.
- **Seed:** ET31 (Connecticut's nine planning regions replaced its eight counties as county-equivalents; a state agency
  splits a fixed $12,000,000 anti-poverty program across the regions on a five-vintage average of the population below
  poverty; older vintages exist only for the counties; the analyst used an area crosswalk). Kept: the world (a New
  England state whose county-equivalents changed mid-series, towns nesting in both geographies), the decision (a fixed
  grant split across the nine regions) and the quantity (each region's average residents in poverty over five years).
  Dropped as the decisive step: the seed's move (rebuild from towns instead of an area crosswalk), which a careful
  analyst takes unprompted; it survives as Layer 1.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (official
  time-series production: an annual series rebuilt across a break, with temporal disaggregation of period data) /
  Data Extraction & Conformation (ETL). The State Data Center's annual model-based poverty estimates (former counties
  for 2020 to 2022, planning regions from 2023), the Census Bureau's five-year town releases (2015-2019 and 2020-2024)
  and the town-county-region relationship are conformed into one region-by-year series, 2020 to 2024, on the new
  geography; the Fund is split on it.
- **Shape:** 05, an allocation to a fixed total: each of the nine regions' FY2027 amounts from $12,000,000.
- **Strategy:** time_semantics (the honest family: what moment a period average describes), Layer 2 estimation_fit,
  pattern none with G2 decisive (five-year town windows against single-year estimates), G13 (the window's span against
  the year) and G6 (the poor's drift from the cities to the suburbs under every split). Gate G method_or_model_selection:
  anchoring each window at the year it holds against at the middle of its span, the native years pinning it.
- **World:** the United States, an unnamed New England state with no county government since the 1960s. The state's
  eight former counties were statistical areas only; a 2022 statute made its nine regional councils of governments the
  county-equivalents, and the State Data Center (SDC) moved its annual poverty estimates to the planning regions with
  the 2023 estimates. The Regional Opportunity Fund ($12,000,000 for FY2027, July 2026 to June 2027) is split among the
  nine councils in proportion to each region's average residents in poverty over the five latest estimate years, 2020
  to 2024 (the Fund's allocation rule, administered by the Office of Policy and Management). Personas from `guard.py
  names --geo "United States" --seed 474`: Wendy Taylor (Director, State Data Center), Mitchell Clark (SDC demographer)
  and Paige Hodges (OPM grants manager).
- **Forcing fact:** the Secretary of the Office of Policy and Management signs the FY2027 allocation; the SDC's table
  goes to OPM in October 2026. The call faces forward (the FY2027 grant); its quantity is the closed 2020 to 2024 years
  the rule names (a retrospective quantity with its reason: the rule allocates on the latest five estimate years).
- **Forum and forcing event:** minister_or_cabinet (the OPM Secretary signs), budget_or_appropriation (the FY2027 round).
  Organisation research_or_statistics_office (the SDC prepares the table); role statistical_office_head.
- **Data-native sentence:** the towns' five-year survey releases are averages over five years of a distribution that is
  moving (the poor of the old mill cities moving out to the inner suburbs across the new region lines inside the same
  former county), so the 2020-2024 release describes the towns around 2022 and the 2015-2019 release around 2017, and a
  former county's single-year estimate for 2020 or 2021 split by the release that holds the year is split by a
  distribution up to two years ahead of it.
- **The WHAT screen.** Population: the residents in poverty of the region's towns (the SDC's estimates; for 2020 to
  2022, the part of each former county's estimate living in the region's towns that year). Outcome: residents in
  poverty, a count. Window: each of 2020, 2021, 2022, 2023 and 2024, averaged with equal weight. Unit: persons, then
  dollars. Comparison: each region's share of the nine regions' sum. The decisive step settles none of them: it is how
  a year's town distribution inside a former county is estimated from two five-year releases (HOW, forced by the data:
  the native years 2023 and 2024 sit on the line through the releases placed at their middle years and off the line
  through their last years).
- **Deliverables (planned):** `rof_fy2027_region_poverty_2020_2024.csv` (the conformed series, region by year) and
  `rof_fy2027_allocation_memo.docx` (the allocation to OPM with a chart).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, survey research: the official-statistics patterns are series
    breaks, revisions and benchmarking; none carries period-average survey windows placed at their middle years to
    disaggregate a single year, which is this build's own pattern.
  - `stumping/references/client/two-layer-task-design.md`: estimation_fit (the data's real structure: each window is an
    average over a span, an interval-aggregated observation of a moving quantity).
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task123 v2 splits interval totals onto calendar
    periods by a measured daily shape (a rate inside one interval); task470 completes a sensor record with the units it
    never sees (an auxiliary choice); task461 carries a short record through a long correlated one. None places two
    period averages at their middle years to interpolate a share that drifts.

## Tried and rejected

- 2026-10-20, at the draw: the seed's own move (rebuild from towns rather than an area crosswalk): a careful analyst
  rebuilds from towns unprompted; kept as Layer 1.
- 2026-10-20, at the draw: re-basing the 2020 to 2021 estimates onto the population the 2020 census revised (the silent
  break behind the loud geography break): the population base is the series' version basis, an axis that must be
  filed, and filing it makes the step rule application while leaving it open forks the call against the published
  figures; dead by the WHAT screen.
- 2026-10-20, at the draw: the auxiliary for splitting the former counties (SNAP recipients over each region's take-up,
  measured where both are published): the same insight as task470 and task448 (the ratio the target actually scales
  with, measured where both are observed); a clone in the lane.
- 2026-10-20, at the draw: the five-year window centred on each year picked from a full run of overlapping releases: a
  lookup once the idea is there, and the one-window routes (2018-2022 or 2019-2023 for both years) sit within half a
  year of the golden, about $5,000 a region; replaced by two non-overlapping releases, where every route but the
  interpolation at the middle years misses by a year of drift or more.
- 2026-10-20, at the draw: a region formed by differencing overlapping published geographies (the pieces pinned by two
  partitions' margins): exact arithmetic with no field in it; the swap test reads it the same for sales territories.
