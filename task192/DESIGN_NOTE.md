# task192 design note

How many of a protest register's recorded actions were confrontational, when most of the record's labels
come from a classifier the association measures against hand coding. Architecture 3.

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
| Calibration | `gold_standard_subsample`, the association's own double-coding sample |
| World | Portugal, a conflict monitoring association, EUR |
| Register opened | 1 May 2026; reporting period 1 May to 30 October 2026 |
| As-of date | 2026-11-06 (the record extract); the trustees meet on 19 November |
| Guard | PASS at WARN; two WARNs answered below |

**Data-native sentence.** Two actions in three reach this register only through the press monitor, whose
classifier reads news text and assigns the action code, and the association's own double-coding sample
shows what that classifier does with a rare class: it puts a confrontational code on about half the
actions that carry one and on about one ordinary action in a hundred, and because the ordinary actions
outnumber the confrontational ones twenty to one, the actions it labels are neither all of them nor a
subset of them.

**The two WARNs the guard raised.**
- `repeat.gate_g` and `overuse.gate_g` (`method_or_model_selection`, 5 of the last 12, repeating task193):
  the other builds in the window select a model by back-test, by a reviewer's reach, by a conversion
  sized at its value and by a maturity correction. None selects between estimators that differ in which
  of an instrument's two error rates they carry, which is what separates the four candidates here.
- The driver sits at 0.10 against task189's left-censored averages and below that against every other
  card on file; no card and no lineage entry corrects a count for an instrument's sensitivity and its
  specificity together.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD15: the decision shape only, one figure committed at a
  date to a standing body about coordinated contention.
- `stumping/references/client/layer2-rigor-patterns.md`: this task type's filed pattern 1 is that
  reported events track media reach and the analysis must condition on the reporting proxy. This build
  takes the other half of the same instrument, not how far the press reaches but what its coder makes of
  what it reaches, which is the validation literature protest event analysis runs on.
- `guard.py mechanisms --objective anomaly-detection`, re-read after the remote merge: the spent drivers
  are a stock from arrivals and time unseen, a selected maximum against its own null, a dominant
  candidate holding the others down, regression to the mean, a paired difference's own interval,
  left-censored measurements, an aoristic weight, a pooled-test density, a conversion sized at its value,
  a measurement that suppresses what it measures and a threshold-avoidance excess. None corrects a count
  for a classifier's measured error.
- `guard.py check` over the whole corpus after the merge, including task266 and task157, which took
  architecture 2's mechanism and its structural triple.
- `guard.py nearest` and the batch's own reach, answered on the card's `differentiation`: **task446 v2**'s
  decisive quantity is a forward count for a population whose base rate has moved, and its error is
  carrying a yield measured on earlier populations onto that one; here nothing is carried anywhere, the
  double-coding sample and the record are the same items at the same time, and the error is that a
  correction built on one of the instrument's two arms is wrong whichever arm it takes, so neither route
  reaches the other's answer: there is no second population here for a yield to be carried to, and there
  is no recorded label set there to rebuild, its count being of outcomes that have not happened yet.
- **task448** completes a register that misses whole producers by estimating a second list's capture on
  the producers both lists hold and carrying it within route strata to the producers the register never
  saw; here nothing is missing from the record, every action is in it and the question is which class it
  belongs to, so the correction takes wrongly marked actions out as well as putting missed ones in,
  which a completeness estimate never does and cannot do.

## Default path

1. Read the accepted items of `registo_itens_imprensa.csv` with `relatos_rede_parceiros.csv` and
   `relatos_linha_publica.csv`, and resolve every reported place through `gazeteiro_localidades.csv`,
   current and former names alike.
2. Resolve the three routes, the two language editions of the Atlantic group and the reposted August
   month so that each action is counted once on the protocol's 2.1 grain, one theme at one locality on
   one calendar day.
