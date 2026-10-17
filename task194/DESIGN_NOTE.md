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

**Data-native sentence.** The partnership's own closed register runs from a unit sitting at its expected
number of complications to one sitting at nearly twice it, and over that spread the shapes a placement's
fall could take predict falls that differ by many times the error a count of a few hundred episodes carries, so the register itself decides what an embed's
effect is proportional to, and nothing else in the pack does.

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

**Decisive step.** Read off the closed placement register what the fall an embed produces is proportional
to. The charter files the baseline, so a unit's position without the team is settled; what is not settled is
whether an embed removes a share of the standing excess the unit is carrying, a constant number of ratio
points, a constant percent of what the unit would have recorded, or a flat number of complications. All four
are models of the same filed quantity, they rank the twelve units differently, and the register is the only
evidence in the pack that chooses between them.

Which part of the estimand does it settle? **None of the five.**

| Part | Filed by | Sentence |
|---|---|---|
| Population | charter clause 4.2 | every acute inpatient unit still reporting under its own cost centre at the decision date, with four or more closed quarters of reported indicator data on specification 4.0, except a unit the team has been placed with in the previous twelve closed quarters and except the unit the team is placed with when the placement is decided (12 units; the three conditions take out the two wards closed into 41510, the eight units in the register and the unit the team is with now, and no unit is near the four-quarter edge except the amalgamated 41510 at five) |
| Outcome | specification 4.0 clauses 2.1 to 2.4 | episodes with one or more hospital-acquired complications, against the published stratum rates by risk band and age band, observed over expected |
| Window | charter clause 4.1 and the prompt | the assessment quarter, being the quarter the team is embedded: 1 April to 30 June 2027. The window of a unit's standing is specification 3.3's: every closed quarter from 1 July 2024, and no other period is reported for a unit |
| Unit | charter clause 4.3 | complications, counted at the unit that hosts the team, over the assessment quarter |
| Comparison | charter clause 4.3 | the complications the unit would have recorded over the assessment quarter without the embedded team, less the complications it records over that quarter with the team there: a difference between two counts over one quarter, not a movement between periods. The position the unit would have held without the team is its position over its own closed quarters before the team arrived, and not its position in any one of them, so the baseline's population and window are filed and only the shape of the fall is left open |

What stays open is the shape of the fall, and the design forces it. The eight closed placements spread
from a unit running at its expected number (standing 1.000) to one running at nearly twice it (1.979), and
over that spread a share of standing excess and a constant drop in the standardised ratio predict falls
that differ by many times the error a count of complications carries. Fitted by weighted least squares with
the counterfactual count as the variance, the shape the register carries leaves chi-square 2.68 on seven
degrees of freedom while a constant ratio-point drop leaves 35.57, a constant percent of the counterfactual
22.50 and a flat number of complications 22.54: likelihood ratios of 1.4e7, 2.0e4 and 2.1e4 to one. The
register is not fitted: its standardised residuals run -1.23 to +0.75 and its per-placement shares run
-0.65 to 1.33, so the scatter is what a few hundred episodes a quarter produce. Filing the difference and
the baseline in clause 4.3, the standing's window in specification 3.3, the row set and the in-progress
placement in clause 4.2 and the separation key in the dictionary closes every reading of WHAT and leaves
the shape of the fall, which is the method, open.

**The three surface promotions, ruled by the author.** `guard.py surface` promotes task194 against
task266, task448 and task466, each at 0.102 in the corpus's top 1 per cent, and none is a finding. The
promotion reason is surface similarity at the corpus's own floor, where `fingerprint` Part 5 puts the
cross-slot 99.9th percentile under 0.10, combined with this build carrying no ledger row yet, which makes
the severity read "status unknown on at least one side". The mechanism layer is card against card and the
hard-tell screen is clean, with only the two drawn personas in the cut pack, both on the card. The four
drivers are unrelated: this build prices the fall a scarce intervention causes against the unit's own
return to level, task266 estimates the share of spells ending one way from a record with many still open,
task448 completes a register from a second list whose capture depends on the filing route, and task466
fits a low quantile of a yearly extreme to two records of one process. Shared only are the coarse
`gate_g` and, with task266, `layer2_family`. `heart` is WARN and not BLOCK, so the stage-3 gate holds; the
adjudicated read stays the author's call under `/clone-check`.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' own grain.

1. Read `episode_outcomes_extract.csv`, apply specification 4.0's denominator and its four exclusions, join
   `drg_risk_bands.csv` and `hac_stratum_rates.csv`, and compute every unit-quarter's observed and expected
   complications; the result ties to `unit_indicator_series.csv` and to the dashboard export for the quarter
   ended 31 December 2026.
