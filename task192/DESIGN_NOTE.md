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
that doubles the record's volume from 5 September has no hand-coded report in it at all, and the
classifier's own marked rate falls from 8.8 per cent inside that window to 4.3 per cent outside it,
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
   share that the coding desk found was really confrontational: of the reports it marked, 81 per cent
   were; of the reports it did not, 9 per cent were.
5. Carry those two shares onto the register's 4,228 press-reported actions and add the 49 an
   organisation or the public line coded by hand, then round to the nearest fifty.

**Ends on:** 600 confrontational actions.
**Golden:** 450 confrontational actions.

## Stump sentence

A competent solver resolves the three routes, builds the actions on the protocol's grain, reads 3.3,
corrects the classifier's labels with the shares the hand coding found on each side of them and files
**600 confrontational actions**, because those two shares were measured on the opening of the period,
where about one audited report in seven was confrontational, and are carried onto a period in which
about one action in ten was.

## Three rules

**The stage-2 re-measurement of 2026-10-21 refused this architecture, and these lines are written to
what it measured rather than to the gate.** The three screens, their harness and their numbers are in
`## Tried and rejected` under that date. Two lines below now record a failure, `Not rule application:`
and `Analyst test:`; the other eleven hold unchanged, and nothing in the call, the decisive step, the
prompt or any graded figure was moved in writing them.

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
  two language editions of one media group; one month of partner reports was loaded twice, the import
  log carries both loads, the portal stamped the second load's rows on the day it arrived and the
  ingest counter counted that arrival again; the monitor's collection and the public line run on the
  association's intake hours and write what lands at night at the next intake; the monitor's reception
  stamps and the partner portal's are UTC while the action times are the local clock of the action's
  own district, the clocks go back an hour on 25 October and the Azores run an hour behind the
  mainland; the partner organisations' monthly returns arrive inside a PDF; one partner's deliveries
  change code after a merger; the gazetteer carries superseded settlement names; and eight of the
  desk's own worksheet rows carry no manual code because the desk could not fix one. None of it is
  placed to be caught and none of it decides the count.
- **Layer 2:** `field_method`. The methodological choice is which of the quantities the hand coding
  measures can be carried to a period the hand coding never reached. Measured, the data does not
  leave that choice open: once the record's own marked rate is read against the worksheet's own
  marked rate, every construction the data leaves standing files one printed call. See
  `Not rule application:`.
- **Decisive step:** rebuild the count of confrontational actions among the actions the press monitor
  carries from the classifier's measured sensitivity and false-mark rate, which are properties of the
  coder and do not depend on how confrontational the audited weeks happened to be, rather than from
  the audited reports' own confrontational shares, which do; then add the actions a filer coded. It
  is the field's own step and it is a reflex once two group-bys are run: the record marks 6.4096 per
  cent of its 4,228 press-reported actions and the worksheet marks 8.9962 per cent of its 1,056 coded
  rows, a two-proportion z of 2.961 at p = 3.064e-03, and across the audit's own window boundary
  8.7923 against 4.3130 per cent, z 5.934 at p = 2.962e-09.
- **Not semantics:** every field, code, zone, offset and place name read correctly still leaves the
  default path carrying the audited batch's own shares onto the record and filing 600. The dictionary
  gives every field, the protocol defines the action grain and lists the confrontational codes, the
  monitor's configuration gives the offsets and the rounding is filed. Reading all of it right is what
  produces the 600.
- **Not rule application: FAILS, MEASURED.** The first half of the line is still true and is worth
  nothing on its own: the protocol files the action grain, the confrontational codes, the reporting
  period, which route's code the register keeps, that the count is of the actions and not of the
  codes, the granularity, and what each round of hand coding drew its batch from, and no shipped
  sentence says how the classifier's labels are to be turned into the count, nothing naming
  sensitivity, specificity, recall, precision, a correction, a false positive, a false negative,
  representativeness or extrapolation, with the word sweep over every shipped file still asserting
  it. What the line owes is the other half, the spread of the family the rule leaves open once every
  filed rule **and the data** are read, and that spread is one call. The family that differs in what
  it does spreads 458.642 actions over seven printed calls (250, 300, 400, 450, 500, 600, 700); the
  family the data leaves standing, the nine constructions built on the classifier's two measured
  error rates, spreads 34.049 actions, 0.68 of a printed unit, and files **one** printed call, 450.
  What rules the other families out is not an argument a solver can miss, it is two one-line
  aggregations that print 0.064096 against 0.089962, and the ladder's whole 159.6192-action reach is
  that same difference times a constant of the worksheet's four cells, by identity and not by
  correlation: PV - RG = N (p - p_a) [(PPV - (1 - NPV)) - 1/(r - f)], residual at or below 1.3e-13 at
  every seed tested. So nothing is left to decide once the data is read, and the step both matters
  and is determinate only because the record announces it, which is readability tests 2 and 3 rather
  than test 1.
- **Analyst test: FAILS AS WRITTEN.** It says a strong analyst who resolves the three routes and the
  two editions, drops the reposted month, resolves the superseded place names, applies every filed
  paragraph and corrects the classifier's labels with the shares the hand coding found on each side
  of them files **600 confrontational actions** (614.53 raw), the default path's `Ends on:`, where the
  period's record gives 450 (454.91 raw). `checks.py` still executes that on the clean truth and it is
  still true of an analyst who does not compare the two marked rates. Measured, that is not the
  analyst the bar is set against: the wave-8 audit reader, cold on the shipped pack, landed the call
  1 of 1 and said in terms that nothing in the files named the step and that it had inferred the step
  from the data, giving the right reason for it. The easy route is available only to an analyst who
  skips the first hygiene check anyone runs on a validation sample, whether the sample covers the
  population it is being carried to, and the record answers that check at p = 2.962e-09.
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
  wrong by a third. No build on file teaches it. The re-measurement adds the lesson that refuses the
  build: on this shape the forcing Gate C requires and the reach Gate F pays are one number, so there
  is no setting of the world at which the correction both matters and is not announced by the record.
  Over the sweep of the composition drop and the surge volume, 300 distinct settings at twenty
  action seeds each, 22 draws deliver a printed cell of reach with the window comparison
  insignificant and the licensed family is unanimous in none of those 22; the family is unanimous
  in 9 of the 300 and every one of those nine has the comparison significant below 0.05. Not one
  draw in the sweep delivers reach, a unanimous licensed family, the 1.15x floor on the nearest
  wrong rung and a mid-bin call at the same time.

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
structure separates them: the audit covers four of the period's six months, two of the protocol's ten
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
| 5 the count rebuilt from the classifier's sensitivity and false-mark rate, which do not move with the audited window's composition (decisive) | no shipped sentence names sensitivity, specificity, recall, precision, a correction, a false positive, a false negative, representativeness or extrapolation, asserted by a word sweep over every shipped file; 3.3 says only that the count is of the actions and not of the codes, and 4.5 says only what each round drew its batch from | no column holds an error rate, a weight or a stratum: the worksheet is two codings, a coder, a coding date, a round, the desk's decision and a margin note | no reflex: the two reflexes above each carry a quantity measured on the audited weeks and file a different number, and the reflex that trusts the hand codes where they exist files a third | nothing scores a count; the earlier bulletins report actions and territory, never confrontational actions | the battery finds the two editions, the reposted month, the ingest counter and the clocks and leaves the count open | no: the six candidate cells are 250, 300, 400, 450, 600 and 700 from the same rows, and the step is a two-rate algebra | silent |

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
| SF11 | rounding | the count to the nearest fifty actions, rounded once at the end | the count as a whole number | `same call`, asserted: the estimate is 454.91 and 450 is the nearest fifty either way |
| SF12 | ties | none against the golden: the six candidate cells are 250, 300, 400, 450, 600 and 700, and the two readings of rung 1 share one of them as the default path shares its cell with rung 4a | two candidates on the golden's cell | `same call`, asserted that no wrong route lands in the golden's cell |
| SF13 | the accepted items | the items the press monitor accepted, which the register carries | every matched item, rejected ones included | rejected items are not actions | 4.2 quoted and the dictionary's acceptance column; asserted |
| SF14 | the extract | the record as extracted on 6 November 2026 | the record as at the period's close | `same call`, asserted: no action dated inside the period is reported after the extract |
| SF15 | actions outside the period | excluded from the count | included because their reports arrived inside it | the count changes | 3.2 quoted, which fixes the period on the action's date; asserted |
| SF16 | the hand coding | the standard the desk measures the classifier against, after the desk's decision on a second coding, on every row the desk could fix a code for | one more opinion to be averaged with the classifier's | the measured rates change | 4.5 quoted and the dictionary's `codigo_manual` line; asserted |
| SF17 | a report the gazetteer does not place | not an action, so outside every count | an action at an unknown locality | the count changes | 2.5 quoted; asserted |
| SF18 | the register's opening | 1 May 2026, with no action carried in | an action before the register opened | nothing to count before it | 3.2 quoted; asserted that no action predates 1 May 2026 |
| SF19 | a fortnight | fourteen days from 1 May | fifteen-day blocks, or a fourteenth one-day row | the fortnight rows change, the count does not | 3.4 quoted, which gives the length in days; asserted |
| SF20 | the days left at the end of the period | into the last fortnight, which has fifteen days | a fourteenth fortnight of one day | the last fortnight's figures change | 3.4 quoted and the `convencoes` sheet; asserted |
| SF21 | a partner's delivery codes | the codes of one agreement count together | each delivery code is its own organisation | one partner's filings and euros change | the agreements' addendum of 8 September and the `convencoes` sheet; asserted that both codes are in the file |
| SF22 | a district's clock | the offset the monitor's configuration gives the district, the Azores an hour behind | the mainland clock everywhere | one route's median moves by a minute | `config_monitor.json` quoted and the gazetteer's district column; asserted that the two island districts are separate |
| SF23 | the reception moment of a press report | the first of its items, the dictionary's sentence | the last item, or every item | one route's median changes | the dictionary's `carimbo_recepcao` line; asserted |
| SF24 | an Azores action | an action in the Azores district, on the Azores clock | none in the record | the median would not move | asserted that the record holds actions in the Azores district |
| SF25 | an action a route reported | an action that route delivered a report of, however many other routes also did | an action only that route reported | the fortnight's partner count falls by three quarters | the `convencoes` sheet quoted; asserted that the two readings give different counts |
| SF26 | the period the route table counts over | the reports each route received between 1 May and 30 October | every report in the file, which runs to the 6 November extract, or the reports of actions dated in the period | the received and unplaced counts and the partner route's median all move | the `convencoes` sheet's `relatos recebidos no periodo` row; asserted that the pinned window gives the golden, that both alternatives give different triples, and that the triple survives every receipt zone in the pack

