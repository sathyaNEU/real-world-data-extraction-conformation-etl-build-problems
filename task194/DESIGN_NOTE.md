# task194 design note

Placing a scarce improvement team when the unit standing worst is partly standing worst by chance.

## Draw

**Architecture 2.** Architecture 1 was sent back at stage 4 and is spent; its identity, fate and driver are
in the card's `lineage` and its dead end is the last entry under `## Tried and rejected`. The world is kept
whole: Mid-Rivers Health Network, four hospitals in regional Australia, the hospital-acquired complication
indicator on specification 4.0, the episode extract, the quarterly series, the activity plan, the unit
register and the closed placement register. What is re-chosen is the quantity the call rests on.

**Card:** `healthcare-delivery-health-economics` / `provider-quality-risk-adjustment`, objective
`anomaly-detection`, shape 14, decision `pick_one_of_n`, gap `objective`, Gate G
`decomposition_attribution`, strategy `composition_mix`, Layer 2 family `field_method`, pattern
`own:internal-against-external-standardisation`, generators G6, G14, G11, G2, calibration form `none`,
context artifact `monitoring_export`, forum `executive_team`, forcing event `budget_or_appropriation`,
question form `which`, role family `portfolio_manager`, people Maureen Watts and Joseph Hunter.
`guard.py check` clears every BLOCK; nearest driver on file 0.06 (task464 v1). Six axes were redrawn
against live BLOCKs while sibling builds registered beside this one: the context artifact twice
(`published_series` against task191, then `filed_standard` against task240, settling on the dashboard
export), the forum, the forcing event twice, the role family, and the decisive gap, which moved from
`population` to `objective` because gap, generator and decision type together were spent in four earlier
builds.

**The two WARNs, answered.** `overuse.objective`: anomaly detection is four of the last twelve, and this
draw is in it because the question is whether a unit's reported excess is the unit or the measurement
system, which is the objective's own work; the Gate G mechanism, the strategy, the Layer 2 family, the gap
and the generators are all different from every other anomaly-detection build on file.
`repeat.question_form`: "which" repeats task240 across the last two prompts, and it is the only honest
opening for a pick of one unit from twelve; the prompt's shape, deliverables and sentence structure are
drawn independently of it.

**The quantity the call rests on is measured, not fitted.** Every graded figure is a count summed from the
record: a unit's observed complications, the complications the comparison population's own rates give its
patients, and the difference between them on the quarter's planned activity. Nothing in the call requires a
functional form to be chosen, which is the failure that spent architecture 1.

**Data-native sentence.** Specification 4.0's stratum rates were set on FY2023-24 network activity and
clause 3.1 says they are not re-estimated between specifications, while the network's own rate has since
moved in opposite directions across the complication groups; because the twelve candidate units differ
several-fold in case mix, a ratio against those published rates carries each unit's composition as well as
its practice, and the units it penalises most are the ones whose patients sit where the standard has gone
most out of date.

**Sources read.** `references/client/two-layer-task-design.md`: the client's two-layer standard, which this
draw answers with the published standard as Layer 1 furniture and the comparison's construction as Layer 2.
`strategies.md` Part 4 and Part 6: `composition_mix` is drawn here because the composition that moves the
answer is a risk-stratum mix the pack publishes a rate table for, not a segment share a column names, and
no build on file carries that. `guard.py mechanisms --objective anomaly-detection`: the anomaly-detection
drivers on file turn on a count read before its records arrive, a selected extreme against the record of
extremes, a shared driver with lagged response, and a detection threshold that moves; none turns on the
standard the excess is measured against.

**Kept from architecture 1, which the judge confirmed sound:** the eight-placement register with its spread
of standing, the charter sentence fixing a unit's position as its own closed quarters rather than any one
of them, the eligible row set and the separation key pinned, the realism work on casemix, weekday,
holidays, length of stay and comorbidity, the measured cracker, and the series tying to the extract on all
215 unit-quarters with no shipped file ranking the candidates.

**Two defects carried forward as stage 3 work, not inherited:** the four hospital-level adjusted rates are
still edge-fragile, one at 0.019 of a bin and another flipping on a single complication either way; and the
activity summary equals a de-duplication on one key in all 90 unit-months while the dictionary states
another, which gives supplementary answer 6 two defensible series. Both are closed before any reader sees
the pack.

## Default path

The pipeline a competent analyst builds from the prompt's words and the files' own grain. Figures are
measured at stage 2 on the built panel; the names below are what the design puts at each step.

1. Read `episode_outcomes_extract.csv`, apply specification 4.0's denominator and its four exclusions, join
   `drg_risk_bands.csv` and `hac_stratum_rates.csv`, and compute every unit-quarter's observed and expected
   complications; the result ties to `unit_indicator_series.csv` row for row and to the dashboard export.
2. Apply charter clause 4.2 through `unit_register.csv` and `improvement_placements.csv`: twelve eligible
   units.
3. Take each unit's observed complications less its expected complications over the specification period,
   and scale that excess to the quarter's planned separations under clause 3.4.
4. Rank the twelve on that excess and read the top.
5. Put the improvement team with the unit at the top of that ranking.

**Ends on:** Alderbrook General Surgery (cost centre 41220).
**Golden:** Alderbrook Orthopaedics (cost centre 41230), 40 avoidable complications on its 2,305
planned separations. The unit the default path names carries minus 3.

## Stump sentence

