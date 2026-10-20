# task472: Ternmouth Port Authority, where the 2027 replacement quay cranes go

Architecture 2, a re-root drawn on 2026-10-20 in the same objective (Data Extraction & Conformation) and the same
number. Architecture 1 (the berth hours crane breakdowns cost a call, read through the slowest of its parallel crane
runs) was spent at stage 4 the same day, both scored readers landing the call; its record is the last line of
`## Tried and rejected` and the card's lineage.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task472.json` (architecture v2, lineage v1), registered 2026-10-20 after a
  pull. Guard WARN on `overuse.objective` (ETL in 4 of the last 12 builds): the lane is ETL by assignment (task468 to
  task477 are the ETL backlog), so the objective is not a free axis here. The structural NOTE against the slot's own
  architecture 1 (driver similarity 0.16) is differentiated on the card; the nearest other driver is task160 at 0.04,
  and the card is differentiated against task92 (a capped service valued only on the days a candidate receives it).
- **Seed:** ET29 (a port authority funds new ship-to-shore cranes at one of six container terminals on the berth time
  of large cargo vessels). Kept: the world (one authority, six terminals, AIS and the terminals' own records), the
  decision (where the cranes go) and the quantity (berth time of large vessels). The seed's mechanism (AIS stretches cut
  at midnight UTC and at hour-long gaps) is not used: the AIS berth segments ship as a distractor with that mess intact.
- **Pairing:** Supply Chain & Logistics (house domain, ports and terminals; card subdomain `transportation-network`)
  sitting in General Statistics & Data Science, task type `data-integration-record-linkage-entity-resolution`, the only
  ETL task type the house domain maps to. The ETL work is real linkage: two terminal operating systems keyed by visit,
  crane and IMO number (one in Eastern clock time, one in UTC), the pilot station's sailings keyed by vessel name as
  typed and call sign in Eastern time with draughts in feet and inches, the bar's tide predictions in local standard
  time all year, and the vessel register keyed by IMO with former names and call signs, conformed into one
  large-vessel call table; the asks link two maintenance systems, a labour ledger and the OEM's timesheets to the
  crane register. Objective: Data Extraction & Conformation (ETL).
- **The decision and the quantity:** the Crane Replacement Program places the 2027 order's six cranes at the terminal
  where they would have saved the most berth hours on the last closed fiscal year's large-vessel calls, the program
  taking a replacement set to complete a call's cargo work (first container move to last) in four fifths of the time it
  took, and a call's berth hours saved as the hours by which the call, all fast to let go, would then have been
  shorter. Retrospective by design: the board places the 2027 order on 27 October 2026 on the record of fiscal year
  2026, the last closed year, because the program files that year; the window is closed, so nothing in it is forecast.
- **Shape:** `other`, a pick of one of six with each candidate's figure: the six terminals' berth hours saved (6), the
  call, the runner-up and the lead (3), the bar chart with its parts (4), the workbook, the calls table and its grain
  (3), and two asks of six terminal figures each (12): 28 criteria from the structure, none stacked.
