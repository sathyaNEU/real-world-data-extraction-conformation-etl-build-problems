# task189 design note

Araglen Regional Water Authority, MCPA compliance in the 2025/26 reporting year: how many of the
district's water bodies the annual return states as non-compliant.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task189.json`, filed and committed with this note |
| Domain, task type | Physical & Environmental Sciences, `environmental-monitoring-exceedance` |
| Objective | Anomaly Detection & Diagnostics (an apparent exceedance separated from a measurement artifact) |
| Shape | 10, scorecard: each water body's check against the standard |
| Decision | a count committed to the National Water Quality Office in the return due 30 November 2026 |
| Gate G | `signal_vs_noise_or_hold`; decisive generator G17 statistical rigor, then G2, G12. The determinism judge read Gate G as `statistical_rigor` on its third pass and `method_or_model_selection` on its second; both fit, and G16 was given up on 2026-10-16 when task148 v2 shipped the same day carrying it. |
| Strategy | `other`: the mean of a left-censored sample whose reporting limits differ by laboratory |
| Layer 2 | `estimation_fit`, own pattern `left-censored-results-with-several-reporting-limits` |
| As-of date | 16 November 2026 (the authority's extract date; the return is due 30 November 2026) |
| Stakeholder | the officer who runs the authority's monitoring programme (`programme_officer`; `field_unit_lead` was given up to task148 v2 on the same ground) |
| Guard | WARN only. `overuse.org_family` government_agency in 28 builds: the unit that files a river basin district's statutory return is a public authority and no other org family is honest here. `test.same_puzzle_older` and `test.same_driver_older` differentiated against task70 and task260 in the card. |

**Data-native sentence.** MCPA is sprayed on rush-infested pasture in a six-week window, so in this
district's record the herbicide is quantified in a handful of spring and summer samples and is below
the laboratory's reporting limit in most of the rest, and because the authority's own framework
laboratory reports to 0.01 ug/L while the catchment partnership's laboratory reports to 0.05 ug/L,
over half the standard, the share of a water body's year that is known only as a bound depends on
which laboratory holds its sample points.

**Sources read.** `analytical_tasks/02_anomaly_detection/AD12_regulator-return-attack-campaign-unit.md`
(seed): the decision shape only, one count committed to a regulator at a date where monitoring fires
at a finer unit than the return counts; its own architecture, a method pinned by reproducing two
published returns, is a certified replay and is not used. `guard.py mechanisms --objective
anomaly-detection`: 21 spent drivers, none on censored measurement; the nearest, task180, turns on
events never recorded at all because the detection threshold moves with a daily noise cycle, where
here every result is present and carries its own upper bound. `references/client/two-layer-task-design.md`:
Layer 2 family `estimation_fit`, censoring and truncation.

## Default path

1. Read `lims_results_export_2025_2026.csv`, keep `determinand_code = MCPA`.
2. Keep `sample_type = FIELD` (drop the blanks, field duplicates, laboratory duplicates and spikes,
   all named in the data dictionary) and keep the approved version of every result, dropping the
   provisional rows the approved ones supersede.
3. Convert the results reported in ng/L to ug/L using the `units` column.
4. Join each `lab_client_point_code` to the authority's `sample_point_code` through
   `sample_point_crosswalk.csv`, then to its water body through `monitoring_programme_2025_26.xlsx`,
   taking the water body code in force in the reporting year from `water_body_register.csv`.
5. Keep the samples whose sample date falls in the reporting year, 1 April 2025 to 31 March 2026.
6. For each result carrying the `<` qualifier, substitute half the value in `reporting_limit_ug_l`.
7. Average the results per water body and compare each average with the 0.08 ug/L annual average
   standard in `surface_water_quality_regulations_2019.pdf`, clause 7.2.
8. Count the water bodies whose average exceeds the standard and write that count into the return.

**Ends on:** 7 non-compliant water bodies (Ballynure, Cloonfad, Derryvore, Glasheen, Kilcrohane,
Owenbeg and Tirneevin Stream).
**Golden:** 4 non-compliant water bodies (Cloonfad, Glasheen, Kilcrohane and Owenbeg).

## Stump sentence

The default path substitutes half the reporting limit for every result reported below it, the
default in practice, and files **7 non-compliant water bodies**; three of those seven
(Ballynure, Derryvore and Tirneevin Stream) are over the standard only because most of their
samples went to the laboratory whose reporting limit is 0.05 ug/L, so half of it, 0.025 ug/L, is
written into their year where the authority's own laboratory shows the concentration at those
points to be nearer 0.004 ug/L.

## Three rules

- **Task type:** `environmental-monitoring-exceedance`, the task type in Physical & Environmental Sciences
that serves Anomaly Detection: a monitoring record assessed against a standard, where the question is
whether an apparent exceedance is the water or the measurement.
- **Domain test:** the deciding quantity is each water body's annual average concentration of MCPA
estimated from a sample in which most results carry only an upper bound, the problem environmental
statistics treats with a censored-data estimator (a maximum likelihood fit on the censored sample,
Kaplan-Meier on the flipped sample, or a fill from the sensitive method's own quantified values at the
same limit) and never with a substituted constant.
- **Swap:** "how many schools does the return state as non-compliant with the standard for recorded
absences" reads as a filter over counted events: there is no limit of quantification beneath which an
absence is merely known to be below a bound, so no result is censored, the estimator disappears and the
whole call becomes an average and a comparison.
- **Layer 1:** the authority's own systems produce all of it. The laboratory export carries a qualifier and
an achieved reporting limit per result (the two methods accredited to 0.005 and 0.10 ug/l, the second twice the standard), results in
ng/L from one method and ug/L from the other, provisional versions superseded by approved ones, QC rows
(field and equipment blanks, field and laboratory duplicates, matrix spikes) beside the field samples,
the laboratory's own client point codes against the authority's sample point codes, water body codes
renumbered in the 2024 revision of the register, the quarterly reports as tables inside PDFs with
multi-row headers, and the monitoring programme as a wide workbook. None of it is placed to be caught
and none of it carries the decisive step.
- **Layer 2:** `estimation_fit`, censoring. The methodological choice is what a result reported below a
reporting limit contributes to a mean when the limits in the sample differ, and the limits differ
because two laboratories with different methods serve one network.
- **Decisive step:** estimating each water body's annual mean from the censored sample using every
observation's own reporting limit, rather than substituting one value for every result below a limit.
- **Not semantics:** the data dictionary states plainly that a `<` qualifier means the determinand was not
detected at the value in `reporting_limit_ug_l`, and the method schedule gives each method's limit, so
the reading is free. A solver who reads every field correctly still has to decide what those results
contribute to an average, and every constant substitution files a different count: 7 at half the limit,
3 at zero, 11 at the limit itself, 8 with them dropped.
- **Not rule application:** clause 7.2 files what is averaged (the compliance samples the programme requires
for the water body in the reporting year, each weighted equally) and clause 7.3 the standard it is
compared with. No shipped sentence says what a result reported below a limit contributes, and the
regulations, the method schedule, the programme and the data dictionary are silent on it. Executing
every stated rule leaves the decisive step untouched.
- **Analyst test:** a strong analyst conforms the export, drops the QC and superseded rows, crosswalks the
points, substitutes half the reporting limit for every non-detect, averages and files 7 non-compliant
water bodies (the `Ends on:` figure) where 4 are.
- **Estimand:** clause 7.2 of `surface_water_quality_regulations_2019.pdf`: "A water body is non-compliant
for a Schedule 2 substance in a reporting year where the average concentration of the substance in the
water body in that year exceeds the standard for the substance. The average is taken over the
compliance samples the authority's monitoring programme requires for the water body in the reporting
year, each sample weighted equally." Population, unit, window, weighting and comparison are literal;
the estimator is not named anywhere.
- **No decoy:** nothing is planted to be caught. No previous return, no draft assessment, no memo, no
stakeholder figure and no ranked list of water bodies ships; no block is copied or backfilled; the one
water body whose points are all on the sensitive method (Kilcrohane) reads the same under every
handling, which is the honest control the data produces rather than a tie built to bless a method.
- **No certified replay:** the seed's architecture (the method for a return must reproduce the counts in
the two previously published returns) is not used and no published return is in the pack, so no method
can be recovered by reproducing a certified figure. The method is forced by the data: the sensitive
method's quantified results at the same points in the same months show what lies below 0.10 ug/L, and
four censored-sample estimators agree on all thirteen verdicts.
- **Lesson:** a result reported below a reporting limit is an observation with an upper bound, not a value
and not a gap, and when the bounds in a sample differ, any constant put in their place ranks the units
by which method measured them. No build on file teaches it: the 21 anomaly-detection drivers include a
detection threshold that moves with a daily noise cycle (task180), where the events are never recorded
at all, and a density from grouped tests (task188), where every group is observed; none has an
observation that is present and bounded.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 substitute half the reporting limit | no clause names a substitution | the qualifier and limit columns invite one | yes, the practice default | no corpus scores it | the battery counts non-detects, not their worth | one pass over the rows | readable |
| 1 treat the non-detects as absent (zero) | no | same columns | yes | no | no | one pass | readable |
| 2 assess on the authority's own compliance points only | clause 7.2 says the programme's required samples, which include the partnership points, so this violates a quotable sentence | the lab code column | yes, a quality reflex | no | no | one filter | readable |
| 3 substitute the limit itself | no | same columns | yes, the precautionary reflex | no | no | one pass | readable |
| 4 drop the non-detects and average the quantified results | no | same columns | yes | no | the battery's missing-value sweep suggests it | one filter | readable |
| 5 estimate the mean from the censored sample, every observation at its own limit **(decisive)** | no sentence names an estimator or points at one | no column isolates it; the limit column is ordinary metadata both halves of the ladder read | no reflex reaches it; every reflex above is a constant | no control or corpus scores the estimators; Kilcrohane ties under all of them because its method is sensitive | the battery finds the non-detects and leaves their worth open | no subtraction, ratio or half of a reported figure gives it | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | water body | the register's water body in force in the reporting year | the 2024 pre-revision code | 4, the same bodies under either code | `same call`, asserted: the revision renamed codes and merged none |
| SF2 | compliance sample | a field sample the programme requires at a listed point | any row in the export, QC included | 7 | clause 7.2 "the compliance samples the authority's monitoring programme requires", and the dictionary's sample type codes |
| SF3 | reporting year | 1 April 2025 to 31 March 2026 | calendar 2025 | 5 | clause 1.4 "the reporting year begins on 1 April" |
| SF4 | which sample date | the date of collection | the date of receipt or of analysis | 4 | `same call`, asserted: every sample is collected and received inside one reporting year, the nearest clear of the boundary by 9 days |
| SF5 | result version | the approved version | the provisional version, or both | 4 and 4 | clause 7.5 "the result as approved by the laboratory"; asserted that no approved value differs from its provisional value for MCPA |
| SF6 | weighting | each sample weighted equally | per point, then averaged over points | 5 | clause 7.2 "each sample weighted equally", quoted against the per-point reading; the separation is asserted |
| SF7 | units | ug/L after converting the ng/L rows | the numbers as reported | 11 | the `units` column and the dictionary's statement that both are in use |
| SF8 | the `<` qualifier | the determinand was not detected at the limit in `reporting_limit_ug_l` | the value is the limit | 11 | the dictionary: "a result qualified `<` was not detected; the figure in reporting_limit_ug_l is the limit the method achieved for that sample" |
| SF9 | standard | 0.05 ug/L, Schedule 2, as an annual average | the 0.10 ug/l drinking water parametric value in the method schedule's scope note | 1 | clause 7.3 "the standard for the substance set out in Schedule 2" |
| SF10 | non-compliant | the average exceeds the standard | the average equals or exceeds it | 4 | `same call`, asserted: no estimate lands within 11 per cent of the standard |
| SF11 | rounding | the count is a whole number of water bodies; no estimate is rounded before the comparison | each average rounded to two decimals first | 4 | `same call`, asserted at two and three decimals |
| SF12 | the district | the thirteen water bodies the programme lists for the authority | the register's full list, which includes three outside the programme | 4 | clause 7.2 "requires for the water body", and the programme's own list |
| SF13 | the average | the mean of the thirteen water bodies' own samples, one concentration per sample | the mean of a lognormal fitted to the censored sample, which is a property of the fit rather than of the samples | 4 | `same call`, asserted: the fitted distribution's own mean gives the same four verdicts with every water body 12 per cent or more clear of the standard; clause 7.2 also says the average is "the mean of the concentrations of the compliance samples ... one concentration for each of those samples" and that the authority "shall not report in place of the average any property of a distribution fitted to them" |
| SF14 | nitrate basis | a result under `NO3N` is nitrogen and converts to the nitrate ion by 4.4268 | the two codes pooled as reported | the asks' figures change at five of the six abstraction points | the field dictionary: "a result under NO3N is 4.4268 times smaller than the same water under NO3" |