3. Read the protocol's 2.2 codes and keep the actions the register carries under `CF`, `RF` or `DP`.
4. Count them for 1 May to 30 October 2026 and file that number.

**Ends on:** 178 confrontational actions.
**Golden:** 234 confrontational actions.

## Stump sentence

A competent solver resolves the three routes, builds the actions on the protocol's grain, applies the
protocol's confrontational codes and files **178 confrontational actions**, which counts the labels the
press classifier assigned rather than the confrontational actions the period held, because the
classifier reaches about half of them and marks about one ordinary action in a hundred.

## Three rules

- **Task type:** `conflict-protest-event-data-analysis`, the task type in Political Science & Public
  Policy that serves Anomaly Detection: turning multi-source reports into an event record and separating
  what happened from what the record's own instruments made of it.
- **Domain test:** the deciding quantity is the count of confrontational actions in a contentious event
  record, which protest event analysis estimates from a machine-coded corpus read against a hand-coded
  double-coding sample, because an automatic coder of news text misses a large share of a rare event type
  and marks a small share of the many ordinary ones. The field's own method carries both error rates into
  the count; a generalist counts the labels, or takes the wrong marks out, or divides by the recall.
- **Swap:** "how many of the parcels the belt recorded were damaged" counts a physical property a scanner
  reads directly. What breaks is that there is no coder reading news text, no hand-coding standard for it
  to be measured against and no protocol definition of the class being counted: the quantity becomes a
  physical count, the double-coding sample has nothing to double code, and nothing is left to estimate.
- **Layer 1:** the association's own pipeline makes all of it. The press monitor's item log carries every
  item the keyword list caught, accepted or rejected, at item grain; the same action arrives from up to
  three access routes and from two language editions of one media group; one month of partner reports was
  loaded twice and the import log carries both loads; the monitor's reception stamps are the collection
  server's UTC clock while the action times are local, and the clocks go back an hour on 25 October; the
  partner organisations' monthly returns arrive inside a PDF; the gazetteer carries superseded settlement
  names. None of it is placed to be caught and none of it decides the count.
- **Layer 2:** `field_method`. The methodological choice is what the classifier's labels are evidence of,
  and which of its two measured error rates the count has to carry.
- **Decisive step:** rebuild the count of confrontational actions among the actions the press monitor
  alone carries from the classifier's measured sensitivity and specificity together, so that the actions
  it missed are added and the ordinary actions it marked are taken out, and add the actions a filer coded
  by hand.
- **Not semantics:** every field, code, zone and place name read correctly still leaves 178 actions
  carrying a confrontational code, which is the correct count of the codes. The dictionary gives every
  field, the protocol defines the action grain and lists the confrontational codes, and the double-coding
  sample is a plain table of two codings. Reading all of it right is what produces the 178.
- **Not rule application:** the protocol files the action grain, the confrontational codes, the reporting
  period, which route's code the register keeps for an action, and that the count the bulletin states is
  of the actions that were confrontational and not of the codes the classifier assigned. No shipped
  sentence says how the classifier's labels are to be turned into that count: nothing names sensitivity,
  specificity, recall, precision, a correction, a false positive or a false negative, and a word sweep
  over every shipped file asserts it. The double-coding sample states two codings per sampled item and no
  rate at all.
- **Analyst test:** a strong analyst who resolves the three routes and the two editions, drops the
  reposted month, resolves the superseded place names and applies 2.1 and 2.2 exactly counts the actions
  the register carries under the confrontational codes and files 178 confrontational actions, the default
  path's `Ends on:`, where the period's record gives 234.
- **Estimand:** the protocol's 3.3, "Indicador 2, acoes de confronto: o numero das acoes registadas no
  periodo de relato que foram acoes de confronto na acepcao de 2.2. O codigo que o classificador do
  monitor de imprensa atribui e a leitura do classificador, que a amostra de dupla codificacao da
  associacao mede contra a codificacao manual. O numero que o boletim fixa e o das acoes que foram de
  confronto e nao o dos codigos atribuidos." Population, outcome, window and unit are all there; how the
  count is rebuilt is not.
