# task402 design note

Architecture 1, drawn 2026-11-03 (wave 7, Root-Cause lane), numbered from seed RC08 (which of five faults on an
underperforming wind turbine gets the one spring crew visit, and the winter energy it cost). The seed's world could not
carry an honest draw (`## Tried and rejected`, first line), so the build moved to another client domain, world and
dataset under the same objective and number (CLAUDE.md, a stuck build is unblocked). Kept from the seed: the decision
kind (one of five candidate causes gets the single fix) and the quantity's kind (what that cause cost over the period,
in the period's natural unit). The kernel is new.

A mental health charity delivers the county's NHS Talking Therapies service under contract to the integrated care
board: step 2 (psychological wellbeing practitioners: guided self-help, digital therapy, groups) and step 3
(high-intensity therapists: cognitive behavioural therapy and counselling for depression). Recoveries, counted on the
national measure, fell between 2024-25 and 2025-26 as a winter rise in referrals formed a step 3 backlog. Five things changed in 2025-26 and the board's improvement review
lists them, each with the fix it would buy: A, agency high-intensity cover brought in from May 2025 on 12-week
assignments renewed quarter by quarter to clear the step 3 waiting list (fix: fixed-term posts); B, telephone-first
step 2 from April 2025 (fix: video and face-to-face as standard); C, the step 3 waiting list itself (fix: an extra
block of step 3 sessions); D, the digital therapy platform changed in July 2025 (fix: return to the old platform); E,
the stress management groups withdrawn from September 2025 (fix: reinstate them). The board's 2026-27 improvement fund
is committed at the year-end contract review to the one change that cost the service the most recoveries in 2025-26.

What nothing in the pack says: an agency therapist whose assignment lapses at the end of a 12-week block leaves mid-course, the
patients are reallocated without a joint session, and many stop attending; agency cover was given the longest waiters,
so the early endings it causes read as the waiting list's.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task402.json`, architecture 1. `guard.py check` on the draft with
  task401's card in the tree (merged from the parent's branch): WARN only (overuse.objective, the lane's own objective;
  repeat.gate_g and overuse.gate_g, decomposition_attribution being the honest Gate G for a correctly counted fall
  assigned to the right change; repeat.question_form, a pick asks which). NOTE test.same_puzzle_older against task270
  v6 (lineage) and test.same_driver_older against task245, differentiated on the card. Nearest driver 0.08 (task130 v2
  loop 1, lineage).
- **Pairing:** Psychology & Behavioral Science (client domain) / `mediation-moderation-process-modeling` /
  Root-Cause Analysis. The task type serves Root-Cause only; no card on file sits on it, and the pairing
  psychology-behavioral-science x root-cause is never built (`coverage`). Probed with `check` before briefing it as
  available: no `three_rules.task_type` refusal.
