# task474 design note: the Regional Opportunity Fund's FY2027 split across the new planning regions

Status lives in `pipeline.json`; this note holds the design. Read `## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each region's residents in poverty
  in 2020 to 2022, built by temporal disaggregation with a benchmarked indicator (each town's monthly SNAP recipients
  scaled to its own 2020-2024 B17001 count), which divides the SDC's former county estimates; the swap to sales
  territories loses the survey period average, the take-up ratio and the model totals. Layer 1: the releases' layouts,
  first against revised estimates, the re-keyed GEO_IDs, DSS's spellings with its UNKNOWN and STATE TOTAL rows, the
  survey's margins and cells, two calendars, awards in thousands; each asserted neutral or loud (checks.py R2). Layer
  2: the estimator of a town's year; the easy route (the release's shares) files Greater Ormsby $1,620,000 and Mill
  River Valley $2,280,000 on the clean truth (R3a), the decisive step alone files the golden (R3b), no plant ships
  (R3c, positive controls on every document).
- **leak.py (REVIEW, no LEAK), each line ruled:** "the model" in the methods note is the SDC's own area-level model
  (field vocabulary); the golden numbers 100, 802 and 920 occur as SNAP counts and one revision by coincidence
  (counts of towns' recipients, a revision of -100), never as the figures; the stump-paragraph words in the releases,
  the Bureau's notes, the methods note and the rule (release, survey, estimate, population, published, averages, the
  region names) are the field's ordinary vocabulary, and no document names the move, SNAP, an indicator or a
  benchmark (checks.py R3c); the 2024 workbook and the transition report carry the SDC's 2023 and 2024 region
  estimates, the estimand's own inputs under rule 2.1, not a ranking on the decision. The audit trail's income value
  "None" read as a Python null and is now "No income".
- **The single-use test.** The DSS SNAP file's only use in the pack is the decisive step's indicator, and no
  document points at it (the methods note, the rule and the Bureau's notes never mention SNAP); a second
  administrative series would give it company but open a fork on which indicator times the years, so the file stays
  alone and the two stage 4 readers measure whether its presence hands over the step.
- **Readers' brief.** The two readers solve the task and hand back their figures for score_reader.py, so they are not
  shown leak.py's REVIEW lines (which quote golden figures and the stump's vocabulary); the main thread ruled those
  lines above.
- **Duplicate.** guard.py heart WARN only (strategy_risk, repeat.gate_g, overuse.gate_g; nearest driver task459 at
  0.06). guard.py surface: nine pairs promoted by the corpus percentile alone, every one at a surface similarity of
  0.100 to 0.101, with no hard tell (no byte-identical file, shared column set, shared invented name or masked prompt
  wording); nothing to rename. Its persona sweep reads "Corbin Community" from the agency's name, not a person.
- **Containers and rebuild.** The pack and the goldens carry no writer signature (H1 audit clean); every PDF opens in
  a strict reader (H25); two consecutive builds are byte-identical and target.zip is cut from the final build.

## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task474.json` (architecture v1), registered 2026-10-20 after a pull and
  brought to the stage-2 driver the same day. Guard check WARN only: `three_rules.strategy_risk` (grain_or_unit;
  answered by the analyst test below, every field read right still files the wrong split), `repeat.gate_g` and
  `overuse.gate_g` (method_or_model_selection, as task271 v2's callback model and task468 v4's linkage-corrected
  mortality: the label is shared, the mechanism is not). The first check BLOCKed on `test.same_driver_older` (gap
  time, G13, method_or_model_selection); the decisive generator is G2, the honest label (the town survey's grain is
  a five-year period, the estimand's a single year). Nearest driver task459 at 0.06.
- **Seed:** ET31 (Connecticut's nine planning regions replaced its eight counties as county-equivalents; a state agency
  splits a fixed $12,000,000 anti-poverty program across the regions on a five-vintage average of the population below
  poverty; older vintages exist only for the counties; the analyst used an area crosswalk). Kept: the world (a New
  England state whose county-equivalents changed mid-series, towns nesting in both geographies), the decision (a fixed
  grant split across the nine regions) and the quantity (each region's average residents in poverty over five years).
  Dropped as the decisive step: the seed's move (rebuild from towns instead of an area crosswalk), which a careful
  analyst takes unprompted; it survives as Layer 1.
- **Pairing:** Survey Research & Official Statistics / seasonal-adjustment-official-time-series-production (official
  time-series production: an annual series rebuilt across a geography break, its missing years produced by temporal
  disaggregation with a benchmarked indicator) / Data Extraction & Conformation (ETL). The State Data Center's annual
  model-based poverty estimates (former counties for 2020 to 2022, planning regions from 2023), the Bureau's
  2020-2024 five-year town table, the Department of Social Services' monthly SNAP counts by town and the
  town-county-region codes are conformed into one region-by-year series, 2020 to 2024, on the new geography; the Fund
  is split on it.
- **Shape:** 05, an allocation to a fixed total: the nine councils' FY2027 amounts from $12,000,000, with the conformed
  series (27 region-years and nine averages) as the construction layer and 27 transition figures as the asks.
- **Strategy:** grain_or_unit (the survey release's five-year grain against the estimand's single year; SNAP's unit,
  recipients, whose ratio to the poor differs by town), Layer 2 field_method, pattern none with G2 decisive, G13 (the
  release's period against the year) and G14 (the indicator's own ratio). Gate G method_or_model_selection: which
  estimator of a town's residents in poverty in a year the data leave standing.
- **World:** the United States, an unnamed New England state with no county government since the 1960s. The state's
  eight former counties were statistical areas only; a 2022 statute made its nine regional councils of governments the
  county-equivalents, and the State Data Center (SDC) moved its annual poverty estimates to the planning regions with
  the 2023 estimates. The Regional Opportunity Fund ($12,000,000 for FY2027, July 2026 to June 2027) is split among the
  nine councils in proportion to each region's average residents in poverty over the five latest estimate years, 2020
  to 2024 (the Fund's allocation rule, issued by the Office of Budget and Policy, OBP). The eight former county
  community action agencies ran the Fund to FY2026 and hand their unspent balances and caseloads to the councils
  (the rule's transition clause). Personas from `guard.py names --geo "United States" --seed 474`: Wendy Taylor
  (Director, SDC), Martin Estrada (SDC demographer) and Paige Hodges (OBP grants manager).
- **Forcing fact:** the OBP signs the FY2027 allocation; the SDC's table goes to the OBP in October 2026. The call faces
  forward (the FY2027 grant); its quantity is the closed 2020 to 2024 years the rule names (a retrospective quantity
  with its reason: the rule allocates on the latest five estimate years).
- **Forum and forcing event:** minister_or_cabinet (the OBP Secretary signs), budget_or_appropriation (the FY2027
  round). Organisation research_or_statistics_office (the SDC prepares the table); role statistical_office_head.
- **Data-native sentence:** the towns' only poverty counts are one five-year survey release, the average of 60 months
  in which the poor of two old cities moved out to suburbs across the new region lines inside their former counties
  (Bellmont Courts' residents from Ormsby to four Mill River Valley towns, April to December 2021; Marlridge Commons'
  from Wexport, June 2021 to February 2022), so its town shares hold those moves for most of its five years and split
  2020 and 2021 by a distribution that did not yet exist, while no published estimate shows the moves at all (each
  stayed inside a former county, and the planning region estimates begin in 2023); the towns' monthly SNAP recipients
  date the moves but count the poor at a take-up that differs by town, so each town's year is its recipients that year
  scaled to its own five-year level.
- **The WHAT screen.** Population: the residents in poverty of the region's towns (the SDC's estimates as last
  published; for 2020 to 2022, each former county's estimate divided among its towns in proportion to each town's
  residents in poverty in that year). Outcome: residents in poverty, a count. Window: each calendar year 2020 to 2024,
  averaged with equal weight. Unit: persons, then dollars; the town is the unit of the 2020-2022 division. Comparison:
  each region's share of the nine averages' sum. The decisive step settles none of them: it is how a town's residents
  in poverty in a year are estimated from a five-year release and a monthly count (HOW, forced by the data: the
  release is a 60-month period average, the counts date the moves, the town ratios differ, and the former counties'
  estimates against their recipients move by one statewide ratio, so the ratio, not the difference, is the town's
  constant).
- **Deliverables:** `rof_fy2027_region_poverty.csv` (the conformed series: each region's 2020 to 2024 figures and its
  2020-2024 average) and `rof_fy2027_allocation_memo.docx` (the nine amounts with a bar chart, and the transition
  figures).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, survey research: series breaks, revisions and benchmarking
    are the official-statistics patterns; this build's own pattern is a period-average survey release disaggregated to
    single years by an administrative indicator benchmarked town by town.
  - `stumping/references/client/two-layer-task-design.md`: field_method (the field's own way of producing a year the
    survey does not publish: an indicator carries the timing, the survey carries the level).
  - The lane's spent drivers (`guard.py mechanisms --objective etl`): task123 v2 splits interval totals onto calendar
    periods by a measured daily shape (a shape inside one interval, no level to meet); task470 completes a sensor
    record with the units it never sees (an auxiliary for a missing count); task461 carries a short record through a
    long correlated one. None benchmarks an indicator whose ratio to the target differs by unit to each unit's own
    period-average level.

## Default path

1. Took each year's SDC estimate as last published: the former counties for 2020, 2021 and 2022 (the 2022 revision
   from the December 2024 transition report), the planning regions for 2023 (revised, December 2025 workbook) and 2024
   (first estimate, same workbook).
2. Keyed the towns through `town_county_region_codes.csv` to the Bureau's 2020-2024 B17001 table (GEO_IDs under the
   region codes) and took each town's below-poverty total.
3. Divided each former county's 2020, 2021 and 2022 estimate among its towns by their shares of the county's
   below-poverty total in the release (the allocation rule's 2.2) and summed the towns' parts into regions.
4. Averaged each region's five years with equal weight and split $12,000,000 in proportion, unrounded, each amount
   rounded to the nearest $10,000.

Ends on: Greater Ormsby $1,620,000, Mill River Valley $2,280,000, Tarrow Uplands $330,000, Southern Shore $740,000,
Wexport Harbor $2,120,000, Two Rivers $1,870,000, Northern Hills $330,000, Quinnet Valley $1,370,000, Eastern Bays
$1,340,000 (six of the nine amounts off).

Golden: Greater Ormsby $1,650,000, Mill River Valley $2,250,000, Tarrow Uplands $330,000, Southern Shore $720,000,
Wexport Harbor $2,140,000, Two Rivers $1,860,000, Northern Hills $330,000, Quinnet Valley $1,380,000, Eastern Bays
$1,340,000.

## Stump sentence

The default path splits each former county's 2020, 2021 and 2022 estimate by its towns' shares in the 2020-2024
five-year release, which holds the 2021 Bellmont Courts and Marlridge Commons relocations for most of its five years,
so it puts about 3,200 of Ormsby's residents in poverty in Mill River Valley in 2020, before they moved (and about
1,300 too few there in 2022, after the move had finished), and files Greater Ormsby $1,620,000 and Mill River Valley
$2,280,000 against the golden's $1,650,000 and $2,250,000, six of the nine amounts off.

## Three rules

Task type: seasonal-adjustment-official-time-series-production (official time-series production: an annual series
rebuilt across a county-equivalent break, the years the new geography lacks produced by temporal disaggregation with a
benchmarked indicator), a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each planning region's residents in poverty in 2020, 2021 and 2022, years the
SDC estimated only for the former counties, produced the way official statisticians produce a single year a survey
publishes only as a multi-year period: an administrative indicator carries the year's timing and is benchmarked to the
survey's level unit by unit (pro-rata benchmarking of monthly SNAP recipients to each town's five-year below-poverty
count), which then divides the model estimate the year does have.

