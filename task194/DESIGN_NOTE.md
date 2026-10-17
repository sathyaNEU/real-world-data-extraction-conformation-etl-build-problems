# task194 design note

Placing a scarce improvement team when the unit standing worst is partly standing worst by chance.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task194.json`, filed and committed with this note |
| Domain, task type | healthcare-delivery-health-economics, `provider-quality-risk-adjustment` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 11 (before and after with a control): each eligible unit's attributable effect, the call, the closest unit, the gap, the chart's parts, the deliverables |
| Decision | pick_one_of_n, named_option (a cost centre) |
| Gate G | `method_or_model_selection`; decisive generator G8 in a graded form (which part of a unit's excess a placement can move: the part that is its own standing, not the part that is this quarter's variation), framed by G16 (the data selects the estimator and the form the record is read in), with G14 (the pooled share against the right pool) and G17 (the unit's own between-quarter variation) supporting |
| Strategy | `causal_design` |
| Layer 2 | `estimand_identification`, own pattern `own:reversion-against-effect-in-a-chosen-worst-unit` |
| World | Australia, Mid-Rivers Health Network (four hospitals, 21 acute inpatient units, 3 non-acute) |
| As-of date | 2027-03-18 (extract pulled 2027-03-05, quality committee 2027-03-24, placement runs 1 April to 30 June 2027) |
| Deliverables | `embed_placement_2027q4.xlsx`, `embed_placement_brief.pdf` (chart embedded, rendered by the generator) |
| Criteria from the shape | 12 per-unit avoided counts + call + closest + gap + 5 chart parts + 2 deliverables + 3 critical components = 25, before the asks' 46 |

**Shape arithmetic.** 12 eligible units x 1 graded figure (the complications the embed would avoid there) = 12;
the call, the closest unit and the gap = 3; the brief's chart (one bar per unit, the recommended unit marked,
the axis in complications, the finding as the title, the units in avoided order) = 5; the two deliverables
present and named = 2; the three critical components = 3. Main side 25. The asks add 12 + 18 + 16 = 46.

**Data-native sentence.** In this panel a unit's quarterly standardised ratio swings by 0.128 about its own
level while the twelve units' own levels are only 0.085 apart, and the quarterly deviations carry no serial
correlation (-0.089 over the candidates' 103 consecutive pairs, -0.091 over the whole panel's 192, which is
what de-meaning a ten-quarter record implies on its own), so the quarter that makes a unit look worst is
mostly the unit's own variation, and the closed placement register is the only thing in the pack that prices
what a placement itself removes.

**Guard.** `guard.py check` and `heart` both WARN, no BLOCK (nearest driver 0.11 task258, nearest stump 0.06
task191). Four axes were redrawn against siblings that re-registered while this build was in design:
`people.first` (Johnathan appears in task457) cleared by redrawing both personas from
`guard.py names --geo Australia --seed 194` (Katherine Klein, Nicholas Fields); `repeat.question_form`
cleared by taking the form from the decision, which is a placement, so the prompt asks `where` the team
should go rather than `which` unit; `ban.forcing_event` (period_close, task191) cleared by the committee
meeting that notes the placement on 24 March; `ban.pattern` and `test.same_driver` (G14 against task233 v2
and task149, then G16 against task148 v2) cleared by naming G8 as the decisive generator, which is what the
decisive rung actually asks: which part of a unit's excess a placement can move. WARNs answered:
`repeat.gate_g` and `overuse.gate_g` are `method_or_model_selection`, which the lane's objective keeps
returning to and which the gap, pattern and driver tests clear; `test.same_puzzle_older` and
`test.same_driver_older` are differentiated in the card against task131 v2, task183, task134, task149,
task258 and task452.

**After the cut.** `guard.py surface` exits 0: three pairs promoted at surface similarity 0.102, the
corpus's top one per cent, none of them a hard tell (the only named tell is `B: same decision type on the
cards` against task50, a pick_one_of_n from another domain and gap); the pack's personas are the two drawn
ones. `guard.py heart` is WARN, nearest driver 0.11 (task258 v1), nearest stump 0.06 (task191).

**Sources read.** `analytical_tasks/02_anomaly_detection/` seed AD17: the decision shape only (one scarce
improvement team, one unit, a quarter, judged on the fall in the outcome users see), per the card's
`slot_note`; the seed's trace-attribution architecture is not used. `guard.py mechanisms --objective
anomaly-detection` read before the draw: task190 spends the undetected-stock insight, task191 the selected
extreme against the record of extremes at the same reach, task192 the process behind a burst, task193 the
comparison population of a measure, task182 a shared driver with unit-specific lags, task183 composition
against rate. None of them prices an intervention's own effect against a chosen unit's reversion, which is
what this build spends. `stumping/references/strategies.md` F9 (`causal_design`, regression to the mean
named, no measured hold, the three deaths 107 v2, 118/124 and 230 read first) and Part 4 G14, G16, G17.

## WHAT screen (`stumping` 1.2)

**Decisive step.** Estimate the counterfactual the charter names (what the unit would have recorded over the
assessment quarter without the team) from the unit's own standing over the specification period rather than
from the quarter it is standing in now, and price the team's effect from the closed placement record as a
share of that persistent excess rather than as the fall that followed a placement.

Which part of the estimand does it settle? **None of the five.**

| Part | Filed by | Sentence |
|---|---|---|
| Population | charter clause 4.2 | every acute inpatient unit with four or more closed quarters of reported indicator data on specification 4.0, except a unit the team has been placed with in the previous twelve closed quarters (12 units; the unit register and the placement register make the set computable, and no unit is near the four-quarter edge except the amalgamated 41510 at five) |
| Outcome | specification 4.0 clauses 2.1 to 2.4 | episodes with one or more hospital-acquired complications, against the published stratum rates by risk band and age band, observed over expected |
| Window | charter clause 4.1 and the prompt | the assessment quarter, being the quarter the team is embedded: 1 April to 30 June 2027 |
| Unit | charter clause 4.3 | complications, counted at the unit that hosts the team, over the assessment quarter |
| Comparison | charter clause 4.3 | the complications the unit would have recorded over the same quarter without the team, against what it records with the team there |

What stays open is how the "without the team" branch is estimated and how the register prices the team.
Both are estimation, and the data separates every candidate: the units' own quarterly deviations carry no
serial correlation, so a quarter's deviation is not the unit's position, and the register's seven closed
placements fit a share of persistent excess (worst miss 21 per cent) against a share of the unit's level
(worst miss 141 per cent) and a reduction per expected complication (worst miss 177 per cent).

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' own grain.

1. Read `episode_outcomes_extract.csv`, apply specification 4.0's denominator and its four exclusions, join
   `drg_risk_bands.csv` and `hac_stratum_rates.csv`, and compute every unit-quarter's observed and expected
   complications; the result ties to `unit_indicator_series.csv` and to the dashboard export for the quarter
   ended 31 December 2026.
2. Apply charter clause 4.2 through `unit_register.csv` and `improvement_placements.csv`: twelve eligible
   units.
3. Take the latest closed quarter (2026-27 Q2) and compute what each eligible unit recorded above its
   expected number: Alderbrook General Medicine 34, Alderbrook Respiratory Medicine 25, Marrowfield
   Orthopaedics 23, Alderbrook Orthopaedics 21.
4. Price the programme off `improvement_placements.csv` and the same extract: across the seven closed
   placements the units' complications fell 38 per cent of the excess they were carrying.
5. Apply that share to each unit's current excess: Alderbrook General Medicine 13 complications avoided,
   Alderbrook Respiratory Medicine 10, Marrowfield Orthopaedics 9, Alderbrook Orthopaedics 8.
6. Place the team with Alderbrook General Medicine, 13 complications avoided over the quarter.

**Ends on:** Alderbrook General Medicine (cost centre 41210), 13 complications avoided.
**Golden:** Alderbrook Orthopaedics (cost centre 41230), 17 complications avoided.

The default path reconciles everywhere a solver checks it: the unit-quarter observed and expected counts tie
to the published indicator series row for row, the quarter's adjusted rates tie to the dashboard export, and
the monthly activity summary ties to the extract's separations.

## Stump sentence

A competent solver computes the complications each eligible unit is recording above its risk-adjusted
expectation in the latest closed quarter, scales them by the 38 per cent of excess the closed placement
register removed, and places the team with Alderbrook General Medicine for 13 complications avoided, which is
the unit with the most room to return to its own level rather than the unit a placement moves most.

## Three rules

- **Task type:** `provider-quality-risk-adjustment`, which the client taxonomy lists under Anomaly Detection
  & Diagnostics: separating a provider's real signal from what measuring it produces is the task type's own
  work, and the pack ships the episode-level raw material the risk model runs on.
- **Domain test:** the deciding quantity is the reduction in a risk-adjusted provider outcome attributable to
  an improvement intervention. Provider profiling estimates it by splitting a unit's observed excess over its
  risk-adjusted expectation into the part that is the unit's own standing and the part that is this quarter's
  variation, and by pricing the intervention on closed placements net of that variation; indirect
  standardisation, the unit's own between-quarter variation and the placement record are the field's own
  instruments and all three ship.
- **Swap:** "Which of our twelve machines should the calibration crew spend the quarter with, and how many
  out-of-tolerance parts would that avoid?" With machines measured without error there is nothing to return
  to: the worst machine now is the worst machine, ranking on the current period is the answer, and the record
  of past crews adds nothing. The task only works where the measured quantity is a rate on a few hundred
  episodes and the unit's own quarters disagree with each other.
- **Layer 1:** episode records at two grains (the episode extract against the monthly activity summary and
  the quarterly indicator series, both rollups of the same records); a national complication list revision on
  1 July 2026 that renames and reissues category codes (the coding service's own change); two medical wards
  amalgamated into cost centre 41510 on 1 October 2025 (a service reconfiguration); a comorbidity score keyed
  on only 85 per cent of episodes (clinical coding does not key it for every episode); a dashboard export
  correct and labelled for the quarter ended 31 December 2026 (the monitoring system's quarterly export);
  tables inside PDFs (the specification's stratum and category appendices); fiscal quarters against the
  calendar year the hospital-level ask uses. Every item is what these systems produce, nothing is placed to
  be caught, and each is asserted neutral in `checks.py` (R2).
- **Layer 2:** `estimand_identification`. The methodological choice that flips the call is which position the
  unit is expected to hold over the assessment quarter without the team, and what the placement register
  prices: the quarter the unit is standing in, or the unit's own standing over the specification period.
- **Decisive step:** take the unit's own standing as the counterfactual and read the register as a share of
  standing excess, because the units' quarterly deviations carry no serial correlation (-0.089) and the
  register's own falls track standing excess (worst miss 21 per cent) rather than the unit's level (worst
  miss 141 per cent) or its expected complications (worst miss 177 per cent).
- **Not semantics:** every field, code, unit and definition read correctly still leaves the easy route on
  Alderbrook General Medicine. The extract's fields are plain, the specification files the denominator, the
  exclusions, the stratum rates, the reporting periods and the forward expectation basis, and the charter
  files the population, the outcome, the window, the unit and the comparison. A solver who reads every one of
  them correctly, and whose observed and expected counts tie to the published series row for row, still ranks
  on the quarter in hand and files 13 complications avoided at 41210.
- **Not rule application:** no filed rule, formula or procedure says what a unit would have recorded without
  the team, or how the placement record prices a placement. The charter names the quantity and stops; the
  specification defines the indicator and its reporting periods and stops. The decisive step is the choice of
  estimator for a counterfactual the records fix but no sentence computes.
- **Analyst test:** a strong analyst who risk-adjusts every unit correctly, applies the charter's eligibility
  and activity clauses and prices the programme off the closed register ranks the units by the complications
  they are recording above expectation in the latest closed quarter and places the team with Alderbrook
  General Medicine (41210) for 13 complications avoided; 41210's ten quarters stand at 1.03 against 1.19 in
  the quarter in hand, so the excess it is carrying now is mostly its own variation and the placement would
  avoid 2.
- **Estimand:** "the complications the unit would have recorded over the assessment quarter and does not
  record because the team is there", charter clause 4.3, with the population in clause 4.2, the assessment
  quarter in clause 4.1, the activity basis in clause 4.4 and the indicator in specification 4.0 clauses 2.1
  to 2.4 and 3.1 to 3.4.
- **No decoy:** nothing in the pack is planted to be caught. No block of readings is copied or backfilled, no
  memo or draft argues a candidate, no stakeholder figure is wrong, and no document ranks the units. The
  dashboard export, the indicator series and the activity summary are each correct for the question they
  answer and reproduce from the extract to the row.
- **No certified replay:** the placement register carries facts only (cycle, unit, decision date, start and
  end dates, team FTE, close-out date) and no achieved-reduction column, so nothing is recovered by
  reproducing a certified figure. The register's seven closed placements price the programme because the
  analyst computes their falls from the same extract everything else comes from.
- **Lesson:** when a scarce intervention is placed on the unit standing worst, the fall that follows is mostly
  the unit's own return to its level, so the decision has to be taken on the persistent part of each unit's
  excess and the intervention priced net of that return. No build on file teaches it: task191 judges one
  selected extreme against the record of extremes at the same reach without any intervention to price,
  task131 v2 prices a treatment whose own rebound returns the load it moved, and task258 decomposes a measure
  into parts an intervention reaches.

## Readability screen

Six tests per rung: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene battery, 6 linear.

| Rung | 1 filed | 2 schema | 3 reflex | 4 bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 default: the quarter's excess, priced off the register | charter names the quantity, not the basis | no column holds either excess | yes, this is the reflex | none scores it | ties everywhere | one subtraction | readable |
| 1 the worst standing: the unit's own ratio over the record | specification files the reporting period, not its use | series carries the quarterly ratio, no cumulative column | yes (the quality-improvement instinct) | none | ties | one ratio | readable |
| 2 the harm the quarter carries: expected complications at planned activity | charter clause 4.4 files the activity basis | planned separations are a column | yes (where the harm is) | none | ties | one product | readable |
| 3 (decisive) the persistent excess the planned quarter carries, priced as a share of persistent excess from the register | no sentence names a counterfactual or a basis for pricing the register | no column holds a unit's persistent position, its excess or any share | no: every reflex (rate now, trend, shrink the quarter toward the network, most complications now, biggest unit) lands on 41210, 41410 or 41220 | no control, corpus or document scores a method; the register carries facts only | the battery reconciles on the wrong path: series, dashboard and activity summary all tie | two constructions and a model choice over seven placements, none of them a subtraction of shipped figures | silent |

## Semantic fork table

| id | Term or convention | Golden reading | Alternatives and their call | Ruled out by |
|---|---|---|---|---|
| SF1 | "inpatient units" eligible for the placement | the 12 acute units with four or more closed quarters on specification 4.0 and no placement in the previous twelve closed quarters | all 21 acute units (41450 at 1.42 would win); all 24 units including non-acute | charter 4.2 names both conditions; specification 2.3 puts non-acute service types outside the indicator |
| SF2 | "hospital-acquired complications" | episodes with one or more complications on the national list in force at separation, specification 2.1 | complications counted (the detail extract's rows) | specification 2.1 counts episodes; `same call` on the ranking, different figures, asserted |
| SF3 | the indicator's denominator | acute multi-day episodes with a valid DRG band from an in-scope unit, specification 2.2 and 2.3 | all separations; all episodes including same-day | specification 2.2 and 2.3, four exclusions listed |
| SF4 | "avoid" | the difference between what the unit records with the team and what it would have recorded without it, charter 4.3 | the fall from the quarter before the placement to the assessment quarter | charter 4.3 states the counterfactual, not a period-on-period fall |
| SF5 | the unit of the answer | complications (a count) at the host unit over the assessment quarter, charter 4.3 | the fall in the unit's adjusted rate (41330 would win) | charter 4.3 counts complications; clause 4.4 ties them to planned separations |
| SF6 | the assessment quarter | 1 April to 30 June 2027, charter 4.1 and the prompt | the quarter after the placement; the following year | charter 4.1 names the quarter the team is embedded |
| SF7 | the activity the quarter carries | the planned separations in `activity_plan_2027q4.csv`, charter 4.4 | the latest closed quarter's separations; the four-quarter mean | charter 4.4 names the published plan |
| SF8 | a unit's expected complications for a future period | planned separations times the unit's expected complications per in-scope episode over the specification period to date, specification 3.4 | the latest quarter's rate per episode; the network's rate | specification 3.4 |
| SF9 | the reporting period of a unit's standardised ratio | every closed quarter from 1 July 2024, specification 3.3 | the last four quarters; the last eight; the fiscal year | specification 3.3; and `same call` under 4, 6 and 8 quarter windows, asserted |
| SF10 | the comparable history | 2024-25 Q1 to 2026-27 Q2 | quarters before 1 July 2024 | specification 3.5: earlier values are on specification 3.2's risk model and not comparable |
| SF11 | the amalgamated unit's record | 41510 from 1 October 2025, its predecessors 41511 and 41512 under their own codes | the three pooled into one ten-quarter record | specification 3.6; `same call` and the same figure either way, asserted (both stand at 1.16) |
| SF12 | the period an episode falls in | the period of its separation date, specification 2.5 | admission date; the complication's onset date | specification 2.5 |
| SF13 | the stratum rates | the rates published with specification 4.0 in `hac_stratum_rates.csv` | rates re-estimated from the extract | specification 3.1 names the published rates; `same call`, asserted |
| SF14 | rounding of the avoided complications | whole complications, as the prompt asks | one decimal | the prompt's closing sentence; every figure sits at least 0.10 of a complication inside its bin |
| SF15 | ties on the recommendation | none arises: 17 against 11 | - | `same call`; the margin is 1.52x, asserted |

## Ladder

Four rungs, each a complete pipeline from the raw files, each naming a different unit, each satisfying to
stop at. Figures measured on the built panel, not intended.

| Rung | The analysis | Names | Its own figure | Dies to |
|---|---|---|---|---|
| 0 | the complications each unit is recording above expectation in the quarter in hand, times the share the register's placements fell | 41210 Alderbrook General Medicine | 13 avoided | the unit's own record: 1.03 over ten quarters against 1.19 in the quarter, deviations with no serial correlation |
| 1 | the unit standing worst on its own record (highest standardised ratio over the specification period) | 41330 Stonecreek Vascular Surgery | 6 avoided | charter 4.3 counts complications and 4.4 ties them to planned separations: its 506 planned separations carry 16 complications above expectation, against 44 at 41230 |
| 2 | the complications the assessment quarter carries at each unit's own standing (where the harm will be) | 41220 Alderbrook General Surgery | 287 complications expected | the charter's word "avoid": 258 of the 287 are the expected number, and the register's falls track the excess, not the level (a share of the level misses the placement at 41440 by 141 per cent) |
| 3 (decisive) | the excess the planned quarter carries at the unit's own standing, priced as the share of persistent excess the seven closed placements removed | 41230 Alderbrook Orthopaedics | 17 avoided | - |

**Arithmetic, measured on the built pack.** Answer 41230, 16.83 complications avoided, rounding to 17.
Final margin 1.51x over 41220 (11.15, rounding to 11), gap 6. Position of the answer: 4th on rung 0 (41210
13.01, 41240 9.63, 41410 8.75, 41230 8.08), 3rd on rung 1 (41330 1.3118, 41420 1.2471, 41230 1.2311), 2nd on
rung 2 by 1.21x (41220 286.6 against 41230 236.4). No rung margin under 1.15x. Dominance: the answer's edge
on the decisive axis (excess at planned activity, 44.4 against 5.8 at the rung-0 unit, 7.7x) against the
rung-0 unit's carried advantage on the quarter in hand (34.0 against 21.3 excess complications, 1.60x):
7.7 >= 1.2 x 1.60. The share a placement removes is 0.3791 of a unit's standing excess, read over the seven
closed placements; its six readings (pooled, mean of the placements' own shares, median, least squares
through the origin, and two other readings of each unit's pre-placement record) span 0.375 to 0.383 and give
every one of the twelve units the same whole-complication figure, asserted.

**Reflexes, each measured on the built pack.** Adjusted rate now: 41410 at 141.0 per 1,000. Trend over the
last four quarters: 41410. Reliability-shrink the quarter toward the network mean: 41210. Most complications
recorded last quarter: 41210 (218). Biggest unit by planned separations: 41220. Every reflex lands on a unit
the golden does not name, asserted in `checks.py`.

**Grid.** Three binary axes: the counterfactual (the quarter in hand or the unit's own standing), the form
the register is read in (a share of the unit's standing excess, a share of its level, or a reduction per
expected complication, taken here as excess against level) and the activity basis (the published plan or the
latest quarter's separations). Eight cells, each computed in `checks.py`: every cell on the quarter in hand
files 41210, every cell that reads the register as a share of the level files 41220, the cell on the
standing with the wrong activity basis keeps 41230 but moves nine of the twelve figures, and only
(standing, share of standing excess, plan) is the golden. Every single-error cell files a feasible figure
and names a unit the answer does not, and the answer is the grid's extreme cell.

**Worth.** The decisive step moves the name (41210 to 41230) and all twelve graded figures; a response that
takes the unit's own standing but prices the register as the fall after a placement keeps the name and loses
every figure (17 becomes 32); a response that prices correctly but ranks on the quarter in hand loses both.
Measured on the graded name and the graded figures separately, as `stumping` Part 3 requires.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which units are candidates | charter 4.2 filed literally, both conditions computable from the registers; no unit near the four-quarter edge but 41510 at five; units not yet observed do not arise (the candidate set is closed at the as-of date) |
| 2 | Unit of account | complications, or the rate | charter 4.3 and 4.4 file complications at the host unit (SF5) |
| 3 | Attribution window | which period an episode falls in | specification 2.5: the separation date; no episode has an admission and separation in different quarters within 12 days of a boundary, asserted |
| 4 | As-of dating | the state of the records at the pull | the extract, the series and the dashboard all carry 2027-03-05 as their export date and stop at 2026-27 Q2; the plan is the published 2027-02-20 version |
| 5 | Version basis | the register's current state against the state in a past month | the manifest states that `unit_register.csv` is the unit master at the export date, and the activity summary carries the facility each unit sat in each month (ask 2's device, not on the call's path) |
| 6 | Denominator | what sits under the indicator | specification 2.2, 2.3 and 3.1 to 3.4, four exclusions, published stratum rates |
| 7 | Weighting | pooled against a mean of quarterly ratios | the pooled ratio is the indicator's own definition (specification 3.2); the mean of quarterly ratios gives the same call and the same twelve figures, asserted |
| 8 | Window length | how far back a unit's standing is measured | specification 3.3 files the reporting period; the call also holds under 4, 6 and 8 quarter windows, asserted |
| 9 | Boundary inclusivity | quarters and years | every period is a whole quarter; the hospital-level ask's year is named in the prompt and the reconfiguration falls on a quarter boundary (1 July 2026) |
| 10 | Rounding path | where rounding happens | computed unrounded, rounded once at the end; the prompt's closing sentence; the workbook and the brief carry the same figures at the same rounding, asserted |
| 11 | Tie-break | two units level | none arises, 17 against 11 (SF15) |
| 12 | Maturity and censoring | episodes still open, quarters not yet coded | the extract carries separated episodes only, and stops at the last quarter coded in full (the coding close date is in the manifest); the placement in progress has no closed assessment quarter, which no figure needs |
| 13 | Order of operations | risk adjustment before or after pooling | specification 3.2 defines the ratio as observed over expected summed over the period; computing quarterly ratios first gives the same twelve figures, asserted |
| 14 | Row order | file order | every figure is a sum or a ratio of sums; asserted invariant under two permutations of the extract |
| 15 | Duplicate resolution | repeated episode records | none in the indicator's population, asserted by count; the re-sent batches sit in the non-acute units (ask 3's device) and the activity summary reconciles them |
| 16 | Identity normalisation | unit codes across files | cost centre codes are the key everywhere, zero-padded five digits, asserted joinable with no residue; the amalgamation is filed (SF11) |
| 17 | Netting against gross | may a unit below expectation offset one above | the question is one unit's placement, so nothing nets; units below expectation carry no excess and the golden names none |
| 18 | Dimensional units | complications, episodes, separations, rates per 1,000 | the dictionary states each column's unit; the reference rate 96.5 per 1,000 is filed in specification 3.2 |
| 19 | Code and status semantics | care type, service type, DRG bands, complication codes | the dictionary and the specification's appendices; never decisive |
| 20 | Integerisation | avoided complications are a count | computed unrounded and rounded once; every figure at least 0.10 of a complication inside its bin, asserted |
| 21 | Clause scope | charter clauses against specification clauses | the charter governs the placement, the specification governs the indicator; no clause of one restates the other, asserted by grep |
| 22 | Forward window contents | what the assessment quarter holds | `activity_plan_2027q4.csv`, the plan published 2027-02-20, is the only forward driver and charter 4.4 files it; dropping it moves every figure, asserted |

## Literal reader

Executing the prompt, charter clauses 4.1 to 4.4 and specification clauses 2.1 to 2.5 and 3.1 to 3.6 word for
word: the population is the twelve eligible units, the outcome is the specification's indicator, the window
is 1 April to 30 June 2027, the quantity is complications at the host unit, and the comparison is against
what the unit would have recorded without the team. Nothing in the shipped text says how that branch is
estimated or how the register prices a placement, and the easy estimator (the quarter in hand) comes from the
same literal estimand, so the literal reading lands on the golden's quantity and the stump sits in the
method. Every alternative reading in the fork table either violates a quoted sentence or returns the same
call, each asserted in `checks.py`.

## Oracles

No shipped control, corpus or document scores a method or ranks the units.

- `unit_indicator_series.csv`: a rollup of the extract at unit-quarter grain; ties on every path, and ties
  first for the default path.
- `quality_dashboard_2026q2.xlsx`: the quarter ended 31 December 2026, correct and labelled, carrying five
  indicators per unit with no rank, no flag and no forward figure. It confirms the default path's own
  quarter, which is the point.
- `activity_summary_monthly.csv`: separations and complications by unit and month; ties to the extract on
  every handling of the main population, and is the referee for ask 3.
- `improvement_placements.csv`: facts only, no achieved-reduction column, so it cannot be quoted back. The
  comparison that prices the programme is a construction the analyst makes from the extract, not a file.
- The three distractors answer other questions and are asserted not to move any graded figure.

## Stage 3 gates, measured

| Gate | Result |
|---|---|
| `generator/build.py` | 526 generator assertions, 88 independent checks, both green |
| Three-rules block on the clean truth | R1 raw material, R2 per Layer 1 item, R3a the easy route files 41210 at 13, R3b the decisive step alone files 41230, R3c no plant: all green |
| Independent verifier | `generator/verify.py` reads only `target/` and `figures.json`, recomputes every stated figure on pandas against the generator's csv path |
| Two byte-identical rebuilds | pack and both goldens identical across two fresh builds; `target/` equals the rebuild |
| Input gates | 20 files, 4 formats (csv, pdf, xlsx, txt), `episode_outcomes_extract.csv` at 219,348 rows, 3 distractors declared in `metadata.json` and named in no file name |
| `figures_check.py task194` | 97 figures in blocks 1 to 4, 0 absent from `generator/figures.json` |
| Realism sweep | no repeated unit-quarter counts, no round headline figure, personas only the two drawn, one export stamp on every file, containers clean under `scrub_producer_metadata.py` |
| `leak.py task194 --asof 2027-03-18` | REVIEW, no LEAK; every REVIEW answered above |
| `guard.py surface task194` | exit 0, three pairs promoted at 0.102 on relative surface similarity, no hard tell |
| `guard.py heart task194` | WARN, no BLOCK |
| `precut.py task194` | 49 checks, 0 FAIL, 0 WARN |
| House fixes | H1 containers scrubbed and audited, H4 the shipped set equals the manifest, H8 every cited clause and file resolves, H9 manifest set equality asserted, H11 one `submission.md` and one `prompt.txt`, H16 the only date past the as-of is the in-progress placement's planned end, H24 the manifest is the organisation's own compile note |

**Stage 4 is staged, not spawned.** This session has no Agent tool, so the leak reader and the determinism
judge are briefs on disk with their isolated inputs beside them, for the orchestrating session to spawn:
`task194_judge/judge_brief.md` (prompt, a fresh unzip of `target.zip`, the submission's graded blocks and
the judge system prompt inlined; verdict to `verdict.md`) and `task194_reader/reader_brief.md` (prompt and a
fresh unzip; answers to `reader_answers.md`), both under this session's scratch directory.


## Leak sweeps answered

`leak.py task194 --asof 2027-03-18` is REVIEW, no LEAK; sweeps 1, 2, 5, 7, 8 and 11 are clean. One line per
REVIEW:

- **Sweep 3, 118 lines, every one a cost centre code (41210 to 41630) in the files that key on it.** The
  candidates' own identifiers have to be in the register, the series, the extract, the plan, the summary, the
  dashboard and the three unit-level files; the answer is a named unit, so its code is in the pack by
  construction. No golden figure of four digits or more appears anywhere in the pack.
- **Sweep 4, three documents sharing 5 to 10 of the design note's 25 stump terms** (charter, activity,
  planned, record, closed, indicator, quarterly). These are the domain's own nouns and the words the
  specification and the charter use for the measure and the cycle. Neither document, nor the thread, names a
  counterfactual, a standing, an excess, a share or a placement's effect.
- **Sweep 6, `quality_dashboard_2026q2.xlsx` names four candidates beside numbers.** It is the monitoring
  export of the closed quarter: every acute unit in one alphabetical table, five indicators, no rank column,
  no flag, no forward figure, and a line under the title saying it is the quarter-end position and not a
  projection. It answers the monitoring question correctly and does not rank the units on the decision
  question. `hospital_sites.csv` (INFO) is a four-row site reference.
- **Sweep 9, one ISO date after the as-of in `improvement_placements.csv`: 2027-03-31.** It is the planned
  end of the placement in progress, which is the fact that puts the next cycle on 1 April; the register
  carries no close-out date for that row and the extract stops at 31 December 2026.
- **Sweep 10 (INFO), no writer signature.** `scrub_producer_metadata.py` reports both the pack and the
  goldens clean.


## Ask sheet

Main call's declared row population: the eligible and previously placed acute units' in-scope episode rows
for 2024-25 Q1 to 2026-27 Q2 and their `unit_code`, `separation_date`, `drg_code`, `age_band`, `care_type`,
`los_days` and `hac_flag` columns; the placement register's unit and quarter columns; the planned separations;
the stratum rates and band map; charter clauses 4.1 to 4.4; specification clauses 2.1 to 2.5 and 3.1 to 3.6.
Device rows in that population: **zero**, asserted by count in `checks.py` (A2 touches only `hospital_code`
and the activity summary's `facility`, A3 only non-acute units' rows, A4 only `hac_category_code`,
`hac_detail_extract.csv` and the category appendix).

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, measured on the built pack |
|---|---|---|---|---|---|---|---|
| A1 construction | 12 per-unit avoided complications, whole | the call's own construction on every candidate | the committee sees what each unit would gain | none (the ladder carries it) | - | 6 files, 11 columns | rung 0 files 13, 10, 9, 8 at the top and 2 at the answer; rung 2 files the expected-complication vector; the golden 17, 11, 9, 7, 6, 4, 3, 2, 2, 2, 2, 1 |
| A2 hospital year | 4 hospitals x (adjusted rate to one decimal, in-scope episodes, complications) = 12 | the audit trail of the indicator the call rests on, at the hospital cut the network reports on | the quality committee's own annual table | D2 attribute at the wrong vintage: three cost centres were realigned to another hospital site on 1 July 2026 and `unit_register.csv` is the master at the export date, so the site each unit reported under in each month lives only in `activity_summary_monthly.csv` | the calendar year against fiscal quarters; the amalgamation; the specification's four exclusions | 5 files, 12 columns | the register's alignment moves every one of the twelve figures: episodes by 42, 931, 1,364 and 2,337, complications by 3, 89, 159 and 251, and the rates by 0.1 to 3.0 per 1,000; a fiscal-year read moves all twelve |
| A3 activity outside the indicator | 10 quarters x (separations, episodes with a complication) = 20 | the audit trail of the indicator's scope, which the call's denominator consumes | the committee asks every cycle what sits outside the indicator | D1 replay under fresh identifiers: the sub-acute and mental health feed loads on an overlapping window, so the episodes separated in the last three days of a month arrive again in the next batch under new episode identifiers with the patient, the admission date and the DRG kept, beside genuine same-day pairs that differ in DRG; `activity_summary_monthly.csv` is the network's separations record and reconciles only on the de-duplicated count | the three non-acute service types; care type against service type | 4 files, 10 columns | the row count runs 8.1 to 11.4 per cent high in every one of the ten quarters; a de-duplication on unit, patient and admission date alone runs low in every quarter and loses an affected episode in 2025-26 Q3; the golden reconciles to the summary |
| A4 complication groups | 8 groups x 2 fiscal years = 16 | the audit trail of the numerator the call consumes, grouped as the specification groups it | the work plan for whichever unit is chosen | D5 silently partial extract: `hac_detail_extract.csv` is the clinical information system's feed and does not reach the wards on the Carrowdean campus, whose complications arrive only through the extract's own category column, one to an episode | the 1 July 2026 list revision, where HAC04 and HAC05 name different categories either side of the date and HAC13 was folded into HAC03; episodes with two complications | 4 files, 9 columns | the detail extract alone runs 1.8 to 4.7 per cent low in every group and both years; a raw code join against the current list moves G1 by +28, G2 by -17, G3 by -46 and G4 by -53 per cent in 2025-26 |

**Hazard table.** The 2026 list revision moves A4's sixteen figures and nothing else. The amalgamation moves
A2's Carrowdean figures and nothing in A3. The fiscal-against-calendar boundary moves A2's twelve figures.
The comorbidity blanks move nothing, and are texture.

**Referee.** `activity_summary_monthly.csv`, byte-clean, arbitrates A3's designed disagreement by carrying
separations and complications by unit and month without any indicator figure or any unit's standing.

**Cracker sheet.** The cracker landed the call, ran the hygiene battery (key uniqueness, exact duplicates,
unmatched joins, fan-out, count ties), executed every filed rule the pack points at and matched every
reconciliation.

| Ask figure (cracker) | What the cracker does | Verdict |
|---|---|---|
| A2 four adjusted rates | joins `unit_register.csv` for the hospital, which is the master at the export date | miss |
| A2 four episode counts | same join | miss |
| A2 four complication counts | same join | miss |
| A3 six separation counts | counts the extract's rows for the non-acute units (no exact duplicates, no fan-out, keys unique) | miss |
| A3 six complication counts | same | miss |
| A3 six rates per 1,000 | same numerator and denominator | miss |
| A4 eight 2025-26 group counts | groups `hac_detail_extract.csv` on the code as recorded | miss |
| A4 eight 2026-27 group counts | same source, so Carrowdean is absent | miss |

**Pair ceiling:** 36.2. The landed call banks 38 + 7 + 55 x (12 of 60 ask criteria) = 56.0 if it keeps the
construction layer whole and misses every device ask; the best response off the call keeps 5 + 7 + 55 x 0.08
= 16.4, since rung 2's response matches none of the twelve avoided counts and carries the same devices.
Average 36.2. The sensitivity worth naming: if the cracker also reads `unit_register.csv` as the master at
the export date and takes A2 whole, the pair rises to 41.7, which is why A2's device is the one measured
against the hygiene battery, where the register has one row per unit so no key check, fan-out check or
unmatched join reaches it.
**Mirror leakage:** 8.0 per cent of ask weight. The mirror stops at rung 2, files none of the twelve avoided
counts (its vector is the expected-complication one, 287, 236, 176, 128), and carries the same devices.

## Tried and rejected

- Ranking units by the fall in their adjusted rate rather than by complications avoided: the charter would
  have to file a rate, and then the whole decision is a one-column sort on each unit's own standing, with the
  planned activity and the register idle. Dropped at the draw; the charter files complications.
- Giving the closed placements a hot quarter the placement was decided on (a selection shock of 0.15), so the
  register's own falls were inflated by reversion as well: it put the share a placement removes 10 per cent
  apart depending on whether the decision quarter stayed in the unit's pre-placement record, which is a fork
  on a graded figure. Replaced by placements decided on units' standing, with the decision quarter at the
  unit's own level (asserted), so the register prices the programme the same way under every reading of its
  pre-placement window.
- Block-correcting each unit's quarterly deviations so the trailing four, eight and ten quarter windows all
  returned the unit's level exactly: it left the panel with a lag-1 autocorrelation of -0.28, which licenses
  an AR(1) counterfactual below the unit's level and forks every figure. Replaced by one uniform shift per
  unit (autocorrelation -0.107 over 156 pairs, what de-meaning a ten-quarter record implies).
- A monthly reconciliation ask whose gap was the activity summary's own vintage: it needed the summary to be
  short for the acute units too, which breaks the referee the call's own reconciliation leans on. Replaced by
  A3 on the non-acute units, where the summary stays exact and the replay is the device.