## Ladder

| Rung | The analysis | Count | Water bodies named |
|---|---|---|---|
| 0 | substitute half the reporting limit for every non-detect | **7** | Ballynure, Cloonfad, Derryvore, Glasheen, Kilcrohane, Owenbeg, Tirneevin Stream |
| 1 | treat the non-detects as absent, averaging over all samples | 3 | Cloonfad, Glasheen, Kilcrohane |
| 2 | assess on the authority's own compliance points only | 3 | Cloonfad, Glasheen, Kilcrohane |
| 3 | substitute the reporting limit itself | 11 | all but Carrowbeg and Lisheenaguile |
| 4 | drop the non-detects and average the quantified results | 8 | the seven of rung 0 plus Knockanure |
| 5 | **answer:** estimate each water body's mean from its censored sample, every observation at its own limit | **4** | Cloonfad, Glasheen, Kilcrohane, Owenbeg |

**Worth on the graded quantity.** Rung 0 to the answer moves the count by 3 and the named set by 3
water bodies; rung 1 and rung 2 by 1; rung 3 by 7; rung 4 by 4. No rung is reachable by a correction
that walks the same way: substituting less (zero) under-states and substituting more (the limit)
over-states, so the answer is bracketed, not extreme, and no monotone correction reaches it.

**Separation.** Five readings that keep a bounded result bounded agree on all thirteen verdicts,
computed in `checks.py` and again in `verify.py`: a lognormal fit with each observation at its own
censoring point and each bounded sample at its conditional expectation, Kaplan-Meier on the flipped
sample, a fill from the sensitive method's quantified results of the same month below the same limit,
the fitted lognormal's own distribution mean, and the clean truth the generator holds. Every verdict
is at least 12 per cent clear of the standard under all of them, asserted. The count stays 4 for any
standard between the widest compliant estimate and the narrowest non-compliant one, and Schedule 2's
0.05 sits mid-corridor.