| SF27 | a report the desk could not code | carries no manual code, so it compares nothing and no cell holds it, the dictionary's `codigo_manual` line and 4.5's "onde a mesa o conseguiu fixar" | the empty code read as an ordinary code, which puts the row in the false-mark cell or the agreed-ordinary cell | `same call`, asserted: the eight rows read as ordinary codings give 447.14 against 454.91, the same cell and 22.1 from its nearest edge |
| SF28 | the delivery moment of a report the network sent twice | the first load's stamp: the portal stamped the reposted rows on 14 September, the day the import log says that load arrived, and the dictionary's `carimbo_entrega_utc` line makes the delivery the first load's | the second load's stamp, which the portal wrote when the file came back | the partner route's median minutes move from 1,385 to 1,450 and its received count is unchanged | the dictionary's two lines quoted; asserted that the reposted rows carry the arrival day, that the golden reads the first load and that the other reading moves the median |

## Ladder

| Rung | The estimate | Raw | To the nearest fifty |
|---|---|---|---|
| 1 | the coded count with the classifier's false marks taken out | 234.97 to 268.65 | 250 |
| 0 | the actions the register carries under the confrontational codes | 320.00 | 300 |
| 2 | the hand codes where the desk audited and the classifier's code elsewhere | 386.00 | 400 |
| 5 | **answer:** the count rebuilt from the classifier's two measured error rates | **454.91** | **450** |
| 3 | **default:** the audited reports' own confrontational shares carried onto the record | 614.53 | 600 |
| 4a | the coded count scaled by the classifier's recall | 615.64 | 600 |
| 4b | the audited prevalence over the press-reported actions | 693.61 | 700 |

Measured on the cut pack, not on a model: the register holds 4,656 actions in the reporting period,
of which 4,228 carry a press monitor report and take its classifier's code and 428 reach the register
only through a partner organisation or the public line and take the filer's. The register carries a
confrontational code on 271 of the first group and 49 of the second. The coding desk's two rounds drew
1,064 of the monitor's reports, 25.2 per cent of the 4,228 the period holds, coded 1,056 of them and
returned 77 agreed confrontational, 84 the classifier missed, 18 it marked wrongly and 877 agreed
ordinary, which is a recall of 0.4783 and a false-mark rate of 0.0201. The answer's raw figure is
454.911 actions.

**Separation.** 250, 300, 400, 450, 600 and 700 are six distinct cells of the stated granularity, and
the two readings of rung 4 fall in two of them. The nearest wrong figure to the answer is 386.00, 15.1
per cent away, and the nearest wrong cell is 400, one cell away; the default path's 614.53 is 35.1 per
cent away. Every candidate is the complete output of a competent pipeline on the same rows, and the
answer is fourth of the six cells and bracketed, so no solver reaches it by stopping early and none by
correcting hardest.

**The candidate set, measured over the judge's own list.** Every route the record leaves standing was
computed on the shipped bundle and asserted in `checks.py` by name (`cand.*`):

| Route | Figure | Cell | Distance from the answer |
|---|---|---|---|
| the false marks taken out on the false-mark rate | 234.97 | 250 | -48.3 per cent |
| the false marks taken out on precision | 268.65 | 250 | -40.9 per cent |
| the codes as the register carries them | 320.00 | 300 | -29.7 per cent |
| the hand codes where audited, the classifier's elsewhere | 386.00 | 400 | -15.1 per cent |
| the two error rates by month, leaving the unaudited months coded | 432.70 | 450 | -4.9 per cent |
| the two error rates by month, pooled where a month has no audited row | 448.70 | 450 | -1.4 per cent |
| a continuity adjustment of half a case in each cell | 450.32 | 450 | -1.0 per cent |
| the two error rates from the first round's cells alone | 450.21 | 450 | -1.0 per cent |
| **the two error rates (the answer)** | **454.91** | **450** | - |
| the same correction as the inverted confusion matrix | 454.91 | 450 | identical by construction, asserted to 1e-9 |
| the audited rows taken as known and the rest corrected | 454.91 | 450 | identical by construction, asserted to 1e-9 |
| the two error rates from the second round's cells alone | 464.98 | 450 | +2.2 per cent |
| the two error rates by theme, pooled where a theme has no audited row | 466.08 | 450 | +2.5 per cent |
| the two error rates by theme, leaving the unaudited themes coded | 466.75 | 450 | +2.6 per cent |
| the audited shares by month, pooled where a month has none | 590.37 | 600 | +29.8 per cent |
| the audited shares on each side of the label | 614.53 | 600 | +35.1 per cent |
| the audited shares by theme, pooled where a theme has none | 615.79 | 600 | +35.4 per cent |
| the coded count scaled by the recall | 615.64 | 600 | +35.3 per cent |
| the audited prevalence over the press-reported actions | 693.61 | 700 | +52.5 per cent |
| the two error rates by month, with no pooling | not computable | - | September and October hold no audited report |
| the two error rates by theme, with no pooling | not computable | - | `ENE` and `FLO` hold no audited report |
| the audited shares by month or by theme, with no pooling | not computable | - | the same two gaps |
| the two error rates by round, with population weights | not computable | - | neither round's window covers the autumn |

Every route built on the classifier's two error rates lands in the answer's cell, each of them at
least 7.7 actions from its edge, including either round's cells taken alone and either way of
patching a stratum the audit never reached; every route built on the audited batch's own
confrontational shares lands three cells away; and every stratified route that refuses to patch has
no rate for part of the population it is applied to, because the audit never reached September or
October and the two dispute themes that opened with the autumn wave have no audited report at all.

**What makes it forced, measured and not narrated.**
- The audit covers months 5 to 8 of the period's 5 to 10, asserted (`dead.audit_window`,
  `dead.population_wider`).
- `ENE` and `FLO`, two of the protocol's ten dispute themes, first appear on 5 September and hold no
  audited report, with 393 and 403 actions each, asserted (`dead.theme_reason`,
  `dead.late_themes_after_surge`, `dead.late_themes_present`).
- The record's own marked rate is 8.79 per cent on the 1,979 press-reported actions inside the audited
  window and 4.31 per cent on the 2,249 outside it, chi-square p = 3.0e-09, asserted
  (`force.marked_rate_moves`). Month by month it runs 9.25, 9.24, 9.02, 7.66, 4.86, 3.78.
- The audit's own hand-coded prevalence is 15.25 per cent against the record's 9.77 per cent, a factor
  of 1.56, asserted (`force.audit_prevalence_above_record`), and inside the audit it falls across the
  window, 16.16, 17.70, 14.92 and 6.54 per cent by month (`force.audit_prevalence_trend`).