- **Strategy:** `binding_constraint`; Gate G `binding_constraint` (a filed operating window, the tide at the river bar,
  removes the natural pick while every reported figure is correct); gap `objective` (the call is scored on berth time,
  which the cargo time saved does not equal where the release is gated), then `time` (the window a ship makes);
  pattern none, generators G7 (operating window, pinned in the Harbour Master's directions, never the prompt), G13,
  G3; Layer 2 family `allocation_constraints`, pattern `own:tide-window departure in a cargo-time counterfactual`.
- **Data-native sentence:** at Ternmouth the two river terminals lie up the Salt River, where a ship leaving with a
  draft of 41 feet or more must pass Salt Point inside a window around high water, so a large ship's stay there ends
  at a tide rather than at its last container move; Saltworks' planners finish cargo for the window, so its ships wait
  hours alongside, while at Millrace the old cranes overrun and ships miss the window they were worked to.
- **Sources, one line each:** seed ET29 (the world and the decision, never its mechanism); the slot's architecture 1
  (the counterfactual stay, solved by readers when the outcome named it, so here the outcome names only a cargo cut and
  the gate lives in a navigation document); task92 (a service valued only on the days it is received, recovered from
  history: here the windows are filed and the quantity is a departure); task87 and task229 (G7 operating windows on
  other ground); strategies F3 (binding constraints held when the limit is shared and died as a per-candidate argmax:
  here the limit is not a cap on a candidate's metric but a gate inside each call's counterfactual, and it moves the
  two river terminals in opposite directions).
- **Same-puzzle test:** gap objective, decisive generator G7, decision pick_one_of_n against the last twelve builds,
  lineage included: no match (task92 and task87 are older and carry pattern C or gap time first). Same-driver test
  (gap, G7, binding_constraint): no match in the last twelve; task92 differentiated on the card.
- **Abstraction test:** nearest drivers stripped of nouns (task160's lagged wave, task167's allotment schedule, task99's
  phased start delay) carry no release window gating a counterfactual saving; none maps onto this driver.

## Default path

Figures from the built pack (`generator/bundle.py`, asserted in `generator/checks.py` L1 to L10).

1. Read the Crane Replacement Program's rules: a large vessel is 10,000 TEU or more in the register, a call belongs to
   the fiscal year of its first container move (Eastern time), cargo work runs from the first container move to the
   last, a replacement set completes a call's cargo work in four fifths of the time it took, and a call's berth hours
   saved are the hours by which it would then have been shorter.
2. Build the harbor calls from tos_vessel_visits_2026.csv and tos_crane_activity_2026.csv (Eastern clock time) and the
   river calls from srt_tos_export_fy2026.xlsx (UTC, converted), join IMO numbers to the vessel register, keep
   10,000 TEU and over with a first move in fiscal 2026: 784 calls.
3. Take each call's cargo work, last move less first, and credit a fifth of it as the hours the new cranes save: the
   stay would have been shorter by the cargo time cut. The pilot station's sailings, the tide predictions and the
   Harbor Master's directions are read, and the river's tidal window noted as how river ships leave.
4. Sum by terminal: Saltworks 990.6, Pine Neck 804.2, Ore Dock 678.2, Halyard 581.7, Millrace 531.3, Gannet Point 427.2.

Ends on: Saltworks, 991 berth hours, 187 ahead of Pine Neck.

Golden: Millrace, 887 berth hours, 331 ahead of Halyard.

## Stump sentence

The default path credits every fiscal 2026 large-vessel call with a fifth of its cargo work and places the cranes at
Saltworks (991 berth hours against Pine Neck's 804), because it never asks whether a ship leaving a river berth could
have sailed any sooner than the tide let it: the berth time a faster finish saves is the change in the sailing the ship
would then have made, next to nothing at Saltworks, whose ships finish ahead of their tide and wait for it, and a whole
tide at Millrace, whose old cranes make ships miss the tide they were worked to.

## Three rules

Task type: data-integration-record-linkage-entity-resolution (General Statistics & Data Science, the task type the house domain maps to): two terminal operating systems, the pilot station's sailings, the bar's tide predictions and the vessel register linked by IMO number, vessel name history and call sign across three clocks into one conformed table of large-vessel calls, a task type serving Data Extraction & Conformation (ETL).

Domain test: the deciding quantity is the berth time a faster crane set would have saved each call, which port berth planning reckons as the change in when the ship could sail: the cargo time cut where nothing else holds the ship, and the change in the tidal or daylight window the ship makes where its departure is gated, so the field's own counterfactual is a sailing re-allocated under the port's access windows from the readiness the faster cranes bring forward.

Swap: "which hospital should get the new MRI scanners, by the bed-days a faster scan would have saved its inpatients" keeps a time cut and a stay but loses the mechanism: no ship that can leave only on a tide, no deep-draught sailing gated at a river bar, no window a faster finish can make or miss, so the counterfactual departure the call turns on does not exist.

Layer 1: the Authority's TOS in Eastern clock time (crane-hour rows, the repeated 2 November hour) and SRT's export in UTC on two sheets; the pilot station's sailings keyed by vessel name as typed and call sign, in Eastern time, with draughts in feet and inches; the tide predictions in local standard time all year; the register's lengths in metres against the directions' feet; former names and a re-flag's new call sign; feeders and calls near the year's ends; each is the systems as they run, nothing is placed to be caught, and each misread leaves Millrace on top (checks.py SF rows).

Layer 2: allocation_constraints, a binding constraint inside a counterfactual: the berth time a faster cargo finish saves is the change in the allocated sailing, re-allocated under the port's access windows from the earlier readiness, not the cargo time cut, and not nothing for every ship that waited for a window.

Decisive step: replaying each gated call's sailing from a readiness brought forward by the cut (its notice less a fifth of its cargo work) to the first time the directions then permit, so a Saltworks ship that would still have waited for the same tide saves nothing and a Millrace ship that would have made the tide it missed saves a whole tide, instead of crediting the cargo time cut, or crediting nothing to every ship that waited.

Not semantics: every field, unit, code and clause read correctly (the deep-draft window at Salt Point with its passage times, the daylight rule for ships of 1,250 feet or more, the hour's notice, local standard time, feet against metres) still leaves the easy route crediting a fifth of each call's cargo work, because none of those readings says that a faster finish moves a sailing only across a window; the step is the counterfactual, not a reading.

Not rule application: the program's rules fix the population, the year, the cargo cut and the outcome, and the directions fix when ships may sail; no rule or procedure says how a call's berth hours saved follow from them, and executing every filed rule with the cut as the saving files Saltworks, so the step no rule performs is recognising that the allocated sailing, not the last container move, binds the end of the stay, and re-running it from the earlier readiness.

Analyst test: a strong analyst who conforms both terminal systems, applies every program rule and reads the directions correctly, but takes the stay as shorter by the cargo time cut, files Saltworks (991 berth hours against Pine Neck's 804, the default path's Ends on); one who sees the tide and credits held river sailings nothing files Pine Neck (804); replaying each sailing from the earlier readiness files Millrace (887, Halyard 556 second); checks.py runs all three on the clean truth (R1, R2).

Estimand: crane_replacement_program_rules.pdf, sections 2 and 3: the population (3.2 a large vessel is 10,000 TEU or more nominal in the register; 3.3 a call belongs to the fiscal year of its first container move, Eastern time, fiscal 2026 being 1 July 2025 to 30 June 2026), the outcome (3.6 the hours by which a call, all fast to let go, would have been shorter had its cargo work taken four fifths of the time it took), the unit (3.7 berth hours, summed unrounded and rounded once per terminal) and the comparison (2, the terminal with the most).

No decoy: nothing is planted: the TOS extracts, the pilot station's sailings, the tide predictions and the register are the systems' own outputs, the directions are the Harbour Master's general directions carrying every section a port's directions carry, and the program's rules state the counterfactual without a method; no memo, draft, briefing, dashboard or stakeholder figure ranks the terminals or argues a saving.

No certified replay: no certified or published saving, berth-hour figure or crane-time figure ships, so nothing is recovered by reproducing a number; the method comes from the port's access rules and its own sailing record.

Lesson: the time a faster process saves a system is the change in when the system's binding constraint releases the job, not the time cut from the process; where release comes only in windows, a job finishing ahead of its window saves nothing and one that just missed a window saves a whole cycle, which no build on file teaches (task92 values a service on the days it is received; this slot's architecture 1 took a job's slowest parallel stream).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0, a fifth of each call's cargo work (Saltworks 991) | rules 3.5, four fifths of the cargo time: fires | first and last move per call: fires | crediting the time cut is the default: fires | none | none | a subtraction and a fifth: fires | readable |
| R1, held river sailings save nothing (Pine Neck 804) | the directions' Salt Point clause names the hold: fires | DRAFT_AFT on each sailing: fires | "the tide sets when they leave" once the clause is read: fires | none | none | one filter: fires | readable |
| R2 (decisive), each held sailing replayed from the earlier readiness to the first permitted time (Millrace 887) | no clause names a saving, a counterfactual sailing, a readiness or a missed tide; the program says only "shorter": silent | no column marks a held sailing, a window made or missed, or a wait; windows come from predictions in another file and another clock: silent | no opponent reflex (reweight, control, shrink, decompose, back-test) re-allocates a departure: silent | no control states a saving or ties any route: silent | every file reconciles and no row is anomalous: silent | per call, a window search over a year of tides and days from a readiness the record does not print: silent | silent |

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | large vessel | nominal capacity in the register, 10,000 TEU or more | capacity at the call; deadweight; length | same call: one register extract, no ship between 9,700 and 10,100 TEU (asserted) | rules 3.2 |
| SF2 | fiscal 2026 call | first container move from 1 July 2025 to 30 June 2026, Eastern time | arrival or sailing in the year; UTC | same call: no large-vessel first move within six hours of either end (asserted) | rules 3.3 |
| SF3 | call | a stay alongside one terminal, all fast to let go | one port visit across terminals | same call: no large vessel shifts between terminals (asserted) | rules 3.1 |
| SF4 | cargo work and its cut | the call's span, first container move to last on any crane, completed in four fifths of its time from the same start | each crane's run cut by a fifth; the start brought forward | Millrace under each (asserted), figures differ | rules 3.4 and 3.5 (the call's cargo work, starting when it started) |
| SF5 | berth hours saved | the call's let-go less the let-go it would then have had | the cargo time cut | Saltworks | rules 3.1 and 3.6 (the call all fast to let go, not its cargo work) and the directions 9.2: a let-go a fifth of the cargo work earlier falls outside the Salt Point window for 234 of 234 deep-draft river sailings (asserted) |
| SF6 | the let-go it would then have had | the first time at least an hour after the earlier notice that the directions permit | the actual let-go (a held ship saves nothing) | Pine Neck | the directions 3.4, 8.1 and 9.2 (windows recur every tide and every day) and the record: every sailing in the extract is the first permitted time an hour or more after its notice (asserted on every sailing) |
| SF7 | readiness | the notice, which follows the last move by the call's own lashing and papers | the last container move | same call (asserted), figures differ | the directions 3.4 (the agent notifies the pilot station when the vessel is ready to sail) and the record (no notice sooner than 24 minutes after its last move) |
| SF8 | the window's place | the berth sailing plus the passage time inside high water less 1 h 30 to plus 0 h 30 | the window applied at the berth | refuted: 118 of Saltworks' 137 held sailings would save less than nothing, and every deep-draft river sailing in the record falls outside such a window (asserted) | the directions 9.2 and 9.3 ("shall pass Salt Point"; the pilot station sets the sailing time on the passage times) |
| SF9 | the tide's clock | predictions in local standard time, an hour added while daylight saving time is in force | read as clock time | same call (asserted), river figures differ | the predictions' header |
| SF10 | deep draft | the deeper of the sailing drafts forward and aft, 41 feet or more | the register's summer draft | same call (asserted) | the directions 1.2 (draft is the deepest, forward or aft) and 9.2 |
| SF11 | 1,250 feet | the register's length overall in metres, 381.0 m or more | rounded lengths | same call: no ship between 368.5 and 398 m (asserted) | the directions 8.1 |
| SF12 | daylight | let-go from 0600 to 2000 Eastern clock time | sunrise to sunset | same call | the directions 8.1 (the hours stated) |
| SF13 | window edges | inclusive | exclusive | same call: no replayed readiness within a minute of an edge (asserted); the record sails ships at the very opening of a window | the directions 8.1 and 9.2 ("between") and the record |
| SF14 | rounding | per terminal, summed unrounded and rounded once | each call rounded to two decimals, then summed | same call, same six figures (asserted) | rules 3.7 |
| SF15 | the lead | the recommended terminal's whole-hour figure less the runner-up's | the unrounded difference rounded | same figure (asserted) | rules 3.7 |

## Ladder

Figures from the built pack (`generator/bundle.py`), every position and margin asserted in `generator/checks.py`.

| Rung | Construction | Winner | Order | Margin | Dies to |
|---|---|---|---|---|---|
| R0 | a fifth of each call's cargo work | Saltworks 990.6 | Pine Neck 804.2, Ore Dock 678.2, Halyard 581.7, Millrace 531.3, Gannet Point 427.2 | 1.232 | the Salt Point window: a let-go a fifth earlier is a time a deep-draft ship may not sail (SF5) |
| R1 | held river sailings save nothing, every other call the cut | Pine Neck 804.2 | Ore Dock 678.2, Halyard 581.7, Gannet Point 427.2, Saltworks 119.7, Millrace 30.9 | 1.186 | the tide recurs: a ship ready before an earlier window sails on it |
| R2 (golden) | each held sailing replayed from the earlier readiness, tide and daylight | Millrace 886.8 | Halyard 555.7, Pine Neck 448.8, Ore Dock 422.8, Gannet Point 395.3, Saltworks 257.0 | 1.596 | none |

- **Position:** Millrace is 5th on R0 (531 against Halyard's 582 and Gannet Point's 427), last on R1, first only on
  R2. Saltworks, R0's winner, is last on R2; Pine Neck, R1's winner, is third on R2.
- **Margins:** every rung at 1.15 or more (R0 1.232, R1 1.186), the final 1.596; the runner-up Halyard 1.238 over Pine
  Neck; the golden runner-up is neither R0's second (Pine Neck) nor R1's second (Ore Dock), so a response off the call
  does not name it.
- **Dominance:** Saltworks' advantage over Millrace on the carried axis (the cut) is 459 hours; Millrace's edge over
  Saltworks on the decisive axis is 630 hours, 1.37 times it.
- **Grid (partial applications, asserted):** every held sailing credited nothing (tide and daylight), Ore Dock 410;
  every ship that waited past its readiness credited nothing, Halyard 499; a fifth of the time alongside, Saltworks
  1,159; the tide replayed without the daylight rule, Millrace with Pine Neck second (804, the runner-up, the lead and
  four harbor figures wrong); the replay from the last move, Millrace 930 with Halyard 617 (every figure wrong);
  standard time read as clock time, Millrace 896 (the river figures wrong); the window at the berth, refuted by the
  record (SF8). Every route without the replay misses the call (L8); no wrong-call route prints any golden terminal
  figure (L10).
- **Worth:** the decisive move takes Millrace from 531 to 887 and Saltworks from 991 to 257, the largest move on the
  ladder; R1 is the smaller, and it reverses nothing for Millrace.
- **Separations financed apart:** R0's lead comes from Saltworks' longer cargo work (its own spans), R2's from
  Millrace's overrun share (71 of its 97 held sailings ready after the window they were worked to had closed) and
  Saltworks' readiness ahead of its window (126 of its 137 held sailings); the harbor's first-light planning at Pine
  Neck and Ore Dock separates the runner-up. Independent parameters, each asserted.
- **No estimator:** the counterfactual is exact arithmetic on the record and the filed windows, so there is no
  standard error and no family of estimators to close; the record's own allocation (every sailing the first permitted
  time an hour or more after its notice, no exception in the record) is what forces the replay (SF6).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | fiscal 2026 large-vessel calls at the six terminals | filed (rules 3.1 to 3.3); closed year, no member unobserved; C1 at the line and the year's ends (SF1, SF2) |
| 2 | Unit of account | the call; the terminal's total | filed (rules 2, 3.1, 3.7) |
| 3 | Attribution window | a call's year by its first container move | filed (rules 3.3); C1, no first move within six hours of either end |
| 4 | As-of dating | the register at its extract (5 October 2026) | filed (rules 3.2); no vessel's capacity changes in the window |
| 5 | Version basis | one extract of each system | C1: no revisions ship |
| 6 | Denominator | none: a total | not applicable, stated |
| 7 | Weighting | none: a sum over calls | not applicable, stated |
| 8 | Window length | one fiscal year | filed (rules 2) |
| 9 | Boundary inclusivity | 10,000 TEU, 41 feet, 1,250 feet, the window edges | C1: nothing within the margins in SF1, SF10, SF11, SF13 (asserted) |
| 10 | Rounding path | summed unrounded, rounded once per terminal | filed (rules 3.7); C1 against per-call rounding (SF14) |
| 11 | Tie-break | none needed | C4: every rung's margin 1.15 or more (asserted) |
| 12 | Maturity and censoring | every call complete inside a closed year | C1: no call open at 30 June 2026 among the population (asserted) |
| 13 | Order of operations | cut the cargo work, then allocate the sailing | the only order the counterfactual has; asserted |
| 14 | Row order | no step depends on file order | C1: no large-vessel first or last move in the repeated 2 November hour (asserted) |
| 15 | Duplicate resolution | one sailing per large-vessel call | C1: no repeated sailing for a population call (asserted) |
| 16 | Identity normalisation | IMO across the TOS and the register; sailings to calls by name history, call sign, berth and time | C4: every population call matches exactly one sailing (asserted) |
| 17 | Netting | none: savings are not negative under the golden | asserted per call |
| 18 | Dimensional units | feet and inches, metres, hours | units in the data and the directions (SF10, SF11) |
| 19 | Code semantics | SRT's call status, the sailings' move code | dictionary semantics; none decides (asserted) |
| 20 | Integerisation | none | not applicable |
| 21 | Clause scope | the Salt Point clause binds deep-draft river passages; the daylight clause harbor berthing and unberthing of 1,250 feet or more | filed scope (directions 8.1, 9.2) |
| 22 | Forward window contents | retrospective call on a closed year | filed (rules 2); the reason in `## Draw` |

## Literal reader

Executed word for word, the rules file the population, the year, the cargo cut and the outcome (the hours by which a
call, all fast to let go, would have been shorter); where they are silent on when a ship would then have let go, the
options are the actual let-go less the cut, the actual let-go, and the first permitted time an hour after the earlier
notice; the first puts deep-draught river let-gos at times directions 9.2 forbids (asserted), the second holds a ship
that would have been ready before an earlier window to a later one (directions 3.4, 9.2 and the record, where every
sailing is the first permitted time after its notice), and only the third violates no shipped sentence: it is the
golden. The easy answer comes from the easy method on the same literal estimand, never from another reading.

## Oracles

- The sailings' own regularity (every sailing the first permitted time an hour or more after its notice): it confirms
  how sailings are allocated, states no saving, ranks nothing, and holds under every reading of the rules.
- The TOS visit lists and SRT's call list: they confirm the population under every reading.
- No file publishes a saving, a berth-hour total, a crane-time total or a ranking of the terminals: none ties a route.

## Ask sheet

- **Ask A, the hours ship-to-shore cranes stood out of service for breakdowns at each terminal over fiscal 2026 (six
  figures, whole hours).** H18 home: the condition of the cranes the order replaces, which the program's board paper
  sets beside the berth hours saved. Path: cmms_sts_work_orders_fy2026.csv (WONUM, ASSETNUM, WORKTYPE, STATUS),
  cmms_asset_status_history_fy2026.csv (ASSETNUM, ISRUNNING, CHANGEDATE, WONUM), srt_maintenance_jobs_2025-26.xlsx
  (EQUIP_TAG, JOB_CLASS, DOWN_UTC, UP_UTC), sts_crane_register.csv (CRANE_ID, ASSETNUM, SRT_TAG, TERMINAL),
  tos_crane_activity_2026.csv and SRT's QC Hours sheet (crane, terminal, hour), the data dictionary: seven files,
  sixteen columns.
  Primary device: D2, a label stored before a silent switch. Three cranes travelled along the common rail to the
  neighbouring terminal during the year (one from Ore Dock to Pine Neck in November 2025, one from Halyard to Gannet
  Point in February 2026, one from Saltworks to Millrace in April 2026); the register gives each crane's terminal at
  the extract and no history, the cranes keep their numbers, and no document mentions a move, which shows only in the
  terminal whose calls each crane works before and after it. Placing every stop at the register's terminal moves all
  six figures.
  Hazards: February 2026's parallel run (river crane breakdowns in the CMMS from 1 February while SRT kept logging
  them to 28 February); reopened orders (two stops on one order); orders re-typed DMG by the pull (damage by a ship or
  a vehicle, which the CMMS dictionary keeps apart from breakdowns); the report and finish times against the status
  history's out-of-service periods; the year cut in Eastern time against SRT's UTC.
  Stops (asserted, checks.py and generator/ceiling.py): the register's terminal, the cracker's handling, misses all six;
  February's copies counted twice misses Saltworks and Millrace; the orders' report and finish times miss all six;
  DMG kept as breakdowns misses the terminals that had one; the golden gives all six.
- **Ask B, the maintenance labour hours spent on ship-to-shore cranes at each terminal over fiscal 2026, the
  Authority's own staff and contractors alike (six figures, whole hours).** H18 home: the maintenance burden of the
  cranes the order replaces, the board paper's second condition figure. Path: cmms_labor_transactions_fy2026.csv
  (WONUM, LABORCODE, TRANSDATE, REGULARHRS), cmms_sts_work_orders_fy2026.csv (WONUM, ASSETNUM),
  crane_maker_service_timesheets_fy2026.xlsx (work order, engineer, date, hours), srt_maintenance_jobs_2025-26.xlsx
  (EQUIP_TAG, LABOUR_HRS, DOWN_UTC), sts_crane_register.csv, the TOS crane activity (where each crane stood), the data
  dictionary: seven files, fifteen columns.
  Primary device: D1, the same hours in two sources. The crane makers' field-service engineers sign a timesheet for
  every visit, which the makers send monthly; where an engineer worked beside the Authority's crew the planners also
  keyed the engineer's hours into the labour ledger under the contractor code, and elsewhere they did not; nothing
  marks which. Adding the timesheets to the ledger counts the keyed hours twice; the ledger alone misses the hours never
  keyed; the records show which (a keyed entry carries the timesheet's order, day and hours).
  Hazards: the relocations (shared with ask A), February's parallel run (the river jobs' labour in both systems), the
  yard equipment's orders and labour in the same CMMS, the year cut.
  Stops: the ledger and SRT alone misses all six; the ledger plus every timesheet, the cracker's handling, misses
  all six; the register's terminal misses all six; the golden gives all six.
- **The construction layer:** the call, the six terminal figures, the runner-up, the lead and the chart; the cracker
  has them.
- **Main population zero-counts (asserted):** the call reads no maintenance, labour or timesheet file; with each of them
  emptied the six figures and the call are unchanged (checks.py S1).
- **Hazard table (asserted):** the relocations move all twelve ask figures; the parallel run moves Saltworks and
  Millrace in both asks; the yard equipment moves ask B's four harbour terminals; none moves the call.
- **Referee:** none; no file states a breakdown or labour total.

| Ask | Cracker (lands the call, runs the battery, executes every filed rule it points at) | Verdict |
|---|---|---|
| A, breakdown hours by terminal | places each stop at the crane's terminal in the register, counts February's river copies once, keeps BD at the pull, two stops on a reopened order, the status history's periods | miss |
| B, maintenance labour hours by terminal | adds the makers' timesheets to the labour ledger and SRT's hours, leaves yard equipment out, places each order at the register's terminal | miss |

- Mirror leakage: 0.0 per cent of ask weight (every rung builds both asks the cracker's way and misses all twelve:
  generator/ceiling.py).
- Pair ceiling: 28.5 (weights 38 / 7 / 55: the cracker keeps the main block and instructions, 45.0; the best mirror off
  the call keeps the chart and file criteria, about 12.0; average 28.5), rerun from the generated rubric at ship.
- Measured by: generator/ceiling.py on the cut pack.

## Tried and rejected

- AIS dwell itself as the decisive quantity (2026-10-20, screened before the draw): once the midnight cuts, reception
  gaps and the shared MMSI are resolved, a call's berth time is fixed by its first and last pings, and the AIS
  endpoint problem under sparse reception is bracketed by the dense moving-state pings; Layer 1 only.
- A queue counterfactual for vessels that left the anchorage (2026-10-20, screened): the would-be wait is fixed only by
  a filed berthing order, which makes the decisive step the execution of that order.
- Night-flow leakage scaled through a pressure exponent (2026-10-20, screened): a water world, and a rate re-read at
  the decision's conditions through a profile sits close to task459's and task460's drivers.
- The GS&DS record-linkage subdomain under its own domain (2026-10-20): `ban.subdomain` against task473, filed the same
  morning; the build sits in the house domain instead, which maps to the same task type.
- Architecture 1, the slowest-crane counterfactual over a call's parallel crane runs (2026-10-20, spent at stage 4):
  both scored readers landed the call (score_reader exit 1 on each: Pine Neck 263 against Halyard 184, every
  terminal exact), each reading rule 2.4's "taken together, lengthened its stay alongside" as the instruction to
  take the latest crane finish with and without its stops, and the whole-hour terminal totals confirmed the
  construction to both; reader 1 also cracked ask A (the berth zone's gaps bridged, anchorage shifts kept apart)
  and reader 2 ask B (status history joined to the BD type, the parallel run's copies counted once). A quantity
  the filed outcome names outright is computed by asking the question; the next decisive step must be one a
  careful analyst who asks the right question still estimates wrongly, and no graded figure is tuned to a bin
  centre.