2. Apply charter clause 4.2 through `unit_register.csv` and `improvement_placements.csv`: twelve eligible
   units.
3. Take each unit's standing over the specification period, which charter 4.3 holds it to without the team,
   and clause 3.4's expected complications on the quarter's planned separations.
4. Price the programme off `improvement_placements.csv`: across the eight closed placements the standardised
   ratio fell by 0.197 on average, which is how a quality team states what an embed achieves.
5. Apply that drop to each unit's expected complications for the quarter: Alderbrook General Surgery 53,
   Alderbrook Orthopaedics 37, Alderbrook General Medicine 34, Alderbrook Respiratory Medicine 23.
6. Place the team with Alderbrook General Surgery, 53 complications avoided over the quarter.

**Ends on:** Alderbrook General Surgery (cost centre 41220), 53 complications avoided.
**Golden:** Alderbrook Orthopaedics (cost centre 41230), 21 complications avoided.

Reading the register as a constant percent of what the unit would have recorded files the same unit (41220
at 53 against 41230 at 41); reading it as a flat number of complications a placement removes files 37.9 for
every unit and ranks nothing. The default path reconciles everywhere a solver checks it: the unit-quarter
observed and expected counts tie to the published indicator series row for row, the quarter's adjusted rates
tie to the dashboard export, and the monthly activity summary ties to the extract's separations.

## Stump sentence

A competent solver takes each unit's standing exactly as charter 4.3 files it, prices the programme off the
closed register as the average drop in the standardised ratio a placement produced, applies that drop to the
complications the quarter's planned activity carries, and places the team with Alderbrook General Surgery
for 53 complications avoided, which is the unit with the most activity rather than the unit with the most
excess for an embed to work on.

## Three rules

- **Task type:** `provider-quality-risk-adjustment`, which the client taxonomy lists under Anomaly Detection
  & Diagnostics: separating a provider's real signal from what measuring it produces is the task type's own
  work, and the pack ships the episode-level raw material the risk model runs on.
- **Domain test:** the deciding quantity is the reduction in a risk-adjusted provider outcome attributable
  to an improvement intervention. Provider profiling estimates it by fitting the intervention's effect to a
  closed record of past interventions, against the sampling error a count of complications carries, and by
  asking what that effect is proportional to: a provider's excess over its risk-adjusted expectation, its
  risk-adjusted rate, or its volume. Indirect standardisation, the dispersion of a count of complications
  and the closed placement record are the field's own instruments and all three ship.
- **Swap:** "Which of our twelve machines should the calibration crew spend the quarter with, and how many
  out-of-tolerance parts would that avoid?" With machines measured without error the record of past crews is
  a clean table that any of the four shapes fits exactly, and nothing chooses between them: the question
  becomes arithmetic. The task only works where the outcome is a count of a few hundred risk-adjusted events,
  because it is the size of that sampling error against the spread of the closed record that decides which
  shape the evidence supports.
- **Layer 1:** episode records at two grains (the episode extract against the monthly activity summary and
  the quarterly indicator series, both rollups of the same records); a national complication list revision on
  1 July 2026 that renames and reissues category codes (the coding service's own change); two medical wards
  amalgamated into cost centre 41510 on 1 October 2025 (a service reconfiguration); a comorbidity score keyed
  on only 85 per cent of episodes network wide and at a rate that varies by unit (clinical coding does not
  key it for every episode); a dashboard export correct and labelled for the quarter ended 31 December 2026
  (the monitoring system's quarterly export); tables inside PDFs (the specification's stratum and category
  appendices); fiscal quarters against the calendar year the hospital-level ask uses; three cost centres
  realigned to another hospital site on 1 July 2026 while the register carries only the current alignment (a
  divisional restructure); wards that are not on the clinical information system, so their complications
  reach the warehouse only as the episode record's own category (a system boundary the register and the
  manifest both declare); patient index numbers issued in blocks as each site came onto the index, so the
  same number is never shared across two sites. Every item is what these systems produce, nothing is placed
  to be caught, and each is asserted neutral in `checks.py` (R2).
- **Layer 2:** `estimand_identification`. The methodological choice that flips the call is what the fall an
  embed produces is proportional to: the standing excess a unit is carrying, the unit's standardised ratio,
  what the unit would have recorded, or nothing at all. Each ranks the twelve units differently, and only the
  closed register's own fit distinguishes them.