**Dominance.** Owenbeg is the water body the ladder turns on: it is non-compliant (0.056 to 0.062
ug/L across the four estimators) and falls out of rungs 1 and 2, while Ballynure, Derryvore and
Tirneevin Stream are compliant (0.032 to 0.048) and enter rung 0. All four are heavy on the
partnership's points; Kilcrohane, which is all on the sensitive method, sits in every rung.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | which results are averaged | clause 7.2 files the compliance samples the programme requires; SF2, SF12; C1 asserted on row and point counts |
| 2 Unit of account | result, sample, point or water body | clause 7.2 averages samples and assesses the water body; SF6 |
| 3 Attribution window | which reporting year a sample falls in | the date of collection, SF4; every sample is 9 or more days clear of the boundary, asserted |
| 4 As-of dating | the state of the register and the programme | the authority's extract of 16 November 2026; the register revision of 2024 is the one in force, SF1 |
| 5 Version basis | provisional or approved | clause 7.5 and SF5; asserted that no MCPA approved value differs from its provisional value |
| 6 Denominator | the number of samples in the average | the count of compliance samples, clause 7.2; asserted per water body |
| 7 Weighting | per sample or per point | clause 7.2 "each sample weighted equally", SF6; the per-point average gives the same verdicts, asserted |
| 8 Window length | one reporting year | clause 1.4, SF3 |
| 9 Boundary inclusivity | exceeds, or equals and exceeds | SF10; no estimate within 11 per cent of the standard, asserted |
| 10 Rounding path | before or after the comparison | SF11; the comparison is on the unrounded estimate and the count is identical at two and three decimals, asserted |
| 11 Tie-break | two water bodies at the same estimate | none: the thirteen estimates are distinct to three decimals, asserted |
| 12 Maturity and censoring | results below a reporting limit | the decisive step; the estimand is filed and the estimator is forced by the data, not by a sentence |
| 13 Order of operations | convert units, then exclude, then average | every order gives the same figures, asserted over the three permutations that are defined |
| 14 Row order | the export's order | C1, asserted over three permutations of the export |
| 15 Duplicate resolution | the same sample under two client codes | the crosswalk resolves them; the main call's population holds no duplicate pair, asserted by count |
| 16 Identity normalisation | laboratory client point codes against authority codes | `sample_point_crosswalk.csv`, every code matched, asserted 1 to 1 on the compliance network |
| 17 Netting against gross | none; concentrations do not offset | no closure needed, asserted that no result is negative |
| 18 Dimensional units | ng/L and ug/L in one column | the `units` column, SF7; asserted that every averaged value is in ug/L |
| 19 Code and status semantics | the qualifier, sample type and status codes | the data dictionary, SF8; never the decisive step |
| 20 Integerisation | the count of water bodies | a whole number by construction |
| 21 Clause scope | per substance, per water body, per year | clause 7.2's own scope, SF9 |
| 22 Forward window contents | none; the reporting year closed on 31 March 2026 | the call is retrospective: the figure is committed at the regulator's deadline of 30 November 2026 and the window it describes is closed. The reason is the decision itself, which is what the authority states in a statutory return, and no forward quantity enters it. |

