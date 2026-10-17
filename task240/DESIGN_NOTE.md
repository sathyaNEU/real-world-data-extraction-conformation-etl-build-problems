# task240 design note

Architecture 1, wave 3, seed DQ13 (whether this wave's estimate trips the weighting pipeline's quality alert): the
seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Survey Research &
Official Statistics, nonresponse, calibration and measurement-error adjustment, Data Quality Monitoring & Alerting.
Larchmere Social Research runs the Household Resources Survey for a Canadian province's statistics branch under
contract: each wave interviews every adult in a stratified, clustered sample of addresses, the weighting post-stratifies
the responding adults to the Branch's population estimates by health region, age group and sex, and the tables give
four estimates for each of twelve health regions (adults receiving a public pension, in privately rented homes,
providing unpaid care, and in households behind on a household bill). The Branch's quality standard QS-7 puts a
low-reliability warning on every published estimate whose coefficient of variation reaches 20 per cent, and the
agency's quality report, delivered with the tables, sets out which estimates carry it.

## Draw

Card `cards/task240.json` (architecture 1, registered 2026-10-17). Guard verdict WARN, each answered here:
repeat.gate_g and overuse.gate_g (method_or_model_selection against task468 and task190, a record-linkage and an
audit-sampling build: the shared key is the generic method family, the mechanisms share nothing); repeat.question_form
(which, against task468: the decision is a designation of estimates, so the form follows it). The decisive generator
is G17, not G16: G16 is task190's decisive pattern inside the ban window, and the call itself is G17's question
(whether each estimate survives its own sampling error), with the variance estimator (G16) the step inside it.

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, serving
  Data Quality Monitoring & Alerting. Not banned against the last three builds (task468, task190, task194). The object
  is the health of the survey's published output (whether each estimate is precise enough to stand without a warning),
  the call a monitoring decision in the quality report.
- **Niche.** The variance of a calibrated (post-stratified) estimator: the weights are ratio-adjusted within region,
  age group and sex cells to known totals, so a published total's sampling error is that of the residuals within the
  cells over the clusters, not of the raw values with the weights held fixed.
- **The call.** Which of the 48 published estimates (twelve regions by four indicators) carry the low-reliability
  warning in the 2027 quality report.
- **Shape.** 07, grid of cells: each region-indicator cell's coefficient of variation and warning. Decision
  designation_set, answer set_of_items, question form which.
