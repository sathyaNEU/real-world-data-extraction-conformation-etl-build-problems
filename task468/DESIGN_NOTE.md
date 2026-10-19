# task468 design note: the specialty clinical pharmacists, by the spend the members on therapy will run

Status lives in `pipeline.json`; this note holds the design of architecture 2. Read `## Tried and rejected` first.
Architecture 1 (the Larkhaven transit nominations) is spent; its record is in the card's lineage and the lines below.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task468.json` (architecture v2), registered 2026-10-19 after a pull. Guard
  check PASS after redrawing the role family (capacity_planner and the filed-standard artifact repeat task248 and
  task249), the decisive generator (G13, horizon, ahead of G6 and G14, which task268 and older builds hold) and one
  differentiation line against task98 v6. Shape 01 is banned by the last two builds (task268), so the call is an
  allocation (shape 05).
- **Pairing:** Healthcare Delivery & Health Economics / payment-claims-health-plan-analytics / Data Extraction &
  Conformation (ETL). Two pharmacy benefit managers' specialty claim files (the outgoing PBM's January 2019 to December
  2025, the incoming PBM's from January 2026) are conformed into one record of fills by plan member, drug class and
  date, repriced at the incoming PBM's 2026 schedule; the call is the program's staffing, which turns on what that
  record says the members now on therapy will cost over the program year.
- **Shape:** 05, an allocation: the plan's Specialty Clinical Pharmacy Program staffs each of nine specialty classes
  with one clinical pharmacist for each $1.5 million of the class's managed spend for July 2026 to June 2027, or part
  (charter 3.1); managed spend is the 2026-schedule cost of the fills the class's members on therapy on 30 June 2026
  will receive in the program year (charter 2.1, 2.2). Criteria: the nine classes' pharmacists (9), the total (1), the
  nine classes' managed spend (9), the nine classes' 2025 rebates (9), the chart with its parts (3) and the file (1),
  32 in all.
- **Strategy:** composition_mix (the members on therapy are a mix of durations on therapy, and in three classes the mix
  moved sharply after January 2026), decisive generator G13 (the program year is a horizon the record covers only
  through members who have already passed each duration), with G6 and G14.
- **World:** the United States, an unnamed state. Merrow Health Plan, a nonprofit regional plan (about 482,000
  members). Its pharmacy benefit moved from Orrin Rx (to 31 December 2025) to Tallis Pharmacy Services (from 1 January
  2026). The January 2026 formulary bulletin removed step therapy for the weight-management GLP-1s, the severe-asthma
  biologics and the CGRP migraine drugs; a hepatitis C outreach drive ran from May 2025. The Specialty Clinical
  Pharmacy Program (adherence calls, side-effect management, refill coordination) is staffed by its charter for the
  program year from 1 July 2026. Personas from `guard.py names --geo "United States" --seed 468`: Erik Marks (Director
  of Pharmacy), John Henry (the plan's pharmacy data analyst), Caleb Fischer (Tallis's account manager).
- **Forcing fact:** the program year began on 1 July 2026; the staffing is set on the claims through 30 June and goes
  to the executive team at its first August meeting (charter 3.1). The call faces forward: the spend is the twelve
  months from July 2026, none of it observed.
- **Forum and forcing event:** executive_team, budget_or_appropriation; org family other (a nonprofit health plan, an
  insurer); role operations_director.
- **Data-native sentence:** a specialty drug's spend on a member depends on how long the member has been on it
  (loading doses on the first fills, a hepatitis C course that ends after two or three fills, the steep early
  discontinuation of oral oncology, the GLP-1s, the asthma biologics and the CGRP drugs, the near-lifelong persistence
  of HIV, multiple sclerosis and cystic fibrosis therapy), and in June 2026 the step-therapy classes' members on therapy
  are 73 to 90 per cent under six months on therapy against 23 to 45 per cent a year earlier, so carrying last year's
  members' following year forward over-staffs exactly those three classes, while the trailing year and the June
  run-rate mis-state the classes whose spend sits in short courses and early fills.