A competent solver reconciles to the published indicator, ranks the eligible units on the complications
each records above the expectation the published stratum rates give it, and places the improvement team
with Alderbrook General Surgery (cost centre 41220), which is the unit whose patients sit where the
published standard has gone most out of date rather than the unit whose own patients are having the most
complications they should not be having; on the comparison the charter asks for, that unit is carrying
minus 3 avoidable complications and the unit that is carrying 40 sits fourth on the ranking it read.

## Three rules

- **Task type:** `provider-quality-risk-adjustment`, which the client taxonomy lists under Anomaly
  Detection & Diagnostics: separating a provider's own signal from what the measurement system produces is
  the task type's own work, and the pack ships the episode-level raw material the risk model runs on.
- **Domain test:** the deciding quantity is a provider's excess over the outcome its own case mix implies.
  Provider profiling obtains it by standardising, either indirectly against a published external standard
  or against the rates the comparison population itself achieves, and the two agree only while the external
  standard still matches that population. Indirect standardisation, stratum-specific rates and the case-mix
  distribution are the field's own instruments and all three ship.
- **Swap:** "Which of our twelve machines should the calibration crew spend the quarter with, and how many
  out-of-tolerance parts is it producing that it should not be?" Machines calibrated against a fixed
  reference run one uniform process, so there is no case mix for a standard to mis-state and the published
  excess is the excess: the question becomes a sort. The task only works where the outcome is risk adjusted
  against a published table and the units differ in the patients they treat.
- **Layer 1:** episode records at two grains; a national complication list revision mid-period; two wards
  amalgamated into one cost centre; a comorbidity score keyed on part of the episodes at a rate that moves
  with the month; three cost centres realigned to another hospital site while the register carries only the
  current alignment; wards off the clinical information system whose complications reach the warehouse only
  as the episode record's own category; fiscal quarters against the calendar year the hospital-level ask
  uses; tables inside PDFs. Every item is what these systems produce and each is asserted neutral (R2).
- **Layer 2:** `field_method`. The methodological choice that flips the call is what the excess is measured
  against: the expectation the published stratum rates give a unit's patients, or the expectation the
  network's own rates over the same period give them.
- **Decisive step:** rebuild the expectation from the rates the comparison population itself achieves,
  because the published rates are a fixed FY2023-24 standard, the network's own rates have since moved by
  different amounts in different complication groups, and the candidate units' case mixes differ
  several-fold, so a ratio against the published rates carries composition as well as practice.
- **Not semantics:** every field, code, unit and definition read correctly still leaves the easy route on
  the published excess. The extract's fields are plain, the specification files the denominator, the
  exclusions, the published rates, the reporting periods and the forward activity basis, and the charter
  files the population, the outcome, the window, the unit and the comparison. A solver who reads every one
  of them correctly, and whose observed and expected counts tie to the published series row for row, still
  ranks on the published excess and names Alderbrook General Surgery.
- **Not rule application:** no filed rule, formula or procedure builds the comparison the charter asks for.
  Specification 3.1 files the published rates and says in the same sentence that they are not re-estimated
  between specifications; nothing in the pack computes what the network's own units achieve, by stratum or
  at all, and no file carries a second rate table. Executing every stated rule gives each unit a published
  ratio and stops there.
- **Analyst test:** a strong analyst who applies charter 4.2 and 4.4, reads every field and every code
  correctly and reconciles to the published series row for row ranks the eligible units on the excess the
  indicator reports and places the team with Alderbrook General Surgery (41220).
- **Estimand:** the complications the unit's planned activity for the quarter carries above the
  complications that patients of the same risk band and age band ordinarily have, charter clause 4.3,
  with the population in clause 4.2, the activity basis in clause 4.4, the reporting period in
  specification 3.3 and the indicator's denominator and exclusions in specification 4.0 clauses 2.1 to 2.4.
- **No decoy:** nothing is planted to be caught. The published stratum rates are the real published rates
  and are correct for the indicator they define; the indicator series, the dashboard and the activity
  summary are each correct for the question they answer and reproduce from the extract to the row. No block
  of readings is copied or backfilled, no memo argues a candidate, no stakeholder figure is wrong, and the
  difficulty survives deleting every wrong number because there is none.
- **No certified replay:** the pack carries no corpus of settled decisions and no achieved-reduction
  column; the calibration form is `none`. The comparison the charter asks for is a construction the analyst
  makes from 290,000 episode records, not a figure a file reproduces.
- **Lesson:** a standardised ratio is a comparison with whatever standard produced its denominator, and
  when that standard is fixed at a vintage the comparison population has moved away from unevenly, ranking
  providers on it ranks their case mix as much as their practice. No build on file teaches it: the
  anomaly-detection drivers on file turn on when a record arrives, how an extreme was selected, a shared
  driver with a lagged response, or a detection threshold that moves.

**The WHAT screen (`stumping` 1.2).** The decisive step settles none of the five parts. Population: charter
4.2, the twelve eligible units. Outcome: specification 2.1 to 2.4, episodes recording a complication.
Window: the assessment quarter for the activity, the specification period for the rates, both filed.
Unit: complications, counted at the unit. Comparison: charter 4.3, against the complications that patients
of the same risk band and age band ordinarily have. What stays open is which
frequency answers "ordinarily have", and the data force it under `determinism-check` section 1's first
licence, the design forcing the method with the data separating the candidates. The separation is measured,
not asserted: the network's own rate runs from 0.887 to 1.313 of the published rate across the six risk
bands, a factor of 1.48 crossing 1.00 in both directions; the twelve candidates' surgical share of in-scope
episodes runs from 0.075 to 0.851 with two carrying none at all; and on the record one unit's own practice
is flat across a case-mix shift while the published basis moves its avoidable count by a factor of 8.5
(`## Literal reader`). Both candidate frequencies are measured sums over the record, neither is a fitted
form, and no free parameter is chosen, so the collinearity that spent architecture 1 cannot arise.

