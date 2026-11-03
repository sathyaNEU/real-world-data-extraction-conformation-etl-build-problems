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
national measure, fell between 2024-25 and 2025-26. Five things changed in 2025-26 and the board's improvement review
lists them, each with the fix it would buy: A, agency high-intensity cover brought in from May 2025 on 12-week
assignments renewed quarter by quarter to clear the step 3 waiting list (fix: fixed-term posts); B, telephone-first
step 2 from April 2025 (fix: video and face-to-face as standard); C, the step 3 waiting list itself (fix: an extra
block of step 3 sessions); D, the digital therapy platform changed in July 2025 (fix: return to the old platform); E,
the stress management groups withdrawn from September 2025 (fix: reinstate them). The board's 2026-27 improvement fund
is committed at the year-end contract review to the one change that cost the service the most recoveries in 2025-26.

What nothing in the pack says: an agency therapist whose assignment lapses at a quarter's end leaves mid-course, the
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

## Default path

1. Read the board's improvement plan: the fund goes to the change that cost the service the most recoveries in
   2025-26, a recovery counted on the national measure (a course ended in the year after at least two treatment
   appointments, at caseness at the first treatment appointment and below caseness on PHQ-9 and GAD-7 at the last).
2. Walk the referral-to-recovery funnel by step and year: recoveries fell by a few hundred; step 2's recovery rate is
   a little lower; step 3 lost the most, because more step 3 courses ended early.
3. Price each change with the field's measures: B from step 2 recovery by modality (telephone against video and
   face-to-face) times the courses on the telephone (about 4 at seed 402); D from digital courses against 2024-25's
   (about 32); E from the group places withdrawn (about nil); A from recovery by practitioner, attributed as the
   national data attributes a course, to the practitioner who discharged it (agency 44.4 against employed 48.0 per
   cent, so A costs nothing); C from step 3 courses by wait band, the long waiters' recovery shortfall against the
   short waiters' (about 269) plus the waiting list's extra leavers against 2024-25 (about 43).
4. C prices highest: fund the extra block of step 3 sessions.

Ends on: C, the step 3 waiting list (about 312 recoveries on the default path's pricing at seed 402).

Golden: A, the agency cover's lapsing assignments (about 250 recoveries at seed 402): the wait's total association
with lost recovery splits into the path through the step 3 courses an agency block's lapse broke off (about 700
courses, most of whose patients stop attending after the reallocation) and the wait's direct path, about nil, since
long waiters whose therapist stayed recover like short waiters; C's own cost is the waiting list's extra leavers plus
that direct path, about 70.

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
  carries preliminary figures the refreshed extract revises; appointments run on local time and the booking log on
  UTC; the fiscal year runs April to March against calendar-month extracts. Nothing is placed to be caught.
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
  courses); the standing family once the records are read is the broken-course reading, whose spread is measured at
  stage 2; what rules the others out is quiet, a relation no document invites.
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
| the broken courses, priced from the reallocation (decisive) | no | no column marks a course broken; practitioner identifiers re-keyed at the migration, booking log on other identifiers and UTC | no, the field prices the wait and the clinician, never a course's run of therapists against assignment ends | no control isolates it | no, the battery chains extensions and maps identifiers but does not split a wait effect by its mediator | no, a landmark comparison per course | no, the booking log is the people team's own record and carries ask 2's rates | silent |

## Semantic fork table

Main-call terms and conventions. The closures marked "to file" are written into the improvement plan at stage 3
and asserted in `generator/checks.py` under these ids.

| Id | Term or convention | Golden reading | Alternatives | Ruled out by |
|---|---|---|---|---|
| SF1 | recovery | the national measure: course ended in the year, two or more attended treatment appointments, at caseness at the first, below on PHQ-9 and GAD-7 at the last | scores at assessment as the first; any two contacts | to file: the plan's measure annex in the national wording |
| SF2 | the year | referrals whose course ended 1 April 2025 to 31 March 2026, local dates | received in the year; calendar 2025 | to file: the plan's period clause |
| SF3 | a change's cost | the recoveries the year's referrals would have had without that change, less those they had | the fall from 2024-25; the KPI shortfall | to file: the plan's cost clause |
| SF4 | the comparison for a referral a change reached | open design tension (`## Ladder`, risk 4) | landmark by count and wait band; pooled; agency-only; banded | to settle at stage 3 by measurement, then file or grade on a band |
| SF5 | an agency assignment | a booking and its extensions, first start to last end | each booking line's end as an end | to file: the booking log's own header line |
| SF6 | a practitioner across the migration | one person under an old and a new identifier, joined through the directory | each identifier a different practitioner | the directory's own mapping columns; asserted that every course spanning 13 October 2025 keeps its therapist under the map |
| SF7 | the step of a referral | step 3 when any treatment appointment is with a high-intensity therapist | step at assessment | to file: the plan's step clause; asserted inert for the call |
| SF8 | which change gets the fund | the change with the largest cost | largest cost per patient reached | to file: the plan's fund rule |

## Closure table

