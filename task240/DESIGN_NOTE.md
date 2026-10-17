# task240 design note

Architecture 1, wave 3, seed DQ13 (whether this wave's estimate trips the weighting pipeline's quality alert): the
seed's world, decision and quantity only, the pitfall re-found from the data under the 10/10 rules. Survey Research &
Official Statistics, nonresponse, calibration and measurement-error adjustment, Data Quality Monitoring & Alerting.
Larchmere Social Research runs the Household Resources Survey for a Canadian province's ministry under contract: each
year's wave interviews every adult in a stratified, clustered sample of households, the weighting post-stratifies the
responding adults to the province's population by health region, age group and sex, and the agency publishes each of
twelve health regions' estimates of four indicators (adults receiving a public pension, in full-time education,
providing unpaid care, and behind on a household bill in the past year). The client's statistical quality standard
puts a low-reliability warning on every published estimate whose coefficient of variation reaches its line, and the
agency's quality report, delivered with the wave's tables under the contract, sets out which estimates carry it.

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
  the call a monitoring decision on the quality report.
- **Niche.** The variance of a calibrated (post-stratified) estimator: the weights are ratio-adjusted within region,
  age group and sex cells to known totals, so a published total's sampling error is that of the residuals within the
  cells over the clusters, not of the raw values with the weights held fixed.
- **The call.** Which of the 48 published estimates (twelve regions by four indicators) carry the low-reliability
  warning in the 2027 quality report.
- **Shape.** 07, grid of cells: each region-indicator cell's estimate, coefficient of variation and warning.
  Decision designation_set, answer set_of_items, question form which.
- **Strategy.** decomposition_attribution (each published total split into the part the population totals fix and
  the residual within the cells, whose spread alone is sampling error), G17 decisive (each estimate judged against its
  own sampling error), G16 (the variance estimator the standard's sampling error of the estimate as published
  entitles), G2 (the cluster as the unit of the variance, a lower rung); Gate G method_or_model_selection; calibration
  none; context artifact filed_standard (the client's statistical quality standard); layer 2 family estimation_fit,
  pattern own:post-stratified-estimate-variance-from-within-cell-residuals.
- **Forum, event, organisation.** customer_or_counterparty (the client ministry's survey statistics lead receives the
  quality report), purchase_order_or_contract (the wave's tables and quality report are the contract's deliverable),
  professional_services. All clear the last three builds.
- **People** (`guard.py names --geo Canada --seed 240`, locale en_CA): Kristina Stephens, the agency's lead survey
  statistician, who signs off the quality report; Latasha Evans, the ministry's survey statistics lead, who receives it;
  Anna Mckee, the agency's fieldwork manager, who wrote the fieldwork close-out.
- **Deliverables.** `hrs27_quality_report.xlsx` (every estimate with its coefficient of variation and warning, and the
  asks' figures) and `hrs27_quality_note.docx` (the note the ministry publishes beside the tables: the warned estimates
  and why).
- **As-of.** 2027-12-03: fieldwork ran from 7 April to 26 September 2027, the weights were frozen on 12 November, and
  the tables and quality report are due to the ministry on 10 December.
- **Data-native sentence.** Every responding adult's weight was scaled within region, age group and sex until the
  weights add to the population; an estimate that age and sex largely decide (who receives a public pension, who is in
  full-time education) is therefore almost fixed by those totals, and its sampling error is only the scatter of adults
  around their cell's rate, which the weights' own spread hides: the smaller a region's sample, the more weight the
  spread carries and the further a fixed-weight error overstates it.

Sources, one line each (what it teaches; how this build differs):
- Särndal, Swensson and Wretman, and Deville and Särndal on calibration estimators: the variance of a calibrated total
  is that of the residuals from the calibration variables; here the calibration is post-stratification and the step is
  never named in the pack.
- Statistics agencies' quality flags (a letter or a warning by coefficient of variation band): the convention the
  client's standard follows; the line and the warning are filed, the variance estimator is not.
- The client's survey patterns (variance reflecting strata and PSUs; domain estimates keeping the full design): the
  lower rungs; neither is this build's step.

## Default path

1. Read the client's standard (a published estimate whose coefficient of variation reaches the line carries the
   warning) and the agency's weighting note (design weights post-stratified by region, age group and sex).