- **The WHAT screen.** Population: the members on therapy in a class on 30 June 2026, by days' supply (charter 2.1),
  none added after; outcome: the 2026-schedule cost of their fills in the class (2.2); window: dispensed 1 July 2026 to
  30 June 2027 (2.2); unit: dollars, then whole pharmacists at $1.5 million or part (3.1); comparison: none, each class
  staffed on its own spend. The decisive step settles none of them: it is how the caseload's unobserved twelve months
  are estimated from a record in which every past member's months on therapy show what follows each duration (HOW,
  forced by the data's structure: the duration mix moved, and within a duration the next twelve months are stable
  across origins).
- **Sources, one line each:**
  - `stumping/references/client/layer2-rigor-patterns.md`, payment-claims 1 and 4: completion and exposure; here the
    exposure is months on therapy and the projection a development conditional on duration, which no build on file
    carries (task451 completes claims by lag, task458 counts conditions by look-back).
  - `stumping/references/strategies.md` F1 and F5: a clock process already in the data, estimated from every unit that
    went through it, and a pool whose duration mix moved (the step-therapy surge).
  - `dataset-generation/references/layer1-messiness.md`: two PBM layouts, reversals and rebills, re-keyed member
    identifiers, 10- and 11-digit NDCs, contract repricing, mail-order long supplies; none on the decisive step.

## Default path

1. Conform `orrin_rx_specialty_claims_2019_2025.csv` and `tallis_specialty_claims_2026h1.csv`: drop reversed claims,
   link members through `member_id_crosswalk_2026.csv`, convert Orrin's 10-digit NDCs to 11 digits and map each to its
   class through `tallis_specialty_drug_list_2026.csv`, price each fill at `tallis_specialty_price_schedule_2026.xlsx`.
2. Take each class's caseload: the members whose fill's days' supply reaches 30 June 2026 (charter 2.1).
3. Project each class's managed spend for July 2026 to June 2027 the careful way a strong analyst does: this June's
   caseload times the following-year spend per member of the class's caseload on 30 June 2025, observed in full from
   July 2025 to June 2026 at the 2026 schedule.
4. Staff one pharmacist per $1.5 million or part.

Ends on: 52 pharmacists, IMM 13, MS 7, ONC 5, HCV 1, GLP 7, HIV 6, AST 5, CF 4, CGR 4: two too many in the GLP-1
class and one too many in the asthma and CGRP classes (managed spend GLP 9, AST 7, CGR 5 million).
Golden: 48 pharmacists, IMM 13, MS 7, ONC 5, HCV 1, GLP 5, HIV 6, AST 4, CF 4, CGR 3, from each class's development by
months on therapy (the next twelve months' spend of the members on therapy at each month end, by months since first
fill, from every month end whose twelve months the record holds) applied at each caseload member's own duration.

## Stump sentence

The default path projects each class's caseload by last year's caseload's following-year spend per member and files 52
pharmacists with GLP 7, AST 5 and CGR 4, because the January 2026 step-therapy change filled those classes with new
starters who mostly stop within months while last year's caseload was mostly members who had already stayed; the
development by months on therapy at each member's own duration gives GLP 5, AST 4, CGR 3 and 48 in all.

## Three rules

Task type: payment-claims-health-plan-analytics: two PBMs' specialty claim files conformed into one repriced record of fills by plan member, class and date, from which each class's program-year spend for its members now on therapy is projected, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is each specialty class's spend over the program year for the members on therapy today, and the field's estimator is a persistence-and-cost development by months on therapy (loading doses, fixed hepatitis C courses, early discontinuation), applied at each member's own duration; carrying the trailing year, the June run-rate or last year's caseload forward each moves pharmacists between classes.

Swap: "the hospital's wards staffed by the bed-days their current inpatients will use" keeps an arithmetic shape but loses why it moves: there is no loading dose, no fixed two- or three-fill course and no months-on-therapy discontinuation curve in a ward census, and the step-therapy change that filled three classes with new starters has no counterpart.

Layer 1: Orrin Rx's file with reversals as negative lines and rebills under new claim numbers; Tallis's file with a status column, resubmissions and its own member numbers linked through the plan's crosswalk; 11-digit NDCs against Orrin's hyphenated 10-digit; Orrin's paid amounts at its own contract against the Tallis 2026 schedule; 28-, 30-, 84- and 90-day supplies with mail-order packages. Each is the PBMs' systems as they run, asserted neutral for the call.

