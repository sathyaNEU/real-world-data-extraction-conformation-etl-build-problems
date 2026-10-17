# task469 design note: Kelderby's summer 2027 ground time review

Status lives in `pipeline.json`; this note holds the design. Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task469.json` (architecture v1), registered 2026-10-17 after a pull, so
  every card filed before it was in the check. Guard check WARN only, answered here: Gate G method_or_model_selection
  is in seven of the last twelve builds (it is the honest key: the decisive step is choosing an estimator that treats
  the hidden turn times as censored, against the observed ground times or the overruns alone). The structural tests'
  older matches are differentiated on the card: task101 (a threshold cut from a distribution the decision's own
  payments had entered), task126 (units a succession link joined) and task450 v1 (durations sampled in proportion to
  length by scheduled visits). Nearest driver task155 at 0.09.
- **Seed:** ET26 (an airport authority's performance team saw its hub's arrival on-time rate fall between two summers;
  the dashboard listed the regional operators apart from the brands they fly for, and the board asked the wrong airline
  for an explanation). Kept: the world (a hub, the brands and the regional operators flying for them, the authority's
  performance team) and the carrier relationship as the unit the authority holds to account; the quantity stays
  punctuality, read where the authority can act on it, the time a relationship's turns need at its stands. Made forward
  facing: the call is on the ground times the airlines filed for summer 2027. Dropped: the seed's move (mix against rate
  between the brand and its partners), which is composition_mix and banned against the last three, and the marketing
  against operating carrier reading, which is data semantics; it survives as a lower rung (pooling one operator's
  turns for two brands).
- **Pairing:** General Statistics & Data Science / data-integration-record-linkage-entity-resolution / ETL. The
  authority's evidence is a linked dataset: its operational database's stand events (on-block and off-block, keyed by
  registration, stand and ATC callsign), the filed schedules (commercial flight numbers in SSIM files), the operators'
  flight logs with their delay codes (two code versions) and the affiliate register, joined into turns. GSDS is a
  methods domain, so the swap is of the method: the deciding quantity is a tail probability of a duration that the
  schedule left-censors (estimation_fit, censoring and truncation), and replacing the censoring-aware estimate with the
  share of observed ground times, of overruns, or of the turns scheduled at the new ground time in 2026 moves the call.
- **Shape:** 14, cuts of a distribution per segment: for each carrier relationship and aircraft type at the E gates,
  the share of turns that need longer than the ground time it filed, the shortest ground time the authority would
  accept on its 20 per cent standard, and the verdict on the filing.
- **Strategy:** maturity_censoring (the censoring family: here the allowance, not the cut, hides the values), decisive
  generator G3 (the stand log's ground time against the turn's need), with G17 (the censoring-aware estimate) and G13
  (the 2026 allowance against the shorter 2027 one).
- **World:** Canada, an unnamed province. Kelderby International Airport is run by the Kelderby Airport Authority, a
  not-for-profit airport authority, and is a schedules-facilitated airport for its regional concourse (the E gates,
  ground-level stands with walk-out boarding). Norvale Air, the hub's dominant brand, sells Norvale Connect flights
  flown by Pellmont Aviation (E175 jets), Grayling Air (ATR 72s) and Sable Coast Air (Q400 turboprops) under capacity
  purchase agreements and turned by Norvale Ground Services; Tellura Airways sells Tellura Express flights flown by
  Pellmont (E175) and Sable Coast (Q400) and turned by Aerocrest Handling; Grayling Air flies and turns its own ATR 72s.
  Six relationships, each sharing its operator and aircraft type with one other (the operator's flying for the other
  brand), which is what lets the 2027 submissions carry each brand's numbers on its partner's rotations. The authority's schedule facilitation
  guideline accepts a filed minimum ground time at the E gates when no more than 20 per cent of the relationship's
  turns of that aircraft type would need longer, judged on the turns of the most recent summer peak (15 June to 15
  September 2026); a turn needs the time from on-block until the aircraft is ready to push back. For summer 2027 the
  carriers filed shorter ground times for most relationships.
- **Forcing fact:** the authority's Schedule Facilitation Committee answers the summer 2027 initial submissions at its
  18 November 2026 meeting; the airside operations director's workbook goes to it. As-of: 30 October 2026. The call
  faces forward (the 2027 season's turns, not yet run); the evidence is the closed 2026 peak.
- **Context artifact, re-keyed at stage 3:** operations_log (the authority's stand log, the spine, with the operators'
  flight logs), was filed_standard; task240 (filed_standard), registered at 18:42 but pushed after this draw, entered
  the last three and the heart screen blocked. SFG-3 stays the filed estimand.
- **Forum and forcing event:** committee_or_panel (the Schedule Facilitation Committee), season_or_peak (the summer
  2027 schedule submissions). Organisation utility_or_infrastructure; role operations_director. Personas from
  `guard.py names --geo Canada --seed 469`: Joanne Gilbert (Director, Airside Operations, who brings the review to
  the committee), Gabriela Armstrong (analyst, Airside Performance, who keeps the stand log) and Arthur Bryant
  (Manager, Gate Planning); Danielle Welch replaced (her first name in task101).
- **Data-native sentence:** a turn at the E gates pushes back on time whenever it is ready by its scheduled departure,
  so the stand log shows how long a turn needed only when the turn held the departure up; under the 2026 schedules most
  turns had more time than the carriers now file for 2027, so the turns that would need longer than the new ground
  time mostly finished inside their old allowance and left on time, and only the turns whose inbound came in late
  enough to leave less than the new ground time show the share in full.
- **The WHAT screen.** Population: a relationship's turns of one aircraft type at the E gates (one aircraft's stand
  visit from on-block to off-block between an arrival and a departure of that relationship), the summer 2027 turns
  judged by the summer 2026 peak's (filed in the guideline). Outcome: the turn needs longer than the filed ground time,
  need being on-block to ready for pushback. Window: 15 June to 15 September 2026 as evidence, summer 2027 as the
  application. Unit: turns. Comparison: 20 per cent. The decisive step settles none of them: it is how the share is
  estimated from turns whose need the schedule hid whenever they finished inside their allowance.
- **Deliverables:** `kelderby_summer2027_ground_time_review.xlsx` (the call: each relationship's verdict on its filed
  ground time and the shortest it could file, each share needing longer, the asks, a chart of the shares against the
  standard).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, data-integration-record-linkage-entity-resolution: the
    ETL task type the conformance sits in; the decisive analytic is the domain's treatment of censored durations
    (`two-layer-task-design.md`, estimation_fit, censoring and truncation), with no pattern on file for an allowance
    hiding the values, so the pattern is the build's own.
  - `dataset-generation/references/layer1-messiness.md`: a stand log in local time beside operators' logs in UTC, ATC
    callsigns against commercial flight numbers, SSIM fixed-width schedules, two delay-code versions, tows splitting a
    turn across stands, registrations with and without the hyphen, an aircraft moving between operators and flight
    number blocks changing hands mid-summer; none on the decisive step, each to be asserted neutral.
  - The lane's spent drivers (`guard.py mechanisms --objective etl`, 47 builds): none reads a duration hidden by an
    allowance; the nearest families are maturity (task451, task458, task462: values not yet observed at a cut) and
    length-biased sampling (task450 v1), both differentiated.

## Default path

1. Read SFG-3 (kda_schedule_facilitation_guideline_e_gates.pdf): a filed minimum ground time is accepted when no more
   than 20 per cent of the relationship's turns would need longer than it, judged on its turns at the E gates with
   on-block from 15 June to 15 September 2026; a turn needs the time from on-block until it is ready to push back.
2. Build the turns from the stand log: each aircraft's on-block at an E stand paired with its next off-block on the
   same operating day, registrations read without the hyphen, tows kept; the relationship from the departing flight's
   callsign number in the affiliate register's blocks and the aircraft register's type: 9,212 peak turns.
3. Join each departure to its operator's log (Pellmont from UTC, Sable Coast's sub-code letters dropped, Grayling's
   delay field split) and group the delay minutes by kdy_delay_code_groups.csv.
4. Read each turn's need: where a not-ready delay held the departure, the time it had (scheduled departure less
   on-block) plus the not-ready minutes, an exact need; where the aircraft left on time it was ready in time, so it did
   not need longer.
5. Count the turns whose need exceeds the filed ground time over all of the relationship's peak turns: 7.1, 2.1, 1.8,
   8.6, 5.6 and 0.2 per cent (Norvale Connect by Pellmont, by Grayling and by Sable Coast, Tellura Express by Pellmont
   and by Sable Coast, Grayling), every one under 20.
6. Accept every filing; each would be accepted at the shortest step on the grid.

Ends on: accept all six filings

Golden: send back the filings of Norvale Connect by Pellmont (E175, 35 minutes), Tellura Express by Pellmont (E175, 40)
and Tellura Express by Sable Coast (Q400, 30), shortest acceptable 40, 45 and 35; accept the other three (shortest 40,
30 and 30)

## Stump sentence

The default path counts as needing longer than the filed ground time only the 2026 turns whose need the records show
above it, the departures a not-ready delay held, over every peak turn, so no relationship comes out above 9 per cent
and it would accept all six filings; but under the 2026 schedules most turns had more time on the ground than the
carriers now file, and a turn ready inside its old allowance left on time with its need hidden, so the share is an
estimate from needs left-censored by the time each turn had: read where it is fully observed (the turns that had less
than the filing) or with the product-limit estimator, 27, 26 and 31 per cent of the Pellmont E175 relationships' and
Tellura's Q400 turns would need longer, and those three filings go back at 40, 45 and 35 minutes.

## Three rules

Task type: data-integration-record-linkage-entity-resolution: the authority's stand log linked to three operators' flight logs (UTC, station local time with AHM 731 sub-codes, a combined delay field), the affiliate register's number blocks and the aircraft register into one table of turns per carrier relationship, and the carriers' merged SSIM submissions conformed to operating turns, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is a tail probability of a duration the schedule left-censors: a turn's need is seen exactly only when it outran the time the 2026 schedule gave it, and is otherwise known only to be no longer than that time; the field's estimators for left-censored durations (the share where the indicator is fully observed, the product-limit estimator in reverse time, a censored maximum-likelihood fit) agree at 27, 26 and 31 per cent for the three filings sent back, while the generic summaries (overruns over all turns, the stand time, the like-for-like turns, pooled operators) each move the call.

Swap: "which wards' requested discharge-preparation times a hospital should accept, judged on last year's discharges, where preparation time shows only when it delayed the planned departure" keeps the shape, because in a methods field the setting is always another field's; the swap is of the method, and the decisions move the moment the censoring-aware estimate is replaced by the visible overruns, the stand times or the like-for-like turns, while the 20 per cent standard, the relationships and the E gates are the airport's own.

Layer 1: the stand log in local time with the docking system's registrations unhyphenated and ramp control's hyphenated, tows splitting a turn across an E and a remote stand, ATC callsigns against the brands' commercial numbers, Pellmont's log in UTC, Sable Coast's workbook in station local time with AHM 731 sub-coded delays, Grayling's sector file with its delays in one field, a minute's difference on some block times between the operators' ACARS and the stand log, late arrivals after midnight that night-stop, the season schedule's period splits at the 3 August retimings and a number block transferred mid-summer; on the ask's side the merged 2027 submissions as each brand sent them (two files in UTC, each brand's legs on its partner's flights, through stops as leg sequences, night stops by rotation layover). Each is asserted neutral for the call (checks.py Layer 1, SF1 to SF4).

Layer 2: estimation_fit under censoring: the need is left-censored by each turn's own allowance, so the share needing longer than a shorter ground time is estimated from the censored sample, where the indicator is fully observed or with the product-limit estimator, never from the overruns the records happen to show.

Decisive step: treating every on-time turn's need as left-censored at the time it had and estimating each relationship's share needing longer than its filing with a censoring-aware estimator (27, 6, 7, 26, 31 and 1 per cent by the product-limit estimator), which sends back the two Pellmont E175 filings and Tellura's Q400 filing and sets the shortest acceptable times.

Not semantics: every field, code, unit and definition read correctly (on-block from the stand log, delay codes grouped by the authority's file with sub-code letters dropped, UTC converted, registrations normalised, the relationship from the departing flight, need as on-block to ready) still leaves the easy route counting only the overruns the records show over every turn, because no field marks a need as hidden; the step is how a censored sample is estimated, not a reading.

Not rule application: SFG-3 fixes the population, the outcome (needing longer than the filing, need from on-block to ready), the 20 per cent standard and the five-minute steps, and the code file groups the codes; no rule or procedure says how the share is estimated when a turn's need is hidden, and executing every filed rule with the visible overruns accepts all six, with the stand time sends all six back.

Analyst test: a strong analyst who builds the turns correctly and reads every field and rule counts the turns whose recorded need exceeds the filing over all turns and would accept all six filings (the default path's Ends on); one who reads each turn's time on the stand as its need sends all six back; the censoring-aware estimate sends back three.

Estimand: SFG-3 2.1 to 2.5 and 3.1 to 3.3 (kda_schedule_facilitation_guideline_e_gates.pdf): the share of a relationship's turns at the E gates with on-block from 15 June to 15 September 2026 that need longer than its filed ground time, need running from on-block to ready for pushback, against no more than 20 per cent, in five-minute steps; a turn is a stand visit within one operating day and belongs to its departing flight's relationship.

No decoy: nothing is planted to be caught; the stand log, the operators' logs, the schedules and the registers are what each system writes; no memo, briefing or draft argues a method or a share; the punctuality workbook and the staffing file are what the authority keeps and rank nothing on the turns' needs; no document computes a share or a decision.

No certified replay: no published or certified figure reproduces only under one method; the pack holds no earlier review, accepted ground time history or published share to back an estimator out of, and nothing is recovered by matching a filed number.

Lesson: when a schedule's allowance hides how long a process needed whenever it finished inside it, the share that would outrun a shorter allowance is a censored-data estimate, read where the outcome is fully observed or with the product-limit estimator, never the overruns that happened to be recorded; no build on file estimates a tail from durations an allowance left-censored.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the overruns the records show over every turn (accept all six) | SFG-3 2.4 defines the need and the code file gives the not-ready minutes: fires | the delay columns give an exact need on every late turn: fires | counting overruns is the reflex: fires | none | none | one share per relationship: fires | readable |
| R1, the stand time as the need (send back all six) | the stand log's on-block and off-block: fires | two columns subtracted: fires | ground time is the reflex for a turn: fires | none | none | one difference: fires | readable |
| R2, the 2026 turns scheduled like the filing (send back Tellura/Pellmont and Grayling) | the 2026 season schedule gives each turn's scheduled time: fires | none | judging a new standard on like cases is a reflex: fires | none | none | one share: fires | readable |
| R4, one operator's type pooled across its two brands (send back Norvale/Pellmont) | the operators' logs come one file per operator: fires | none | grouping by the file is a reflex: fires | none | none | none | readable |
| R5, every late minute as the turn's (send back four) | the delay minutes: fires | the delay columns: fires | none | none | none | one sum: fires | readable |
| D (decisive), each on-time turn's need left-censored at the time it had, the share estimated where fully observed or by the product-limit estimator (send back three) | no clause says an on-time turn's need is hidden or names a censored estimate; 2.4 defines need and is silent on how to estimate it: silent | no column flags a hidden need; the bound is computed (scheduled departure less on-block) from two files: silent | the reflexes are the overruns and the stand time; treating ready-in-time turns as censored is no battery step: silent | no control, earlier review or published share scores an estimator: silent | every file reconciles and nothing is anomalous: silent | a product-limit product over hundreds of risk sets, or a share on a computed subset: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a turn that is towed | kept: the visit runs from on-block on the E stand to off-block, after the tow included | towed turns dropped | same call (asserted) | SFG-3 2.2 "including any time on a remote stand after a tow" |
| SF2 | turns at the E gates | visits whose on-block is on an E stand | every turn, remote stands included | same call (asserted) | SFG-3 2.2 and 3.2 "an aircraft's visit to an E gate stand", "turns at the E gates" |
| SF3 | a through stop (the same flight number in and out) | a turn: an arrival and the same aircraft's next departure | through stops dropped | same call (asserted) | SFG-3 2.2 defines the turn by the aircraft's visit, not the flight number |
| SF4 | on-block and off-block | the stand log's times | the operators' own block times (a minute apart on some movements) | same call (asserted) | SFG-3 2.3 "the times the authority's stand log records" |
| SF5 | needing longer than | need strictly over the ground time | at least the ground time | same call (asserted) | SFG-3 3.1 "need longer than it" |
| SF6 | no more than 20 per cent | at or under 20 per cent | under 20 per cent | same call: no share within 6 points of 20 at any step (asserted) | SFG-3 3.1 "no more than" |
| SF7 | the peak | on-block 15 June to 15 September 2026 inclusive | a day off either end | same call (asserted) | SFG-3 3.2 "from 15 June to 15 September inclusive" |
| SF8 | the turn's relationship | the departing flight's | the arriving flight's | same call: no turn's two flights differ (asserted) | SFG-3 2.1 "the relationship of its departing flight" |
| SF9 | IATA code 93 (late inbound rotation) | aircraft not ready | held for another reason | accept all six (asserted) | kdy_delay_code_groups.csv: 93 "aircraft not ready" |
| SF10 | Sable Coast's lettered sub-codes | the two digits' group | codes not in the file left unread | send back the Pellmont E175 pair only (asserted) | SFG-3 2.5 "an operator's sub-code letter does not change the group" |
| SF11 | minutes a ready aircraft was held | not need | counted as need | send back four (asserted, R5) | SFG-3 2.4 "time a ready aircraft is held ... is not time the turn needs" |
| SF12 | the estimate of the share | the product-limit estimator for left-censored needs | the share among turns with less than the ground time (strictly or not), a censored lognormal fit | same call and the same shortest times on five populations, nearest edge 5.7 points (C1, asserted) | the data's structure: every censoring-aware estimator agrees; the estimators that ignore the censoring are the rungs |

## Ladder

- **R0, the default path: the visible overruns over every turn (accept all six).** 7.1, 2.1, 1.8, 8.6, 5.6 and 0.2 per
  cent; the largest is 11.4 points under the standard. Dies to one fact: a turn that left on time had, under the 2026
  schedule, 35 to 50 minutes on the ground, more than most filings, so being ready in time says nothing about whether
  it needed more than the filing.
- **R1, the obvious correction: the stand time as the need (send back all six).** 74 to 91 per cent of turns sat on
  the stand longer than the filing. Dies to SFG-3 2.4: a ready aircraft waited for its scheduled departure.
- **R2, the sophisticated one: the 2026 turns scheduled with no more than the filing (send back Tellura/Pellmont and
  Grayling).** 31 and 32 per cent of those turns held their departure; Norvale/Pellmont 10, Tellura/Sable 10, and
  Norvale/Grayling and Norvale/Sable have no 2026 turn scheduled that short. Dies to the data's structure: the turns
  scheduled short are particular hours and lines (Grayling's evening turns, Tellura's midday bank), and holding the
  departure is not needing longer than the filing.
- **R4, one operator's type pooled across its brands (send back Norvale/Pellmont only).** Pellmont's E175s at 35 and
  40 minutes, Sable Coast's Q400s at 30, Grayling's ATR 72s at 40 and 35: 40, 13, 13, 13, 2 and 13 per cent. Dies to
  SFG-3 2.1: the relationship is the brand, the operator and the type, and each brand's handler turns its own.
- **R5, every late minute as the turn's (send back four).** Adds Norvale/Grayling at 29 per cent. Dies to SFG-3 2.4.
- **D, the decisive move (send back three).** Product-limit estimates at the filings 27, 6, 7, 26, 31 and 1 per cent;
  shortest acceptable 40, 40, 30, 45, 35 and 30 minutes. The clean truth (every need known) gives 33, 9, 8, 30, 44 and 1
  per cent and the same six decisions and shortest times (asserted).
- **Margins:** across five populations (golden, remote stands added, towed out, through stops out, a day off each end)
  by four estimators (fully observed with < and <=, product-limit, censored lognormal) every decision and every
  shortest time holds; the nearest edge to 20 per cent is 5.7 points (Norvale/Sable at its filing, lognormal, through
  stops out). R0's nearest is 11.4 points under, R1's 54 over.
- **Position, separation and dominance:** every rung names its own set (none, all six, {Tellura/Pellmont, Grayling},
  {Norvale/Pellmont}, four, three); the corrections from R0 walk the count of send-backs up through R1's six and only
  the censoring-aware estimate brings it to three, with two of R2's picks wrong both ways.
- **Worth on the graded quantities:** six decisions and six shortest times; R0 gets three decisions and no shortest
  time, R1 three and none, R2 three and none, R4 four and two, R5 five and four (generator/ceiling.py).
- **Grid:** recognising the censoring is the move every other correction lacks; codes misread (SF9, SF10) and held
  minutes counted (SF11) land on named wrong sets, and none of them composes back to the golden.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | each relationship's turns at the E gates with on-block 15 June to 15 September 2026 (SFG-3 2.2, 3.2); towed in, remote-stand turns out, through stops in (SF1 to SF3, C1) |
| 2 | Unit of account | the turn (SFG-3 2.2); ground times in minutes (3.3) |
| 3 | Attribution window | a turn on its on-block date; one operating day, 03:00 to 02:59 (SFG-3 2.2) |
| 4 | As-of dating | the stand log exported 2 October 2026; each operator's log as sent; the filings of October 2026 |
| 5 | Version basis | one version of every file; one filing per relationship |
| 6 | Denominator | all the relationship's peak turns (SFG-3 3.1 "the relationship's turns"); the estimator's conditioning is the method (C1) |
| 7 | Weighting | each turn once |
| 8 | Window length | the filed peak (SFG-3 3.2); a day either way gives the same call (SF7) |
| 9 | Boundary inclusivity | "no more than 20 per cent" at or under (SF6); "need longer than" strictly over (SF5) |
| 10 | Rounding path | the share unrounded against 20 per cent; the shortest acceptable is the shortest five-minute step at or under it (SFG-3 3.3) |
| 11 | Tie-break | none: each relationship's decision is its own |
| 12 | Maturity and censoring | the 2026 peak is closed; the need is left-censored by each turn's own allowance, the decisive step (HOW), every censoring-aware estimator agreeing (SF12) |
| 13 | Order of operations | turns, relationship, need (exact or bounded), share, decision, shortest step |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | no duplicate turn or event on the main path (event ids unique, asserted) |
| 16 | Identity normalisation | registrations with and without the hyphen are one aircraft; the callsign number is the commercial number (Layer 1, asserted neutral) |
| 17 | Netting | minutes a ready aircraft was held are not need (SFG-3 2.4, SF11) |
| 18 | Dimensional units | minutes; Pellmont's UTC to Kelderby local (UTC-4 all summer, the stations file and the SSIM variations) |
| 19 | Code and status semantics | delay codes grouped by kdy_delay_code_groups.csv, sub-code letters dropped (SF9, SF10); never the stump |
| 20 | Integerisation | whole minutes; whole turns |
| 21 | Clause scope | SFG-3 3.2: summer 2027 filings judged on the summer 2026 peak |
| 22 | Forward window contents | the filed 2027 ground times (filings file); the 2027 week from the initial submissions |

## Literal reader

Executed word for word, SFG-3 takes each relationship's turns at the E gates with on-block in the 2026 peak (9,212
turns), each turn's need from on-block to ready for pushback, and asks whether more than 20 per cent of them would need
longer than the filing; the files show a turn's need exactly only where it held its departure and otherwise bound it by
the time the turn had, a structure SFG-3 files without saying how to estimate across it; of the estimates the files
support, the visible overruns over every turn contradict the bound (a turn ready in time could still need longer than a
shorter ground time), the stand time contradicts 2.4, and every censoring-aware estimate agrees on all six decisions and
shortest times, so the literal execution sends back three filings at 40, 45 and 35 minutes; no filed rule, basis or
formula reads to another set.

## Oracles

- The monthly punctuality workbook (a distractor): on-time departure and arrival rates by brand and month; on the
  wrong path it reads as Tellura's turns being slower, but it carries no turn, no ground time and no share, and ties to
  nothing under any basis.
- The handling staffing file (a distractor): agents rostered and present by handler and shift; no figure ties.
- The 2026 season schedule's ground times: the scheduled times R2 reads; they tie to the operators' logs under every
  reading and score no estimator.
- None ties only under the golden.

## Ask sheet

- **Ask A, for each relationship, the turns the summer 2027 initial submissions schedule at Kelderby in the week of 12
  to 18 July 2027 and how many are scheduled shorter than the ground time it filed (whole turns).** H18 home: the audit
  trail of the input the call is about: each filing's peak-week exposure in the submissions it governs, and the turns
  the carrier already schedules below its own filing. Use: the committee's response to each carrier quotes the turns
  its decision touches. Path: kdy_initial_submissions_s27.ssim (records 2 and 3: time mode, airline, flight, leg
  sequence, period, days, stations, aircraft times, UTC variations, equipment, onward airline, flight and layover, date
  variation), kdy_schedule_file_layout.pdf, the affiliate register's blocks, the filings, SFG-3 2.1 and 2.2, the fleet
  plan and the 2026 season schedule: seven files, fifteen columns. Primary device: D1, the same records under two key
  schemes: each brand files the rotations it sells on its partner's aircraft again under its own numbers, inside its
  own block for the same operator, so the affiliate register maps every such leg to the brand's own relationship with
  that operator and type (Tellura's numbers on a Norvale/Pellmont rotation read as Tellura/Pellmont, and so for every
  pair). The authority's schedule database holds record types 1, 2, 3 and 5, so no segment data record ties a leg to
  its operating flight; the evidence is split: the rotation repeated leg for leg (stations, times, type) in the 2027
  file, numbers the 2026 season schedule never carried, and a fleet plan that gives each operator one aircraft per
  operating rotation and a spare (Pellmont would need 19 E175s for its filed rotations against 13, Sable Coast 17 Q400s
  against 12, Grayling 11 ATR 72s against 7). Every relationship carries such rotations and has turns shorter than its
  filing, so all twelve figures move (asserted). Hazards: two brands' files in UTC (their rotation layover counts UTC
  days), through stops as a leg sequence with no onward link (each is also the turn the carriers schedule short), night
  stops by rotation layover, and genuine same-minute trips of two relationships' aircraft beside the repeated
  rotations. Stops (asserted, generator/ceiling.py and checks.py): every leg counted (the cracker: key checks pass, no
  exact duplicate, every join maps) misses all 12; schedule fields deduplicated on Kelderby time (the over-cleaner)
  misses all 12; each repeated rotation kept once under the first file's numbers misses all 12; the through stops
  missed misses all 12; the rotation layover as the day test misses 2; the golden keeps each repeated rotation once,
  under the numbers that operated in 2026, and equals the operating lines' truth.
  Realism: a facilitated airport merges the brands' files as received, and a stand-planning database that keeps leg
  records drops the carriers' marketing cross-references.
- **The construction layer:** the six decisions, the six shortest times and the chart; the cracker has them.
- **Main population zero-counts (asserted):** the call reads the stand log, the three operators' logs, the delay code
  groups, the registers and the filings; no 2026 file carries a DEI 050 record or a partner's number, and deleting the
  2027 submissions, the fleet plan and the 2026 schedule leaves every turn and every need.
- **Hazard table (asserted):** D1 moves all 12 figures; the through stops all 12 for a response that follows onward
  links only; the layover read as the day one (Tellura/Pellmont's turns); a schedule-field deduplication all 12.
- **Referee:** none; no total in the ask's files ties under one handling only (the fleet plan gives aircraft by
  operator and month, which the repeated rotations exceed, a cross-file cut nothing invites).

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each relationship's peak-week turns and turns shorter than its filing, 2027 submissions | parses the merged file by the layout note, converts the UTC files, follows onward links and leg sequences, maps every leg through the register's blocks; the partners' rotations pass every key check, carry no cross-reference and land in the other brand's relationship | miss |

- Mirror leakage: 0.0 per cent of ask weight (the best mirror, on R5, keeps no Ask A figure: generator/ceiling.py).
- Pair ceiling: 37.2 (weights 38 / 7 / 55: the call 8, each relationship's decision and shortest time 2.5; the
  cracker keeps the main block and instructions, 45.0; the best mirror, R5, keeps five decisions and four shortest
  times, 29.5; average 37.2), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Pre-ship check

- **Three rules, re-read against the built pack.** Domain: the deciding quantity is each relationship's share of 2026
  peak turns needing longer than its filing, a tail of a duration the schedule left-censors, estimated the way
  statistics treats censored durations; the visible overruns accept all six, the stand time sends all six back, the
  censoring-aware estimates send back three, on the clean truth and on the pack (checks.py R1 to R3b). Two layers: the
  Layer 1 inventory in `## Three rules`, each item asserted neutral on the call (Layer 1 rows, SF1 to SF4); the ask's
  device confined to the 2027 submissions (separation rows); Layer 2 the censoring. The decisive step is none of the
  three banned kinds, each executed in checks.py: not a plant (R3c: no document names censoring, an estimator, a
  verdict or a shortest time; no copied block, memo or draft); not data semantics (SF1 to SF11: every term read right
  still leaves the overruns accepting all six); not rule application (R2: every filed rule executed with the visible
  overruns accepts all six; R3b with the stand time sends all six back; R3a only the censored estimate sends back
  three).