2. Build the responding adults from the adult file, join the final weights, and code each indicator from its question
   (yes counts; don't know and refused do not).
3. Estimate each region's total of each indicator with the final weights.
4. Take each total's standard error by Taylor linearisation over the strata and PSUs, the final weights treated as
   fixed (the with-replacement formula, or a survey package given the weights, strata and PSUs).
5. Divide by the estimate and warn every estimate at or over the line.

Ends on: 14 of the 48 estimates warned, the pension and full-time-education counts of the smallest regions among them.

Golden: 6 of the 48 warned, from each total's variance as the post-stratified estimator's (the residuals within the
region, age group and sex cells, linearised over the strata and PSUs); the pension and education counts of the small
regions are precise.

## Stump sentence

A competent analyst takes each published total's standard error by Taylor linearisation over the strata and PSUs with
the final weights treated as fixed and warns 14 of the 48 estimates, the pension and full-time-education counts of the
smallest regions among them; the step that lands it there is treating post-stratified weights as fixed, when a
post-stratified total's sampling error is that of its residuals within the region, age group and sex cells, which
warns 6.

## Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting (calibration of survey weights and the precision it gives the published
  estimates).
- **Domain test:** the quantity that decides is each published estimate's sampling error under the survey's clustered
  design and its post-stratification to population totals, the variance of a calibrated estimator that survey
  statisticians take from the residuals within the calibration cells over the PSUs.
- **Swap:** "which of the region estimates carry the low-reliability warning" rewritten as "which of the substations'
  monthly loads carry the low-reliability warning", with megawatt-hours for adults: there is no sample, no design, no
  post-stratification and no sampling error, so the task stops making sense.
- **Layer 1:** the fieldwork system's household and adult files at two grains beside the sample file of issued
  addresses; the weighting pipeline's weights file keyed by a person number that restarts within each household;
  don't know and refused codes and proxy answers; adults entered twice when a roster was re-sent and household members
  under 16 in the adult file; older PSUs carrying pre-review health-region codes read through a lookup; population
  totals in thousands by five-year band. Each is how the system that writes it works; none is placed to be caught.
- **Layer 2:** estimation_fit: the sampling error of a post-stratified total, from the residuals within the cells the
  weights were scaled in, not from the raw values with the weights held fixed.
- **Decisive step:** computing each published total's variance as the post-stratified estimator's (each adult's
  departure from the weighted rate of their region, age group and sex cell, totalled by PSU and linearised over the
  strata), not as a fixed-weight total's.
- **Not semantics:** reading every field, code and weight right (the adults deduplicated, the codes scored, the weights
  joined on household and person, the regions read through the lookup) still leaves the default path on 14 warnings:
  the overstatement comes from the variance formula, not from any value read.
- **Not rule application:** the standard files the coefficient of variation, its line and the warning, and the
  weighting note files how the weights were made; no rule says how to compute a post-stratified estimate's standard
  error, so executing every stated rule with the fixed-weight variance still files 14.
- **Analyst test:** a strong analyst who builds the responding adults, attaches the final weights, reads the strata
  and PSUs and computes each coefficient of variation by Taylor linearisation with the final weights treated as fixed
  warns 14 estimates (Ends on: 14 of the 48 estimates warned, the pension and full-time-education counts of the
  smallest regions among them); one who ignores the clustering warns a different set; only the post-stratified
  estimator's variance gives the 6.
- **Estimand:** the client's statistical quality standard (`hrs27_statistical_quality_standard.pdf`) fixes the
  population (the 48 published totals), the quantity (each total's standard error as the estimate is published, over
  the estimate), the line and the warning; the weighting note fixes how the published totals are made.
- **No decoy:** nothing is planted: no earlier report, draft or certified figure gives a coefficient of variation or a
  warning list for 2027; the 2026 quality report (a distractor) gives last year's warnings on a different sample.
- **No certified replay:** no certified or published 2027 coefficient of variation exists for a method to reproduce.
- **Lesson:** a calibrated estimate's precision lives in its residuals from the calibration cells; holding calibrated
  weights fixed overstates the error most where the cells explain the most, which no build on file teaches (task195
  takes a paired difference's uncertainty, task228 a variance at the randomised unit).

## Tried and rejected

- The seed's pitfall (one overall nonresponse factor against adjustment within cells): with the cells named it is
  rule application, without them the call is not determinate; dropped at the draw.
- The variance of a wave-on-wave change with overlapping samples: task195 holds the paired difference's own
  uncertainty, and the task type serving it (complex-survey-estimation-variance) does not serve Data Quality; dropped
  at the draw.