- **No decoy:** nothing is planted to be caught. No block of items is copied, no memo argues a count, no
  stakeholder figure carries one, and no shipped file states a confrontational count, a rate, a
  sensitivity or a specificity. The double-coding sample is the association's own standing quality
  record, published with its methodology as every machine-coded event dataset publishes one.
- **No certified replay:** no published confrontational count ships. The earlier monthly bulletins report
  actions recorded and municipalities touched and never the confrontational ones, so no method can be
  recovered by reproducing a figure.
- **Lesson:** when most of a record's labels come from an instrument that both misses and over-marks, the
  count of the labelled units is not the count of the units: the misses and the false marks cancel only
  if the two error rates happen to balance at that prevalence, and only carrying both of them together
  rebuilds the count. No build on file teaches it.

## WHAT screen

The decisive step is the one above: carry the classifier's two measured error rates into the count. It
settles no part of the estimand.

| Part of the estimand | Settled by | The sentence that files it |
|---|---|---|
| Population | the protocol, not the decisive step | 3.2 files the reporting period and 2.1 the actions the register holds |
| Outcome | the protocol | 2.2 lists `CF`, `RF` and `DP` as the confrontational actions, and 3.3 says the count is of the actions that were confrontational |
| Window | the protocol | 3.2, 1 May to 30 October 2026 inclusive |
| Unit | the protocol | 2.1, one theme at one locality on one calendar day, however many reports |
| Comparison | none; the indicator is a level | 3.3 states a count, against nothing |