## Literal reader

Executing the prompt, clause 7.2, clause 7.3, clause 7.5, clause 1.4, the method schedule and the data
dictionary word for word selects 427 MCPA compliance results at 37 sample points in 13 water bodies and
asks for the mean of each water body's samples' concentrations against 0.05 ug/l, one concentration per
sample. The text is silent on what a sample the laboratory reported no value for contributes, so every
option was computed: zero 3, half the limit 7, the limit 11, dropped 8, and each of the five readings
that keep the sample bounded 4. The easy ones are easy methods on the same literal estimand, not other
readings of it, and the one reading that is a different quantity, the mean of a distribution fitted to
the sample, both converges on the golden and is excluded by clause 7.2's own words. Every other term and convention has an SF row that is
either ruled out by a quoted sentence or asserted to give the same call.

## Oracles

- The labs' quarterly report PDFs confirm result counts per quarter and the values as issued; they tie
  under every handling of the non-detects, because they carry no average and no assessment.
- The programme workbook confirms each point's required frequency; it ties under every handling.
- `export_manifest.csv` confirms the export's row count and date range; it ties under every handling.
- Kilcrohane, the one water body wholly on the sensitive method, reads 0.0606 to 0.0612 ug/L under all
  six pipelines and is non-compliant in every one. It is the data's own consequence of an accredited
  limit twelve times below the standard, it is not quoted anywhere, and it blesses no method: it is
  non-compliant under rung 0 too.