Layer 2: forecast_uncertainty, a development of spend by months on therapy conditional on the duration each current member has reached, estimated from every member who has passed each month since first fill.

Decisive step: projecting each class's caseload by the class's own next-twelve-months spend at each month since first fill, starting each member at the duration they have reached, instead of last year's caseload, the trailing year, the June run-rate or a curve applied from first fill.

Not semantics: every field read correctly (reversals, crosswalk, NDCs, the schedule, days' supply, the charter's caseload, spend and window) still leaves the easy route projecting this June's caseload by last year's caseload's following year, because no field says how long a member has been on therapy or that three classes' mix of durations moved; the durations have to be built from each member's first fill across both PBMs' files.

Not rule application: the charter fixes the caseload, the window, the prices and the staffing rule; no rule or procedure says how the caseload's next twelve months are projected, and executing every filed rule with last year's caseload files 52 pharmacists, so the step no rule performs is the development by months on therapy.

Analyst test: a strong analyst who conforms both files and reads every charter rule projects this June's caseload by last year's caseload's following-year spend per member and files 52 pharmacists with GLP 7, AST 5 and CGR 4 (the default path's Ends on); the development by months on therapy files 48 with GLP 5, AST 4 and CGR 3.

Estimand: the Specialty Clinical Pharmacy Program charter (2.1 the members on therapy in a class on 30 June 2026 by days' supply; 2.2 the plan's spend on their fills in the class dispensed 1 July 2026 to 30 June 2027 at the Tallis 2026 schedule plus its fee, before cost sharing; 3.1 one pharmacist per $1.5 million or part), in the charter PDF.

No decoy: nothing is planted; the claim files are the PBMs' extracts as delivered, the drug list and schedule are Tallis's, the formulary bulletin is the committee's notice, and no memo, draft or briefing argues a projection method or a staffing.

No certified replay: no published or certified figure reproduces under one projection only; Orrin's trend report (a distractor) states past spend trend and no staffing.

Lesson: a caseload's forward cost is its development at the durations its members have reached, and last year's caseload stands for this year's only when the mix of durations has not moved; the decisive skill is to rebuild each member's duration from the record and develop from there, which no build on file teaches in a claims record.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the trailing year (55) | the charter's "managed spend for the program year" invites the last year's spend: fires | the claim files' spend columns: fires | trailing-twelve-months spend is the budget reflex: fires | none | none | one sum per class: fires | readable |
| R1, the June run-rate times twelve (65) | none | the fill dates: fires | annualising the latest month: fires | none | none | one product: fires | readable |
| R2, last year's caseload's following year per member (52) | charter 2.1 names a caseload on a day, so a past caseload on the same day is the natural analog: fires | none | the cohort analog is the careful analyst's reflex: fires | the record holds last year's caseload's full year: fires | none | one ratio per class: fires | readable |
| R2b, a development from first fill applied to every caseload member (41) | none | none | the textbook persistence curve starts at first fill: fires | none | none | one curve per class: silent | readable |
| G (decisive), the development by months on therapy at each member's own duration (48) | no document names months on therapy, persistence, continuation, a cohort or a development (R1 assertion): silent | no column carries a start, a first fill or a duration; durations are built from each member's earliest fill across both files through the crosswalk: silent | the reflexes are the trailing year, the run-rate and the analog: silent | nothing scores the projections; a back-test is the solver's own: silent | every file reconciles; nothing is anomalous: silent | a cell per class and duration over 78 month ends: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | caseload | members whose fill's days' supply reaches 30 June 2026 | members with any fill in the last 30, 60 or 90 days | another caseload | charter 2.1 "a fill ... has a days' supply that reaches it" |
| SF2 | managed spend's price | units times the 2026 schedule's unit price plus its fee, before cost sharing | Orrin's paid amounts, plan paid net of copay | Orrin's amounts: same call (asserted); net of copay ruled out | charter 2.2 "priced at the Tallis 2026 specialty price schedule ... before member cost sharing" |
| SF3 | the program year | fills dispensed 1 July 2026 to 30 June 2027 | days of supply falling in the year | none ships | charter 2.2 "dispensed from July 1, 2026 to June 30, 2027" |
| SF4 | a drug's class | its class code in Tallis's drug list | Orrin's product descriptions | same call: every NDC is listed (asserted) | charter 1.2 |
| SF5 | pharmacists | one per $1.5 million or part, a ceiling | rounding to the nearest | none ships | charter 3.1 "or part of $1.5 million" |
| SF6 | the duration cap | every month since first fill to 36, then pooled | capped at 12, 24 or 48 | same call (asserted) | the data: nearest bin edge 0.21 of a pharmacist |
| SF7 | the duration grain | single months | three- or six-month bands | same call (asserted) | the data |
| SF8 | a member's start | the first fill in the record, a start before April 2019 pooled with the longest durations | every first fill read as a start; the development chained month to month | same call (asserted) | the data |
| SF9 | managed spend's rounding | the nearest million | under every reading of SF6 to SF8 | same million in every class (asserted, nearest edge 0.07 million) | the data |
| SF10 | rebates on fills dispensed in 2025 (ask) | the statement's 2025 utilization quarters | the 2025 invoice quarters | the ask's figures move | the statement's header: "Utilization quarter is the quarter the fills were dispensed" |
| SF11 | whose spend | the caseload members' fills only | every fill in the class in the program year, new starters included | none ships | charter 2.2 "the plan's spend on its caseload members' fills in the class" |
| SF12 | a member across the PBM change | one member through the crosswalk | every Tallis member a new start | another staffing (asserted) | the crosswalk; the transition notes |