Two or more estimators of that one filed quantity stand after it is filed: the coded count, the coded
count with the classifier's false marks removed, the coded count scaled by its recall, and the count
rebuilt from both error rates. The record's own structure separates them, because the double-coding
sample shows a recall near one half against a false-mark rate near one in a hundred over a negative pool
twenty times the size of the positive one.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the actions the register carries under the confrontational codes | 2.2 lists the codes and 3.3 names the count | `codigo_acao` is a column of every report file | yes, the first group-by anyone writes | none | the battery finds the duplicate feeds, not this | one filter and one count | readable |
| 1 the coded count with the classifier's false marks taken out | no sentence names a false mark | the sample's two coding columns invite the comparison | yes, the precision reflex: of the ones it marked, this share were right | none | no | one ratio | readable |
| 2 the coded count scaled by the classifier's recall | no | the sample's two coding columns again | yes, the recall reflex: it finds this share, so divide by it | none | no | one ratio | readable |
| 3 the count rebuilt from both error rates together (decisive) | no shipped sentence names sensitivity, specificity, recall, precision, a correction, a false positive or a false negative, asserted by a word sweep over every shipped file; 3.3 says only that the count is of the actions and not of the codes | no column holds an error rate: the sample is two codings per item and the rates are built from it | no reflex: the two reflexes above each carry one error rate and file a different number | nothing scores a count; the earlier bulletins report actions and municipalities, never confrontational actions | the battery finds the two editions, the reposted month and the clocks and leaves the count open | no: the four candidates are 126, 178, 234 and 336 from the same rows | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | action | one theme at one locality on one calendar day, however many reports, 2.1 | one report, so a double-reported action counts twice | the count changes | 2.1 quoted; asserted |
| SF2 | confrontational action | an action that was of a kind 2.2 lists, whatever code the record carries | an action whose recorded code is `CF`, `RF` or `DP` | the count is rung 0, 178 | 3.3 quoted, the count is of the actions and not of the codes assigned; asserted |
| SF3 | the confrontational codes | `CF`, `RF` and `DP` | `CF` alone, or any code a report's text calls violent | the count changes | 2.2 quoted, which lists the three; asserted |
| SF4 | the reporting period | actions dated 1 May to 30 October 2026 inclusive | the calendar half year, or to the extract date | the count changes | 3.2 quoted and the prompt's period; asserted |
| SF5 | which code an action carries | the code of the report the register keeps: a filer's code where one exists, the classifier's otherwise, 2.6 | the classifier's code wherever one exists | the corrected population changes | 2.6 quoted; asserted |
| SF6 | the double-coding sample | the association's sample of items the classifier coded, with the hand coding beside it | a sample of all actions, or a sample of confrontational actions | the error rates change | 4.5 quoted and the dictionary's scope line; asserted that every sampled item is a press-monitor item |
| SF7 | the action date | the local calendar day the register fixes, which no reception stamp overrides | the reception stamp's date | up to two actions move day | the dictionary's two sentences; asserted that no action's date moves |
| SF8 | a locality | the gazetteer's settlement, with superseded names resolved | the free-text place name as reported | localities split, actions do not | 2.3 and the gazetteer's name-state column; asserted |
| SF9 | the reposted month | each action counted once however many loads carry its reports | the month's reports counted twice, or the month dropped | the report counts change, the action count does not | the import log's two entries and the repeated report identifiers; asserted both ways |
| SF10 | the two language editions | one action however many editions report it | one action per edition | the report counts change, the action count does not | the dictionary's report-identifier sentence; asserted |
| SF11 | rounding | the count as a whole number of actions | the count to the nearest ten | `same call`, asserted: the estimate is 234.13 and no reading of the rounding moves it off 234 |
| SF12 | ties | none: the four candidate counts are 126, 178, 234 and 336 | two candidates on one count | `same call`, asserted pairwise distinct |
| SF13 | the accepted items | the items the press monitor accepted, which the register carries | every matched item, rejected ones included | rejected items are not actions | 4.2 quoted and the dictionary's acceptance column; asserted |
| SF14 | the extract | the record as extracted on 6 November 2026 | the record as at the period's close | `same call`, asserted: no action dated inside the period is reported after the period's close |
| SF15 | actions outside the period | excluded from the count | included because their reports arrived inside it | the count changes | 3.2 quoted, which fixes the period on the action's date; asserted |
| SF16 | the hand coding | the standard the sample measures the classifier against | one more opinion to be averaged with the classifier's | the error rates change | 4.5 quoted, which names the hand coding as the association's own standard; asserted |
| SF17 | a report the gazetteer does not place | not an action, so outside every count | an action at an unknown locality | the count changes | 2.5 quoted; asserted |
| SF18 | the register's opening | 1 May 2026, with no action carried in | an action before the register opened | nothing to count before it | 3.2 quoted; asserted that no action predates 1 May 2026 |

## Ladder

| Rung | The estimate | Confrontational actions |
|---|---|---|
| 1 | the coded count with the classifier's false marks taken out, the precision read | 126 |
| 0 | **default:** the actions the register carries under the confrontational codes | **178** |
| 3 | **answer:** the count rebuilt from both of the classifier's measured error rates | **234** |
| 2 | the coded count scaled by the classifier's recall | 336 |

Measured on the cut pack, not on a model: the register holds 4,790 actions in the reporting period, of
which 4,357 carry a press monitor report and take its classifier's code and 433 reach the register only
through a partner organisation or the public line and take the filer's. The register carries a
confrontational code on 153 of the first group and 25 of the second. The coding desk's two rounds hand
coded 2,600 of the monitor's reports and returned 59 agreed confrontational, 61 the classifier missed,
30 it marked wrongly and 2,450 agreed ordinary, which is a recall of 0.4917 and a false-mark rate of
0.0121. Rung 3's raw figure is 234.134 actions.

**Separation.** 126, 178, 234 and 336 are four distinct counts, each at least 31 per cent from the next
(126 to 178 is 41 per cent, 178 to 234 is 31 per cent, 234 to 336 is 44 per cent). Each is the complete
output of a competent pipeline on the same rows. The answer is third of the four and bracketed, so no
solver reaches it by stopping early and none by correcting hardest: the two corrections that carry one
error rate land either side of it, and the decisive move, 336 down to 234, is the largest on the ladder.

