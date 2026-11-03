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
  assignment end broke off, an exposure no column marks, and which cases the outcome is counted over, since the
  recovery rate's finished courses drop the patients a broken course loses before a second treatment appointment); Gate
  G `decomposition_attribution` (a correctly counted fall assigned to the right change). Gap population then objective;
  pattern none; generators G9 (the measured outcome, the recovery rate on finished courses, is not the kept one), G4
  (who holds the course after the handover), G6 (agency cover was given the longest waiters, so the wait and the cover
  move together).
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
  Josh Parry (people and resourcing lead, keeper of the agency booking log), Lesley Thompson (performance and
  information analyst, the monthly report). None is in the prompt.
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
  practitioner who held it, and counts the outcome over every course that began, not over the finished ones. The
  nearest device on file is task399's (an actor's roster read against each case); the insight differs (there the
  advocate's absence at the call confounds another actor's measured disparity; here the practitioner's departure
  breaks the course and the patient is lost).
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
3. Price each change with the field's measures: B from step 2 recovery by modality (telephone below video and
   face-to-face) times the courses moved to the telephone; D from the digital platform's completions; E from the
   group places withdrawn; A from recovery by practitioner (agency therapists' recovery rate is level with or above
   employed therapists', so A costs nothing); C from step 3 early endings by wait band (they climb steeply with the
   wait), the excess among long waiters plus the patients who left the waiting list.
4. C prices highest: fund the extra block of step 3 sessions.

Ends on: C, the step 3 waiting list (about 190 recoveries on the default path's pricing).

Golden: A, the agency cover's lapsing assignments (about 140 recoveries): the step 3 courses an agency therapist's
assignment end broke off lose most of their patients after the handover, and long waiters held by a therapist who
stayed end early no more often than short waiters; C's own cost is about 50.

## Stump sentence

A competent solver walks the year's fall in recoveries down the referral-to-recovery funnel, finds it in step 3
courses that end early, reads those early endings as the waiting list's because they climb with the wait, finds agency
therapists' recovery rates level with employed therapists', and files C, the step 3 waiting list (Ends on: C); the step
that lands it there is never setting each step 3 course's run of therapists, rebuilt across the record migration,
against the agency booking log's assignment ends, which shows the early endings come from the courses an agency
therapist's lapsing assignment broke off (agency cover was bought for the longest waiters), so the change that cost the
most recoveries is A.

## Three rules

- **Task type:** `mediation-moderation-process-modeling` (Psychology & Behavioral Science): how a change reaches an
  outcome through the process that produces it; it serves Root-Cause in the taxonomy.
- **Domain test:** the quantity that decides is the recoveries each service change cost through the process by which
  a course of psychological therapy produces a recovery (attending, finishing, crossing caseness on PHQ-9 and GAD-7),
  estimated as therapy outcome research models a service change through its mediators; the field's reflex measures are
  the national recovery rate by step, modality, wait and clinician.
- **Swap:** "fund fixed-term posts because the courses agency therapists' lapsing assignments broke off lost most of
  their patients" with a gym's nouns ("members whose trainer's contract ended stopped coming") loses the course of
  therapy measured session by session against caseness thresholds and the alliance a handover breaks, so the estimate
  has nothing to run on.
- **Layer 1:** an electronic record migration in October 2025 re-keyed practitioner identifiers, joined back only
  through a directory whose names differ from the booking log's; the booking log writes an extended assignment as a new
  row, not an end; outcome measures are item-level before the migration and totals after it; the monthly KPI report
  carries preliminary figures the refreshed extract revises; appointments run on local time and the booking log on
  UTC; the fiscal year runs April to March against calendar-month extracts. Nothing is placed to be caught.
- **Layer 2:** estimand and identification: the right exposure (the courses an assignment end broke off, not the
  courses an agency therapist finished) and the right population for the outcome (every course that began, not only
  the finished ones the recovery rate counts), against a wait gradient that the allocation of agency cover produces.
- **Decisive step:** reading each step 3 course's run of therapists against the assignment ends of the therapist who
  held it, and counting what the broken courses lost from the handover on over every course that began, rather than
  reading the early endings by wait band or the outcomes by the therapist who discharged.
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