## Ladder

- **R0, the trailing year (55 pharmacists).** Each class's July 2025 to June 2026 spend at the 2026 schedule: IMM 15,
  MS 7, ONC 7, HCV 4, GLP 5, HIV 6, AST 4, CF 4, CGR 3. Dies to the caseload: the year's spend includes members who
  stopped, the hepatitis C outreach's finished courses and the loading fills of the caseload's long-standing members.
- **R1, the June run-rate times twelve (65).** IMM 15, MS 7, ONC 7, HCV 4, GLP 9, HIV 6, AST 7, CF 4, CGR 6. Dies to
  the same fact and to June's new starters' loading doses.
- **R2, the analyst test: last year's caseload's following year per member (52).** IMM 13, MS 7, ONC 5, HCV 1, GLP 7,
  HIV 6, AST 5, CF 4, CGR 4. Dies to the durations: GLP's caseload is 90 per cent under six months on therapy against 45
  a year earlier, AST's 73 against 23, CGR's 82 against 36, and those months carry the steepest discontinuation.
- **R2b, the development from first fill applied to every caseload member (41).** IMM 11, MS 7, ONC 3, HCV 1, GLP 4,
  HIV 6, AST 3, CF 4, CGR 2. Dies to the caseload: its members have already survived to their durations.
- **G, the decisive move (48).** IMM 13, MS 7, ONC 5, HCV 1, GLP 5, HIV 6, AST 4, CF 4, CGR 3; quotas 12.51, 6.50,
  4.43, 0.23, 4.62, 5.52, 3.30, 3.51, 2.46.