- **Gates.** 16 files in 4 formats (csv, pdf, ssim, xlsx); the stand log at 28,392 rows; two distractors (the monthly
  punctuality workbook and the handling staffing file), each deletion asserted; checks.py green; verify.py from the
  bundle alone (its own readers, turn builder, product-limit estimator and SSIM parser) matches the golden; two builds
  byte-identical; figures_check.py (107 figures), precut.py (50) and voice-check.py exit 0; leak.py REVIEW (no LEAK);
  guard heart WARN after the context artifact was re-keyed (Gate G overuse, answered in the draw); the containers clean
  (H1 audit, pack and golden); golden-realism pass on the workbook (finding titles, a Notes sheet from SFG-3 and the
  pack's own exclusions, totals, frozen headers, a palette marking the three filings sent back).
- **Surface screen, for the author (not adjudicated here):** three promoted pairs: task468 (back to back, the same
  domain and objective pairing, gap and context artifact; task468 is paused), task101 (gap, pattern and decision
  family, differentiated on the card) and task126 (gap, pattern and Gate G, differentiated on the card).

## Leak check

`leak.py --asof 2026-10-30`: REVIEW, no LEAK. Each REVIEW line answered: the guideline's example relationship
(Norvale Connect flown by Pellmont's Embraer 175s) is the definition's example, naming no share, estimator or decision;
its world nouns (Pellmont, Norvale, aircraft, filing, operator, departure) describe its subject; the registers and the
fleet plan name the relationships beside counts, numbers and dates and rank nothing on the turns' needs. Harmless.

Reader, round 1 (answers in `leak_check_report.md`): nothing quoted as the decisive step beyond SFG-3 2.4, 3.1 and
3.2, which define need, the standard and the window; no ranking or answer-shaped file; its own answer sent all six
filings back (shortest 55, 55, 50, 60, 45 and 50 minutes) on each turn's stand time less the minutes a ready aircraft
was held, the R1 rung exactly, and its question 6 described that path as rules applied to data read correctly, which
is what R1 is: it never asked what an on-time turn's record hides. On the schedule ask it dropped the DEI 050 legs as
marketing duplicates and filed all twelve figures: the device was dead and was rebuilt (`## Tried and rejected`). Its
realism findings were fixed in the generator in one pass: spare aircraft carried Embraer serials on Dash 8s and ATRs
and place names for a home base (serials now in each type's series, bases as station codes); a number block passed to
Sable Coast that no flight used (removed); the stations file repeated the schedule's block minutes (now the summer and
winter UTC offsets); a ready aircraft always pushed back on the scheduled minute (now within a couple of minutes, the
late minute coded as a start-up hold); an added 2027 line kept its template's first arrival number (renumbered); 2027
ground times now include the longer midday turns. Every graded figure is unchanged (figures.json differs only in its
stated-reference block).

Judge, pass 1 (`determinism_check_report.md`): DETERMINISTIC, APPROVE. Every graded figure reproduced from a fresh
unzip (the six peak turn counts, the shares, the six decisions and shortest times, the twelve week figures); the
nearest decision edge 6 points; a second estimator, uncoded minutes as not ready, other windows and remote-stand turns
all give the same decisions. Gate G statistical_rigor, analytical_non_defect, no surface-read dependency; Gate H
domain pass, layers pass, decisive step analytical. Optional: whether an accepted relationship's shortest time is the
standard's step or its filing (the literal reading already gives Grayling's 30); left as it is.

## Tried and rejected

- 2026-10-17, at the draw: the seed's own move, the hub's on-time fall split into mix against rate between the brand's
  mainline and its regional partners: composition_mix, banned against the last three (task194), and the client counts
  it as Simpson's paradox already taught.
- 2026-10-17, at the draw: marketing brand against operating carrier as the decisive step: a field reading (data
  semantics); kept only as a lower rung, one operator's turns for two brands pooled.
- 2026-10-17, at the draw: delay propagation through aircraft rotations (delay the hub generated against delay carried
  in): the decisive step defines the outcome (what delay a station generated), so the WHAT screen kills it; filed it is
  rule application, unfiled the call is not determinate.
- 2026-10-17, at the draw: linking the stand log's ATC callsigns to commercial flight numbers with nearest-schedule
  false links pulling late arrivals onto the next flight: the record-linkage pattern's other half, but task468, one
  build back, carried the matcher-error family, and catching the false links would be what decides (a plant by the
  litmus).
- 2026-10-17, at the draw: operators' reported arrival times against the authority's docking sensors, corrected by a
  sensor subsample's sensitivity and specificity: the reporting error reads as planted, and task230 and task456 already
  teach misclassification correction.
- 2026-10-17, at the draw: ramp-log times rounded to five minutes heaping on the 15-minute threshold: the decisive step
  would be reading the rounding convention (data semantics), on a margin under a point.
- 2026-10-17, at the draw: day-clustered uncertainty in the summers' on-time change (signal against noise): the
  analytic belongs to complex-survey-estimation-variance, which serves no ETL objective, and the call would retag as
  anomaly detection.
- 2026-10-17, at design: Pellmont's CRJ900 lines filed as CR9 in the 2027 submissions while the fleet plan retires the
  type on 31 May 2027, as the schedule ask's device: the relationship of a July turn would turn on which source names
  the type, a fork a judge closes with a pin, and the pin hands the reading to the cracker; the CRJ900 relationship
  was replaced by Norvale Connect flown by Grayling's ATR 72s, so every relationship has a partner for the duplicates.
- 2026-10-17, at design: turns scheduled shorter than the filing at random: some relationships' second figure then
  sat outside every duplicated line and the device missed it; the carriers' through stops are the short turns instead,
  as transit stops with passengers on board are scheduled.
- 2026-10-17, at design: a turn as an arrival and departure on the same calendar date: a late arrival after midnight
  paired with the next morning's first departure (nine visits); SFG-3 2.2 now files the operating day, 03:00 to 02:59.
- 2026-10-17, at stage 4: the partners' legs tied to their operating flights by DEI 050 segment data records: reader
  round 1 knew the record (a marketing duplicate's cross-reference), dropped those legs and filed all twelve figures,
  so the device was free to any schedule-literate solver; the merged file now holds record types 1, 2, 3 and 5, as the
  authority's schedule database keeps them, and a partner's rotation is found only as a rotation repeated leg for leg,
  the fleet plan and the 2026 season schedule corroborating.
