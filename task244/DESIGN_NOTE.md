# task244 design note

## Draw

Card `cards/task244.json` (architecture 1, registered 2026-10-18). Guard verdict WARN, no BLOCK. The one WARN left,
repeat.decision (designation_set after task246), is answered here: the candidates are a grid of 24 published rates
(twelve survey districts, a job-finding and a job-loss rate each), not a list of sites or offices, and the question is a
whether (can the release go out without the warning, and if not on which rates), so the prompt does not take the
"which of the twelve carry the note" carrier of task243, task245 and task246. The people WARN (a recycled first name)
and the overuse WARNs (government_agency, method_or_model_selection) were cleared by redrawing those axes. Nearest
driver 0.05 (task229 v2 lineage, task465, task266, task246, task267 v0).

- **Pairing.** Survey Research & Official Statistics / nonresponse-calibration-measurement-error-adjustment, a task type
  serving Descriptive & Distribution Analysis and Data Quality Monitoring; drawn for Data Quality Monitoring & Alerting.
  Not banned against the last three builds (task168 supply chain transportation network, task167 grant-making other,
  task246 general statistics measurement error). The object is the health of the flows the bureau publishes (how much
  of each published labour market flow is classification error rather than people moving), the call a monitoring
  decision: which published rates go out under the classification-error warning in the 2027 annual flows release.
- **Niche.** A state bureau of statistics' quarterly labour force survey interviews each household in four consecutive
  quarters, so each matched pair of quarters gives a person's labour force status twice and the bureau publishes, per
  survey district, the job-finding rate (unemployed to employed) and the job-loss rate (employed to unemployed). A
  supervisor reinterviews a random subsample of each quarter's respondents and reconciles every difference with the
  respondent; the reconciled status is the bureau's measure of a person's true status.
- **The call.** Whether the 2027 annual flows release can go out without the classification-error warning, and if not,
  which of the 24 district rates carry it: a rate carries the warning when a third or more of the moves it counts are
  not real moves (persons counted as moving between the two statuses whose true statuses in the two quarters were not
  that pair).
- **Shape.** 07, grid of cells: 12 districts by 2 flows, per cell the published rate, the share of its counted moves
  that are not real moves and the warning (24 cells, 72 figures), the warned set and its count, plus the asks (per
  district figures), well over 25 criteria. Decision designation_set, answer set_of_items, question form whether.