- **Separation:** back-tests at 30 June 2023, 2024 and 2025 (the solver's own, nothing ships them) give the development
  a mean absolute error of 13.7, 7.5 and 4.3 per cent across the nine classes against the analog's 14.9, 11.1 and 6.5,
  the trailing year's 181, 301 and 70 and the run-rate's 177, 314 and 183; the analog's errors then were small because
  the mix had not moved, and in June 2026 it moved in three classes.
- **Margins:** every reading in the fork table files the golden with the nearest class 0.21 of a pharmacist from its
  edge; every rung's staffing differs from the golden in at least three classes and in the total.
- **Position, separation and dominance:** R0 and R1 err on the short-course and loading classes (IMM, ONC, HCV, and
  R1 the step-therapy classes too); R2 errs only on the step-therapy classes; R2b errs the other way. Only the
  conditional development moves GLP, AST and CGR down without moving IMM, ONC and HCV up.
- **Worth on the graded quantities:** the call (6), each class's pharmacists (2) and managed spend (1.5): R2 keeps 6 of
  9 pharmacists and 4 of 9 spends (main 18.0 of 37.5), R0 6 and 3, R1 3 and 2, R2b 4 and 3 (generator/ceiling.py for
  R2; the others by checks.py's rung lines).
- **Grid:** the Layer 1 items mishandled one at a time (Orrin's paid amounts) leave the call; the crosswalk ignored
  moves IMM, ONC and AST (SF12, a Layer 1 slip on a lower rung); every reading of SF6 to SF8 files the golden.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | the members on therapy in each class on 30 June 2026 by days' supply (charter 2.1); no member added after (SF11) |
| 2 | Unit of account | the member in a class; spend in dollars, pharmacists whole |
| 3 | Attribution window | fills dispensed 1 July 2026 to 30 June 2027 (charter 2.2, SF3) |
| 4 | As-of dating | the claims through 30 June 2026 (charter 3.1); both files end there |
| 5 | Version basis | one version of every file; reversed claims out (charter 2.2 "A reversed claim is not spend") |
| 6 | Denominator | none: each class's spend is a total |
| 7 | Weighting | each caseload member weighted once at their own duration; the development cells pool every month end |
| 8 | Window length | twelve months |
| 9 | Boundary inclusivity | a fill whose days' supply reaches 30 June counts (2.1: "dispensed on or before that day") |
| 10 | Rounding path | spend unrounded to the staffing, rounded to the million for reporting (SF9) |
| 11 | Tie-break | none: each class is staffed on its own spend |
| 12 | Maturity and censoring | the program year is unobserved; the development uses only month ends whose twelve months the record holds; starts before April 2019 pooled (SF8) |
| 13 | Order of operations | conform, price, caseload, durations, development, projection, ceiling |
| 14 | Row order | no dependence |
| 15 | Duplicate resolution | a reversed claim and its original out, the rebill kept; Tallis R lines out with their claims, resubmissions kept |
| 16 | Identity normalisation | Orrin keys and Tallis numbers to plan member IDs through the crosswalk (SF12) |
| 17 | Netting | spend before cost sharing (SF2) |
| 18 | Dimensional units | 10-digit 5-3-2 NDCs padded to 11; units per package from the drug list and schedule |
| 19 | Code and status semantics | class codes from the drug list (SF4); Orrin REVERSAL and Tallis R lines; never the stump |
| 20 | Integerisation | pharmacists a ceiling at $1.5 million (SF5) |
| 21 | Clause scope | charter 2 and 3 for the call, 4.1 and the prompt for the rebates; the bulletin's step-therapy change applies from January 2026 |
| 22 | Forward window contents | the twelve months from July 2026, none observed; the call faces forward |

## Literal reader

Executed word for word, the charter fixes the caseload (2.1), the spend's basis and window (2.2) and the staffing rule
(3.1), and leaves one thing open: how the caseload's spend over the unobserved program year is estimated. The candidates
are the trailing year (R0), the run-rate (R1), last year's caseload (R2), a development from first fill (R2b) and the
development at each member's own duration (G). The data separates them: a member's next twelve months depend on their
months on therapy, the step-therapy classes' caseloads moved from 23 to 45 per cent under six months to 73 to 90, and
back-tests at the three earlier Junes rank G first each time (mean errors 13.7, 7.5 and 4.3 per cent against R2's
14.9, 11.1 and 6.5). Every reading of G's construction (caps 12 to 48, one-, three- and six-month bands, starts read at
the first fill in the files, the month-to-month chain) files the same 48 and the same spend to the million (checks.py).
Every write-up step names the file and rule it executes.

## Oracles

None. Nothing ships a staffing, a projection or a past caseload's cost; Orrin's trend report (a distractor) gives
2024 to 2025 spend trend by class on Orrin's prices and ranks no staffing; the medical-benefit drug list (a distractor)
is outside the program by charter 1.1. The rebate statement is the ask's file and the projection never reads it.

## Ask sheet

- **Ask A, each class's manufacturer rebates on its fills dispensed in 2025 (nearest thousand dollars): nine figures.**
  H18 home: charter 4.1 reports each class's rebates on the previous year's utilization beside its staffing, so the
  staffing file carries them. Path: `orrin_rx_rebate_statement_2025.xlsx` (invoice quarter, utilization quarter,
  product, class code, channel, units, rebate) and its header line.
  Primary device: D6, an event's quantity on every line it covers. The statement gives each product's quarterly rebate
  (all channels) on each of the product's channel lines, two to four of them, the same amount on each, beside that
  channel's own units; nothing flags the repetition, no line is a total, and every key is unique, so summing the rebate
  column over the 2025 utilization quarters counts each product-quarter's rebate two to four times.
  Mirror: the invoice quarter against the utilization quarter. The statement runs invoices 2025Q1 to 2026Q1, so the
  2025 invoices carry 2024Q4's utilization (at the 2024 contract's lower rate per unit) and leave out 2025Q4's.
  Stops (asserted, checks.py and generator/ceiling.py): every line summed misses 9 of 9; the 2025 invoices, each
  product-quarter once, miss 9 of 9; each product-quarter once over the 2025 utilization quarters gives all 9.
  Realism: rebate statements report at the product and quarter the rebate contract pays on, and channel detail is
  appended for the plan's own reporting; the invoice lag is the manufacturers' quarter in arrears.
- **The construction layer:** the caseloads, the nine managed spends and the chart; the cracker has them.
- **Separation (asserted):** the call reads no rebate; the statement is not read by the projection.
- **Referee:** none.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, each class's rebates on its fills dispensed in 2025 | filters the 2025 utilization quarters by the header's definition and sums the rebate column by class; the product's quarterly rebate repeated on each channel line is counted two to four times | miss |

- Mirror leakage: 0.0 per cent of ask weight (the best mirror, R2, takes the better of the two wrong rebate paths and
  keeps none of the nine: generator/ceiling.py).
- Pair ceiling: 34.8 (planning weights 38 / 7 / 55: the call 6, each class's pharmacists 2, each managed spend 1.5, each
  rebate 55/9; the cracker keeps the main block and instructions, 44.5; the mirror on R2 keeps 6 pharmacists and 4
  spends, 25.0; average 34.8), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- 2026-10-17, at the draw: Urban & Regional Science for a transit seed: none of its task types serves ETL, so the
  pairing cannot be filed.
- 2026-10-17, at the draw: a passenger's average wait from the timetable's gaps (half the mean gap against the
  length-biased mean): generic arithmetic of any periodic service, so the domain reads as a backdrop, and it is not the
  data-integration task type's method (it survives as Ask C's device, which the 10/10 rules leave free).