Swap: "how should a fixed fund be split among nine new sales territories, given that 2020 to 2022 sales exist only for
the old districts" keeps the division but loses what decides it: there is no survey period average that leads the
year, no administrative count whose take-up differs by town and must be benchmarked to the survey's level, and no
model estimate the towns' figures must sum to; nothing then says why a five-year share is wrong for 2020 or why the
indicator alone is wrong.

Layer 1: the county-equivalent change (the former counties' estimates in four December PDF releases, the regions' in a
workbook, the SDC's own systems); a first and a revised estimate for every year in consecutive releases (the SDC's
revision cycle); the Bureau's town GEO_IDs re-keyed under the region codes, the codes file carrying both (the Bureau's
2022 change); DSS town names in its eligibility system's own spellings (upper case, abbreviations, a hyphen) with an
UNKNOWN row and a STATE TOTAL row each month; margins of error beside every count and 26 age-sex cells beside the
total (the survey's table layout); the Fund's July-June fiscal years against the estimates' calendar years and SNAP's
benefit months; the closeout workbook's awards in thousands against expenditures in dollars. Each asserted neutral on
the call and on every graded main figure (checks.py L1 rows).

Layer 2: field_method, temporal disaggregation with a benchmarked indicator: the survey's five-year release is the
average of a distribution that moved during it, so a year inside it is estimated by an annual indicator benchmarked to
each town's own five-year level, never by the release's shares (which carry later moves back) or the indicator's
shares (which carry its own ratio).

Decisive step: estimating each town's residents in poverty in 2020, 2021 and 2022 as its SNAP recipients that calendar
year times its 2020-2024 below-poverty count over its mean recipients for the same five years, then dividing each
former county's estimate among its towns by those figures, which files Greater Ormsby $1,650,000 and Mill River Valley
$2,250,000 and moves six of the nine amounts.

Not semantics: every field, code, unit and definition read correctly (the release's below-poverty total and its 60
months, the SDC's calendar years and revisions, the region codes, DSS's town names, recipients as persons) still
leaves the easy route on the release's town shares for every year, because no field and no published estimate shows
that the shares moved; the relocations show only as dated falls and rises in a monthly count, and the step is the
choice of estimator.

Not rule application: the allocation rule files the quantity (2.2: each former county's estimate divided among its
towns in proportion to each town's residents in poverty in that year) and says nothing about how a town's year is
estimated; no document names SNAP, an indicator, a benchmark or a ratio, and executing every filed rule with the
release's shares files the default path.

Analyst test: a strong analyst who reads every file and rule correctly divides each former county's 2020-2022
estimates by its towns' shares in the 2020-2024 release and files Greater Ormsby $1,620,000 and Mill River Valley
$2,280,000 (the default path's Ends on, six of nine amounts off); dividing by the year's SNAP recipients instead files
Greater Ormsby $1,750,000 and Southern Shore $660,000 (all nine off); reading the release as 2022 and moving it by
SNAP files Greater Ormsby $1,680,000 and Mill River Valley $2,210,000; only each town's recipients that year scaled to
its own five-year level files the golden.

Estimand: `obp_rof_fy2027_allocation_rule.pdf` 1.1 (the $12,000,000 split in proportion to each region's average
residents in poverty over 2020 to 2024), 2.1 (a region's figure for a year is the SDC's estimate as last published),
2.2 (for 2020, 2021 and 2022, each former county's estimate divided among its towns in proportion to each town's
residents in poverty in that year, each region taking its towns' parts), 2.3 (the five years with equal weight) and
2.4 (amounts from the unrounded averages); the year is the calendar year (`sdc_poverty_estimates_methods_note.pdf`).

No decoy: nothing is planted to be caught: the releases, the survey table, the SNAP counts, the codes and the Fund's
records are what each system writes; no memo, draft, briefing or stakeholder figure argues a split; the Bureau's
county-to-region allocation factors are its own product for population data, declared as the wrong-basis distractor
and ruled out by their basis (2020 census population) against rule 1.1's residents in poverty.

No certified replay: no region figure for 2020 to 2022, no earlier allocation on the new regions and no certified
split ships; the 2023 and 2024 region estimates are the estimand's own years and differ from every route's town sums
by the survey's sampling error (up to 6.9 per cent under the golden's own construction), so they rank nothing without
a construction nobody asks for.

Lesson: a multi-year survey release is a period average of a distribution that moves, so a single year inside it is
placed by an annual indicator benchmarked to each unit's own period level, never by the period's shares (which carry
later moves back) nor by the indicator's shares (which carry its own ratio to the target); no build on file
disaggregates a period-average release by a benchmarked indicator whose ratio differs by unit.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the release's town shares for every year (GO $1,620,000, MRV $2,280,000; six off) | rule 2.2 asks for each town's residents in poverty and the release is the only town poverty count: fires | B17001's below-poverty total by town, keyed through the codes file: fires | apportioning by a survey's small-area shares is the reflex: fires | none | none | one share per town: fires | readable |
| R1, the year's SNAP recipients as the shares (GO $1,750,000, SS $660,000; nine off) | none | DSS's recipients by town and month: fires | a count dated to the year is the reflex for a year-specific split: fires | none | none | one share per town-year: fires | readable |
| R1b, the year's SNAP households (nine off) | none | the households column: fires | as R1: fires | none | none | one share: fires | readable |
| R2, half the release's share and half the year's SNAP share (six off) | none | both files: fires | splitting the difference: fires | none | none | an average of two shares: fires | readable |
| R3, the Bureau's county-to-region allocation factors, population (nine off; declared wrong-basis distractor) | none | a factor per county-region piece in the factor file's header: fires | the published crosswalk factor is the reflex: fires | none | none | one product per piece: fires | readable |
| R4, the regions' 2023 shares carried back to the State's 2020-2022 total (six off) | none | the 2023 region estimates beside the county years: fires | carrying the first new-geography year back: fires | none | none | one share per region: fires | readable |
| R5 and R6, the survey's universe or the 2020 census population as the shares (nine off) | none | the universe column, the factor file's population: fires | population shares: fires | none | none | one share: fires | readable |
| R7, the release read as 2022 and moved by SNAP (GO $1,680,000, MRV $2,210,000; four off) | none | both files: fires | labelling a five-year release by its middle year is a common habit: fires | none | none | one ratio per town-year: fires | readable |
| R8, the release moved by SNAP's difference from its five-year mean (GO $1,640,000, SS $730,000; four off) | none | both files: fires | none | none | none | one difference per town-year: fires | readable |
| G (decisive), each town's recipients that year scaled to its own five-year level, the county divided by those figures (golden) | rule 2.2 files each town's residents in poverty in that year and the default answer to it is the release; no clause names SNAP, an indicator, a benchmark or a ratio, and the SDC's methods note never mentions SNAP: silent | no column holds a town's figure for a year; it is built from a monthly file keyed by DSS's names, a five-year table keyed by GEO_ID and the codes file; nothing marks a town whose poor moved, and no published estimate shows the 2021 moves: silent | the reflexes are the release's shares and the year's SNAP shares; scaling a monthly count to a survey level town by town is no apportionment reflex: silent | no published figure scores a split; the 2023-2024 region estimates sit up to 7 per cent from every route's town sums through survey error and rank nothing without a construction nobody asks for: silent | every file reconciles, the counties sum to the State, nothing is anomalous: silent | a three-file join, a ratio per town over 60 months and a division within eight counties: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a region's residents in poverty in a year | the SDC's estimate as last published (2020-2023 revised, 2024 first) | each year's first estimate | one amount, two averages and 11 cells move | rule 2.1 "as last published" |
| SF2 | the 2020-2022 figure | each former county's estimate divided among its towns, each region taking its towns' parts | a region figure built from the town data alone, not summing to the counties | other figures | rule 2.2 "each former county's estimate is divided among the former county's towns" |
| SF3 | that year | the calendar year | the federal fiscal year, the State's fiscal year, a July or December month of SNAP | up to four amounts move | the SDC's methods note (an estimate for a year counts the residents in poverty in that calendar year); the Bureau's notes (data collected January 1, 2020 to December 31, 2024) |
| SF4 | the town's five-year level | the release's below-poverty total, a 60-month period average | the total read as 2022 (R7) | four amounts move | the Bureau's notes: the 5-year estimates describe the average characteristics of the population over the 60 months |
| SF5 | the indicator | SNAP recipients (persons) | SNAP households | same call, and every graded figure in its bin (asserted) | C1 convergence |
| SF6 | whose ratio a town's year uses | the town's own (its release over its own mean recipients) | the county-region piece's pooled ratio; the county's (which is R1) | piece: the same nine amounts, averages by up to 24 and cells by up to 114; county: all nine amounts | rule 2.2 divides the estimate "among the former county's towns in proportion to each town's residents in poverty"; each town's release is its own benchmark, and the ratios differ inside every piece (0.87 to 1.26 among Halden's Greater Ormsby towns), asserted |
| SF7 | how the indicator moves the level | in proportion (the town's ratio held) | additively (R8) | four amounts move | the data: the former counties' estimates against their recipients, 2019 to 2022, move by one statewide ratio (two-way residual 0.58 per cent, inside the SDC's model error) while the differences do not (up to 31.0 per cent at Pennock), asserted |
| SF8 | the average | the five years' mean with equal weight | weighted by year or by population | none ships | rule 2.3 "each year with equal weight" |
| SF9 | a region's towns | the codes file's towns under the 2022 statute's region | towns by the Bureau's GEO_ID prefix | same towns (asserted, 118 of 118) | `town_county_region_codes.csv` |
| SF10 | rounding path | amounts from the unrounded averages, each rounded to $10,000 at the end | amounts from the averages rounded to hundreds | same call (asserted) | rule 2.4 "computed from the unrounded averages" |
| SF11 | the FY2027 amount | the share of $12,000,000 | the share plus the transition carry-in | none ships: the carry-in is a separate payment | rule 3.1 "in addition to their FY2027 allocations" |
| SF12 | the councils | one per planning region, nine | the eight former county agencies | none ships | rule 1.1 |
| SF13 | the 2022 figure | the former counties' revised 2022 estimates (December 2024 transition report) | the first (December 2023) | covered by SF1, asserted with it | rule 2.1 |

## Ladder

- **R0, the default path: the release's town shares for every year (six amounts off).** Greater Ormsby $1,620,000,
  Mill River Valley $2,280,000, Southern Shore $740,000, Wexport Harbor $2,120,000, Two Rivers $1,870,000, Quinnet Valley
  $1,370,000. It puts 3,245 of Greater Ormsby's residents in poverty in Mill River Valley in 2020 and 1,401 in 2021,
  before they moved, and about 1,300 too few there in 2022, after the move had finished; Wexport Harbor's side loses
  1,301 to Southern Shore in 2020. Dies to the SNAP counts: Ormsby's recipients fall from 26,954 in March 2021 to 22,496
  in January 2022 while Fenbrook, Tilcombe, Carrholt and Draywick rise from 6,304 to 9,667 (Fenbrook 642 to 1,783), and
  Marlridge rises from 2,765 to 3,920 as Wexport falls; none of it shows before April 2021, so the release's shares are
  not 2020's.
- **R1, the obvious correction: the year's SNAP recipients as the shares (all nine off).** Greater Ormsby $1,750,000,
  Southern Shore $660,000. Dies to the towns' ratios: release over mean recipients runs 0.87 to 3.13 across the towns
  (1.01 to 1.08 in the six cities), so SNAP shares overweight the cities and starve the hill towns; R1b (households)
  dies to the same fact (all nine off).
- **R2, splitting the difference (six off).** Inherits both errors in halves.
- **R3, the Bureau's allocation factors (nine off), the declared wrong-basis distractor.** Population, not poverty:
  Southern Shore $1,060,000. Dies to rule 1.1's basis.
- **R4, the regions' 2023 shares carried back (six off).** Dies to the counties: it ignores which former county each
  year's poor were in (the counties' estimates move differently, Ashgrove up 7.5 per cent from 2019 to 2022, Ludbury
  down 1.0).
- **R7, the sophisticated near miss: the release read as 2022 and moved by SNAP (four off).** Uses the indicator but
  anchors the level at the middle year, so the moves that the five-year average holds for most of its span are read as
  2022's level: Greater Ormsby $1,680,000, Mill River Valley $2,210,000, Southern Shore $710,000, Wexport Harbor
  $2,150,000. Dies to the Bureau's notes: the release is the 60 months' average, not a point.
- **R8, the additive benchmark (four off).** Moves each town's level by its recipients' difference from their mean:
  Greater Ormsby $1,640,000, Southern Shore $730,000, Wexport Harbor $2,130,000, Two Rivers $1,870,000. Dies to the
  county panel: the counties' estimates against their recipients move by one statewide ratio in 2019 to 2022 (two-way
  residual 0.58 per cent) and not by one difference (up to 31.0 per cent at Pennock, 13.4 at Ludbury).
- **G, the decisive move (golden).** Each town's recipients that calendar year times its release over its mean
  recipients 2020 to 2024 (each town's five-year average of the estimates equals its release exactly), each former
  county's estimate divided by those figures, the towns summed into regions, 2023 and 2024 from the region estimates.
- **Family and margins:** SNAP households for recipients moves no graded figure (amounts within $104, averages within
  2.1, cells within 6.0); every graded main figure clears its rounding edge by more than the family's spread (amounts
  by $1,283 or more, averages by 9.5, cells by 5.0), the tightest amount $1,335 from its edge; the piece-pooled ratio
  gives the same nine amounts and is ruled out for the averages and cells (SF6); fiscal-year and single-month
  indicators are ruled out (SF3).
- **Position, separation and dominance:** every rung names its own allocation; R0 and R7 move Greater Ormsby in
  opposite directions; no rung outside the golden family lands the nine amounts; only the benchmarked indicator moves
  Greater Ormsby up and Mill River Valley and Southern Shore down from R0 together.
- **Worth on the graded quantities (main block, 45 figures: nine amounts, nine averages, 27 cells):** R0 keeps 14, R1
  0, R1b 0, R2 7, R3 0, R4 3, R5 0, R6 0, R7 23, R8 22; none lands the call (generator/ceiling.py).
- **Grid:** the Layer 1 items mishandled one at a time and SNAP households for recipients leave the call and every
  main figure in place (checks.py); every rung lands on its named wrong allocation.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the residents in poverty of each region's towns (rules 2.1 and 2.2); the 118 towns of the codes file; the nine regions |
| 2 | Unit of account | the region (its council); persons, then dollars; the town is the unit of the 2020-2022 division (rule 2.2, SF6) |
| 3 | Attribution window | calendar years 2020 to 2024 (rule 1.1, the SDC's methods note); SNAP's benefit months January to December of each year (SF3) |
| 4 | As-of dating | the SDC's estimates as last published at October 2026 (the December 2025 workbook the latest); the Bureau's 2020-2024 release; DSS through June 2026 |
| 5 | Version basis | as last published (rule 2.1): 2020 to 2022 and 2023 revised, 2024 first (SF1, SF13) |
| 6 | Denominator | each town's own mean recipients over the release's five years (SF6, the decisive step, HOW); the nine averages' sum for the shares (rule 1.1) |
| 7 | Weighting | the five years equal (rule 2.3); the twelve months of a year equal; SNAP households for recipients converge (SF5) |
| 8 | Window length | five years for the average (rule 1.1); the release's 60 months for each town's benchmark |
| 9 | Boundary inclusivity | 2020 to 2024 inclusive; FY2026 is July 1, 2025 to June 30, 2026 inclusive (asks) |
| 10 | Rounding path | amounts from the unrounded averages (rule 2.4, SF10), rounded to $10,000; residents to the nearest hundred; carry-ins and energy assistance to $100; people exact |
| 11 | Tie-break | none: each region's amount is its own |
| 12 | Maturity and censoring | every year 2020 to 2024 is estimated and published; 2024 has only its first estimate, which rule 2.1 takes |
| 13 | Order of operations | town-years, county division, region sums, the five-year average, the allocation, rounding last |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | no repeated town-month or code on the main path; the twice-received upload sits in the asks' records only |
| 16 | Identity normalisation | DSS's town names matched to the codes file (upper case, abbreviations, Layer 1, asserted 118 of 118); GEO_IDs under the region codes |
| 17 | Netting | none on the main path; unspent is award less spent (asks) |
| 18 | Dimensional units | persons on the main path; dollars for the amounts; the closeout's awards in thousands (asks) |
| 19 | Code and status semantics | B17001_002 is the below-poverty total; region codes 110 to 190, county codes 001 to 015; never the stump |
| 20 | Integerisation | amounts each rounded to $10,000 (the nine rounded amounts' sum stated in the memo); residents to the nearest hundred |
| 21 | Clause scope | rule 2.2 for 2020 to 2022 only; 2023 and 2024 from the region estimates (rule 2.1); rule 3 for the transition figures only |
| 22 | Forward window contents | FY2027's allocation on the closed 2020 to 2024 estimate years (a retrospective quantity with its reason, Draw) |

## Literal reader

Executed word for word, the allocation rule fixes the population (the residents in poverty of each region's towns),
the source (the SDC's estimates as last published), the division of 2020 to 2022 (each former county's estimate among
its towns in proportion to each town's residents in poverty in that year), the calendar years, the equal weights, the
rounding path and the total, and leaves one thing open: how a town's residents in poverty in a year are estimated. The
candidates are the release's shares (R0), the year's SNAP shares (R1, R1b), their average (R2), population or universe
shares (R3, R5, R6), the 2023 shares carried back (R4), the release read as 2022 and moved by SNAP (R7), the release
moved additively by SNAP (R8) and the release benchmarked to SNAP town by town (G). The data separate them: SNAP dates
relocations from April 2021 that a five-year average holds for most of its span; the towns' ratios of release to mean
recipients run 0.87 to 3.13; the Bureau's notes make the release a 60-month average; the counties' estimates against
their recipients move by one ratio, not one difference (checks.py). The family left standing (recipients or
households, each town's own ratio) gives the same nine amounts and every graded figure in its bin. Every write-up step
names the file and rule it executes.

## Oracles

None that ties only under the golden. The 2023 and 2024 region estimates are the estimand's own years; every route's
town sums miss them by up to 7 per cent through the survey's sampling error, so no route is confirmed and none is
refuted without a back-test nobody asks for. The State's total ties under every route (each former county's estimate is
divided, never changed). The Bureau's county-to-region allocation factors give a split on another basis (2020 census
population) and land on nine wrong amounts, neither the golden nor rung 0 (the declared wrong-basis distractor). The
OBP's FY2026 allocation table divides an earlier fund among the eight county agencies and ranks no council (the second
declared distractor).

## Ask sheet

- **The construction layer:** the nine averages and the 27 region-years in `rof_fy2027_region_poverty.csv` and the
  nine amounts with their chart; the cracker has them all, and every one is the decisive construction's output.
- **Ask A, each council's share of the former county agencies' unspent FY2026 balances (nearest $100), nine
  figures.** H18 home: the transition clause (rule 3.1) passes each agency's balance unexpended at June 30, 2026 to the
  councils in proportion to the distinct people the agency served in FY2026 while they lived in each council's
  region; it is the trail from the agencies' FY2026 closeout through client records the allocation never reads. Use:
  the carry-in is paid with the FY2027 award and the OBP books it beside it. Path: the closeout workbook (award in
  thousands, expended, unexpended), the client services extract (agency code, client number, service date, entry
  date, town), the grants data system's profile audit trail (client number, field, old and new value, effective
  date), Corbin Community Action's client number conversion (old and new numbers) and the codes file (town to region),
  with the rule (3.1): six files, eighteen columns.
  Primary devices: D2 (a later snapshot: each service row carries the town its client record held when the extract
  was cut on September 30, 2026, or when a Corbin record closed on December 31, 2025, so the 2,372 households that
  moved during FY2026, 1,432 of them across council lines, carry a later town on earlier services; the town each lived
  in when served is recovered from the profile audit trail, where 5,538 town edits sit among phone, email, language,
  household-size and income edits, 36,528 rows in all) and D7 (Corbin's conversion to new client numbers on January 1,
  2026: a client served on both sides carries two numbers, matched in the 5,393-row conversion file). No sweep sees
  either: every row is complete, every town resolves, nothing repeats, and the extract's counts tie to nothing.
  Hazards: Wexmoor's April 2026 upload received twice (1,176 exact duplicate rows; inert on distinct counts), 14,983
  rows entered in the extract's window whose service date falls outside FY2026, awards in thousands (loud).
  Stops (asserted, checks.py and generator/ceiling.py): the extract's town with numbers as given misses all nine
  (Greater Ormsby $66,500 against $68,600, Mill River Valley $100,300 against $98,700, Southern Shore $41,400 against
  $39,600); the audit trail applied without the conversion misses Mill River Valley and Southern Shore; the conversion
  without the audit trail misses all nine; both give all nine.
  Realism: case management exports join the current client record to service history; agencies key an address
  change with the date the client moved; a conversion renumbers clients on a cut-over date and closes the old records.
- **Ask B, the number of people each share is counted on (exact), nine figures.** The counts behind ask A, summed over
  the agencies: a person served while living in two regions counts in each (rule 3.1). Same path and devices. Stops:
  the careful path misses all nine (Greater Ormsby 3,841 against 4,080, Mill River Valley 6,909 against 5,677); the
  audit trail alone misses Mill River Valley (6,985) and Southern Shore (2,354); the conversion alone misses all nine.
- **Ask C, the energy assistance the agencies paid to households in each council's towns in FY2026 (nearest $100),
  nine figures.** H18 home: rule 3.2 hands each council the energy assistance caseload, and the FY2026 payments in its
  towns are the base of its FY2027 energy plan. Path: the extract's energy assistance rows (household, amount, service
  date, town), the audit trail, the codes file and the rule. Primary device: D6 (a household's one payment exported
  on the row of every member listed in the household), with D2 shared. Stops: the rows' amounts by the extract's town
  miss all nine (Greater Ormsby $1,114,800 against $505,600); one payment per household by the extract's town misses
  all nine (Greater Ormsby $485,600, Southern Shore $296,400 against $262,600); the rows' amounts by the town when paid
  miss all nine; one payment per household by the town when paid gives all nine.
- **Main population zero-counts (asserted):** no device or hazard row is read by the allocation: the main path reads
  the SDC releases, the survey table, the SNAP counts and the codes file only, and none of the Fund's records.
- **Hazard table (asserted):** the extract kept whole, its 14,983 rows dated outside FY2026 included, moves the 18
  figures of asks A and B (ask C's payments all fall inside the year); the duplicate upload moves none; neither touches
  a main figure.
- **Referee:** none; the closeout's unexpended balances tie under every handling (they are the agencies' own totals).
- **Shared-device note:** D2 sits under all three asks, so a reader who finds the address history keeps 14 of the 18
  figures in asks A and B and, with one payment per household, all nine of ask C; the audit trail's mixed edits are
  the silence it rests on, measured by the stage 4 reader.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each council's share of the unspent balances | dedups the twice-received upload, keeps service dates in FY2026, reads the extract's town for each service, counts distinct client numbers per agency and council, shares each agency's unexpended balance by those counts | miss |
| B, the people each share is counted on | the same distinct client numbers per agency and council, summed per council | miss |
| C, energy assistance paid to households in each council's towns | sums the energy assistance amounts on the extract's FY2026 rows by the extract's town | miss |

- Mirror leakage: 0.0 per cent of ask weight (every rung takes the cracker's ask path and misses all 27:
  generator/ceiling.py).
- Pair ceiling: 35.5 (weights 38 / 7 / 55: the call and the 45 main figures under 38; the cracker keeps the main block
  and instructions, 45.0; the best mirror, R7, keeps 23 of the 45 main figures, 26.0; average 35.5), rerun from the
  generated rubric at ship.
- Measured by: generator/ceiling.py on the generator's copies (design stage), then on the cut pack.

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
- 2026-10-20, at stage 2: two non-overlapping five-year releases (2015-2019, 2020-2024) placed at their middle years
  and a year's town shares interpolated between them: its forcing evidence (the native years 2023 and 2024 on the line
  through the middle years) sat inside the regions' survey noise of 5 to 12 per cent, and the drift between the two
  releases' middle years, five years apart, was smaller than that noise; replaced by an annual indicator benchmarked to the one release.
- 2026-10-20, at stage 2: a growth component (each town's drift estimated from the two releases and carried by year):
  the difference of two town releases carries both sampling errors and swamped the drift; dropped.
- 2026-10-20, at stage 2: shipping the 2015-2019 release beside the 2020-2024 one under the benchmarked indicator: with
  two benchmarks a proportional Denton spreads the ratio across the years and moves amounts by up to $12,000 against
  the pro-rata golden, an open method; only the 2020-2024 release ships, where Denton and pro-rata coincide.
- 2026-10-20, at stage 2: SNAP benefits in dollars in the DSS file: a dollar indicator for a person count carries the
  emergency allotments of April 2020 to February 2023 and moves two amounts; the file ships recipients and households.
- 2026-10-20, at stage 2: the client address changes as their own file: a file named for address changes announces
  that the extract's town is not the town when served, and with it a reader keeps 14 of the 18 figures in asks A and B;
  the moves ship as address edits inside the grants data system's profile audit trail.
- 2026-10-20, at stage 3: the two relocations dated July 2023 to June 2024: the State Data Center's own planning region
  series then showed the drift outright (Greater Ormsby down 10.6 per cent from 2023 to 2024, Mill River Valley up
  8.1), so the record displayed the step; both relocations now run from April 2021 to February 2022, inside a former
  county each, where no published estimate shows them (the planning region estimates begin in 2023, and every region
  moves under 1.3 per cent from 2023 to 2024).
- 2026-10-20, at stage 4 (architecture 1 spent): two isolated scored readers. Reader 1 benchmarked each town's SNAP
  recipients to its own five-year survey count unprompted ("SNAP levels are not proportional to poverty across towns,
  but SNAP's year-to-year movement is usable") and landed all nine amounts (score_reader.py exit 1); reader 2 took SNAP
  shares (missed the call) but, like reader 1, rebuilt the town at service date from the audit trail, mapped Corbin's
  numbers and counted one energy payment per household, keeping 27 of 27 ask figures. Rule 2.2's "in that year" beside
  a single five-year release and a monthly town series displays the decisive step, and the ask devices are work orders
  a careful reader executes; the architecture is spent and the draw is re-rooted at stage 1.
- 2026-10-20, stage 4 judge on architecture 1: DETERMINISTIC, APPROVE, Gate H analytical; it named two pins worth
  carrying into the re-root (an effective date is the first day the new value applies; a household payment repeats on
  each member's row), and that the release-shares route is defensible enough that a miss there can read interpretive.