| # | Axis | Reading here | Closure |
|---|---|---|---|
| 1 | Population | referrals whose course ended in 2025-26, every one that began (not only finished courses) | SF2, SF3 filed |
| 2 | Unit of account | the referral; a recovery is one referral | SF1 filed |
| 3 | Attribution window | the course's end date | SF2; C1 checked: no broken course's counterfactual end leaves the year (to assert) |
| 4 | As-of dating | the refreshed extract of 6 May 2026 | filed as-of; the preliminary report is a different release |
| 5 | Version basis | refreshed extract over the preliminary monthly report | the plan names the refreshed extract |
| 6 | Denominator | the recovery measure's finished courses at caseness for rates; costs are counts | SF1, SF3 |
| 7 | Weighting | none; counts | n/a |
| 8 | Window length | one fiscal year | SF2 |
| 9 | Boundary inclusivity | 1 April to 31 March inclusive, local dates | C1: assert no course ends within a day of either boundary under UTC against local |
| 10 | Rounding path | whole recoveries, rounded once at the end | to file in the prompt's rounding sentence |
| 11 | Tie-break | not needed: A clears every rival by 2.7 times or more | asserted margin |
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

On paper at stage 2: executing the prompt and the plan's clauses word for word (SF1 to SF3, SF5 to SF8) gives one
reading of every term except the comparison for a reached referral (SF4), which stays open until stage 3 settles it
by measurement; the call (A) is the same under every member of the standing family, the figure is not yet.

## Oracles

None that rank the candidates. The monthly KPI report (preliminary) reports the recovery rate, waits and the
clinician rates correctly for what it measures and agrees with the wrong path on every figure it prints; the vendor's
usage reports and the timesheets feed the asks only. To check at stage 3 that no shipped figure ties only under the
golden.

## Ask sheet

The asks sit on quantities the call never computes, each from an ask-only file, each a component of the review's
case for another change on the list (H18), with the call's population carrying no device (zero device rows among
step 3 referrals ending in 2025-26, asserted by count). Devices are engineered and measured at stage 3; nothing
below is measured yet.

- **Ask 1, the digital programme's engagement funnel (evidence on D)** from the two vendors' usage exports (the old
  platform to June 2025, the new from July): for each month of 2025-26, the patients who began a programme and how
  many of them completed four of its modules within eight weeks (24 figures, whole numbers). Primary device to
  engineer (D7, a reconstruction across two systems): patients carried across in July sit in both exports in their
  first weeks under different keys; hazard D8 (UTC events against local months).
- **Ask 2, the agency cover's hours and cost by month (context for A's fix)** from the agency timesheets: for each
  month from May to December 2025, hours worked and their cost at the booking line's charge rate (16 figures). Primary
  device to engineer (D2, a rate stored on an extension line): extensions booked from 1 October carry the new
  framework rate; hazard D6 (weekly timesheets split across month ends by their daily columns).
- **Ask 3, the step 3 waiting list at each month end (evidence on C)** from the list's monthly snapshots: the number
  waiting and the number waiting over 18 weeks from referral (24 figures). Primary device to engineer (D5, the
  snapshot's clock runs from assessment for patients re-added after a pause); hazard shared with ask 1 (D8).
- **Main population zero-counts:** to assert. **Hazard table:** to write with per-ask deltas.
- **Cracker sheet** (the cracker lands the call, runs the hygiene battery, executes every filed rule): to measure on
  the cut pack; every row must read `miss`.
- Mirror leakage: pending, under 50 per cent required.
- Pair ceiling: pending, 60 or under required.
- Measured by: generator/ceiling.py (to write at stage 3; shares no code with the generator).

## Ladder

Measured on the clean truth by `generator/harness.py` (never shipped) at seed 402 and swept over seeds 1 to 5
(`generator/seeds.py`). Recoveries on the national measure, courses ending 1 April 2025 to 31 March 2026, step 3
started courses unless stated. Each rung names its candidate and the one fact that kills it.

| Rung | Construction | Files | Seed 402 | Seeds 1-5 | Dies to |
|---|---|---|---|---|---|
| 0 | funnel plus the clinician KPI: A by the discharging practitioner (agency 44.4, employed 48.0 per cent) | contacts, scores | A 0.3 | 0 to 9 | every broken course is discharged by an employed therapist |
| 0 | B by modality; D against 2024-25 digital; E groups withdrawn | contacts, scores | B 4, D 32, E -3 | B -86 to 59, D -7 to 32, E -10 to 9 | small at every seed; below A's floor |
| 1 (Ends on) | C by wait band: long waiters' shortfall (269) plus extra leavers (43) | contacts, referrals | C 312 | 229 to 277 | long waiters whose therapist stayed recover like short waiters |
| 2 | A by the first practitioner's kind (agency-first shortfall) | contacts, directory | A 270 | 197 to 257 | it sits beside C's 312 on the same courses: the cover and the wait are one block |
| 2 | cross-tab wait band by first kind | contacts | long-employed 59 courses; short-agency 44.4 against short-employed 48.0 | 36 to 62 courses | no cell separates the wait from the cover |
| 3 (decisive) | the broken courses: each course's therapists against the booking log, priced from the reallocation against courses that had come as far | contacts, directory, booking log | A 251 (714 courses) | 194 to 237 | (golden) |

The standing estimators of A's counterfactual at seed 402: landmark at the exact count of attended treatment
appointments 250.9, landmark in bands 247.6, pooled over all unbroken courses 234.3, unbroken agency courses only
192.2, every reallocation including the one employed leaver's planned handovers 247.5. C's golden is 71.7 (extra
leavers 43.2 plus the direct path among courses whose therapist stayed, 28.5). Under every estimator A exceeds the
largest rival (C 71.7) by 2.7 times or more at seed 402 and by 2.9 times or more at the lowest seed; B's widest read
(99 at seed 5, telephone against 2024-25 telephone) stays under A's floor at every seed. The default path's C (312)
beats the default reads of A (0.3), B (4), D (32) and E (-3) at seed 402, and the coarse first-practitioner read of A
(270) stays below it, so a solver who prices the cover the coarse way still files C. Broken before a second treatment
appointment: 84 of 714 (12 per cent), so the recovery rate's finished-course rule carries little and is out of the
driver. The comparison the counterfactual is read from is part of the estimand and is filed (`## Semantic fork
table`); the bin for A's graded figure is set at stage 3 from the standing family's spread on the shipped seed.

**The coordinator's four stage-2 risks, each a generator change to make and measure before `precut.py`** (written
2026-11-03 when the session paused; nothing below is measured yet unless it says so):