- Across the two rounds the classifier's recall (0.511 against 0.438, p = 0.36) and its false-mark
  rate (0.0172 against 0.0233, p = 0.52) are homogeneous, and so is the hand-coded prevalence (0.159
  against 0.145, p = 0.53), asserted (`force.rates_homogeneous`, `force.prevalence_falls_in_audit`).
  The monitor's configuration states the model and the date it was trained, before the register
  opened, with no change inside the period.
- **The two rounds agree closely enough that either one alone lands in the call's cell**, 450.21 from
  the first and 464.98 from the second, 14.8 apart and each at least 10.0 actions from a cell edge
  (`cand.family_band.rg_r1`, `cand.family_band.rg_r2`, `cand.rounds_agree`). That is a property of
  this draw rather than of the design: a single round's estimate carries a sampling standard
  deviation near 80 actions, 1.6 cells, so the shipped record was chosen from the action layer's own
  stream for a realisation in which the two windows' measured rates sit close together, and the
  homogeneity the p-values report is what makes such a realisation ordinary rather than lucky.

**The noise, measured, because forcing on data too smooth or too noisy to separate is not forcing.**
Resampling the audit's four cells 20,000 times: the answer's sampling standard deviation is 53.5
actions (11.8 per cent), the standard deviation of the gap between the two families is 47.1, and the
gap's mean is 156.7, so the separation is 3.33 standard deviations of its own sampling error, the
observed gap of 159.62 is 3.39, and the gap is positive on 99.88 per cent of the draws
(`noise.gap_beats_sd`, `noise.gap_observed`, `noise.gap_positive`). The stated granularity of fifty
actions is 0.93 of that standard deviation, so the bulletin states the indicator no finer than the
audit can carry it (`noise.grain_not_finer_than_sd`); a whole-number count would have claimed 0.2 per
cent precision on a figure whose own standard error is 11.8 per cent. The record itself is not
smoothed: daily action counts have a chi-square per degree of freedom of 0.972 against a weekday mean
before the surge and 1.337 from it, with an unconditional 1.76 that is the register's own working
week, and the daily count of marked actions is at 1.03 (`noise.dispersion_plausible`,
`noise.dispersion_plausible_surge`, `noise.weekly_cycle_present`, `noise.dispersion_marked`).

**What the stated figure is, and what it is not, accepted and recorded.** The committed count is a
**point estimate**: its audit-sampling standard deviation is 53.5 actions, larger than the
fifty-action granularity it is stated to, so a fresh draw of the same audit design would land in the
stated cell about **36 per cent** of the time. Three things stand beside that and are why it ships.
- **Determinism holds on the shipped data, which is what the gates ask.** Every estimator built on
  the classifier's two error rates agrees on 450 on this record, whether it pools, stratifies with a
  fallback, leaves an unaudited stratum coded or uses one round alone; every stratified one that
  refuses to patch is not computable; and the judge confirmed the pooled reading by recomputation.
- **The granularity is squeezed from both sides and has exactly one workable value.** Finer splits the
  right family: at twenty-five the by-month route that leaves the autumn coded at 432.70 and the
  theme routes at 466.08 and 466.75 leave the call's cell. Coarser swallows a wrong route: at one
  hundred the hand-code-where-audited route at 386.00 falls into the call's cell. Fifty is therefore
  the only grain available rather than a choice declined, and it is 0.93 of the sampling standard
  deviation, so it over-claims by no margin at all.
- **Only the count is an estimate.** The thirteen fortnight rows, the three route rows and the seven
  partner rows are censuses of the record: every one of those 69 graded cells is a count, a median of
  observed minutes or a rate times a count, with no sampling in it.

**Two thin closures the judge named, both accepted and recorded.**
- **Either round alone is now inside the call's cell,** which closes the one the judge raised: round
  one gives 450.21 and round two 464.98, so a solver who pools and a solver who takes a single batch
  of the same instrument file the same count. Nothing in the pack forces pooling and nothing needs
  to: pooling is what the field does with two batches of one instrument, and the record no longer
  punishes a solver who does not.
- **The euros column rested on clause 6.2 by one inferential step,** since 6.2 says a report delivered
  after a period's close is paid with the period it was delivered in and the golden read that as
  excluding it here. That one is closed in the asking sentence rather than in 6.2, which sits next to
  the device: the ask names the observable, "the euros its data agreement pays for the ones filed by
  the close", so the euro column is over the reports delivered on or before 30 October and the
  late-filing count stays its own figure.

**Robustness and fairness.** The truth behind the simulated record is 468 confrontational actions and
the estimate is 454.91, 0.24 of the answer's own sampling standard deviation below it, so the
estimator is fair as well as determinate; the generator asserts the gap in those units
(`noise.fair_to_truth`). The answer's raw figure sits 4.91 from the centre of its cell and 20.09 from
the nearest edge, and one more agreed-confrontational row in the worksheet moves it by 2.8
actions, so eight such rows would be needed to reach a cell boundary (`bin.total`, `bin.total_mid`).

**Every graded figure off its rounding edge.** The call sits 20.09 of 25 from its nearest edge. The
seven euro totals are a per-report rate in cents times a count, so the generator's rates were moved
until each total sits at least 0.30 of a euro from its edge (926.10, 2,385.95, 2,211.90, 369.85,
545.10, 354.20 and 701.10 raw): the schedule reads 6.30, 5.95, 7.30, 5.45, 6.90, 8.05 and 6.15, and
the adenda of 24 July raises P04 to 6.30 from 1 August. The three medians are whole minutes and each route's two middle
values are equal, so neither the rounding nor the even-set convention can move them, and the
`convencoes` sheet files the even-set rule anyway. **The build grades no percentage at all.** The fortnight's partner column is a count of
the fortnight's actions the network reported, not a share of them, so thirteen graded cells have no
rounding in them and axis 10 carries no percentage anywhere: the graded set is the count to the
nearest fifty, 39 fortnight counts, 6 route counts, 3 medians in whole minutes and 7 euro
totals. Measured over all 70 of them, the tightest sits 0.300 of its own rounding unit from the edge
of the value it prints (`bin.graded_unit_edge`), against the 0.15 the design point asks for.
`bin.no_graded_percentage` asserts the deliverable answers state no percentage and
`bin.prompt_rounds_no_share` that the prompt asks for none. The bulletin's own rounding rule for a
percentage is filed in the dictionary anyway, which closes the axis for anything later:
`convencoes` carries "uma percentagem e arredondada uma vez, a uma decimal, a partir do valor exato, e
nao truncada nem arredondada por etapas", asserted by `bin.share_rounding_filed`.

**The grid.** Two axes, how the reports are resolved and which measured quantity the count carries:

| | false marks out | labels as they stand | the audited shares | the two error rates | the recall only |
|---|---|---|---|---|---|
| the three routes resolved to actions | 250 | 300 | 600 | **450** | 600 |
| each accepted report counted as an action | higher in every column, asserted | | | the decisive column still the only one the protocol asks for | |

Every cell is a named figure. The decisive column is the only one that answers the protocol's
question, and it is the column least moved by a solver who fails to resolve the routes, because the
correction is a ratio of the worksheet's own cells and not of the record's volume.

**Dominance.** The ordinary actions outnumber the confrontational ones about nine to one, so the
classifier's one-in-fifty false-mark rate puts 18 wrong marks in the worksheet against 84 misses: the
two errors are of the same order and neither cancels the other, which is what makes each easy route
land on a different wrong cell.