- No control, published figure or corpus ties only under the golden. There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 the year's sampling record | per water body, the compliance samples the year holds and how many came back below the reporting limit (26 figures) | the audit trail of the call's own population | the return's own columns; the regulator asks every authority for them | none (construction layer) | QC sample types, provisional superseded by approved, the ng/L rows, the 2024 point renumbering, a re-issued batch | export, programme, crosswalk, register, dictionary; 11 columns | 5 stops; the lazy read (every MCPA row at the programme's points, QC and all) gives 475 against 427 | the return form asks for the sample count behind every assessment |
| A2 nitrate at the abstraction points | per abstraction point, the highest nitrate result of the year as mg/L NO3 to one decimal and the number of samples at or above 37.5 mg/L NO3 (12 figures) | an input the call consumes (the same export) read on rows the call never touches | the authority's drinking water source protection report | D1, the same samples submitted under two client codes, the water services section's and the laboratory's own, so a plain count double-counts; resolved only by the crosswalk and the collection timestamp | the two determinand codes, nitrate as NO3 and as N; a point renamed mid-year | export, crosswalk, abstraction register, dictionary, method schedule; 9 columns | 4 stops; the lazy read double-counts 40 rounds and files the as-N figures at five of the six points | abstraction points are monitored for nitrate under a separate programme |
| A3 the quarter's reconciliation | for October to December 2025, the ortho-phosphate results the quarterly reports show for the district, the number the export holds, and the number in only one of the two (3 figures) | an input reconciled to another system's total | the authority's data quality log, which the regulator audits | D2 version, the reports were issued on a cut-off before some results were approved, so the export holds replacements the reports do not | a report page with a continued multi-row header; one report issued twice | two report PDFs, export, manifest; 7 columns | 4 stops; the lazy read compares the two totals, 250 against 242, and files 8 rather than 18 | the quarterly report is the laboratory's contractual deliverable |