- **Strategy.** decomposition_attribution (each published total split into the part the population totals fix and
  the residual within the cells, whose spread alone is sampling error), G17 decisive (each estimate judged against its
  own sampling error), G16 (the variance estimator the estimate as published entitles), G2 (the cluster as the unit of
  the variance, a lower rung); Gate G method_or_model_selection; calibration none; context artifact filed_standard (the
  Branch's statistical quality standard); layer 2 family estimation_fit, pattern
  own:post-stratified-estimate-variance-from-within-cell-residuals.
- **Forum, event, organisation.** customer_or_counterparty (the Branch's survey statistics lead receives the quality
  report), purchase_order_or_contract (the wave's tables and quality report are the contract's deliverable),
  professional_services. All clear the last three builds.
- **People** (`guard.py names --geo Canada --seed 240`, locale en_CA): Kristina Stephens, the agency's lead survey
  statistician, who wrote the weighting note and signs the quality report; Latasha Evans, the Branch's survey
  statistics lead, who owns QS-7 and receives the report; Anna Mckee, the agency's fieldwork manager, who wrote the
  fieldwork close-out.
- **Deliverables.** `hrs27_quality_report.xlsx` (every estimate with its coefficient of variation and warning, each
  region's response rate and calls, a chart of the coefficients against the line) and `hrs27_quality_note.docx` (the
  note the Branch publishes beside the tables, naming the warned estimates).
- **As-of.** Friday 3 December 2027: fieldwork ran from 7 April to 26 September 2027, the outcome extract was taken on
  30 September, the call records exported on 18 October, the weights frozen on 12 November, and the tables and quality
  report are due to the Branch on 10 December.
- **Data-native sentence.** Every responding adult's weight was scaled within region, age group and sex until the
  weights add to the population; an estimate that age largely decides (who receives a public pension) is therefore
  almost fixed by those totals, and its sampling error is only the scatter of adults around their cell's rate, which
  the weights' own spread hides: in the four northern regions, with 62 to 127 responding adults over 7 to 13 PSUs, the
  fixed-weight error counts that spread as sampling error and puts the pension and renting estimates over the line.

Sources, one line each (what it teaches; how this build differs):
- Särndal, Swensson and Wretman, and Deville and Särndal on calibration estimators: the variance of a calibrated total
  is that of the residuals from the calibration variables; here the calibration is post-stratification and the step is
  never named in the pack.
- Statistics agencies' quality flags (a letter or a warning by coefficient of variation band): the convention QS-7
  follows; the line and the warning are filed, the variance estimator's treatment of the weighting is not.
- The client's survey patterns (variance reflecting strata and PSUs; domain estimates keeping the full design): the
  lower rungs; neither is this build's step.

## Default path

1. Read QS-7 (a published estimate whose coefficient of variation is 20.0 per cent or more carries the warning; the
   standard error by Taylor linearisation over the strata and PSUs, with replacement) and the weighting note (final
   weights post-stratified by region, age group and sex).
2. Build the responding adults: members aged 16 and over joined to their final weights on household and person number
   and to their household's region, stratum, PSU and household answers; code each estimate from its question (yes
   counts; don't know and refused do not; proxy answers count).
3. Estimate each region's total of each indicator with the final weights.
4. Take each total's standard error by Taylor linearisation over the strata and PSUs with the final weights treated as
   fixed: each adult's weighted value totalled by PSU, the with-replacement variance within each stratum (or a survey
   package given the weights, strata and PSUs).
5. Divide by the estimate and warn every estimate at or over the line.

Ends on: 15 of the 48 estimates warned, the public pension estimates of all four northern regions and the private
renting estimates of R01 and R03 among them.

Golden: 9 of the 48 warned (unpaid care and household-bill arrears in R01 to R04, private renting in R02), from each
total's variance as the post-stratified estimator's (each adult's departure from the weighted rate of their region,
age group and sex cell, totalled by PSU and linearised over the strata); the pension estimates of the northern regions
sit at 5.0 to 8.4 per cent.

## Stump sentence

A competent analyst takes each published total's standard error by Taylor linearisation over the strata and PSUs with
the final weights treated as fixed and files 15 of the 48 estimates warned, the public pension estimates of all four
northern regions and the private renting estimates of R01 and R03 among them; the step that lands it there is
treating post-stratified weights as fixed, when a post-stratified total's sampling error is that of its residuals
within the region, age group and sex cells, which warns 9.

## Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting (calibration of survey weights and the precision it gives the published
  estimates, judged by the quality standard's warning line).
- **Domain test:** the quantity that decides is each published estimate's sampling error under the survey's clustered
  design and its post-stratification to population totals, the variance of a calibrated estimator that survey
  statisticians take from the residuals within the calibration cells over the PSUs.
- **Swap:** "which of the 48 regional estimates carry the low-reliability warning" rewritten as "which of the 48
  feeder loads carry the low-reliability warning", with megawatt-hours for adults: there is no sample, no design, no
  post-stratification and no sampling error, so the task stops making sense.
- **Layer 1:** the analysis files at two grains (households with their region, stratum, PSU and household answers;
  members with their own answers) and the weighting pipeline's weights file keyed by household and a person number that
  restarts in each household; children under 16 on the household rosters with no weight; not-asked, don't know and
  refused codes and proxy answers; the master sample's health-region code on PSUs selected before the 2025 boundary
  review; an outcome extract taken before every tablet had synced; issued addresses never worked; one outcome row per
  issue for reissued addresses; tablets re-writing a day's calls after a failed sync; advance letters and calling cards
  in the call log; population estimates in thousands by five-year band. Each is how the system that writes it works;
  none is placed to be caught, and none sits on the call's decisive step.
