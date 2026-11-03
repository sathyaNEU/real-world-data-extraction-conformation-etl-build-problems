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
- **Not semantics:** regulation 4.3 has every result carry the reporting limit the method achieved for the
sample, and the method schedule says a result below the limit is reported with the qualifier shown in the
export and gives each method's limit, so the reading is free. A solver who reads every field correctly still has to decide what those results
contribute to an average, and every constant substitution files a different count: 7 at half the limit,
3 at zero, 11 at the limit itself, 8 with them dropped.
- **Not rule application:** clause 7.2 files what is averaged (the compliance samples the programme requires
for the water body in the reporting year, each weighted equally) and clause 7.3 the standard it is
compared with. No shipped sentence says what a result reported below a limit contributes, and the
regulations, the method schedule and the programme name no value for it. Executing
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

## Survivor anatomy

- **Actor:** the deciding property is each water body's annual mean over its compliance samples with every result below a limit valued from what the record supports; no column stores it, and the qualifier and limit columns are ordinary metadata that every rung of the ladder reads alike.
- **Link:** the signal is read across the two laboratories, the sensitive method's quantified results in the same water bodies and months showing what lies under the legacy method's 0.10 ug/l, a comparison no key joins and no sentence asks for.
- **Reflex:** the field's own regulatory convention for a mean over results below the limit of quantification, half the limit (the convention the EU's QA/QC directive for water monitoring sets), sits at rung 0 and files 7, the `Ends on:` figure.
- **Back-test:** the one internal check the pack offers passes the easy route: Kilcrohane, the only water body measured wholly by the sensitive method, is non-compliant under half the limit too, and the quarterly reports and the programme tie under every handling.
- **Second use:** every file the decisive step reads sits in the pack for its own reason: the export for every figure, the method schedule for the methods and limits regulation 4.3 has recorded, the regulations for the standard and the population.
- **Shock:** weak on this build and frozen with the call: measured on the cut pack, the golden four are also the top four of the zero and half-limit rankings, so the step moves where the line falls rather than the order; the call is the count, which those two rungs put at 3 and 7.
- **Pins:** clause 7.2 files the population, the weighting and the comparison and no sentence names an estimator, but its third sentence (a sample's own concentration at the figure the results it holds support) is the one sentence whose deletion unforces the call, 8 of 13 verdicts open without it (`## Tried and rejected`), so this line holds only in part.

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
| SF2 | compliance sample | a field sample the programme requires at a listed point | any row in the export, QC included | 7 | clause 7.2 "the compliance samples the authority's monitoring programme requires", and regulation 4.2, which names the blanks, duplicates and spikes |
| SF3 | reporting year | 1 April 2025 to 31 March 2026 | calendar 2025 | 5 | clause 1.4 "the reporting year begins on 1 April" |
| SF4 | which sample date | the date of collection | the date of receipt or of analysis | 4 | `same call`, asserted: every sample is collected and received inside one reporting year, the nearest clear of the boundary by 9 days |
| SF5 | result version | the approved version | the provisional version, or both | 4 and 4 | clause 7.5 "the result as approved by the laboratory"; asserted that no approved value differs from its provisional value for MCPA |
| SF6 | weighting | each sample weighted equally | per point, then averaged over points | 5 | clause 7.2 "each sample weighted equally", quoted against the per-point reading; the separation is asserted |
| SF7 | units | ug/L after converting the ng/L rows | the numbers as reported | 11 | the `units` column and the method schedule's note that TAS-LC-PHX-04 reports in ng/l |
| SF8 | the `<` qualifier | the determinand was not detected at the limit in `reporting_limit_ug_l` | the value is the limit | 11 | regulation 4.3 (every result carries the reporting limit the method achieved for the sample) and the method schedule's note that a result below the limit is reported with the qualifier |
| SF9 | standard | 0.05 ug/L, Schedule 2, as an annual average | the 0.10 ug/l drinking water parametric value in the method schedule's scope note | 1 | clause 7.3 "the standard for the substance set out in Schedule 2" |
| SF10 | non-compliant | the average exceeds the standard | the average equals or exceeds it | 4 | `same call`, asserted: no estimate lands within 11 per cent of the standard |
| SF11 | rounding | the count is a whole number of water bodies; no estimate is rounded before the comparison | each average rounded to two decimals first | 4 | `same call`, asserted at two and three decimals |
| SF12 | the district | the thirteen water bodies the programme lists for the authority | the register's full list, which includes three outside the programme | 4 | clause 7.2 "requires for the water body", and the programme's own list |
| SF13 | the average | the mean of the thirteen water bodies' own samples, one concentration per sample | the mean of a lognormal fitted to the censored sample, which is a property of the fit rather than of the samples | 4 | `same call`, asserted: the fitted distribution's own mean gives the same four verdicts with every water body 12 per cent or more clear of the standard; clause 7.2 also says the average is "the mean of the concentrations of the compliance samples ... one concentration for each of those samples" and that the authority "shall not report in place of the average any property of a distribution fitted to them" |

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
| 16 Identity normalisation | laboratory client point codes against authority codes | `monitoring_point_crosswalk.csv`, every MCPA code matched, asserted 1 to 1 on the compliance network |
| 17 Netting against gross | none; concentrations do not offset | no closure needed, asserted that no result is negative |
| 18 Dimensional units | ng/L and ug/L in one column | the `units` column, SF7; asserted that every averaged value is in ug/L |
| 19 Code and status semantics | the qualifier, sample type and status codes | regulations 4.2, 4.3 and 7.5 and the method schedule, SF2, SF5, SF8; never the decisive step |
| 20 Integerisation | the count of water bodies | a whole number by construction |
| 21 Clause scope | per substance, per water body, per year | clause 7.2's own scope, SF9 |
| 22 Forward window contents | none; the reporting year closed on 31 March 2026 | the call is retrospective: the figure is committed at the regulator's deadline of 30 November 2026 and the window it describes is closed. The reason is the decision itself, which is what the authority states in a statutory return, and no forward quantity enters it. |

## Literal reader

Executing the prompt, clause 7.2, clause 7.3, clause 7.5, clause 1.4 and the method schedule word for
word selects 427 MCPA compliance results at 37 sample points in 13 water bodies and
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
- Kilcrohane, the one water body wholly on the sensitive method, reads 0.0606 to 0.0612 ug/L under all
  six pipelines and is non-compliant in every one. It is the data's own consequence of an accredited
  limit twelve times below the standard, it is not quoted anywhere, and it blesses no method: it is
  non-compliant under rung 0 too.
- No control, published figure or corpus ties only under the golden. There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary devices | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| W the return's ortho-phosphate figures | per water body, the compliance samples the year holds an approved ortho-phosphate result for, and how many of those results were below the reporting limit (26 cells; the chart's 13 bars carry the same cells) | a measure every candidate carries that the call does not turn on: the same return's ortho-phosphate row for each water body (regulation 7.6, Schedule 3), on rows the MCPA call never reads | the return states each listed substance's compliance samples and below-limit results for every water body, and ortho-phosphate is the listed substance the nutrient suite carries at every compliance point | three, each a reconstruction, one referee deciding them (a compliance point's nutrient bottle is filled on the visit that takes its pesticide sample, so it carries that sample's collection date and time): (D7) a bottle the reception booked to a compliance point's open slot and booked again later under the operational point that took it, the first booking's withdrawal never reaching the authority, 13 bottles, one into every water body, each into the slot that point's own lost bottle left open and each dated on a day that point was not visited; (D1) a bottle booked twice by one reception, from the round's pre-registration one to three days early and from the chain of custody form, one analysis issued to both, 22 at the compliance points of 11 water bodies and 3 at operational points; (D7) the Tirneevin code, catchment and last two digits, that operational points ARW-2122 and ARW-2241 share with compliance points ARW-0322 and ARW-1041, neither operational point having a crosswalk row of its own | QC sample types (4.2); October to December provisional and late-approved results (7.5); ARW-1043 in the programme only from October and ARW-0853 only to September (4.1); five missed visits; 14 bottles lost on the way, which nothing in the programme shows; every Tirneevin result below its 0.10 mg/l limit | export (13 columns), crosswalk (4), programme (points and dates, the operational network), register (2), regulations 1.4, 4.1, 4.2, 7.5 and 7.6; 5 files, 21 columns | 6 stops: the lazy read (every ortho-phosphate row at the programme's points, QC and versions included) 498 and 259 against the golden 413 and 187; the cracker 472 and 246; the plan reader and the one-a-month reader, each over by every lost bottle; a reader of any one reconstruction, 0 of 26; the golden | two contracted laboratories' receptions and a client numbering that drops the hundreds digit produce exactly these records, and nothing in the pack narrates them |

**Pin test.** The asking sentence pins the substance, the unit (the compliance samples with an approved
result), the year and the grain (the water body); regulations 4.1, 4.2 and 7.5 file the programme's
points and dates, what a compliance sample is and the approved result. No filed sentence names a
booking, a bottle's identity, a visit or a code's owner, and each device sits in one of those three dimensions:
which bookings are one bottle, which point a bottle belongs to, which point a shared code's bottle came
from. Filing the WHAT a judge would force (compliance samples, approved results, the programme's dates)
leaves all three in place.

**Forcing, asserted on the cut pack.** One identity decides every device, asserted in `checks.py`: a
compliance point's own nutrient bottle carries the collection date and time of the point's pesticide
sample that month (the visit), at all 37 points and 427 visits. Of the 472 nutrient bookings under a
compliance point's code, 413 fall on one of that point's visits, at most one to a visit, and the other
59 are exactly the device bookings, none of which falls on a visit: the 22 second bookings, each dated
one to three days before a visit of its point and repeating that visit's bottle result for result; the
13 misbooked bottles, each dated on a day its compliance point was not visited, that point's visit of the
month leaving no booked bottle, each with an identical and newer twin under the operational point that
took it; the 12 ARW-2122 bottles under ARWA-BN-22 (each month exactly one of that code's two bottles falls
on ARW-0322's visit) and the 12 ARW-2241 bottles under ARWA-CB-41, none on the day of an ARW-1041 visit,
while all 11 of ARW-1041's Kilgarron bottles fall on its visits. The golden read from the shipped files
equals the generator's truth, and `verify.py` rebuilds it twice without the generator, once from the
visits and once from the bottles alone (the double bookings merged by their shared receipt and results,
each twin kept at its newer booking, the shared codes split), the two agreeing cell for cell.

**Main population separation.** Zero device rows in the main call's population (MCPA, field samples,
approved versions, the 13 programmed water bodies' 37 points, 1 April 2025 to 31 March 2026): every
device row is a nutrient-suite field row, none in October to December. `checks.py` asserts it by count
from the shipped rows and asserts the call's own files and rows against the shipped commit: the
regulations, the register and the crosswalk byte for byte, the 1,898 pesticide-suite rows byte for
byte, and the programme's points, names, water bodies, laboratories, pesticide rounds, dates and notes
cell for cell. The only cells that moved in the programme are the nutrient and physico-chemical round
counts of ARW-1043 and ARW-0853, from 12 and 24 to 6 and 12, so the required rounds match the dates the
programme already gave.

**No marker.** No column, code, status or flag separates a device row: the misbooked bottles keep
their first booking's number and status, and the re-bookings and second bookings are numbered from the
end of Tirneevin's series together with 80 ordinary bottles whose chain of custody forms reached
reception late, so no number range isolates them either (asserted: device bookings are under half of that
block). Their times, batches and receipts follow the same patterns as every other nutrient bottle.

**Hazard table.** The QC rows and the October to December versions move the lazy read at every water
body (498 rows against the cracker's 472); the programme dates of ARW-1043 and ARW-0853 move Carrowbeg
and Tirneevin Stream for a reader without regulation 4.1; the lost bottles and the missed visits move
the plan reader at every water body; the double bookings, the misbooked bottles and the shared codes
move the cracker at every water body, by 3 to 13 samples.

**Referee.** One, and it hands over no level: the monthly visit, read from the export's own pesticide
rows (their collection date and time), which the call reads unchanged and byte for byte as shipped. It
decides which booking is a compliance sample in each device; the visits number 427 and the figures are
the visits with a booked bottle, a count nothing states. The two quarterly reports, declared
distractors, list October to December only, where no device sits, and tie under every handling.

**Cracker sheet.** The cracker landed the call at rung 5, ran the hygiene battery (exact duplicates,
natural-key duplicates on point, determinand, collection date and time, unmatched joins, the governing
version) and executed regulations 1.4, 4.1, 4.2 and 7.5. Measured on target.zip f2c0b70568a20c9a.

| Water body | Cracker's samples, below limit | Golden | Result |
|---|---|---|---|
| Aghavannagh | 25, 13 | 22, 10 | miss |
| Ballynure | 59, 35 | 46, 22 | miss |
| Carrowbeg | 41, 24 | 28, 11 | miss |
| Cloonfad | 38, 14 | 35, 11 | miss |
| Derryvore | 37, 13 | 34, 10 | miss |
| Drominagh | 38, 26 | 35, 23 | miss |
| Glasheen | 38, 14 | 35, 11 | miss |
| Kilcrohane | 26, 14 | 23, 11 | miss |
| Knockanure | 37, 25 | 34, 22 | miss |
| Lisheenaguile | 26, 14 | 23, 11 | miss |
| Moneycashen | 26, 14 | 23, 11 | miss |
| Owenbeg | 49, 26 | 46, 23 | miss |
| Tirneevin Stream | 32, 14 | 29, 11 | miss |

Stress readings, measured on the same pack:

| Reading | Cells kept of 26 | Score on the call |
|---|---|---|
| the plan reader: required nutrient rounds less the rounds the programme records as not sampled | 0 | 45.0 |
| one bottle a month at every point | 0 | 45.0 |
| double bookings merged, nothing else | 0 | 45.0 |
| re-bookings resolved, nothing else | 0 | 45.0 |
| shared codes split, nothing else | 0 | 45.0 |
| double bookings and re-bookings | 22 | 91.5 |
| re-bookings and shared codes | 4 | 53.5 |
| re-bookings resolved, then one bottle a month | 24 | 95.8 |
| all three reconstructions from the bottles alone | 26 | 100.0 |
| the visit reader: each compliance point's bookings on its pesticide visits (the golden) | 26 | 100.0 |

Pair ceiling: 28.5
Mirror leakage: 0.0 per cent of the ask weight
Measured by: generator/ceiling.py, run on the cut pack (target.zip f2c0b70568a20c9a)

**The weak side, priced.** The mirror files rung 0 on the call and handles the ask exactly as the cracker
does, since the ask reads no row the call's construction produces, so both keep 0 of 26 and the pair is
28.5 on paper. A response that joins each compliance point's nutrient bookings to its pesticide visits
keeps all 26: the referee is the layer's single point of failure, and the layer holds only while no top
response matches nutrient bottles to pesticide visits, a cross-suite join no battery sweep makes. A
response that finds the re-bookings, a cross-point comparison of whole bottles, and then caps every point
at one bottle a month keeps 24 of 26 (Carrowbeg's shared code alone holds it) and scores 95.8 on the call;
one that also merges the double bookings but not the shared codes keeps 22.

**Leak sweeps answered.** `leak.py --asof 2026-11-16` returns REVIEW on four lines, each harmless, and no
LEAK. Sweep 4 flags the regulations (11 of the stump paragraph's terms), the method schedule (7) and the
two quarterly reports (3 each) for ordinary words of the field (sample, method, authority, programme,
standard, average, laboratory, export, qualifier): they are the domain's own nouns, no document names the
decisive step, and the word sweep in `checks.py` asserts over every shipped file that none says
substitute, censor, non-detect, Kaplan or maximum likelihood.

**Scope, proved.** `freeze.py check task189 --mode rubric` FAILs on two keys and nothing else:
`a2_nitrate.Gortaleen Borehole.at_or_above_trigger` (25) and `a2_nitrate.Rathvilly Borehole 2.at_or_above_trigger`
(3). Both were figures of the retired nitrate ask, classed main-call only because their values equal a
Critical Components number (Derryvore's 25 bounded results) and a Final Recommendation number (3 under
zero substitution) by coincidence; neither number moved in either block. With those two keys named by
`--allow` the check PASSes: blocks 1 and 2, every other main-call figure (the call, the rungs, the
construction counts), the stump, the card's stump and driver, the ladder, the default path and the call
sentence are unchanged.

## Pre-ship check

- **The 10/10 rules re-read against the built pack.** The decisive step is still the estimate of a
  left-censored mean with two reporting limits in play, and `checks.py` executes it: the easy route on
  the generator's clean truth files 7 and the same clean truth assessed on the limits as reported files
  4. The mess in the pack is Layer 1 only: the QC rows, the provisional versions, the ng/l rows, the
  crosswalk, the renumbering and the incomplete rounds are all typed or filed, and removing every one of
  them leaves the call exactly as hard, because the decisive step is in the 427 compliance samples
  themselves. The reship moved no MCPA row: the 1,898 pesticide-suite rows, the regulations, the
  register and the crosswalk are the shipped commit's byte for byte.
- **Rule 3, each class.** Nothing is planted (every quantified MCPA value is its own draw, asserted
  distinct; no block is copied; no memo, draft or stakeholder figure ships). Not semantics (regulation
  4.3 and the method schedule say what the qualifier and the reporting limit carry, so the reading is
  free, and a word sweep over every shipped file asserts that none of them says substitute, censor,
  non-detect, Kaplan or maximum likelihood). Not rule application (clause 7.2 files the population, the
  unit, the window and the weighting, clause 7.3 the standard, clause 7.5 the governing version; the
  limits of that line are in `## Survivor anatomy`, Pins). The ask turns on which bookings are one
  bottle and which point a bottle belongs to, decided by the visit each bottle was filled on, which rule
  3 leaves free for an ask.
- **Input gates.** 12 files, 4 formats (csv, xlsx, json, pdf), the export at 25,316 rows, five
  distractors declared in `metadata.json` (the flow record, the sales returns, the two quarterly
  reports, the abstraction register) and named in neither a file name nor the prompt.
- **Gate G.** No shipped artifact assesses or ranks the water bodies: the regulations give the standard
  and the method, the programme gives the points and the rounds, the quarterly reports list
  ortho-phosphate results and say in their own words that they are not a compliance assessment, and
  the word `non-compliant` appears only in the regulations' own clauses. The ortho-phosphate chart
  carries no MCPA assessment. There is no declared wrong-basis distractor.
- **Free gates on the final cut (target.zip f2c0b70568a20c9a).** Generator assertions 3,898 and
  independent checks 78, green; two builds byte-identical (`target/`, `golden/`, `metadata.json`,
  `figures.json`, `target.zip`); `figures_check.py` 34 of 34; `precut.py` 61 checks, 0 FAIL;
  `voice-check.py` PASS at 617 characters; `leak.py` REVIEW with every line answered above;
  `guard.py heart` WARN only and `surface` with five promoted pairs answered on the card (task143,
  task155, task181, task192, task462); `freeze.py --mode rubric` as above; `ceiling.py` 0 of 26 for the cracker and the
  mirror, pair 28.5.
- **Heart WARNs answered.** `government_agency` overuse: the body that files a river basin district's
  statutory return is a public authority. The decision type repeating task151 is the frozen call's. The
  deliverable pair svg and xlsx repeating task150 is the shell: the return is the regulator's workbook
  form and its chart the companion the prompt names, and the voice gate's quotas pass. The repeated
  first name George was replaced from the seeded draw (Polly Caddow, Tirneevin's contact).
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
- **(2026-10-25, measured) A blind reader landed the call and took 86.4 per cent of the ask figures.** One isolated Sonnet reader at medium effort, holding only a fresh unzip of `target.zip`, `prompt.txt` and the flat `figures.json` key list, filed **4 non-compliant water bodies** against the golden 4 and named Owenbeg, Cloonfad, Glasheen and Kilcrohane in its prose, so the call is landed on the members as well as the count, and **51 of 59 ask figures hit**. It reached the call by substituting each legacy-limit non-detect with that water body's same-month sensitive-limit mean, which is the decisive step this architecture rests on, and it reported all five rung counts (3, 7, 11, 8, 4) unprompted, so the ladder is visible from the pack. Both halves of Gate F fail at once: with the call landed the pair floors at 45 plus 55 times the ask keep, so no ask repair reaches it. Re-root, do not harden.
- Reship of 10-31 without the dictionary and the manifest (the nitrate factor moved into the method schedule, the chart an SVG, figures unchanged): held on the ask layer. A1, each water body's compliance samples and below-limit counts (26 figures), is the call's own construction, so a careful cracker (QC samples out, approved results, the programme's points) keeps all 26 and so does the mirror; the sheet's cracker had taken a lazier read. Pair about 74 against the 70 bar; the asks need devices outside the call's construction and the hygiene battery before a reship.

- (11-01, rubric reship) A1, each water body's MCPA compliance samples and below-limit counts, retired as an ask: it was the call's own construction over the call's own population, so a careful cracker and the default-path mirror both kept all 26 cells (pair about 74). Its counts stay in `figures.json` only as the construction behind Critical Components 1 and 4, and the chart that drew them is gone with it.
- (11-01, rubric reship) A2, the abstraction points' nitrate, retired: under H18 the drinking water source protection report is another decision with another owner, and its two devices were a conversion factor the method schedule files and copies on the same collection timestamp, both executed by the battery.
- (11-01, rubric reship) A3, the October to December reconciliation, retired: the reports' printed counts, the governing-version filter and an identifier-level comparison hand all three figures to the careful cracker, and the device that would bite there, a result re-booked under a new number, reads as two results to a literal grader, which is a fork rather than a device.
- (11-01, rubric reship) The return's ortho-phosphate figures on the nutrient suite as it shipped, before any device: each determinand of a bottle carried its own collection day and receipt, and a water body's samples equalled the programme's required rounds less the missed visits, so the programme alone recovered every cell (the blind-response test). A bottle now carries one date, time and receipt across its determinands, its total oxidised nitrogen is its nitrate plus nitrite, the method schedule lists every nutrient determinand each method carries, and the bottles lost on the way, which nothing in the programme shows, take the plan reader off every cell.
- (11-01, rubric reship) The double booking alone as the ask's device: a reader that keeps one bottle per point and month removes every double booking without identifying one, and so would a reader of the shared Ballynure code. The misbooked bottles were placed in the slots their target points' own lost bottles left open, the causal order a reception follows, and that reader now misses every cell; it still keeps 25 of 26 once it has also resolved the re-bookings (the ask sheet prices it).
- (11-01, rubric reship, judge pass 2) The ortho-phosphate counts resting on conventions no file states: a bottle under two points counted at its newer booking, status V excluded with no code list in the pack (the quarterly reports print those rows approved), and the Tirneevin ARWA-CB-41 bottles given to an operational point the crosswalk does not name. The judge found each a competing reading, the newer-booking rule even contradicted by the programme's twelve rounds at the misbooked point, whose own bottle was the lost one. Replaced by one identity the data carry: a compliance point's nutrient bottle is filled on the visit that takes its pesticide sample and carries that sample's collection date and time, which decides all three devices; the withdrawn status dropped from the reissued batches; the operational points sharing a code kept off the compliance point's visit day.
- (11-01, rubric reship, judge pass 3) The visit identity as the ortho-phosphate devices' referee (a compliance point's nutrient bottle carries its pesticide sample's collection date and time): the judge reproduced the golden only under that rule and ruled it an unfiled convention, the literal count of every approved field booking at a programme point (472 and 246 across the network) being the reading the files support. Second determinism failure of this ask layer: filing the visit as WHAT hands the reconstruction to the cracker (157's closure arithmetic), and removing the devices hands it the cells, so the layer is spent and the next pass re-sites the ask onto a new device family whose truth a judge can force from one filed WHAT that the cracker cannot execute without the reconstruction.

- (11-03, rubric reship, ask design) The nutrient verdicts as the ask, so that a device moving values could bite (the return's ortho-phosphate and ammonium compliant column and Schedule 3's count of non-compliant water bodies): every one of the 13 water bodies holds Tirneevin nutrient results censored at 0.10 mg/l, above both standards (13 to 35 a water body), and the count of non-compliant water bodies runs 0, 13, 13 and 13 for ortho-phosphate and 0, 0, 13 and 0 for ammonium with the results below the limit at zero, at half the limit, at the limit and dropped (screened on target.zip f2c0b70568a20c9a). Any nutrient verdict or average is the call's own decisive step on another substance, a figure the mirror and the cracker part on by the call's rung (coupled, `supplemental-stumping` 1.2 ban 4). Decoupling it needs a sensitive Tirneevin nutrient method in the method schedule the call reads, and with every result quantified no value device survived either: a blank correction, a rounding or a method change leaves the reported result the result, and a reporting basis is executed by the battery once a file states it.
- (11-03) A date-basis device on the ortho-phosphate counts (`task129`'s family: after a system change a source dates each bottle by its receipt or its approval, the collection date left in another field): every compliance nutrient bottle is collected on days 4 to 13 of its month, no receipt date leaves its month and an approval date moves 1 bottle out of the year and none across a programme date (ARW-1043 from 1 October, ARW-0853 to 30 September), so the device has no mass on a year's count by water body.
- (11-03) A label at the wrong vintage on the point a bottle belongs to (`task257`'s and `task463`'s family: a laboratory's client codes reissued on 1 October 2025 and a later site list naming every row by its current holder): the call's crosswalk carries every client code the frozen pesticide rows use, so a reissue either moves those rows or sits on the nine Kilgarron codes only nutrient bottles carry. With 16 of Kilgarron's 19 nutrient points holding 12 bookings, a permutation of its codes moves no water body's count at most of them and 6 at the most, and a reissue onto operational points is the shared-code identity judge pass 3 ruled unfiled.
- (11-03) A reporting basis switched at a date and shown by the suite's own chemistry (`task460`'s family, an exact referee telling which rows sit on which basis): the one exact referee the nutrient suite carries is total oxidised nitrogen against nitrate (TON less nitrate as N runs 0.006 to 0.056 mg/l at both laboratories, the nitrite, and every Tirneevin NO3 row sits above its TON as reported), and nitrate is not a Schedule 2 substance, so the ask would be another decision (H18). Ortho-phosphate as P against PO4 has no exact referee here: total phosphorus would bound only the rows switched to PO4, leaving a schedule that states PO4 for every row unrefuted on the other side.
- (11-03) A quality-control device (a laboratory system change typing its QC bottles as field samples, each known by chloride below its limit or a spike's constant offset): it is a counting convention on which bookings are compliance samples, which this reship rules out after the visit identity, and the literal reader keeps every row the export types FIELD unless a laboratory record names the QC sample, at which point the battery reconciles it.
- (11-03) Conclusion of the ask design: no honest ask layer survives in this world while the call is frozen. The return's second measure per water body is its nutrient rows; their counts admit only identity and counting devices (spent, judge passes 2 and 3), their verdicts and averages are the call's estimator, and the four families that held this batch need, respectively, mass at a period edge, a code space the call does not share, an exact referee on a listed substance and an ask-only grouping, none of which the pack has. Measured on target.zip f2c0b70568a20c9a by read-only screens of the shipped export, crosswalk, register and programme (each nutrient result at its governing approved version, joined as the call joins); no file in the pack, the generator or the goldens moved, and the next step is the author's, in `pipeline.json`'s resume line.