**Main population separation.** Zero device rows in the main call's population (MCPA, field samples,
approved versions, the 13 programmed water bodies' 37 points, 1 April 2025 to 31 March 2026): the A2
double submissions are nitrate at the six abstraction points, which are not in the compliance network;
the A3 superseded versions are ortho-phosphate. Asserted by count in `checks.py`. The main path still
carries its own texture (QC rows, provisional versions, ng/L, the crosswalk), all of it coded and found
by the hygiene battery.

**Hazard table.** 475 MCPA rows sit at the programme's points and 427 of them are compliance samples. QC sample types move A1 and A2; the ng/L rows move A1 and A2; the 2024 renumbering
moves A1 and A3; the multi-row report header moves A3.

**Referee.** `export_manifest.csv` arbitrates the export's own extent (row count, date range, the
determinands it covers) and nothing else; it ties under every handling and settles no level.

**Cracker sheet.** The cracker landed the call at rung 5, ran the hygiene battery, executed clauses
1.4, 7.2, 7.3 and 7.5 and matched the quarterly reports.

| Ask figure | Cracker's figure | Golden | Result |
|---|---|---|---|
| A1 compliance samples, Ballynure | counts every MCPA row at the water body's points, 53 against 47 | 47 | miss |
| A1 below-limit count, Owenbeg | counts every `<` row including the field duplicates and blanks | 31 | miss |
| A2 highest nitrate, Gortaleen Borehole | takes the maximum as reported, without the nitrate-ion basis, 14.9 | 65.9 | miss |
| A2 rounds at or above 37.5, Sheskin Shallow Well | reads the as-N results as the nitrate ion, so no round reaches the level and it files 0 | 19 | miss |
| A3 identifiers in only one of the two | subtracts the two totals and files 8 | 18 | miss |