- **Decisive step:** read the register as a share of standing excess, because its eight closed placements
  spread from a unit at its expected number to one at nearly twice it, and over that spread only a share of
  standing excess fits within the error a count of complications carries: chi-square 2.68 on seven degrees of
  freedom against 35.57 for a constant drop in the standardised ratio, 22.50 for a constant percent of the
  counterfactual and 22.54 for a flat number, likelihood ratios of 1.4e7, 2.0e4 and 2.1e4 to one.
- **Not semantics:** every field, code, unit and definition read correctly still leaves the easy route on
  Alderbrook General Surgery. The extract's fields are plain, the specification files the denominator, the
  exclusions, the stratum rates, the reporting periods and the forward expectation basis, and the charter
  files the population, the outcome, the window, the unit, the comparison and the baseline that comparison is
  taken over. A solver who reads every one of them correctly, whose observed and expected counts tie to the
  published series row for row and who takes the standing exactly as clause 4.3 files it, still prices the
  programme as the average drop in the standardised ratio a placement produced and files 35 complications
  avoided at 41220.
- **Not rule application:** no filed rule, formula or procedure says what the fall an embed produces is
  proportional to. The charter names the quantity, the baseline and the activity basis and stops; the
  specification defines the indicator and its reporting periods and stops; the register carries dates, cost
  centres and staffing and no achieved reduction. Executing every stated rule gives each unit a standing and
  an expected number and leaves four shapes of the fall standing, which only a fit against the register's own
  sampling error separates.
- **Analyst test:** a strong analyst who risk-adjusts every unit correctly, applies the charter's
  eligibility, baseline and activity clauses and prices the programme off the closed register states the
  programme's effect the way a quality team states it, as the drop in the standardised ratio a placement
  produced, and places the team with Alderbrook General Surgery (41220) for 35 complications avoided; the
  same register read as a share of standing excess gives 41220 15 and names Alderbrook Orthopaedics at 24.