- **Objective and call:** which one of the review's five changes gets the 2026-27 improvement fund, decided by the
  recoveries each cost in 2025-26 (the board's plan files the WHAT). The fund runs in 2026-27, so the call faces
  forward; it is judged on the closed 2025-26 record because the plan says so. Root-Cause, not Forecasting: nothing is
  projected.
- **Shape:** 09, the funnel of stages: the referral-to-recovery funnel by step and year (each stage's volume and rate)
  carries the asks; the call and its cost carry the main recommendation.
- **Strategy and Gate G:** `population_selection` (the decisive move fixes which courses carry the change, the ones an
  agency block's lapse broke off, an exposure no column marks, and that exposure is what splits the wait's total
  effect into its mediated and direct paths); Gate G `decomposition_attribution` (a correctly counted fall assigned to
  the right change). Gap population then objective; pattern none; generators G9 (the service measures each therapist's
  recovery rate on the courses the therapist kept to discharge, and the courses an agency therapist lost when the
  block lapsed sit behind the care-contact to booking-log join), G4 (who holds the course after the reallocation), G6
  (agency cover took the backlog, so the wait and the cover move together). G4 and G6 were each tried as the decisive
  generator at stage 2 and refused by `check` (test.same_driver against task232 v2, task121 v6, task129 v2 and
  task243; test.same_puzzle_older against task144, task228, task265 and task68), so they stay as frame. Gate G's
  repeat and overuse WARNs (decomposition_attribution on four of the wave's five builds) are answered by the
  strategies differing: composition_mix (task401), causal_design (task400), binding_constraint (task399),
  population_selection here; the vocabulary gives a root-cause call no other honest key.
- **Furniture:** forum `customer_or_counterparty` (the integrated care board as commissioner), forcing event
  `period_close` (the 2025-26 year-end review on the refreshed extract), org family `nonprofit_or_charity` (the charity
  provider), role `field_unit_lead` (the service's head of psychological therapies), context artifact `register` (the
  agency booking log), calibration none. The last three live cards (task399 architecture 4, task400, task401) hold
  minister_or_cabinet, committee_or_panel and executive_team; budget_or_appropriation, incident_or_complaint and
  purchase_order_or_contract; government_agency, other and hospital_or_health_provider. The first draft carried
  purchase_order_or_contract and hospital_or_health_provider, both held by task401; redrawn because the year-end close
  on the refreshed extract is what forces the review now, and NHS Talking Therapies services are commonly run under
  contract by charities, which is the honester organisation here and moves the world off task401's NHS trust.
- **People** (`guard.py names --geo "England" --seed 402`): Wendy Gibson (head of psychological therapies, the asker,
  on the card only), Jemma Fletcher (the board's mental health commissioning manager, owner of the improvement plan),
  Josh Parry (people and resourcing lead, keeper of the agency booking log), Hollie Smith (performance and
  information analyst, the monthly report; drawn from the same list in place of Lesley Thompson, whose surname
  warned against task155). None is in the prompt.
- **Data-native sentence:** the care record stores the practitioner of each appointment and the agency booking log
  stores when each locum's assignment ended, under different identifiers on different clocks, so whether a course was
  broken off by an assignment end exists only as a relation between a practitioner's last appointment with a patient
  and that practitioner's assignment end; and the national measure counts a recovery only on a course that reaches a
  second treatment appointment, so the patients a broken course loses before then never enter it.
- **The abstraction sentence:** "a fixed-term staffing arrangement ends practitioners' assignments in the middle of
  the cases they hold; the cases handed on are abandoned, and because the arrangement was used on the longest-waiting
  cases the loss reads as the waiting list's while every practitioner's own outcome rate looks sound." Written against
  every approved and delivered Root-Cause driver and the spent list the coordinator gave: none is an assignment's end
  breaking the cases it held.
- **Semantic screen** (`guard.py mechanisms --objective root-cause`, one line per nearest build's spent insight):
  task121 rebuilds rest or fatigue from a worker's consecutive records (and its lineage compares a unit's hours with
  the same unit's hours on other days); task129 rates tree outages per exposure, read at each unit's time since trim
  and surroundings; task202 places each inflow's phosphorus at the depth its density sends it; task398 re-runs a rule
  keyed to the whole's own path; task399 architecture 3 rebuilds a capacity stock to find unmet demand, and task399
  reads the duty lawyer's presence at each call against a second list; task400 reads a staggered rollout's natural
  comparison; task187 reads a unit's shortfall against a reference curve at matched conditions; task401 standardises a
  pilot year to a mix that care home closures changed. The decisive step here rebuilds no state from a worker's own
  rest, places no exposure in surroundings or layers, re-runs no rule, rebuilds no stock, uses no rollout, reads no
  reference curve and restandardises no mix: it reads each patient's course against the end of the assignment of the
  practitioner who held it, and splits the wait's apparent harm into the path through those broken courses and the
  wait's direct path. The nearest device on file is task399's (an actor's roster read against each case), and a
  reviewer holding the two will hear the rhyme, so the card carries the line on the insight: task399 reads an
  advocate's absence at the moment each case is decided, which confounds another decision-maker's measured
  disparity; here a therapist's departure breaks a course already under way, the patient is lost after the
  handover, and the loss is a mediated path of the wait counted over every course begun, not an absence at a
  decision. The shell is drawn away from task399 and task400 (`## Ask sheet`, prompt) and `heart`'s shell lines are
  read at stage 3, not only its verdict.
- **Library test:** the golden is not a named correction. The field's measures (the national recovery rate, the
  funnel by step, recovery by modality, waits and clinician) sit at rungs 0 to 3.
- **Sources:** every file synthetic, generated by `generator/` from seed 402, invented world, no real organisation,
  service or person; licence CC BY 4.0, recorded in `metadata.json`. Planned pack (stage 3 fixes the list): referrals,
  care contacts (the spine, about 130,000 rows), outcome measures (item-level before the record migration, totals
  after), the practitioner directory across the migration, the agency booking log, the board's improvement plan with
  the measure definitions, the monthly KPI report (preliminary), the waiting list snapshots, the digital platform's
  usage report, the group programme schedule, and two distractors named in `metadata.json`.

- **Stage 3 record (2026-11-03).** Shell redrawn after `heart`'s shell lines matched task400's role sequence (a "which"
  question, a docx paper carrying the call and a monthly chart, an xlsx of workings): question form now "what" (heart reads
  how-many), second-sentence opener "Our commissioner", the case a contract-review deck (pptx) setting this year's
  recoveries against last year's; heart exit 0, WARN only (overuse.objective; repeat.gate_g and repeat.decision against
  task400, answered at the draw; repeat.deliverables pptx+xlsx against task398, four builds back). `guard.py surface`
  promotes one pair for adjudication, task245 at surface 0.077 (40th percentile), on the card's structural triple, the
  same-driver signature differentiated on the card at the draw; no shared names, files or surface tells.
- **leak.py REVIEW rulings.** The plan carries the call's words because it lists all five changes alike (no ranking):
  harmless. The plan and the provisional report carry 7 and 6 of the stump paragraph's terms (course, recovery,
  assignment, therapist, clinician, monthly, report), the service's ordinary vocabulary; neither names a handover, a
  lapse or a course's run of therapists: harmless. The vendor export's "generated_utc" key read as a generator's word:
  renamed "exported_utc".

## Default path

1. Read the board's improvement plan: the fund goes to the change that cost the service the most recoveries in
   2025-26, a recovery counted on the national measure (a course ended in the year after at least two treatment
   appointments, at caseness at the first treatment appointment and below caseness on PHQ-9 and GAD-7 at the last).
2. Walk the referral-to-recovery funnel by step and year: recoveries fell by a few hundred; step 2's recovery rate is
   a little lower; step 3 lost the most, because more step 3 courses ended early.
3. Price each change with the field's measures: B from step 2 recovery by modality (telephone against video and
   face-to-face) times the courses on the telephone (-17.6 at seed 402); D from digital courses against 2024-25's
   (58.8); E from the group places withdrawn (4.9); A from recovery by practitioner, attributed as the
   national data attributes a course, to the practitioner who discharged it (agency 48.6 against employed 46.5 per
   cent, so A costs nothing); C from step 3 courses by wait band, the long waiters' recovery shortfall against the
   short waiters' (263.8) plus the waiting list's extra leavers against 2024-25 (56.1).
4. C prices highest: fund the extra block of step 3 sessions.

Ends on: C, the step 3 waiting list (about 320 recoveries on the default path's pricing at seed 402).

Golden: A, the agency cover's lapsing assignments (257.3 recoveries at seed 402, graded 250 to the nearest 50): the
wait's total association with lost recovery splits into the path through the 733 step 3 courses an agency block's
lapse broke off (114 recovered against 371.3 expected, most of the patients stopping after the reallocation) and the
wait's direct path, small; C's own cost is the waiting list's extra leavers plus that direct path, 70.9.

## Stump sentence

A competent solver walks the year's fall in recoveries down the referral-to-recovery funnel, finds it in step 3
courses that end early, reads those early endings as the waiting list's because they climb with the wait, finds agency
therapists' recovery rates on the courses they discharged level with employed therapists', and files C, the step 3
waiting list (Ends on: C); the step that lands it there is never splitting the wait's effect by setting each step 3
course's run of therapists, rebuilt across the record migration, against the agency booking log's assignment ends,
which shows the loss runs through the courses a lapsing agency block broke off (agency cover took the backlog) while
the wait's direct path is about nil, so the change that cost the most recoveries is A.

## Three rules

- **Task type:** `mediation-moderation-process-modeling` (Psychology & Behavioral Science): how a change reaches an
  outcome through the process that produces it; it serves Root-Cause in the taxonomy.
- **Domain test:** the quantity that decides is a mediation decomposition, the task type's own analysis: the wait's
  total association with lost recovery split into the indirect path through allocation to agency cover whose
  assignment lapsed mid-course (reallocation, then disengagement, the therapist-discontinuity dropout that
  psychotherapy process research reports after an unplanned change of therapist) and the wait's direct path; the
  field's reflex measures are the national recovery rate by step, modality, wait band and clinician, which read the
  total effect and call it the wait's.
- **Swap:** "the wait's harm runs through the courses a lapsing agency block broke off, and its direct path is nil"
  with a gym's nouns ("long-waiting members given to trainers whose contracts lapsed stopped coming") keeps the
  arithmetic of a split but loses the mediator the decomposition is about: there is no course of treatment scored
  session by session against caseness, no therapeutic alliance for a handover to rupture and no recovery for the
  indirect path to remove, so the decision quantity (recoveries lost through each path) does not exist.
- **Layer 1:** an electronic record migration in October 2025 re-keyed practitioner identifiers, joined back only
  through a directory whose names differ from the booking log's; the booking log writes an extended assignment as a new
  row, not an end; outcome measures are item-level before the migration and totals after it; the monthly KPI report
  carries provisional figures the refreshed extract revises; appointments run on local time and the booking log on
  UTC; the agency portal records weekly totals; the waiting list module snapshots after the month end; the digital
  vendor exports section events in UTC; the fiscal year runs April to March against calendar-month extracts.
  Nothing is placed to be caught.
- **Layer 2:** estimand and identification: a mediation decomposition whose mediator has no column (the courses an
  agency block's lapse broke off, not the courses an agency therapist discharged), against a wait gradient that the
  allocation of agency cover to the backlog produces.
- **Decisive step:** splitting the wait's effect by its mediator: setting each step 3 course's run of therapists
  against the assignment ends of the therapist who held it, pricing what the broken courses lost from the
  reallocation on against courses that had come as far without one, and reading the wait's direct path among courses
  whose therapist stayed, rather than reading the early endings by wait band or the outcomes by the therapist who
  discharged.
- **Not semantics:** every code, clock, identifier and definition read right (the migration's identifiers, the
  booking log's extensions, the measure's caseness and finished-course rules) still leaves the easy route on C: no
  field says a course was broken off, and the wait gradient and the clinician rates are read correctly.
- **Not rule application:** no filed rule says to trace a course's therapists, to link them to the booking log or to
  count from the handover; the plan files only the measure, the year and "the change that cost the most recoveries".
  The enumerated family files C (early endings by wait), B (recovery by modality), A at zero (recovery by clinician),
  A diluted or C (completion by allocated practitioner, the cover and the wait moving together), and A (the broken
  courses); the standing family once the records and the plan's comparison clause are read is the broken-course
  reading, eight constructions spreading 246.0 to 262.6 (all 250 at the graded nearest 50); the enumerated family
  spreads 0 (A by the discharging clinician) to 320.0 (C by wait band with leavers); what rules the others out is
  quiet, a relation no document invites.
- **Analyst test:** a strong analyst who reads every field and rule correctly walks the funnel, finds step 3's early
  endings climbing with the wait and agency therapists' recovery rates level with employed ones, and files C (Ends on:
  C); one who also prices completion by the allocated practitioner finds the cover and the wait moving together and
  cannot separate them; only the broken-course reading separates the cover's lapsing assignments from the wait.
- **Estimand:** the board's improvement plan (stage 3 fixes the file): recoveries on the national measure, counted on
  courses ending 1 April 2025 to 31 March 2026 on the refreshed extract; a change's cost is the recoveries the year's
  courses would have had without it, less those they had; the fund goes to the change that cost the most.
- **No decoy:** nothing is planted: the monthly report is correct for what it measures, the clinician outcomes are
  true, no memo, draft or stakeholder figure argues a change, and no block of records is copied.
- **No certified replay:** no certified or published figure encodes the method; the golden reproduces no shipped
  figure.
- **Lesson:** a staffing arrangement can cost outcomes through the cases it breaks off rather than through the
  quality of the people it supplies, and a recovery rate on finished courses never sees the patients a broken course
  loses; no build on file reads a case's run of practitioners against their assignment ends.

## Survivor anatomy

- **Actor:** whether a course was broken off by an assignment end has no column: appointments carry a practitioner and
  a date, the booking log carries assignment start and end dates, and the property is a relation between a
  practitioner's last appointment with a patient, the next practitioner in the course and the first practitioner's
  assignment end.
- **Link:** care contact practitioner identifiers, re-keyed at the October 2025 migration, joined through the
  directory by name to the booking log's worker records (no shared key, names in two styles), the assignment's last
  extended end date against the course's last appointment with that therapist; no key is shared by the care record and
  the booking log.
- **Reflex:** the field's measures (the national recovery rate, the funnel by step, recovery by modality, early
  endings by wait, outcomes by clinician) sit at rungs 0 to 3 and file C.
- **Back-test:** the textbook route validates: early endings climb monotonically with the wait, as the field's
  literature expects, and agency therapists' recovery rates on the courses they finished match employed therapists'.
- **Second use:** the care contacts carry every funnel stage the asks read; the booking log carries the agency hours
  and spend the board's workforce return needs; the directory is the record migration's own mapping; delete the
  decisive step and every file stays.
- **Shock:** the loss the step recovers sits in no shipped statistic; step 3's fall reads as the waiting list's
  ordinary early leavers, and the golden tops no sort (the wait tops the early endings, the telephone tops the courses
  changed).
- **Pins:** the plan files the WHAT in the board's own genre (the measure, the year, the cost definition, the fund
  rule); no sentence names a course's therapists, a handover, the booking log or continuity, and deleting any filed
  sentence leaves the call forced by the records.

## Readability screen

Seven tests per rung (1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 dedicated
organ); a rung any test fires on is readable.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| C by wait band (rung 1) | no | wait from two dates | yes, the field's wait story | no | no | yes, one group-by | no | readable |
| A by the discharging practitioner (rung 0) | no | practitioner on the last contact | yes, the clinician KPI | no | no | yes | no | readable |
| B, D, E by modality and year (rung 0) | no | modality column | yes | no | no | yes | no | readable |
| A by the first practitioner (rung 2) | no | first contact's practitioner, directory | partly | no | no | yes | no | readable |
| cross-tab wait band by first kind (rung 2) | no | two columns | yes, stratification | no | no | yes | no | readable |
| monthly chart: starts, early endings, practitioners in post by kind (rung 2) | no | dates and staff group | yes, the run chart | no | no | yes | no | readable |
| the broken courses, priced from the reallocation (decisive) | no | no column marks a course broken; practitioner identifiers re-keyed at the migration, booking log on other identifiers and UTC | no, the field prices the wait and the clinician, never a course's run of therapists against assignment ends | no control isolates it | no, the battery chains extensions and maps identifiers but does not split a wait effect by its mediator | no, a landmark comparison per course | no, the booking log is the people team's own record and carries ask 2's rates | silent |

## Semantic fork table

Main-call terms and conventions. The closures marked "to file" are written into the improvement plan at stage 3
and asserted in `generator/checks.py` under these ids.

| Id | Term or convention | Golden reading | Alternatives | Ruled out by |
|---|---|---|---|---|
| SF1 | recovery | the national measure: course ended in the year, two or more attended treatment appointments, at caseness at the first, below on PHQ-9 and GAD-7 at the last | scores at assessment as the first; any two contacts | to file: the plan's measure annex in the national wording |
| SF2 | the year | referrals whose course ended 1 April 2025 to 31 March 2026, local dates | received in the year; calendar 2025 | to file: the plan's period clause |
| SF3 | a change's cost | the recoveries the year's referrals would have had without that change, less those they had | the fall from 2024-25; the KPI shortfall | to file: the plan's cost clause |
| SF4 | the comparison for a referral a change reached | the year's other referrals at the same step; inside it landmark, banded, pooled, employed-only and coarse members all 250 | a subgroup pool (unbroken agency, unbroken long waiters); 2024-25's courses | filed: plan 3.3 "read from the year's other referrals at the same step"; graded to the nearest 50, every member mid-bin, asserted |
| SF5 | an agency assignment | a booking and its extensions, first start to last end | each booking line's end as an end | to file: the booking log's own header line |
| SF6 | a practitioner across the migration | one person under an old and a new identifier, joined through the directory | each identifier a different practitioner | the directory's own mapping columns; asserted that every course spanning 13 October 2025 keeps its therapist under the map |
| SF7 | the step of a referral | step 3 when any treatment appointment is with a high-intensity therapist | step at assessment | to file: the plan's step clause; asserted inert for the call |
| SF8 | which change gets the fund | the change with the largest cost | largest cost per patient reached | to file: the plan's fund rule |

## Closure table

| # | Axis | Reading here | Closure |
|---|---|---|---|
| 1 | Population | referrals whose course ended in 2025-26, every one that began (not only finished courses) | SF2, SF3 filed |
| 2 | Unit of account | the referral; a recovery is one referral | SF1 filed |
| 3 | Attribution window | the course's end date | SF2; C1: every broken course's counterfactual end is inside 2025-26 (latest 24 December 2025), asserted |
| 4 | As-of dating | the refreshed extract of 6 May 2026 | filed as-of; the preliminary report is a different release |
| 5 | Version basis | refreshed extract over the preliminary monthly report | the plan names the refreshed extract |
| 6 | Denominator | the recovery measure's finished courses at caseness for rates; costs are counts | SF1, SF3 |
| 7 | Weighting | none; counts | n/a |
| 8 | Window length | one fiscal year | SF2 |
| 9 | Boundary inclusivity | 1 April to 31 March inclusive, local dates | C1: no broken course ends within a day of either boundary, asserted |
| 10 | Rounding path | whole recoveries, rounded once at the end | to file in the prompt's rounding sentence |
| 11 | Tie-break | not needed: A clears every rival's widest read by 2.87 times under every estimator | asserted margin |
| 12 | Maturity and censoring | courses open at 31 March are outside the year; broken courses' counterfactuals end inside it | C1 by construction, asserted |
| 13 | Order of operations | identify broken courses, then price from the reallocation | one order |
| 14 | Row order | none | C1 over permutations, asserted |
| 15 | Duplicate resolution | contacts deduplicated on contact identifier | C1: duplicates carry identical rows |
| 16 | Identity normalisation | practitioners across the migration via the directory; booking-log workers via the directory's names | SF6; C4 asserted (unmapped joins misplace every spanning course) |
| 17 | Netting against gross | none | n/a |
| 18 | Dimensional units | recoveries are counts | n/a |
| 19 | Code and status semantics | attended, did not attend, cancelled; treatment against assessment contacts | the export's own code list; never the stump |
| 20 | Integerisation | whole recoveries | rounding once |
| 21 | Clause scope | the cost clause applies to every change alike | SF3 |
| 22 | Forward window contents | none: the fund is decided on the closed year | n/a |

## Literal reader

Executing the prompt and the plan's clauses word for word (SF1 to SF4, SF7, SF8, the register's SF5 header) gives one
reading of every term; the comparison is filed (SF4) and the method inside it stays open, every member grading to 250;
the call (A) is the same under every member of the enumerated family once the broken courses are read.