- **Layer 2:** estimation_fit: the sampling error of a post-stratified total, from the residuals within the cells the
  weights were scaled in, not from the weighted values with the weights held fixed.
- **Decisive step:** computing each published total's variance as the post-stratified estimator's (each adult's
  departure from the weighted rate of their region, age group and sex cell, totalled by PSU and linearised over the
  strata), not as a fixed-weight total's.
- **Not semantics:** reading every field, code and weight right (the adults joined to their weights on household and
  person, the codes scored, the children left out, the proxies kept) still leaves the default path on 15 warnings: the
  overstatement comes from the variance formula, not from any value read.
- **Not rule application:** QS-7 files the coefficient of variation, the general method (Taylor linearisation of the
  estimate as published over strata and PSUs), the line and the warning, and the weighting note files how the weights
  were made; no rule says that a post-stratified total linearises to its residuals within the cells, so executing every
  stated rule with the weights held fixed still files 15.
- **Analyst test:** a strong analyst who builds the responding adults, attaches the final weights, reads the strata and
  PSUs and computes each coefficient of variation by Taylor linearisation with the final weights treated as fixed warns
  15 estimates (Ends on: 15 of the 48 estimates warned, the public pension estimates of all four northern regions and
  the private renting estimates of R01 and R03 among them); one who ignores the clustering warns another set of 7 or 9;
  only the post-stratified estimator's variance gives the 9.
- **Estimand:** QS-7 (`ssb_qs7_statistical_quality_standard.pdf`) fixes the population (the 48 published totals of
  adults aged 16 and over in the 2025 health regions), the quantity (each total's standard error as the estimate is
  published over the unrounded estimate), the line (20.0 per cent or more) and the warning; the weighting note fixes
  how the published totals are made.
- **No decoy:** nothing is planted: no earlier quality report, draft or stakeholder figure gives a coefficient of
  variation or a warning list; the population estimates and the interviewer list (distractors) carry no precision
  figure.