Pair ceiling: 34.0
Mirror leakage: 20.0 per cent of the ask weight

**Leak sweeps answered.** `leak.py` returns REVIEW on six lines, each harmless. Sweep 4 flags the
regulations, the method schedule, the dictionary and the two quarterly reports for sharing three to
eight ordinary words with the stump paragraph (sample, method, average, authority, standard,
programme, laboratory): those are the domain's own nouns and no document names the decisive step, which
the word sweep in `checks.py` asserts over every shipped file. Sweep 3 flags 0.005 and 0.10 in the
method schedule: they are the two accredited reporting limits, an input the pack must carry, and both
are listed under `stated_inputs` in `metadata.json`.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** The decisive step is still the estimate of a
  left-censored mean with two reporting limits in play, and `checks.py` executes it: the easy route on
  the generator's clean truth files 7 and the same clean truth assessed on the limits as reported files
  4. The mess in the pack is Layer 1 only: the QC rows, the provisional versions, the ng/l rows, the
  crosswalk, the renumbering and the incomplete rounds are all typed or documented, and removing every
  one of them leaves the call exactly as hard, because the decisive step is in the 427 compliance
  samples themselves.
- **Rule 3, each class.** Nothing is planted (every quantified MCPA value is its own draw, asserted
  distinct; no block is copied; no memo, draft or stakeholder figure ships). Not semantics (the
  dictionary states what the `<` qualifier and `reporting_limit` mean, so the reading is free, and a
  word sweep over every shipped file asserts that none of them says substitute, censor, non-detect,
  Kaplan or maximum likelihood). Not rule application (clause 7.2 files the population, the unit, the
  window and the weighting, clause 7.3 the standard, clause 7.5 the governing version, and no shipped
  sentence says what a result below a limit contributes).
- **Input gates.** 14 files, 4 formats (csv, xlsx, json, pdf), the export at 25,524 rows, two
  distractors declared in `metadata.json` and named in neither a file name nor the prompt.
- **Gate G.** No shipped artifact assesses or ranks the water bodies: the regulations give the standard
  and the method, the programme gives the points and the rounds, the quarterly reports list
  ortho-phosphate results and say in their own words that they are not a compliance assessment, and
  the word `non-compliant` appears only in the regulations' own clauses. There is no declared
  wrong-basis distractor and the difficulty survives deleting every number in the pack that is not a
  laboratory result.
- **Free gates.** `precut.py` 49 checks 0 FAIL 0 WARN; `voice-check.py` PASS at 908 characters;
  generator assertions 209; independent checks 68; two byte-identical rebuilds of `target/` and
  `golden/`; `figures_check.py` 42 of 42; `leak.py` REVIEW with every line answered above;
  `guard.py surface` clean and `heart` WARN only (`government_agency` overuse).
- **Retrospective call.** The reporting year closed on 31 March 2026 and the figure is committed to the
  regulator at the 30 November 2026 deadline, which is the decision the authority actually makes; no
  forward quantity enters it (closure axis 22).

## Tried and rejected

- Shrinkage of each water body's mean before the threshold comparison (the small-sample selection
  reading): `guard.py nearest` measured the driver at 0.12 against task253 v3, which already builds
  "how many units have a latent level below a fixed line, seen only through averages of small and
  unequal samples". Dropped at the draw.
- A flow-weighted against time-weighted annual mean as the decisive step: the weighting is a reading
  of "annual average" and would be a semantic fork on the main call, so clause 7.2 files the
  arithmetic mean of the compliance results and the uneven sampling interval becomes ask-layer mess.
- The seed's own architecture (the return's method must reproduce the two previously published
  returns): a certified replay, banned by the 10/10 rules and by `guard.py` as a validated decoy; no
  previous return ships in the pack at all.