**Worth of each rung, on the graded quantity.** Rung 1 to rung 0 is one cell, rung 0 to rung 2 two
cells, rung 2 to the answer one, the answer to the default path three, and the default path to rung
4b two. Rung 4a, the coded count scaled by the recall, shares the default path's cell on this record:
the two are 1.1 actions apart, which is the one place the ladder is worth less than a cell, and both
of them are three cells from the answer. Nothing else between the rungs is worth less than one cell
of fifty actions, which is 11 per cent of the answer, and every rung is satisfying to stop at: each
is the whole output of a pipeline whose every input figure is correct.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which actions are in the count | 3.2 files the period and 2.1 the action; asserted |
| 2 | Unit of account | the item, the report, the action | 2.1 files the action; asserted |
| 3 | Attribution window | which day an action falls on | the register's local action date, which no reception stamp overrides; SF7, asserted |
| 4 | As-of dating | the record at the extract | the manifest files 6 November 2026; SF14, asserted |
| 5 | Version basis | the reposted month, whose second load carries the stamp of the day it arrived, and the superseded place names | the import log, the dictionary's `carimbo_entrega_utc` line and the gazetteer; SF9, SF28, SF8, asserted |
| 6 | Denominator | none: the answer is a count | nothing to close, stated |
| 7 | Weighting | each round draws its batch at random from the reports entered since the previous close, so the batch carries no weights of its own | 4.5 states the draw and its window; asserted that every row is a press item and that two months and two themes have no row |
| 8 | Window length | the reporting period | 3.2; asserted |
| 9 | Boundary inclusivity | 1 May and 30 October | 3.2 states both inclusive; asserted that actions fall on both days |
| 10 | Rounding path | the count to the nearest fifty actions, rounded once at the end | 3.3 and SF11; asserted that the raw 454.91 is 20.09 from its cell edge |
| 11 | Tie-break | two candidates on one cell | none against the golden: 250, 300, 400, 450, 600 and 700, asserted |
| 12 | Maturity and censoring | reports still arriving | the period closed a week before the extract; asserted that no action dated in the period is reported after the extract |
| 13 | Order of operations | resolve the routes then read the codes, or read then resolve | C1: a duplicate report carries the same identifier, theme, locality and day, so either order gives the same actions, asserted |
| 14 | Row order | the item log's own order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the three routes, the two editions, the reposted month, the ingest counter's second count | C1 for the actions; the dictionary's load sentence and `convencoes` for the report counts, asserted |
| 16 | Identity normalisation | place names, partner delivery codes | the gazetteer's superseded names; the agreements' addendum of 8 September for the delivery codes; SF21, asserted |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | items, reports, actions, minutes, euros | the dictionary names each; the indicator reads actions only, asserted |
| 19 | Code and status semantics | the route codes, the action codes, the acceptance column, the worksheet's two coding columns, the rows the desk could not code and the desk's decision | the protocol and the dictionary; SF27 for the empty manual code, asserted to give the same call; the codes are read correctly on every rung |
| 20 | Integerisation | the count to the nearest fifty actions | 3.3; the raw 454.911 rounds to 450, asserted |
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
computed on the same rows: the codes as filed give 300, the codes with the false marks out 250, the
hand codes where the desk audited with the classifier's elsewhere 400, the audited reports' own
confrontational shares carried onto the record 600, the coded count scaled by the recall 600, the
audited prevalence over the press-reported actions 700, and the count rebuilt from the classifier's
two measured error rates 450, which the worksheet's own four cells fix. Every stratified variant of
any of them that refuses to patch has no rate for September, October, `ENE` or `FLO` and is not
computable; every one that patches, by pooling or by leaving the unaudited stratum coded, and either
round's cells taken alone, land in the same 450. The easy routes are easy estimators of the same literal estimand, not other readings
of it, and every other term and convention has an SF row ruled out by a quoted sentence or asserted to
give the same call.

## Oracles

- `amostra_dupla_codificacao.csv`, the coding desk's own worksheet, carries two codings per row and no
  rate, no count and no method; it is the raw material the decisive step reads and it ties under every
  rung, because each rung reads a different pair of its four cells.
- The earlier monthly bulletins report actions recorded and territory touched and never confrontational
  actions, so they tie under every rung. Their monthly rows show the register's territory widening
  with the autumn's volume, 82 municipalities in May against 117 in September, which is a fact about
  the register and not about any count.
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

`leak.py task192 --asof 2026-11-06` returns REVIEW on three lines and no LEAK: one figure collision,
the notifications distractor's planned dates and the manifest cell derived from them, plus one INFO
on container metadata. Each is answered here.

- **`protocolo_vigilancia_v4.pdf`, the number 4.3.** That is the protocol's own paragraph 4.3, on what
  each partner is paid per accepted report, and it collides with the 4.3 per cent marked rate the
  write-up states for the part of the period the audit never reached. A paragraph number and a
  percentage are not the same kind of thing, the protocol states no rate of any kind, and the
  write-up's own figure is computed from the register rather than read from the protocol. Under every
  rung the paragraph ties.
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
- **Gone with the realism pass.** The three collisions the earlier pack carried (118 and 119 in the
  monthly bulletins against a fortnight's municipality count, and 103 in the partner returns) are no
  longer there: the register's geography now moves with its volume, so the monthly rows read 82, 83,
  86, 88 and 117 municipalities and no longer sit on a graded fortnight's figure.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per fortnight, the actions recorded, the municipalities touched and how many of those actions the partner network reported | 3 per fortnight, 13 fortnights | the construction's own output on the segment the trustees want anyway, the actions the count is taken from | the bulletin's standing table | D5 scope: the partner column counts the fortnight's actions by the day of the action, and the network's deliveries lag the action by a median 1,385 minutes, so dating the column by the delivery moves twelve of the thirteen rows | D1 the re-imported month doubles the network's rows and no actions, which moves three rows hard (Q7 97 against 68, Q8 134 against 67, Q9 102 against 58); D6 grain: an action the network reported is one the network delivered a report of, however many routes also did, and the stricter reading drops every row by about three quarters; D5 again: the last fortnight has fifteen days, so a solver who stops the thirteenth at 29 October loses 54 actions | item log, partner reports, public line, gazetteer, protocol, dictionary, manifest, import log; 12 columns | 4 stops, lazy delta 11 of 13 fortnights | the bulletin's own standing table |

**On the partner column being a count and not a share.** It is not a different quantity and it is not
fewer graded cells: thirteen cells stay thirteen, and because the fortnight's total actions are graded
beside it, the count and the share are each derivable from the other from what the write-up states
either way. One independent quantity, presented the way that carries no rounding edge, which is why
the conversion loses no difficulty: getting it right still means resolving the action grain, the
reposted load, the delivery lag against the action's own day and the gazetteer.
| A2 per access route, the reports received, those the association could not place and the median minutes from the action to the report | 3 per route, 3 routes | the audit trail from an input the call consumes, through rows it never reads, to the route's own control total | the pipeline review the data manager runs each period | D4 absence as the signal: the reports that could not be placed are held in a separate exceptions file no habitual join reaches, and the ingest counter counts the reposted load's second arrival again | D8 the reception stamps are UTC, the action times are the local clock of the action's district, the clocks go back on 25 October and the Azores run an hour behind; D6 a press report entered the monitor with the first of its items | exceptions file, ingest counter, item log, partner reports, public line, monitor configuration, gazetteer, dictionary, manifest; 12 columns | 5 stops, lazy delta 3 of 3 routes | an ingest pipeline's own period review |
| A3 per partner organisation, the reports it filed on actions in the period, those filed after the period closed and the euros its data agreement pays for the ones filed by the close | 3 per partner, 7 partners | an input reconciled to another system's total, the gap made of devices | the finance office settles the data agreements | D2 version: one agreement was amended mid-period and the rate paid is the amended one, which the superseded schedule does not carry | D7 one partner's deliveries change code after a merger, under a second addendum; D8 the delivery stamp is UTC against the period close; D1 the reposted load is paid once; D3 basis: each organisation's own monthly return counts its reports by the month of the action while the portal stamps the delivery, so the returns and the delivered rows differ at a month boundary | partner monthly tables in PDF, agreement schedule, two addenda, ingest counter, manifest, dictionary; 13 columns | 5 stops, lazy delta 4 of 7 partners | the finance office's quarterly settlement |

**The main population's zero counts.** Zero device rows and zero hazard rows in the actions and
episodes the share rests on: every device sits in the exceptions file, the ingest counter, the
agreement schedule, the addenda or the partner monthly tables, none of which carries an action.
Deleting every device leaves the share exactly as hard, asserted by count.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D8 the clocks: UTC against the district's local time, the 25 October change and the Azores hour | A2, A3 | A2 one route's median by 56 minutes and another by one; A3 the late-filing counts |
| D1 the reposted load's own stamps: the portal wrote them on the day the file came back | A2, A3 | A2 the partner route's median by 65 minutes under the second load's stamps; A3 nothing, because the agreement pays a report once |
| D6 grain | A1, A2 | A1 the partner count, every row, under the stricter reading of a reported action; A2 one route's median by 12 minutes |
| D1 the re-imported month | A1, A2, A3 | A1 three fortnight partner counts (Q7 97 against 68, Q8 134 against 67, Q9 102 against 58); A2 the partner route's received count by 140; A3 the euros of every partner |
| D5 scope | A1 | twelve partner counts when the column is dated by the delivery, and the thirteenth fortnight's three figures when the last fortnight is cut at fourteen days, which loses 54 actions |
| D7 the second delivery code | A3 | one partner's filings by 29 and its euros by 172 |
| D3 the returns' own basis | A3 | each organisation's declared month totals against its delivered rows at a month boundary, P01's May reading 18 against 17 delivered |

**The referee.** `manifesto_extracao.csv` states each file's rows, range and extract date and settles
the one designed disagreement, the exceptions file's extent, without naming a level.

**The cracker sheet.** The cracker filed 450 confrontational actions, ran the hygiene battery,
executed every filed paragraph and matched every control total. Every row below is computed on the cut
pack rather than read off by hand, because two builds in this wave shipped a sheet whose figure was the
complement or the mirror of the truth.

**Measured by:** `generator/cracker.py`, which runs each named wrong path through `golden.py`'s own
readers on the shipped bundle, prints this table and exits non-zero if any row's cracker figure equals
the golden.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 actions the partner network reported, fortnight 8 | counts the network's rows, so the reposted August load counts twice | 134 | 67 | miss |
| A1 actions the partner network reported, fortnight 10 | dates the column by the delivery rather than the action | 289 | 157 | miss |
| A1 actions the partner network reported, fortnight 11 | counts only the actions no other route reported | 32 | 155 | miss |
| A2 reports received, the partner network | sums the ingest counter, which counts the reposted load again | 1347 | 1207 | miss |
| A2 reports that could not be placed, the press monitor | the item log alone, which holds only the items it placed | 0 | 147 | miss |
| A2 median minutes from the action to the report, the press monitor | reads the monitor's reception stamp as local time | 59.0 | 115.0 | miss |
| A2 median minutes, the press monitor, every item | takes every item of a report rather than the first | 127.0 | 115.0 | miss |
| A3 euros paid, the amended partner | the schedule's rate for the whole period, without the July adenda | 332 | 370 | miss |
| A3 reports filed, the merged partner | one delivery code, without the September addendum | 86 | 115 | miss |
| A3 euros paid, the merged partner | one delivery code, without the September addendum | 529 | 701 | miss |
| A3 reports filed, all seven partners | every row of the partner file rather than the period's actions | 1248 | 1165 | miss |

**Pair ceiling:** 39.0
**Mirror leakage:** 20.0

## Pre-ship check

**The loop-2 judge's two advisories, answered rather than fixed.**

- **The figure's own sampling error is wider than the grading grain.** The generator measures the
  committed count's standard deviation over the four audit cells at 53.5 against a 50-action grain,
  so a fresh audit of the same thousand reports would land in the 450 cell about a third of the
  time. That is a statement about a counterfactual audit, not about this bundle: the shipped audit
  is fixed data, 454.91 sits 20.1 below the 475 edge and 29.9 above the 425 edge, and every route
  the bundle leaves standing on the classifier's two error rates lands in the same cell, each of
  them at least 7.7 actions from its edge. What the decision rests on is the gap between the
  families, and that is earned rather than drawn: 156.7 wide against a standard deviation of 47.1,
  so 3.3 standard deviations from zero and positive on 99.88 per cent of 20,000 resamples, with the
  audit's 15.25 per cent hand-coded prevalence against the record's 9.77 per cent carrying it. The
  grain is not coarsened, because coarsening to the nearest hundred would move the committed figure
  to 500 and merge the 400 and 450 cells the ladder separates.
- **Constant error rates in September and October are an assumption the bundle cannot test.** No
  hand coding exists after 31 August. `config_monitor.json` carries `alteracoes_no_periodo:
  nenhuma` with the training date, which is the shipped fact the correction stands on, and within
  the audit the classifier's sensitivity and its false-mark rate are homogeneous by round (p 0.36
  and 0.52) and by theme. It is the right assumption for the field to make and the pack says so; it
  is not a figure anyone recomputes.