- 2026-10-17, at the draw: two operators' stops linked across feeds to build combined corridor frequency: the right
  link is read off direction and stop sequence, a field reading, and the guard's identity risk lands on it.
- 2026-10-17, at the draw: delivered frequency from the planned schedule less cancellations cancelled by whole runs:
  needs a dispatch log, and a complete log counts delivered departures exactly, bypassing any estimate.
- 2026-10-17, stage 2: the review as a simple random sample of the unmatched events, its raw route mix the decisive
  step: a single insight the review file signposts (133 v1 died on a development sample pointing at its decisive
  step); the review is now a bus-day sample with one event each, so using it is R2 and weighting it is the move.
- 2026-10-17, stage 2: the composition varying by time band (trunk routes late in the afternoon only, pull-in deadheads
  at night): pooled and band-level shares gave different calls on Route 17, a grain fork (H14); lateness now flat
  through the day and out-of-service movements spread over it, so every stratification agrees.
- 2026-10-17, stage 2: Riverside failing on a four-an-hour timetable: Good Friday's Saturday service pulled its
  timetable average under four too, so the timetable rung landed on the golden; Riverside now runs five an hour and
  its afternoon runs went a quarter short of operators.
- 2026-10-17, stage 2: each candidate's lowest hourly average graded to one decimal: the weighted variants spread up
  to 0.3 on Route 2, so the prompt asks for the verdicts and the workbook carries the figures as supporting detail.
- 2026-10-17, stage 3: on-time shares to one decimal of a per cent: two routes' shares sat within a hundredth of a
  rounding edge, so the shares are graded to the whole per cent (every share further from its edge than one departure
  moves it, asserted); Hillcrest's lateness and timetable jitter moved so its share and its wait sit clear of their edges.
