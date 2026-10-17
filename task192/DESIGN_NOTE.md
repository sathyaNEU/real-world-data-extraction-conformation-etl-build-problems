# task192 design note

How much of a monitoring register's dispute episodes will have turned confrontational by the time they
close. Architecture 2.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task192.json`, architecture v2, registered 2026-10-17T14:59:48Z |
| Domain, task type | political-science-public-policy, `conflict-protest-event-data-analysis` |
| Objective | Anomaly Detection & Diagnostics |
| Shape | 17, periods around a change point, one workbook and one chart |
| Decision | quantity_figure, a share with the number of episodes it stands for |
| Gap | time, then population |
| Gate G | `method_or_model_selection`; decisive generator G12, then G7 |
| Strategy | `other`: no vocab strategy names a competing exit |
| Layer 2 | `estimation_fit`, own pattern `own:competing-exit-not-censoring-in-an-episode-register` |
| World | Portugal, a conflict monitoring association, EUR |
| Register opened | 1 May 2026; reporting period 1 May to 30 October 2026 |
| As-of date | 2026-11-06 (the record extract); the trustees vote the 2027 field budget on 19 November |
| Guard | PASS at WARN; three WARNs answered below |

**Data-native sentence.** A dispute episode in this register ends one of two ways and the register records
both: it reaches a confrontational action, or it goes quiet and the protocol's twenty-one clear days close
it; at the extract 312 of the period's 635 episodes have closed quietly, 89 have already recorded a
confrontational action and 234 are still open, so the one number the bulletin owes is a number about
episodes whose lives are not all over, and an episode already closed is out of the population that can
still produce one while an episode still running is not.

**The three WARNs the guard raised.**
- `overuse.objective` (anomaly-detection in 5 of the last 12): the lane owns the objective for this slot
  and the re-root keeps it; the draw varies every other axis.
- `repeat.gate_g` and `overuse.gate_g` (`method_or_model_selection`, 7 of the last 12, repeating task193):
  the four other builds in the window select a model by back-test (task154), by a reviewer's reach
  (task190), by a conversion sized at its value (task185) and by a maturity correction (task445). None
  selects between estimators that differ only in whether a unit that has reached its other terminal state
  is still in the population at risk, which is what separates the four candidates here.
- `test.same_driver_older` against task445 v1 (differentiated on the card): task445 completes a period for
  reporters whose reports have not arrived, so every unit's outcome has already happened and the gap is in
  the recording. Here every report has arrived and the gap is in the outcome.

**Sources read.**
- `analytical_tasks/02_anomaly_detection/` seed AD15: the decision shape only, one figure committed at a
  date to a standing body about coordinated contention. Its own architecture turns on a stated definition
  plus a verification subsample that blesses one reading, which is rule application with a certified
  replay, so nothing but the shape is kept.
- `stumping/references/client/layer2-rigor-patterns.md`: this task type's three filed patterns are media
  reach, onset against ongoing episodes, and overdispersion. Pattern 2's episode-with-a-peace-interval is
  the unit this build uses; the rigor is written here as its own pattern, because the client's
  competing-exit pattern is filed for three other domains and for none of them on an event register whose
  episodes are built from reports by a filed peace interval.
- `guard.py mechanisms --objective anomaly-detection`: the spent drivers are a stock from arrivals and
  time unseen (task190), a selected maximum against its own null (task191), a dominant candidate holding
  every other down (task193), regression to the mean (task194), a paired difference's own interval
  (task195), left-censored measurements with several limits (task189) and an aoristic weight (task184).
  None turns on a unit leaving the population at risk.
- `guard.py check`: nearest driver 0.06 (task142), every other under 0.06.

## Default path

1. Read `registo_itens_imprensa.csv`, `relatos_rede_parceiros.csv` and `relatos_linha_publica.csv`, keep
   the accepted items, and resolve the three routes, the two language feeds of one media group and the
   re-imported month so each action is counted once.
2. Resolve each reported place through `gazeteiro_localidades.csv`, including the superseded names, to a
   settlement and its municipality.
3. Build actions on the protocol's §2.1 grain, one dispute theme at one locality on one calendar day, and
   read the protocol's §2.2 codes so that `CF`, `RF` and `DP` are the confrontational ones.
4. Build the register's dispute episodes on §3.1: one municipality and one theme, opening on the day of the
   first action and closing when twenty-one clear days have passed with no action, and keep the 635
   episodes whose opening day falls between 1 May and 30 October 2026.
5. Count the episodes that record a confrontational action, divide by the 635 and file the share.

**Ends on:** 14 per cent, 89 episodes.
**Golden:** 17 per cent, 108 episodes.

## Stump sentence

A competent solver cleans the three routes, applies the protocol's episode rule to the letter, counts the
89 episodes in the period's cohort that have recorded a confrontational action and files **14 per cent, 89
episodes**, which is the confrontation the record has already seen rather than the confrontation the
cohort will have recorded by the time its episodes close, because 234 of the 635 episodes are still open
and the 312 that have already closed quietly can never produce one.

## Three rules

- **Task type:** `conflict-protest-event-data-analysis`, the task type in Political Science & Public Policy
  that serves Anomaly Detection: building contentious episodes out of multi-source reports and separating
  what the record has seen from what the period's contention actually did.
- **Domain test:** the deciding quantity is the share of contentious episodes that turn confrontational,
  which event-data analysis estimates over the life of an episode from a register in which an episode ends
  either in a confrontation or in demobilisation under a filed peace interval, so a demobilised episode is
  out of the population at risk while an episode still mobilised is not. The field's own estimate of that
  share takes both ends of an episode as outcomes and the open episodes as episodes whose end is still to
  come; a generalist reads the recorded confrontations as the answer.
- **Swap:** "how many of the shops in the register had a break-in before they closed" counts rows against
  rows, because a shop is a standing unit with one state, not a run of actions by contending parties at a
  place that the protocol's twenty-one clear days turn into an episode. What breaks is the unit itself: no
  episode can be built, demobilisation has no meaning to compete with the outcome, and nothing is left to
  estimate.
- **Layer 1:** the association's own pipeline makes all of it. The media monitor's item log carries every
  item it matched, accepted or rejected, at item grain; the same action arrives from up to three access
  routes and from two language feeds of one media group; one month of partner reports was loaded twice and
  the import log carries both loads; report filing stamps are in the publisher's zone while the register's
  action dates are local, and the clocks go back an hour on 25 October inside the window; the partner
  organisations' monthly tables arrive inside PDFs; the gazetteer carries superseded settlement names.
  None of it is placed to be caught and none of it decides the share.
- **Layer 2:** `estimation_fit`. The methodological choice is what an episode that has already closed
  quietly is in the estimate: a unit whose observation stopped, or a unit that has left the population at
  risk.
- **Decisive step:** estimate the cohort's confrontation share over the whole life of its episodes with
  demobilisation treated as the other way an episode ends, so that a closed quiet episode is out of the
  at-risk population and only the open episodes carry a confrontation still to come.
- **Not semantics:** every field, code, zone and place name read correctly still leaves 89 recorded
  confrontational episodes, 312 quiet closures and 234 open episodes, all three correct. The dictionary
  gives every field, the protocol defines the action grain, the codes, the episode and the indicator, and
  the calendar note gives the clock change. Reading all of it right is what produces the 89, which is the
  wrong answer's input.
- **Not rule application:** the protocol files the action grain, the confrontational codes, the twenty-one
  clear days, the reporting period and the indicator's population, and states that the figure for a period
  whose episodes have not all ended is an estimate. No shipped sentence says how that estimate is made:
  nothing names a risk set, a survival or hazard quantity, a competing or terminal event, a cumulative
  incidence, a censoring rule or a projection, and a word sweep over every shipped file asserts it.
- **Analyst test:** a strong analyst who resolves the three routes and the two feeds, drops the re-imported
  month, resolves the superseded place names and applies §2.1, §2.2 and §3.1 exactly counts the cohort's
  recorded confrontational episodes and files 14 per cent, 89 episodes, the default path's `Ends on:`,
  where the cohort's own record gives 17 per cent, 108 episodes.
- **Estimand:** the protocol's §3.3: "Indicator 3, the confrontation rate: of the dispute episodes opened
  in the reporting period, the share that record at least one confrontational action before the episode
  closes, as a whole percentage, with the number of episodes it stands for. Episodes still open when the
  record is extracted belong to the period's cohort, and the indicator covers the whole life of each
  episode, so for a period whose episodes have not all ended the figure is an estimate." Population, the
  not-yet-ended members included, outcome, window, unit and comparison are all there; how the estimate is
  made is not.
- **No decoy:** nothing is planted to be caught. No block of reports is copied, no memo argues a share, no
  stakeholder figure carries one, and the association has never published a confrontation rate: the Watch
  register opened on 1 May 2026 and this is its first full reporting period. The re-imported month is an
  ordinary pipeline fact, visible in the import log, and the share is invariant to how it is resolved.
- **No certified replay:** no published confrontation rate or episode count ships. The earlier monthly
  bulletins report actions recorded and municipalities touched and never episodes, so no method can be
  recovered by reproducing a figure.
- **Lesson:** in a register where a unit can reach the outcome or leave for good, the share that will
  reach the outcome is neither what the record has already seen, nor the share among the units whose story
  has finished, nor what a survival curve gives when leaving for good is treated as an observation cut
  short: the units that have left for good are out of the population at risk and the ones still running
  are the only ones with the outcome still to come. No build on file teaches it.

## WHAT screen

The decisive step is the one above: estimate the cohort's share with demobilisation treated as the other
end of an episode rather than as an observation cut short. It settles no part of the estimand.

| Part of the estimand | Settled by | The sentence that files it |
|---|---|---|
| Population | the protocol, not the decisive step | §3.3 "of the dispute episodes opened in the reporting period", with §3.2's 1 May to 30 October 2026 and "episodes still open when the record is extracted belong to the period's cohort" |
| Outcome | the protocol | §3.3 "record at least one confrontational action before the episode closes", with §2.2's codes `CF`, `RF`, `DP` |
| Window | the protocol | §3.2 for the opening window; §3.3 "covers the whole life of each episode" for the outcome window |
| Unit | the protocol | §3.1, one municipality and one dispute theme, opened by its first action and closed by twenty-one clear days |
| Comparison | none; the indicator is a level | §3.3 states a share of the cohort, against nothing |

Two or more estimators of that one filed quantity stand after it is filed: the recorded share, the share
among the episodes whose outcome is known, a product-limit survival of the time to a confrontational
action, and the cumulative share with demobilisation as the competing end. The register's own structure
separates them, because 312 of 635 episodes have demobilised and 234 are open, and only the last estimator
keeps a demobilised episode out of the at-risk population while leaving the open ones in it.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex | 4 control bench | 5 hygiene | 6 linear | Verdict |
|---|---|---|---|---|---|---|---|
| 0 the episodes that have already recorded a confrontational action | §3.3 names the share, and the count of episodes that have recorded one is the first thing anyone computes | the register the solver builds carries the confrontational action date | yes, the first group-by anyone writes | none | the battery finds the duplicate feeds, not this | one division | readable |
| 1 the share among the episodes whose outcome is known | no sentence names a known outcome | the open episodes are visible once the register is built | yes, the complete-case reflex | none | no | one filter and one division | readable |
| 2 a product-limit survival of the time to a confrontational action, the quiet closures carried as observations that stop | no | the episode's last action date is in the register the solver builds | yes, the survival reflex for data that is not fully observed | none | no | no | readable |
| 3 the cumulative share with demobilisation as the other end of an episode (decisive) | no shipped sentence names a risk set, a competing or terminal event, a cumulative incidence, a censoring rule, a survival, a hazard or a projection, asserted by a word sweep over every shipped file; §3.3 says the figure is an estimate and says nothing about how | no column marks an episode's state, at risk or out of it: the register is built by the solver from reports, and the protocol gives only the action grain and the peace interval | no reflex: of the three groupings a solver reaches for, two ignore the open episodes and the third gives the quiet closures a confrontation each | nothing scores a share; the earlier bulletins report actions and municipalities, never episodes | the battery finds the two feeds, the re-import and the zones and leaves the share open | no: the four candidates are 89, 141, 178 and 108 episodes from the same rows | silent |

## Semantic fork table

| id | term or convention | golden reading | alternative | call under it | ruled out by |
|---|---|---|---|---|---|
| SF1 | dispute episode | one municipality and one theme, opened by its first action, closed when twenty-one clear days pass with no action, §3.1 | a run of actions at one locality, or one municipality whatever the theme | the cohort size and every count change | §3.1 quoted, which names the municipality and the theme; asserted |
| SF2 | action | one theme at one locality on one calendar day, however many reports, §2.1 | one report, so a double-reported action counts twice | the action counts change, the episode set does not | §2.1 quoted; asserted that the share and the episode set are invariant to report-level duplication |
| SF3 | confrontational action | an action coded `CF`, `RF` or `DP`, §2.2 | any action the report text calls violent, or `CF` alone | the share changes | §2.2 quoted, which lists the three codes; asserted |
| SF4 | the reporting period | openings from 1 May to 30 October 2026 inclusive, §3.2 | the calendar half year, or openings to the extract date | the cohort changes | §3.2 quoted and the prompt's period; asserted |
| SF5 | the cohort | every episode opened in the period, the open ones included, §3.3 | the episodes that have ended | the share is rung 1, 22 per cent | §3.3 quoted, "episodes still open ... belong to the period's cohort"; asserted |
| SF6 | before the episode closes | at any time in the episode's life, including after the period's close, §3.3 | only actions dated inside the reporting period | the count is 110 of 635 and the share is still 17 per cent | §3.3 quoted, "covers the whole life of each episode", and the manifest's extract date; asserted both ways on the share |
| SF7 | the episode's own dates | the opening day is the first action's day and the closing day the last action's, §3.1 | the closing day is the day the twenty-one clear days complete | every episode's length moves by 21 days | §3.1 quoted, "the episode's last day is the day of its last recorded action"; asserted |
| SF8 | twenty-one clear days | twenty-one calendar days with no action at that municipality for that theme, §3.1 | working days, or twenty-one days inclusive of the action day | the episode set changes | §3.1 quoted, "twenty-one consecutive calendar days"; asserted |
| SF9 | a locality | the gazetteer's settlement, with superseded names resolved | the free-text place name as reported | localities split and episodes split | §2.3 and the gazetteer's superseded-name column; asserted that every reported name resolves to one settlement |
| SF10 | the municipality | the gazetteer's municipality for the settlement | the district, or the reported municipality text | the episode unit changes | §2.3 quoted; asserted |
| SF11 | the action date | the local calendar day the register files, which no report clock overrides | the report's filing stamp converted from the publisher's zone | up to two actions move day | the dictionary's two sentences, one for the register's action date and one for the filing stamp; asserted that no action's date moves |
| SF12 | the re-imported month | each action counted once however many loads carry its reports | the month's reports counted twice, or the month dropped | the report counts change, the share does not | the import log's two entries for one month and the repeated report identifiers; asserted both ways |
| SF13 | the two language feeds | one action however many feeds report it | one action per feed | the report counts change, the share does not | the dictionary's report-identifier sentence; asserted |
| SF14 | rounding | the share as a whole percentage and the episodes as a whole number | one decimal on the share | `same call`, asserted: 17.03 per cent rounds to 17 either way and the episode figure is 108 |
| SF15 | ties | none: the four candidate shares are 14, 17, 22 and 28 per cent | two candidates on one share, which could not be separated | `same call`, asserted pairwise distinct |
| SF16 | the accepted items | the items the media monitor accepted, which the register carries | every matched item, rejected ones included | rejected items are not actions and the action set would grow | the dictionary's acceptance column and §4.2; asserted |
| SF17 | the extract | the record as extracted on 6 November 2026 | the record as at the period's close | SF6's reading; the share is 17 per cent either way | the manifest's extract date, quoted; asserted |
| SF18 | episodes carried in from before the register opened | none: the register opened on 1 May 2026 and carries no episode from before it, §3.2 | the first action in May continues an April episode | the cohort would be unknowable | §3.2 quoted; asserted that no action predates 1 May 2026 |

## Ladder

| Rung | The estimate | Share | Episodes |
|---|---|---|---|
| 0 | the episodes that have already recorded a confrontational action | **14 per cent** | **89** |
| 1 | the share among the episodes whose outcome is known, the 234 open ones dropped | 22 per cent | 141 |
| 2 | a product-limit survival of the time to a confrontational action with the quiet closures carried as observations that stop | 28 per cent | 178 |
| 3 | **answer:** the cumulative share with demobilisation as the other end of an episode | **17 per cent** | **108** |

Measured on the world model at `scratchpad/t192/m7.py`, seed 293: 635 episodes opened in the period, 89
with a confrontational action recorded by the extract, 312 closed quietly, 234 open. Rung 3's raw figure is
108.12 episodes and 17.03 per cent.

**Separation.** 14, 17, 22 and 28 per cent are four distinct whole percentages, each at least 21 per cent
from the next (14 to 17 is 21 per cent, 17 to 22 is 30 per cent, 22 to 28 is 26 per cent), and in episodes
89, 108, 141 and 178. Each is the complete output of a competent pipeline on the same rows. The answer is
bracketed, second lowest of the four, so no solver reaches it by stopping early and none by correcting
hardest: the two corrections that handle the open episodes both overshoot, and the decisive move is the
largest single move on the ladder, 178 down to 108.

**Robustness of the decisive rung.** The same estimate computed on weekly intervals gives 108.27 and on
fortnightly intervals 107.89 episodes, 17.05 and 16.99 per cent, so every nonparametric reading of the
decisive step files 108 episodes and 17 per cent. Summing each open episode's own remaining chance instead
of taking the cohort share gives 108.12 exactly, the estimator's self-consistency, asserted.

**The grid.** Two axes, how far the record is read and what is estimated:

| | already recorded | known outcomes only | survival, closures stopped | demobilisation as an end |
|---|---|---|---|---|
| the record to the 6 November extract | 89, 14 per cent | 141, 22 per cent | 178, 28 per cent | **108, 17 per cent** |
| the record cut at the period's close | 84, 13 per cent | 143, 23 per cent | 180, 28 per cent | 110, **17 per cent** |

Every cell is a named figure. The decisive column is the only one whose share holds across the rows, which
is the fairness the ladder needs: a solver who reads the record only to 30 October still files 17 per cent
if the estimate is built the right way, while every easy route moves and none of them lands on 17.

**Dominance.** The episodes the ladder turns on are the 144 standing disputes, which act every week or two
for months without a confrontational action: 73 of them are open at the extract with more than eight weeks
behind them, so rung 1 drops a block of episodes that will never produce a confrontation and rung 2 hands
each of them a share of one.

**Worth of each rung, on the graded quantity.** Rung 0 to rung 1 is +52 episodes, rung 1 to rung 2 is +37,
and the decisive move is -70. Nothing between the rungs is worth less than 19 episodes, and every rung is
satisfying to stop at: each is the whole output of a pipeline whose every input figure is correct.

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | which episodes are in the cohort | §3.2 and §3.3 file the opening window and that open episodes belong to the cohort; asserted |
| 2 | Unit of account | the report, the action, the episode | §2.1 files the action and §3.1 the episode; asserted |
| 3 | Attribution window | which day an action falls on | the register's local action date, which no report clock overrides; SF11, asserted |
| 4 | As-of dating | the record at the extract | the manifest files 6 November 2026; §3.3 covers each episode's whole life; asserted |
| 5 | Version basis | the re-imported month and the superseded place names | the import log and the gazetteer; SF12, SF9, asserted |
| 6 | Denominator | the 635 episodes opened in the period | §3.3; asserted |
| 7 | Weighting | none: episodes are counted, not weighted | stated |
| 8 | Window length | the reporting period for the openings, the episode's life for the outcome | §3.2 and §3.3; asserted |
| 9 | Boundary inclusivity | 1 May and 30 October | §3.2 states both inclusive; asserted that episodes open on both days |
| 10 | Rounding path | the share to a whole percentage, episodes to a whole number, rounded once at the end | SF14; asserted that 17.03 and 108.12 are at least 0.35 from their bin edges |
| 11 | Tie-break | two candidates on one share | none: 14, 17, 22 and 28 are pairwise distinct, asserted |
| 12 | Maturity and censoring | the episodes still open at the extract | §3.3 keeps them in the cohort and calls the figure an estimate; the method is open, the register's structure separates the candidates, asserted |
| 13 | Order of operations | resolve routes then build actions, or build then resolve | C1: a duplicate report carries the same identifier, theme, locality and day, so either order gives the same actions, asserted |
| 14 | Row order | the item log's own order | C1, asserted over three permutations |
| 15 | Duplicate resolution | the three routes, the two feeds, the re-imported month | C1: duplicates share the report identifier and resolve to one action under any handling, asserted both ways |
| 16 | Identity normalisation | place names, partner organisation codes | the gazetteer's superseded names; the partner codes are read only by the asks; asserted |
| 17 | Netting against gross | nothing is netted | stated |
| 18 | Dimensional units | items, reports, actions, episodes | the dictionary names each; the indicator reads episodes only, asserted |
| 19 | Code and status semantics | the route codes, the action codes, the acceptance column | the protocol and the dictionary; never the decisive step |
| 20 | Integerisation | the episode figure is a whole number of episodes | §3.3; the raw 108.12 rounds to 108, 0.38 from the bin edge, asserted |
| 21 | Clause scope | §2.1 per theme per locality per day; §3.1 per municipality per theme | both paragraphs state their scope; asserted |
| 22 | Forward window contents | the episodes whose outcome has not happened | the call is the cohort's own figure, which the record cannot yet show in full: 234 episodes are open at the extract and the protocol files the figure as an estimate, so the quantity is about a window not yet closed |

## Literal reader

Executing the prompt, §2.1, §2.2, §2.3, §3.1, §3.2 and §3.3 of the protocol, the dictionary, the gazetteer
and the manifest word for word selects the accepted reports between 1 May and 6 November 2026, resolves
them to actions at gazetteer settlements, builds the register's dispute episodes on the municipality and
theme with twenty-one clear days closing each one, keeps the 635 whose opening day falls in the reporting
period, and asks for the share of them that record an action coded `CF`, `RF` or `DP` before the episode
closes, as a whole percentage with the number of episodes it stands for, the open episodes inside the
cohort and the figure stated as an estimate because their lives are not over. The text is silent on how the
estimate is made, so every option was computed on the same rows: the episodes that have already recorded
one give 89 and 14 per cent, the share among those whose outcome is known gives 141 and 22 per cent, a
product-limit survival with the quiet closures carried as observations that stop gives 178 and 28 per cent,
and the cumulative share with demobilisation as the other end of an episode gives 108 and 17 per cent,
which the register's own 312 quiet closures and 234 open episodes select. The easy three are easy
estimators of the same literal estimand, not other readings of it, and every other term and convention has
an SF row ruled out by a quoted sentence or asserted to give the same call.

## Oracles

- The earlier monthly bulletins (`boletins_anteriores_2026.pdf`) report actions recorded and
  municipalities touched by month and never episodes or confrontation rates, so they tie under every rung.
- `registo_importacoes.csv` confirms which month was loaded twice and when each load completed; it ties
  under every rung, and the share is asserted invariant to the resolution.
- `gazeteiro_localidades.csv` confirms the settlements, their municipalities and their superseded names; it
  ties under every rung.
- `totais_por_via.csv` and `excecoes_geocodificacao.csv` are route-level control totals and the reports the
  association could not place; neither carries an episode and both tie under every rung.
- `manifesto_extracao.csv` states each file's rows, range and extract date and settles the one designed
  disagreement in the ask layer without naming a level.
- No control, published figure or corpus states a confrontation rate, an episode count or an episode's
  state, and no earlier rate ships. There is no calibration organ.

## Ask sheet

| Ask | Figures | H18 home | Use | Primary device | Hazards | Files, columns | Stops, lazy delta | Realism |
|---|---|---|---|---|---|---|---|---|
| A1 per fortnight, the actions recorded, the municipalities touched and the share of those actions the partner network reported | 3 per fortnight, 13 fortnights | the construction's own output on the segment the trustees want anyway | the bulletin's standing table | D5 scope: the protocol's fortnights run from 1 May and the last one ends with the period, so it has fifteen days, while fixed fourteen-day blocks make a fourteenth fortnight holding 30 October alone and leave 52 actions out of the thirteenth | D6 the partner share is per action, not per report; D1 the re-imported month doubles reports and no actions | item log, partner reports, public line, gazetteer, protocol, dictionary, manifest, import log; 12 columns | 4 stops, lazy delta 9 of 13 fortnights | the bulletin's own standing table |
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

**The cracker sheet.** The cracker filed 17 per cent and 108 episodes, ran the hygiene battery, executed
every filed paragraph and matched every control total.

| Ask figure | Cracker's path | Cracker's figure | Golden | Result |
|---|---|---|---|---|
| A1 actions recorded, fortnight 13 | fixed fourteen-day blocks, so the thirteenth ends on 29 October and a fourteenth holds 30 October | 626 | 678 | miss |
| A1 share the partner network reported, fortnight 7 | counts reports, not actions | 32.8 per cent | 46.3 per cent | miss |
| A2 reports received, the partner network | counts the rows of the partner file, so the reposted August month counts twice and the unplaceable reports are missing | 2,329 | 1,947 | miss |
| A2 reports that could not be placed, the press monitor | the item log alone, which holds only the items it placed | 0 | 149 | miss |
| A2 median minutes from the action to the report, the press monitor | reads the monitor's reception stamp as local time | 49.0 | 109.0 | miss |
| A3 euros paid, the amended partner | the schedule's rate for the whole period, without the July adenda | 1,024 | 1,154 | miss |
| A3 reports filed, the merged partner | one delivery code | 191 | 262 | miss |

**Pair ceiling:** 39.5
**Mirror leakage:** 20.0

## Build and the free gates

Cut from `generator/`, seed 293 for the episode layer and 2930 for the pack. The bundle carries 17 files
in four formats, the press monitor's item log 25,688 rows, and three distractors declared in
`metadata.json`. The build's own figures are the note's: 635 episodes in the cohort, 89 with a
confrontational action recorded at the extract, 312 closed quietly, 234 open, and 108.123 episodes,
17.027 per cent, on the decisive estimate. 108 generator assertions and 99 independent checks in
`verify.py`, which reads only the bundle and walks the timeline day by day instead of event by event,
both green; two consecutive rebuilds byte-identical across `target/` and `golden/`; `figures_check.py`
exit 0 on 101 figures.

**The pre-ship check.** 17 files in four formats (csv, pdf, xlsx, json), the press monitor's item log
25,688 rows, three distractors declared in `metadata.json` and named in no file name; 108 generator
assertions and 99 independent checks green, two rebuilds byte-identical over `target/` and `golden/`,
`target.zip` 17 members with no content mismatch against the tree, `figures_check.py` exit 0,
`precut.py` 49 checks with 0 FAIL and 0 WARN, `leak.py` REVIEW with every line answered above,
`guard.py heart` and `guard.py surface` at WARN with no BLOCK, the container audit clean on `target/`
and on `golden/`, one `submission.md` and one `prompt.txt` in the tree. The two deliverables carry the
call in the workbook's first sheet and the period's actions in the chart; every figure they state is in
`generator/figures.json` and recomputes from the bundle.

**Stage 4 is staged, not run.** This session has no agent tool, so the leak reader and the determinism
judge are prepared for the orchestrating session to spawn, each with its own isolated inputs:
`<scratch>/t192/stage4/judge/` (judge_brief.md with the isolation rules, the literal-reading-first
method, the recompute requirement, three probes for this build, a request for the Gate G and Gate H
lines, the reviewer's system prompt inlined verbatim, prompt.txt, the graded blocks and a fresh unzip in
`target/`; the verdict goes to verdict.md) and `<scratch>/t192/stage4/reader/` (reader_brief.md with the
six solver's-eye questions and the three working-analyst questions, prompt.txt and a fresh unzip in
`bundle/`; the answers go to reader_answers.md).

**The leak sweep's REVIEW lines, answered.** Sweep 4 twice: the prompt's sentences carry the protocol's
own nouns (dispute episode, confrontational action, the fortnights, the partner network) because the
question cannot be asked without them; none of them names the decisive step, and the word sweep in
`checks.py` asserts that no shipped file carries a risk, censoring, survival, incidence or estimation
word. Sweep 9 twice: `notificacoes_reuniao_publica.csv` holds notified gatherings whose planned dates run
past the extract, which is what a notification register is, and the manifest reports that file's last
planned date; no record of an action, a report or a load is dated after 6 November 2026, asserted.

**The surface screen's promoted pairs, answered.** task191 shares only the context-artifact type (a
published series, here five monthly bulletins that report actions and municipalities and never episodes);
task189 shares only the decision type (a quantity); task193 is back to back in the batch at 0.100, the
corpus's own median neighbourhood. The drivers sit 0.06 and below against every card on file, and the
spine, world, unit, estimand and decisive step differ in all three.

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