- **No certified replay:** no certified or published 2027 coefficient of variation exists for a method to reproduce.
- **Lesson:** a calibrated estimate's precision lives in its residuals from the calibration cells; holding calibrated
  weights fixed overstates the error most where the cells explain the most, which no build on file teaches (task195
  takes a paired difference's uncertainty, task228 a variance at the randomised unit, task239 a factor at team level).

## Readability screen

Six tests per rung (stumping 2.1): 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a
column, key or marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control
or corpus scores the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or
half of a reported figure.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0a simple random sampling on the adults: 7 warned (pension in R01 and R02 in, arrears in R01, R03, R04 out) | 3.2 names strata and PSUs, which the rung ignores | the adults and weights | yes, the textbook p(1-p)/n | none | no | one ratio | readable |
| 0b the same with the weights' design effect (Kish): another 9, six cells off the golden | none | the weight column | yes, a common shortcut | none | no | one ratio | readable |
| 1 (default) Taylor linearisation over strata and PSUs, final weights fixed: 15 warned | 3.2 names the method and the design variables | stratum and psu columns on every household | yes: the survey package's default given weights, strata and PSUs | none | no | PSU totals, one formula | readable |
| 2 the region's adult total treated as known (the share's linearisation), or residuals within region by age or region by sex only: 10 or 11 warned | 2.1 sends the reader to the weighting note | none | partly, for an analyst who knows the region totals are fixed | none | no | a ratio's linearisation | readable |
| 3 (decisive) the post-stratified estimator's linearisation, residuals within the 96 region, age group and sex cells: 9 warned | no sentence links the weighting to the variance; QS-7 says only "the estimate as published", and the weighting note says nothing of sampling error | no design weight, cell id or residual ships; the final weight is one column | no: the reflex declares weights, strata and PSUs and stops | no control scores a variance estimator; no earlier report ships | no | not linear: cell rates, residuals, PSU totals, stratum variances | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | an estimate | the number of adults (QS-7 2.1) | the percentage of the region's adults | same call (the region total is fixed by the post-stratification: identical CVs) | QS-7 2.1; same call (asserted) |
| SF2 | the CV's denominator | the unrounded estimate | the published figure in thousands | same call | QS-7 3.1 ("before the estimate is rounded"); same call (asserted) |
| SF3 | 20.0 per cent or more | inclusive | exclusive | same call (no CV within a point of 20.0) | QS-7 3.3; same call (asserted) |
| SF4 | don't know and refused | not counted | the adult left out of the base | same call | QS-7 2.3; same call (asserted) |
| SF5 | proxy answers | the adult's own | dropped | same call | QS-7 2.3; same call (asserted) |
| SF6 | strata | as the analysis files give them | the master sample's region codes for the 12 moved PSUs | same call | QS-7 3.2 ("as the contractor's analysis files give them"); same call (asserted) |
| SF7 | an estimate's region | the households file's region (2025 regions) | the issued sample's master-sample code | same call | QS-7 2.2; same call (asserted) |
| SF8 | PSUs with replacement | no finite population correction | a correction for the address sampling fraction | same call (fractions under 1 per cent) | QS-7 3.2; same call (asserted) |
| SF9 | Taylor linearisation | the linearised variance | a replicate method (jackknife, each replicate post-stratified again) | same call | QS-7 3.2; same call (asserted) |
| SF10 | RENT and ARR | every adult in a renting or behind household | households | another quantity | codebook sheet Published tables ("each adult in the household") |
| SF11 | a region's estimate | a domain of the full design, every adult of the region in it (counted 1 or 0) | the region's records alone; or only the adults with the characteristic | same call for the region's records (strata nest in regions: identical); the holders alone are not the estimate's design | QS-7 3.2 ("over the wave's strata and primary sampling units"); same call (asserted) |
| SF12 | an adult's age group | age at interview | none other in the files | same call | weighting note |
| SF13 | the cell rate | weighted by the final weights | weighted by the design weights | same call (proportional within a cell) | same call (asserted) |
| SF14 | rounding | one decimal place at the close | none | same call (every CV 7 per cent of a bin or more from its edge) | the prompt's closing sentence; same call (asserted) |
| SF15 | adults | aged 16 and over | every roster member | same call (children carry no weight) | QS-7 2.1; same call (asserted) |
| SF16 | the with-replacement variance | n_h/(n_h - 1) times the squared deviations | the deviations without the factor | same call (every warned CV over 20/0.93) | QS-7 3.2; same call (asserted) |
| SF17 | a stratum with one PSU | none: every stratum holds two or more PSUs | a lonely-PSU convention | same call (nothing to apply it to) | the households file; same call (asserted) |

## Ladder

Four rungs and a floor, each a defensible way to take an estimate's sampling error, each dying to one fact of the
design (figures on the cut pack, asserted in `checks.py`).

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0a | simple random sampling on the responding adults | 7 warned: pension in R01 and R02 in, arrears in R01, R03 and R04 out | QS-7 3.2's strata and PSUs: adults cluster in households and PSUs |
| 0b | the same with the weighting design effect | 9 warned, six cells off the golden (pension in R01, R02, R03; arrears in R01, R03, R04 out) | the same: no clustering |
| 1 (default) | Taylor linearisation over strata and PSUs, final weights fixed | 15 warned: the golden nine plus pension in R01 to R04 (24.9, 37.8, 21.8, 25.1) and renting in R01 and R03 (28.4, 27.9) | the estimate as published is post-stratified: the weights were scaled to known totals within the cells, so the spread the fixed weights carry across cells is not sampling error |
| 2 | partial calibration: the region's total fixed (the share's linearisation), or residuals within region by age only or region by sex only | 11, 10 and 11 warned | the weights were scaled within all three of region, age group and sex |
| 3 (golden) | the post-stratified estimator's linearisation: residuals within the 96 cells, by PSU, with replacement | 9 warned; the jackknife with each replicate post-stratified again files the same 9 | |