## Oracles

None that rank the candidates. The provisional KPI report prints the recovery rate by month and by the staff group of
the discharging clinician (step 3 substantive against agency) and agrees with the wrong path on every figure it prints;
the timesheets, the snapshots and the vendor export feed the asks only. No shipped figure ties only under the golden.

## Ask sheet

The asks sit on quantities the call never computes, each a component of the review's case for another line on the list
(H18), each from ask-only files, each figure moved by a device for the careful solver. Blocks no device reaches were cut at
stage 2 (the digital beginners, the over-18-week counts, the agency cover's November and December). The main call's files
(referrals, both appointment exports, the item scores, the user list, the booking register's lines) carry no device row:
the ask builders write only the timesheets, the snapshots and the vendor export, and the bundle's main-call figures equal
the clean truth (asserted).

- **Ask 1, the step 3 waiting list at each month end of 2025-26 (evidence on C)**, 12 figures, whole patients, from
  `step3_waiting_list_month_end_2025-04_to_2025-09.csv` and `..._2025-10_to_2026-03.csv` (6 columns each) read against the
  appointment files. Primary (D4, absence evidenced in a file no habitual join reaches): each snapshot is taken at 06:00 on
  the first working day after the month end, and a patient leaves the list only when the first treatment appointment is
  outcomed, up to four working days later, so every snapshot still lists patients first seen in the month's last days;
  only the appointment files show they had started. Moves every month by 11 to 59 patients. Hazards: the snapshots change
  layout at the record migration (D2); the weeks-on-list column runs from the date added. **Not two-sided, and why:** the
  WHAT is fixed for the whole year (waiting until the first attended treatment appointment), so dropping a listed patient
  already seen by the month end is never wrong on either side of the migration; a two-sided version would need a changed
  definition of waiting, which the cracker would read and execute. The rows as they stand miss every month, so the full
  includer keeps none of it; a response that cross-checks the appointments keeps all of it.
- **Ask 2, the new digital platform's four-module finishers by month began, September 2025 to February 2026 (evidence on
  D)**, 6 figures, whole patients, from `steadyway_activity_export_2025-07_to_2026-05.json` (users and section events,
  UTC). Primary (D2, a label stored before a silent switch): the vendor's content release for patients beginning from 5
  January 2026 replaced the last section of module 3 with two new ones and added a section to module 5, under new content
  IDs, while earlier patients kept the old structure. A module is finished when all of its sections are completed.
  Inferring each module's sections from the whole export over-counts both structures, and reading rows as they stand (a
  module finished when every section the patient opened is completed) over-counts both sides too. Found only by an internal
  inconsistency: few patients ever finish modules 3 and 5. Moves every month by 3 to 11 patients. Hazard: UTC timestamps
  against local months (D8). Pin test: the sentence carries the population (patients who began on the new platform), the
  window (eight weeks from beginning) and the count (four modules); the device sits in which records are one module.