**The free gates, run on the shipped pack.**

| Gate | Result |
|---|---|
| generator assertions | 310, 0 failures |
| `verify.py`, own code path, bundle only | 138 independent checks, 0 failures |
| `cracker.py` | 11 rows, 0 kept by the cracker, exit 0 |
| rebuilds | two byte-identical over `target/` and `golden/`, `6967fdeeed32d8cab624e17eea1e22b07bc22e1afb70417322c61daba4c65d29` |
| `figures_check.py` | exit 0, 111 figures in blocks 1 to 4, 0 absent |
| `precut.py` | exit 0, 50 checks, 0 FAIL, 0 WARN |
| `voice-check.py` | exit 0, 983 characters |
| `leak.py --asof 2026-11-06` | REVIEW, no LEAK, three lines each answered above |
| `guard.py surface` | 0 BLOCK lines, one pair promoted for adjudication (task191, surface 0.101) |
| `guard.py heart` | WARN, no BLOCK, nearest driver 0.09 |
| container audit | `target/` and `golden/` clean, no producer signature, no out-of-band stamp |
| input gates | 18 files, 4 formats, 25,982-row item log, 3 distractors |
| `target.zip` | 18 members at the archive root, content byte-identical to the tree, `060f895956fa86a025eec2d9aac7c93a988ae685667de4c6f050e301711706d1` |

**The client's three rules, re-read against the built pack and not against the design.**

1. **The task really uses its domain.** The deciding quantity is the count of confrontational actions
   in a contentious event record, and what decides it is which of the quantities a hand-coded
   validation batch measures can be carried to a window the batch never reached. That is the
   measurement-error half of protest event analysis, the literature the task type runs on. Swap run on
   the sentence: with parcels on a belt and a scanner there is no coder reading news text, no
   hand-coding standard to measure it against and no protocol definition of the class, so the quantity
   becomes a physical count and nothing is left to estimate. No stated score, eligibility check, sort
   or filter decides anything.
2. **Two layers, both in the built pack.** Layer 1 is what the association's own systems produce: an
   item log at item grain with accepted and rejected items and a report entering with its first item,
   three routes and two language editions on the same actions, a month loaded twice whose second load
   carries the stamp of the day it arrived while the ingest counter counts that arrival again, an
   intake window that writes the night's arrivals at the next collection, UTC stamps against each
   district's local clock with a summer-time change and an island district an hour behind, monthly
   returns inside a PDF counted on the action's month, a delivery code change after a merger,
   superseded settlement names, a coding desk whose lot is as big as the days it had and eight of
   whose rows carry no manual code at all. None of it decides the count, and `R2.*` asserts the count
   is invariant to the reload, the clocks and the name resolution. Layer 2 is the correction and it
   carries the stump.
3. **None of the three banned kinds decides the call.** No decoy: nothing is planted, no block copied
   (asserted), no memo or stakeholder figure carries a count, and no shipped file states a
   confrontational count, a rate or an error rate. Not semantics: every field, code, offset and
   definition read correctly still leaves the default path carrying the audited batch's own shares onto
   the record and filing 600. Not rule application: no shipped sentence says how the labels become the
   count, and a word sweep over every file, every PDF and the workbook's cells asserts that nothing
   names sensitivity, specificity, recall, precision, a correction, a false positive, a false negative,
   representativeness or extrapolation.

**The test, answered in writing.** Could a strong analyst who cleaned the data and read every rule
correctly still get the answer wrong by doing the analysis the easy way? **Yes.** They resolve the
three routes, the two editions and the reposted month, apply the offsets, read 3.3, open the worksheet,
take the share of the audited reports on each side of the classifier's label that the desk found
confrontational, carry those two shares onto the 4,228 press-reported actions and file 600. The shares
were measured on the four months the desk audited, where the classifier marked 8.8 per cent of
actions, and are carried onto a period where it marked 4.3 per cent after the cut. Analytical, and the
generator executes it (`R3a.analyst_test`).

## Held for the next pass

**Nothing is held.** The six items this section carried were worked in the realism pass of
2026-10-17 and each one is recorded in `## Tried and rejected` with what it cost. The paragraphs
below stay because they are the build's Gate F evidence and the record of two readings of it.

**The loop-3 reader, read cold on the pinned pack, is the Gate F evidence this build needed.** It
committed to **550** at about 45 per cent, with 30 per cent on 600 and 15 per cent on 500, and it
reached there by the right kind of analysis and the wrong estimator: it found the classifier hiding
confrontations inside the ordinary label and corrected label by label on predictive values, which is
the default path's family, rather than on the classifier's sensitivity and false-mark rate, which is
the answer. That is the field's own distinction between a predictive value and an error rate, and it
is the distinction this build is built on. The two figures the reader quotes, about 531 and about 580,
are that family with and without filer precedence; 2.6 rules filer precedence out, which is why 531
is reachable but not defensible. A strong cold reader spread over three cells and confident in none
is what the ladder was for.

**Two corrections to the reader's own reading, for the record.** Its question 5 quoted 3.3 and then
executed the one thing 3.3 forbids: the sentence says the number the bulletin fixes is of the actions
that were confrontational and not of the codes assigned, so the coded count is ruled out by the
sentence the reader quoted to reach it. And `amostra_dupla_codificacao.csv` is not a file that exists
to help the analyst; it is the evidence the call rests on, and a coding desk that measures its
classifier against hand coding keeps exactly such a worksheet. The reader's point that it is the only
route to the call is fair and is the design. What the reader was right about, and what the realism
pass fixed, is that the worksheet was built rather than kept: the six items below it named are now
the desk's own calendar, capacity, rota, notes and failures to code.