- **Margins.** On the golden every warned estimate sits at 27.6 or more and every other at 18.4 or less; on the
  jackknife 28.9 or more and 18.7 or less. On the default path the six extras sit 1.8 to 17.8 points over the line.
  Every golden CV sits 0.0075 or more from its rounding edge.
- **Position.** The golden nine is reached by no other rung: simple random sampling gives seven, Kish another nine,
  the default fifteen, the partial calibrations ten or eleven.
- **Dominance.** The decisive move lowers each extra by 10.1 to 30.3 points (the pension estimates of the northern
  regions from 21.8 to 37.8 down to 5.0 to 8.4) and leaves the golden nine over the line.
- **Grid.** The cells the checks run: no clustering (7, another 9), fixed weights (15), partial calibration (10, 11,
  11), full post-stratification by linearisation and by jackknife (the golden 9). On the simulator's clean truth the
  same rungs file 15 and the golden (R3).

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the 48 published totals of adults aged 16 and over in the twelve 2025 health regions (QS-7 2.1, 2.2); children carry no weight (SF15) |
| 2 | Unit of account | one published estimate; its CV is its standard error over it (QS-7 3.1) |
| 3 | Attribution window | the 2027 wave's responding households; fieldwork 7 April to 26 September |
| 4 | As-of dating | the analysis files frozen with the weights on 12 November 2027 |
| 5 | Version basis | the 2025 health regions; the master-sample code gives the same call (SF7) |
| 6 | Denominator | the unrounded estimate (QS-7 3.1, SF2) |
| 7 | Weighting | the final weights; the estimate as published is the post-stratified total (weighting note) |
| 8 | Window length | one wave; nothing longer is read |
| 9 | Boundary inclusivity | 20.0 or more (QS-7 3.3); no CV within a point of it (SF3) |
| 10 | Rounding path | CVs from unrounded figures, one decimal at the close, every CV mid-bin (SF14) |
| 11 | Tie-break | none needed: no tied CVs near the line |
| 12 | Maturity and censoring | the wave is closed; every interview is in the analysis files |
| 13 | Order of operations | adults built, estimates coded, totals, linearised values, PSU totals, stratum variances, CV, line |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the analysis files hold one row per household and per adult (asserted) |
| 16 | Identity normalisation | household and person number join exactly; no key needs normalising |
| 17 | Netting against gross | not applicable: no amounts net |
| 18 | Dimensional units | adults; estimates published in thousands, the CV unitless |
| 19 | Code and status semantics | yes counts; don't know, refused and not asked do not; proxies count (QS-7 2.3, SF4, SF5) |
| 20 | Integerisation | none: totals and CVs continuous |
| 21 | Clause scope | QS-7 sections 2 and 3 apply to every published estimate of the wave |
| 22 | Forward window contents | the call is the 2027 tables' warnings; nothing is forecast |

## Literal reader

Executing the prompt, QS-7 and the weighting note word for word: the 48 estimates are the weighted numbers of adults
in each 2025 health region with each characteristic (2.1, 2.2, 2.3), made with the final weights, which are the design
weights post-stratified within the 96 region, age group and sex cells; each estimate's CV is the standard error of
that estimate as published over the unrounded estimate (3.1, 3.2), by Taylor linearisation over the analysis files'
strata and PSUs with replacement; 20.0 or more warns (3.3). The estimate as published is a post-stratified total, and
its Taylor linearisation is each adult's departure from their cell's weighted rate; that literal estimand files the
nine, and the replicate route the standard does not file (a jackknife post-stratifying each replicate) files the same
nine. The easy answer, fifteen, comes from an easy method on that same literal estimand (the final weights linearised
as if fixed), never from another reading: every reading in the fork table files the nine.

## Oracles