1. *Coarse A against wait-band C are one set of courses counted twice.* Measured at seed 402: coarse A (first
   practitioner) 270, C's wait-band shortfall alone 269, C with the extra list leavers 312. They are structurally
   equal (both read the broken courses' loss), so the only separators are the list leavers and any direct wait path.
   Change: raise the list-leaving hazard from 0.30 to about 0.60 per cent a week so the leavers carry about 85 (C's
   golden stays near 100, under half of A), and measure both C variants against coarse A over seeds 1 to 5. The
   ladder then says plainly which rung each solver reaches: the default (A by the discharging practitioner, C with
   its leavers) files C; a solver who prices A by the first practitioner and C without leavers reaches a tie on the
   same courses and must split them, and the split is the decisive step.
2. *The stratified cross-tab* (early ending and recovery by wait band and first practitioner kind) is the cracker's
   natural move. Measured at seed 402: long-wait employed 59 courses, short-wait agency 44.4 against short-wait
   employed 48.0 per cent recovery per started course; the long-wait cells' rates are still to print. Change: the
   initiative clears the backlog longest-first, so cap the backlog's waits at 33 weeks; long-wait employed then falls
   under about 15 courses at every seed, and the long-standing locum's ordinary short-wait courses keep short-wait
   agency at the short-wait rate. The cracker then reads "agency cover is sound at short waits and long waits do
   badly", which is C. Print the four cells (n, early-ending rate, recovery rate) at seed 402 and over the sweep, and
   assert in `checks.py` that the long-wait employed cell's 95 per cent interval covers both the long-wait agency rate
   and the short-wait rate, so it cannot separate the cover from the wait.
3. *The funding end.* With staggered 12-week blocks, lapses fall through July to November at each therapist's own
   block end (no quarter-end waves, which would announce the renewal cycle); the 19 December end is the one
   synchronised date. Change: taper the programme (no new cover starts after August, no block renewed to end after
   mid-November) so the final lapse breaks under about 60 courses, and give both years a holiday disengagement in the
   last fortnight of December and the first of January, so what remains of the December rise reads as the season
   that 2024-25 also shows. Run the readability screen on the monthly chart a careful solver draws (step 3 starts,
   early endings and active practitioners by kind, by month, both years) and record it.
4. *A's graded cost* spread 192 to 251 across estimators, about 27 per cent, which no mid-bin grade survives. The
   comparison is part of the WHAT and must be filed so the literal execution is one number, and this is the open
   design tension the next session settles first, measured, before any pack is cut:
   - filing the comparison as referrals "whose course ran to its own end" (or any wording that excludes the broken
     courses) makes the solver ask which courses were cut short, which is readability test 1 on the decisive step,
     so it fails the fork-is-the-stump test;
   - filing it as all of the year's step 3 referrals in the same wait band that had attended as many treatment
     appointments keeps the decisive step silent and executes to one number, but the broken courses sit inside their
     own comparison group and drag the expectation down, most in the long-wait band where they are the majority; A's
     figure under that clause must be measured against C before it is adopted;
   - the third option is to grade A's cost on a band (nearest 50, or a range) shown mid-bin for every standing
     estimator, keeping the comparison open where the design forces it (the landmark is the counterfactual the WHAT's
     "would have had" implies) and asserting the call under every member.
   Settle by measurement at the shipped seed, record the choice in `## Semantic fork table`, and never file a clause
   that names a handover, a reallocation, the booking log or a therapist's departure. No ask grades C's direct
   path.

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
