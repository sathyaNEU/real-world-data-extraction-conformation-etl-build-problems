# task192 design note

How many of a protest register's recorded actions were confrontational, when most of the record's
labels come from a classifier the association measures against hand coding, and the hand coding only
ever reached the opening of the period. Architecture 3.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task192.json`, architecture v3, registered 2026-10-17T15:52:44Z |
| Domain, task type | political-science-public-policy, `conflict-protest-event-data-analysis` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 17, periods around a change point, one workbook and one bulletin page |
| Decision | quantity_figure, a count of actions |
| Gap | objective, then population |
| Gate G | `method_or_model_selection`; decisive generator G12, then G3 |
| Strategy | `other`: no vocab strategy names a measurement-error correction |
| Layer 2 | `field_method`, own pattern `own:machine-coded-record-corrected-in-both-directions` |
| Calibration | `gold_standard_subsample`, the association's own double-coding worksheet |
| World | Portugal, a conflict monitoring association, EUR |
| Register opened | 1 May 2026; reporting period 1 May to 30 October 2026 |
| As-of date | 2026-11-06 (the record extract); the trustees meet on 19 November |
| Guard | PASS at WARN; two WARNs answered below |

**Data-native sentence.** Two actions in three reach this register only through the press monitor,
whose classifier reads news text and assigns the action code, and the association's own hand coding
only ever reached the opening of the period: the coding desk's two rounds closed on 20 June and 10
September and between them cover the reports of 1 May to 31 August, while the autumn mobilisation
that trebles the record's volume from 5 September has no hand-coded report in it at all, and the
classifier's own marked rate falls from 9.7 per cent inside that window to 4.9 per cent outside it,
so the only thing the audited reports can carry forward is what the classifier does to a report of a
given kind, never what share of the reports were of that kind.

**The two WARNs the guard raised.**
- `repeat.gate_g` and `overuse.gate_g` (`method_or_model_selection`, 5 of the last 12, repeating task193):
  the other builds in the window select a model by back-test, by a reviewer's reach, by a conversion
  sized at its value and by a maturity correction. None selects between estimators that differ in
  which of an instrument's measured quantities transport to a population the instrument was not
  measured on, which is what separates the candidates here.
- The driver sits at 0.10 against task189's left-censored averages and below that against every other
  card on file; no card and no lineage entry corrects a count for an instrument's error rates where
  the validation window and the population differ in composition.
- Neither this build nor task193 moves on it, and that is the author's call rather than the guard's.
  `method_or_model_selection` is the label every build carries whose decisive step is choosing the
  field's estimator over the generic move, which is what the client's rule 1 asks for, so it recurs in
  any wave built to the spec and is not evidence of a monoculture on its own. What would be is a
  repeated driver, and the drivers here are 0.09 at their nearest neighbour and sit in different Layer
  2 families (`field_method` against task193's `estimation_fit`), different domains and different
  patterns.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD15: the decision shape only, one figure committed at
  a date to a standing body about coordinated contention.
- `stumping/references/client/layer2-rigor-patterns.md`: this task type's filed pattern 1 is that
  reported events track media reach and the analysis must condition on the reporting proxy. This build
  takes the other half of the same instrument, not how far the press reaches but what its coder makes
  of what it reaches, which is the validation literature protest event analysis runs on.
- `guard.py mechanisms --objective anomaly-detection`, re-read after the remote merge: none of the
  spent drivers corrects a count for a classifier's measured error, and none turns on a validation
  sample whose own composition differs from the population it is carried to.
- `guard.py check` over the whole corpus after the merge, including task266 and task157, which took
  architecture 2's mechanism and its structural triple.
- **task446 v2**'s decisive quantity is a forward count for a population whose base rate has moved,
  and its error is carrying a yield measured on earlier populations onto that one; here the error is
  the mirror image, that one of the two things the audit measures (what share of the audited reports
  were confrontational) does not transport while the other (what the classifier does to a report that
  is) does, and the correction takes wrongly marked actions out as well as putting missed ones in.
- **task448** completes a register that misses whole producers by estimating a second list's capture;
  here nothing is missing from the record, every action is in it and the question is which class it
  belongs to.

## Default path

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, and resolve every reported place through `gazeteiro_localidades.csv`,
   current and former names alike.
2. Resolve the three routes, the two language editions of the Atlantic group and the reposted August
   month so that each action is counted once on the protocol's 2.1 grain, one theme at one locality on
   one calendar day.
3. Read 3.3 and see that the number is of the actions that were confrontational and not of the codes
   the classifier assigned, so open `amostra_dupla_codificacao.csv`.
4. Split the hand-coded reports by what the classifier said about them, and take from each side the
   share that the coding desk found was really confrontational: of the reports it marked, 78 per cent
   were; of the reports it did not, 8 per cent were.
5. Carry those two shares onto the register's 4,200 press-reported actions and add the 30 an
   organisation or the public line coded by hand, then round to the nearest fifty.

**Ends on:** 600 confrontational actions.
**Golden:** 450 confrontational actions.

## Stump sentence

A competent solver resolves the three routes, builds the actions on the protocol's grain, reads 3.3,
corrects the classifier's labels with the shares the hand coding found on each side of them and files
**600 confrontational actions**, because those two shares were measured on the opening of the period,
where about one press-reported action in seven was confrontational, and are carried onto a period in
which about one in ten was.

## Three rules

- **Task type:** `conflict-protest-event-data-analysis`, the task type in Political Science & Public
  Policy that serves Anomaly Detection: turning multi-source reports into an event record and
  separating what happened from what the record's own instruments made of it.
- **Domain test:** the deciding quantity is the count of confrontational actions in a contentious
  event record, which protest event analysis estimates from a machine-coded corpus read against a
  hand-coded validation batch, because an automatic coder of news text misses about half of a
  confrontational action's reports and marks a small share of the many ordinary ones. The field's own
  method carries the classifier's sensitivity and its false-mark rate into the count, which are
  properties of the coder and hold wherever it ran; a generalist carries the validation batch's own
  confrontational shares instead, which are properties of the batch.
- **Swap:** "how many of the parcels the belt recorded were damaged" counts a physical property a
  scanner reads directly. What breaks is that there is no coder reading news text, no hand-coding
  standard for it to be measured against and no protocol definition of the class being counted: the
  quantity becomes a physical count, the hand-coding worksheet has nothing to code and nothing is left
  to estimate.
- **Layer 1:** the association's own pipeline makes all of it. The press monitor's item log carries
  every item the keyword list caught, accepted or rejected, at item grain, and a report entered the
  monitor with the first of its items; the same action arrives from up to three access routes and from
  two language editions of one media group; one month of partner reports was loaded twice and the
  import log carries both loads while the ingest counter counted the second arrival again; the
  monitor's reception stamps and the partner portal's are UTC while the action times are the local
  clock of the action's own district, the clocks go back an hour on 25 October and the Azores run an
  hour behind the mainland; the partner organisations' monthly returns arrive inside a PDF; one
  partner's deliveries change code after a merger; the gazetteer carries superseded settlement names.
  None of it is placed to be caught and none of it decides the count.
- **Layer 2:** `field_method`. The methodological choice is which of the quantities the hand coding
  measures can be carried to a period the hand coding never reached.
- **Decisive step:** rebuild the count of confrontational actions among the actions the press monitor
  carries from the classifier's measured sensitivity and false-mark rate, which are properties of the
  coder and do not depend on how confrontational the audited weeks happened to be, rather than from
  the audited reports' own confrontational shares, which do; then add the actions a filer coded.
- **Not semantics:** every field, code, zone, offset and place name read correctly still leaves the
  default path carrying the audited batch's own shares onto the record and filing 600. The dictionary
  gives every field, the protocol defines the action grain and lists the confrontational codes, the
  monitor's configuration gives the offsets and the rounding is filed. Reading all of it right is what
  produces the 600.
- **Not rule application:** the protocol files the action grain, the confrontational codes, the
  reporting period, which route's code the register keeps, that the count is of the actions and not of
  the codes, the granularity, and what each round of hand coding drew its batch from. No shipped
  sentence says how the classifier's labels are to be turned into the count: nothing names
  sensitivity, specificity, recall, precision, a correction, a false positive, a false negative,
  representativeness or extrapolation, and a word sweep over every shipped file asserts it. The
  worksheet states two codings per row and no rate at all.
- **Analyst test:** a strong analyst who resolves the three routes and the two editions, drops the
  reposted month, resolves the superseded place names, applies every filed paragraph and corrects the
  classifier's labels with the shares the hand coding found on each side of them files **600
  confrontational actions**, the default path's `Ends on:`, where the period's record gives 450.
- **Estimand:** the protocol's 3.3, "Indicador 2, acoes de confronto: o numero das acoes registadas no
  periodo de relato que foram acoes de confronto na acepcao de 2.2, ao mais proximo de cinquenta
  acoes. O codigo que o classificador do monitor de imprensa atribui e a leitura do classificador, que
  a mesa de codificacao mede contra a codificacao manual. O numero que o boletim fixa e o das acoes
  que foram de confronto e nao o dos codigos atribuidos." Population, outcome, window, unit and
  rounding are all there, and 4.5 files what each round of hand coding is a batch of and over what;
  how the count is rebuilt is not.
- **No decoy:** nothing is planted to be caught. No block of items is copied, no memo argues a count,
  no stakeholder figure carries one, and no shipped file states a confrontational count, a rate, a
  sensitivity or a false-mark rate. The hand-coding worksheet is the association's own standing
  quality record, with its coders, its coding dates, its second codings and the desk's decisions on
  them, as every machine-coded event dataset publishes one.
- **No certified replay:** no published confrontational count ships. The earlier monthly bulletins
  report actions recorded and territory touched and never the confrontational ones, so no method can
  be recovered by reproducing a figure.
- **Lesson:** a validation batch measures two different kinds of thing at once, what the instrument
  does to a unit of a given class and what share of the units were of that class, and only the first
  travels to a window the batch never covered. When the record's own composition moves between the
  audited window and the rest, the easy correction inherits the audit's calendar and the count is
  wrong by a third. No build on file teaches it.

## WHAT screen

The decisive step is the one above: carry the classifier's two measured error rates rather than the
audited batch's own shares. It settles no part of the estimand.

| Part of the estimand | Settled by | The sentence that files it |
|---|---|---|
| Population | the protocol, not the decisive step | 3.2 files the reporting period and 2.1 the actions the register holds |
| Outcome | the protocol | 2.2 lists `CF`, `RF` and `DP` as the confrontational actions, and 3.3 says the count is of the actions that were confrontational |
| Window | the protocol | 3.2, 1 May to 30 October 2026 inclusive |
| Unit | the protocol | 2.1, one theme at one locality on one calendar day, however many reports |
| Comparison | none; the indicator is a level | 3.3 states a count, against nothing |
| Rounding | the protocol | 3.3, to the nearest fifty actions |

Two or more estimators of that one filed quantity stand after it is filed, and the record's own
structure separates them: the audit covers four of the period's six months, two of the fourteen
dispute themes have no audited report at all, and the classifier's marked rate inside the audited
window is twice what it is outside it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the actions the register carries under the confrontational codes | 2.2 lists the codes and 3.3 names the count | `codigo_acao` is a column of every report file | yes, the first group-by anyone writes | none | the battery finds the duplicate feeds, not this | one filter and one count | readable |
| 1 the coded count with the classifier's false marks taken out | no sentence names a false mark | the worksheet's two coding columns invite the comparison | yes, the precision reflex | none | no | one ratio | readable |
| 2 the hand codes where the desk audited and the classifier's code elsewhere | no | the worksheet's report identifiers join straight to the item log | yes, trust what you measured and leave the rest | none | no | one join and one count | readable |
| 3 the audited reports' own confrontational shares on each side of the classifier's label, carried onto the record (the default) | no sentence names a share or a correction; 4.5 names only what each round drew its batch from | the worksheet's two coding columns are the whole input | yes, the predictive-value reflex: of the ones it marked this share were, of the ones it did not this share were | none | no | two ratios | readable |
| 4 the coded count scaled by the classifier's recall | no | the same two columns | yes, the recall reflex | none | no | one ratio | readable |
| 5 the count rebuilt from the classifier's sensitivity and false-mark rate, which do not move with the audited window's composition (decisive) | no shipped sentence names sensitivity, specificity, recall, precision, a correction, a false positive, a false negative, representativeness or extrapolation, asserted by a word sweep over every shipped file; 3.3 says only that the count is of the actions and not of the codes, and 4.5 says only what each round drew its batch from | no column holds an error rate, a weight or a stratum: the worksheet is two codings, a coder, a coding date, a round and the desk's decision | no reflex: the two reflexes above each carry a quantity measured on the audited weeks and file a different number, and the reflex that trusts the hand codes where they exist files a third | nothing scores a count; the earlier bulletins report actions and territory, never confrontational actions | the battery finds the two editions, the reposted month, the ingest counter and the clocks and leaves the count open | no: the six candidates are 250, 350, 400, 450, 600 and 650 from the same rows, and the step is a two-rate algebra | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | action | one theme at one locality on one calendar day, however many reports, 2.1 | one report, so a double-reported action counts twice | the count changes | 2.1 quoted; asserted |
| SF2 | confrontational action | an action that was of a kind 2.2 lists, whatever code the record carries | an action whose recorded code is `CF`, `RF` or `DP` | the count is rung 0, 350 | 3.3 quoted, the count is of the actions and not of the codes assigned; asserted |
| SF3 | the confrontational codes | `CF`, `RF` and `DP` | `CF` alone, or any code a report's text calls violent | the count changes | 2.2 quoted, which lists the three; asserted |
| SF4 | the reporting period | actions dated 1 May to 30 October 2026 inclusive | the calendar half year, or to the extract date | the count changes | 3.2 quoted and the prompt's period; asserted |
| SF5 | which code an action carries | the code of the report the register keeps: a filer's where one exists, the classifier's otherwise, 2.6 | the classifier's code wherever one exists | the corrected population changes | 2.6 quoted; asserted |
| SF6 | the hand-coding worksheet | the desk's batches of items the classifier coded, with the hand coding beside each | a sample of all actions, or a sample of confrontational actions | the measured rates change | 4.5 quoted and the dictionary's scope line; asserted that every row is a press-monitor report |
| SF7 | the action date | the local calendar day the register fixes, which no reception stamp overrides | the reception stamp's date | up to two actions move day | the dictionary's two sentences; asserted that no action's date moves |
| SF8 | a locality | the gazetteer's settlement, with superseded names resolved | the free-text place name as reported | localities split, actions do not | 2.3 and the gazetteer's name-state column; asserted |
| SF9 | the reposted month | each action counted once however many loads carry its reports | the month's reports counted twice, or the month dropped | the report counts change, the action count does not | the import log's two entries, the dictionary's load sentence and the repeated report identifiers; asserted both ways |
| SF10 | the two language editions | one action however many editions report it | one action per edition | the report counts change, the action count does not | the dictionary's report-identifier sentence; asserted |
| SF11 | rounding | the count to the nearest fifty actions, rounded once at the end | the count as a whole number | `same call`, asserted: the estimate is 453.01 and 450 is the nearest fifty either way |
| SF12 | ties | none: the six candidate cells are 250, 350, 400, 450, 600 and 650 | two candidates on one cell | `same call`, asserted pairwise distinct from the golden's cell |
| SF13 | the accepted items | the items the press monitor accepted, which the register carries | every matched item, rejected ones included | rejected items are not actions | 4.2 quoted and the dictionary's acceptance column; asserted |
| SF14 | the extract | the record as extracted on 6 November 2026 | the record as at the period's close | `same call`, asserted: no action dated inside the period is reported after the extract |
| SF15 | actions outside the period | excluded from the count | included because their reports arrived inside it | the count changes | 3.2 quoted, which fixes the period on the action's date; asserted |
| SF16 | the hand coding | the standard the desk measures the classifier against, after the desk's decision on a second coding | one more opinion to be averaged with the classifier's | the measured rates change | 4.5 quoted and the dictionary's `codigo_manual` line; asserted |
| SF17 | a report the gazetteer does not place | not an action, so outside every count | an action at an unknown locality | the count changes | 2.5 quoted; asserted |
| SF18 | the register's opening | 1 May 2026, with no action carried in | an action before the register opened | nothing to count before it | 3.2 quoted; asserted that no action predates 1 May 2026 |
| SF19 | a fortnight | fourteen days from 1 May | fifteen-day blocks, or a fourteenth one-day row | the fortnight rows change, the count does not | 3.4 quoted, which gives the length in days; asserted |
| SF20 | the days left at the end of the period | into the last fortnight, which has fifteen days | a fourteenth fortnight of one day | the last fortnight's figures change | 3.4 quoted and the `convencoes` sheet; asserted |
| SF21 | a partner's delivery codes | the codes of one agreement count together | each delivery code is its own organisation | one partner's filings and euros change | the agreements' addendum of 8 September and the `convencoes` sheet; asserted that both codes are in the file |
| SF22 | a district's clock | the offset the monitor's configuration gives the district, the Azores an hour behind | the mainland clock everywhere | one route's median moves by a minute | `config_monitor.json` quoted and the gazetteer's district column; asserted that the two island districts are separate |
| SF23 | the reception moment of a press report | the first of its items, the dictionary's sentence | the last item, or every item | one route's median changes | the dictionary's `carimbo_recepcao` line; asserted |
| SF24 | an Azores action | an action in the Azores district, on the Azores clock | none in the record | the median would not move | asserted that the record holds actions in the Azores district |

## Ladder

| Rung | The estimate | Raw | To the nearest fifty |
|---|---|---|---|
| 1 | the coded count with the classifier's false marks taken out | 228 to 265 | 250 |
| 0 | the actions the register carries under the confrontational codes | 332.00 | 350 |
| 2 | the hand codes where the desk audited and the classifier's code elsewhere | 387.00 | 400 |
| 5 | **answer:** the count rebuilt from the classifier's two measured error rates | **453.01** | **450** |
| 3 | **default:** the audited reports' own confrontational shares carried onto the record | 592.59 | 600 |
| 4 | the coded count scaled by the classifier's recall, or the audited prevalence over the record | 642 to 660 | 650 |

Measured on the cut pack, not on a model: the register holds 4,627 actions in the reporting period,
of which 4,200 carry a press monitor report and take its classifier's code and 427 reach the register
only through a partner organisation or the public line and take the filer's. The register carries a
confrontational code on 302 of the first group and 30 of the second. The coding desk's two rounds hand
coded 1,000 of the monitor's reports, 23.8 per cent of the 4,200 the period holds, and returned 74
agreed confrontational, 76 the classifier missed, 21 it marked wrongly and 829 agreed ordinary, which
is a recall of 0.4933 and a false-mark rate of 0.0247. The answer's raw figure is 453.013 actions.

**Separation.** 250, 350, 400, 450, 600 and 650 are six distinct cells of the stated granularity. The
nearest wrong figure to the answer is 387.00, 14.6 per cent away, and the nearest wrong cell is 400,
one cell away; the default path's 592.59 is 30.8 per cent away. Every candidate is the complete output
of a competent pipeline on the same rows, and the answer is fourth of the six and bracketed, so no
solver reaches it by stopping early and none by correcting hardest.

**The candidate set, measured over the judge's own list.** Every route the record leaves standing was
computed on the shipped bundle and asserted in `checks.py` by name (`cand.*`):

| Route | Figure | Cell | Distance from the answer |
|---|---|---|---|
| the false marks taken out on the false-mark rate | 228.24 | 250 | -49.6 per cent |
| the false marks taken out on precision | 265.24 | 250 | -41.4 per cent |
| the codes as the register carries them | 332.00 | 350 | -26.7 per cent |
| the hand codes where audited, the classifier's elsewhere | 387.00 | 400 | -14.6 per cent |
| a continuity adjustment of half a case in each cell | 448.47 | 450 | -1.0 per cent |
| **the two error rates (the answer)** | **453.01** | **450** | - |
| the same correction as the inverted confusion matrix | 453.01 | 450 | identical by construction, asserted to 1e-9 |
| the audited rows taken as known and the rest corrected | 453.01 | 450 | identical by construction, asserted to 1e-9 |
| the two error rates by month, pooled where a month has no audited row | 457.84 | 450 | +1.1 per cent |
| the two error rates by theme, pooled where a theme has no audited row | 470.40 | 450 | +3.8 per cent |
| the audited shares by month, pooled where a month has none | 591.65 | 600 | +30.6 per cent |
| the audited shares on each side of the label | 592.59 | 600 | +30.8 per cent |
| the audited shares by theme, pooled where a theme has none | 598.81 | 600 | +32.2 per cent |
| the coded count scaled by the recall | 642.16 | 650 | +41.8 per cent |
| the audited prevalence over the press-reported actions | 660.00 | 650 | +45.7 per cent |
| the two error rates by month, with no pooling | not computable | - | September and October hold no audited report |
| the two error rates by theme, with no pooling | not computable | - | `ENE` and `FLO` hold no audited report |
| the audited shares by month or by theme, with no pooling | not computable | - | the same two gaps |
| the two error rates by round, with population weights | not computable | - | neither round's window covers the autumn |

Every route built on the classifier's two error rates lands in the answer's cell; every route built on
the audited batch's own confrontational shares lands two cells away; and every stratified route has no
rate for part of the population it is applied to, because the audit never reached September or October
and the two dispute themes that opened with the autumn wave have no audited report at all.

**What makes it forced, measured and not narrated.**
- The audit covers months 5 to 8 of the period's 5 to 10, asserted (`dead.audit_window`,
  `dead.population_wider`).
- `ENE` and `FLO`, two of the protocol's fourteen dispute themes, first appear on or after 5 September
  and hold no audited report, asserted (`dead.theme_reason`, `dead.late_themes_after_surge`).
- The record's own marked rate is 9.70 per cent on the 2,001 press-reported actions inside the audited
  window and 4.91 per cent on the 2,199 outside it, chi-square p = 2.0e-09, asserted
  (`force.marked_rate_moves`). Month by month it runs 11.73, 8.30, 9.48, 9.03, 5.49, 4.38.
- The audit's own hand-coded prevalence is 15.00 per cent against the record's 9.79 per cent, a factor
  of 1.53, asserted (`force.audit_prevalence_above_record`), and inside the audit it falls month by
  month, 18.64, 15.22, 13.65, 11.98 (`force.audit_prevalence_trend`).
- Across the two rounds the classifier's recall (0.514 against 0.474, p = 0.63) and its false-mark
  rate (0.0260 against 0.0238, p = 0.84) are homogeneous while the hand-coded prevalence moves (0.176
  against 0.131, p = 0.048), asserted (`force.rates_homogeneous`,
  `force.prevalence_falls_in_audit`). The monitor's configuration states the model and the date it was
  trained, before the register opened, with no change inside the period.

**The noise, measured, because forcing on data too smooth or too noisy to separate is not forcing.**
Resampling the four cells of the worksheet 20,000 times: the answer's sampling standard deviation is
57.4 actions (12.7 per cent), the standard deviation of the gap between the two families is 50.2, and
the gap's mean is 136.8, so the separation is 2.73 standard deviations of its own sampling error and
the observed gap of 139.58 is 2.78 (`noise.gap_beats_sd`, `noise.gap_observed`). The stated
granularity of fifty actions is 0.87 of that standard deviation, so the bulletin states the indicator
no finer than the audit can carry it (`noise.grain_not_finer_than_sd`); a whole-number count would
have claimed 0.2 per cent precision on a figure whose own standard error is 12.7 per cent. The record
itself is not smoothed: daily action counts before the surge have a chi-square per degree of freedom
of 0.987 against a weekday mean and 2.094 unconditionally, which is the register's own working week,
and the daily count of marked actions is at 1.191 (`noise.dispersion_plausible`,
`noise.weekly_cycle_present`, `noise.dispersion_marked`).

**Robustness and fairness.** The truth behind the simulated record is 436 confrontational actions,
3.9 per cent below the estimate, so the estimator is fair as well as determinate; the generator
asserts the gap. The answer's raw figure sits 3.01 from the centre of its cell and 21.99 from the
nearest edge, and one more agreed-confrontational row in the worksheet moves it by about four actions,
so five such rows would be needed to reach a cell boundary (`bin.total`, `bin.total_mid`).

**Every graded figure off its rounding edge.** The call sits 21.99 of 25 from its nearest edge. The
seven euro totals are a per-report rate in cents times a count, so the generator's rates were moved
until each total sits at least 0.25 of a euro from its edge (850.90, 2,493.05, 1,548.00, 742.10,
558.90, 413.10 and 731.85): the schedule reads 6.35, 7.20, 6.90, 8.10 and 6.15 where it read 6.40,
7.25, 6.75, 8.15 and 6.40, and the July adenda raises P04 to 6.30 rather than 6.20. The three medians
are whole minutes and each route's two middle values are equal, so neither the rounding nor the
even-set convention can move them. The thirteen partner shares are exact ratios of two integers, so no
convention and no order of operations can move which side of an edge they fall: the generator asserts
that none of them is an exact x.x5 and that the tightest, Q9 at 23.3871 per cent, clears its edge by
0.0129 percentage points, with every other share at 0.0151 or more. All of it is asserted
(`bin.total`, `bin.cand.*`, `bin.euros.*`, `bin.share.*`, `bin.share_exact.*`, `bin.median.*`).

**The grid.** Two axes, how the reports are resolved and which measured quantity the count carries:

| | false marks out | labels as they stand | the audited shares | the two error rates | the recall only |
|---|---|---|---|---|---|
| the three routes resolved to actions | 250 | 350 | 600 | **450** | 650 |
| each accepted report counted as an action | higher in every column, asserted | | | the decisive column still the only one the protocol asks for | |

Every cell is a named figure. The decisive column is the only one that answers the protocol's
question, and it is the column least moved by a solver who fails to resolve the routes, because the
correction is a ratio of the worksheet's own cells and not of the record's volume.

**Dominance.** The ordinary actions outnumber the confrontational ones about nine to one, so the
classifier's one-in-forty false-mark rate puts 21 wrong marks in the worksheet against 76 misses: the
two errors are of the same order and neither cancels the other, which is what makes each easy route
land on a different wrong cell.

**Worth of each rung, on the graded quantity.** Rung 1 to rung 0 is two cells, rung 0 to rung 2 one,
rung 2 to the answer one, the answer to the default path three, and the default path to rung 4 one.
Nothing between the rungs is worth less than one cell of fifty actions, which is 11 per cent of the
answer, and every rung is satisfying to stop at: each is the whole output of a pipeline whose every
input figure is correct.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which actions are in the count | 3.2 files the period and 2.1 the action; asserted |
| 2 | Unit of account | the item, the report, the action | 2.1 files the action; asserted |
| 3 | Attribution window | which day an action falls on | the register's local action date, which no reception stamp overrides; SF7, asserted |
| 4 | As-of dating | the record at the extract | the manifest files 6 November 2026; SF14, asserted |
| 5 | Version basis | the reposted month and the superseded place names | the import log and the gazetteer; SF9, SF8, asserted |
| 6 | Denominator | none: the answer is a count | nothing to close, stated |
| 7 | Weighting | each round draws its batch at random from the reports entered since the previous close, so the batch carries no weights of its own | 4.5 states the draw and its window; asserted that every row is a press item and that two months and two themes have no row |
| 8 | Window length | the reporting period | 3.2; asserted |
| 9 | Boundary inclusivity | 1 May and 30 October | 3.2 states both inclusive; asserted that actions fall on both days |
| 10 | Rounding path | the count to the nearest fifty actions, rounded once at the end | 3.3 and SF11; asserted that the raw 453.01 is 21.99 from its cell edge |
| 11 | Tie-break | two candidates on one cell | none against the golden: 250, 350, 400, 450, 600 and 650, asserted |
| 12 | Maturity and censoring | reports still arriving | the period closed a week before the extract; asserted that no action dated in the period is reported after the extract |
| 13 | Order of operations | resolve the routes then read the codes, or read then resolve | C1: a duplicate report carries the same identifier, theme, locality and day, so either order gives the same actions, asserted |
| 14 | Row order | the item log's own order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the three routes, the two editions, the reposted month, the ingest counter's second count | C1 for the actions; the dictionary's load sentence and `convencoes` for the report counts, asserted |
| 16 | Identity normalisation | place names, partner delivery codes | the gazetteer's superseded names; the agreements' addendum of 8 September for the delivery codes; SF21, asserted |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | items, reports, actions, minutes, euros | the dictionary names each; the indicator reads actions only, asserted |
| 19 | Code and status semantics | the route codes, the action codes, the acceptance column, the worksheet's two coding columns and the desk's decision | the protocol and the dictionary; the codes are read correctly on every rung |
| 20 | Integerisation | the count to the nearest fifty actions | 3.3; the raw 453.013 rounds to 450, asserted |
| 21 | Clause scope | 2.1 per theme per locality per day; 2.6 per action; 4.5 per round | each paragraph states its scope; asserted |
| 22 | Forward window contents | none: the count is for the closed period | the call is retrospective with its reason, that the bulletin reports the period that closed and the trustees' vote of 19 November sets the next year's field budget on it |

## Literal reader

Executing the prompt, paragraphs 2.1 to 2.7, 3.2, 3.3, 3.4, 4.2, 4.5 and 4.6 of the protocol, the
agreements and their two addenda, the dictionary, the monitor's configuration, the gazetteer and the
manifest word for word selects the accepted reports of the three routes between 1 May and 6 November
2026, resolves them to actions at gazetteer settlements on the protocol's grain, keeps the actions
dated inside the reporting period, and asks how many of them were confrontational actions on 2.2's
list, the count being of the actions and not of the codes the classifier assigned, to the nearest
fifty. The text is silent on how the classifier's labels become that count, so every option was
computed on the same rows: the codes as filed give 350, the codes with the false marks out 250, the
hand codes where the desk audited with the classifier's elsewhere 400, the audited reports' own
confrontational shares carried onto the record 600, the coded count scaled by the recall 650, and the
count rebuilt from the classifier's two measured error rates 450, which the worksheet's own four cells
fix. Every stratified variant of any of them has no rate for September, October, `ENE` or `FLO` and is
not computable. The easy routes are easy estimators of the same literal estimand, not other readings
of it, and every other term and convention has an SF row ruled out by a quoted sentence or asserted to
give the same call.

## Oracles

- `amostra_dupla_codificacao.csv`, the coding desk's own worksheet, carries two codings per row and no
  rate, no count and no method; it is the raw material the decisive step reads and it ties under every
  rung, because each rung reads a different pair of its four cells.
- The earlier monthly bulletins report actions recorded and territory touched and never confrontational
  actions, so they tie under every rung. Their September note records that two dispute themes opened
  with the autumn wave, which is a fact about the register and not about any count.
- `registo_importacoes.csv` confirms which month was loaded twice; it ties under every rung and the
  count is asserted invariant to the resolution.
- `gazeteiro_localidades.csv` confirms the settlements, their municipalities and their districts; it
  ties under every rung.
- `totais_por_via.csv` is the ingest counter and `excecoes_geocodificacao.csv` the reports the
  association could not place; neither carries an action code and both tie under every rung. The
  counter counts each arrival, so it over-counts the partner route by the reposted load, which the
  import log and the dictionary close.
- `config_monitor.json` states the classifier's model, the date it was trained and that it did not
  change inside the period, and the offsets of each district's clock; it carries no rate and no count
  and ties under every rung.
- `manifesto_extracao.csv` states each file's rows, range and extract date and settles the one designed
  disagreement in the ask layer without naming a level.
- No control, published figure or corpus states a confrontational count, a rate or an error rate.

## Leak sweep answers

`leak.py task192 --asof 2026-11-06` returns REVIEW on five lines and no LEAK: three figure
collisions, the notifications distractor's planned dates and the manifest cell derived from them, plus
one INFO on container metadata. Each is answered here.

- **`boletins_anteriores_2026.pdf`, the integers 118 and 119.** The earlier bulletins print one row per
  month from May to September with the actions recorded, the municipalities touched and the localities
  touched (592 / 118 / 349 for May, and so on). The collision is on a municipality count in a
  different cut: the graded fortnight rows Q11, Q12 and Q13 touch 118, 119 and 119 municipalities, and
  a count of municipalities is bounded by the 119 the gazetteer carries, so a monthly figure and a
  fortnight's figure land on the same number without either being the other. No monthly row is graded,
  no fortnight row is recoverable from a monthly one, and the file states nothing about confrontational
  actions: the note under its table says the confrontation indicators belong to the period bulletin
  and go to the trustees in November. Under every rung the file ties.
- **`relatorios_mensais_parceiros_2026.pdf`, the integer 103.** That is one partner's own declared
  deliveries for September, and it collides with the 103 municipalities the graded fortnights Q4 and Q6
  touch. The two are counts of different things in different files at the same order of magnitude; the
  partner table carries no municipality and no action, and the monthly returns are read only by the
  partner ask, where they reconcile to the delivery counts rather than to any territory figure.
- **`notificacoes_reuniao_publica.csv`, dates after 6 November.** The column is `data_prevista`, the
  day a gathering is *planned* for, on notifications lodged with the councils before the extract. A
  notification for later in November filed in October is exactly what the councils hold on 6 November,
  and a register of planned gatherings with nothing beyond the extract date would be the unrealistic
  artifact. The file is a declared distractor: a notification is a declared intention, not an action
  the register recorded, so it enters no graded figure.
- **`manifesto_extracao.csv`, a date after the extract.** That is the `ultimo_registo` cell of the
  notifications row, the latest `data_prevista` in the file it describes. The manifest states each
  file's rows and date range, so the cell is derived from the distractor above and carries nothing
  further.
- **Container metadata, no writer signature.** The two goldens and the pack's documents are written by
  reportlab and openpyxl through `postprocess`, which strips the producer, the creation trail and the
  OOXML core properties, so the audit finds no signature to report. That is the intended state.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per fortnight, the actions recorded, the municipalities touched and the share of those actions the partner network reported | 3 per fortnight, 13 fortnights | the construction's own output on the segment the trustees want anyway, the actions the count is taken from | the bulletin's standing table | D6 grain: the share is the part of the fortnight's actions the network reported, not the part of the fortnight's reports the network filed, which moves nine of the thirteen rows and the last one by 6.5 points | D1 the re-imported month doubles reports and no actions; D5 scope: the last fortnight has fifteen days, so a solver who stops the thirteenth at 29 October loses 52 actions | item log, partner reports, public line, gazetteer, protocol, dictionary, manifest, import log; 12 columns | 4 stops, lazy delta 11 of 13 fortnights | the bulletin's own standing table |
| A2 per access route, the reports received, those the association could not place and the median minutes from the action to the report | 3 per route, 3 routes | the audit trail from an input the call consumes, through rows it never reads, to the route's own control total | the pipeline review the data manager runs each period | D4 absence as the signal: the reports that could not be placed are held in a separate exceptions file no habitual join reaches, and the ingest counter counts the reposted load's second arrival again | D8 the reception stamps are UTC, the action times are the local clock of the action's district, the clocks go back on 25 October and the Azores run an hour behind; D6 a press report entered the monitor with the first of its items | exceptions file, ingest counter, item log, partner reports, public line, monitor configuration, gazetteer, dictionary, manifest; 12 columns | 5 stops, lazy delta 3 of 3 routes | an ingest pipeline's own period review |
| A3 per partner organisation, the reports it filed on actions in the period, those filed after the period closed and the euros paid under its data agreement | 3 per partner, 7 partners | an input reconciled to another system's total, the gap made of devices | the finance office settles the data agreements | D2 version: one agreement was amended mid-period and the rate paid is the amended one, which the superseded schedule does not carry | D7 one partner's deliveries change code after a merger, under a second addendum; D8 the delivery stamp is UTC against the period close; D1 the reposted load is paid once | partner monthly tables in PDF, agreement schedule, two addenda, ingest counter, manifest, dictionary; 13 columns | 5 stops, lazy delta 4 of 7 partners | the finance office's quarterly settlement |

**The main population's zero counts.** Zero device rows and zero hazard rows in the actions and
episodes the share rests on: every device sits in the exceptions file, the ingest counter, the
agreement schedule, the addenda or the partner monthly tables, none of which carries an action.
Deleting every device leaves the share exactly as hard, asserted by count.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D8 the clocks: UTC against the district's local time, the 25 October change and the Azores hour | A2, A3 | A2 one route's median by 56 minutes and another by one; A3 the late-filing counts |
| D6 grain | A1, A2 | A1 the partner share in nine fortnights; A2 one route's median by 12 minutes |
| D1 the re-imported month | A2, A3 | A2 the partner route's received count by 126; A3 the euros of every partner |
| D5 scope | A1 | the thirteenth fortnight's three figures |
| D7 the second delivery code | A3 | one partner's filings by 28 and its euros by 166 |

**The referee.** `manifesto_extracao.csv` states each file's rows, range and extract date and settles
the one designed disagreement, the exceptions file's extent, without naming a level.

**The cracker sheet.** The cracker filed 450 confrontational actions, ran the hygiene battery,
executed every filed paragraph and matched every control total.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 share the partner network reported, fortnight 13 | counts reports, not actions | 18.9 per cent | 25.4 per cent | miss |
| A1 share the partner network reported, fortnight 9 | counts reports, not actions | 26.9 per cent | 23.4 per cent | miss |
| A2 reports received, the partner network | sums the ingest counter, which counts the reposted load again | 1,330 | 1,204 | miss |
| A2 reports that could not be placed, the press monitor | the item log alone, which holds only the items it placed | 0 | 148 | miss |
| A2 median minutes from the action to the report, the press monitor | reads the monitor's reception stamp as local time | 59.0 | 115.0 | miss |
| A2 median minutes, the press monitor, every item | takes every item of a report rather than the first | 127.0 | 115.0 | miss |
| A3 euros paid, the amended partner | the schedule's rate for the whole period, without the July adenda | 676 | 742 | miss |
| A3 reports filed, the merged partner | one delivery code, without the September addendum | 92 | 120 | miss |
| A3 reports filed, all seven partners | every row of the partner file rather than the period's actions | 1,250 | 1,154 | miss |

**Pair ceiling:** 39.0
**Mirror leakage:** 20.0

## Tried and rejected

- The seed's own architecture, a filed definition of a campaign plus a verification subsample that
  blesses one reading of it: the definition makes the count rule application and the subsample is a
  certified replay, both of which the client's rules ban as the decisive step. Re-rooted at the draw.
- Recovering the number of operations from a periodogram of the daily action counts: the number of
  peaks depends on the window, the detrending and the significance threshold, so the count would not
  be determinate. Replaced by the intervals read off the locations each operation alone touches, which
  needs no threshold.
- Letting the institute's flag file group the location-days into episodes: that ships an artifact that
  answers the decision question wrongly, which Gate G forbids. The flag file flags days and groups
  nothing.
- (architecture 2) A confrontation risk filed with an eight-week horizon from each episode's opening,
  the cohort the episodes opened in a window that ends a week before the extract: measured on the
  model, the complete-case share over the episodes with a full eight weeks of follow-up is an unbiased
  estimate of the same quantity and lands within a point of the golden, so the easy route reaches the
  answer. Replaced by the whole-life estimand.
- (architecture 2) Grading the share to one decimal: the weekly and fortnightly readings of the
  decisive estimate give 17.05 and 16.99 against the daily 17.03, which a one-decimal figure splits.
- (architecture 2) A ranked watch list of the live episodes by remaining confrontation risk: the
  remaining risk is a monotone function of an episode's age alone, so the ranking degenerates.
- (architecture 2) The whole competing-exit architecture, designed, built and gated: on the remote
  merge of 2026-10-17 task266 arrived with the same mechanism in other nouns, and task157 arrived with
  the same gap, decisive pattern and decision type while task190 v2 took the stakeholder role.
  Re-rooted at the draw rather than shipped into a clone finding.
- (architecture 3) Correcting the count by the classifier's precision alone, or by its recall alone:
  each carries one of the two measured error rates and lands two cells away, which is why both are
  rungs rather than the answer.
- (architecture 3) A double-coding sample that verifies every classifier positive and a sample of its
  negatives, which is what a real quality desk draws: it makes the predictive values the design-exact
  quantities and the sensitivity the derived one, which inverts the decisive step and leaves the
  weighting of the two strata arguable, so each round draws at random from the reports entered since
  the previous close and 4.5 says so.
- Dating the desk's hand coding forward from each round, the round day plus nought to eight days: the
  November round then codes reports after the 6 November extract, which the leak sweep caught.
  Replaced by the desk's own working calendar before each round's close, with the batch worked in the
  order the reports arrived.
- Partner rates of 5.25 and 6.15 euros for the amended agreement: the paid reports came to exactly
  892.50 euros, so a solver rounding half up and one rounding half to even would file different euros.
  Replaced by rates that land every total at least a quarter of a euro from its edge.
- **(architecture 3, the stage-4 determinism finding of 2026-10-17) A correction forced by nothing but
  the shape of the record, with a flat confrontational rate and a validation sample spread over the
  whole period.** The judge found eight routes standing between 226 and 237 on a golden of 234: a
  pooled predictive-value correction, its month-, theme- and round-stratified variants, the sample
  prevalence, a continuity adjustment, the hand-code-where-sampled route and the pooled Rogan-Gladen
  the golden used. Measured, the two families differ by less than their own sampling error (the gap's
  mean was 7 against a standard deviation of 24) because the two are algebraically the same quantity
  when the validation sample is representative of the population it corrects, and that sample's
  coverage varied while its prevalence did not (p = 0.81 across months). Nothing in the record could
  pick one. Re-rooted inside the architecture, not away from it: the audit's window now stops before
  the autumn surge, the confrontational share falls fourfold across the period, and the two families
  are 30.8 per cent apart at 2.78 standard deviations of the gap's own sampling error.
- **(architecture 3) Keeping the validation sample at 2,600 rows over 59.7 per cent of the period's
  accepted reports.** The reader's verdict was that no desk produces that file in that shape, and the
  arithmetic agrees: at the audited batch's size the stratified variants of the right family sit
  within a per cent of the pooled one, so they cannot be told from it, and the hand-code-where-sampled
  route closes to within 6 per cent of the answer. Measured over the repaired design, the audit has to
  sit between about 900 and about 1,350 rows: below 900 the theme-stratified route with a pooled
  fallback leaves the answer's cell, above about 1,400 the hand-code-where-audited route comes inside
  6 per cent of it. Built at 1,000 rows in two rounds, 23.8 per cent of the period's accepted press
  reports and about 500 a round, which is what the reader put a real desk's own output at.
- **(architecture 3) Grading the count as a whole number.** The audit's four cells carry a sampling
  standard deviation of 57.4 actions on the answer, so a whole number claims 0.2 per cent precision on
  a figure whose own standard error is 12.7 per cent, which is the arithmetic task190 paid for.
  Replaced by the nearest fifty actions, 0.87 of that standard deviation, with every candidate route's
  cell asserted.
- **(architecture 3) Cutting the audit to a few per cent of the record.** Measured rather than argued:
  the answer's relative sampling error is about 1.5 over the square root of the hand-coded
  confrontational reports, and that count is the audit's row count times the audited prevalence, so an
  audit of a few per cent of 4,200 press-reported actions would hold about a dozen such rows and carry
  a standard error near 30 per cent, at which no granularity separates the two families and no cell
  holds the right one. The record's volume cannot be raised to buy the coverage back without putting
  more than fifty contentious actions a day into a country of ten million. The audit is therefore
  sized by what it has to measure, 1,000 rows, and the coverage that follows, 23.8 per cent, is
  reported rather than disguised.
- (architecture 3) A single nine-day burst per round with four coders at equal loads and no second
  codings: the reader read it as a file built to be read by an analyst. Replaced by the desk's own
  working calendar, 65 coding days at loads from 1 to 41, unequal coder loads of 345, 290, 212 and
  153, 78 rows sent to a second coder with the desk's decision recorded on each, and 49 coding notes.
- (architecture 3) A classifier that relabels at random: the reader measured its agreement with the
  hand code at 21.8 per cent against 19.8 expected by chance, which reads as noise rather than an
  instrument. Replaced by a confusion matrix over the protocol's eight codes with a strong diagonal
  and neighbour confusion, which agrees with the hand code on 64.2 per cent of the worksheet's rows
  and confuses a code with a neighbour more often than with a distant one, both asserted.
- (architecture 3) Action start times on the quarter hour between 08:00 and 19:59 with nothing over
  lunch, no weekday to weekend difference, partner deliveries flat across the 24 hours and line lags
  bounded at 42 to 206 minutes: every one of them a tell the reader read off the pack in one pass.
  Replaced by start times from 07:00 to 21:59 with 82 per cent of minutes on a multiple of five, a
  working week in the daily counts, partner deliveries inside each organisation's working day, and
  lognormal lags, all asserted.
- (architecture 3) Three Azores municipalities in the gazetteer's "Ilhas" district beside the Madeira
  ones, with the clock offsets in no shipped file: a geography error of the pack's own making that
  left the medians open four ways. The gazetteer now carries "Acores" and "Madeira" as separate
  districts and the monitor's configuration states each one's offset and the 25 October change, which
  closes the medians and leaves the Azores hour as a device in A2 rather than an accident.

## Architecture 2, blocked at the draw by the remote merge

Architecture 2 asked what share of the register's dispute episodes would have recorded a
confrontational action by the time they closed, with a quiet close treated as the other way an episode
ends rather than as an observation that stopped. It was drawn, designed, built and gated: 635 episodes
in the cohort, 89 with a confrontational action at the extract, 312 closed quietly, 234 still open,
and 108 episodes, 17 per cent, on the decisive estimate, against 89 on the recorded count, 141 on the
known outcomes and 178 on a product-limit survival. The pack carried 17 files in four formats and a
25,688-row item log, with 108 generator assertions, 99 independent checks in a verifier that read only
the bundle, two byte-identical rebuilds, `figures_check.py` exit 0 and `precut.py` at 0 FAIL and 0
WARN.

It is spent for one reason outside the build. The remote merge of 2026-10-17 brought in task266,
drawn the same day in sociology-demography, whose driver is that mechanism in other nouns, and the
clone check reads mechanisms rather than nouns; the same merge brought in task157, which took the
structural triple, and task190 v2, which took the stakeholder role. Competing risks against censoring
is therefore on this slot's banned list with the rest.

What architecture 3 keeps: the world, the three access routes, the settlement gazetteer, the partner
organisations and their agreements, the ask layer with its devices, and every pack writer that is not
about the decisive quantity. What it discards: the episode construction and its peace interval, the
whole-life cohort estimand, the four survival estimators, the ladder, the prompt, the goldens and the
submission. Its pack, zip, goldens, submission and metadata were removed from the task tree when the
draw was blocked, so that nothing a consumer discovers by name can be graded as this build's
(`reduce-house-fixes` H11); the architecture is on the slot's banned list and will not be rebuilt.

## Architecture 1, spent at stage 3 on measurement

The generator was written far enough to measure the ladder on the record itself, before any file was
cut. Two findings kill the architecture, and neither is a tuning problem.

**1. The default path has no parameter-free answer, and its parameter range covers the golden.**
"Group the flagged location-days that touch in time and place" is a single-linkage clustering, and its
one free parameter is the gap in days it tolerates. Measured on the record (748 location-days, nine
operations, reach 0.70):

| Gap tolerated | Components, no same-day link | Components, same-day link |
|---|---|---|
| 1 day | 673 | 65 |
| 2 days | 598 | 22 |
| 3 days | 562 | **9** |
| 5 days | 310 | 1 |

The count falls monotonically from 673 to 1 and passes through 9, so a solver who tunes the gap to a
sensible-looking cluster count can land the answer without the insight, and no parameter-free reading
of "contiguous" lands on a plausible count: the two parameter-free readings give 65 and 673, which
nobody files as a count of coordinated operations. The design note's 23 was never reproducible. A
ladder whose rung 0 is one live degree of freedom in the graded quantity holds nothing
(`stumping` Part 3), and the sweep over flag rules (seven variants, 196 to 602 flagged cells) moved
the component counts by two or three and never separated them from 9.

**2. The decisive quantity is not one the field estimates, so rule 1 fails on measurement.** The step
is recovering the number of arithmetic progressions in a union of them: per-settlement gcds of the
observed gaps return exactly `[4, 5, 6, 9, 11, 13, 17, 23, 29]` on the 20 settlements one operation
reaches, and nine distinct interval-and-phase pairs. That is signal processing, not conflict event
analysis: no monitoring institute estimates how many periodic processes generated its record, and the
swap reads unchanged with machines on fixed maintenance cycles in place of coordinated operations.
Exact lattices over six months is also the kind of structure a realism read calls constructed.

The architecture is spent. Re-root at stage 1 in the same number and objective. The world (a
Portuguese conflict monitoring institute, three access routes, a settlement gazetteer, partner
organisations under data agreements) is sound and can be kept; the decisive step cannot.

**Ruled out for the re-root, with the reason, so the new draw does not walk into one:**
- capture of one list measured on the overlap with another: task448's driver, spent;
- the selected extreme judged against the record of extremes at the same reach: task191, one build ago;
- a shared external driver with unit-specific lagged response: task182;
- composition against rate: task183, task125, task188;
- a count read before its records have arrived: task190, task457;
- an event entering the record only above a detection threshold that moves on a cycle: task180.

**How architecture 3 clears each of them.** The decisive step is none of the six: nothing is captured
from an overlap (the duplicate reports collapse to one action and the count is invariant to them,
asserted); nothing extreme is selected and no null of extremes is built; no external driver and no lag
appear; the count is a count with no composition against any rate, and although the record's own
composition moves across the period that movement is what rules a method out rather than the quantity
being compared; every report has arrived, the import log closes the one month that arrived twice, and
the gap is in what the classifier made of the reports rather than in the recording; and no detection
threshold exists, the action grain being filed and every accepted item carried.