## Tried and rejected
- The loop-4 reader, cold on the re-drawn record, **missed the call**: it filed 550 at 50 per cent
  with 600 at 20, 500 at 12, the stored-code count's 300 at 8 and the golden's 450 at **6**. That is
  the first cold thread in this wave to go wrong on a call, and it matters for more than Gate F: the
  pair ceiling assumes a ladder that keeps all but one response off the call, and until a cold thread
  misses it the measured pair is an assumption rather than evidence. task190 was retired today on
  exactly that premise failing. Here it holds, so this build's ask arithmetic means what it says.
  The reader's route is the predictive-value family again, now with an extra step: it treated the
  partner and line codes as ground truth because they agree on 205 of 205 overlapping actions, and
  corrected only the monitor-only actions. Without that step it lands on 605, the 600 cell.
- The realism list from that read, held until the judge reports. **The worst of it is that a realism
  defect is generating a wrong route:** the partner and line codes agreeing on 205 of 205 overlaps is,
  in the reader's words, the most generated-looking statistic in the pack, because independent
  reporters never agree perfectly, and that perfect agreement is what licensed it to treat those codes
  as truth. Breaking the agreement moves the filer-confrontational count, so it is a figure-moving fix.
  Next: the audit covers 54 per cent of accepted May to August reports, 91 per cent in May falling to
  22 in August, and a desk double-coding half of everything is a validation exercise rather than a
  sample. That one is answered by framing rather than data, since the protocol can say what the
  exercise was, and no figure moves. The classifier reads as a relabeller instead of an instrument,
  its errors concentrated in three labels while two stay almost clean. Identifiers are gap-free across
  three files. The exception file reuses identifiers, about two rows per identifier across 308 rows,
  which is a key-uniqueness defect the hygiene battery would flag and which nothing declares. The
  tension index contradicts itself, labelling a rise from 56.3 to 67.2 as falling. The media coverage
  file is a literal expansion of the monitor's own config weights. And the report lags have no long
  tail at all, the press maximum sitting at 20 hours.
- Credit where the pass earned it: the surge now touches new ground, 66 municipalities to 112 and 214
  localities to 421, which was the reader's complaint last round and is no longer one.
- **(architecture 3, the realism pass of 2026-10-17) A hand-coding worksheet drawn as a fixed half of each round's window.** Two cold readers read the file as built rather than kept: exactly 1,000 rows split 420 and 580, exactly 50.0 per cent of each round's pool, rows in identifier order with the coding dates running monotonically down the page, daily loads repeating, 47 notes from six stock phrases with ten of them on rows no second coder had seen, eleven of eighteen changed decisions ending on the classifier's own code, agreement flat at 74 to 79 per cent across all four coders, and not one report the desk could not code. The desk now has its own random stream (`SEED_DESK`), its own calendar and its own capacity: the lot is the sum of what its coders got through on the days they sat, which is 1,064 rows, 68.4 per cent of round one's pool and 43.5 per cent of round two's; the file is written as the desk's journal, by round, coding day and coder, so consecutive rows run up the identifier half the time (0.505); the daily load runs 5 to 45 over 58 coding days; a note sits only on a row a second coder read or a row nobody could code, composed from two pools into 35 distinct texts on 63 rows; a second coder reads a row far more often when the report is one the classifier also got wrong, so 15 of the 19 changed decisions end on a code the classifier did not give; each coder reads an ambiguous report as a neighbouring code of the same kind at their own rate, so exact agreement runs 0.614 to 0.737 across the four; and eight rows carry no manual code at all, with the dictionary and protocol 4.5 saying what an empty code means and SF27 asserting that reading those rows as ordinary codings gives the same call. **What it cost:** the audit's four cells, and therefore the committed count and every figure downstream of them, had to be re-tuned (see the entry on the design point below); the protocol's 4.5 now says the file carries the manual code "onde a mesa o conseguiu fixar".
- **(architecture 3, the realism pass) The six weeks with no coding in them.** `desk_calendar` worked each lot in the fixed 34 days before its own close, so round one coded 17 May to 19 June, round two 7 August to 9 September, and the 48 days between them were empty although round two's lot held reports dated from 20 June: either the desk worked that stretch or the round's dates were wrong. Each round now opens its lot the working day after the previous round closed and works it to its own close, with the association's holiday month thinner rather than empty and the odd catch-up Saturday. Coding now runs 4 May to 8 September with no gap longer than seven days and coding days in every month from May to September, asserted (`real.coding_calendar_has_no_hole`, `real.coding_covers_every_month`, `real.round_opens_on_the_previous_close.R2`). **What it cost:** the desk draws from the reports that had arrived by each coding day, so the lot is weighted towards the early part of each window: May gives 458 of the audit's rows and August 107. That is the stated process working, it strengthens rather than weakens the engine (the audit's prevalence sits 1.56 times the record's), and it moved every audit cell.
- **(architecture 3, the realism pass) The reposted August load keeping its original delivery stamps.** The second load of the August partner file carried the same `carimbo_entrega_utc` as the first while the import log said it arrived on 14 September and the ingest counter counted it there, so the only thing that marked the reload was the load id. The portal now stamps the second load's rows on the day the log says they arrived, spread across that morning, which is what actually double-counts a month. **What it cost:** the two stamps a reposted report now carries open a reading the pack had not had, so the dictionary's `carimbo_entrega_utc` line makes the delivery moment the first load's, SF28 carries the row, and the alternative is asserted to move the partner route's median from 1,385 to 1,450 minutes. The device is stronger for it: D1 now moves the A2 median as well as the counts.
- **(architecture 3, the realism pass) One clock profile across the three routes.** All three routes drew the action's start hour from one shared distribution, so the press monitor, the partner network and the public line filed on actions with the same mean hour of 14.0 to 14.2, the same standard deviation of 3.6, the same 07:00 floor and the same 21:55 cap. Each route now has its own hours and its own shape: the monitor's titles cover the set-piece daytime actions (mean 13.55, 07:00 to 21:59), a partner organisation writes up what its own people were at during their working day (11.76, 08:00 to 20:59) and the public line is where the evening and night-time blockades arrive (15.68, 05:00 to 23:59), asserted pairwise (`real.route_clocks_differ.*`, `real.route_clock_ranges_differ`). **What it cost:** the start hours move every receipt stamp, so the three route medians and the two partner columns moved with them.
- **(architecture 3, the realism pass) Start minutes on a quarter-hour lattice.** 52 per cent of start minutes were exactly a quarter hour, 26 per cent were one of eight other five-minute marks and the rest were uniform, which a reader read off as a lattice with a small second group ending 05, 10, 25 and 55. The minute is now drawn from a distribution with a quarter-hour mode and a shoulder around it: 44 per cent on a quarter hour, 22 per cent on another five-minute mark, 22 per cent within four minutes of a quarter hour and 12 per cent anywhere, which puts 45 per cent on the quarter hours, every one of the 60 minute values in the file and 29 per cent off a multiple of five, asserted (`real.minute_mode_is_the_quarter_hour`, `real.minute_lattice_broken`). **What it cost:** nothing beyond the stream: no graded figure reads a start minute, and the medians move only through the stamps.
- **(architecture 3, the realism pass) A surge that doubled the volume without touching new ground.** Monthly actions roughly doubled from September while the municipalities touched moved only between 117 and 119, because every action drew its municipality uniformly from the gazetteer's 119. The geography is now the register's own: each municipality carries a share of its district's standing contention (the district capital and the two island capitals most, a long tail of small ones), each dispute theme falls on the territory it belongs to, and the two themes the autumn brings, the transmission network and the fire season, run the municipality size the other way, because the lines and the burnt ground are where the people are not. The spring and summer months now touch 82, 83, 86 and 88 municipalities and the two autumn months 117, thirteen municipalities have no action in the register before 5 September, the interior districts' share rises by 37 per cent while the metro districts' falls, and Beja doubles, all asserted (`real.geography_moves_with_the_volume`, `real.register_does_not_start_saturated`, `real.surge_reaches_new_ground`, `real.surge_concentrates_in_districts`). **What it cost:** the fortnight municipality counts, the graded column of the A1 table, fell from 100 to 119 to 63 to 112, and the protocol's dispute-theme list went from fourteen themes to ten so that a theme-stratified correction has strata big enough to be worth computing (see the design point below). The earlier bulletins' three figure collisions with graded fortnight rows went with it.
- **(architecture 3, the realism pass) Re-tuning the design point on the coding desk's stream alone.** The first attempt searched `SEED_DESK` for a draw in which either round's cells alone land in the call's cell: 7,200 desk seeds gave one hit and none with both rounds inside the band. Measured, the reason is structural: the desk draws more than half of each round's pool, so a round's estimate is pinned by that window's own realised rates and the desk's draw only jitters it by about 30 actions. The two rounds' anchors are a property of the action layer, so the search moved there: 12,000 action seeds were screened on the pooled call, the two round anchors, the stratified family's anchors at seven reference desk draws, the seven wrong routes' cells, the record's dispersion in both regimes, the three medians and the fortnight ties, which gave twelve candidates, and the desk's own stream was then searched on the best of them. The shipped point is action seed 10461 with desk seed 4. **What it cost:** the two sub-routes of rung 1 now share the 250 cell while rung 0 sits at 300 and the audited prevalence at 700, so the ladder is six cells rather than the five it was, and rung 4a (the coded count scaled by the recall, 615.64) shares the default path's 600 cell, 1.1 actions from it, which is the one place the ladder is worth less than a cell. Against that, every route in the right family is now at least 7.7 actions from its cell edge where two of them used to sit 0.8 and 4.6 from one, and the family gap is 3.3 sigma where it was 2.7.
- **(architecture 3, the realism pass) The classifier's nominal rates at 0.46 and 0.0295 with a fourfold fall in the confrontational share.** The re-centring measured the candidates' positions as functions of the nominal recall, the nominal false-mark rate, the level of the confrontational share and its fall across the period, and the combination the ladder needs is a recall near one half, a false-mark rate near one in fifty, an audit prevalence near 15 per cent and a record prevalence near 10 per cent. The shipped values are 0.46 and 0.023 nominal, measured at 0.4783 and 0.0201 on the shipped worksheet, with the confrontational share falling by a factor of 2.6 rather than 4.2 so that the audit's prevalence stays inside the cell the audited-prevalence route needs. **What it cost:** nothing in the record's story, which still has a confrontational spring and summer and a peaceful autumn mobilisation; the marked rate still halves across the cut (8.8 against 4.3 per cent, p = 3.0e-09).
- **(architecture 3, the realism pass) The monitor and the public line stamping receipts at any hour.** With the start hours re-drawn, one press report landed at 23:21 on 30 October, 38 minutes from the period's edge, and the route table's zone-invariance assertion caught it: a solver who read the receipt stamps an hour out would have counted a different triple. The association's own intake hours, 06:00 to 23:00, are now in the monitor's configuration, and whatever lands outside them is written at the next collection, so no receipt stamp sits within an hour of either edge and the triple survives every zone in the pack by construction rather than by luck (`SF26.route_window_zone_invariant`). **What it cost:** the night's arrivals pile into the morning, which is what a real intake does, and the three medians moved with it.
- Loop 3, the route table shipped with no window. The loop-2 judge computed three windows off the same sentence (received in the period 4,346 / 1,204 / 945, received to the 6 November extract 4,658 / 1,313 / 988, reports of actions dated in the period 4,348 / 1,215 / 945, with the partner median moving 1,327.0 / 1,312.0 / 1,331.0), so the ask was an open fork. Closed with one `convencoes` row fixing the basis, scoped to the route figures: the partner table's own row beside it stays action-dated, so the two conventions read as the two different things they are. The row is load-bearing, not a giveaway: delete it and the three windows compute again, and it says nothing about the repost, the placement or the medians. Measured zone-robust before it was written, the nearest receipt stamp sitting 1.25 hours from a window edge.
- Loop 3, five figures graded that the prompt never asked for. The decomposition (4,200 / 427 / 302 / 30 / 1,000) and the per-fortnight shaded series left block 4; the decomposition stays in Critical Components, where it is a component of the call rather than an answer the rubric owes, and the shading stays in the bulletin as the house's own context, described but not graded.

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
- **(architecture 3) The earlier bulletins' note that two dispute themes entered the register with
  the autumn mobilisation.** "O boletim de setembro registou a entrada de dois temas de disputa que o
  registo ainda nao tinha visto, energia e redes e florestas e fogos, com a mobilizacao do outono."
  Two independent cold readers named it, in the same company as 3.3, 4.5 and the classifier's
  stability line, as part of what lets a solver see that the autumn is unmeasured by the audit. Cut.
  It was the only optional member of that company and the pack loses nothing by it: the surge is
  visible in the monthly action counts, and the two themes are visible as codes that appear in the
  record only from September. The protocol's thematic table keeps both codes, because a code list is a
  code list and says nothing about when either theme entered the register. **Why the other three stay,
  so nobody cuts them later:** 3.3 files the estimand, so it is the WHAT; 4.5 with the dictionary's
  round definition files the sampling frame, which is also the WHAT and which `determinism-check` §1
  requires; and `config_monitor.json`'s "alteracoes_no_periodo: nenhuma" is a decisive fact Gate B
  requires shipped, because without it the classifier's error rates would not transport either and the
  problem would have no answer at all. Cutting the sentence moved no figure: `figures.json` is
  byte-identical across the rebuild and only the bulletins PDF's own bytes changed.