**The variants a careful analyst tries, measured.** The decisive estimate was computed five more ways on
the shipped bundle, and the spread is reported rather than claimed:

| Variant | Figure | Standing |
|---|---|---|
| the correction written as the sample's confusion matrix inverted over the observed counts | 234.134 | identical to the golden by construction, asserted to 1e-9 |
| the rates read on the sample rows whose action also reached another route, against all of them | 234.134 | identical: the sample's population is the corrected population, 2.6 and 4.5 |
| a continuity adjustment of half a case in each cell of the table | 232.403 | not licensed: a continuity adjustment is for an empty cell and none of the four is empty (59, 61, 30, 2450), asserted |
| the correction taken inside each hand-coding round and added | 235.060 | ruled out by 4.5, which files the period's sample as the two rounds together, measuring the classifier over the period's accepted reports as a whole |
| the correction taken inside each dispute theme and added | 235.925 | ruled out by the same sentence; the sample is a simple random sample of the reports and is not stratified, and four themes hold three or fewer agreed confrontational rows |

The widest of the five sits 1.8 actions from the golden, so no variant crosses the next rung and the
three that differ are each closed by a quoted sentence or by the table's own cells.

**Robustness and fairness.** The figure sits 0.134 from the centre of its bin, 0.37 from the nearest
edge. The truth behind the simulated record is 239 confrontational actions, 2.1 per cent above the
estimate, so the estimator is fair as well as determinate; the generator asserts the gap.

**The grid.** Two axes, how the reports are resolved and which error rates the count carries:

| | false marks out | labels as they stand | both rates | recall only |
|---|---|---|---|---|
| the three routes resolved to actions | 126 | 178 | **234** | 336 |
| each accepted report counted as an action | higher in every column, asserted | | | the decisive column still the only one the protocol asks for |

Every cell is a named figure. The decisive column is the only one that answers the protocol's question,
and it is the column least moved by a solver who fails to resolve the routes, because the correction is a
ratio of the sample's own cells and not of the record's volume.

**Dominance.** The ordinary actions outnumber the confrontational ones about twenty to one, so the
classifier's one-in-a-hundred false-mark rate puts 30 wrong marks in the sample against 61 misses: the
two errors are of the same order and neither cancels the other, which is what makes all three easy routes
land on different wrong numbers.

**Worth of each rung, on the graded quantity.** Rung 1 to rung 0 is 52 actions, rung 0 to rung 3 is 56,
and rung 2 to rung 3 is 102. Nothing between the rungs is worth less than 52 actions, and every rung is
satisfying to stop at: each is the whole output of a pipeline whose every input figure is correct.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which actions are in the count | 3.2 files the period and 2.1 the action; asserted |
| 2 | Unit of account | the item, the report, the action | 2.1 files the action; asserted |
| 3 | Attribution window | which day an action falls on | the register's local action date, which no reception stamp overrides; SF7, asserted |
| 4 | As-of dating | the record at the extract | the manifest files 6 November 2026; SF14, asserted |
| 5 | Version basis | the reposted month and the superseded place names | the import log and the gazetteer; SF9, SF8, asserted |
| 6 | Denominator | none: the answer is a count | nothing to close, stated |
| 7 | Weighting | the double-coding sample is drawn simple at random from the press monitor's items, so no weights | 4.5 states the draw; asserted that every sampled item is a press item and that the sample is not stratified |
| 8 | Window length | the reporting period | 3.2; asserted |
| 9 | Boundary inclusivity | 1 May and 30 October | 3.2 states both inclusive; asserted that actions fall on both days |
| 10 | Rounding path | the count to a whole action, rounded once at the end | SF11; asserted that the raw 234.13 is 0.37 from its bin edge |
| 11 | Tie-break | two candidates on one count | none: 152, 182, 225 and 285 are pairwise distinct, asserted |
| 12 | Maturity and censoring | reports still arriving | the period closed a week before the extract; asserted that no action dated in the period is reported after the extract |
| 13 | Order of operations | resolve the routes then read the codes, or read then resolve | C1: a duplicate report carries the same identifier, theme, locality and day, so either order gives the same actions, asserted |
| 14 | Row order | the item log's own order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the three routes, the two editions, the reposted month | C1: duplicates resolve to one action under any handling, asserted |
| 16 | Identity normalisation | place names, partner organisation codes | the gazetteer's superseded names; the partner codes are read only by the asks; asserted |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | items, reports, actions | the dictionary names each; the indicator reads actions only, asserted |
| 19 | Code and status semantics | the route codes, the action codes, the acceptance column, the sample's two coding columns | the protocol and the dictionary; the codes are read correctly on every rung |
| 20 | Integerisation | the count is a whole number of actions | 3.3; the raw 234.134 rounds to 234, asserted |
| 21 | Clause scope | 2.1 per theme per locality per day; 2.6 per action | both paragraphs state their scope; asserted |
| 22 | Forward window contents | none: the count is for the closed period | the call is retrospective with its reason, that the bulletin reports the period that closed and the trustees' vote of 19 November sets the next year's field budget on it |