- **Ask 3, the waiting list initiative's agency hours and cost by month, May to October 2025 (context for A's fix)**, 12
  figures, hours to the nearest hour and cost to the nearest 100 pounds, from `agency_timesheets_2025-04_to_2026-03.csv`
  (10 columns) with the booking register and the appointment files.
  - **Two-sided primary (D1 and D2, a system change whose date one filed WHAT pins):** the register files that timesheets
    went through the agency portal until 31 July 2025 and through e-rostering from 1 August 2025. A corrected claim is a
    second timesheet for the same week. On the portal it replaces the first; on e-rostering it is an adjustment line for
    the difference. So the battery's latest-version rule is right before 1 August and wrong after, and summing every row
    is right after and wrong before. Corrections run at about one week in seven, so every month moves.
  - **Second primary (D6, an allocation whose weight is recorded):** the portal records a week's total. A week that crosses
    a month end belongs to the months of the days worked, and a 30-hour booking works four days whose weekdays only the
    therapist's appointments show.
  - **Third primary (151's family, a catch-up half settled in a later line):** about half the initiative's therapists filed
    their first two or three weeks late as one timesheet in a later week. That is an impossible weekly total, and it
    belongs to the weeks it covers.
  - **Hazards:** the long-standing locum's timesheets in the same export (scope), extension lines at the 2025 framework rate
    from 1 October (D2), UTC register stamps (D8).
  - **Pin test:** the sentence carries the population (the agency therapists brought in for the waiting list), the measure
    (hours worked and their cost) and the months. The devices sit in which rows are one week's claim and which days carry
    the hours.

**Hazard table.**
- **UTC stamps:** asks 2 and 3, under one bin each when mishandled.
- **Migration layout:** ask 1, no figure moved when read.
- **The locum's timesheets:** ask 3, about 160 hours and 9,000 pounds a month when kept.
- **Framework rates:** ask 3, cost only, October.

**Referee.** None arbitrates: the appointment files are the second source for asks 1 and 3 and agree with the golden on
every day they cover.

| Block | Cracker keeps | Mirror keeps | Cracker |
|---|---|---|---|
| Ask 1, step 3 patients waiting at each month end (12) | 0 of 12 | 0 of 12 | miss |
| Ask 2, digital four-module finishers by month began, September to February (6) | 0 of 6 | 0 of 6 | miss |
| Ask 3, agency hours, May to October (6) | 0 of 6 | 0 of 6 | miss |
| Ask 3, agency cost, May to October (6) | 0 of 6 | 0 of 6 | miss |

The three profiles, each scored on the cut pack:
- **The cracker** lands the call, converts UTC, removes exact duplicates and closed referrals, applies the latest-version
  rule to timesheets, joins booking lines as of the day, keeps only the initiative's bookings, spreads each week over Monday
  to Friday and infers module structure from the whole export. It keeps nothing.
- **The mirror** (off the call) reads the snapshots as they stand, counts a module as finished when any section is, and
  books each week to the month it starts in with the locum included. It keeps nothing.
- **The full includer** (off the call: every row as it stands, no exclusion, no dedupe) keeps none of the 30 figures.

A response that reads the snapshots against the appointments, splits module structure at the January release, applies
each timesheet route's own correction rule and spreads weeks and late claims over the therapists' own days reproduces the
asks. That is the fair handling every device has.

Mirror leakage: 0.0 per cent of ask weight.
Pair ceiling: 28.5 (landed call 45.0 with no ask figure kept, missed call 12.0; the same with the full includer as the miss).
Measured by: generator/ceiling.py on the cut pack.

## Ladder

Measured on the clean truth by `generator/harness.py` (never shipped) at the shipped seed 402 and swept over seeds 1 to 15
(`generator/seeds.py` and the stage-2 sweep), on the world as built: a winter rise in referrals (October 2024 to March
2025) forms a step 3 backlog, the waiting list initiative clears it longest waiter first between 12 May and 22 August
2025 (no wait past 33 weeks), 32 agency therapists at a time from 5 May, first starts spread over ten weeks, a first block
renewed with p 0.4 and later blocks with p 0.45 while the renewed block ends by 14 November, no new cover after 22
August, and the list's leaving hazard 0.3 per cent a week to 18 weeks and 2 per cent after. Recoveries on the national
measure, courses ending 1 April 2025 to 31 March 2026, step 3 courses that attended a treatment appointment unless
stated. Each rung names its candidate and the one fact that kills it.

| Rung | Construction | Files | Seed 402 | Seeds 1-15 | Dies to |
|---|---|---|---|---|---|
| 0 | the clinician KPI: A by the discharging practitioner (agency 48.6, employed 46.5 per cent) | contacts, scores, directory | A 0 | 0 at every seed | every broken course is discharged by an employed therapist |
| 0 | B by modality (and against 2024-25 telephone); D against 2024-25 digital; E groups withdrawn | contacts, scores | B -17.6 (-32.5), D 58.8, E 4.9 | largest rival read 93 (B, seed 12) | each is a small or noisy read below A's floor |
| 1 (Ends on) | C by wait band: long waiters' shortfall 263.8 plus extra list leavers 56.1 | contacts, referrals | C 320.0 | 1.21 to 1.41 times coarse A | long waiters' poorer outcomes sit on the same courses the cover held |
| 2 | A by the first practitioner's kind (agency-first shortfall) | contacts, directory | A 262.5 | 0.96 to 1.04 of C without leavers | it is C's wait-band shortfall counted on the same courses: the cover and the wait are one block |
| 2 | cross-tab wait band by first kind | contacts | 4 cells below | long-wait employed 2 to 12 courses | the only short-wait agency courses are the long-standing locum's; long-wait employed is 6 courses |
| 3 (decisive) | the broken courses: each course's therapists against the booking register's assignment ends, priced from the lapse against the year's other step 3 referrals that had attended as many treatment appointments | contacts, directory, booking register | A 257.3 (733 courses, 114 recovered, 371.3 expected) | 198.9 to 260.6 | (golden) |

**Risk 1, C against coarse A.** The default path's C with its list leavers (320.0) beats the coarse first-practitioner
read of A (262.5) by 1.22 times at seed 402 and 1.21 to 1.41 times over seeds 1 to 15. Without the leavers C's wait-band
shortfall (263.8) and coarse A (262.5) are one quantity read twice (1.00 at seed 402, 0.96 to 1.04 over the sweep): the
backlog cohort is the cover's caseload, so no honest lever separates them; a direct effect of the wait adds to both and
the off-diagonal cells are a few courses each. So the solver who prices C without its leavers and A by the first
practitioner reaches a tie on the same courses at rung 2 and has to split the block; the cross-tab and the clinician KPI
both lean to C there, and the split is the decisive step. This is the crack Gate F will look at: a solver who gives the
whole block to the cover lands A at about 260 without the decisive step. The leaving hazard heavier after 18 weeks is
the honest lever that widens the with-leavers margin (C's leavers 56.1, from 12 under a flat hazard).

**Risk 2, the cross-tab.** Started step 3 courses ending in 2025-26 (n, early-ending rate, recovery rate): short-wait
employed 3,843, 4.6, 49.5 per cent; short-wait agency (the long-standing locum alone) 109, 1.8, 49.5; long-wait employed 6,
16.7, 33.3; long-wait agency 967, 50.6, 22.3. A careful solver concludes that agency therapists do as well as employed ones
at short waits and that long waits do badly whoever holds them, with six long-wait employed courses too few to say
otherwise (their 95 per cent interval covers both the long-wait agency and the short-wait rate, asserted); that reads as
C, and the short-wait agency cell is one long-standing locum, not the initiative's cover, so it cannot separate the cover
from the wait either. Within the long waits there is no gradient: 18 to 21 weeks 49.1 per cent ending early (recovery
25.2), 22 to 25 weeks 53.2 (20.8), 26 to 29 weeks 52.8 (21.0), 30 to 33 weeks 45.7 (23.0). The timing route without the
register (agency-first courses by start month against the blocks' ends) shows nothing either: 47.5, 49.6 and 50.1 per cent
ending early for June, July and August starters, because each therapist's block ends on their own date.

**Risk 3, the funding end and the monthly chart.** No new cover after 22 August and no block renewed to end after 14
November: breaks by lapse month July 55, August 277, September 340, November 61; the last lapse (13 November) breaks 7
courses and the largest single date 70; 19 December is never reached. The chart a careful solver draws (step 3 starts,
early endings and practitioners in post by kind, by month, both years): starts 887 in July and 697 in August as the
backlog cohort begins treatment; early endings 179 in September, 225 in October, 71 in November, then 59 and 62 over the
new year (the holiday rise that 2024-25 also shows, 55 in January 2025); agency therapists in post 33, 35, 24, 7 from
July to October. The early endings follow the cohort's starts by the length of a course, which is the wait story, and
the cover's run-down moves with them because the cover held the cohort: the chart shows the confound, not a separation.
Readability row added below; verdict readable, as a rung below the decisive one.

**Risk 4, A's graded cost (SF4 settled).** The comparison is part of the WHAT and is filed in the plan's own voice: what a
referral would have had "is read from the year's other referrals at the same step" (3.3). It names no handover,
reallocation, register, continuity or departure. Inside it the method stays open and every member grades to 250 at the
nearest 50: landmark at the exact count 256.7 (257.3 with the 24 employed-leaver handovers in the pool, the bundle's
literal reading and the golden), landmark in bands 254.0, pooled 246.0, every handover 254.8, employed-only pool 258.0
(pooled 248.3), the cover's own courses coarse 262.6 (landmark 261.9); tightest edge 12.4, a quarter of the bin. The
generator closes the spread (ordinary dropout 0.3 per cent a session, no wait-dependent drift in the scores). Outside the
filed comparison the subgroup pools spread wider (unbroken agency 220.5 and 239.5, unbroken long waiters 203.6 and 227.8,
2024-25's courses 260.0) and are ruled out by "the year's other referrals at the same step"; A still exceeds every
rival's widest read by 2.87 times under them. C's golden is 70.9 (extra leavers 56.1 plus 14.8 on the pooled long-wait
comparison, whose unbroken long waiters are the courses that ended before their cover lapsed). Over seeds 1 to 15 A's
smallest estimator is at least 1.96 times the largest rival read (seed 3) and at least 2.14 at every other seed.

**Pricing sequence.** 1 residue: which courses carry the change, then a comparison the plan files. 2 ceiling: the
affected population (967 long-wait agency courses) could lose about 480 recoveries; A needs 257. 3 one-group-by routes:
by discharging practitioner (0), by first practitioner (262.5, the block), by wait band (263.8, the block). 4 standard
error of A in its own units: about 6 recoveries on the landmark pool. 7 the subset recovered exactly is the broken
courses themselves, read from the register's ends. 8 the reflex sweep is the rung table above. Broken before a second
treatment appointment: 31 of 733, so the recovery rate's finished-course rule carries little and stays out of the
driver.

## Tried and rejected

- The seed's world (2026-11-03, at the draw): a wind turbine's five faults read against the turbine's own healthy-year
  power curve is task187's insight (a unit's shortfall against the right reference curve at matched conditions) in the
  same room (turbines, nacelle anemometers, icing, yaw, pitch); its client domain (Supply Chain & Logistics) reaches
  Root-Cause only through interpretability, ruled a backdrop for an operations world at task129 v1; energy's
  Root-Cause cell is task129's and the room is task187's. Moved before any harness.
- Screened on paper at the draw (2026-11-03), each set aside before any code, with the reason:
  - an epidemiology composition draw (a borough's excess admissions carried by care home residents): task401's cell
    and insight, registered the same day;
  - drug co-prescription (the "triple whammy") behind excess acute kidney injury: the coarse exposure (any of the
    three drugs) contains the fine one, so the attributable count is the same either way, and naming the target
    population makes the step a filed rule;
  - a point-of-care assay's missed RSV corrected from quality-control re-tests: two-phase verification weighted by the
    testing rate is spent (task267, task120, task124, task228, task274's screen) and a verification report names the
    sensitivity;
  - stated cancellation reasons corrected from a save desk's probed reasons: the "true" reason is another opinion, so
    either the plan names it (a rule) or the reading forks, and it re-attributes losses away from a filed label
    (task13);
  - fluoridated water supply zones behind child dental extractions: an outcome scaling with a property of each case's
    surroundings is task129's form;
  - preventer supply lapsing over the school holidays behind September asthma admissions: a per-event state rebuilt
    from consecutive records is task121's device and close to its insight;
  - stock against flow (length-biased) census sampling: task182's driver;
  - an inspection window's onset: task487;
  - competing exits in a cumulative incidence: task133's lesson;
  - immortal time in a churn driver model: the decisive step is the exposure clock, which a pin would name;
  - net of recovered or deferred demand: either a count of listed recoveries (a rule) or a window the WHAT names;
  - a production line's restart tail booked as speed loss: no client domain with a Root-Cause task type holds it;
  - a fraud model's false declines from a holdout: precision moving with the base rate is task446's insight;
  - a mystery-shop routine blind to evenings: the swap test reads the same in any branch network.
- The first harness world (2026-11-03, stage 2): agency cover allocated by a wait threshold of 16 weeks, so short and
  long waiters both reached it; the cross-tab of wait band by first practitioner separated the wait from the cover at
  once (101 long waiters with employed therapists recovering at 51.6 per cent, 142 short waiters with agency cover), a
  cheap route to A. Redrawn so the cover takes the backlog (waits of 18 weeks and over) and one long-standing locum
  carries ordinary short-wait courses.
- Waits rising through the year with the cover ending in early November (2026-11-03, stage 2): about 400 long waiters
  started after the cover ended and went to employed therapists, the same cheap separation. Redrawn so the backlog
  forms between January and June 2025 and the initiative's funding ends on 19 December 2025 with final blocks booked
  to that date.
- A waiting-list leaving hazard of 0.85 per cent a week (2026-11-03, stage 2): with the longer backlog, C's own cost
  (the extra leavers) exceeded A's at three seeds of six. Lowered to 0.30 per cent.
- Telephone-first step 2 at 2.2 points of recovery with a small video and face-to-face group (2026-11-03, stage 2):
  B's reads swung from -25 to 102 by method, within reach of A. Cut to 0.4 points with a larger comparison group.
- G4 and then G6 as the decisive generator (2026-11-03, stage 2): refused by `check` (test.same_driver against task232
  v2, whose interviewer change between waves identifies a roster effect, task121 v6, task129 v2 and task243;
  test.same_puzzle_older against task144, task228, task265 and task68). G9 stays decisive.
- A flat list-leaving hazard of 0.6 per cent a week (2026-11-03, stage 2, risk 1): the backlog's leavers split across
  2024-25 and 2025-26, so C's extra leavers fell to 12 and C with leavers came within 1.07 times of coarse A. Replaced by
  0.3 per cent a week to 18 weeks and 2 per cent after (C's leavers 56.1).
- Monday-start agency bookings (2026-11-03, stage 2): lapses bunched on single Sundays (130 to 215 broken courses a date)
  and the long-wait employed cell rose to 21. Starts drawn over working days.
- A first wave started over six weeks with a first renewal of 0.2 (2026-11-03, stage 2, risk 3): 524 of 762 breaks fell in
  August and early endings jumped to 313 in September as agency therapists in post fell from 38 to 16, the readability
  screen firing on the monthly chart. Spread over ten weeks with a first renewal of 0.4.
- No referral surge (2026-11-03, stage 2): step 3 starts fell to 0.4 of normal from December 2024 to April 2025 while 40
  employed therapists stayed in post, an idle-staff tell. A winter rise in referrals forms the backlog instead.
- Loose clearance without longest-first order (2026-11-03, stage 2): broken courses halved, A fell to 110 to 160 and rivals
  came within 1.2 times at some seeds. Longest-first kept.
- The long-standing locum taking 5 per cent of ordinary step 3 patients: about 40 sessions a week. Cut to 2.5 per cent.
- Seeds 7 and 14 (2026-11-03, stage 2): seed 14's longest waiters recovered best inside the backlog cohort (30 to 33 weeks
  38.6 per cent against 20.7 at 18 to 21 weeks), a dose-response a careful solver would read against the wait; seed 7 sat
  on an earlier world. Seed 402 shipped: no gradient inside the cohort, every filed-comparison estimator mid-bin.
- Ask devices dropped at stage 2: carried-across digital patients (discovery and remedy one act); the digital beginners,
  the over-18-week counts and the agency cover's November and December (no device reaches them); three agency therapists
  booked after the backlog cleared, with no patients (an idle booking reads as generated), left out of the pack.
- Ask devices one-sided against the full includer (2026-11-03, stage 2, the coordinator's precut read): an off-call
  response that handles every device banks the ask weight. The timesheet corrections were made two-sided at the route
  change of 1 August 2025 (filed in the register), and the digital ask was moved to span the January 2026 content release.
  Its first form, which only added sections, let the cracker's whole-export inference keep January and February (2 of 6),
  so the release also retires a section of module 3, and both structures now count against any single inference. The
  waiting list ask stays one-sided (its WHAT cannot change mid-year without a filed rule the cracker would execute).