- The non-detect row carrying a copy of its reporting limit in the `result` field: the stage 4 reader
  showed that a literal "average of results" could then take 0.1000 as a measured value and reach 11,
  which is a reading rather than a method. The row now carries an empty `result` and the limit only in
  `reporting_limit`, with the dictionary saying so; every graded figure is unchanged.
- The method schedule's scope note explaining that the legacy limit was set for the drinking water
  parametric value: the reader called it "unusually explanatory" and said it pointed at the mismatch
  with the standard. The note now gives the accredited limit, the units and the method's age, and
  leaves the comparison to the analyst.

- Clause 7.2's third sentence cut in full, the data left to force the valuation of a sample the
  laboratory reported no value for: on the generator's clean truth the record then leaves 8 of the 13
  verdicts open, because the interval between valuing every censored row at zero and valuing it at its
  own limit straddles the 0.05 standard (Owenbeg, the ladder's own discriminator, runs 0.0488 to
  0.1067), and the count spans 3 at zero, 4 at every bound-respecting estimator, 7 at half the limit, 8
  with the non-detects dropped and 11 at the limit. The sentence was carrying the determinism of 8
  verdicts, so deleting it fails Gate C rather than moving the elimination into the data.
- An inter-laboratory split-sample set (the same bottle analysed by both laboratories) as the
  data-native eliminator: it measures the sub-limit concentrations directly, so it refutes half the
  limit by arithmetic, and a set that refutes the naive read is a control bench (readability test 4,
  `stumping` Part 7). It makes the decisive rung readable, which is a worse break than the clause.
- Censoring demoted to Layer 1 (every achieved limit well below the standard, so every valuation
  converges) with the ladder re-rooted on a new Layer 2 in the same world: at a coarse limit of 0.02 the
  record settles all 13 verdicts and every analytical reflex lands the golden (per point 4, per month 4,
  Kaplan-Meier 4, the conditional fill 4), while the only routes still missing are ones a filed sentence
  forbids (the non-detects dropped 8, the authority's own points 3, a fitted distribution's own mean 5,
  the median 0, the pulse months trimmed 0). Once the valuation is harmless this world has no analytical
  residue left, because the regulation files the population, the unit, the weighting and the comparison.
- The judgment beyond the method (the censored fit conditioned on the point or the month, so the
  textbook pooled estimator becomes the named wrong answer): 0 of 30 cells over the coarse limit from
  0.10 to 0.01 and the within-water-body contrast from 0.5x to 3x have the conventions harmless and the
  pooled fit wrong. The pooled lognormal, Kaplan-Meier and the conditional fill all land the golden set
  in all 30 cells, so conditioning the fit has no lever at any contrast.
- Grading only the verdicts the record settles: 5 of the 13 are settled at the shipped limit and 3 of
  those are non-compliant, and both the zero route and the authority's-own-points route file 3, so the
  easy route lands the call.
- A C2 criterion in general terms in place of the third sentence: zero, half the limit, the limit itself
  and dropping the sample are exactly the members of the family whose output is a function of the sample
  count, the detected values' sum and the limits alone, so any criterion that excludes them says in
  general terms "value each unmeasured sample from the results the record holds", which is the decisive
  step stated at authority. There is no weaker wording that reaches them.
- Architecture 1 abandoned at stage 1 rather than stage 2, on an identity rather than a margin: a water
  body's verdict is wrong under some valuation convention if and only if the record does not settle that
  verdict (195 of 195 cells over 13 water bodies and 15 settings of the coarse limit, 0 cells either way
  off the diagonal), and the dial crosses between a coarse limit of 0.080 (7 verdicts open, the easy
  route filing 6) and 0.075 (6 open, the easy route filing the golden 4), with no cell in between. The
  bound that makes the valuation matter is the bound that makes every valuation defensible, so the
  stump's lever and the determinism hole are the same cells and no clause-free wording separates them.