## Literal reader

Executing the prompt, paragraphs 2.1 to 2.6, 3.2, 3.3, 4.2 and 4.5 of the protocol, the dictionary, the
gazetteer and the manifest word for word selects the accepted reports of the three routes between 1 May
and 6 November 2026, resolves them to actions at gazetteer settlements on the protocol's grain, keeps the
actions dated inside the reporting period, and asks how many of them were confrontational actions on
2.2's list, the count being of the actions and not of the codes the classifier assigned. The text is
silent on how the classifier's labels become that count, so every option was computed on the same rows:
the coded count gives 178, the coded count with the classifier's false marks taken out gives 126, the
coded count scaled by its recall gives 336, and the count rebuilt from both measured error rates gives
234, which the double-coding sample's own four cells fix. The easy three are easy estimators of the same
literal estimand, not other readings of it, and every other term and convention has an SF row ruled out
by a quoted sentence or asserted to give the same call.

## Oracles

- `amostra_dupla_codificacao.csv`, the association's own double-coding sample, carries two codings per
  sampled press item and no rate, no count and no method; it is the raw material the decisive step reads
  and it ties under every rung, because each rung reads a different pair of its four cells.
- The earlier monthly bulletins report actions recorded and municipalities touched and never
  confrontational actions, so they tie under every rung.
- `registo_importacoes.csv` confirms which month was loaded twice; it ties under every rung and the count
  is asserted invariant to the resolution.
- `gazeteiro_localidades.csv` confirms the settlements and their municipalities; it ties under every rung.
- `totais_por_via.csv` and `excecoes_geocodificacao.csv` are route control totals and the reports the
  association could not place; neither carries an action code and both tie under every rung.
- `manifesto_extracao.csv` states each file's rows, range and extract date and settles the one designed
  disagreement in the ask layer without naming a level.