None for the call: no earlier quality report, published CV or certified figure ships; the population estimates (a
distractor) tie to the weights' totals under every variance method; the interviewer list (a distractor) carries no
precision figure. For the asks, the households file is the one referee: it says which households gave a full
interview, and it ties to no response rate or call count by itself.

## Ask sheet

**Ask 1, response rate by health region** (12 figures, per cent to one decimal). H18: QS-7 5.1's fieldwork measure the
quality report carries for every region, beside the warnings; the call does not read it. Use: the Branch's survey
statistics lead reads each region's response with its estimates. Primary device D2 (an attribute at the wrong vintage:
the issued sample's `region_code` is the master sample's code, and for the 12 PSUs the 2025 boundary review moved,
P1045, P1114, P1291, P1302, P1311, P3964, P4396, P4559, P4567, P4601, P5428 and P5721, it is the region before the
review; the region each PSU lies in is the one the households file gives its households); hazards: issued addresses
never worked (94, absent from the outcome extract, eligibility never established), the extract taken on 30 September
before 107 interviews' tablets synced (their extract codes 220, 230 or 310), one outcome row per issue for reissued
addresses (264), and e across the wave rather than by region (filed). Path: issued sample, outcome extract, households
file, call records, QS-7 sections 4.1 and 4.2 and Table 1, the dictionary (6 files, 11 columns: address_id, psu,
region_code, psu_frame, issue_no, outcome_code, outcome_date, hh_id, region, received_at, event_type). Stops: the
natural read (codes as held, extract only, extract codes final) R01 56.3, R02 52.4, R10 56.3 against 59.6, 49.9, 54.8;
the master-sample code alone moves every rate by 0.2 to 3.1; unworked addresses dropped alone, 0.2 to 1.2; the stale
extract alone, 0.9 to 2.2; every issue a row, up to 1.3 in eleven regions; e by region, up to 0.7 in seven. Realism: a
master sample keeps the strata it was drawn in; a case system extract holds each case's last synced status; an
address nobody reached has no outcome row.

**Ask 2, calls to the addresses that gave a full interview, by health region** (12 counts). H18: QS-7 5.1's measure of
the fieldwork effort behind each region's interviews; the call does not read it. Use: the Branch weighs each region's
response against the effort it took. Primary device D1 (a replay under fresh ids, key kept, beside genuine same-day
pairs: a tablet whose sync failed wrote the day's calls again when it next connected, 769 copies under new record ids,
their event numbers continuing the address's sequence, received two to five days later; every region holds at least
one responding address with a copy); hazards: the master-sample code (as ask 1), the stale extract's interviews, advance
letters and calling cards beside the calls, and the reissue's calls. Path: call records, households file, outcome
extract, issued sample, QS-7 4.3, the codebook's call log codes (6 files, 10 columns). Stops: copies kept alone add 1 to
74 calls in every region; the master-sample code alone moves every count by up to 86; the stale extract alone drops 2
to 103; letters and cards counted add 48 to 1,037; the last issue's calls only drop up to 55 in eight regions; the
natural read R01 78, R05 1,574 against 96 and 1,660. Realism: a tablet's sync retry writing records again is what the
office's log shows; letters and cards are logged by the same system as calls.

Main population zero-counts: the analysis files hold none of the 769 copies, no outcome row and no issued-sample code;
the call reads only the households, members and weights files, QS-7, the weighting note and the codebook; read with the
master-sample codes the call is the same nine (SF7, asserted), and no ask device touches the analysis files.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the master-sample code (D2) | 1, 2 | rate R02 +3.1; calls R07 +51, R09 -86 |
| the stale extract (D2) | 1, 2 | rate R04 -2.2; calls R05 -103 |
| never-worked addresses (D5) | 1 | rate R03 +1.2 |
| issue rows (D6) | 1 | rate R03 -1.3 |
| letters and cards | 2 | calls R05 +1,037 |
| re-written calls (D1) | 2 | calls R06 +74 |