## Readability screen

Every rung's own step, and whether a reader could take it off a shipped sentence instead of analysing. The
decisive rung has to be silent; a readable decisive rung is a dead stump.

| Rung | The step the rung takes | What a reader would have to read it off | Verdict |
|---|---|---|---|
| 0 | Expect a unit's complications at the published stratum rates and rank the excess | specification 3.1 and Appendix A, the indicator series and the dashboard export all carry the published expectation | readable |
| 3 | Rank the excess as a rate per 1,000 rather than as a count | charter 4.3, "the most avoidable complications", "counted patient by patient and summed over the unit's episodes" | readable |
| 4 (decisive) | Measure what patients of each stratum ordinarily have from the record, and expect each unit's own patients at that | nothing. No file carries a second rate table, no clause names whose rates answer 4.3, and the words "network", "internal", "own rates", "current", "achievable" and "comparable" appear nowhere in that role in the pack | silent |

**Counter-pin sweep.** `achieve`, `attainable`, `current`, `recent` and `comparable` were swept across the
charter, the specification, the dictionary, the manifest and every CSV header. Two hits were real and both
were repaired: charter 6.2 said "The partnership does not maintain a measure of its own", which rules the
decisive step out by elimination and is now narrowed to how the partnership's own performance is reported;
and charter 4.3 said the comparison patients "would be expected to have", which collides with
specification 3.1's defined term "expected complications" and would have made the published rates
rule-mandated and the golden wrong. 4.3 now reads "ordinarily have", a claim about frequency that the
record can and does contradict. `current` survives only as "the current specification", a version pointer;
`comparable` only in 3.5, about values reported under specification 3.2. `peer_group` stays as a column of
`hospital_sites.csv` because that is what a site register carries, and the route it invites is measured and
ruled out (SF4).

## Semantic fork table

Every term in the main ask and every convention the main computation needs. The decisive step is not in
this table and must never be: a reading difference is never the stump. It is in `## Literal reader`.

| id | Term or convention | Golden reading | Alternative, and the call under it | Ruled out by |
|---|---|---|---|---|
| SF1 | "over a period" in charter 4.3, the unit's own record | every closed quarter under specification 4.0, ten quarters | the latest quarter alone (45.6), the last four (45.0), the last eight (39.5) | specification 3.3, "for the specification period to date, being every closed quarter from 1 July 2024. No other period is reported for a unit"; and `same call` on all four readings, each naming 41230 |
| SF2 | "the most avoidable complications" | a count of complications | a rate per 1,000 separations, which names 41420 at 23.0 against 41230's 17.4 | charter 4.3, "the most avoidable complications ... counted patient by patient and summed over the unit's episodes in that period"; a count, not a rate. This is rung 3 |
| SF3 | the exposure a record rate is carried on | all separations, to planned separations | in-scope episodes to planned separations (41230 at 43.0) | specification 3.4, "the separations planned for the unit multiplied by the unit's expected complications per separation", and charter 4.4; `same call` |
| SF4 | "patients of the same risk band and age band" | every such patient in the network's record | restricted to the unit's own hospital (names 41410 at 1.42x) or to the hospital's peer group (names 41420 at 1.36x) | charter 4.3 stratifies on a risk band and an age band and names no site, division or peer condition; adding one adds a stratum the clause does not state |
| SF5 | whether the unit's own patients sit inside the comparison | they do; the plain standard | leave-one-out, which gives 41230 75.6 | `same call`, measured at 2.86x; the asking sentence names the plain standard and the figure is graded on it |
| SF6 | the window the comparison frequency is measured over | the same ten closed quarters | eight (42.5), four (35.0), the latest alone (37.0) | `same call` on all four, each naming 41230 |
| SF7 | whether the comparison is stratified at all | by risk band and age band | one crude network rate, which names 41330 | charter 4.3, "patients of the same risk band and age band" |
| SF8 | "closed quarters" at the decision date | the ten quarters to 31 December 2026 | including the quarter in progress | specification 3.7, coding closes eight weeks after the quarter ends, and charter 4.1, "on the indicator data closed at the time of the decision"; the extract's pull date is 5 March 2027 and carries no 2026-27 Q3 separations, so the readings converge |
| SF9 | eligibility | charter 4.2, twelve units | counting the in-progress placement, the eight closed placements, the two amalgamated predecessors or the three non-acute units | charter 4.2's two exceptions and its four-quarter floor, specification 2.3 on service type, specification 3.6 on amalgamation |
| SF10 | a complication category code | read against the revision in force at separation | read against the 2026 revision throughout, which folds HAC13 into HAC03 | specification Appendix B, "A code is read against the revision in force at separation" |
| SF11 | the indicator's denominator | specification 2.1 to 2.4 | including same-day separations, unacceptable principal diagnoses or non-acute care types | specification 2.1, 2.2, 2.3 and 2.4, and 2.4's "An episode excluded from the denominator is excluded from the numerator" |
| SF12 | the reference rate of 96.6 | used for the adjusted rate only | applied to the avoidable count | specification 3.2 scopes it to the adjusted rate; charter 4.3 counts complications; `same call` |
| SF13 | the rounding of the graded count | one decimal, stated in the asking sentence | nearest whole complication | the asking sentence carries the unit and the rounding; every graded figure is asserted mid-bin |