- No control, published figure or corpus states a confrontational count, a rate or an error rate.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per fortnight, the actions recorded, the municipalities touched and the share of those actions the partner network reported | 3 per fortnight, 13 fortnights | the construction's own output on the segment the trustees want anyway, the actions the count is taken from | the bulletin's standing table | D5 scope: the protocol's fortnights run from 1 May and the last one ends with the period, so it has fifteen days, while fixed fourteen-day blocks make a fourteenth fortnight holding 30 October alone and leave 52 actions out of the thirteenth | D6 the partner share is per action, not per report; D1 the re-imported month doubles reports and no actions | item log, partner reports, public line, gazetteer, protocol, dictionary, manifest, import log; 12 columns | 4 stops, lazy delta 9 of 13 fortnights | the bulletin's own standing table |
| A2 per access route, the reports received, those the association could not place and the median minutes from action to report | 3 per route, 3 routes | the audit trail from an input the call consumes, through rows it never reads, to the route's own control total | the pipeline review the data manager runs each period | D4 absence as the signal: the reports that could not be placed are held in a separate exceptions file no habitual join reaches | D8 the filing stamp is the publisher's zone and the clocks go back on 25 October; D6 the exceptions file is per report and the route totals per day | exceptions file, route totals, item log, partner reports, public line, dictionary, manifest; 11 columns | 4 stops, lazy delta 2 of 3 routes | an ingest pipeline's own period review |
| A3 per partner organisation, the reports it filed, those filed after the period closed and the euros paid under its data agreement | 3 per partner, 7 partners | an input reconciled to another system's total, the gap made of devices | the finance office settles the data agreements | D2 version: one agreement was amended mid-period and the rate paid is the amended one, which the superseded schedule does not carry | D7 one partner filed under two organisation codes after a merger; D8 the filing stamp against the period close | partner monthly tables in PDF, agreement schedule, amendment, route totals, manifest, dictionary; 13 columns | 5 stops, lazy delta 3 of 7 partners | the finance office's quarterly settlement |

**The main population's zero counts.** Zero device rows and zero hazard rows in the actions and episodes
the share rests on: every device sits in the exceptions file, the agreement schedule, the amendment or the
partner monthly tables, none of which carries an action. Deleting every device leaves the share exactly as
hard, asserted by count.

**The hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| D8 the filing stamp's zone and the 25 October clock change | A2, A3 | A2 one route's median by 41 minutes, A3 two partners' late-filing counts |
| D6 grain | A1, A2 | A1 the partner share in nine fortnights, A2 one route |
| D1 the re-imported month | A1, A2 | A1 the partner share in two fortnights, A2 one route's received count |

**The referee.** `manifesto_extracao.csv` states each file's rows, range and extract date and settles the
one designed disagreement, the exceptions file's extent, without naming a level.

**The cracker sheet.** The cracker filed 234 confrontational actions, ran the hygiene battery,
executed every filed paragraph and matched every control total.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 actions recorded, the last fortnight | fixed fourteen-day blocks, so the last one ends on 29 October and a fourteenth holds 30 October | 647 | 683 | miss |
| A1 share the partner network reported, fortnight 7 | counts reports, not actions | 24.0 per cent | 22.7 per cent | miss |
| A2 reports received, the partner network | counts the rows of the partner file, so the reposted August month counts twice and the unplaceable reports are missing | 1,463 | 1,298 | miss |
| A2 reports that could not be placed, the press monitor | the item log alone, which holds only the items it placed | 0 | 148 | miss |
| A2 median minutes from the action to the report, the press monitor | reads the monitor's reception stamp as local time | 51.0 | 111.0 | miss |
| A3 euros paid, the amended partner | the schedule's rate for the whole period, without the July adenda | 798 | 892 | miss |
| A3 reports filed, the merged partner | one delivery code | 122 | 156 | miss |

**Pair ceiling:** 39.5
**Mirror leakage:** 20.0

## Tried and rejected

- The seed's own architecture, a filed definition of a campaign plus a verification subsample that
  blesses one reading of it: the definition makes the count rule application and the subsample is a
  certified replay, both of which the client's rules ban as the decisive step. Re-rooted at the draw.
- Recovering the number of operations from a periodogram of the daily action counts: the number of peaks
  depends on the window, the detrending and the significance threshold, so the count would not be
  determinate. Replaced by the intervals read off the locations each operation alone touches, which needs
  no threshold.
- Letting the institute's flag file group the location-days into episodes: that ships an artifact that
  answers the decision question wrongly, which Gate G forbids. The flag file flags days and groups
  nothing.