Referee: the households file arbitrates the full interviews; nothing else ties.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask 1, R01 and R02 | P1045 counted in R02 under its master-sample code | miss |
| Ask 1, R03 and R04 | P1114 counted in R04 | miss |
| Ask 1, R05 and R06 | P1291, P1302 and P1311 counted in R06 | miss |
| Ask 1, R07 and R08 | P3964 and P4396 counted in R07 | miss |
| Ask 1, R09 and R10 | P4559, P4567 and P4601 counted in R10 | miss |
| Ask 1, R11 and R12 | P5428 and P5721 counted in R12 | miss |
| Ask 2, R01 and R02 | the re-written calls kept (record ids, event numbers and rows all unique), P1045 in R02 | miss |
| Ask 2, R03 and R04 | the re-written calls kept, P1114 in R04 | miss |
| Ask 2, R05 and R06 | the re-written calls kept | miss |
| Ask 2, R07 and R08 | the re-written calls kept | miss |
| Ask 2, R09 and R10 | the re-written calls kept | miss |
| Ask 2, R11 and R12 | the re-written calls kept | miss |

The cracker keeps the call and none of the 24 ask figures, Lc 0; the mirror (stopped at the fixed weights) keeps the
cells its fifteen shares with the golden nine where the rubric grades them (r about 8) and no ask figure, Ls 0.