## Ladder

Three rungs, each naming a different unit, every figure measured on the built record (not a target). The
decisive quantity is the avoidable count of charter 4.3 carried onto the planned separations under 3.4.

| Rung | The route | Names | Figure | Rung margin | Golden's rank |
|---|---|---|---|---|---|
| 0 | the published excess, carried onto the planned separations: the route the series, the dashboard and specification 3.1 all invite | 41220 Alderbrook General Surgery | 59.2 | 2.11x over 41320 | 4 of 12 (20.5) |
| 3 | the avoidable count rebuilt on the record's own stratum frequencies, then ranked as a rate per 1,000 rather than as a count | 41420 Marrowfield General Medicine | 23.0 per 1,000 | 1.32x over 41230's 17.4 | 2 of 12 |
| 4 (decisive) | the same rebuilt count, counted and carried onto the quarter's planned separations | **41230 Alderbrook Orthopaedics** | **40** | **1.60x over 41420's 25** | 1 of 12 |

**The golden's lead in both units, as the coordinator asked.** Over the runner-up, 41420 Marrowfield
General Medicine: **15.05 complications, 1.60x, and 2.41 standard errors** of the gap (each unit's excess
carries a Poisson standard error of sqrt(observed) scaled by planned separations over record separations:
5.17 for 41230, 3.52 for 41420, 6.25 for the gap). Over the third unit, 41410: 32.12 complications, 5.04x,
5.51 standard errors. Every candidate's own excess against its own standard error: 41230 at 7.76, 41420 at
7.11, 41410 at 2.96, and the remaining nine between -1.34 and 0.92. The top two are therefore not inside a
standard error of each other and the ladder is not drawn on noise.

**Ladder arithmetic (`dataset-generation` 6.2).** The answer is 4th on rung 0, never 1st on an intermediate
rung, and 2nd on exactly one intermediate rung by 1.32x (the rule allows one at 1.20x or more). No rung
margin is under 1.15x. The final margin is 1.60x, inside the 1.5 to 2x target. No rung is idle: rung 3 is
the closest sibling of the right answer and is the one a careful solver reaches.

**The nine other routes, measured rather than asserted.** Each was computed on the built record, so the next
reader can see what was ruled out rather than that it was ruled. Routes naming a unit other than the golden:
the published excess uncarried (41220, 434.0); the published standardised ratio (41420, 1.302); the
published adjusted rate (41420, 125.8); the raw complication count (41220, 2,444); the crude rate per 1,000
in-scope episodes (41330, 137.7); the published excess on the latest quarter alone (41210, 35.4). Routes
that also name the golden, so the call is robust to them: the rebuilt count on the latest quarter alone
(45.6, 1.33x); the rebuilt count uncarried over the window (328.7, 1.45x); the rebuilt count over the last
four quarters (45.0, 2.18x). Two of the six wrong-route margins are thin (the published ratio at 1.05x and
the latest quarter at 1.06x) and neither is claimed as a rung for that reason.

**No functional form is chosen anywhere.** The architecture-1 failure was a graded quantity that needed a
fitted counterfactual, and two forms fitted the register at a likelihood ratio of 1.02 to 1. Architecture 2
grades only sums over the record, so the enumeration above is of comparison constructions, not of forms,
and each one's result is a measured ranking rather than a fit. There is no free parameter to estimate, no
chi-square to compare and nothing whose separation could be inflated by under-dispersion.

## Closure table

The 22 axes of `determinism-check/references/forcing-the-answer.md` Part 1, each with the reading this
build takes and the move that closes it. Axes that cannot move this answer are included and marked so.

| Axis | Reading here | Closure move |
|---|---|---|
| 1 Population | the twelve units of charter 4.2, and for the graded count the unit's not-yet-observed patients in the quarter from 1 April 2027 | estimand filed literally in 4.2 and 4.4; the unobserved members are the planned separations, which ship in `activity_plan_2027q4.csv`; SF9 |
| 2 Unit of account | a complication, counted at the unit | charter 4.3 names it ("the most avoidable complications ... counted patient by patient"); C4 against the rate route at 1.33x; SF2 |
| 3 Attribution window | an episode falls in the period its separation date falls in | specification 2.5 states it; C1, the record carries no episode straddling the pull |
| 4 As-of dating | the decision date 18 March 2027, the extract pulled 5 March 2027 | both filed in the pack; the eligible set and the plan are static across the window; SF8 |
| 5 Version basis | specification 4.0 throughout; values under 3.2 are not used | specification 3.5 states the non-comparability; the extract starts at 1 July 2024 so no 3.2 period is in scope |
| 6 Denominator | in-scope episodes for the rates, all separations for the carrying | specification 2.1 to 2.4 for the first, 3.4's own words for the second; SF3, SF11 |
| 7 Weighting | the unit's own stratum counts, patient by patient | charter 4.3's "counted patient by patient and summed"; indirect standardisation, so no peer average is formed; SF4 |
| 8 Window length | ten closed quarters | specification 3.3 files it; C1 across four lengths, every one naming 41230; SF1, SF6 |
| 9 Boundary inclusivity | quarters are closed or they are not | specification 3.7's eight-week rule; C1, the pull date leaves nothing on the edge |
| 10 Rounding path | once, at the figure the asking sentence names | the asking sentence carries the unit and the rounding; asserted mid-bin in `checks.py`; SF13 |
| 11 Tie-break | none needed: the lead is 1.60x and 2.41 standard errors | measured separation, not a rule; the second level would be the unit's own ratio, which also puts 41230 above 41420's rank on the count |
| 12 Maturity and censoring | only fully closed quarters enter the record; the placement quarter is entirely unobserved and enters only as planned separations | specification 3.7 and 3.4; the forward window's contents ship as a driver file; axis 22 |
| 13 Order of operations | expect per episode, then sum, then difference, then carry | charter 4.3 fixes the order inside the count ("counted patient by patient and summed"); summing before differencing gives the same number, asserted |
| 14 Row order | the extract ships in separation order and the result is order-free | C1, asserted over permutations of the extract in `checks.py` |
| 15 Duplicate resolution | the separation key pinned in the dictionary; replayed rows collapse | the dictionary's grain sentence; the activity summary's own de-duplication is the subject of a supplemental ask, not of the call |
| 16 Identity normalisation | the patient index is issued in blocks by site, so no patient number spans two hospitals | built that way at the root rather than ruled out by a sentence; asserted zero cross-site collisions |
| 17 Netting against gross | a negative avoidable count is reported as negative and is not floored | five of the twelve candidates carry a negative count and they stay negative; nothing nets across units |
| 18 Dimensional units | complications are counts; rates are per episode; the adjusted rate is per 1,000 | specification 3.2 scopes the per-1,000 rate; SF12 |
| 19 Code and status semantics | a complication code is read against the revision in force at separation | Appendix B's sentence; never the stump; SF10 |
| 20 Integerisation | nothing is integerised: the graded count is reported to one decimal | the asking sentence; the expected count is a sum of rates and is never rounded mid-path |
| 21 Clause scope | charter Part 4 governs the placement; specification Parts 2 and 3 govern the indicator | each clause cited by number in the write-up; 6.2 narrowed so no clause scopes the decision to the published measure |
| 22 Forward window contents | the quarter from 1 April 2027 holds the planned separations and nothing else | `activity_plan_2027q4.csv` is the shipped driver file for the uncovered span, with planning notes on four units |