- (architecture 2) A confrontation risk filed with an eight-week horizon from each episode's opening, the
  cohort the episodes opened in a window that ends a week before the extract: measured on the model, the
  complete-case share over the episodes with a full eight weeks of follow-up is an unbiased estimate of
  the same quantity and lands within a point of the golden, so the easy route reaches the answer. A filed
  horizon always leaves that route available, and shortening the horizon until the route starves also
  thins the risk set the estimate needs. Replaced by the whole-life estimand, where the long-running open
  episodes make every complete-case route wrong: measured, restricting to the episodes opened more than
  seventy days before the extract gives 14 per cent, rung 0's figure, not the golden.
- (architecture 2) Grading the share to one decimal: the weekly and fortnightly readings of the decisive
  estimate give 17.05 and 16.99 against the daily 17.03, which a one-decimal figure splits. Graded as a
  whole percentage with the episode count beside it, every nonparametric reading files 17 per cent and 108
  episodes.
- (architecture 2) A ranked watch list of the live episodes by remaining confrontation risk: the remaining
  risk is a monotone function of an episode's age alone, so the ranking degenerates to the youngest
  episodes first and a solver lands it without the insight. Dropped for the cohort share.
- (architecture 2) The whole competing-exit architecture, designed, built and gated: on the remote merge
  of 2026-10-17 task266 arrived with the same mechanism in other nouns (the share of spells that end one
  way when the others end another, a cumulative incidence against a product-limit survival), and task157
  arrived with the same gap, decisive pattern and decision type (time, G12, quantity_figure) while
  task190 v2 took the stakeholder role. Re-rooted at the draw rather than shipped into a clone finding.
- (architecture 3) Correcting the count by the classifier's precision alone, or by its recall alone: each
  carries one of the two measured error rates and lands on 152 and 285, which is why both are rungs
  rather than the answer.
- (architecture 3) A double-coding sample that verifies every classifier positive and a sample of its
  negatives, which is what a real quality desk draws: it forces a weighted estimator and leaves two
  defensible weightings of the same cells, so the sample is drawn simple at random from the press
  monitor's items and paragraph 4.5 says so.

## Architecture 2, blocked at the draw by the remote merge

Architecture 2 asked what share of the register's dispute episodes would have recorded a confrontational
action by the time they closed, with a quiet close treated as the other way an episode ends rather than
as an observation that stopped. It was drawn, designed, built and gated: 635 episodes in the cohort, 89
with a confrontational action at the extract, 312 closed quietly, 234 still open, and 108 episodes, 17
per cent, on the decisive estimate, against 89 on the recorded count, 141 on the known outcomes and 178
on a product-limit survival. The pack carried 17 files in four formats and a 25,688-row item log, with
108 generator assertions, 99 independent checks in a verifier that read only the bundle, two
byte-identical rebuilds, `figures_check.py` exit 0 and `precut.py` at 0 FAIL and 0 WARN.

It is spent for one reason outside the build. The remote merge of 2026-10-17 brought in task266, drawn
the same day in sociology-demography, whose driver is that mechanism in other nouns, and the clone check
reads mechanisms rather than nouns; the same merge brought in task157, which took the structural triple,
and task190 v2, which took the stakeholder role. Competing risks against censoring is therefore on this
slot's banned list with the rest.

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

**How architecture 2 clears each of them.** The decisive step is none of the six: nothing is captured from
an overlap (the duplicate reports collapse to one action and the share is invariant to them, asserted);
nothing extreme is selected and no null of extremes is built; no external driver and no lag appear; the
share is a share of episodes with no composition against any rate, and the mix of dispute themes is never
read; every report has arrived, the import log closes the one month that arrived twice, and the gap is in
the outcome rather than in the recording; and no detection threshold exists, the action grain being filed
and every accepted item carried. Architecture 1's periodic-process decomposition is gone with its unit:
no interval, tempo, cycle or period is computed anywhere in the golden.