- **(architecture 3) Grading the fortnight's partner column as a share of the fortnight's actions.**
  The share put a one-decimal percentage in thirteen graded cells, and `determinism-check` §3 says
  never grade a percentage near a one-decimal edge, flatly, without an exception for a filed rounding
  path. Filing the path closed the one route that misprinted Q11, but managing one instance of a hazard
  class is not removing the class, and a judge reading the rule as written costs a determinism return.
  The column is now a count of the fortnight's actions the network reported. No data moved, so the
  call, the candidate table, the 2.8-sigma family gap and the audit's own draw are untouched; thirteen
  cells stay thirteen cells; and the difficulty is unchanged, because the count still turns on the
  action grain, the reposted load, the delivery lag against the action's own day and the gazetteer,
  measured at three misses on the cracker sheet. Exactly fourteen graded figures moved, the thirteen
  converted cells and P07's euro total, confirmed by diffing `figures.json`.
- **(architecture 3) A cracker sheet measured by hand.** Two builds in this wave shipped a sheet whose
  figure was the complement or the mirror of the truth, and the gate that reads the sheet cannot tell.
  The sheet is now the printed output of `generator/cracker.py`, which runs each named wrong path
  through `golden.py`'s own readers on the shipped bundle and exits non-zero if any row's cracker
  figure equals the golden.
- **(architecture 3, the author's pre-ship pass of 2026-10-17) Measuring a share's distance to its
  rounding edge as the distance to its printed value.** `checks.py` computed `abs(t - round(t))` on the
  share in tenths of a point, which is the distance to the middle of the printed cell and not to its
  edge, so it named Q9 at 0.0129 as the tightest when the real tightest is Q11 at 0.0013 and Q9 is
  comfortably clear at 0.0371. The judge found it. The check now computes `(0.5 - abs(t - round(t)))/10`
  and reports every one of the thirteen, and the seed hunt that had optimised the wrong quantity is
  superseded by filing the rounding path instead (axis 10). A bar of 0.010 points on all thirteen is
  reachable, 27 of 360 pack seeds clear it with no two-step drift, but reaching it means a different
  `SEED_PACK`, which re-draws all 69 graded ask cells, the audit's own draw and therefore the call, and
  voids the judge's reproduction table; held for the author's call rather than taken.
- (architecture 3) P07's rate at 6.15, which put its euro total at 731.85, 0.35 of a euro from its
  edge and the tightest of the seven: moved to 6.10, which lands 725.90 and 0.40, the clearance the
  other six have. Only that one graded figure moved, confirmed by diffing `figures.json` across the
  rebuild.
- (architecture 3) Leaving "the euros paid under its data agreement" to clause 6.2. Two independent
  threads reached two values on the same reading, 7,337.90 against 7,410.85 and P02 at 2,493.05
  against 2,504.95, because 6.2 pays a late delivery with the period it was delivered in and whether
  that excludes it here is one inferential step. Closed in the asking sentence rather than in 6.2,
  which sits next to the device: the ask now names the observable, the euros the agreement pays for the
  reports filed by the close. No golden figure moved, because the golden already computed exactly that.
- (architecture 3) Paragraph 4.5 saying each round draws from the reports entered since the previous
  round closed, while round two closed on 10 September and its batch stops at 31 August: the 305 press
  reports of 1 to 10 September were in neither reading and a close reader was left holding a
  contradiction, although the figure never moved because the dictionary's range is what controls. 4.5
  now gives each round a cut and a close, the batch runs from the previous cut to its own cut, and the
  round closes when the desk signs the batch off; the dictionary's `ronda` column states both dates for
  both rounds. Text only, no figure moved.
- (architecture 3) The dictionary saying the desk works the batch on working days while 56 of the
  1,000 rows carry a weekend coding date: the generator's own calendar already models the occasional
  catch-up Saturday, so the dictionary now admits it rather than the rows being moved. Text only.
- (architecture 3) Leaving each partner's own monthly return to be read as the delivered rows. The
  returns count a report by the month of its action and the portal stamps the delivery, so at a month
  boundary the two differ, P01's May reading 18 against 17 delivered. That is the pack's own basis
  difference and it is now a declared device in the ask sheet (D3) with the basis filed in the
  dictionary's description of the returns, rather than an accident a reader has to guess at.
- (architecture 3) Paragraph 4.5 closing on the desk's schedule, that the round the calendar puts in
  the autumn is done in the next reporting period: of the whole pack it was the one line nearest the
  signpost boundary, because its only function was to tell a reader that the autumn holds no audited
  report. Cut. The frame stays, which is the sentence saying what each round drew its batch from and
  over which period, and that is the WHAT the estimand owes; the coverage gap is visible in the
  worksheet's own dates and the uncomputability of every stratified route is asserted on the data
  rather than on that line. Dropping it moved no figure: `figures.json` is byte-identical across the
  rebuild and only the protocol's own bytes changed.
- (architecture 3) Three Azores municipalities in the gazetteer's "Ilhas" district beside the Madeira
  ones, with the clock offsets in no shipped file: a geography error of the pack's own making that
  left the medians open four ways. The gazetteer now carries "Acores" and "Madeira" as separate
  districts and the monitor's configuration states each one's offset and the 25 October change, which
  closes the medians and leaves the Azores hour as a device in A2 rather than an accident.
- **(architecture 3, the stage-2 re-measurement of 2026-10-21) The magnitude fix itself: widening the
  composition drop so the easy family sits further from the call.** Dead on the floor it spends. The
  drop and the margin on the nearest wrong rung are one quantity with two signs: sweeping
  `CONF_RATE_LO = CONF_RATE_HI / k` over k = 1.0 to 8.0 at the shipped surge, the reach `PV - RG` rises
  36.95, 89.56, 114.37, 139.19, **159.62 (shipped, k = 2.6)**, 180.05, 190.27, 197.57, 206.33 actions
  while the gap to rung 2 falls 180.10, 125.68, 105.57, 85.47, **68.91**, 52.35, 44.07, 38.16, 31.06
  and its ratio falls 1.3588, 1.2824, 1.2496, 1.2126, **1.1785**, 1.1423, 1.1245, 1.1103, 1.0919. The
  1.15x floor is crossed between k = 2.6 and k = 3.2, the gap falls under one printed cell by
  k = 4.0 (0.88 cells) and rung 2 shares the call's own printed cell at k = 8.0 (369.064 against
  338.000, both printing 350). Over twenty action seeds a setting, the floor passes falls from 20
  of 20 at k = 1.0 to 13 of 20 at the shipped point and 8 of 20 at k = 4.0. The shipped point is
  therefore already at or past the widest setting the floor allows, and the realism pass of
  2026-10-17 had already walked this dial down from a fall of 4.2 to 2.6 to keep a wrong route
  inside its own printed cell (its own entry above), which is this same trade read from the other
  side. `corr(reach, gap to the nearest rung)` = -0.5791 over the sweep.