## Literal reader

Executed word for word, charter 4.3 asks for the complications a unit's own patients had less the
complications that patients of the same risk band and age band ordinarily have. Two frequencies in the pack
could answer "ordinarily have": Appendix A's published stratum rates, and the frequencies the record itself
carries. The published reading is ruled out by the pack's own sentences once the record is consulted.
Appendix A states that its rates are "Derived from network activity in the year ended 30 June 2024";
specification 3.1 states in the same breath that they "are not re-estimated between specifications"; and
the record shows the network's own frequency now runs from 0.887 to 1.313 of those rates across the six
risk bands. A table of what patients had three years before, never re-estimated since, is not what patients
of the same risk band and age band ordinarily have, and the record is what proves it is not.

**The demonstration that forces it, computed on closed data.** Marrowfield Orthopaedics (41410) treated the
same number of patients in every one of the ten quarters and its own practice did not change. For two of
them its orthopaedic theatre was closed, elective joint replacement stopped and its beds carried the
hospital's emergency general surgical admissions, so its major-surgical share moved from 0.000 to 0.43 and
back. On the published basis its avoidable count reads 1.1, 1.5, 1.6, 1.7, 1.8, 1.9, 1.9 and 2.1
complications in the eight ordinary quarters and **9.2 and 9.4** in the two shifted ones, a factor of
**8.5**, and its published standardised ratio moves from 1.02 to 1.04 up to 1.27 and 1.28. On the record's
own frequencies the same unit's avoidable count reads **6.2 to 7.1 in every one of the ten quarters**, a
spread of 0.90 of a complication, flat across the shift. The published basis therefore reports a unit's
avoidable burden multiplying by eight when nothing it does has changed, which is not a count of complications a unit carries as
avoidable. This is the sentence the whole call turns on, and it is a measurement rather than an assertion.

**Why this is analysis and not a reading.** Both frequencies are read correctly by both solvers: Appendix A
genuinely is a published table of stratum rates and is correct for the indicator specification 3.1 defines
with it, and the record genuinely carries observed frequencies. Nothing is misread, no code is misread, no
unit is misread. What separates the two answers is whether the analyst validates an external standard
against the population it is being applied to before ranking providers on it. A solver who does not test
the standard's currency ranks on the published excess and names 41220, whose avoidable count is actually
minus 3. That is the recognised failure of indirect standardisation against a stale external standard,
and it is the first item on the client's own Layer 2 list, the right comparison group.

**Every write-up step passes the same test.** Each step of the recommendation names the file and the clause
it rests on, and none needs an unstated inference: the denominator from 2.1 to 2.4, the eligible set from
4.2, the record window from 3.3, the stratum frequencies from the extract, the carrying from 3.4 and the
exposure from 4.4.

## Oracles

What the pack confirms, and on which path. An oracle that confirms a figure on the wrong path is legal
where the figure it confirms is genuinely correct for what it defines and is never the answer.