Pair ceiling: 30.0 ((38 + 7 + 55 x 0) and (8 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each published estimate's sampling error under the survey's clustered design and its
   post-stratification, the variance of a calibrated estimator a survey statistician takes from the residuals within
   the calibration cells; with feeder loads or hospital visits in place of the sampled adults there is no sample, no
   design and no post-stratification, and nothing for the warning to judge.
2. Two layers: Layer 1 (the analysis files at two grains with the weights in their own file; children on the rosters;
   not-asked, don't know and refused codes and proxy answers; the master sample's pre-review region codes; the
   outcome extract taken before every tablet synced; addresses never worked; issue rows; tablets' re-written calls;
   letters and cards; population estimates by five-year band) is neutral on the call: every slip in R2 keeps the nine
   and leaves the default path on fifteen. Layer 2 is the post-stratified estimator's linearisation, asserted alone to
   move the default path to the golden on the simulator's clean truth (R3b).
3. No banned stump decides: nothing is planted (no earlier report, draft or published CV); not semantics (the default
   path reads every field and code right and files fifteen on the clean truth, R3a); not rule application (QS-7 files
   the estimand, the general method, the line and the warning, and names no calibration step or variance estimator,
   asserted on its text; the weighting note says nothing of sampling error, asserted).
4. Gate G: no shipped artifact ranks the estimates on precision or on the warning; the two distractors (the
   population estimates and the interviewer list) carry no precision figure.
5. Determinism: every CV sits 7 per cent of a bin or more from its rounding edge and every response rate too; the
   warning set holds under the jackknife, without the with-replacement factor, on the rounded estimate, with the
   master-sample codes and under every Layer 1 slip; the call counts are integers; the 16 fork rows are asserted in
   `checks.py` and the verifier recomputes every figure from the bundle alone.
6. Fingerprint: heart WARN (repeat.gate_g, overuse.gate_g, repeat.question_form, answered under Draw); the client was
   renamed from a name task186 already holds (tell.names) to the province's Statistics and Surveys Branch, every figure
   unchanged; surface promotes task238 (same pairing two builds apart, outside the ban window: a mode effect's
   estimand against a calibrated estimator's variance, differentiated on the card), task239 and task233 (the batch's
   shared README name and decision type).
7. Judge (one isolated thread, Sonnet, medium, the bundle and the graded blocks only). Pass 1: DETERMINISTIC, FIX_NOW
   on the write-up alone (step 7 said the 107 interviews postdated the extract; they predate it and reached the office
   after it), its low findings closed in the write-up and the dictionary (the households file named as the final
   outcome 110). Pass 2: DETERMINISTIC, APPROVE: all 48 CVs, the nine warnings, the 12 response rates (e = 0.91697) and
   the 12 call counts reproduced from the files; the fixed-weight route files 15; the nine hold without the
   with-replacement factor and under the re-post-stratified jackknife. Gate G method_or_model_selection,
   analytical_non_defect, no surface read, not a sole data defect; Gate H domain pass, layers pass, decisive step
   analytical. Its optional polish (a dictionary line saying the master-sample code is not the 2025 region) is not
   taken: it would narrate the first ask's device, and the judge notes it changes nothing a solver must do.

## Leak check

`leak.py --asof 2027-12-03`: REVIEW, no LEAK. The REVIEW lines: the figure 20.0 in QS-7 3.3 (the standard's own line,
harmless); 2.2 (a section number, harmless); the stump paragraph's vocabulary in the standard, the weighting note, the
close-out, the readme and the dictionary (weights, population, strata, post-stratified: the weighting note's account of
how the weights were made and the standard's account of what is published, which the call needs; none names the
variance step, asserted on the standard's and the note's text).

Solver's-eye reads (two isolated reads, Sonnet, medium, the prompt and the bundle only; the second after the
dictionary's households entry changed):
- Question 1: none, both times. The closest cue each quoted is QS-7 3.2's "the estimate as published", which neither
  read as naming the step ("hinted but never named").
- Questions 2 to 4: none, both times.
- Question 5: QS-7 2.1, 2.3, 3.1, 3.2 and the codebook, each executing to the golden's population and quantity; both
  reads noted that 3.2 does not say how the post-stratification enters the variance, which is the decisive step left
  to the analyst.
- Question 6: an analytical choice, both times (whether the variance reflects the post-stratification), the second
  read adding a semantics risk on "as published"; the judge holds it analytical for the same reason (the weighting
  note describes the weights and says nothing of sampling error).
- Realism: letters all logged at 09:00 (fixed: each day's mailing-run time); event numbers out of time order where a
  tablet re-wrote calls, the moved PSUs' 82 responding households, the regions' uneven sizes and three-decimal
  weights (kept: each is how the systems write the records or how the province's population falls).
- Ambiguities raised and where each closes: the region of a non-responding address (QS-7 4.2 "the health region it
  lies in" with 2.2's 2025 regions, the PSU's region in the households file; the judge reproduced it); the 94
  addresses with no outcome (4.2 "every address issued counts", their eligibility never established, each with only
  its advance letter); the extract's stale codes (the dictionary: the households file is "one row per household that
  gave a full interview (final outcome 110)"); a call written twice (4.3 counts calls, not records); single-PSU strata
  (none, SF17); the domain (SF11).

## Tried and rejected

- The seed's pitfall (one overall nonresponse factor against adjustment within cells): with the cells named it is
  rule application, without them the call is not determinate; dropped at the draw.
- The variance of a wave-on-wave change with overlapping samples: task195 holds the paired difference's own
  uncertainty, and the task type serving it (complex-survey-estimation-variance) does not serve Data Quality; dropped
  at the draw.
- Full-time education as the second age-driven estimate (the prototype's indicator set): replaced by private
  renting, a household answer every adult carries, before the simulator was tuned at seed 61.
- The average calls per responding household: R06's figure sat 0.004 of a bin from its rounding edge; the count of
  calls is graded instead.
- e taken within each region: four rates sat within 7 per cent of a bin of their edge; e across the wave is filed.
- A lookup file of the PSUs' 2025 regions: it turned the master-sample code into a work order; the households file's
  region is the only current code.
- Selection probabilities in the issued sample: a design weight would let a solver linearise with design weights
  rather than final weights and open a fork on the main call; not shipped.
- A 2026 quality report as a distractor: it ranks the same estimates on the decision question (Gate G); dropped.
- Calls at the same address in the same minute from the simulator's clock: re-timed to the next free minute, so the
  only duplicates on address, issue, time, type, result and interviewer are the tablets' copies.