- **(architecture 3, the stage-2 re-measurement) Widening on the volume axis instead, where the two
  separations do not trade off.** `ACTIONS_SURGE` 1.0 to 6.0 at the shipped drop raises the reach
  65.23, 82.77, **159.62**, 207.10, 250.98 actions with the floor holding (ratios 1.2027, 1.2306,
  **1.1785**, 1.1896, 1.2190), so it is the one axis that buys reach without spending the floor, and
  it is dead on Gate C: over 120 draws on that axis the licensed error-rate family is unanimous on
  one printed call in 5, going 2, 1, 2, 0, 0, 0 of 20 seeds at surges 1.0, 1.6, 2.45, 3.4, 4.5 and
  6.0. The axis that keeps the ladder splits the call.
- **(architecture 3, the stage-2 re-measurement) The architecture, on the identity behind both of
  those.** `PV - RG = N (p - p_a) [(PPV - (1 - NPV)) - 1/(r - f)]` holds to 1.3e-13 at every seed, so
  the reach the ladder stands on **is** the difference between the record's own marked rate and the
  worksheet's own marked rate, times a constant of the four cells. Both are one group-by on a shipped
  column (`codigo_acao` on the item log, `codigo_monitor` against a non-empty `codigo_manual` on the
  worksheet), so the exchange rate is fixed by arithmetic rather than by tuning: 26.90 actions of
  reach per sigma of the window comparison at the shipped point, 25.29 to 48.00 across the drop axis.
  Counted over the two axes at twenty action seeds a setting, 245 of 300 draws give a printed
  cell of reach or more and 66 leave the window comparison insignificant, 22 do both, and **0**
  of those 22 have the licensed family unanimous; the family is unanimous in 9 of the 300 and all
  nine sit where the comparison is significant below 0.05. **0** of 320 draws give reach, a
  unanimous family, the 1.15x floor and a mid-bin call together, and the three that give the
  first three are the shipped setting and two at surge 1.0. So every draw with reach and a quiet
  record forks the call and every draw that files one call announces the step: the dial's two
  ends are the same end, the failure is not magnitude and no magnitude fix exists. Re-root or
  retire, the author's call: this is architecture 3.
- **(architecture 3, the stage-2 re-measurement) Re-shipping this pack as it stands, independently
  of the screens.** `guard.py heart task192` now returns **BLOCK** where on 2026-10-17 it returned
  WARN with no BLOCK, because the corpus moved under it: `ban.role` on the `research_desk`
  stakeholder family, `ban.forum` on `trustees_or_governors` and `ban.forcing_event` on
  `vote_or_meeting` all against task266 (v1), now delivered or approved, and
  `test.same_driver_older` because the decisive gap, the decisive pattern and the Gate G mechanism
  all repeat task270 (v2, lineage) with no differentiation line on the card. The driver text is not
  the problem, its nearest neighbour on file sits at 0.06; the axes are. So the role, the forum and
  the forcing event have to be redrawn whatever is decided about the magnitudes, which is a second
  reason the number wants a re-root rather than a resumption. `guard.py validate` is clean (277
  cards, 0 invalid) and the pack itself is untouched: `verify.py` passes all 138 independent checks
  and `target/`, `golden/` and `target.zip` hash to what the ship recorded.
  `guard.py surface` is exit 0 with no BLOCK lines and no personas in the cut pack, and it now
  promotes **three** pairs for adjudication with task192 in all three, each at exclusion level
  with both sides delivered: task191 vs task192 at 0.101 (corpus pct 99, back to back, same
  decisive gap and same context-artifact type on the cards), task192 vs task193 at 0.100 (pct 98,
  back to back, same decisive gap) and task189 vs task192 at 0.101 (pct 99, same decision type).
  On 2026-10-17 only the task191 pair was promoted, so two have appeared since. These are B-track
  card-axis matches rather than driver text, and they point the same way as the heart BLOCK.
- **(architecture 3, the stage-2 re-measurement) A seventh cell nothing in the pack rules out, found
  on the way.** A calibration model fitted on the worksheet with the classifier's label and a month
  term, extrapolated over the two months the audit never reached, files 504.483 and prints **500**,
  which is neither the call nor the default path and has no row in the candidate table and no `cand.*`
  assertion. Without the month term the same model reproduces the default path exactly (614.530). It
  is a construction a competent analyst would use and it is an open Gate C candidate on the shipped
  pack, which the loop-4 judge never tested; recorded here because it would have to be closed by any
  repair and cannot be closed by a magnitude.

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
- **(2026-10-25, measured) A blind reader landed the call exactly, took 92.5 per cent of the ask figures, and reproduced this note's whole ladder as its own list of rejected methods.** One isolated Sonnet reader at medium effort, holding only the pack, the prompt and the emitted key list, filed **450 confrontational actions** against the golden 450 (its exact 455 against the generator's 454.91), on 4,656 actions built as tema plus gazetteer locality plus occurrence day, and hit **98 of 106 ask figures**. It took the decisive step and said why: because the mix changed after the audited months it corrected the 271 press marks with recall and the false-mark rate only, `true = (marks - FPR x N) / (recall - FPR)`, "that correction does not depend on how common confrontation is, so it carries to the unaudited months". Then it listed, by figure, every rung this note designed: naive 320, recall only 616, times precision 269, audit prevalence 694, hand codes where audited 386. A theme-stratified cross-check gave 466, still rounding to 450.
- **(2026-10-25, measured) The seventh cell is CONFIRMED open by an independent reader.** Asked to fit the calibration model (hand code on classifier mark plus a month index, extrapolated over the two unaudited months) and to say whether anything in the bundle rules it in or out, the reader returned **504, reported as 500**, a different fifty-bucket from the call, and answered: **"Nothing in the bundle rules it in."** It argued against it on three grounds of its own (the audit stops in August, two themes appear only in September so no month or theme term can be fitted for them, and the month term is not significant at p = 0.088), but those are judgements a competent analyst could decide the other way, not a shipped fact. So the Gate C finding recorded above is not a paper worry: it is a reachable candidate on the shipped pack, it has no row in the candidate table and no `cand.*` assertion, and any repair of this number owes its closure.