| Oracle | What it confirms | On which path |
|---|---|---|
| `unit_indicator_series.csv`, the published indicator series | that the solver's observed and expected counts reproduce the network's own published standardised ratio and adjusted rate on all 215 unit-quarters | **It confirms the easy route.** The published indicator blesses the easy route by construction: a solver who rebuilds the published expectation gets a row-for-row tie with the network's own system and reads that tie as confirmation that the basis is right. The figure is genuinely correct for the indicator specification 3.1 defines, and it is never the answer. It is therefore not declared a wrong-basis distractor in `metadata.json`; declaring it would make the pack say the published indicator is wrong, which it is not. |
| `quality_dashboard_2026q2.xlsx`, the quarter-position export | that the latest closed quarter's episodes, complications, expected count, standardised ratio and adjusted rate reproduce from the extract | the same easy route, one quarter deep. It carries every acute unit, not the twelve candidates, and it sorts by hospital then unit name, so it ranks nothing on the decision question |
| `activity_summary_monthly.csv` | that separations and affected episodes reconcile to the extract by unit and month on all care types | a reconciliation path, used by a supplemental ask; its de-duplication key is the device there |
| `hac_stratum_rates.csv` and Appendix A | that the two carry the same published table | a consistency check; the lookup is the published standard and carries its own vintage |
| the record's own stratum frequencies | nothing. No file carries them, no file carries a second rate table, and no document states one | the decisive path has no oracle, which is what makes it silent |

**Gate G, checked file by file.** No shipped artifact ranks the twelve candidates on the decision question.
The series is one row per unit and quarter in code and quarter order; the dashboard export sorts by hospital
then unit name and covers every acute unit including the eight the charter excludes; the plan, register,
sites, bands, strata, category list and placement files sort by code or date; the summary sorts by month and
unit; the three distractor files carry no complication measure. The only indicator-ordered sort in the
repository is in `generator/figures.py`, which writes the grading key and ships nothing. No document names a
unit code at all.

## Ask sheet

Three asks, 48 separately gradable figures, each outside the main call's row population and consuming
nothing the call's construction produces. The construction layer is the twelve avoidable counts the
decisive construction produces, which the workbook grades a row at a time.

**A2, each hospital's adjusted complication rate for the year ended 31 December 2026, with the episodes
and complications behind it.** 12 figures (4 sites x episodes, complications, adjusted rate per 1,000).
H18 home: a measure every candidate's hospital carries that the call does not turn on. Use: the quality
committee reports by site and the partnership reports to it by site. Path: `episode_outcomes_extract.csv`,
`activity_summary_monthly.csv`, `unit_register.csv`, `hospital_sites.csv`, `drg_risk_bands.csv`,
`hac_stratum_rates.csv`, 11 columns. Primary device: **none, and this is the open defect in the ask
layer.** The device it carries is the vintage of a unit's site: three cost centres were realigned to
another hospital during the period, the register carries the alignment at the export date and the activity
summary carries the site each unit reported under in each month, so the register join mis-assigns 3,918
episodes away from Alderbrook and 4,958 onto Stonecreek. The dictionary describes both columns, so a
response that reads it handles the device correctly: it is a mirror device, legitimate and worth having,
and it is what holds the mirror to 0 of 12, but it cannot be the primary. Realism: a site register carries
the current alignment and a monthly activity file carries the month's, which is what both systems are for.

**A3, the separations the sub-acute and mental health units reported each quarter, and the episodes with a
complication.** 20 figures (10 quarters x 2). H18 home: an input reconciled to another system's total, the
gap made of devices, on rows the indicator excludes entirely. Use: the committee is asked every cycle why
the partnership does not work on the sub-acute units, and the answer is the activity they carry.
Path: `episode_outcomes_extract.csv`, `activity_summary_monthly.csv`, `unit_register.csv`,
`data_dictionary.csv`, `export_manifest.csv`, 10 columns. **Primary device (D6 grain, a count that does
not sum):** a stay whose care type changes inside it is statistically discharged and readmitted the same
day, so one separation reaches the episode feed as two episode records under the same group. The patient
administration system counts the separation once, so the activity summary sits below the extract however
the extract is de-duplicated. Nothing in the pack says the extract carries more episodes than there are
separations, and the only way to see it is to reconcile the two files' counts across their two grains.
Hazard: the feed's overlapping monthly load re-sends the last three days of a month under fresh episode
identifiers, which the stated separation key collapses exactly. Stops, measured on the cut pack: every row
of the extract 10,117; de-duplicated on the separation key the dictionary states 9,143; chained into stays
**8,605, the answer**, which ties to the activity summary in all ten quarters. Lazy delta on the careful
read: **+538 separations, 6.3 per cent**, every quarter outside its bin. Realism: a statistical discharge
is how a care-type change is recorded, and no file carries a flag for it.

**A4, the in-scope episodes recording a complication by complication group, 2025-26 and 2026-27 to date.**
16 figures (8 groups x 2 years). H18 home: the trail from an input the call consumes, through rows it
never reads, to its control total. Use: the committee's standing report is by complication group.
Path: `hac_detail_extract.csv`, `episode_outcomes_extract.csv`, `hac_category_list.csv`, the specification
PDF's Appendix B, `unit_register.csv`, 9 columns. **Primary device (D5 scope, a silently partial
extract):** the complication detail reaches only the units whose wards are on the clinical information
system; for the rest, the complication is in the episode extract's own category column, one to an episode.
The detail extract is therefore below the extract's own flag for those units, and the gap is visible only
by reconciling the two across grains. Hazard: the national list was revised on 1 July 2026, the revision
renumbered HAC03 to HAC06 and folded HAC13 into HAC03, and a code is read against the revision in force at
separation. Stops, 2025-26: the detail extract on the current revision throughout 823 to 3,069 by group;
on the revision in force at separation 1,056 to 2,443; **the answer 1,082 to 2,500**, above both, because
the units the detail extract does not reach are only in the extract's own column. Realism: a clinical
information system reaches the wards it has been rolled out to, and a national list is revised.