- **Strategy.** other: the decisive move inverts the reinterview's misclassification matrix at both quarters of every
  matched pair (the true flows), which no strategy key names; it is regression to the mean from classification error
  (a counted move is far likelier than a random record to be a misreading of someone who stayed put). G2 decisive (what
  one counted move is: a recorded pair of statuses, not a move), G16 (the share of real moves taken as the product of
  the two ends' predictive values, as the product of their correct-reading rates, or from the inverted matrix); gap
  time (two readings of a persistent status manufacture change between them) with population second; Gate G
  signal_vs_noise_or_hold (the warning marks rates whose counted moves are largely misreading); calibration
  gold_standard_subsample (the reconciled reinterview, a random subsample re-read and reconciled with the respondent);
  context artifact published_series (the bureau's flows tables); Layer 2 family estimand_identification, pattern
  own:true-flows-by-inverting-misclassification-at-both-ends.
- **Forum, event, organisation.** executive_team (the bureau's management meeting, the Statistician-General and the
  directors, which clears each release and its quality note), period_close (the 2027 annual flows tables, released in February 2028 once the
  year's four quarter pairs are closed), research_or_statistics_office (the state bureau of statistics). Role
  statistical_office_head (the Director of Labour and Social Statistics, who signs each release's quality note). The
  forum was committee_or_panel at the draw; task170, drawn in a sibling session at 09:10 and registered before this
  card, carries committee_or_panel too, so `guard.py heart` blocked at stage 3 and the forum was redrawn to the
  management meeting (executive_team), free against task170, task246 and task167; the event and the organisation
  clear them as well (purchase_order_or_contract, other, vote_or_meeting; government_agency, local_government,
  foundation_or_funder).
- **People** (`guard.py names --geo Nigeria --locale yo_NG --seed 244`; `--geo Nigeria` alone falls back to en_US):
  Atinuke Adebisi, the Director of Labour and Social Statistics, who asks; Babasola Oginni, the head of field
  operations, whose supervisors run the reinterview; Comfort Olawale (en_NG draw), the survey methodologist; Ronke
  Shekoni, the secretary to the management meeting. None appears in the prompt.
- **Data-native sentence.** Each household's members are read four times a quarter apart, most adults stay employed or
  outside the labour force from one quarter to the next, and an employed adult is now and then recorded as unemployed
  (a lost day's work read as a search, a job between contracts); because the employed stock is many times the
  unemployed stock and the true job-loss rate is a percent or two a quarter, those single misreadings make up a large
  part of every counted move into and out of unemployment, and only the reinterview, which re-reads a random
  subsample and reconciles it with the respondent, measures the misreading.
- **Sources.** The client's two-layer standard (estimand_identification: regression to the mean; a measured change that
  is partly the measurement's own noise) and the task type's pattern 3 in layer2-rigor-patterns.md (prevalence
  corrected for sensitivity and specificity from a record check; shortcut: the observed share, or divide by the
  sensitivity alone); here the correction is of a transition between two readings, not of one prevalence, and the
  shortcut that bites is multiplying the two ends' predictive values. Labour statistics practice gave the method (the
  true flows recovered by inverting the reinterview's misclassification matrix at both ends of the matched pair, as in
  the gross-flows adjustments of Abowd and Zellner and of Poterba and Summers). The seed DQ17 gave the world, the
  decision and the quantity only.
- **Mechanisms on file** (`guard.py mechanisms --objective data-quality-monitoring`, 18 builds), the insight each
  spends: 229 a convex conversion of a daily mean; 231 exits reaching the record late; 232 a transmission rate from
  delayed closed episodes; 230 a late channel moving items to default categories; 228 events clustered within
  randomised units; 233 a gold-standard follow-up carried across base rates; 234 a share in a source's output that
  transit loss cannot move; 235 an item lost only once its device had its next chance; 236 a capture change changing
  which cases are reached; 237 the share of a composite's variance due to its attribute; 238 a channel effect through a
  randomised nudge; 239 a group-level factor; 240 the error of a post-stratified total; 241 a sensor's error against a
  reference at a displaced position; 242 a detector whose sensitivity fades with time since the event; 243 a growth
  balance carrying movement; 245 losses falling on the outcome's own high values; 246 a measurer's offset and field
  error out of a tail share. None spends a change between two readings manufactured by misreading either of them.

The call is retrospective by design: the four quarter pairs of 2027 are closed and the warning is a monitoring decision
on their published flows; what faces forward is the release (the annual flows tables go out in February 2028 and stand
until the 2028 tables replace them).

As of 2 February 2028 (the Director's request; the tables as tabulated on 28 January 2028). Seeds: simulation 336, reinterview 69, records 289 (the last four lines of Tried and rejected give why).

## Default path

1. Open elfs_2027_annual_flows_tables.xlsx: Table F2 carries each district's published job-finding and job-loss rates,
   Table F1 the flows between the three statuses behind them.
2. Open elfs_reinterview_results_2026q4_2027q4.csv and cross the status the original interview recorded with the
   reconciled status, every person once and unweighted (protocol section 7): 15,221 persons.
3. For each recorded status, the chance the record is right: of the persons recorded employed, 98.58 per cent are
   reconciled employed; of those recorded unemployed, 83.10 per cent are reconciled unemployed.
4. A counted move between employment and unemployment is real when both of its recorded statuses are right, the two
   chances multiplied (81.92 per cent), so 18.1 per cent of every rate's counted moves are not real moves.
5. Compare with section 8.1's third: no rate reaches it, and the release goes out without the warning.

Ends on: no rate carries the warning (every rate at 18.1 per cent), the tables go out without it
Golden: 13 of the 24 rates carry the warning (job-finding: Industrial Corridor, Cocoa Belt East, Cocoa Belt West,
Northern Savanna, Central Hills, Creeks; job-loss: Lagoon Coast, Cocoa Belt East, Cocoa Belt West, Northern Savanna,
Central Hills, River Basin, University Towns)

## Stump sentence

Multiplying the reinterview's predictive values of a counted move's two recorded statuses puts every rate at 18.1 per
cent of its counted moves not real and files no warning, because it treats the two readings of a counted mover as if
they were two records drawn at random from the recorded stocks; a person counted as moving is far likelier than a random
record to be a misreading of someone whose status did not change, and only the true flows (the published flows with the
reconciled reinterview's classification error taken out at both quarters of each pair) show 13 of the 24 rates at 45.1
to 69.0 per cent.

## Three rules

- **Task type:** survey-research-official-statistics / nonresponse-calibration-measurement-error-adjustment, which
  serves Data Quality Monitoring & Alerting: the published flows are the monitored statistic, the classification-error
  warning the monitoring decision the bureau's release clearance takes on them.
- **Domain test:** the quantity that decides is each published gross flow's share of counted moves that are not real
  moves, which labour force statisticians estimate by taking the reinterview's misclassification out of the matched-pair
  flows at both quarters (the gross-flows adjustment of Abowd and Zellner and of Poterba and Summers: the true flows are
  the inverse of the classification error applied on both sides of the flows table), then the true flow read correctly
  in both quarters over the counted flow.
- **Swap:** "which of a hospital's 24 ward transfer rates carry the coding-error warning" keeps the words and loses the
  task: a transfer is recorded once as an event, not read twice as a persistent status by two interviewers, so there is
  no flows table of two independent readings and no reconciled re-reading to take out at both ends; the call needs a
  rotating panel whose persistent status is re-read each quarter.
- **Layer 1:** six enumeration areas moved from the Industrial Corridor to the Metropolitan Fringe on 1 April 2027 and
  2,005 records before then keep the old codes (the bureau's area frame); one area's second-quarter batch received
  twice, 261 rows (the tablets' sync); from an app update each supervisor's tablet took at a Friday sync between 18
  June and 9 July 2027, the fieldwork log's call date is the date the tablet next synchronised (the supervisors'
  tablets); households that split are interviewed as two, the new household
  numbered afresh (the CAPI roster); birth months taken down wrongly at a first interview and corrected at the next;
  members interviewed on callback days; the server's restore of 17 May taking in the uploads of 14 May again under
  new household numbers; one supervisor's second-quarter workload in two districts
  never attempted; reinterviews completed late, in the log without results. Each is what the system that writes it
  produces; none decides the call, which reads Table F1 and the reinterview results and is the same under every
  handling of each (SF rows).
- **Layer 2:** estimand_identification: the change between two readings of a persistent status is manufactured by
  misreading either one, so a counted move is a recorded pair of statuses whose truth needs the true flows; multiplying
  each recorded status's predictive value treats the pair as two random records and misses the regression to the mean
  that the persistence of most people's status builds into every counted move.
- **Decisive step:** taking the reconciled reinterview's classification error out of each district's published flows at
  both quarters of the pair (the true flows) before asking what share of the counted movers were true movers recorded
  correctly in both quarters, rather than multiplying the two recorded statuses' chances of being right.
- **Not semantics:** reading every field right (orig_status against the reconciled words, Table F1's cells, the 24
  rates of section 8.1) and reading section 8.1's definition as written still leaves the predictive-value route at 18.1
  per cent for every rate: no field, code, unit or definition carries the misreading's concentration in counted moves.
- **Not rule application:** section 8.1 files the quantity (the persons counted whose reconciled statuses were not
  that pair, a third or more) and protocol section 7 the reinterviews that measure the error (five quarters, unweighted,
  the state); no filed rule says how to estimate the share, and executing both with the reinterview's usual statistic
  files no warning.
- **Analyst test:** a strong analyst who reads every file right and applies sections 8.1 and protocol 7 as filed takes
  the reinterview's chance that a recorded status is right, multiplies the origin's and the destination's, and files no
  rate carries the warning (every rate at 18.1 per cent): the tables go out without it.
- **Estimand:** methodology note section 8.1 (elfs_methodology_note_2027.pdf): of the persons each of the 24 annual
  rates counts as moving (Table F1's cell, the average of the four quarter pairs), the share whose reconciled statuses
  in the two quarters were not that pair, a third or more; the reinterviews of the interviews of 2026Q4 to 2027Q4, each
  person once and unweighted, for the state (protocol section 7).
- **No decoy:** nothing is planted to be caught: no memo, draft, briefing or stakeholder figure argues for releasing
  without the warning or names any rate; the third-quarter bulletin, the projections and the job centre registers rank
  nothing on classification error, and Table F1 and F2 are the bureau's own tabulation as it stands.
- **No certified replay:** no certified or published figure carries a share, a true flow or a past warning, so no
  method can be recovered by reproducing one; the method follows from the definition and the reinterview's design.
- **Lesson:** a measured change between two readings of a persistent state is mostly the readings' error once true
  change is rare, and the error has to come out of the transition table at both ends, never be multiplied in as two
  independent chances; no build on file spends a change manufactured by misreading either of two readings (task233
  carries a gold-standard follow-up across base rates for one reading, task246 a measurer's error out of one tail).

## Readability screen

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 the two recorded statuses' predictive values multiplied | no clause names it; section 8.1 defines the quantity, protocol section 7 the reinterviews | the results file's orig_status and reconciled columns make the crosstab | yes, the first move on a reinterview table | none | none | yes, two ratios multiplied | readable |
| R1 the two statuses' chances of a correct record multiplied | none | the same crosstab, read by rows | yes, the sensitivity reflex | none | none | yes | readable |
| R1 the predictive values by district | protocol section 7 says a district's sample is too small | the district column on each result | yes, the regional reflex | none | none | yes | readable |
| R2 the rate's overstatement (net) | section 8.1's "persons it counts as moving" rules it out | none | a reflex once true rates are in hand | none | none | yes, one subtraction of two rates | readable |
| R3 the error out at both quarters of each pair (decisive) | no clause names true flows, an inversion or a correction at both ends | no column holds a true flow, a share or a warning | the opponent multiplies, reweights or regionalises the error; none inverts it through the flows table | no prior warnings, adjusted flows or back-test ship | the battery (duplicates, codes, dates, boundaries) points nowhere near it | no: a three-by-three inversion applied on both sides of each district's table, then the correct-reading chances | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative and its call | Ruled out by |
|---|---|---|---|---|
| SF1 | "moves it counts that are not real moves" | the persons Table F1 counts as moving whose true pair was another, gross | the rate's overstatement of the true rate (net): 12 rates, Cocoa Belt West's job-finding off at 31.7; the counted flow's excess over the true flow: the same 13 | section 8.1: "a third or more of the persons it counts as moving ... did not in fact hold the first status in the first quarter and the second status in the second" |
| SF2 | a person's true status | the reinterview's reconciled status | the supervisor's own reading before review: 14 rates (the Creeks' job-loss rate added) and a share of 105.1 per cent | section 8.1: "the status the supervisors' reinterview records for that quarter once every difference has been reconciled with the respondent" |
| SF3 | which reinterviews | the interviews of 2026Q4 to 2027Q4 | 2027Q1 to 2027Q4 only: the same 13 (same call) | protocol section 7 names the five quarters |
| SF4 | weighting of the reinterview | each person once, unweighted | the persons' cross-sectional weights: the same 13 (same call) | protocol section 7: "Each person reinterviewed counts once; the reinterview carries no weights" |
| SF5 | the classification error's scope | the state's, every district | each district's own: 12 rates, the University Towns' job-loss rate off at 14.8 | protocol section 7: "not large enough to measure classification error for a single district or a single quarter" |
| SF6 | the published flows | Table F1 as tabulated | rebuilt from the person files on the bureau's key and the cross-sectional weights: the same 13 (same call) | section 8.1 ("a published flow rate"); same call |
| SF7 | the persons linked | the bureau's link as published | every person interviewed again, split households linked: the same 13 (same call) | same call |
| SF8 | the rate | Table F2's rate, Table F1's flow over the first status | none: Table F2 ties to Table F1 on all 24 rates | section 7's definitions; asserted |
| SF9 | the 24 rates | each district's job-finding (unemployed to employed) and job-loss (employed to unemployed) rate | none | section 8.1's last sentence and section 7 |
| SF10 | "a third or more" | the unrounded share at 1/3 or above | the printed share at 33.3 or above, or a line five points either side: the same 13 (same call); nearest rate 10.1 points off | same call |
| SF11 | the recorded status | orig_status in the results file | the person file's lfs_status: identical for every reinterviewed person (same call) | asserted |
| SF12 | the districts | as from 1 April 2027 | the codes in force at the interview: Table F1 is already on the 2027 districts | section 6; same call |
| SF13 | each person reinterviewed | once, one row each | none: no person twice in a quarter | protocol section 7; asserted |
| SF14 | the rounding path | Table F1's persons as published | the bureau's unrounded flows: the same 13, every share within 0.2 points (same call) | same call |
| SF15 | the annual flows | the average of the four quarter pairs (Table F1) | the mean of the four pairs' own shares: the same 13 (same call) | section 7; same call |
| SF16 | the codes 1 to 3 | employed, unemployed, outside the labour force (the dictionary) | any other mapping puts most persons off the diagonal | the dictionary; asserted |

## Ladder

| Rung | Route | Warns | Shares | Dies to |
|---|---|---|---|---|
| R0 (default) | the two recorded statuses' predictive values multiplied | none | 18.1 for every rate, 15.3 points under the line | the persistence of most people's status (Table F1's diagonal): a counted move is not two random records |
| R1 | the two statuses' chances of a correct record multiplied | none | 17.0 for every rate | the same: it ignores how rare a true move is |
| R1 (regional) | the predictive values from each district's own reinterviews | none | 13.1 to 25.9 | protocol section 7, and the same fact |
| R2 | the error out at both quarters, read as the rate's overstatement (net) | 12 | Cocoa Belt West's job-finding at 31.7, under the line | section 8.1's persons counted |
| R3 (decisive) | the error out at both quarters, the persons counted whose true pair was another | 13 | 45.1 to 69.0 warned, 11.9 to 23.2 clear | the golden |

Position and margins: the golden's nearest rate is the Creeks' job-loss rate, 23.2 per cent, 10.1 points under the
line; the nearest warned is the Lagoon Coast's job-loss rate at 45.1, 11.7 over. On the simulator's clean truth the
default path warns none and the decisive step alone gives the same 13, 10.9 points clear (R3a, R3b in checks.py).
Every correction short of the inversion walks the shares the same way (all under 26 per cent); only the inversion
reverses the call. Grid (method by truth by scope by reading, 16 cells, generator/pair.py --ladder): every
cell without the inversion warns none, except with the supervisor's unreconciled reading by district (6 and 4 rates,
two errors); with the inversion, the district error warns 12 or 10, the unreconciled reading 14 or 11 with shares above
100 per cent, and one cell, the unreconciled reading read net, lands the 13 by two errors in opposite directions with a
share of 107.1 per cent and none of the 24 figures. Worth: the decisive move is the whole of the call (13 rates and 24
figures); R0 and R1 keep 11 of the 24 warnings and none of the figures.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the persons each of the 24 annual rates counts as moving, Table F1's cell (section 8.1); the reinterviewed persons of 2026Q4 to 2027Q4 (protocol section 7) |
| 2 | Unit of account | one rate (a district's job-finding or job-loss rate) and one warning a rate (section 8.1, SF9) |
| 3 | Attribution window | the four quarter pairs 2026Q4 to 2027Q4, averaged in Table F1 (section 7, SF15) |
| 4 | As-of dating | the tables as tabulated on 28 January 2028; the request of 2 February 2028 |
| 5 | Version basis | the 2027 edition of the methodology note; the reinterview protocol's version 3, in force from 2026Q4 |
| 6 | Denominator | the counted flow, Table F1's cell, for each share (section 8.1); the persons due another visit for the match rate (8.2); the persons whose household reinterview was completed for the timing (8.3) |
| 7 | Weighting | the published flows as the bureau weighted them (SF6); the reinterview unweighted (protocol section 7, SF4) |
| 8 | Window length | the year's four pairs; five quarters of reinterviews (SF3) |
| 9 | Boundary inclusivity | a third or more (SF10); the nearest rate 10.1 points from the line |
| 10 | Rounding path | each share from Table F1's persons and the unrounded classification error, printed to one decimal (SF14) |
| 11 | Tie-break | none needed |
| 12 | Maturity and censoring | every quarter of 2027 closed; reinterviews completed after the window carry no result (protocol section 5) |
| 13 | Order of operations | the classification error from the reinterview, the error out of each district's flows at both quarters, the shares, the line |
| 14 | Row order | no step depends on file order |
| 15 | Duplicate resolution | the one batch received twice (Market Towns area 5, 2027Q2) counted once; no person twice in the results (SF13) |
| 16 | Identity normalisation | the call reads Table F1; the asks link a person on the dwelling, household and line, or a new household's sex and month and year of birth |
| 17 | Netting against gross | the persons counted, gross (section 8.1, SF1) |
| 18 | Dimensional units | persons; per cent; days |
| 19 | Code and status semantics | orig_status 1 to 3 against the reconciled status's words (SF11, SF16); the reconciled status as the truth (section 8.1, SF2) |
| 20 | Integerisation | none for the call; Table F1's persons as published |
| 21 | Clause scope | section 8.1 applies to each of the 24 rates; protocol section 7's state error to every district (SF5) |
| 22 | Forward window contents | the 2027 annual tables stand until the 2028 tables replace them; nothing is forecast |

## Literal reader

Executed word for word, the prompt and section 8.1 fix the population (the persons Table F1 counts as moving), the
outcome (whose reconciled statuses in the two quarters were not that pair), the unit (each of the 24 rates), the
window (the four pairs) and the comparison (a third); protocol section 7 fixes the reinterviews (five quarters, each
person once, unweighted, the state). Every alternative reading of a term or convention (SF1 to SF16) either gives the
same 13 rates or breaks a quoted sentence; the easy answer (none) comes from an easy method on the same literal
estimand, the predictive values multiplied, never from another reading.

## Oracles

None arbitrates the call. No file carries an adjusted flow, a share of counted moves, a past warning list or a
back-test. The third-quarter bulletin's unemployment and employment rates and the job centres' registers rank no rate
on classification error, and the population projections carry only the weights' calibration totals. Table F2 ties to
Table F1 under every route (SF8) and so confirms nothing about the warning.

## Ask sheet

**Ask A, each district's match rate (per cent, one decimal) and the persons it is based on (whole numbers)** (24
figures). H18: the quality note's standing panel item (the request: "the match rate and the reinterview figures the note
always gives"; section 8.2), the share of each district's panel the flows rest on; the call reads Table F1 and no person
file. The paid pin: section 8.2 files the link (the dwelling, household and line numbers or, in a household new to the
dwelling, sex and month and year of birth, so the 469 members of households that split are found) and that a person
counts once in each pair. Primary device D1 (a replay under fresh ids, key kept): the server's restore of 17 May 2027
took in the uploads of Friday 14 May again and numbered each household it received as the dwelling's next household,
so 714 records of 2027Q2 repeat another record of their dwelling in every field but the household number; nothing in the
pack mentions the restore, the hygiene battery's exact-duplicate and key checks both pass the copies (the household
number differs, dwelling, household and line stay unique), and the copies, never found at the next visit, sit in every
district's base (36 to 65 a district). Hazards: Market Towns area 5's batch received twice (exact, 261 rows), the six
areas moved on 1 April 2027 (2,005 earlier records under the Industrial Corridor's codes; section 6 reports every
quarter on the 2027 districts), the fourth visit's dwellings not due another visit, the split households (filed).
Path: the five person files, the gazetteer, sections 6 and 8.2, the dictionary (8 files, 12 columns). Stops: the
filed link over identical rows taken once (the cracker): bases 36 to 65 persons larger and rates 0.29 to 0.54 points
lower, all 24 missed; the rows as received: bases 36 to 276 larger, every rate lower; the line key alone: every rate
0.17 to 0.67 lower; the recorded codes: the Fringe 1,490 persons smaller, the Corridor 1,490 larger. Realism: a server
that numbers the households it receives gives a re-ingested upload new household numbers, while the tablets' own
numbers survive only in the original upload.

**Ask B, each district's mean days from interview to reinterview (one decimal)** (12 figures). H18: the note's
standing fieldwork item (section 8.3), how promptly the supervisors re-read the statuses the call corrects with; the
call reads the results file and no log row. Primary device D2 (a stored value whose meaning changed on a date): from the
tablet app update, which each supervisor's tablet took at a Friday sync between 18 June and 9 July 2027, the log's
attempt_date is the date the tablet next synchronised with the server (the supervisors spend Friday at the area office
for the sync and make Friday's calls in the evening), while visit_start keeps the time the reinterview form was opened;
nothing marks the change, and the log shows it (the two dates agree on all 5,268 calls before each tablet's update and on
none of the 3,752 after, every later attempt_date a Friday) as does the results file (by attempt_date 1,122
reinterviewed persons would fall outside the 14-day window that protocol sections 5 and 6 say every result is inside; by
visit_start none does). Hazards: callbacks (a person's own interview date after the household's first, section 8.3's
"a person's original interview"), the late reinterviews (in, section 8.3), the 2026Q4 selections (out), the boundary,
the batch received twice. Path: the log, the person files, the results file, the protocol's sections 5 and 6, section
8.3, the gazetteer (10 files, 12 columns). Stops: the call's date as recorded (the cracker): 1.94 to 2.42 days more,
all 12 missed; the household's first interview: 0.14 to 0.22 more, all 12; the late reinterviews left out: 0.27 to 1.24
fewer, all 12; 2026Q4 kept: 10 of 12 moved. Realism: a tablet app that stamps a record when it reaches the server
rather than when it was made is a common update side effect, and a field team that syncs weekly from an area office
makes the stamp a Friday.

Main population zero-counts: the call reads Table F1 and the reinterview results; no person-file row, log row or
gazetteer row is among them, and no device or hazard row of either ask sits in Table F1 or the results file's statuses.

| Hazard | Asks moved | Per-ask deltas (largest) |
|---|---|---|
| the uploads of 14 May taken in again under new household numbers (D1, primary) | A | base +65, rate -0.54 |
| the batch received twice kept (D1, texture) | A | Market Towns base +211 with the replay |
| the line key alone, split households unfound | A | rate -0.67 |
| the codes in force at the interview (D3) | A | the Fringe -1,490, the Corridor +1,490 persons |
| the call's date as recorded (D2, primary) | B | +2.42 days |
| the household's first interview | B | +0.22 days |
| the late reinterviews left out | B | -1.24 days |
| 2026Q4 kept | B | 10 of 12 districts moved |

Referee: the person files' birth details for the splits and the protocol's window for the log's dates; neither names a
split, a key or a date column.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Ask A, the persons each rate is based on, all twelve districts | section 8.2's link, identical rows once (the batch received twice), the 2027 districts; the records taken in again under new household numbers kept | miss |
| Ask A, match rate, all twelve districts | the same | miss |
| Ask B, mean days, all twelve districts | the call's date as the log records it, each person's own interview, late reinterviews in, 2027 selections | miss |

Measured by: generator/pair.py on the cut pack (--asks prints every stop, device and hazard count above): the cracker keeps 0 of the 36 ask figures; every lazier path keeps 0
(the rows as received, the recorded codes, the household's first interview, the late reinterviews left out, the line
key alone); the mirror (stopped at the counted flow's excess, which warns the same 13 with none of the 24 shares)
keeps 14.2 of the 38 recommendation points and none of the ask figures.

Pair ceiling: 33.1 ((38 + 7 + 55 x 0) and (14.2 + 7 + 55 x 0), averaged)

Mirror leakage: 0.0 per cent of ask weight

## Pre-ship check

1. Domain: the call stands on each published gross flow's share of counted moves that are not real moves, estimated
   the way labour force statisticians adjust gross flows, the reconciled reinterview's classification error taken out
   of the matched-pair flows at both quarters; with a hospital's ward transfers there is no persistent status read twice
   by different interviewers and no reconciled re-reading to take out at both ends, so the swap stops making sense.
2. Two layers: Layer 1 (the six areas moved on 1 April 2027, the batch received twice, the 17 May restore, each
   tablet's app update stamping the call date at the next Friday sync, split households, corrected birth months,
   callbacks, late reinterviews, the workload never attempted) is neutral on the call, which reads Table F1 and the
   reinterview results, and no device or hazard row sits in either (SF1 to SF16). Layer 2 is the true flows, asserted
   on the simulator's clean truth: the predictive values multiplied, the correct readings multiplied and each district's
   own predictive values warn none (R3a), and the decisive step alone gives the golden 13 with 8 points to the line
   (R3b).
3. No banned stump decides: nothing is planted (no memo, draft or figure argues for releasing without the warning;
   Table F1 and F2 are correct as tabulated); not semantics (every field read right, the predictive-value route files
   none at 18.1 per cent); not rule application (section 8.1 files the quantity and protocol section 7 the
   reinterviews, and no filed rule estimates the share).
4. Gate G: no shipped artifact ranks the rates on the warning; the projections, the job centre registers and the
   third-quarter bulletin give no rate a share.
5. Determinism: the same 13 under every route that takes the error out at both quarters (the matrix of 2027 alone, the
   weighted matrix, flows rebuilt from the person files); the nearest rate 10.1 points from the line (Creeks job-loss,
   23.2); the reinterview's own status (14), the net excess (12) and a matrix by district (12) each closed by a filed
   sentence; 16 fork rows asserted; every graded figure at least 7 per cent of a bin from its rounding edge, asserted
   in the checks and again by the verifier's own code; two builds byte-identical; figures_check 84 found, 0 missing.
6. Fingerprint: heart PASS on the corpus pulled at ship (248 cards, 0 invalid, nearest driver 0.05); the forum
   redrawn to the management meeting at stage 3 when task170's draw reached this checkout. The surface screen promotes
   four pairs, none on the decisive mechanism: task242 (gap, decision type, calibration form and context artifact) is
   epidemiology with G13 decisive against G2, its gold standard measuring a test's sensitivity fading with time since
   infection rather than misreadings taken out of both ends of a transition table; task243 (the same client domain and
   objective, back to back by number) is the register task type with G4 decisive, a register's recorded share of
   exits recovered from two complete counts; task245 and task246 share only the decision type.
7. Judge (one isolated thread a pass, Sonnet, medium, the bundle and the graded blocks only). Pass 1: DETERMINISTIC,
   APPROVE. Pass 2: NOT_DETERMINISTIC, FIX_NOW on Ask A's unfiled link for split households, closed by filing the link
   in section 8.2 with the 17 May restore as the new silent primary (Tried and rejected). Pass 3: DETERMINISTIC,
   APPROVE, fix none; every figure reproduced (the 24 shares, the 13, the match rates and persons, the days); Gate G
   etl_conformance, analytical_non_defect; Gate H domain, layers and decisive step pass; every rate on its side in 500
   bootstrap resamples of the reinterview. Its advisory (carry the matrix unrounded; at coarse rounding Lagoon Coast
   job-loss reads 44.9 or 42.6) is in solution step 2. Its tension note (inversion read as the literal reading of
   section 8.1's joint pair, against this note's "no filed rule estimates the share") is no fork: both end on the 13 and
   the predictive-value route is not a literal reading. Its process note (the log-only rebuild after pass 3 not
   re-judged) re-run on a fresh unzip of the shipped zip: the verifier passes 258 checks, and the call's date as
   recorded moves every district's mean days by 1.94 to 2.42 (pair.py --asks).

## Leak check

`leak.py --asof 2028-02-02`: the first cut's one LEAK was the request's file name (`quality_note`, an author-vocabulary
token), renamed elfs_2027_flows_release_request.eml; since then REVIEW, no LEAK. Each REVIEW line:
- Sweep 3, the bulletin: 11.9 is the Metropolitan Fringe's third-quarter unemployment rate, equal to that district's
  graded job-finding share only by coincidence of value (a different quantity, a different period). Harmless.
- Sweep 3, the bulletin's district names beside "unemployment remained highest": a descriptive sentence about
  unemployment rates, nothing on classification error or the warning; the 32 shared words of the call are the
  district names and the release's vocabulary. Harmless.
- Sweep 4, the dictionary, the README, the bulletin, the methodology note and the protocol: the shared terms are the
  field's nouns (quarter, status, reconciled, recorded, section, reinterview); none names true flows, an inversion or
  a correction at both quarters. Protocol section 7's "not large enough to measure classification error for a single
  district or a single quarter" is the design's own statement of what the reinterview measures (it pins the error's
  scope, SF5) and would exist without the build. Harmless.
- Sweep 6, the flows tables, the bulletin and the job centre registers: they name the districts beside flows, rates,
  unemployment and registrations; none gives a rate a share of counted moves or a warning, and none ranks the rates
  on the call. Harmless.

Reader (one isolated agent, Sonnet, medium, the prompt and the pack only), on the first cut: Q1 none ("No file names
it outright"; protocol section 7 read as a legitimate design statement); Q2 to Q4 none; Q5 section 8.1, executed as
the share of the persons Table F1 counts whose reconciled statuses were not the pair, the state's classification
error carried to each district's cells, the method left open (the design's own open HOW); Q6 an analytical choice;
every REVIEW line harmless. Its realism notes taken in one generator pass: the reconciled status now carries the same
codes as the two readings beside it, the log's call date is written like the visit start (yyyy-mm-dd), and the
dictionary lists the items in the files' column order. It also read the bulletin's employment rates (49 to 54 per cent)
as uniform; they are the simulated districts' own stocks and the bulletin is a distractor, left as drawn. The pass
moved no graded figure (179 checks, 258 verifier checks).

Second read (fresh copy of the rebuilt bundle, same isolation): Q1 none ("No file or sentence names a decisive step";
protocol section 7 read as a statement of what the reinterview supports); Q2 to Q4 none; Q5 section 8.1, executed as
the per-rate share of counted movers whose reconciled statuses were not the pair; Q6 "mostly an analytical choice about
pooling and about turning reconciled misclassification into a per-rate false-move share", nothing planted; every
REVIEW line harmless. It read section 8.2 as leaving the match rate's linking of split households open, the point the
judge's pass 2 made (Tried and rejected), and the visit's date in section 8.3 as two columns, which the window closes
(1,096 results outside it by the call's recorded date at the time, none by visit_start). Its realism notes taken in the same pass:
callbacks no longer fall on a Sunday (section 3's Monday to Saturday; a Sunday callback is the Saturday before), the
supervisors' visits open their forms in the day as well as the evening, and section 2 now says every district's sample
is the same size, which is why the reinterview counts are even across districts of different populations.

Third read (fresh copy, same isolation): Q1 to Q4 none; Q5 section 8.1, the estimator left open; Q6 "an analytical
choice"; the match rate "quite explicit... I found no open reading"; the visit's date in section 8.3 read as two
columns, closed by the data (the judge's passes 1 to 3 all reproduce on visit_start). Every REVIEW line harmless. Its
realism notes taken in one log-only pass (no graded figure moved, 186 checks): the app update no longer lands on every
tablet on one quarter boundary but at each supervisor's own Friday sync between 18 June and 9 July 2027, and the visits'
clock times run as a daytime spread and an evening peak about 18:00, with Friday's calls in the evening after the
office day. It also read the bimodal job-loss rates (1.0 to 1.5 against 3.9 to 4.8) as designed; they are the
districts' labour markets (farming districts where few lose work, urban districts with high turnover), left as drawn.

## Tried and rejected

- 2026-10-18, architecture 0 (the seed's own world, coded write-ins and a recode): the net against gross difference
  rate decides only by reading a definition (data semantics); correlated coder variance through interpenetrated
  workloads repeats task228's lesson (variance built at the unit that carries many records); a fallible expert recode
  repeats task246; error rates carried route by route repeat task230 and task242; a fixed take per coder or batch is
  one reweighting (an opponent reflex); acceptance-sampling outgoing quality reads the same with factory lots (fails the
  swap). World moved to the labour force survey's panel flows, keeping the reinterview, the published categories and
  the classification error.
- 2026-10-18, laboratory proficiency testing with results below each laboratory's reporting limit: dropping or
  substituting the censored results moves the consensus by about 3 per cent at realistic censoring, too little to move
  a laboratory across the action line with margin; and censored results are listed as Layer 1 mess for this domain.
- 2026-10-18, simulation seed 253 kept for its margin: three match rates (River Basin 0.001 from the edge, Central
  Hills 0.002, University Towns 0.005) and five shares sat inside 7 per cent of a bin of their rounding edges, and no
  records seed moves the match rates. The reinterview was given its own random stream (the households, the flows and
  the match rates stay put while the classification error is redrawn) and the simulation, reinterview and records seeds
  were searched jointly for every graded figure off its edge.
- 2026-10-18, simulation seed 364: Cocoa Belt East's job-finding rate came out at 1.3 per cent with the error taken
  out (91.6 per cent of its counted moves not real) against 9.0 per cent in the simulation's own truth, sampling noise
  in a small unemployed stock; an implausible adjusted rate beside a published 11.3. Seeds kept only where every
  adjusted job-finding rate is 5 per cent or more and no share passes 80 per cent.
- 2026-10-18, a reconciliation that always returned the true status: protocol section 4 reviews only a difference
  between the two readings, so two readings that agree stand, right or wrong; the reconciled status now equals the
  original reading wherever the supervisor's own reading agrees with it.
- 2026-10-18, callbacks drawn without regard to the reinterview: a member interviewed on a callback day could be
  interviewed after the supervisor's first call, or fall inside the window of a household completed late; callbacks in
  selected households are capped so every member is interviewed before the first call and a late reinterview is late
  for every member.
- 2026-10-18, Ask A's primary on the split households' renumbered lines (judge pass 2, FIX_NOW): the golden linked a
  split-off household's members on sex and month and year of birth, but no filed sentence said so, and the link section
  7 documents (dwelling, household and line) gives other figures in all twelve districts (underspecified_objective).
  Filing the link closes the fork and hands the device to the careful solver (the measured pair ceiling would pass 50),
  so the link is filed in section 8.2 as a paid pin and the primary moved to the server's restore of 17 May, which took
  in the uploads of 14 May again under the dwelling's next household numbers (D1, a replay under fresh ids); the ask's
  second figure moved from the persons interviewed again to the persons the rate is based on, which the replay moves.