- **Estimand:** "the complications the unit would have recorded over the assessment quarter without the
  embedded team, less the complications it records over that quarter with the team there", charter clause
  4.3, with the population in clause 4.2, the assessment quarter in clause 4.1, the activity basis in clause
  4.4, the standing's reporting period in specification 3.3 and the indicator in specification 4.0 clauses
  2.1 to 2.4 and 3.1 to 3.4.
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
| SF1 | "inpatient units" eligible for the placement | the 12 acute units still reporting under their own cost centre with four or more closed quarters on specification 4.0, no placement in the previous twelve closed quarters and not the unit the team is with now | all 21 open acute units (41450 at 1.98 would win); the 2 wards closed into 41510, which would make 14 rows; the unit the team is with now, which would make 13 | charter 4.2 names all three conditions, and `closed_date` in the unit register makes the first computable; specification 2.3 puts non-acute service types outside the indicator |
| SF2 | "hospital-acquired complications" | episodes with one or more complications on the national list in force at separation, specification 2.1 | complications counted (the detail extract's rows) | specification 2.1 counts episodes; `hac_category_list.csv` carries both revisions with the date each took effect; `same call` on the ranking, different figures, asserted |
| SF3 | the indicator's denominator | acute multi-day episodes with a valid DRG band from an in-scope unit, specification 2.2 and 2.3 | all separations; all episodes including same-day | specification 2.2 and 2.3, four exclusions listed |
| SF4 | "avoid", and the position it is measured from | the difference between what the unit records with the team and what it would have recorded without it, charter 4.3, with the without-team position taken over the unit's own closed quarters before the team arrived | the fall from the quarter before the placement to the assessment quarter; the position in the quarter closed at the decision (41210 would win on either) | charter 4.3 states a difference between two counts over the same quarter and names the quarters the without-team position is taken over |
| SF5 | the unit of the answer | complications (a count) at the host unit over the assessment quarter, charter 4.3 | the fall in the unit's adjusted rate (41330 would win) | charter 4.3 counts complications; clause 4.4 ties them to planned separations |
| SF6 | the assessment quarter | 1 April to 30 June 2027, charter 4.1 and the prompt | the quarter after the placement; the following year | charter 4.1 names the quarter the team is embedded |
| SF7 | the activity the quarter carries | the planned separations in `activity_plan_2027q4.csv`, charter 4.4 | the latest closed quarter's separations; the four-quarter mean | charter 4.4 names the published plan |
| SF8 | a unit's expected complications for a future period | planned separations times the unit's expected complications per in-scope episode over the specification period to date, specification 3.4 | the latest quarter's rate per episode; the network's rate | specification 3.4 |
| SF9 | the reporting period of a unit's standardised ratio | every closed quarter from 1 July 2024, specification 3.3, which is also the window charter 4.3's without-team position is taken over for a unit with no placement | the last four quarters; the last eight; the fiscal year | specification 3.3's second sentence, that no other period is reported for a unit; and `same call` under 4, 6 and 8 quarter windows, asserted |
| SF10 | the comparable history | 2024-25 Q1 to 2026-27 Q2 | quarters before 1 July 2024 | specification 3.5: earlier values are on specification 3.2's risk model and not comparable |
| SF11 | the amalgamated unit's record | 41510 from 1 October 2025, its predecessors 41511 and 41512 under their own codes | the three pooled into one ten-quarter record | specification 3.6; `same call` and the same figure either way, which the generator makes exact by setting the two wards' pooled position to the amalgamated unit's own, asserted |
| SF12 | the period an episode falls in | the period of its separation date, specification 2.5 | admission date; the complication's onset date | specification 2.5; and `same call` on the admission period, computed and asserted (7.1 per cent of in-scope episodes span a quarter boundary) |
| SF13 | the stratum rates | the rates published with specification 4.0 in `hac_stratum_rates.csv` | rates re-estimated from the extract | specification 3.1 names the published rates; `same call`, asserted |
| SF14 | rounding of the avoided complications | whole complications, as the prompt asks | one decimal | the prompt's closing sentence; every figure sits at least 0.15 of a complication inside its bin under every one of the eight routes through the register, and the register would have to move by 6.6 complications of fall before any of them changed |
| SF15 | ties on the recommendation | none arises: 21 against 13 | - | `same call`; the margin is 1.59x, asserted |

## Ladder

Four rungs, each a complete pipeline from the raw files, each naming a different unit, each satisfying to
stop at. Figures measured on the built panel, not intended.

| Rung | The analysis | Names | Its own figure | Dies to |
|---|---|---|---|---|
| 0 | the complications each unit is recording above expectation in the quarter in hand, times the share the register's placements fell | 41210 Alderbrook General Medicine | 22 avoided | charter 4.3, which takes the position the unit would have held from its own closed quarters before the team arrived and not from one of them; and the unit's own record, 1.0291 over ten quarters against 1.1778 in the quarter |
| 1 | the unit standing worst on its own record (highest standardised ratio over the specification period) | 41330 Stonecreek Vascular Surgery | 10 avoided | charter 4.3 counts complications and 4.4 ties them to planned separations: its 506 planned separations carry 14.8 complications above its standing, against 31.1 at 41230 |
| 2 (the default path) | the standing the charter files, with the programme priced off the register as the average drop in the standardised ratio a placement produced | 41220 Alderbrook General Surgery | 53 avoided | the register's own fit: a constant ratio-point drop leaves chi-square 47.35 on seven degrees of freedom against 2.67 for a share of standing excess, 5.0e9 to one against it |
| 3 (decisive) | the same standing, with the programme priced as the share of standing excess the register's own spread supports | 41230 Alderbrook Orthopaedics | 21 avoided | - |

**Arithmetic, measured on the built pack.** Answer 41230, 20.98 complications avoided, rounding to 21.
Final margin 1.59x over 41220 (13.18, rounding to 13), gap 8. Position of the answer: 4th on rung 0 (41210
22.31, 41240 14.01, 41410 12.00, 41230 11.35), 3rd on rung 1 (41330 1.2887, 41420 1.1709, 41230 1.1641), 2nd
on rung 2 by 1.32x (41220 290.3 against 41230 220.5). No rung margin under 1.15x. Dominance: the answer's
edge on the decisive axis (excess at planned activity, 31.1 against 4.9 at the rung-0 unit, 6.29x) against
the rung-0 unit's carried advantage on the quarter in hand (33.1 against 16.8 excess complications, 1.97x):
6.29 >= 1.2 x 1.97.

**How the register forces the shape, measured.** Eight closed placements, fitted by weighted least squares
with the counterfactual count as the variance, on seven degrees of freedom:

| Shape of the fall | Parameter | Chi-square | Against the register's own fit |
|---|---|---|---|
| a share of the unit's standing excess | 0.67312 | 2.67 | - |
| a constant drop in the standardised ratio | 0.19739 | 47.35 | 5.0e9 to 1 |
| a constant percent of the counterfactual | 0.18397 | 27.71 | 2.7e5 to 1 |
| a constant number of complications | 38.36 | 25.51 | 9.2e4 to 1 |

What separates them is the spread of standing across the register: the placements run from units sitting a
tenth above their expected number (1.102, 1.104, 1.110, 1.121) to units sitting nearly twice it (1.719,
1.871, 1.930, 1.979), and over that spread a share of the excess and a drop in the ratio predict falls that
differ by many times the error a count of complications carries. Each fit, its parameter, its chi-square and
its likelihood ratio is asserted by its measured value in `checks.py` and again in `verify.py`.

**The register is read, not averaged, and its scatter says so.** The eight placements' own shares run
0.022, 0.587, 0.639, 0.652, 0.673, 0.776, 0.796 and 1.232: one placement took off almost none of the
standing excess its unit was carrying and one took off more than all of it. The standardised residuals run
-0.92 to +0.84 and the fit leaves chi-square 2.67 on seven degrees of freedom, which is what a few hundred
episodes a quarter produce. **A reader meeting a share of 0.022 beside one of 1.232 is seeing the point, not
a defect**: the shares scatter because they are ratios of two noisy counts, which is exactly why the shape
has to be fitted against that noise rather than read off an average, and it is why the four shapes separate
by nine orders of magnitude while the eight ways of pooling the register agree to one per cent.

**Every route through the register, and all eight converge.** Every closed placement carries a standing
excess a share can be formed on (the smallest is 15.9 complications), so no route is refused because it
cannot be computed. The expected-weighted mean of the placements' shares gives 0.679434; least squares with
an intercept 0.679270; least squares through the origin 0.676115; the pooled sums 0.674867; the pooled fall
net of what the units the team was not working on did over the same two quarters 0.674821; the
variance-weighted fit 0.673123; the median of the shares 0.672593; their unweighted mean 0.672126. They span
0.007308 of a share, 1.087 per cent, and every one of them gives all twelve units the same whole
complication and the same gap of 8, each asserted by name with its measured value in `checks.py` and again
in `verify.py`.

**Edges, stated as flip conditions.** The shares that reproduce all twelve counts run 0.66011 to 0.69109.
The pooled share 0.67487 sits 0.01476 above the floor and 0.01622 below the ceiling; the register's eight
placements carry 447 complications of standing excess between them, so **6.6 complications more in the
assessment quarters would take the share to the floor and 7.3 fewer to the ceiling**, and either edge moves
the answer's count off 21. No avoided count sits within 0.15 of a half (the closest is 41430 at 0.151). The
hospital year rates sit 0.345, 0.396, 0.191 and 0.445 of a bin from their own one-decimal edges.

**Why the reference rate is 96.6 and not 96.4.** The rate is specification 3.2's published constant and
nothing outside the pack depends on it. It was moved one tenth in the pass that rebuilt the hospital cut,
and one tenth again in the pass that rebuilt the register and the placed units, each time for the same
reason: it is the only lever on the four hospital-level adjusted rates, and at 96.4 and again at 96.5 one of
the four sat inside 0.07 of a bin from its one-decimal edge. At 96.6 the worst of the four sits 0.191 of a
bin clear. The arithmetic is in this note so the constant is not read as tuning.

**Reflexes, each measured on the built pack.** Adjusted rate now: 41410. Trailing four-quarter rate: 41330.
Reliability-shrink the standing toward the network mean: 41330. Most complications recorded last quarter:
41210. Biggest unit by planned separations: 41220. Fifteen rankings a careful analyst would try are computed
in `checks.py` with the unit each one names; only the golden's own family names 41230, and it holds the
answer by at least 1.30x wherever it does.

**Grid.** Two axes: the position the unit would have held without the team (the quarter in hand or its own
closed quarters before the team arrived, which charter 4.3 settles) and the shape of the fall (a share of
standing excess, a constant drop in the standardised ratio, a constant percent of the counterfactual, or a
flat number). Eight cells, each computed in `checks.py`: every cell on the quarter in hand files 41210,
every cell that prices the register on the unit's level or its volume files 41220, the flat-number cell
ranks nothing, and only (the filed baseline, a share of standing excess) is the golden. Every single-error
cell files a feasible figure and names a unit the answer does not.

**Worth.** The decisive step moves the name (41220 to 41230) and all twelve graded figures; a response that
takes the filed baseline but prices the register as a drop in the standardised ratio loses the name and
every figure (21 becomes 53 at the wrong unit); a response that also reads the baseline off the quarter in
hand loses both and lands on 41210. Measured on the graded name and the graded figures separately, as
`stumping` Part 3 requires.

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
| 18 | Dimensional units | complications, episodes, separations, rates per 1,000 | the dictionary states each column's unit; the reference rate 96.6 per 1,000 is filed in specification 3.2 |
| 19 | Code and status semantics | care type, service type, DRG bands, complication codes | the dictionary and the specification's appendices; never decisive |
| 20 | Integerisation | avoided complications are a count | computed unrounded and rounded once; every figure at least 0.10 of a complication inside its bin, asserted |
| 21 | Clause scope | charter clauses against specification clauses | the charter governs the placement, the specification governs the indicator; no clause of one restates the other, asserted by grep |
| 22 | Forward window contents | what the assessment quarter holds | `activity_plan_2027q4.csv`, the plan published 2027-02-20, is the only forward driver and charter 4.4 files it; dropping it moves every figure, asserted |

## Literal reader

Executing the prompt, charter clauses 4.1 to 4.4 and specification clauses 2.1 to 2.5 and 3.1 to 3.6 word for
word: the population is the twelve eligible units (clause 4.2's two exceptions both computable, the second
excluding the unit the team is with when the placement is decided), the outcome is the specification's
indicator, the window is 1 April to 30 June 2027 for the placement and specification 3.3's every closed
quarter from 1 July 2024 for a unit's standing, the quantity is complications at the host unit, and the
comparison is the count without the team less the count with it, clause 4.3. The hospital-level ask's basis
is pinned in its own asking sentence. Nothing in the shipped text says how that branch is
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
| `generator/build.py` | 690 generator assertions, 204 independent checks, both green |
| Three-rules block on the clean truth | R1 raw material, R2 per Layer 1 item, R3a the easy route files 41220 at 53 and the lower route 41210 at 22, R3b changing only the shape of the fall files 41230, R3c no plant: all green |
| Independent verifier | `generator/verify.py` reads only `target/` and `figures.json`, recomputes every stated figure on pandas against the generator's csv path |
| Two byte-identical rebuilds | pack and both goldens identical across two fresh builds; `target/` equals the rebuild |
| Input gates | 20 files, 4 formats (csv, pdf, xlsx, txt), `episode_outcomes_extract.csv` at 290,787 rows, 3 distractors declared in `metadata.json` and named in no file name |
| `figures_check.py task194` | 100 figures in blocks 1 to 4, 0 absent from `generator/figures.json` |
| Realism sweep | no repeated unit-quarter counts, no round headline figure, personas only the two drawn, one export stamp on every file, containers clean under `scrub_producer_metadata.py` |
| `leak.py task194 --asof 2027-03-18` | REVIEW, no LEAK; every REVIEW answered above |
| `guard.py surface task194` | exit 0, five pairs promoted on relative surface similarity in the corpus top 1 per cent, no hard tell, only the two drawn personas in the cut pack |
| `guard.py heart task194` | WARN, no BLOCK |
| `precut.py task194` | 49 checks, 0 FAIL, 0 WARN |
| `target.zip` | 20 entries at the archive root under their own names, md5 a1985ee1649f92a3ff69ccbfb6d03a1f, every entry asserted byte-identical to the file of the same name in `target/` and no entry carrying a directory |
| Register routes | the eight routes through the register span 0.672126 to 0.679434 (1.087 per cent) and give all twelve units the same whole complication and the same gap of 8; the four shapes the fall could take leave chi-square 2.67, 47.35, 27.71 and 25.51 on seven degrees of freedom, likelihood ratios of 5.0e9, 2.7e5 and 9.2e4 to one against the register's own fit; every one asserted by name with its measured value in `checks.py` and again in `verify.py` |
| House fixes | H1 containers scrubbed and audited, H4 the shipped set equals the manifest, H8 every cited clause and file resolves, H9 manifest set equality asserted, H11 one `submission.md` and one `prompt.txt`, H16 the only date past the as-of is the in-progress placement's planned end, H24 the manifest is the organisation's own compile note |

**Stage 4 is staged, not spawned.** This session has no Agent tool, so the leak reader and the determinism
judge are briefs on disk with their isolated inputs beside them, for the orchestrating session to spawn:
`task194_judge/judge_brief.md` (prompt, a fresh unzip of `target.zip`, the submission's graded blocks and
the judge system prompt inlined; verdict to `verdict.md`) and `task194_reader/reader_brief.md` (prompt and a
fresh unzip; answers to `reader_answers.md`), both under this session's scratch directory.


## Leak sweeps answered

`leak.py task194 --asof 2027-03-18` is REVIEW, no LEAK; sweeps 1, 2, 5, 7, 8 and 11 are clean. One line per
REVIEW:

- **Sweep 3, 119 lines, every one a cost centre code (41210 to 41630) in the files that key on it.** The
  candidates' own identifiers have to be in the register, the series, the extract, the plan, the summary, the
  dashboard and the three unit-level files; the answer is a named unit, so its code is in the pack by
  construction. No golden figure of four digits or more appears anywhere in the pack.
- **Sweep 4, three documents sharing 5 to 13 of the design note's 25 stump terms** (charter, activity,
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
| A1 construction | 12 per-unit avoided complications, whole | the call's own construction on every candidate | the committee sees what each unit would gain | none (the ladder carries it) | - | 6 files, 11 columns | rung 0 files 22, 14, 12, 11 at the top and 11 at the answer; rung 2 files 53, 37, 34, 23 at the top; the golden 21, 13, 11, 10, 8, 5, 4, 3, 3, 3, 2, 1 |
| A2 hospital year | 4 hospitals x (adjusted rate to one decimal, in-scope episodes, complications) = 12 | the audit trail of the indicator the call rests on, at the hospital cut the network reports on | the quality committee's own annual table | D2 attribute at the wrong vintage: three cost centres were realigned to another hospital site on 1 July 2026 and `unit_register.csv` is the master at the export date, so the site each unit reported under when an episode separated lives only in `activity_summary_monthly.csv`'s `facility` column, which the asking sentence points at without naming | the calendar year against fiscal quarters; the amalgamation; the specification's four exclusions | 5 files, 12 columns | the register's alignment moves every one of the twelve figures: episodes by 3,918, 4,960, 112 and 930 at the four hospitals, and the rates with them; a fiscal-year read moves all twelve |
| A3 activity outside the indicator | 10 quarters x (separations, episodes with a complication) = 20 | the audit trail of the indicator's scope, which the call's denominator consumes | the committee asks every cycle what sits outside the indicator | D1 replay under fresh identifiers: the sub-acute and mental health feed loads on an overlapping window, so the episodes separated in the last three days of a month arrive again in the next batch under new episode identifiers with the patient, the admission date and the DRG kept, beside genuine same-day pairs that differ in DRG; `activity_summary_monthly.csv` is the network's separations record and reconciles only on the de-duplicated count | the three non-acute service types; care type against service type | 4 files, 10 columns | the row count runs 7.7 to 10.1 per cent high in every one of the ten quarters; a de-duplication on unit, patient and admission date alone runs low in every quarter and loses an affected episode in 2025-26 Q3; the golden reconciles to the summary |
| A4 complication groups | 8 groups x 2 fiscal years = 16 | the audit trail of the numerator the call consumes, grouped as the specification groups it | the work plan for whichever unit is chosen | D5 silently partial extract: `hac_detail_extract.csv` is the clinical information system's feed and does not reach the wards that are not on that system, whose complications arrive only through the extract's own category column, one to an episode; `unit_register.csv`'s `clinical_information_system` column says which units those are and the manifest says what the feed omits | the 1 July 2026 list revision, where HAC04 and HAC05 name different categories either side of the date and HAC13 was folded into HAC03; episodes with two complications | 4 files, 9 columns | the detail extract alone runs 0.9 to 3.1 per cent low in every group and both years; a raw code join that ignores the revision column moves G1 by +30, G2 by -12, G3 by -47 and G4 by -50 per cent in 2025-26 |

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
| A2 four adjusted rates | joins `unit_register.csv` for the hospital, which is the master at the export date and not the site the episode separated under | miss |
| A2 four episode counts | same join | miss |
| A2 four complication counts | same join | miss |
| A3 six separation counts | counts the extract's rows for the non-acute units (no exact duplicates, no fan-out, keys unique) | miss |
| A3 six complication counts | same | miss |
| A3 six rates per 1,000 | same numerator and denominator | miss |
| A4 eight 2025-26 group counts | groups `hac_detail_extract.csv` on the code as recorded | miss |
| A4 eight 2026-27 group counts | same source, so the units off the clinical information system are absent | miss |

**Measured by:** `generator/cracker.py`, run on the cut pack; `checks.py` asserts both figures against it.

**Pair ceiling:** 34.5. The landed call banks 38 + 7 + 55 x (12 construction criteria of 60) = 56.0, keeping
the construction layer whole and missing every device ask: the cracker's hospital figures all miss on the
register join, its ten quarters outside the indicator all miss on the row count, and its sixteen group
counts all miss on the code as recorded. The best response off the call banks 5 + 7 + 55 x (1 of 60) = 12.9,
because rung 2's vector matches one of the twelve avoided counts and it carries the same devices. Average
34.5. The sensitivity worth naming: if the cracker reads `activity_summary_monthly.csv` for the site each
unit reported under and takes A2 whole, the pair rises to 39.2, which is why A2's device is the one measured
against the hygiene battery, where the register has one row per unit so no key check, fan-out check or
unmatched join reaches it.

**Mirror leakage:** 1.7 per cent of ask weight. The mirror stops at rung 2, matches one of the twelve
avoided counts and carries the same devices.

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

- **This pass, the reader's and the judge's findings in one generator pass.** The judge's recomputation
  confirmed the structure and asked for four things; the reader found a data defect and a realism list. The
  register's ten readings were brought from a 10.75 per cent spread to 2.9 per cent by levelling the network's
  own quarterly position and holding the comparison units still across each placement's two quarters, with
  the two operations writing disjoint unit-quarters so they no longer undo each other, and by choosing the
  embed-quarter counts once on the narrowest reading band rather than twice on different objectives. What
  "avoided" means is filed as a difference between two counts in charter 4.3, the standing's window in
  specification 3.3, and the in-progress placement in charter 4.2. The shared-admission path recomputed the
  length of stay, so no episode now separates before it was admitted. Ask 1's basis is pinned in the asking
  sentence and ask 3's missing units are declared in `unit_register.csv`.
- **Rejected: grading the twelve per-unit figures as the effect-free excess** to take the register's reading
  out of them. The prompt would then have to ask for the complications a unit's planned activity carries
  above its own standing, which files the decisive step. Kept the avoided counts and centred each unit's
  planned volume so all twelve round the same way under every reading instead.
- **Rejected: a cross-site patient index collision as texture.** Two episodes in different hospitals shared a
  patient number and an admission date, which reads as one duplicated episode and puts ask 1's episode count
  in play. Issued the index in blocks by site instead, which is what a master index does.

- **This pass, the judge's SEND_BACK closed on the register rather than by filing a method.** The judge
  found three pricings of the embed defensible on a register that carried no sampling noise: its own fit was
  chi-square 0.006 on six degrees of freedom and the likelihood ratio over the constant-drop shape was 1.8 to
  1. The repair widened the closed placements' standing from a unit at its expected number to one at nearly
  twice it, which is what makes a share of excess and a constant drop predict different falls, and let the
  quarters before each placement and the assessment quarters carry their own scatter instead of being forced.
  The three competing shapes now sit 1.4e7, 2.0e4 and 2.1e4 to one against the register's own fit, measured
  and asserted. The charter files the baseline's population and window and nothing about the shape of the
  fall.
- **Rejected: filing the effect model in the charter**, which the judge offered. It closes the fork and
  spends the stump in the same sentence: with the shape filed, every remaining step is arithmetic the
  specification already prescribes.
- **Rejected: more closed placements at the same spread of standing.** Volume moves a chi-square linearly
  and the gap needed was two orders of magnitude; what moved it was the second constraint inside the record,
  the spread of the placements themselves, which is the lesson task190 landed on from the other side.
- **Rejected: the unweighted and expected-weighted means of the per-placement shares as readings that have
  to converge.** One closed placement was made with a unit running at its expected number, so it has no
  standing excess to take a share of; those two estimators cannot be formed at all, and the register's own
  structure is what rules them out rather than a sentence.
- **Rejected: the two-constraint levelling** (holding both the unweighted and the pooled movement of the
  comparison units flat). With placed units an order of magnitude apart in size, the slope it needs pushes
  small units down and large units up by 0.1 of a ratio across the panel. One pooled constraint, and one
  difference-in-differences reading rather than two, leaves every unit's own record where it was.

- **This pass, the two routes the coordinator found.** A solver who meets an undefined per-placement share
  drops that placement and averages the rest, and that route is formable. Measured on the previous pack it
  gave 0.50719 against a pooled 0.52947 and the expected-weighted version gave 0.55306, both outside the
  window the twelve counts allow (0.51834 to 0.53955), moving six of the twelve. Rather than narrow the
  route set, the placement that was running at its expected number was raised to a tenth above it, so every
  share can be formed and all eight routes are asserted. The price was paid on the fit, as offered: the
  constant-percent shape went from 2.7e5 to one down and back up to 2.7e5 to one once the register was
  re-searched, and the headroom improved rather than fell, from 4.5 complications to 6.6.
- **Rejected: keeping a negative per-placement share alongside the two mean routes.** A placement that shows
  a rise is the right texture, but on a placement carrying 16 complications of standing excess it moves the
  unweighted mean of the shares by about 0.011, which is a third of a bin on the answer against the slack the
  eight routes leave. The register keeps the scatter in the form the window allows: one placement at 0.022
  that took off almost none of the excess it was carrying, one at 1.232 that took off more than all of it,
  and standardised residuals from -0.92 to +0.84.