**The main population's zero counts.** Zero device rows and zero hazard rows sit in the main call's
declared population. A3's statistical discharges are on the three non-acute units only, which
specification 2.3 puts outside the indicator, asserted at zero on every acute unit. A4's partial detail
coverage moves no observed or expected count, because the indicator reads the extract's own flag and never
the detail file, asserted. A2 reads the same episodes the call reads, so it carries no device at all: its
site attribution is a reconciliation, not a device, which is exactly why it keeps nothing back from the
cracker.

**The referee.** `unit_indicator_series.csv` is byte-clean and arbitrates every disagreement about observed
and expected complications without handing over a level: it ties to the extract on all 215 unit-quarters
under every handling of the asks' devices, because none of them touches an in-scope acute episode.

| Cracker row (the response that landed the call) | Figures | Verdict |
|---|---|---|
| A2 each hospital's episodes, complications and adjusted rate | 12 | keeps 12 of 12 |
| A3 the separations outside the indicator, by quarter | 20 | miss |
| A4 the complication groups, by year | 16 | miss |

**Pair ceiling: 39.5** (cracker 67.0, mirror 12.0, measured on the cut pack).
**Mirror leakage: 0.0** per cent of ask weight.
**Measured by:** `generator/cracker.py`, which scores the two responses from their own handling and prints
one row per response. The asks consume nothing the call's construction produces, so the two ask readings
come from the two responses' own care rather than from the call, and the script says so in its output
instead of printing a duplicate row.

**The open defect, stated rather than dressed.** A2 keeps 12 of 12 against the cracker, so Part 1.1's rule
that every cracker row misses is not met. The two gated figures are the worst honest measurements and both
pass, and the ladder and the construction layer are what carry the pair. A2 needs a silent primary of a
family A3 and A4 do not use, and until it has one this sheet says so.

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

- **Architecture 1 is spent: the fitted-counterfactual family is closed for this slot.** Its decisive
  quantity was the fall a scarce intervention causes, read off a closed register of past interventions. The
  judge sent it back NOT_DETERMINISTIC on `competing_defensible_answer` with margin fragility, and the
  reason is structural rather than a shortage of data. A power on the standardised ratio, where observed
  equals expected times the ratio raised to g, fits the register at chi-square 3.34 on seven degrees of
  freedom against 3.30 for a share of standing excess: **a likelihood ratio of 1.02 to 1**, and it gives 19
  against 21 for the recommended unit with a gap of 7 rather than 8. Near a standardised ratio of 1 the two
  forms agree to first order and they diverge only at high ratios, so separating them would need placements
  at ratios of three or four, which no hospital unit carries. The register's own assessment quarters were
  also **under-dispersed at 0.47 per degree of freedom against 1.65 for the rest of the record**, about
  three and a half times too clean, so every likelihood ratio the build reported was inflated and fixing
  the dispersion makes the separation worse rather than better. Three of the eight pooling routes also
  moved ten of twelve counts once enumerated properly (the mean excluding one placement 0.765, the
  geometric mean 0.480, the mean with the baseline lagged a quarter 0.537). Both forms named the same unit,
  so the call was robust and only the graded counts were not. **The rule this slot now carries: a graded
  quantity is either measured from the record or it is not graded.** A fitted quantity needs a forced
  functional form, a functional form can only be forced by the data when the plausible domain separates the
  candidates, and that has to be checked at the draw by listing the forms a competent analyst would try and
  asking whether any two agree to first order over the domain the world allows.
- **Rejected at the draw: making the window of a unit's position the decisive step.** It is the obvious
  replacement once the fitted fall is gone, and it is dead on the `stumping` 1.2 screen: the window is one
  of the estimand's five parts, so filing it makes the computation follow from the clause and leaving it
  unfiled makes the call indeterminate. The latest-quarter trap stays in the build as a rung, ruled out by
  charter 4.3, and is not the decisive step.
- **Rejected at the draw: judging each unit's excess against its own sampling error.** Measured and in the
  domain, but the ways of accounting for the error (a Poisson limit, a shrunk estimate, an
  over-dispersion-adjusted funnel) are again a family of forms with a free parameter, which is the disease
  that spent architecture 1 in another dress.

- **This pass, the design point measured rather than targeted.** Four rounds on the built record. The
  separation opened by deepening the published table's staleness in the orthopaedic bands and raising the
  golden's own standing together, holding their product fixed so its published excess stayed at fourth:
  the golden's lead went from 7.33 complications, 1.45x and 1.19 standard errors to 15.05, 1.60x and 2.41.
- **Rejected: scaling the golden unit up to buy standard errors.** A unit's excess against its own Poisson
  error improves with the square root of its record volume, so the cheapest way to clear two standard
  errors was to make Alderbrook Orthopaedics a 2,500-separation-a-quarter unit. Ten thousand orthopaedic
  separations a year is not a real unit at a principal referral hospital. The separation was bought from the
  drift and the standing instead, which cost nothing in realism because both are already in the story.
- **Rejected: a charter clause filing the mix-insensitivity criterion.** The clean way to satisfy
  `determinism-check` section 1 was a clause saying a unit is not placed with because the patients it
  treated changed, so that a measure which moves on a mix shift violates a quotable sentence. It was drafted
  and dropped: with only two rate sets in the pack, a clause ruling one out selects the other by
  elimination, which is the HOW filed in a fairness voice. The forcing sits on the data instead, where the
  record carries it by a factor of 8.5.