- 2026-10-17, stage 2: a scheduled-departures table from both feeds as an ask: a GTFS-literate cracker executes the
  calendar, calendar_dates and frequencies correctly, so no device held; replaced by the waits (an analytical device).
- 2026-10-17, stage 4: Ask A, Quinnell's April to June record by stop and service-day month: both outside readers
  found the file-head repeats by bus, stop and second and assigned the service days, the judge read the repeats as a
  fork, and no silent device reaches the record without touching the review's frame; dropped (the repeats, the 31
  March copy and the after-midnight service stay as Layer 1 on the call's path, asserted neutral).
- 2026-10-17, stage 4: Ask C, the scheduled wait on 13 May: the prompt's definition made the waiting-time paradox a
  literal integral both readers computed, the frequency window's end read two ways, and no representation of the feed
  hides a departure from a careful reader; dropped (the frequency trips now exact times, each block ending between
  two trips).
- 2026-10-17, stage 4: the on-time device as Quinnell's DeviationSec taken at arrival: both readers timed the
  departures from the timestamps and read the field as noise, and guidance 4.2's "as the AVL system records it"
  invited it; DeviationSec is now the departure against ScheduledDeparture, and the device is Arbor's minute-held
  schedule against the feeds' half minute.
- 2026-10-17, stage 4: Route 6's on-time share at 47.46, 0.04 from its edge (a reader rounding to one decimal first
  filed 48): the half-minute bands, set per transfer point, put every share at least 0.19 from its edge.
- 2026-10-17, stage 4: the eleven candidates named only by route colour in routes.txt (the judge's Gate B and E
  finding): Planning's candidate list now ships with each route's designated stop.
- 2026-10-17, stage 4: the on-time device as Arbor's minute-held schedule against the feeds' half minute: judge pass 2
  read the two schedule sources as an open fork (FIX_NOW), the pin naming the published timetable in guidance 4.1 and
  4.2 closed it, and reader round 3 then timed all eleven shares against the feeds. A device whose basis a filed
  sentence must name dies with the pin, and every other column the ask reads (the departure, the trip tie, the window,
  the days) is the call's own population, so no device on this ask can stay off the call's rows.
- 2026-10-19, repair: the stop-hour grain fork (reader round 3): the review drew 250 bus-days a month, so the
  stop-by-clock-hour cells held one to seven reviewed events and the minimum of thirteen noisy hourly estimates sat
  biased low; at 400 bus-days a month, with the within-bus-day draw on its own stream, every weighted grain (stop, stop
  and hour, band, month, vendor, the within-bus-day weight, counting-day reviews) files the golden and every raw grain
  the R2 slate (checks.py R3b, verify.py's stop-hour estimator).
- 2026-10-19, repair: replacing the dead on-time ask, measures tried on paper and dropped: the average scheduled wait
  (computed exactly from the feeds by any GTFS-literate solver, and "a weekday of current service" splits on the class
  days); missed trips from a dispatch log (it would hand every solver each route's delivered departures, the call's own
  quantity); APC boardings at the designated stops (doors open only in service, which would identify the out-of-service
  passes the review estimates); the fleet roster's asset tags moved between buses (it would move the review's bus-day
  join on the call's path); evening and Saturday counts (Quinnell's repeats and the cutover overlap are seen, not
  silent). The shelter ask takes none of the call's rows.
- 2026-10-19, architecture 1 spent (the transit nominations): four isolated readers landed the call, so the review
  weighted by its design was read off the memo's sampling procedure by every careful solver (Gate F, score_reader exit
  1), and judge pass 3 found the shelter ask NOT_DETERMINISTIC (no file states the moved-stop rule, and stating it
  hands over the device). The author chose to re-root.
- 2026-10-19, architecture 2 spent at stage 4 (the specialty pharmacists by months on therapy): the isolated reader
  projected the caseload by tenure since first fill from past month ends, its first move once it saw the program year
  unobserved, and landed the call (10 of 10) and 27 of 28 ask figures (score_reader exit 1); the bulletin's step-therapy
  sentence and the caseloads' 2026 starters made the duration mix visible, and the rebate statement's repeated
  product-quarter amount was caught on sight. A forward window over a record that shows the process invites the
  conditional development; the next architecture needs a decisive step the record does not display.