- **Rejected: the first backfill story.** The case-mix shift that forces the rate set was built by moving
  the demonstration unit into SURG-MAJ, which in this DRG set is major bowel resection and coronary bypass.
  Two hundred and thirty of those a quarter inside an orthopaedics cost centre is not a hospital. Replaced
  by the orthopaedic theatre closing for ventilation works, elective joint replacement stopping and the
  ward carrying the hospital's emergency general surgical admissions, which is SURG-MIN, keeps the unit's
  volume flat as the mechanism requires, needs no second unit to change because the elective work was
  deferred rather than transferred, and still moves the published avoidable count by a factor of 8.5.
- **Rejected: claiming the published-ratio route and the latest-quarter route as ladder rungs.** Both are
  routes a solver takes, and both were measured, but their own first-to-second margins are 1.04x and 1.12x,
  under the 1.15x floor. A rung whose own winner is ambiguous is not a rung. They are recorded under the
  ladder as measured routes, and the ladder claims three rungs whose margins are 2.11x, 1.32x and 1.60x.

- **This pass, the ask layer measured rather than described.** The sheet was written from a script run on
  the cut pack, as the skill requires, and the first measurement came back at a pair ceiling of 50.0 with
  the cracker keeping 32 of the 48 ask figures. Building A3's statistical-discharge primary took A3 from
  20 of 20 to 0 of 20 and the ceiling to 40.4; giving the renal and Carrowdean medical units a case mix
  the published table's drift reaches took the mirror's construction leakage from 2 of 12 to 0 and the
  ceiling to **39.5**, with mirror leakage at **0.0**. Both gated figures are the worst honest
  measurement, as `supplemental-stumping` Part 7 requires.
- **Rejected, and it is structural: a silent primary for A2 as the ask is worded.** A2 is each hospital's
  adjusted complication rate over in-scope acute episodes, and those are exactly the episodes the call's
  comparison frequency is computed over. Four devices were drafted and all four die on the separation
  line. A cross-source duplication on a candidate's episodes sits in the main population. The same
  duplication on an embedded unit still shifts the network's own stratum frequencies, so it moves the
  call, which is the gravest finding in the book. A partial extract for one site makes the site's expected
  count unrecoverable, which law 6 forbids. A site attribution the summary cannot resolve makes the truth
  unrecoverable the same way. The conclusion is not that A2 needs a cleverer device but that **an ask
  computed over the call's own population cannot carry one**, and the fix is a redraw: take A2 to a
  quantity over all care types, where the same-day, ungroupable and non-acute episodes of the acute units
  are rows the call never reads and a device can live. Held rather than rushed, with the ask sheet saying
  A2 keeps 12 of 12 so the defect is visible instead of dressed.
- **Rejected: softening the cracker assertion so `checks.py` would pass.** The gate that fails is Part
  1.1's, every cracker row misses, and A2 does not. The assertion stays strict and the build's own checks
  fail on it, which is the state of the ask layer; the two gated figures carry the measurement rather than
  the favourable of two numbers.
- **The chain rule had to be made exact before it could carry A3.** Recovering a stay from the feed by
  chaining an episode onto one that ended the same day first over-counted by three (another episode of the
  same patient sorted between the two segments, so the chain broke) and then under-counted by one (a
  genuine same-day readmission under the same group looked like a split stay). Matching segment ends
  rather than adjacency fixed the first; regrouping the one episode in the record that was readmitted
  under its own group fixed the second. The rule now reproduces the activity summary's separations exactly
  in all ten quarters, which is law 6, and that is what makes the device fair rather than merely hard.
- **This pass, two consistency defects in the fiction's own history, found by reading the register against
  the charter it is governed by.** The register placed the team with Alderbrook Aged Care twice, in
  2023-24 Q4 and again in 2026-27 Q1, and nine closed quarters apart is inside charter 4.2's twelve, so the
  partnership's own record breached its own rule. No unit in the register can legally be reused, because
  twelve closed quarters after the earliest row is the quarter being decided, so the earliest cycle was
  moved to a unit that appears nowhere else: the Stonecreek sub-acute unit, placed with under charter
  version 2.0 before clause 2.3 put sub-acute units outside the indicator and before 4.2 limited
  eligibility to acute units. It adds texture rather than losing it, because the register now carries a
  cycle the current rules would not allow, and it cannot move the eligible twelve because a non-acute unit
  is excluded by service type anyway. The second defect: the register's in-progress cycle is IP-10, and the
  deliverables called the cycle being decided IP-10 as well. The placement for the quarter from 1 April
  2027 is IP-11.
- **The theatre closure leaves a trace a hospital would actually have, checked rather than assumed.** The
  case mix shows it loudly: elective joint replacements at 41410 run about 300 a quarter and fall to 63 and
  60 in the two closed quarters. Bed-days do not show it, because length of stay is drawn per unit rather
  than per procedure, so the unit's mean stay holds at 6.8 and 7.2 nights across the closure against 6.7
  to 7.3 elsewhere. The operational trace is therefore in the rostering file, whose coverage was widened
  from four quarters to six so it reaches both closed quarters: nursing hours per patient day at 41410 run
  4.49 to 4.66 in the ordinary months and **5.13 to 5.30 in exactly the six months of the closure**, with
  the agency share up by nearly half, because unplanned general surgical admissions need more nursing per
  patient day than an elective list and the roster had been built for the list that stopped. The file is a
  declared distractor and no graded figure reads it, so the trace corroborates the argument without
  entering the computation. **Open realism item for the next pass:** length of stay should follow the
  episode's risk band, not only the unit's mix, which would put the closure in bed-days too and would fix
  a joint replacement and an appendicectomy currently averaging the same stay. It was held because the
  stay feeds the complication selection, so changing it moves the realised stratum frequencies and would
  need the design point and the hospital-rate centring re-measured.
