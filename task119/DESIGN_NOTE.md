# task119: the region's one external review of deaths after delayed escalation, realising analytical_tasks note AD01

Source note: `analytical_tasks/02_anomaly_detection/AD01_mortality-review-transfer-chain-origin.md`. This is the slot's second
draw, made at checkpoint A on 2026-10-09 after the author rejected the first draft (its architecture is in `## Tried and
rejected` and in the card's lineage). It keeps the note's world and decision, a regional health board placing its one
twelve-month external mortality-review engagement at one of eight acute trusts, narrows the remit to deaths after delayed
escalation to critical care, drops the transfer chain and draws a new decisive move. Stage 1 (draw) only: the ladder in full,
the closure table, the ask sheet and the prompt come at stage 2.

```
DRAW  (independent draws, checked with ../.claude/skills/fingerprint/guard.py)
  Card filed: yes, registered 2026-10-09 after checkpoint A (go on the redraw) (the coordinator registers approved redraws in draw order;
      scratch card <scratchpad>/cards/task119.json)          Verdict: PASS
  Shape: other   (8 trusts x 3 figures = 24, the trust, its confirmable deaths, the runner-up and the gap = 4,
                  5 named chart parts, 3 files: 36 criteria; not 01, because nothing is ranked under a cap)
  Gate G mechanism: decomposition_attribution
  Gap: objective (deaths after long waits are counted correctly and are not what the review is scored on), then population
  Pattern: C (the share of each trust's long waits the review can attribute to the trust, reached through a join to its unit's
           other admissions); decisive generator G3 (the occupancy record says capacity, the admissions made during the wait
           say allocation), G8 in support, G2 at the morning-return rung
  Domain: Policy & Education (policy-education)   Subdomain (enumerated): public-administration
  Objective: Anomaly Detection & Diagnostics (anomaly-detection)
  Pairing repeated from last build? no (task123 is nonprofit-grant-making x etl; this pairing was last built as task25)
  Stakeholder role: head of quality surveillance at a regional health board (compliance_or_audit)
  Context-artifact type: capacity_report (the critical care network's monthly capacity report: occupancy at 08:00 by unit and
           referrals waiting over four hours by trust, 36 months, correct and ranking no trust)
  Calibration form: retry_or_revision_log (the national rapid-review programme's log of thematic escalation reviews in the four
           neighbouring regions: 34 reviews closed 2021 to 2025, 41 attempts, each review's confirmed deaths, with the reviewed
           windows' referral, unit and bed-return records)
  Decision type: pick_one_of_n (named_option)   Scoring unit: per resolved case (a death confirmed as avoidable in the trust's
           own care)
  Decisive mechanism: for every death after a wait of more than four hours for a level-3 bed, what the referring trust's own
           unit did while the referral waited, read from the unit's admissions and its hour-level census: the wait counts where
           the unit held an empty staffed bed or admitted planned post-operative patients from the trust's own theatres
  Repeats from prior builds: none on a banned axis; (objective, C, pick_one_of_n) repeats task25, task26, task28 v2, task35 v1,
           task38 v3 and task53 v1, and (objective, C, decomposition_attribution) task38 v3, all older and differentiated on the card
  Forum: board_of_directors (the regional health board's board places the engagement)   Forcing event: audit_or_inspection
           (the engagement's fieldwork opens 1 April 2027)   Org family: hospital_or_health_provider
  Spine (planned): critical_care_referrals_202307_202606.csv, one referral of an adult ward or emergency department patient for
           a critical care bed (referring trust and ward, decision-to-admit time, level of care, admitting unit, admission time),
           about 42,000 rows, synthetic; the admitted patient care episodes (about 900,000 rows) carry the deaths and the segment
  World: United Kingdom, England, a fictional NHS region of eight acute trusts (labelled A to H until stage 2 names them) and its
           adult critical care network (level-3 units at A, C, D and G; B, E, F and H run level-2 care only); GBP; invented
           names carried from the note: Kellow Bridge, Sandmere, Fenwold (trusts in the neighbouring regions' review log)
  People (guard.py names --geo "United Kingdom, England" --seed 119, locale en_GB):
           Andrea Davey, head of quality surveillance (the requester)
           Norman Scott, chair of the regional health board
           Maria Reynolds, critical care network manager (the capacity report and the bed returns)
           Diana Smith, information manager (the referral log and its dictionary)
           Sharon Banks, national rapid-review programme coordinator (the review log)
           Benjamin Davies, lead reviewer at the external review provider
  Deliverables (planned): external_review_placement_2027-28.docx (the board paper that commits),
           review_placement_workings.xlsx (the per-trust figures and the device-carried asks),
           review_placement_by_trust.png (the visual)
  Opening move (planned): question-first
  Committed call: the one acute trust at which the external review examines, in 2027-28, the deaths of adult patients who
           waited more than four hours for a level-3 bed. Forward facing (a window that has not opened) but not a forecast:
           the decisive practice runs steadily through all 36 months, so the latest four quarters stand for the engagement
           year and the tag stays Anomaly Detection.
  Remit (planned, filed): the engagement is judged by the deaths its reviewers confirm as avoidable because of problems in
           the reviewed trust's own care, the methodology note counting the trust's decisions about the use of its own beds
           and staff as its own care; no sentence names planned admissions, occupancy or the order of admission
  Decisive trap (measured): #17 guesses an attribution the data can settle, behind #11 beats the headline trap, misses the
           quiet one, with #7 uses the ready-made measure at the morning-return rung
  Windows: 36 months to 30 June 2026; latest four quarters July 2025 to June 2026; extract taken 14 August 2026 (45 days after
           the last discharge; death registration lags at most 14 days)
  As-of date: 2026-10-02 (the scenario's analysis date, unchanged from the first draft; this draw made 2026-10-09)
```

Similarity claim: no prior build places a scarce engagement by attributing waits to a unit's own allocation, found only in the
sequence of the unit's other admissions during each wait. The serviceable-share builds on file (task25, task28 v2, task38 v3)
reach part of a reported magnitude through a property of the candidate's own records, and the conduct-and-constraint builds
(task111 v1, task88) excuse an apparent conduct failure by its outside cause or price displaced demand in a full period, while
here every occupancy measure excuses the answer and the decisive fact is a second patient's planned admission during the first
patient's wait.

## Stump sentence

Hardening loop 3's sentence, the build's current one (loop 2's, G at 15 by the admission type, and loop 1's, A at 37 by the
any-admission reading, are now grid cells):

A competent solver counts each trust's deaths after a wait of more than four hours for a level-3 bed, sets aside the
trusts holding no level-3 beds, rebuilds every unit's census from its stays, writes the remit's methodology sentence as
its test (an empty staffed bed, or a freed bed given to a patient the trust placed itself, the bureau's transfers set
aside) and files Prideswick (G) at 15 over Ristenholm's 2; the step that lands it there is reading the unit feed's bed
assignment as the patient in the bed: through every Stennock long wait since the platform went live its unit held one or
two staffed beds assigned at the morning bed meeting to its own elective centre patients, who the theatre extract shows had
not left recovery when the waiting patient's decision was made, so Stennock kept beds empty for its own planned surgery
while its emergency patient waited, 27 deaths, the largest number the review can confirm. A solver who re-times every held
bed, the bureau's included, files Ristenholm (A) at 37 instead.

## Decisive rung

**Hardening loop 3 puts #13 Validates on one population, applies to another** (`_measured.md`: decided 3 of 64 client tasks,
2 under 0.50, established) **at the decisive step**: the feed's assignment minute is the occupied minute on every row a
solver can check, and not for the beds Stennock assigns to its elective centre patients at the morning bed meeting, which
only the regional theatre extract dates (`### Hardening loop 3`). The admission-type and who-placed readings below (#5, #17)
now decide only whose hold each held bed was. The rest of this section is the frame as written at the draw and in loop 2.

**Hardening loop 2 puts #5 Takes the population a flag or filter suggests** (`_measured.md`: decided 5 of 64 client tasks,
3 under 0.50, established) **at the decisive step.** The admissions a trust placed itself are defined through a join, the
admitted patient's referral (and, for a transfer between trusts, the bureau's audit), and the unit feed ships a flag that
agrees with that rule for most admissions and not for all: `admission_type` 02 is a bureau transfer and 04 a trust's own
planned case, but Stennock's own planned surgical patients come from its other hospital coded 03, a planned transfer in, and
so do the planned transfers the bureau booked into Ristenholm's evening beds. Reading the code as the population files G
(types 01, 04 and 05, or 04 alone) or A (03, 04 and 05, or anything but 02); only the join names D, record by record. The
frame below (#17, with #6, #11 and #7 behind it) stands as written at the draw.

**#17 Guesses an attribution the data can settle** (`_measured.md`): decided 2 of 64 client tasks, both under 0.50, status
emerging. The records leave out whose decision a long wait was. A solver who takes up the remit's "own care" question reads
a wait at a full unit as capacity, and one who reads the methodology sentence literally counts any bed the unit gave to
another patient during the wait as the trust's decision; what settles each wait is the unit's own admissions joined to the
referral log and the bureau's transfer audit: through each of D's long waits D's unit, full at every hour, admitted planned
post-operative patients from D's theatres, while every admission during A's, C's and G's long waits was a transfer the
network's bed bureau placed. It is reached behind **#6 Treats a mixed segment all one way** (5 of 64, 2 under 0.50,
established): the admissions to the own unit during a wait carry one meaning in the methodology sentence's literal test (a
bed given away), and what splits them sits away from the stays table, in the field guide's entry for the transfer audit's
`bed_confirmed_at` (the bureau's allocation) and in each admitted patient's referring trust; read all one way they name A.
#6 sits behind **#11 Beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50, established), where the solver
who distrusts the morning return and rebuilds the census stops at G, and **#7 Uses the ready-made measure** (5 of 64, 2
under 0.50) carries the 08:00 rung below that. #17's recipe ships a settled case that only the signal reproduces; this
build ships none, because a case that refutes the capacity reading would be a corpus built to refute the naive read, and
the remit's methodology note and the field guide's bureau line pin the attribution instead.

**Corpus blind for a computable reason (L1).** In every corpus case every wait over four hours passed while the reviewed trust's
own unit held an empty staffed bed, because the four neighbouring networks never ran full from 2021 to 2025, so counting every
long wait, counting waits on days the morning return showed a free bed, counting waits in hours the census shows a free bed,
counting waits through which the unit admitted anyone and counting waits the trust's own care could have shortened return the
same deaths for all 34 reviews. Under the naive path (count
every long wait) the corpus reproduces (L7), and every attribution partitions the same deaths, so every total ties (L8).

**Gate G at the draw.** Litmus: no. Every figure is correct (the waits, the 08:00 returns, the units' admission and discharge
times, the deaths, the capacity report) and no voice's claim about its own numbers is overturned; the difficulty is attributing
correctly recorded waits to what held them. surface_read_dependency: no · stumping_family: analytical_non_defect ·
sole_data_defect: no (the 08:00 return is complete and correct at its stated meaning, an hourly return would still show D's
unit full because D filled it, and the allocation is a relation between two patients' records that no field carries). Deletion:
no wrong number exists to delete.

**Draw checks (stumping Part 6.1 against proven-in-production.md).**

- Strategy: S7, every screen is right and the answer is what nothing flags, at a cross-record grain (a wait set against the
  other admissions to the same unit while it ran), with C's attributable share as the frame. Laws L1, L3, L7 and L8 are writable
  in this world: each partial correction (morning return, hour-level census) lands on a named wrong trust further from D.
- Dead shapes (Part 4), each closed at design: a corpus built to refute (the corpus reproduces under every attribution); a
  device announced by its own columns (the referral log says nothing about what the unit was doing, the unit admissions carry
  each admission's source and nothing joins them to a wait); silence in a pack that breaks it (no document may say that units
  admit planned cases while referrals wait); a recovery of what an instrument could not observe (the answer is a name, and an
  hourly bed return still excuses D); argmax under a stated rule (no rule states the attribution beyond the methodology's general
  sentence); a dated cause (D's practice is steady, the only dated events sit under decoys).
- First moves of the opponent: the one-period group-by names E; the occupancy decomposition names C (morning return) or G
  (census); the methodology sentence read as a work order (any bed given to another patient) names A; the corpus back-test
  reproduces under every reading; no series steps; every total ties.
- Objective: the call separates each trust's waits held by network capacity (the artifact) from the waits its own care made (the
  real event), and places the one review there; no forecast enters the call.

## Ladder sketch

The draw's four-rung sketch, kept as the draw record. Stage 2 replaces it with the five-rung ladder under `## Stage 2: design`
(a structural rung added, D moved to fourth on rung 0, E killed by the unit register; hardening loop 1 then put the
any-admission rung in the structural rung's place).

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deaths after a wait of more than four hours for a level-3 bed, by referring trust, latest four quarters | E, a district general hospital with level-2 care only, every referral waiting for a bed elsewhere | The remit's own population, and every corpus review reproduces the count | The network's 08:00 returns: on every day E's referrals waited, every level-3 unit in the region reported no empty staffed bed |
| 1 | Waits set aside on days the 08:00 return showed the unit (for E, every unit) full | C, whose unit reports empty beds most mornings | A capacity check on the network's own published figures, and C still leads | The census rebuilt from the units' admission and discharge times: C's unit fills with emergencies through each afternoon, and every one of C's long waits passed in evening hours with all four units full |
| 2 | Waits set aside in the hours the census shows the unit full | G, whose ward referrals waited through afternoons while its unit held empty staffed beds | The exact occupancy at the hour, and G's waits are its own gatekeeping | Overtaken: through every one of D's waits D's unit admitted planned post-operative patients from D's theatres, and D's deaths after those waits outnumber G's |
| 3 | **Decisive:** waits through which the referring trust's own unit held an empty staffed bed or admitted planned patients from the trust's own theatres | **D** | | |

- **Position.** D is third on rung 0, excused on rungs 1 and 2 (its unit is full at 08:00 and at every hour of every wait), and
  leads only rung 3; rung margins and the dominance ratio (D's attributable deaths against G's, and against C's carried lead on
  the raw count) are settled at design.
- **Grid.** Occupancy basis (none, morning return, census) by unit scope (own unit, whole network) by allocation (ignored, read)
  gives 12 cells; every cell without the allocation reading names E, C or G, asserted at design. The own-unit and network
  readings agree everywhere by construction: D's waits pass with every unit in the region full, G's with its own beds empty,
  and C's and E's with every unit full and no planned admission anywhere.
- **The chain.** Dropped, not demoted: transfers sit in the referral log as ordinary rows (E's referrals go to other units'
  beds), and no rung links spells across trusts.
- **Asks.** Components of the call only (per trust: referrals that waited more than four hours, deaths after them, and the deaths
  the review can confirm in the trust's own care); the device layer is designed with `supplemental-stumping` at stage 2.

## Nearest exemplars

* Medicare Billing Integrity Review, "Refer NPI 1508302506 for the review year 2024 level-mix records review" (filed under
  Policy & Education), measured mean 0.18 over 4 runs. Nearest on decision: one provider sent for a
  review out of a field where the face-value measure ties; the model broke a 111-way tie by volume instead of reconciling each
  provider's summary total to its detail rows (trap #19).
* School District Finance Review, "Select Jurupa Unified School District for the cycle 3 fiscal diagnostic review" (Policy &
  Education), measured mean 0.41 over 1 run. Nearest on decision and on the stop: one system named for a diagnostic
  review, where the model got close to the controls, kept the winner and lost the runner-up, the counts and the margin (trap #3).

Both stumps sit on a reproduction gate, the architecture this redraw leaves; the redraw puts the miss on an attribution the
records settle (#17). The measured records for #17 are *Scope re-observation for P-0447 at 262 sessions* (mean 0.39) and *Return
134,225 dollars to the Threadgill Endowment* (mean 0.19).

## Guard

Verdict against the registered corpus (task117, task118, task120 and task123 included): **PASS** (`guard.py check`, exit 0)
at the draw. The card is registered at `.claude/skills/fingerprint/cards/task119.json`; re-checked at stage 2 against the corpus
with task121 and task122 now registered, it returns **WARN** (exit 0) on repeat.gate_g (task121, task122) and repeat.decision
(task122), the two rules the batch preview below already answers.

- BLOCKs met while drawing, and how each was cleared: test.same_puzzle_older on (objective, C, pick_one_of_n) against task25,
  task26, task28 v2, task35 v1, task38 v3 and task53 v1, and test.same_driver_older on (objective, C, decomposition_attribution)
  against task38 v3, cleared by one differentiation line each on the card; every one is older than the window of twelve.
- No relabel. C is the pattern the corpus files for a serviceable share and carries the decisive computation here (the share of
  each trust's long waits the review can attribute, behind a join to the unit's other admissions); G3 names the decisive insight
  and is listed as the decisive generator. Filing G3 as the decisive mechanism instead would put this card on the structural
  signature of the unregistered sibling task121 v2 (population, G3, decomposition_attribution, pick_one_of_n) inside the window.
- WARN people.first on Carole (task105) and on Raymond (task105) while drawing: cleared by Maria Reynolds from the same seed.
- Nearest drivers: task89 v4 and v5 lineage at 0.06, task111 v1 lineage at 0.06, task94 v3 at 0.05, task88 at 0.04, all under
  the 0.12 WARN line. task111 v1 shares the frame (whether a delay is the unit's own) and not the move, which runs the other way
  here; the card carries lines for task111 and task88 as well.
- Batch preview, not binding: with this card registered first, the current scratch cards for task121 and task122 (both drawn
  2026-10-09) check at WARN only, on repeat.gate_g and repeat.decision (all three are decomposition_attribution picks) and, for
  task121, overuse.org_family. Calibration, artifact, role, forum, event and organisation family were chosen clear of both
  siblings, and with task122 registered first this card also checks at WARN on the same two rules.
- Hardening loop 1 (2026-10-09): the card's stump is the loop-1 sentence (A at the any-admission rung), its spine row count the
  rebuilt 30,785 and its notes carry #6 behind the decisive rung; `guard.py validate task119` 0 invalid, `guard.py heart task119`
  **WARN** (exit 0) on the same two rules, nearest heart text 0.05 (task89 lineage) and nearest driver 0.06, under the 0.12 WARN
  line.
- Hardening loop 2 (2026-10-09): the card's stump is the loop-2 sentence (G at 15 by the admission type, A at 37 for a solver who
  keeps planned admissions), its spine row count the rebuilt 33,739 and its notes carry #5 at the decisive step; the driver
  sentence stands (the intakes during each wait, read for whose decision placed them). `guard.py validate task119` 1 card, 0
  invalid; `guard.py heart task119` **WARN** (exit 0) on repeat.gate_g and repeat.decision, nearest heart text 0.05 (task89
  lineage), nearest driver 0.06, under the 0.12 WARN line.
- Hardening loop 3 (2026-10-10): the card's stump, driver and concrete driver now carry the held beds (#13), spine rows
  33,719; `guard.py validate task119` 1 card, 0 invalid. `guard.py heart task119` returns **BLOCK** on ban.subdomain against
  task126, a card drawn and registered on 2026-10-10, after this one, with the same domain and subdomain
  (policy-education/public-administration); the heart window is the last three cards by draw date, so a later draw now sits in
  it. The ban belongs to task126's draw, which this build cannot change (its card and folder are outside this build's scope);
  run as of this card's draw date (cards drawn to 2026-10-09 only, a scratch copy), the heart is **WARN** (repeat.gate_g,
  repeat.decision), nearest heart text 0.05 (task89 lineage) on the full corpus and nearest driver 0.07, under the 0.12 WARN
  line. Raised to the coordinator rather than answered here.
- Variants checked and not taken: crediting delays to a unit only when a bed stood free anywhere in the network forks between
  own-unit and network readings, needs a pin that names the question, and repeats task111 v1's frame and task88's full-period
  blindness as the decisive move; a fixed random review sample that makes the yield a density is C on reach and reads as
  Opportunity Sizing; a documented exclusion over-applied to a mixed segment (the hospice unit, specialist transfers, a virtual
  ward) is either the confirm shape whose top responses check, a G3 card on the sibling's signature, or the first draft's
  transfer story again; the chain itself is (population, G2), banned against task120, or (population, D), spent in seven
  older builds.

## Changes from the source note

1. **A new decisive move.** The note's own move, chains of spells linked across trusts and credited to the trust where the chain
   began, collides under honest labels and is the architecture the author rejected (an unstored unit recovered and gated by
   reproducing published reviews). The decisive rung is now what each trust's own critical care unit did while its referrals
   waited (C, decisive generator G3), and the chain is dropped.
2. **The remit narrows** to the region's external review of deaths after delayed escalation to critical care, a thematic
   mortality review, so the engagement, the deaths it examines and every rung sit on administrative records (referrals, bed
   returns, unit admissions) with no risk model. The note's SHMI funnel, palliative coding, risk-adjusted CUSUM and case-mix
   framing are dropped.
3. **The corpus no longer refutes anything.** The national programme's thematic rapid reviews reproduce under every attribution
   because the neighbouring networks never ran full (L1). The note's retry log, which only the chain reproduced, is gone; the form
   stays a retry log because the programme retries a review that confirmed nothing.
4. **The context artifact** is the critical care network's monthly capacity report (capacity_report), replacing the note's
   monitor export and the first draft's published series; it is correct and ranks no trust.
5. **The decoys** become the capacity ladder (E's level-2-only waits, C's morning vacancies, G's empty afternoon beds) in place of
   the five documented flags (elective case mix, hospice unit, weekend diversion, virtual ward, coastal catchment).
6. **The asks** become components of the committed call (per-trust long waits, deaths after them, deaths the review can confirm),
   replacing the note's critical care bed-day and ambulance handover asks, which answered other decisions (H18); the chart shows
   the deaths the review can confirm by trust and names no construction.
7. **Furniture.** Forum board_of_directors, because the note's quality committee is committee_or_panel, banned against task118;
   forcing event audit_or_inspection kept; deliverables renamed `external_review_placement_2027-28.docx`,
   `review_placement_workings.xlsx` and `review_placement_by_trust.png`.
8. **People.** Howard Singh (the weekend belief) leaves with the weekend decoy; Maria Reynolds, the critical care network manager,
   is drawn from the same seed (Carole Brown and Raymond Hooper repeat a first name in task105).

## Stage 2: design (2026-10-09)

Every number below is a target the generator builds forward and asserts. The targets were checked on a scratch prototype
(wait-level counts by attribute, the twelve-cell grid, the record-wide ask targets, every subset of device mishandlings, the
census-path collisions and the pair sweep); the prototype is not the generator and does not ship. Trusts keep their letters in
this note; their names are provisional until the stage-3 H21 sweep.

### Settlements of the draw's open items

1. **Five rungs, not four.** The stage gate asks for 5 to 6 rungs, and the sketch had four with D third on rung 0, which breaks
   the position rule (stumping Part 3, 4th or 5th). A structural rung goes in after the raw count: the remit's own-care clause
   read at the trust's structure, which sets aside the four trusts holding no level-3 beds and names A, the regional centre. D now
   sits fourth on rung 0 and third on rung 1. Hardening loop 1 moved that structural reading into the correction grid (the
   none/own cell, A 44 over C 35) and put the any-admission rung (A 37 over D 27) fourth, so A leads one rung, not two.
2. **Rung 0 is killed by the unit register.** E's long waits pass in evenings and nights with every unit full, and some of their
   decision dates follow a morning when C's unit reported an empty staffed bed, so the sketch's killing fact (every unit full at
   08:00 on every day E waited) no longer holds. The register does: E holds no level-3 beds, so every E wait is for another
   trust's bed.
3. **The asks keep the draw's three figures per trust and move to the whole record.** On the latest four quarters the trio is
   free for both top responses (the census path and the decisive path agree on every trust but D, so the mirror keeps 22 to 24 of
   24 figures and the pair sits near 83), and its rows are the main call's own rows, where no device may sit (supplemental-stumping
   Part 1). Over the whole of the network's record (July 2023 to June 2026) the same trio crosses the nine months before the
   referral platform replaced the legacy system, which is where the device layer lives, off every row the main call reads. A total
   row is added (three criteria).
4. **The corpus refutes nothing.** It reproduces all 34 reviews under the naive count and under every attribution the ladder offers
   (L1, L7, L8); no settled case refutes the capacity reading, and the remit's methodology note pins the attribution.
5. **Own unit against whole network.** They agree at the census basis with admissions ignored by construction (no long wait
   overlaps an hour when another unit held an empty staffed bed). Once admissions are read, the network reading counts other
   units' admissions during E's and A's waits and names E; at the 08:00 basis C reports empty beds on mornings before other
   trusts' patients wait, and the network reading names C or E. Each is a wrong cell, mapped to "its own beds".
6. **The census-grain fork is closed by the bed-assignment convention.** The unit feed dates a stay from the minute its bed is
   assigned, so a bed that frees and goes to the next patient shows no empty interval at any grain.
7. **Deaths** come from the admitted patient care episodes' linked date of death, as the draw planned, so in-hospital and
   post-discharge deaths within 30 days both count; the discharge method alone gives in-hospital deaths, a rival the corpus refuses.
8. **The prompt names no window.** The placement window is filed in the remit (the latest four complete quarters); the docx asks for
   what a year of review could confirm and the chart for the period the placement rests on.

### The world

The Ostle Regional Health Board commissions and oversees eight acute trusts and the Ostle Adult Critical Care Network.

| | Trust (provisional name) | Level-3 beds | Role |
|---|---|---|---|
| A | Ostlebury Teaching Hospitals NHS Foundation Trust | 30 staffed, regional centre | rung 3 decoy: its full unit takes bureau transfers from trusts without level-3 beds through most of its long waits |
| B | Tannerby Hospital NHS Trust | none (level-2 unit) | texture |
| C | Brenhythe Hospitals NHS Foundation Trust | 14 staffed at night, 16 by day | rung 1 decoy: empty staffed beds at 08:00 on most weekday mornings, full by midday with emergencies |
| D | Stennock University Hospitals NHS Foundation Trust | 18 staffed, surgical centre | the answer: weekday elective lists send planned post-operative patients to its unit |
| E | Lessington Hospitals NHS Trust | none (level-2 unit) | rung 0 decoy: most deaths after long waits, all for other trusts' beds |
| F | Ellerdyke Hospitals NHS Trust | level 3 until 31 March 2024, level 2 since | carries the register-vintage device |
| G | Gorrington Hospitals NHS Foundation Trust | 12 staffed | rung 2 decoy: holds staffed beds empty through weekend afternoons until a consultant review |
| H | Pevenham Hospitals NHS Trust | 3 winter level-3 beds, 4 December 2023 to 31 March 2024 | carries the register-vintage device |

Timing, constructed and asserted: D's planned post-operative admissions arrive on weekdays from late morning to early evening, and
every D long wait falls inside those hours (since hardening loop 2 each is a patient of D's elective centre, a second Stennock
hospital with no level-3 beds: referred by Stennock from the centre's theatre recovery, `REC`, level 3, and admitted 10 to 90
minutes later as a planned transfer in, type 03, source 01, absent from the bureau's audit); C's long waits start in the evening after its unit fills; G's start on weekend
afternoons; A's, B's, E's, F's and H's long waits pass in evenings and nights with every unit full. No planned admission at any unit falls inside a long wait at any trust but D, no long wait
overlaps an hour when a unit other than its own held an empty staffed bed, and physical beds equal staffed beds at the four units
through the latest four quarters. A bed that frees inside an A, C or G long wait goes to a patient referred earlier by a trust
without level-3 beds, placed by the network's bed bureau and logged in its transfer audit (117 such admissions inside A's waits
in the latest four quarters, 23 inside C's, 6 inside G's). At A since loop 2, 66 of the 117 are planned post-operative transfers
(type 03, source 01) referred from the sending trust's recovery after A's waiting patient and given the next bed that freed on a
list-day evening, one inside each of A's 35 death-waits the unit filled and 31 of its 82 survivor waits; the other 51 and every
transfer at C and G are unplanned (02) and were referred before the waiting patient.

Latest four quarters (July 2025 to June 2026): patients who waited more than four hours from the decision to admit to the
assignment of a level-3 bed, deaths within 30 days of the decision among them, and the deaths the review can confirm.

| Trust | Long-wait patients | Deaths after them | Confirmable |
|---|---|---|---|
| A | 150 | 44 | 2 |
| B | 36 | 10 | 0 |
| C | 118 | 35 | 0 |
| D | 92 | 27 | 27 |
| E | 190 | 56 | 0 |
| F | 46 | 13 | 0 |
| G | 74 | 21 | 15 |
| H | 25 | 7 | 0 |
| Network | 731 | 213 | 44 |

D's 27 are deaths after waits through which D's unit, full at every hour, admitted planned post-operative patients from D's own
theatres: every D long wait falls on a weekday during the elective lists, and at weekends D's freed beds reach its waiting ward
patients inside four hours. G's 15 are waits through which G's own unit held an empty staffed bed from
the decision to the assignment; its other 6 are capacity. A's 2 are waits with an hour of empty staffed bed at A; 35 of its
other 42 followed waits through which its full unit took bureau transfers, and 7 waits through which it admitted nobody. Long-wait
mortality runs 28 to 30 per cent at every trust. E also leads the deaths before a bed was assigned, so the chair's belief points at
E on either reading.

### Gate G

- **Litmus.** No. Every figure in the pack is correct (the waits, the 08:00 returns, the units' stays, the deaths, the capacity
  report, the corpus), and no voice's claim about its own numbers is overturned: the network manager's "D's unit is full every
  morning" is true. The difficulty is attributing correctly recorded waits to what held them, which no field carries.
- **Mechanism** decomposition_attribution: each trust's long-wait deaths split into network capacity and the trust's own care.
  surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
- **Deletion test.** Delete the chair's belief, the network manager's notes, the capacity report and the licensed basis: the natural
  pipeline still counts E first, the census still shows D's unit full at every hour of every D wait, and the answer is still D. No
  wrong number exists to delete.
- **Clean-data test, per suspect file (asserted in the generator).** The daily 08:00 bed return: filled (it has no gap), corrected
  (it is correct at its stated meaning) and replaced by an hourly return of occupancy against staffed beds; rung 1 then names G, the
  answer stays D because D's unit is full at every hour (D filled it), the naive leader stays E, and D differs from E. The capacity
  report: deleted, nothing moves. An instrument observing the decision's own quantity would be a field on each referral saying
  whether the trust's own unit took a planned case during the wait; no system records it, because it is a relation between two
  patients' records, and the records carrying both halves are complete in the pack.
- **Lens-swap test.** The naive read (every long-wait death by referring trust) and the answer are not one population under two
  lenses: the answer is the subset whose interval contains another patient's planned admission to the referring trust's own unit,
  a join to a different entity's records over a time interval. Asserted: no column or pair of columns on the referral log reproduces
  any trust's confirmable count within 8 per cent.
- **Identity test.** Confirmable deaths equal deaths after own-care long waits, and own care is neither filed as a construction nor
  forced by any symptom.

### Entity, unit of value and decision

The regional health board places one twelve-month external review and is scored on the deaths its reviewers confirm as avoidable
because of problems in the reviewed trust's own care (per resolved case). Two quantities read as size: the deaths after a long wait
(the review's case load) and the deaths the review can confirm (its yield). They rank the trusts differently because the long waits
at trusts holding no level-3 beds, and the waits that passed with a unit full of emergencies, are network capacity, while a unit that
keeps itself full with its own planned work turns its full hours into its own care.

Decision: exactly one acute trust from {A to H} for the 2027-28 engagement (pick_one_of_n, named option), placed on the latest four
complete quarters (filed). Forward facing and not a forecast: D's practice runs steadily through all 36 months.

### The answer

**D**: 27 confirmable deaths in the latest four quarters; runner-up G with 15; gap 12 deaths; margin 1.80x. D ranks 4th of 8 on the
natural pipeline, behind E by 2.07x.

### The ladder

Current since hardening loop 3 (2026-10-10; the loop-2 ladder, where rung 4 read who placed an admission during the wait, is
in `## Tried and rejected`). Rungs 0 to 2 are unchanged; rung 3 is now led by A over G with D at zero, and rung 4 reads the
patient in the bed.

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deaths within 30 days after a wait of more than four hours for a level-3 bed, by referring trust, latest four quarters | E, 56 over A 44 (1.27x) | The remit's own population counted exactly as filed, and the corpus reproduces all 34 reviews under it | The unit register: E holds no level-3 beds, so every E wait is for another trust's bed |
| 1 | Waits set aside on days the trust's own 08:00 return showed no empty staffed bed (trusts without level-3 beds carry none) | C, 34 over G 4 (8.50x) | A capacity check on the network's own published return, and C's waits survive it | The census rebuilt from C's stays: C's unit was full at every hour of every C long wait |
| 2 | An empty staffed bed in the own unit's census (by bed assignment, as the feed dates a stay) at some minute of the wait | G, 15 over A 2 (7.50x) | The exact occupancy through each wait, and G's waits passed beside its own empty staffed beds | The theatre extract against Stennock's stays: through every Stennock wait its unit held beds assigned to its own planned surgical patients still in theatre, 27 deaths against G's 15 |
| 3 | An empty staffed bed or any admission to the own unit during the wait | A, 37 over G 17 (2.18x); D 0 | The methodology sentence read literally: a bed given to another patient while this one waited | The transfer audit and the field guide's `bed_confirmed_at`: every admission inside an A long wait was a patient referred by a trust without level-3 beds on a bed the bureau allocated |
| 4 | **Decisive:** a staffed bed in the own unit with no patient in it and not held by the bureau at some minute of the wait (a bed the trust assigned to its own patient who had not left theatre recovery is empty until then), or an admission the trust placed itself | **D, 27 over G 15 (1.80x)** | | |

- Round 3's own test (rung 3 with the bureau's placements set aside: an empty bed by assignment, or an admission the trust
  placed itself) is the grid cell census/own/placed and files G at 15 over A's 2, the stump sentence's wrong answer; a solver
  who re-times every held bed, the bureau's included, files A at 37 over D's 27 (held_all cells).
- Every rung names a different trust (E, C, G, A, D), asserted by name after every parameter change.
- Rung 4 carries the stump: measured trap #13 (validates on one population, applies to another), with #17 and #5 behind it
  in the attribution of each hold, #11 at rung 2 and #7 at rung 1.
- The admission-type and queue readings of own placement (loop 2) now all sit on the assignment census and land on the decoys:
  local types or 04 alone name G 15 over A 2; planned types, anything but 02 and the queue order name A 37 over G 15.
- The structural reading (the raw count at the four trusts holding level-3 beds, A 44 over C 35, 1.26x) is the none/own cell of
  the grid, killed by A's 08:00 returns (no empty staffed bed on any of the 139 days A's referrals waited in the latest four
  quarters).
- Gaps (stumping Part 1). Rung 0 to 1 opens the objective gap; rungs 1 and 2 move the moment at which the own unit's capacity is
  read; rung 3 reads the full unit's admissions. Rung 3 to 4 opens the population gap twice over: which beds the feed counts as
  taken held no patient (a relation between a stay and its patient's theatre case), and whose hold each was (the trust's or the
  bureau's). Decisive gap objective, reached through population, as the card files it.
- Survival properties of rung 4 (loop 3 design, `### Hardening loop 3`): written nowhere; the corpus is blind; no arithmetic
  symptom; not a row predicate; round 3's own step completes and returns G; no cutover in the placement window; the theatre
  extract is evidence, not a wrong number. Accepted weak points are stated there.
- Worth on the graded quantity: the leading count walks 56, 34, 15, 37, then 27.

### Position table (asserted row by row)

| Rung | Leader | D's rank among the four trusts holding level-3 beds | D's count | D behind the leader by |
|---|---|---|---|---|
| 0 | E 56 | 4 of 8 overall | 27 | 2.07x |
| 1 | C 34 | last | 0 | (at zero) |
| 2 | G 15 | last | 0 | (at zero) |
| 3 | A 37 | last | 0 | (at zero) |
| 4 | D 27 | 1 | 27 | leads G by 1.80x |

D leads no intermediate rung and is second on none. No rung margin is under 1.15x; the thinnest is 1.27x at rung 0. On the
grid cells that re-time every hold (A 37 over D 27) D is second at 1.37x, a wrong cell, not a rung.

### Discriminator dominance

- Against A on the every-hold reading: A carries 37 against D's 27 (1.37x). On the decisive axis D keeps all 27 (share 1.000)
  and A keeps 2 of 37 (0.054), an edge of 18.5x against the 1.64x required (1.2 x 1.37).
- Against A at rung 3 (by assignment): A 37 against D 0; on the decisive axis D 27 against A 2.
- The rung-2 decoy G carries no raw advantage into rung 4 (G 21 against D 27); D's decisive edge is 27 against 15, 1.80x.
- Against the raw leaders: E (56 against 27, 2.07x; share 0 against D's 1.0), A (44, 1.63x; share 0.045, an edge of 22x against
  the 1.96 required), C (35, 1.30x; share 0). Every product clears the 1.2 floor.

### Correction grid (asserted cell by cell)

Toggles, since hardening loop 3: occupancy basis (none, 08:00 return, the census by bed assignment, the census with the
trust's own held beds empty until the patient left theatre recovery, the census with every held bed empty including the
bureau's) by unit scope (own unit, whole network) by the reading of the unit's admissions during the wait (ignored, any
admission, admissions the trust placed itself), thirty cells, measured on the shipped pack.

| Basis | Scope | Admissions | Names | Violates |
|---|---|---|---|---|
| none | own | any of the three | A 44 over C 35 (1.26x) | own care at the hour (A's unit full through every A wait) |
| none | network | any of the three | E 56 over A 44 (1.27x) | own care (E holds no level-3 beds) |
| 08:00 | own | ignored or placed | C 34 over G 4 (8.50x) | own care at the hour of the wait (the 08:00 return describes the morning) |
| 08:00 | own | any | A 35, C 34; two wrong trusts within 1.2x, D 0 | as above |
| 08:00 | network | ignored | C 34 over D 24 (1.42x) | "its own beds" |
| 08:00 | network | any | E 54 over A 43 (1.26x) | "its own beds" |
| 08:00 | network | placed | E 51 over C 34 (1.50x) | "its own beds" |
| assignment census | own | ignored | G 15 over A 2 (7.50x) | the methodology note and the theatre extract: a bed kept for the trust's own patient still in theatre is an empty staffed bed the trust kept |
| assignment census | own | any | A 37 over G 17 (2.18x) | the bed bureau allocates every transfer's bed (field guide, transfer audit) |
| assignment census | own | placed (round 3's test) | **G 15 over A 2 (7.50x)**, the stump | as for ignored |
| assignment census | network | ignored | G 15 over A 2 (7.50x), equal per trust to the own-unit cell (C1) | "its own beds" |
| assignment census | network | any | E 52, A 43 (1.21x), D 27 | "its own beds" |
| assignment census | network | placed | E 44 over D 27 (1.63x) | "its own beds" |
| own holds empty | own | ignored or placed | **D 27 over G 15 (1.80x)** (equal per trust, C1) | |
| own holds empty | own | any | A 37 over D 27 (1.37x) | the bureau allocates every transfer's bed |
| own holds empty | network | ignored | D 27 over G 15 (1.80x), equal per trust to the own-unit cell (C1) | |
| own holds empty | network | any | E 52, A 43 (1.21x), D 27 | "its own beds" |
| own holds empty | network | placed | E 44 over D 27 (1.63x) | "its own beds" |
| every hold empty | own | any of the three | A 37 over D 27 (1.37x) | a bed the bureau holds for an incoming transfer is not the trust's to give |
| every hold empty | network | ignored | A 41, E 40; two wrong trusts within 1.2x, D 27 | "its own beds" |
| every hold empty | network | any or placed | E 54 over A 43 (1.26x) | "its own beds" |

Only the own-holds basis names D, and its three D cells select the same deaths per trust (no own placement inside any
latest-year wait and no other unit's vacancy inside any Stennock wait). The admission-type and queue readings of own placement
(loop 2) sit on the assignment census and name G 15 over A 2 (types 01, 04 and 05, or 04) or A 37 over G 15 (types 03, 04
and 05, anything but 02, the queue order). The four-hour counterfactual converges: each held patient left recovery 10 to 215
minutes after the waiting patient's decision, inside the first four hours, so "the bed was free in time" and "the bed was free
at some minute" select the same waits. Window cells: the record (D 80 over G 46) names D, so no window moves the name; the
counts are pinned by the remit's placement clause (C4).

### The calibration corpus

- **Form.** The national rapid-review programme's log from the four neighbouring networks: 34 thematic escalation reviews closed
  2021 to 2025, 41 attempts. Seven reviews confirmed nothing, were retried with a doubled case-note sample and confirmed nothing
  again; 27 confirmed between 4 and 31 deaths, 412 in all. Each review's trust-year ships with its referrals, unit stays and daily
  bed returns.
- **What it certifies (C2).** Confirmed deaths equal the deaths within 30 days of the decision among patients who waited more than
  four hours from the decision to admit to the assignment of a level-3 bed, counted at the referring trust: 34 of 34 exactly, so
  the review's yield is the count itself, with no confirmation share. Swept family: clock (decision to assignment, receipt to
  assignment, decision to arrival) by death window (30 days, in hospital only, 7 days, 90 days) by level (decision level 3,
  requested level 3, levels 2 and 3) by deaths before assignment (kept, dropped) by threshold (4, 3, 6 hours), 216 rules. Every
  rival misses at least 4 reviews row by row (L2); every rival that moves the count one way (the clock, the window, the threshold,
  deaths before assignment dropped) misses the 412 total by at least 10 per cent; the nearest rival is named with its miss count at
  stage 3.
- **Blind to the decisive move, for a computable reason (L1).** In every corpus review every long wait passed while the reviewed
  trust's own unit held an empty staffed bed, because the four neighbouring networks never ran a unit full in 2021 to 2025. The raw,
  structural, 08:00, census, any-admission and decisive constructions therefore return the same deaths on all 34 (asserted: zero
  corpus long waits with the reviewed unit full at any hour, and the raw, structural, 08:00, census and decisive constructions
  re-run review by review; the any-admission count follows, every corpus wait already holding an empty bed).
- **Corpus direction.** Under the naive path the corpus reproduces, 34 of 34; it refutes no rung.
- **Twin pair.** Kellow Bridge (2022) and Sandmere (2023): identical on trust type (a district general hospital with a 14-bed
  level-3 unit), referrals in the year, the programme's screen (71 referrals waiting more than four hours from receipt, each),
  mean 08:00 occupancy and all-cause 30-day deaths among level-3 referrals; confirmed 24 and 11 (2.18x). The filed rule reproduces
  both from the records (Sandmere's delay sat before the decision to admit, so fewer of its waits run four hours from the
  decision); the receipt clock gives both 71, and no lookup reproduces the pair.
- **Every rule exercised.** The 30-day window (Fenwold 2021: three post-discharge deaths inside 30 days counted, five between day 31
  and 60 not); deaths before assignment (a review whose count includes four deaths while waiting); the decision level (a review with
  six deaths after long level-2 waits the rule leaves out, and one whose escalated referrals the requested level misses); the threshold (a review with deaths after waits between three and four
  hours); the clock (the twin pair). The attribution is exercised by no case, by design.
- **Resemblance nominates the decoy.** Every corpus review's waits passed beside the reviewed trust's own empty staffed beds, which
  among the live trusts is G's profile. No corpus trust lacks level-3 beds, so E has no analogue.

### Pins and counter-pins

- **Filed, the remit (the board's terms of reference for the engagement, authority 1 to 2).** The scope: adult patients referred
  from a ward or an emergency department for a level-3 critical care bed who waited more than four hours from the decision to admit
  to the assignment of a bed and died within 30 days of the decision. The judging rule: the deaths its reviewers confirm as avoidable
  because of problems in the reviewed trust's own care. The methodology note, one sentence: the trust's decisions about the use of its
  own beds and staff are its own care. The placement clause: the board places the engagement on the latest four complete quarters of
  the network's record. The licensed wrong basis: the national programme screens trusts on referrals waiting more than four hours
  from receipt, and Sharon Banks will present that screen to the board (it ranks E first).
- **Filed, the field guide (authority 4).** A unit stay's `admitted_at` is the minute its bed was assigned; times are as each system
  recorded them; the unit register is effective-dated; death registrations lag at most 14 days and the extract was taken on 14
  August 2026; the transfer audit's `bed_confirmed_at` is the time the network bed bureau allocated the bed at the receiving
  unit (the rung-3 killing fact, stated once, as a field definition).
- **Empirical, the corpus.** The yield equals the count (34 of 34).
- **Counter-pins: none.** The capacity report is labelled in-file (occupancy is the 08:00 return; referrals waiting over four hours
  are counted from receipt, the network's operational standard; it ranks no trust). The network manager's notes state facts (D's
  unit is full every morning) and beliefs (C could take its own patients), never a rule that a full unit is capacity. No
  document says that a transfer is or is not the receiving trust's own care. The stage-3 sweep greps every shipped document for
  quotable sentences near capacity, full, own, planned, theatre, elective, bureau and transfer.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | adult ward and ED referrals whose decision to admit was for a level-3 bed, waiting more than four hours to the bed's assignment; deaths within 30 days of the decision | filed (remit); C1: since 2 April 2024 the level on every referral is the decision's level; C2: the corpus confirms 34 of 34 |
| 2 | Unit of account | one patient, one death | C1: no patient holds two long waits in the latest four quarters, so patient and referral counts agree (asserted); in the record they differ only on device rows (identity merges, parallel-run copies and DV7's 14 repeat patients), where the prompt's "every figure counts people" governs |
| 3 | Attribution window | a death belongs to the window of its decision to admit | C1: no long-wait death straddles either edge of the latest four quarters (asserted), so decision-dated and death-dated windows select the same deaths |
| 4 | As-of dating | a unit's level and staffed beds as of the wait | C1 in the latest four quarters (no register change in the window, asserted); before April 2024 the as-of reading is ask device DV3 |
| 5 | Version basis | one vintage of every main-path file | C1 |
| 6 | Divisor | none: every graded figure is a count | n/a, asserted integer |
| 7 | Weighting | none | n/a |
| 8 | Window length | the latest four complete quarters | filed (placement clause); C1 on the name (four quarters, eight quarters and the record all name D, asserted); C4 on the counts |
| 9 | Boundary inclusivity | more than four hours; within 30 days | C1: no wait in the latest four quarters within five minutes of four hours, no long-wait death between day 25 and day 35 (asserted) |
| 10 | Rounding path | counts, no rounding | n/a |
| 11 | Tie-break | none needed | C4: every rung's top two at least 1.26x apart |
| 12 | Maturity | 30-day deaths complete for decisions to 30 June 2026 | filed (14-day registration lag, extract 14 August 2026); C1: no death registered after 13 August 2026 could fall in any window (asserted) |
| 13 | Order of operations | filter the long waits, then classify | C1: filter and classify commute |
| 14 | Row order | none | C1 |
| 15 | Duplicate resolution | no duplicate decision in the latest four quarters | C1; the parallel-run copies are spring 2024 (ask hazard HZ2) |
| 16 | Identity normalisation | verified identities since 2 April 2024 | C1; temporary identities are legacy (ask device DV2) |
| 17 | Netting | none | n/a |
| 18 | Dimensional units | local time throughout the platform era and the unit feed; a wait is elapsed time | C1 in the window: no wait in the latest four quarters crosses a clock change (asserted), so elapsed and clock readings agree; the legacy UTC clock is ask hazard DV1 and the two spring clock-change nights are ask device DV5 |
| 19 | Code semantics | own care counts the admissions the trust placed itself, read from each admitted patient's referring trust (the bureau's audit agrees for transfers between trusts), never from the admission type | C1 between the referral and audit readings (asserted on the window and the record). Since loop 2 the admission type is a rung, not a fork the closure leaves open: inside the window's long waits the code disagrees with the placement both ways (D's own planned transfers and the bureau's planned transfers into A's unit are both 03), so the type readings name G (01/04/05, 04) or A (03/04/05, not 02), each violating the methodology note read with the field guide's `bed_confirmed_at` line and the referral log's referring trust (C4: G 15 over A 2 and A 37 over D 27 against D 27 over G 15); any admission against own placement is the rung-3 fork, closed the same way; before April 2024 the CCRS-era feed coded every unplanned admission 01, which the type readings price on the record |
| 20 | Integerisation | none | n/a |
| 21 | Scope of a stated clause | own care governs every wait; "own unit" scope | C1 at the census basis with admissions ignored (no wait overlaps another unit's empty staffed bed, asserted); with admissions read the network reading names E, and at the 08:00 basis C or E (C4, each violates "its own beds") |
| 22 | Forward window contents | 2027-28, placed on the latest four quarters | filed; D leads the decisive construction in each four-quarter year of the record (25, 28, 27 against G's 14, 17, 15, asserted); no register change or reconfiguration inside the latest four quarters |
| + | Census grain (hourly snapshot or continuous) | the bed is assigned at the minute it frees | C1: no capacity wait shows an empty staffed bed at any grain; every own-empty wait holds the empty bed from decision to assignment (asserted at minute grain and at hourly snapshots) |
| + | Census reading (empty at the decision, at any time, for an hour, through the wait) | any of them | C1 by the same construction |
| + | Which trust a death belongs to | the referring trust | filed (the remit examines the reviewed trust's patients); C1: every own-care wait ends in the trust's own unit or in death |
| + | Staffed against physical beds | staffed beds from the daily return | C1: physical equals staffed at the four units in the window |

### Deliverables and the criteria arithmetic

Prompt shape: other, one repeated unit (the trust) carrying three figures.

1. `external_review_placement_2027-28.docx` (text, the board paper that commits): opens on D; the deaths a year of review there
   could confirm (27), the runner-up G and the gap (12 deaths). Golden content beyond the asks: why each other trust is not it, in
   words.
2. `review_placement_workings.xlsx` (data, script-written): one row per trust over the whole record, with patients inside the remit
   (3a), deaths among them (3b) and the deaths the reviewers could have confirmed (3c), and a total row.
3. `review_placement_by_trust.png` (visual, script-rendered): one bar per trust for the deaths inside the remit in the latest four
   quarters, the confirmable part shaded, trusts ordered by that part, the gap to the runner-up marked, a title naming D.

Criteria: 8 trusts x 3 figures (24) + 3 totals + the trust, its count, the runner-up and the gap (4) + 5 named chart parts + 3
files = 39, over the 25 floor. Distinct findings: the decisive yield, the three-year record of case load and yield, the network
totals. Validity check: the record against the latest year (the call's persistence). Over-determination: no ask names a source, a
time of day or a share, so nothing solves back for the allocation class. Each ask fails under a wrong path: the call furniture under
every rung below 4 and under every admission-type reading; 3a under legacy transfers read to their arrival, repeat patients
counted per referral, the clock-change nights read on the clock, the legacy level, the legacy clock or unmerged identities; 3b
under those, a per-referral death count and deaths of never-resolved identities missed; 3c under the census path (A, C, D, G),
the any-admission path (A, C, F, G), the planned, not-02 and queue readings (A at least), the 04 and local readings (D at
least), the current register (F, H), the legacy feed's bed episodes read as admissions (A, C, G), the held beds read as empty
(A, C, F, G) and the devices on 3a and 3b.

### The ask ledger (supplemental-stumping Part 9)

The ledger as rebuilt in hardening loop 2. Loop 1 gave each ask a fresh primary (DV7 on 3a, DV5 on 3b, DV6 on 3c) after round
1's solver handled every stage-2 device; round 2's solver then executed every one of them, the loop-1 primaries included, and
kept the whole workbook exact. Loop 2 adds two silent primaries (DV8 on 3a, DV9 on 3b), keeps DV3 as the 3c primary, turns DV5
and DV7 into hazards and retires DV6 into the construction layer (with own placement read from the referring trust it moves
nothing; the CCRS-era coding it carried is now part of what the admission-type readings price).

**Main call's declared row population.** Files: the referral log (decisions 1 July 2025 to 30 June 2026, every trust and level),
the unit stays at A, C, D and G overlapping 1 June 2025 to 30 June 2026 (the census lead-in), the daily bed returns for that span,
the transfer audit's rows in that span, the admitted patient care episodes of patients referred in the window (date of death),
the unit register rows in force in the window, the remit, the field guide and the capacity report. Columns: referral
`referral_id, patient_key, referring_trust, dta_at, level_of_care, outcome, outcome_at`; stays `unit_code, referral_id,
patient_key, admitted_at, discharged_at, admission_type, source_location`; returns `unit_code, return_date, beds_open,
beds_occupied_0800`; transfer audit `patient_key, from_trust, to_unit, bed_confirmed_at`; episodes `patient_key,
date_of_death`; register `unit_code, trust_code, care_level, valid_from, valid_to`. **Every device and hazard row sits outside
the latest four quarters**: the legacy months to 1 April 2024 (DV1, DV2, DV4, DV8, DV9, HZ1, HZ2, and DV3's register rows valid
to 31 March 2024), the two spring clock-change nights (DV5: 30 March 2024 and 29 March 2025) and year 2 (DV7's repeat patients,
July 2024 to June 2025). The zero-counts inside the population are asserted per device (DV8: no stay in the window dated from an
arrival; DV9: no unresolved temporary key in the window); the call, its count, the runner-up and the gap are recomputed with every
device mishandled and asserted identical, and on the whole record D leads with the devices handled or not.

| Ask | Figures, unit | Pool; construction layer | Device layer: primary; hazards | File path (causal) | Use, and how it enters the call (H18) |
|---|---|---|---|---|---|
| 1 Call furniture | the trust; its confirmable deaths in a year; the runner-up; the gap in deaths | A (the recommendation block); rung 4 | none (main path) | register, referral log, stays, returns, transfer audit, episodes, remit, field guide | component |
| 2 Chart | 5 parts | A (the call drawn); rung 4 | none | as ask 1 | component: the call at a glance |
| 3a Record: patients inside the remit | per trust, whole patients; total | B; none | **DV8** legacy transfers dated from the arrival (D8); hazards DV1 legacy clock (D8), DV2 temporary identities (D7), DV4 legacy level semantics (D3), DV5, DV7 repeat patients (D6) | referral log, stays, transfer audit, CCRS level entries, key links, CCRS specification, episode specification, remit, field guide: 9 files, 20 columns | qualifier: the record behind the forward call, which lets one year stand for 2027-28 |
| 3b Record: deaths among them | per trust, whole deaths; total | B; none | **DV9** temporary identities never resolved (D4); hazards DV1, DV4, DV5, DV7, DV8, HZ2 parallel-run copies (D1) | 3a plus episodes: 10 files, 24 columns | qualifier |
| 3c Record: deaths the reviewers could have confirmed | per trust, whole deaths; total | B, both layers; rung 4 (the census path misses A, C, D, G; any admission, the planned and not-02 readings and the queue reading miss A, C, F or G; the 04 and local readings miss D) | **DV3** register vintage (D2); hazards DV1, DV4, DV5, DV8 held beds, DV9 at D and G, HZ1 legacy unit-feed grain (D6), HZ2 at D | 3b plus register, returns, the 2023 board paper: 13 files, 30 columns | qualifier |

Pool A is the call and its picture only (9 criteria, the cracker's by construction); every ask block is pool B. No primary family
repeats (D8, D4, D2).

**Primaries, organs and root causes.** Three root causes: the referral platform replacing the legacy system (CCRS) on 2 April
2024 after a six-week parallel run (RC1), the network's level-3 consolidation on 1 April 2024 (RC2) and the clock itself (RC3:
the platform and the bed-management feed record local time). Each primary's two organs sit in different files, the documentary
one in a document the main call does not read, and no file carries two primaries' documentary organs (DV8 the CCRS
specification, DV9 the episode extract specification, DV3 the board paper).

- **DV8, the legacy bed list dated a transfer from the arrival (primary on 3a; hazard on 3b and 3c).** The CCRS-era
  bed-management list began a row "from the time the patient was placed in the bed"; the platform dates it from the bed's
  assignment. For a transfer between trusts the bureau allocated the bed (`bed_confirmed_at`) and it stood empty until the patient
  arrived (40 to 110 minutes), so on the shipped stays all 974 legacy transfers begin at the audit's `arrived_at` and all 2,823
  platform transfers at `bed_confirmed_at`. Read from the stays, a legacy transfer's wait ends at the arrival: 28 waits whose
  allocation came 3h10 to 3h52 after the decision read past 4h15 (18 designed near misses, two dead patients at each trust whose
  own unit was full and four, two and two at E, B and H; plus the 8 summer clock rows and 2 clock-change-night rows that are
  transfers), so 3a +2 at A, C, D, F and G, +5 at B, +9 at E, +4 at H, and 3b +2 at A, C, D, F and G, +3 at B and H, +5 at E. And
  the census rebuilt from the stays shows each held bed as an empty staffed bed inside the receiving trust's own capacity wait:
  3c +24 at A, +6 at C, +3 at F, +2 at G (the year-1 bureau transfers inside those waits). Organs: the transfer audit (structural)
  and the CCRS specification's "placed in the bed" (documentary). Silent: the 08:00 returns are computed from the same feed and no
  held bed spans 08:00; every other legacy transfer reads under four hours at its arrival; no held bed touches a wait at the
  receiving unit's own trust beyond the designed ones; a trust moving its own patient between its sites assigns the bed on
  arrival, so no Stennock row is held. Over-correction stop: every legacy admission moved back by the audit's median transit (70
  minutes), totals 2,075 / 599 / 143.
- **DV9, temporary identities never resolved (primary on 3b).** Ten legacy emergency referrals inside the remit, one at each
  trust and three at E, carry a temporary key the links never resolve; each patient died in hospital within 30 days, so the death
  is in the episode extract only as the temporary-key spell's discharge method 4 and date, with no date of death (registrations
  link through the verified NHS number). Missed, 3b falls one at every trust and three at E, and 3c one at D and G (the two rows
  that are own-care waits). Organs: the episode extract (structural) and the extract specification's "carry no date of death"
  line (documentary). Silent: the referral-to-episode join on the temporary key still matches. Over-correction stop: every death
  read from the discharge method alone (post-discharge deaths lost, the corpus's refused in-hospital rival), totals 2,163 / 499 / 112.
- **DV3, register vintage (primary on 3c).** 3c minus 6 at F and minus 3 at H when the register's current rows are read for
  2023-24; organs the register's dates and the 2023 board paper's "level 2 care only"; stop: F and H read as level 3
  throughout, 3c 191, call unchanged.
- **Hazards.** DV1 legacy UTC clock (3a +4 at A and E, +2 elsewhere; 3b +2; 3c +11 at A, +5 at C, +2 at D and F, +4 at G; organs
  "held in UTC" and the audit's local decision times; stop: every legacy time shifted an hour, 2,133 / 623 / 143). DV2 temporary
  identities resolved through the links (3a +1, E +2; stop: every referral of a merged identity dropped, 2,154 / 629 / 148).
  DV4 legacy level semantics (3a +2 and 3b +2 at every trust, 3c +2 at D and H; stop 2,154 / 626 / 148). DV5 the spring
  clock change (3a +2 at A, B, C, E and G, +3 at F and H, +4 at D; 3b +2 at A, C, E, F and G, +3 at H, +4 at D; 3c +4 at D, +2 at
  F and H; stop: every clock-change-eve wait dropped, 2,147 / 624 / 147). DV7 repeat patients (3a +3 at A, B, C, F, G and H, +4 at
  E, +1 at D; 3b +2 at the seven; stop 2,140 / 615 / 148). HZ1 legacy bed-episode rows (3c +2 at A and C, +4 at G; stop 3c 146).
  HZ2 parallel-run copies on a per-referral death count (3b +4 at every trust, 3c +4 at D; stop 2,157 / 627 / 148).

**No-cancel rule.** Asserted by enumeration: no subset of the 1,023 combinations of mishandled devices lands any touched figure
or total on its golden, per trust and per total; and for each of the seven wrong readings of own care (census, any admission,
planned, not 02, queue, local, 04) no subset lands its 3c on the golden at a trust where the reading differs.

**Targets (record, July 2023 to June 2026).**

| Trust | 3a patients | 3b deaths | 3c confirmable | Natural path 3a / 3b / 3c | Census path 3c, devices handled / not | Any admission 3c | Planned or queue 3c | 04 reading 3c |
|---|---|---|---|---|---|---|---|---|
| A | 438 | 126 | 8 | 454 / 137 / 39 | 6 / 32 | 99 / 106 | 99 / 105 | 8 / 38 |
| B | 104 | 29 | 0 | 128 / 38 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| C | 351 | 104 | 5 | 365 / 115 / 17 | 1 / 8 | 23 / 29 | 5 / 15 | 5 / 15 |
| D | 275 | 80 | 80 | 291 / 93 / 91 | 0 / 5 | 80 / 91 | 80 / 91 (queue 90) | 0 / 5 |
| E | 559 | 165 | 0 | 632 / 176 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| F | 140 | 40 | 6 | 155 / 51 / 0 | 6 / 0 | 9 / 0 | 6 / 0 | 6 / 0 |
| G | 221 | 63 | 46 | 234 / 74 / 57 | 45 / 51 | 51 / 60 | 46 / 57 | 46 / 57 |
| H | 75 | 22 | 3 | 104 / 36 / 0 | 3 / 0 | 3 / 0 | 3 / 0 | 3 / 0 |
| Total | 2,163 | 629 | 148 | 2,363 / 720 / 204 | 61 / 96 | 265 / 286 | 239 / 268 | 68 / 115 |

The local reading (01, 04, 05) handled: A 8, C 11, D 0, F 9, G 48, H 3; the not-02 reading: A 99, C 11, D 80, F 9, G 48, H 3.
By four-quarter year (golden): patients 695, 737, 731; deaths 204, 212, 213; confirmable 54, 50, 44 (D 25, 28, 27; G 14, 17, 15).
The confirmable figures split into empty-bed waits (A 6, C 1, F 6, G 45, H 3) and own-placement waits (A 2, C 4, D 80, G 1).
Every device alone moves exactly its measured deltas per trust per figure (asserted); every figure but B's and E's 3c sits under
three or more devices; the necessity matrix holds (each device moves a figure at every trust it is planted at).

**Referee (exactly one).** The network's transfer audit: 3,797 transfers between trusts, local decision times, the referral's
patient key and the bureau's allocation and arrival times, all 36 months, no deaths, no levels, byte-clean. It is on the main path
for rung 3 and the decisive join (its rows in the window), and is the structural organ of DV8 and DV1 (its legacy rows). It covers
transfers only (36 per cent of long waits), so it hands over no column.

**Pair arithmetic (Part 0), planning weights 38 / 7 / 55, r = 5, 32 ask criteria at 1.72 points.** Cracker (files D):
recommendation 38, instruction-following 7, the chart's five parts and the structural zeros; mirror: r 5, instruction-following
7, one chart part, scored on whichever of the seven wrong readings of own care keeps it highest. With every device missed the
pair is **37.1**; every single catch and every double catch leaves it at 37.1. Named profiles, both top responses making the same
catches (asserted and printed by the generator): round 1's catches (its six stage-2 devices and the discharge-method fallback)
37.1; **round 2's catches, every device before loop 2, 38.8**; round 2's and DV9 40.5; round 2's and DV8 59.4; every device
78.3. Leaving one device out: DV1 38.8, DV8 40.5, DV4 or DV5 44.0, DV7 49.1, DV9 59.4, HZ2 61.2, DV2 62.9, HZ1 73.2, DV3 74.0. The
layer holds the pair at or under 40 while both top responses miss DV8 and DV9, and under 50 while they miss DV8 alone; a
response that catches every device and misses the call still keeps 56.6 (the planned or 04 reading, wrong at one trust's 3c),
because 3a and 3b carry no construction. Reachability (A1): 5 of 32 ask criteria are reachable from the landed call. The pass
condition rests on the ladder holding the field to at most one response on D, and on DV8 staying silent.

### Prompt (stage 2)

`prompt.md` written under guide-to-prompt after prompt-voice.md and prompt-economy.md. Opening move question-first (the last three
builds opened stakes-first, evidence-first and number-first); the role sits mid-paragraph; one belief clause (the chair, pointing at
E); the call is the context's last sentence ("Name the one trust the review should sit in."); the docx leads with the trust alone;
each later paragraph ties back to the call. No sentence fixes the basis, window, population or method (the remit carries all four),
no input file is named, and every figure is a count under one convention sentence. voice-check.py 119: 226 words, 20.5 words a
sentence, context 34.1 per cent, longest paragraph 77 words, a sentence under eight words, one rounding carrier with its convention,
no "because", no flagged carrier, no shared six-word run. Institutional nouns for H20: acute trusts, the regional health board, the
board funding one twelve-month engagement, quality surveillance.

### Assertion plan (54 at stage 2, as revised by hardening loops 1 and 2; generator then independent verifier)

1. Rung 0 leader E, margin at least 1.20 (1.27).
2. Rung 1 leader C, margin at least 1.20 (8.5); the mixed reading (network for trusts with no level-3 beds) also names C (1.62).
3. Rung 2 leader G, margin at least 1.20 (7.5).
4. Rung 3 leader A, margin at least 1.20 (1.37).
5. Rung 4 leader D, margin at least 1.50 (1.80).
6. Five distinct leaders.
7. D 4th on rung 0, behind by at least 1.5x.
8. D never first on rungs 1 to 3, and second on at most one of them by at least 1.20x (rung 3, 1.37x).
9. Dominance against G, E, A and C, both ratios and the product, and against A at rung 3 on the share each keeps at rung 4.
10. Eighteen grid cells by name; exactly the census, own-unit, own-placement cell names D.
11. Own and network scope equal per trust at the census basis with admissions ignored.
12. Inside every long wait in the window the own unit admitted only the trust's own planned transfers (D, type 03) or bureau
    transfers (A types 02 and 03, C and G type 02); on the record own placements are coded 03 or 04 and bureau transfers 01, 02
    or 03; every bureau transfer is in the audit at its bed time and no own placement is; any admission and own placement part
    only at A, C and G.
13. Every own-placement wait holds an own placement inside its first four hours.
14. Every own-empty wait holds the empty staffed bed from decision to assignment; no capacity wait shows an empty staffed bed at
    minute grain or at hourly snapshots.
15. No long wait at a trust without level-3 beds overlaps any unit's empty staffed bed or planned own placement.
16. No wait in the window within five minutes of four hours.
17. No long-wait death between day 25 and day 35 after its decision.
18. No long-wait death straddles either window edge.
19. No patient with two long waits in the window, and none in the record after identity resolution outside the device rows.
20. Register static through the window; physical beds equal staffed beds at the four units.
21. Name convergence across four quarters, eight quarters and the record.
22. D leads the decisive construction in each four-quarter year by at least 1.2x.
23. Long-wait mortality between 25 and 33 per cent at every trust.
24. Corpus: the filed rule reproduces 34 of 34 exactly.
25. Corpus: 216 rules swept; every rival misses at least 4 reviews; every one-directional rival misses the total by at least 10 per
    cent; the nearest rival named.
26. Corpus blindness: zero corpus long waits with the reviewed unit full at any hour; the five rung constructions identical on every
    review.
27. Twin pair identical on the listed columns, 24 against 11, reproduced by the rule, refused by the receipt clock.
28. Retry log: seven zero reviews, zero under the rule, retries zero, rivals non-zero on at least four.
29. Clean-data test on the 08:00 return (hourly replacement): answer D, naive E, D differs from E.
30. Capacity report deleted: nothing moves.
31. Lens swap: no referral-log column or pair reproduces any trust's confirmable count within 8 per cent.
32. No shipped artifact orders the trusts on the decision question.
33. Golden record targets (24 figures, 3 totals) and the three yearly series.
34. Zero device and hazard rows inside the main call's declared population, per device.
35. Main call identical with every device mishandled; D leads on the record window with devices handled or not.
36. Device deltas per trust per figure as designed; at least three devices on every figure but B's and E's 3c.
37. No-cancel over every subset of mishandlings, per trust and per total.
38. No census-path subset lands on the golden at A, C, D or G.
39. Stops per ask (natural, each device alone, each over-correction) off the golden at every trust touched.
40. Hygiene battery on the natural path clean: unique keys, no exact duplicates, no unmatched joins, no fan-out.
41. Lazy sweep lands on stop 1 for 3a, 3b and 3c.
42. Necessity matrix: every device moves at least one figure at every trust it is planted at.
43. Pair simulation at or under 40 with the battery applied; every single and double catch at or under 40; the triple catch reported.
44. Referee byte-clean and covering transfers only.
45. Span: 3a at least 10 files, 3b 12, 3c 15, each at least 10 columns, counted from the golden's code path.
46. Each device's two organs in two files, neither a main-path document, and no file holding two primaries' documentary organs.
47. Device vocabulary absent from every main-path document and from the prompt (grep).
48. Pack gates: at least 10 files, 3 formats, a file of 25,000 rows or more, two distractors named in metadata.json.
49. Single-statement rule for every pin.
50. Every graded figure an integer.
51. Invented names clear of real organisations and places (H21) and of every card's invented names.
52. E leads both deaths after a long wait and deaths before a bed was assigned.
53. Two consecutive builds byte-identical.
54. Distractors unused on the golden's code path.
55. Hardening loop 1: the clock-change nights carry exactly the designed waits (11 and 9) and none of them is long in elapsed
    time; the repeat patients are exactly the designed pairs (two at each trust but D); DV5 and DV7 have zero rows in the main
    population, their measured deltas and two organs each.
56. Hardening loop 2, the rung: no unit-feed column separates own from bureau placements inside the window's long waits (the
    pair (03, 01) and the referral ward REC carry both); every own placement there is coded as a transfer in, and a planned bureau
    transfer sits inside every A death-wait the unit filled; own placements and planned bureau transfers were referred after the
    waiting patient, unplanned ones before (record).
57. Hardening loop 2, the readings on the window: referral and audit D 27 over G 15; local and 04 G 15 over A 2; planned, not 02,
    queue and any admission A 37 over D 27; the referral and audit readings equal per trust and on the record.
58. DV8: every legacy transfer's stay begins at its arrival and every platform transfer's at its allocation; no held bed spans
    08:00; exactly 28 legacy transfers read past four hours at the arrival and 35 held beds sit inside designed capacity waits.
59. DV9: ten long waits under temporary keys the links never resolve, each death recorded only as the temporary-key spell's
    discharge method, the referral-to-episode join still matching.
60. Each of the seven wrong readings of own care: no subset of mishandlings lands its 3c on the golden where the reading differs.
61. Pair simulation with the best of the seven mirrors: 37.1 with every device missed, every single catch at or under 40,
    round 2's own profile at or under 40; one primary's documentary organ per file (DV8 the CCRS specification, DV9 the extract
    specification, DV3 the board paper).

### Realism debts (stated)

1. **Timing segregation.** No long wait overlaps another unit's empty staffed bed or planned admission, and the trusts without
   level-3 beds wait only in evenings and nights. Forced by the own-against-network convergence. Mitigation: weekday daytime elective
   lists and weekend gatekeeping are ordinary patterns, and evenings and nights are when a network runs out of beds.
2. **D's planned admissions through every one of its long waits.** Forced by the stump sentence approved at checkpoint A and by
   D's 1.80x margin from fourth on the raw count. Mitigation: a surgical centre running two elective lists a weekday that need
   level-3 recovery admits three or four planned patients a weekday, and at weekends, with no lists, its ward patients reach a bed
   inside four hours.
3. **Instant bed assignment in the unit feed.** Forced by the census-grain convergence. Mitigation: bed-management systems date a
   stay from the bed's assignment, and the field guide says so.
4. **G holds staffed beds empty through whole weekend-afternoon waits.** Forced by the census-reading convergence. Mitigation: a
   weekend rule admitting after a consultant review is real practice, recorded in a short G unit note with no numbers.
5. **Long-wait mortality near 29 per cent**, plausible for deteriorating ward patients referred for level 3.
6. **The corpus networks never ran a unit full in five years.** Forced by L1. Mitigation: those networks carry more level-3 beds per
   head; nothing in the pack states it, the records show it.
7. **Most devices in nine legacy months.** A platform migration concentrates exactly this mess, and the clean months after it are
   what a cutover looks like. DV5 and DV7 sit outside them, on two clock-change nights and in year 2.
8. **Bureau transfers into A's full unit through 78 per cent of its long waits in the placement year** (117 admissions; 35 of A's
   44 deaths follow such a wait). Forced by the rung-3 margin (A 37 over D 27, 1.37x) and by A's carried advantage over D on the
   raw count. Mitigation: A is the regional centre with 30 staffed beds, and a regional centre's freed beds go to the patients the
   bureau has waiting from trusts without level-3 units, who were referred earlier.
9. **Twenty waits on two clock-change nights, 17 of them followed by a death within 30 days** (85 per cent, against 28 to 30 per
   cent among long waits), and empty staffed beds at D, F and H through those nights. Forced by DV5's weight on 3b and 3c.
   Mitigation: 20 waits in three years, outside the remit when read correctly, with nothing in the pack pointing at the nights.
10. **Fourteen patients discharged from critical care inside four days, referred again 8 to 13 days after the first decision and
    dead inside 21 days of it.** Forced by DV7 moving 3b. Mitigation: early readmission to critical care is a recognised
    high-mortality group; the pairs fall at seven trusts, two each.
11. **Stennock's elective centre exists only in the codes.** Its planned surgical patients are referred from theatre recovery
    (`REC`) at a second Stennock hospital no document names, and admitted to STN-ACC as planned transfers in (03, source 01), 2,973
    referrals over the record. Forced by the loop-2 rung: a document naming the centre would point at the join. Mitigation:
    multi-site trusts with a separate elective hospital are common, a move between two hospitals is coded as a transfer under the
    critical care data set's admission types, and the referral log's referring trust says whose patient it is.
12. **Planned post-operative transfers into Ristenholm's unit on list-day evenings, one inside every A death-wait the unit filled**
    (66 in the placement year, booked by the bureau for patients of trusts without level-3 beds and referred after A's waiting
    patient). Forced by the planned and queue readings naming A. Mitigation: the regional centre takes post-operative patients
    that smaller hospitals cannot hold overnight, booked through the bureau.
13. **Ten never-identified patients whose deaths sit only on a spell ending in death.** Forced by DV9. Mitigation: unidentified
    emergency patients registered under temporary numbers are routine, and death registrations link only through a verified NHS
    number.
14. **The CCRS bed list dated a transfer's row from the patient's arrival, the platform from the allocation.** Forced by DV8.
    Mitigation: bed-management systems differ on exactly this, and the export specification says what the old list held. The ten
    patients of trusts with full level-3 units who waited 3h10 to 3h52 for another trust's bed on winter evenings (two at each of
    A, C, D, F and G) are ordinary network practice: a full unit's patient goes where the bureau finds a bed.

### Stopping rule (written before any round)

- At ceiling: two consecutive rounds (in-house or portal) in which a response files D at 27 by the allocation route, or one round in
  which both top responses file D. The ladder is then a computation; re-root at stage 1.
- One more repair is licensed by a round whose top responses stop at G, C, A or E while the pair clears 40 through the asks: harden
  the device layer (supplemental-stumping Part 10), not the ladder.
- A response filing D without reading D's stays (by resemblance or by chance) is a shortcut to find and close before anything else.
- State after round 1 (2026-10-09): one round in which a response filed D at 27 by the allocation route, read straight off the
  methodology sentence; loop 1 makes that reading name A. A second consecutive round with a response on D by the placement route
  puts the ladder at ceiling.
- State after round 2 (2026-10-09): the second consecutive round with a response on D by the placement route (own placement read
  as admission type 04, transfers coded 02 set aside). Read literally, the first line above now calls for a re-root at stage 1. The
  coordinator ordered hardening loop 2 on this architecture (loop 2 of at most 3), so loop 2 makes the round-2 route itself
  complete and land on G, and makes every other code reading land on A or G, rather than re-rooting; this conflict is flagged in
  the loop-2 hand-back. The next round decides: a response on D by any route in round 3 is the ceiling without appeal, and the
  architecture is then re-rooted with this card's driver moved into its lineage.

### Hardening loop 2 (2026-10-09): the design on paper

Brief: round 2 (plain, proxy 82.3, call landed) "kept only own-unit admissions coded admission_type 04 (planned
local) during each wait and dropped the type 02 transfers in as bureau-allocated beds", so rung 3 (A at about 37) was
seen and declined with one row filter, and every workbook figure came back exact: its trace executes each filed device
rule in turn (UTC, decision level, key links, pilot copies, elapsed time, one patient once, register dates). Loop 2
repairs both halves and moves no graded figure: the rungs keep 56, 34, 15, 37 and 27, the placement year 731 / 213 /
44, the record 2,163 / 629 / 148.

**Main ladder: the admission type stops standing in for who placed the patient** (stumping Part 10 escalation 2, the
discriminator behind a join; measured trap #5, the population a flag suggests, with #6 behind it).

1. Stennock's planned surgery runs at its elective centre, a second Stennock hospital with no level-3 beds. Every
   planned post-operative admission to STN-ACC is a planned transfer in (`admission_type` 03, source location 01),
   referred by Stennock from the centre's theatre recovery (referral log: STN, `REC`, level 3), given the bed 10 to 90
   minutes after the referral, and absent from the bureau's audit, which lists transfers between trusts. Inside every
   D long wait the planned transfer was referred after the waiting patient: D put its own elective patient ahead.
2. Through Ristenholm's long waits the bureau's placements become, on every death-wait and on half the survivors,
   planned post-operative transfers in (03, source 01) booked for patients of trusts without level-3 beds, referred
   from their recovery after Ristenholm's waiting patient and given the next bed that freed on a weekday evening; the
   rest stay unplanned transfers (02) referred earlier. Every one is in the audit with its `bed_confirmed_at`.
3. No unit-feed column separates them: 03 and source 01 carry D's own patients and the bureau's alike. The admitted
   patient's referring trust does, and for transfers between trusts the audit agrees (C1, asserted).

Readings of "an admission the trust placed itself" on the latest four quarters (deaths): the referring trust, or the
audit: D 27 over G 15 (golden); by type, local (01, 04, 05) or 04 alone: G 15 over A 2, D 0; by type, planned (03,
04, 05) or "not 02": A 37 over D 27; any admission: A 37 over D 27; queue order (an admission referred after the
waiting patient is the unit's choice): A 37 over D 27. Every code reading and the queue reading land on A or G; only
the join from the unit's admission to the admitted patient's referral names D. Round 2's own step ("type 02 out, 04
in") now completes and files G at 15.

**Ask layer: two silent primaries; the executed ones become hazards** (supplemental-stumping Parts 4 and 5).

- **DV8 (primary on 3a; hazard on 3b and 3c; D8)**, the legacy bed list dated a stay from the minute the patient was
  placed in the bed, where the platform dates it from the assignment. For a transfer between trusts the bureau
  allocated the bed (`bed_confirmed_at`) and it stood empty until the patient arrived, so on the shipped stays a legacy
  transfer's wait ends at the arrival (3a and 3b up at B, E and H, where allocation waits of 3h10 to 3h52 read past
  four hours) and the legacy census shows the held bed as an empty staffed bed inside the receiving trust's capacity
  wait (3c up at A, C, F and G). Organs: the transfer audit (each legacy transfer's stay begins at `arrived_at`, each
  platform transfer's at `bed_confirmed_at`) and the CCRS specification ("from the time the patient was placed in the
  bed"). A trust moving its own patient between its sites assigns the bed on arrival, so no Stennock row is held.
  Silent: the 08:00 returns are computed from the same feed and agree with the shipped census, no held bed spans 08:00,
  every other legacy transfer's wait plus transit stays under four hours, and no held bed overlaps an own-trust wait
  except the designed ones. Over-correction stop: every legacy stay moved back by the audit's median transit.
- **DV9 (primary on 3b; D4)**, temporary identities never merged: the ten old DV2a rows become legacy ED referrals
  inside the remit whose temporary key the links file never resolves. The patient died in hospital within 30 days,
  so the death is in the episode extract only as a spell under the temporary key ending in death (discharge method
  4), with no date of death: 3b down one at every trust (three at E), 3c down one at D and G. Organs: the episode
  extract (discharge method and date) and the extract specification's temporary-registration line. Over-correction
  stop: deaths from the discharge method for everyone (post-discharge deaths lost, the corpus's refused rival). DV2
  keeps its repeat-wait rows and moves 3a only.
- DV3 stays the 3c primary (its documentary organ is the only one in the board paper). DV6 leaves the device layer:
  with own placement read from the referring trust it moves nothing, and the legacy coding it carried is now part of
  the type readings the construction layer prices. DV5 and DV7 become hazards. Primaries' documentary organs: DV8 the
  CCRS specification, DV9 the extract specification, DV3 the board paper, one each.

**Stump sentence (loop 2).** A competent solver counts each trust's deaths after a wait of more than four hours for a
level-3 bed, sets aside the trusts holding no level-3 beds, rebuilds every unit's census from its stays, writes the
remit's methodology sentence as its test, declines the any-admission reading by setting aside every transfer into a
unit as the bed bureau's placement by its admission type, and files G at 15 over A's 2; the step that lands it there
is reading the admission type as who placed the patient: every planned transfer into D's unit during D's long waits
was D's own post-operative patient, referred by D from its elective centre (the referral log's referring trust; none is
in the bureau's audit), which makes D's 27 the largest number the review can confirm, while the planned transfers into
A's unit were patients of trusts without level-3 beds on beds the bureau booked, so a solver who keeps planned
admissions as the trust's choice instead files A at 37.

**Targets asserted at the rebuild** (measured values replace the paper ones in the tables above): rungs and the
record unchanged; the two type readings and the queue reading name G and A as above; no unit-feed column separates
own from bureau placements inside long waits in the window (both directions); DV8 and DV9 each move only the trusts
listed, with zero rows in the main call's population; the no-cancel enumeration over every subset of the ten devices;
the pair simulation with mirrors on the census, any-admission and both type readings.

**Measured at the rebuild, and what moved from the paper.** Every target above holds (150 assertions, `## Build record`). Five
changes were forced while cutting the pack:

1. DV8 at every trust. On paper DV8 moved 3a and 3b only at B, E and H, so round 2's own catches with DV8 and DV9 missed left
   3a right at five trusts and the pair at 47.4. Two dead near misses now sit at each of A, C, D, F and G as well (a patient of
   a trust whose own unit was full, transferred out on a winter evening, the own unit held full with no admission until the
   arrival), so the device moves 3a and 3b at every trust (+2 there; its 3b move never meets DV9's minus one on a cancellation)
   and the round-2 profile falls to 38.8.
2. The DV2 over-correction. With DV2a's deaths gone to DV9, dropping temporary-key referrals landed exactly on the golden (the
   repeat patient's second wait survives under the verified key); the stop is now every referral of a merged identity dropped,
   2,154 / 629 / 148.
3. Legacy transit room. A held bed may not span 08:00 or run into a wait at the receiving trust, so a background legacy
   transfer allocated where the arrival would cross either goes to one of the unit's own patients instead (`sim.py`), and four
   designed E waits allocated just before a Brackenford morning vacancy may run into the vacancy's opening (an empty bed beside an
   empty bed; `legacy.py`).
4. A survivor's planned bureau transfer that no list-day evening can carry falls back to an unplanned one: 31 of A's 82 survivor
   waits with a transfer carry a planned one in the placement year, not half (no graded figure reads a survivor's transfer type).
5. The two network-scope cells with admissions read any way lead with E by 1.19x and 1.21x over A (A's evening planned waits
   moved the world's random stream); asserted as two wrong trusts with D at least 1.2x behind, like the 08:00, own, any cell.

### Hardening loop 3 (2026-10-10): the design on paper

Brief: round 3 (plain, proxy 72.6, call landed) "at path step 6 read the remit's methodology sentence (a trust's own beds
and staff are its own care) as a work order: it counted a freed bed given to a patient the trust chose itself (its own
planned recovery admissions) and set aside every bureau-allocated transfer by joining to the transfer audit, which reached
D at 27 without stopping at G (rung 2) or A (rung 3)". Path depth: rung 4 reached straight from rung 0. Every refinement of
who placed an admitted patient is that sentence executed, so loop 3 moves the decisive step off the admissions altogether
and leaves the solver's own test intact: written exactly as round 3 wrote it, the test still completes and now files G.

**The new rung: a bed the feed shows taken is not always a patient in a bed** (measured trap #13, validates on one
population, applies to another: established, decided 3 of 64 client tasks, 2 under 0.50; #7, the ready-made measure, behind
it, as at rung 1). The unit feed dates a stay from the minute the bed was assigned (field guide, unchanged). On every row a
solver can check, the assigned minute is the occupied minute: the 08:00 returns are computed from the feed and agree with
the census to the bed, a local admission arrives as its bed is assigned, and a bureau transfer's held bed belongs to the
bureau, which the audit dates. From the platform's go-live (2 April 2024) Stennock's unit assigns a bed to an elective
centre patient at its morning bed meeting when one frees, and holds it for the patient, who is still in theatre at the
elective centre and arrives in the afternoon. Through every platform-era Stennock long wait one or two such beds stand
assigned and empty: booked between 08:10 and a quarter of an hour before the waiting patient's decision, their patients
leaving the centre's recovery 10 minutes or more after that decision and arriving inside the first four hours of the wait.
Read by assignment, Stennock's unit is full at every minute of every wait and admits no one during it; read for who was in
the bed, it held a staffed bed empty for its own planned patient, which the methodology note makes Stennock's own care,
exactly as Prideswick's beds held empty until a consultant review are Prideswick's.

1. **Evidence, one new operating file.** The regional data service's theatre extract for the patients in the referral
   record or the unit feed (`rds_theatre_cases_2023-2026.parquet`, its fields in the RDS specification beside the episode
   extract's): one row per theatre case, provider, site, case date, urgency, procedure, into theatre, out of theatre,
   left recovery and the recovery destination. Every unit stay that came from theatre has its case; for every one but the
   booked holds the patient left recovery before the bed was assigned (a local admission minutes before, a bureau transfer
   before its departure from the sending trust). The booked holds are the only own-trust stays assigned before the patient
   left recovery. Nothing in any document says when a bed is assigned to a planned patient or that a bed can be held.
2. **The legacy months are untouched.** The legacy bed list dates a row from the patient's placement, and Stennock's legacy
   allocation waits keep their planned admissions inside the wait (each the next bed that freed), so the record's 3c and
   every device delta stand. Booked patients carry no referral (the platform books a planned bed in its bed module; the
   elective centre's other patients keep their recovery referrals), so no referral, return or outcome time disagrees with a
   stay: no negative interval, no stay before its referral, no bed held across 08:00.
3. **The graded figures do not move.** Rungs 56, 34, 15, 37, 27; the placement year 731 / 213 / 44; the record
   2,163 / 629 / 148 and its eight rows: the platform-era Stennock waits change how they are Stennock's, not whether.

**Readings of an empty staffed bed on the latest four quarters (deaths).** By assignment (the feed's census), with own
placement read any way (round 3's own test, the type readings, the queue): G 15 over A 2, D 0. By assignment with any
admission: A 37 over G 17, D 0. By the patient in the bed with every held bed empty (the bureau's included, from the audit's
arrival): A 37 over D 27. By the patient in the bed with the bureau's held beds taken and the trust's own holds empty, plus
own placement (the golden): D 27 over G 15. Only the last names D.

**Ladder (loop 3).**

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deaths within 30 days after a wait of more than four hours for a level-3 bed, by referring trust, latest four quarters | E, 56 over A 44 (1.27x) | The remit's own population counted exactly as filed; the corpus reproduces all 34 reviews | The unit register: E holds no level-3 beds |
| 1 | Waits set aside on days the own 08:00 return showed no empty staffed bed | C, 34 over G 4 (8.50x) | A capacity check on the network's published return | The census from C's stays: C full at every hour of every C long wait |
| 2 | An empty staffed bed in the own unit's census at some minute of the wait | G, 15 over A 2 (7.50x) | The exact occupancy through each wait, beside the trust's own empty beds | The theatre extract against Stennock's stays: through every Stennock wait its unit held beds assigned to its own elective patients still in theatre, 27 deaths against 15 |
| 3 | An empty bed or any admission to the own unit during the wait | A, 37 over G 17 (2.18x) | The methodology sentence read literally: a bed given to another patient | The audit and the field guide's `bed_confirmed_at`: every admission inside an A wait was a bureau placement |
| 4 | **Decisive:** a staffed bed in the own unit with no patient in it and not held by the bureau, at some minute of the wait, or an admission the trust placed itself | **D, 27 over G 15 (1.80x)** | | |

Round 3's test (rung 3 with the bureau's placements set aside) is the grid cell "assignment census, own placement": it lands
back on G at 15, the stump. The position rule holds: D 4th on rung 0, 0 on rungs 1 to 3 (last of the four trusts holding
level-3 beds), never second; thinnest rung margin 1.27x (rung 0).

**Dominance.** G carries no raw advantage into rung 4 (21 deaths against D's 27); on the decisive axis D keeps 27 of 27 and
G 15 of 21, 1.80x. Against A, the rung-3 leader: A carries 37 against D's 0 by assignment; on the decisive axis A keeps 2 of
44 (0.045) and D 27 of 27, an edge of 22x; against the physical, every-hold cell (A 37 over D 27, 1.37x) the edge is 18.5x
against the 1.64x required.

**Survival properties.** 1 Written nowhere: the field guide says only that a stay is dated from the bed's assignment; no
document says a planned bed is assigned early or held. 2 The corpus is blind: no reviewed unit was ever full, so held beds
never decided a review. 3 No arithmetic symptom: the census reproduces every 08:00 return, every referral's outcome time
matches its stay, no stay starts before its referral, no booked bed spans 08:00, and the theatre extract's other cases all
end before their stays begin. 4 Not a row predicate: a stay, the same patient's theatre case and another patient's wait at
the same unit. 5 The solver's own step completes and returns G. 6 The holds run through all 27 platform months and Stennock's long waits, deaths
and 08:00 returns run level through the go-live; the legacy months carry the same own care as an admission during the wait.
7 Delete the theatre extract and the holds cannot be seen, which is the rung's evidence, not a wrong number. **Accepted weak
points, both on the route the rung is built to be found by:** a solver who joins the theatre extract to the stays, or who
asks why Stennock's elective centre stays begin before its lists end, finds the holds, and the methodology note then hands
over the attribution; and round 3's own test counts Stennock's legacy-month waits (each with a planned admission inside)
and none after the go-live, so a solver who tabulates Stennock's own care by year sees it stop at the platform's go-live and
can ask why. Option rejected for the second: making Stennock's legacy waits capacity would strip the ask layer's devices from
Stennock's confirmable column (DV9, DV1oc, DV4 and HZ2 all move it through allocation waits) and move the record's 3c.

**Gate G, restated.** Litmus no: every figure is correct, the assignment minute is the feed's documented meaning and the
theatre times are the theatre system's. Mechanism decomposition_attribution (each trust's long-wait deaths split into
network capacity and its own care). surface_read_dependency no; stumping_family analytical_non_defect; sole_data_defect no.
Clean-data test: an hourly return computed from the feed still shows Stennock full (the bed is assigned); an instrument
that recorded the patient in the bed would show Stennock's held beds, Ristenholm's bureau holds and Prideswick's empty beds
alike (the physical, every-hold cell names A), so the attribution of each hold is still the solver's work. The decision's
own quantity, a bed the trust kept for itself, is a relation between a bed assignment, the assigned patient's theatre record
and who made the assignment, which no field carries.

**Stump sentence (loop 3).** A competent solver counts each trust's deaths after a wait of more than four hours for a
level-3 bed, sets aside the trusts holding no level-3 beds, rebuilds every unit's census from its stays, writes the remit's
methodology sentence as its test (an empty staffed bed, or a freed bed given to a patient the trust placed itself, the
bureau's transfers set aside) and files Prideswick at 15 over Ristenholm's 2; the step that lands it there is reading the
unit feed's bed assignment as the patient in the bed: through every Stennock long wait since the platform went live its
unit held one or two staffed beds assigned at the morning bed meeting to its own elective centre patients, who the theatre
extract shows had not left recovery when the waiting patient's decision was made, so Stennock kept beds empty for
its own planned surgery while its emergency patient waited, 27 deaths, the largest number the review can confirm.

**Stopping rule.** Loop 3 is the last loop on this architecture. A solver that files D in round 4 retires the build. A solver
that files G at 15, A at 37 or any other trust sends it to the determinism judge.

### Pack plan (provisional; dataset-generation builds against it)

Spine `critical_care_referrals_202307_202606.csv` (about 42,000 referrals, both levels); unit stays (parquet); daily 08:00 bed returns
(csv); admitted patient care episodes with the linked date of death (about 900,000 rows, parquet); unit register (effective-dated,
csv); the network's monthly capacity report (xlsx, context artifact); the remit (docx, governing); the field guide (pdf); the
programme's review log (xlsx) with its review records (sqlite); the device organs (legacy referral events, legacy referral form guide,
legacy export specification, legacy unit export note, temporary-identity merges, platform go-live notice, 2024 consolidation paper);
the transfer audit (csv, referee); a short G unit note; correspondence (eml); the provenance note. Distractor candidates: the level-2
units' daily returns and an ambulance handover extract. Stage 3 consolidates into the 10-to-19 band in the organisations' own idiom,
without merging any device's two organs into one file and without one file holding two primaries' documentary organs.

## Build record

Stage 3, 2026-10-09, rebuilt in hardening loops 1 and 2 the same day. Generator `task119/generator/`, seed 119: `build.py` (entry
point), `plan.py` (designed waits and device rows), `world.py` (day roles and every designed wait on the clock), `sim.py` (each
unit's events into stays), `people.py` (referrals, deaths, episodes), `legacy.py` (migrated rows, level entries, parallel-run
copies, bed-episode rows, transfer audit, key links), `extracts.py` (capacity report, ambulance and level-2 extracts),
`corpus.py` (review records), `docs.py` and `texts.py` (papers), `golden.py` (every figure from the shipped files), `checks.py`
(assertions). `verify.py` is the independent verifier (DuckDB joins, pandas time-zone conversion, numpy census over islands of
contiguous rows; imports nothing from the generator). `reproduce.py` builds twice and compares bytes.

**Gates (loop 2).** Generator: 150 assertions, 0 failed, on the build into the task folder. Verifier: 32 claims, 0 failed, on
`task119/target` (it now re-dates legacy transfers from the audit in DuckDB, takes an unresolved key's death from its spell ending
in death, and recomputes the four admission-type readings). Two consecutive builds into the scratchpad byte-identical (20 files: 19
under `target/` plus `metadata.json`, file times equal), and the task folder's pack byte-identical to them. Input gates: 19 files;
8 formats (csv, docx, eml, parquet, pdf, sqlite, txt, xlsx); referral log 33,739 rows (2,973 of them Stennock's referrals from
theatre recovery), episode extract 88,342 rows; review database a SQLite file with five tables; distractors
`level2_unit_bed_return_0800_2025-26.csv` and `ambulance_handovers_hourly_2025-26.csv`, named in `metadata.json` only and each
asserted unused (every figure unchanged with it deleted); `metadata.json` clean. Loop 1's gates were 137 assertions and 24 claims
on the same pack shape.

**The answer.** STN (D), Stennock University Hospitals NHS Foundation Trust: 27 deaths a year of review could confirm;
runner-up PRW (G) 15; gap 12 deaths; margin 1.80x. D ranks 4th on the natural pipeline, 2.07x behind E.

| Rung | Leader | Runner-up | Margin |
|---|---|---|---|
| 0 raw | LAT (E) 56 | RIS (A) 44 | 1.27x |
| 1 08:00 | BRK (C) 34 | PRW (G) 4 | 8.50x |
| 2 census | PRW (G) 15 | RIS (A) 2 | 7.50x |
| 3 any admission | RIS (A) 37 | STN (D) 27 | 1.37x |
| 4 decisive | STN (D) 27 | PRW (G) 15 | 1.80x |

Position: D 4th on rung 0, last of the four trusts holding level-3 beds on rungs 1 and 2, second on rung 3 (1.37x behind A);
thinnest margin 1.273 (rung 0). Dominance over A at rung 3: shares 1.000 against 0.054, edge 18.5 against 1.64 required. Grid:
eighteen cells, each naming the trust the design table names, and only census, own unit, own placement naming D. Killing facts
(verifier): LAT holds no level-3 beds; RIS-ACC reported no empty bed at 08:00 on any of the 135 days RIS referrals waited;
BRK-ACC full at every moment of all 118 BRK long waits; the full units admitted other patients through 78 per cent of RIS's long
waits and every STN wait; all 117 admissions inside RIS long waits were patients referred by another trust and listed in the
bureau's transfer audit at their bed time (66 coded 03, 51 coded 02); STN-ACC admitted patients Stennock referred itself, coded
03 and absent from the audit, through all 92 STN long waits; the type readings name PRW 15 over RIS 2 (local, 04) and RIS 37 over
STN 27 (planned, not 02).
Clean-data test (hourly return): rung names G 15, call D, naive E. Lens swap: no referral-log column or pair reproduces the
confirmable counts.

**The asks (record, July 2023 to June 2026; patients / deaths / confirmable).** A 438 / 126 / 8; B 104 / 29 / 0;
C 351 / 104 / 5; D 275 / 80 / 80; E 559 / 165 / 0; F 140 / 40 / 6; G 221 / 63 / 46; H 75 / 22 / 3; total 2,163 / 629 / 148.
By four-quarter year: 695 / 204 / 54, 737 / 212 / 50, 731 / 213 / 44 (D 25, 28, 27; G 14, 17, 15). Confirmable split:
empty-bed waits A 6, C 1, F 6, G 45, H 3; own-placement waits A 2, C 4, D 80, G 1. Unchanged by loop 1.

**Device layer (measured, loop 2).** The ask ledger carries the measured tables: natural path 2,363 / 720 / 204; every
device's deltas per trust per figure; the census, any-admission, planned, queue, local and 04 paths with devices handled and
not; the over-correction stops; the pair profiles. Each device alone moves its measured deltas exactly (asserted per trust per
figure); no subset of the 1,023 lands a touched figure or total on its golden; for each of the seven wrong readings no subset lands
its 3c on the golden where the reading differs; zero device and hazard rows inside the main call's declared population. DV8: 974
legacy transfers begin at the arrival, 2,823 platform transfers at the allocation, no held bed spans 08:00, 28 legacy transfers
read past four hours at the arrival, 35 held beds inside designed capacity waits. DV9: 10 unresolved temporary keys, each death on
its spell ending in death. Clock-change nights: 11 waits on 30 March 2024 and 9 on 29 March 2025, none long in elapsed time.
Repeat patients: 14 designed among 46 people with two long waits in the record. Hygiene battery clean on the natural path. Pair
simulation 37.1 with every device missed; every single and double catch 37.1; round 2's own profile 38.8. Referee: 3,797
transfers, 36 per cent of long waits. Spans from the golden's code path: 3a 9 files / 20 columns, 3b 10 / 24, 3c 13 / 30.

**The corpus.** The filed rule reproduces 34 of 34 (412 confirmed, 41 attempts, 7 zero reviews retried on a doubled sample
and zero again). 216 rules swept; the nearest rival (requested level 3) misses 19 reviews; every one-directional rival
misses the 412 total by 14.8 per cent or more (deaths before assignment dropped: 351). Every widening rival is non-zero on
all seven zero reviews. Blind: no reviewed unit was ever full, so every construction equals the rule on every review.
Twin pair Ormerleby 2022 and Selarwell 2023: district general, 14 beds, 1,184 referrals, screen 71, 8.6 beds occupied at
08:00, 96 deaths; confirmed 24 and 11; the receipt clock gives both 24. Feningby 2021 counts three post-discharge deaths
inside 30 days and not five between days 31 and 60.

**Deviations from stage 2, each forced at build.**

1. Names, after the H21 sweep (a 5,617-place GB gazetteer, an NHS organisation list and every other card's invented names;
   edit distance two or containment fails): region Wenmarsh; A Ristenholm (RIS), B Tannerby (TAN), C Brackenford (BRK),
   D Stennock (STN), E Lathingbury (LAT), F Ellerdyke (ELL), G Prideswick (PRW), H Pellowham (PEL); provider Thornleholm
   Clinical Review LLP; corpus regions Haskminster, Isterdale, Tevermouth, Morrowcombe; the twin pair Ormerleby and
   Selarwell (were Kellow Bridge and Sandmere); the window case Feningby (was Fenwold).
2. Nineteen files. One CCRS migration specification carries DV4's documentary organ with the DV1 and HZ1 hazards' (one
   primary per file holds); the go-live notice, the network manager's notes and G's weekend rule sit in the correspondence;
   provenance and dictionary are one field guide. Spans fall from the planned 10 / 12 / 15 to 8 / 9 / 12, at the skill floor.
3. HZ2 at D is four duplicated deaths, not two: with two, {DV2, DV4, HZ2} cancelled on the 3c total. HZ2 counts per
   referral row on 3b and 3c alike, so the stage-3 natural path was 2,208 / 669 / 161, not 2,208 / 667 / 157.
4. The capacity report covers April 2024 to June 2026, not 36 months (`## Tried and rejected`).
5. C runs 16 staffed beds day and night, so one staffed figure per day holds and physical equals staffed.
6. The 08:00 return is read on the decision's date; no long wait has its decision between midnight and 08:00, so the
   latest-return reading converges.
7. Hardening loop 1 (rung 3 and the re-rooted device layer): bureau transfers placed into A's, C's and G's full units
   inside their capacity waits (`plan.TX_INSIDE`), the transfer audit's `bed_confirmed_at` defined in the field guide, the
   structural reading moved into the grid; DV5 on the two spring clock-change nights (stays and receipts kept clear of the
   nonexistent local hour, the capacity report computed in elapsed time); DV6 by recoding every CCRS-era unplanned admission 01;
   DV7 as lethal repeat pairs at seven trusts. The pack grew from the stage-3 build with the transfers, the clock-change waits,
   the repeat patients and the background that moved with the world's random stream (referral log 30,259 to 30,785 rows,
   transfer audit 3,419 to 3,852); every golden figure is unchanged, and rungs 0 to 2 and the call keep their figures.
8. Hardening loop 2 (the admission type no longer stands in for who placed the patient, and the new device layer): Stennock's
   planned admissions arrive from its elective centre as planned transfers in (03, source 01) with a Stennock referral from
   theatre recovery (`people.py`, `sim.py`); the bureau's placements inside A's death-waits are planned transfers in (03) referred
   after A's patient on list-day evenings (`plan.TX_PLANNED_LETTERS`, `world.py`); the legacy bed list dates every transfer
   between trusts from the arrival (`legacy.py`, transit 40 to 110 minutes, the designed near misses in `plan.DV8_NEAR`); ten
   legacy identities are never merged (`plan.GOLDEN_DEVICE_ROWS` DV9); the CCRS specification's bed-management section and the
   episode specification's admission methods (81) carry the new organs, the field guide defines `REC`, and the board paper says
   "Transfers between trusts". The referral log grew to 33,739 rows and the audit fell to 3,797 (the bureau transfers that moved
   with the random stream); every golden figure, every rung and the call keep their figures.

9. Hardening loop 3 (the decisive rung reads the patient in the bed): from the platform's go-live each Stennock allocation
   wait's planned admissions become morning bookings (`world.try_alloc`, `plan.BOOK_LEAD`, `EC_TRANSIT`, `HOLD_CLEAR`; booking
   times on their own stream, `rng("booked")`, so the world's stream is untouched): the bed is assigned between 08:10 and a
   quarter of an hour before the waiting patient's decision and held (`hold_until`) until the patient, whose booking referral
   comes from the surgical day unit (`SDU`, `rng("ec_booked")`), leaves the treatment centre's recovery inside the wait. The
   legacy months keep their in-wait admissions. New operating file `rds_theatre_cases_2023-2026.parquet` (`theatre.py`): one case
   per unit stay from theatre, the patient leaving recovery before the bed was assigned (own trust) or before the transfer
   departed (bureau), except the 301 holds; 2,744 ward cases of referred patients as texture; elective cases inside list
   hours. The RDS specification gains the companion extract's fields; the field guide's file table lists it. Legacy transit:
   an allocation at exactly 08:00 now counts as spanning the return (`sim.legacy_transit_room`, `legacy.finalize`), which the
   rebuild exposed. Every graded figure, every rung figure but rung 3's runner-up (G 17, D 0) and the call keep their values.

**Gates (loop 3, 2026-10-10).** Generator: 175 assertions, 0 failed (25 new or rewritten: the ladder with rung 3 at A 37 over
G 17 and D 0; the thirty-cell grid; round 3's own test naming G 15 over A 2; dominance on the every-hold reading, edge 18.5
against 1.64; the hold checks: 301 holds, only at STN-ACC, platform months, assigned 08:21 at the earliest on weekdays, none
across 08:00, every one of the 206 platform-era Stennock long waits beside a hold whose patient left recovery 10 to 215 minutes
after the decision, no other wait meeting one, by assignment Stennock full and admitting no one through each; the theatre
extract: 5,282 critical care cases for 5,282 stays from theatre, none missing, none late outside the holds; every hold's bed
requested from SDU and assigned within 15 minutes; the record's 3c under round 3's test keeps Stennock's legacy months only,
20 against 80). Verifier: 33 claims, 0 failed (new DuckDB tables `st2_own` and `st2_all` re-time the holds from the theatre
extract). Two scratch builds byte-identical (21 files) and the task folder's pack identical to them. Input gates: 20 files
(over the 19-file target, a stated debt: the theatre extract is the rung's only evidence and no organ file could carry it);
8 formats; referral log 33,719 rows, episode extract 88,202, theatre extract 8,026; distractors unchanged. Natural path (every
device mishandled) 2,368 / 720 / 205 (was 2,363 / 720 / 204, background moved with the booking events); every device alone
moves exactly its ledgered deltas; no-cancel, over-correction stops, battery, organs and spans green; pair simulation 37.1
with nine mirrors (round 3's own test and the every-hold reading added), worst single and double catch 37.1, round 2's profile
38.8, round 3's catches (UTC, decision level, key links, pilot copies, one patient once, CCRS beds from the audit, the
discharge-method fallback) 38.8.

## Write-up and ship checks

Stage 3 close, 2026-10-09, redone in hardening loop 1. `generator/golden.py` run as a script reads only `target/` and writes the
three deliverables into `golden/`: `external_review_placement_2027-28.docx` (the board paper: the call, 27, Prideswick at 15, a
gap of 12; why each other trust is not it, Ristenholm's transfers included; the record totals; the chart),
`review_placement_workings.xlsx` (Record by trust, Placement year, Notes) and `review_placement_by_trust.png` (deaths inside the
remit by trust, July 2025 to June 2026, the confirmable part shaded, ordered by it, the gap bracketed, titled on Stennock). It
prints the critical components and the five rungs, and asserts the paper's worded rules on the record: all 92 of Stennock's
long waits in the placement year are allocation waits and fall on weekdays, no Stennock weekend referral waited more than four
hours, no other trust's long wait holds an own placement outside an empty-bed wait, Ristenholm's any-admission count (37) is
its empty-bed deaths plus its bureau-transfer deaths and exceeds Stennock's, every bed Ristenholm's full unit gave away during
one of its long waits went to a patient referred by a trust holding no level-3 beds on that date, every Brackenford long wait
began at 18:00 or later with its unit full, and Brackenford's 08:00 return showed an empty staffed bed on most mornings (206 of
365).

- **Figures.** Every figure in `submission.md` and the goldens recomputes from the engine the checks use: rungs 56, 34, 15, 37,
  27; the placement year 731 / 213 / 44; the record 2,163 / 629 / 148 with the eight trust rows as the build record states;
  Stennock 25, 28, 27 and Prideswick 14, 17, 15 by year. The chart's zero-confirmable trusts tie, so block 4 states the order
  only for the three with a confirmable part. Loop 1 moved no graded figure: blocks 2 and 4 are unchanged, block 1's Ristenholm
  clause now names the bureau's transfers, step 5 cites `interhospital_transfer_audit_202307_202606.csv` and the field guide's
  `bed_confirmed_at`, and step 7 adds elapsed time across the March clock changes and transfers by the referring trust.
- **Golden realism.** Board-paper identifying block, a title stating the finding, lopsided sections, the decision in prose and
  the trusts in a table with a source line, one footnote on the death linkage and its completeness, page footer; the Ristenholm
  paragraph and table reason (35 after waits through which its full unit took transfers the bureau placed, 7 with the unit full
  and no admission, 2 beside an empty staffed bed) added in loop 1; workbook with named sheets, frozen panes, set widths, number
  formats, a tied total row and a Notes sheet whose definitions now carry the bureau's allocation, waits in elapsed time and one
  patient per person; chart with a deliberate two-tone palette, direct labels and the gap bracket. Figures frozen before the
  pass; the goldens regenerated from the final pack are byte-identical to the shipped ones.
- **Container.** `golden.py` scrubs both OOXML files through `writers.scrub_ooxml` (producer "Quality surveillance, Wenmarsh
  Regional Health Board", stamped 2 October 2026, fixed entry times) and sets the file times; the H1 audit reads `golden/` and
  `target/` clean.
- **Reduce-house-fixes.** H4: `golden/` holds exactly the three named files, one `submission.md` and one `prompt.md` in the
  tree. H6: the worded rules above are back-tested in code, the bureau rule included. H8: every file, column and clause the
  write-up and paper cite resolves (WRHB/26/097 sections 3, 4 and 5; the transfer audit and its field-guide entry). H3: the
  Ristenholm sentence counts deaths and the waits behind them in one population ("the waits behind 35 of its 44 deaths").
- **Pack rebuild.** 137 of 137 assertions, 24 of 24 verifier claims, two scratch builds byte-identical to each other and to the
  task folder's pack.
- **Surface screen** (`guard.py surface`, loop 1): no byte-identical file, same-seed table, shared name or prompt wording
  promoted; the five promoted pairs are the stage-3 ones on the mechanism layer only (task118 back to back on gap and decision
  type; task25, task26, task28 and task38 on gap, pattern and decision type), which no rebuild moves, each answered by a
  differentiation line on the card. People in the cut pack: the six drawn personas and nobody else.
- **Heart check** (`guard.py heart task119`): see `## Guard`; the card's stump is the loop-1 sentence.
- **Stage 3 re-run after loop 1 (2026-10-09).** `golden.py` re-run from the shipped pack: every figure unchanged (rungs 56,
  34, 15, 37, 27; placement year 731 / 213 / 44; record 2,163 / 629 / 148), workbook and chart byte-identical. H3 found one
  count-word defect in the paper's table: Prideswick's row split its 21 deaths as 15 and 4 and dropped the 2 after waits
  through which its full unit took bureau transfers; the row now reads 15, 2 and 4, emitted from the same counts, and
  `figures()` asserts the parts tie to the row for Prideswick and Ristenholm. H6 tightened two worded rules to the sentence
  as written: no Stennock weekend referral at any level waited more than four hours (open waits included), and Stennock
  leads with Prideswick second in each four-quarter year. Only the docx moved (one table cell); the regenerated golden
  equals a scratch build byte for byte, the H1 audit reads `golden/` and `target/` clean, the verifier passes 24 of 24 and
  `submission.md` needed no change. Surface screen: the same five mechanism-layer pairs, nothing on the surface layer.
  Heart: **WARN** (exit 0) on repeat.gate_g and repeat.decision, nearest heart text 0.05 (task89 lineage), nearest driver
  0.06; card fields agree with the submission and the pack, `guard.py validate` 119 cards, 0 invalid.
- **Hardening loop 2 (2026-10-09).** No graded figure moved: rungs 56, 34, 15, 37, 27; placement year 731 / 213 / 44; record
  2,163 / 629 / 148 and its eight rows; Stennock 25, 28, 27 and Prideswick 14, 17, 15 by year. `submission.md` (after
  `submission-writeup`): block 1's Ristenholm clause says the beds went to patients referred by other trusts, planned transfers
  included; component 2 and step 5 say Stennock's in-wait admissions were planned patients it referred itself from theatre
  recovery (coded 03, none in the audit), step 5 now joins each admission to the admitted patient's referral; step 7 adds a
  CCRS-era transfer's bed from the audit's `bed_confirmed_at` and an unresolved key's death from its spell ending in death.
  Block 4 is unchanged. Goldens (`golden-realism`, figures frozen first): the paper's Stennock paragraphs now say the unit
  assigned beds to Stennock's own planned surgical patients referred from theatre recovery and that the feed codes them as
  planned transfers in although none passed through the bureau; the Ristenholm paragraph says many of the patients were planned
  transfers, all referred by trusts without level 3 beds; the table's Stennock reason and the workbook's notes (could have
  confirmed, CCRS conformance, long wait, death, own placement "whatever the admission type") follow. `figures()` asserts the new
  sentences on the record: every admission inside a Stennock long wait coded 03, referred by Stennock from REC and absent from
  the audit; a planned transfer inside more than half (in fact all 35) of the Ristenholm death-waits its unit filled. H1: the
  container audit reads `golden/` and `target/` clean. H3: each new sentence's count word, comparator and population read
  against the code that asserts it. H4 and H11: three files in `golden/`, one `submission.md` and one `prompt.md` in the tree.
  H8: every cited file, field and section resolves (the CCRS specification's "placed in the bed", the extract specification's
  discharge method). No em dash in any file written. The goldens regenerated from the final pack are byte-identical to the
  shipped ones; the verifier passes 32 of 32.
- **Surface screen** (`guard.py surface`, loop 2): the same five mechanism-layer pairs as stage 3 (task118 back to back on gap
  and decision type; task25, task26, task28 and task38 on gap, pattern and decision type), nothing on the surface layer; people
  in the cut pack the six drawn personas.
- **Stage 3 re-run after loop 2 (2026-10-09).** `golden.py` re-run from the shipped pack into the scratchpad: every figure
  unchanged (rungs 56, 34, 15, 37, 27; placement year 731 / 213 / 44; record 2,163 / 629 / 148 and its eight rows) and all
  three goldens byte-identical to `golden/`. Pack: two scratch builds at 150 of 150 assertions, byte-identical to each other
  and to `target/` and `metadata.json`; the verifier passes 32 of 32 on `target/`. `submission.md` (after `submission-writeup`): one incidental figure cut, step 1's
  731 patients, which no component or ask owes; blocks 1, 2 and 4 unchanged. `golden-realism`: the paper, workbook and chart
  read again cold, nothing moved. Reduce-house-fixes: H1 audit clean on `golden/` (band August to November 2026) and
  `target/` (to the as-of date); H4 and H11 three files in `golden/`, one `submission.md` and one `prompt.md` in the tree;
  H8 every file the write-up names is in `target/` and sections 2 to 5 of WRHB/26/097, the field guide's `bed_confirmed_at`,
  `beds_open` and `REC` and the CCRS specification's "placed in the bed" resolve; H6 the paper's worded rules are asserted in
  `figures()` and passed on the re-run. Leak check REVIEW (the same five sweep-4 documents, answered below), surface screen
  the same five mechanism-layer pairs and nothing on the surface layer, heart **WARN** (exit 0) on repeat.gate_g and
  repeat.decision, nearest heart text 0.05 (task89 lineage), nearest driver 0.06; the card's answer, answer source, spine rows
  (33,739), deliverables and opening move already agree with the submission and the pack; `guard.py validate` 119 cards, 0
  invalid.

- **Hardening loop 3 (2026-10-10).** No graded figure moved: rungs 56, 34, 15, 37, 27 (rung 3's runner-up is now G at 17,
  D 0); placement year 731 / 213 / 44; record 2,163 / 629 / 148 and its eight rows; Stennock 25, 28, 27 and Prideswick 14, 17, 15
  by year. `submission.md` (after `submission-writeup`): component 2 now says Stennock's unit kept staffed beds assigned to its
  own planned surgical patients who were still in theatre; step 4 reads the census by assignment, step 5 states the
  own-placement rule and keeps the bureau's placements out, step 6 matches each Stennock stay to its case in
  `rds_theatre_cases_2023-2026.parquet` (`left_recovery_at` after the decision) and ranks 27, 15, gap 12; step 7 repeats steps 1
  to 6. Blocks 1 and 4 unchanged. Goldens (`golden-realism`, figures frozen first): the paper's Stennock paragraphs say the
  feed counts a bed as taken from its assignment, that on each of the 92 waits one or two such beds had been assigned that
  morning to Stennock's own planned surgical patients, that none of them had left recovery at the Stennock Treatment Centre when
  the waiting patient's decision was made and each left during the wait, and that those staffed empty beds are Stennock's
  decision; the table's Stennock reason, the source lines (paper table and chart, transfer audit and theatre cases added; the
  chart's source line wrapped after the render showed it clipped) and the workbook's notes (could have confirmed, empty staffed
  bed, own placement, extract) follow. `figures()` asserts every new sentence on the record: all 92 Stennock waits beside a hold,
  one or two holds each, assigned the same day, the held patient leaving recovery inside the wait, no admission inside any
  Stennock wait, every hold's case at the Stennock Treatment Centre, no own placement inside any latest-year wait. Goldens
  regenerated twice byte-identical and equal to the shipped copies. Reduce-house-fixes: H1 the scrub audit clean on `golden/`
  (band August to November 2026) and `target/` (to the as-of date); H3 each new sentence's count word, population and
  comparator read against the assertion that backs it; H4 and H11 three files in `golden/`, one `submission.md` and one
  `prompt.md` in the tree; H8 every file, field and section the write-up and paper name resolves (the theatre extract and its
  `left_recovery_at`, WRHB/26/097 section 4); H9 the field guide's file table lists every shipped file, the new extract
  included, and `metadata.json` lists exactly the shipped files; H16 the theatre extract's latest date is 2 July 2026, before
  the 14 August extract; H21 the new site name passes the invented-name sweep. No em dash in any file written.
- **Surface screen** (`guard.py surface`, loop 3): the same five mechanism-layer pairs (task118 back to back; task25, task26,
  task28 and task38 on gap, pattern and decision type), nothing on the surface layer; people in the cut pack the six drawn
  personas.

- **Stage 3b re-run after loop 3 (2026-10-10).** Pack: two scratch builds at 175 of 175 assertions, byte-identical to each
  other and to `target/` and `metadata.json`; the verifier passes 33 of 33 on `target/`. `golden.py` from the shipped pack: every
  figure unchanged (rungs 56, 34, 15, 37, 27; placement year 731 / 213 / 44; record 2,163 / 629 / 148 and its eight rows; Stennock
  92 of 92 waits beside a hold). H3/H6 found one worded rule looser than the generator: the rule counts a held bed empty until the
  patient's `left_recovery_at`, and on 34 hold-wait pairs the patient was out of theatre and in recovery at the decision, so "still
  in theatre" was false as written. Component 2, the paper's table reason for Stennock, the workbook's "could have confirmed"
  definition, the card's `driver_concrete` and the stump sentence now say the patients had not left theatre recovery; the paper's
  prose already said so. Only the docx and xlsx moved; goldens regenerated twice byte-identical. Reduce-house-fixes: H1 audit clean
  on `golden/` (August to November 2026) and `target/` (to 2 October 2026); H4 and H11 three files in `golden/`, one
  `submission.md` and one `prompt.md`; H8 every file the write-up names is in `target/`; no em dash in any file written. Surface
  screen: the same five mechanism-layer pairs, nothing on the surface layer, personas the six drawn. Heart **WARN** (exit 0) on
  repeat.gate_g against task129 (decomposition_attribution in one of the last two builds; the Gate G label is the honest one for a
  split of each trust's deaths into network capacity and own care, and the driver texts sit at 0.05 or below), nearest heart text
  0.05 (task89 lineage); card answer, answer source, spine rows (33,719), deliverables and opening move agree with the submission
  and the pack; `guard.py validate` 126 cards, 0 invalid.

- **Stage 6, fix cycle 1 (2026-10-10), the judge's FIX_NOW findings** (`determinism_check_report.md`: DETERMINISTIC, FIX_NOW,
  Gate G line matching this note on all four fields). (1) CCU and SDU were undefined while the remit puts "patients referred
  from another critical care unit" out of scope: excluding CCU moves BRK and RIS (record 2,086 / 603 / 146, bars BRK 31, RIS 41),
  and Stennock carries 18 platform-era long waits referred from SDU, which a step-down reading would also drop. The field guide's
  `referred_from` line now says AMU, SAU, SDU (surgical day unit) and CCU (coronary care unit) are wards, as is each W code, a flat
  code list in `texts.GUIDE_FIELDS`; no figure moved (only the field guide's bytes and its metadata size changed). (2) The goldens
  and the write-up used legal trust titles no input carries; `golden.NAME` is now the short names the files use, and blocks 1, 3
  and 4 say Stennock (STN) and Prideswick (PRW); the card's `answer` follows. The chart was already on short names and is
  byte-unchanged. (3) `DISTRACTORS` adds the capacity report, the NRR log and the NRR database: each is off the golden's path
  (asserted: every rung and ask figure unchanged with it deleted), each looks relevant, and none answers the decision on the
  live trusts (the capacity report counts waits from receipt and ranks nothing; the NRR files cover four neighbouring
  networks), so none is a wrong-basis distractor and the section 8.3 inequalities do not apply. The capacity report stays this
  note's context artifact by type; since stage 2 it has been off the solution path (assertion 30), which is what the judge read.
  (4) `metadata.json` records the prompt shape as 07 (grid of cells), eight trusts by three record columns with totals plus the
  ranked chart. The card keeps `shape: other`, see `## Tried and rejected`. (5) Lens swap re-run on the loop-3 step and asserted
  in `checks.grid_checks`: the bed lens alone (every held bed read empty) names Ristenholm in both allocation readings (37), the
  placement lens alone names Prideswick (census/own/ignored and census/own/placed both G), and only the two together (a hold read
  empty when the trust that placed the patient is the referring trust) name Stennock; two lenses on two different entities'
  records, so the mechanism stays decomposition_attribution. The referral-log column test still passes. (6) The two thin forks
  (died before admission, last CCRS level) are closed by the remit's wording and the level-entry timing as the judge found;
  unchanged. (7) Realism notes kept as debts: typed workbook totals (see Tried and rejected), constant `beds_open`, RIS and STN
  at 100 per cent each morning, long waits in fixed windows, the remit-death gap at days 24 to 35 (axis 9's C1 closure), and the
  board paper's PDF date a week before the meeting that approved it (a paper is circulated before its meeting).
  Gates: two scratch builds at 179 of 179 assertions (175 plus the lens-swap line and three new distractor lines), byte-identical
  to each other, and the task build byte-identical to them; verifier 33 of 33 on `target/`; goldens regenerated twice
  byte-identical, every figure unchanged (rungs 56, 34, 15, 37, 27; placement year 213; record 2,163 / 629 / 148 and its eight
  rows; Stennock 27, Prideswick 15, gap 12). Reduce-house-fixes: H1 audit clean on `golden/` (August to November 2026) and
  `target/` (to 2 October 2026); H4 and H11 one `submission.md` and one `prompt.md`, no snapshot or backup; H8 every file the
  write-up names is in `target/`; H3 the renamed sentences read cleanly with the short names; no em dash. Golden-realism:
  presentation only (the workbook's name column narrowed to fit the short names). Surface screen: the same five mechanism-layer
  pairs, nothing on the surface layer, personas the six drawn. Heart **WARN** (exit 0), the same repeat.gate_g against task129.

- **Stage 3b re-run after fix cycle 1 (2026-10-10).** Pack: a scratch build at 179 of 179 assertions, byte-identical to
  `target/` and `metadata.json`; the verifier passes 33 of 33 on `target/`. `golden.py` from the shipped pack into the scratchpad:
  every figure unchanged (rungs 56, 34, 15, 37, 27; placement year 213; record 2,163 / 629 / 148 and its eight rows; Stennock 92 of
  92 waits beside a hold, 27, Prideswick 15, gap 12) and all three goldens byte-identical to `golden/`. `submission.md` (after
  `submission-writeup`): no change, every figure recomputes and the short names hold in blocks 1, 3 and 4. `golden-realism`: the
  paper, workbook and chart read again cold, no legal title left, nothing moved. Reduce-house-fixes: H1 audit clean on `golden/`
  and `target/`; H4 and H11 three files in `golden/`, one `submission.md` and one `prompt.md`, no backup or snapshot; H8 every file
  the write-up names is in `target/`; H9 `metadata.json` lists exactly the 20 shipped files and five distractors; no em dash.
  Leak check REVIEW (the same six lines, answered below), surface screen the same five mechanism-layer pairs and nothing on the
  surface layer, personas the six drawn, heart **WARN** (exit 0) on repeat.gate_g against task129, nearest heart text 0.05
  (task89 lineage); the card's answer, answer source, spine rows (33,719), deliverables and opening move agree; `guard.py
  validate` 126 cards, 0 invalid.

- **Stage 6, fix cycle 2 (2026-10-10), the pass 2 judge's FIX_NOW findings** (`determinism_check_report_pass2.md`:
  DETERMINISTIC, FIX_NOW, Gate G line matching this note on all four flags). (1) `submission.md` step 1 now states the remit's
  population the way `golden.py` applies it: level 3 referrals from a ward or the emergency department whose elapsed wait from
  `dta_at` to the bed's assignment, or to death before a bed was assigned, exceeded four hours; step 2 names the 20 deaths before a
  bed was assigned inside the 213 (recounted from the shipped log). The same convention is now pinned once in a filed document:
  the terms of reference's scope paragraph adds "A patient who died still waiting more than four hours after the decision to admit
  is inside the scope." (`texts.REMIT`), closing the died-before-admission fork both judges called thin (excluding them gives bars
  RIS 41, LAT 46, BRK 33, ELL 11, TAN 8, PEL 6 and a 2,113 / 579 record). (2) The 225-minute clamp: `people.short_wait` drew a
  lognormal and clipped it to [8, hi], piling 348 admitted waits on minute 225 (and the legacy BST draws on 170, which shows at
  230 on the raw UTC clock). Each attempt still takes one draw, and the tails now fold back inside the band (above hi to
  hi minus the excess modulo max(30, hi minus 100); below 8 to 16 minus the value), so the 190 to 225 minutes carry about 20
  waits a minute, falling to 0 to 4 a minute from 232. Asserted: no admitted wait minute from 8 to 239 holds more than twice
  its ten neighbours' median plus 10 (`checks.pack_checks`, assertion 180). Remit membership did not move; the folded draws shift
  the referral stream where a fold changes a clock-change retry, so background rows moved: episode extract 88,145 rows (was
  88,202), the capacity report's receipt-based screen (still reproduced by the verifier), two wrong grid cells by one death at E
  (held_all/network: E 39 and 53, D still at least 1.2x behind), DV8's over-correction stop (2,065 / 597 / 140) and the natural
  path's stop (2,366 / 720 / 205, TAN 132 / 39 / 0, PEL 105 / 34 / 0; `checks.NATURAL` and the verifier's `natural_total`
  updated). (3) The board paper's last line now reads "The board is asked to approve the changes in sections 1 and 2.", which
  agrees with its 14 November 2023 date and its future tense; the register still carries the effective dates. (4) The levels
  file is `ccrs_referral_levels_202307_202404.csv` in `build.F`, the golden's file map and the verifier; the field guide's file
  list and `metadata.json` follow from `F`, and step 7 cites the new name. (5) The optional field-guide sentence on bureau
  allocations is not added: the fork is closed by the field guide's `bed_confirmed_at`, ACCN/23/41 s.3, ToR s.2 and the network
  manager's rule, and the sentence would disarm the Ristenholm lure that carries rung 3. (6) Block 4's chart order now reads
  "then the five trusts with none in any order", so the generated rubric does not grade the golden's secondary sort. (7) Realism
  debts kept as stated: constant `beds_open`, RIS and STN full every morning, typed workbook totals (see `## Tried and rejected`).
  Gates: two scratch builds at 180 of 180 assertions, byte-identical (21 files, file times equal), and the task build at 180 of
  180 byte-identical to them; verifier 33 of 33 on `target/`; `golden.py` from the shipped pack: every figure unchanged (rungs 56,
  34, 15, 37, 27; placement year 213; record 2,163 / 629 / 148 and its eight rows; Stennock 27, Prideswick 15, gap 12) and all
  three goldens byte-identical to `golden/`, so `golden-realism` has nothing new to read. Reduce-house-fixes: H1 audit clean on
  `target/` (2021-01-01 to 2026-10-02) and `golden/` (August to November 2026); H4 and H11 three files in `golden/`, one
  `submission.md`, one `prompt.md`, no backup or snapshot; H8 every file the write-up names is in `target/` (the renamed levels
  file included); H9 `metadata.json` lists exactly the 20 shipped files and five distractors; no em dash. Leak check REVIEW, no
  LEAK, the same six lines (below). Surface screen the same five mechanism-layer pairs and nothing on the surface layer, personas
  the six drawn; heart **PASS** (exit 0).

- **Stage 3b re-run after fix cycle 2 (2026-10-10).** Pack: a scratch build at 180 of 180 assertions, byte-identical to
  `target/` and `metadata.json`; the verifier passes 33 of 33 on `target/`. `golden.py` from the shipped pack: every figure
  unchanged (rungs 56, 34, 15, 37, 27; placement year 731 / 213 / 44; record 2,163 / 629 / 148 and its eight rows; Stennock 92 of
  92 waits beside a hold, 27, Prideswick 15, gap 12). H6 found one worded rule looser than the generator: the workbook's
  "Inside the remit" line on Record by trust stopped at the assignment of a bed and left out the patient who died still waiting,
  which `golden.py`, step 1 and the terms of reference's scope paragraph all include; it now adds "or died still waiting more
  than four hours after it", the terms of reference's own wording. Only the xlsx moved (that one line); goldens regenerated twice
  byte-identical, docx and png byte-unchanged. `submission.md` (after `submission-writeup`): no change, every figure recomputes and
  block 4 follows the prompt's file and ask order. `golden-realism`: paper, workbook and chart read again cold, nothing else
  moved. Reduce-house-fixes: H1 audit clean on `golden/` (August to November 2026) and `target/` (2021-01-01 to 2026-10-02); H4
  and H11 three files in `golden/`, one `submission.md`, one `prompt.md`, no backup or snapshot; H8 all eleven files the write-up
  names are in `target/`; H9 `metadata.json` names all 20 shipped files; no em dash. Leak check REVIEW, no LEAK, the same six
  lines (below). Surface screen the same five mechanism-layer pairs and nothing on the surface layer, personas the six drawn;
  heart **PASS** (exit 0), nearest heart text 0.05 (task89 lineage), nearest driver 0.06; card answer, answer source, spine rows
  (33,719), deliverables and opening move agree; `guard.py validate` 126 cards, 0 invalid.

## Leak review

`leak.py task119 --asof 2026-10-02`, re-run in hardening loop 2 against the loop-2 stump sentence on the rebuilt pack
(2026-10-09): **REVIEW**, no LEAK; sweeps 1 to 3 and 5 to 11 clean, and sweep 4's five REVIEW lines are the same five
documents, now carrying "transfer" and "reading" among the generic terms. Each was read again in full after the loop-2 edits:
the CCRS specification's bed-management section says each legacy row ran "from the time the patient was placed in the bed"
(DV8's organ; it says nothing about who placed a patient or about planned admissions) and its section 2 now says only that
admissions are held in the bed-management feed; the board paper says "Transfers between trusts" go through the bureau, which is
true of every transfer in the audit and names no trust, code or wait; the extract specification gains admission method 81 in its
code list; the field guide defines `REC` as theatre recovery in the referral field's code note and gives the audit's coverage as
every transfer between trusts, field semantics that state no rule about own care and never say which admissions a trust placed.
The loop-1 reading of each document, below, still holds. Stage 3 re-run (2026-10-09, `--quiet`): **REVIEW**, no LEAK, the
same five sweep-4 lines on the same unchanged documents (board paper 5 terms, CCRS specification 7, extract specification 5,
terms of reference 7, field guide 13), each answered by its line below; sweeps 1 to 3 and 5 to 11 clean.

Hardening loop 3 (2026-10-10, against the loop-3 stump sentence on the rebuilt pack): **REVIEW**, no LEAK; sweeps 1 to 3 and 5
to 11 clean, sweep 4's five REVIEW lines the same five documents as before (board paper 4 terms, CCRS specification 8, RDS
specification 5, terms of reference 7, field guide 11). The RDS specification now carries the theatre extract's field list
(into theatre, out of theatre, left recovery, destination) and the field guide one file-table row for it: field semantics that
say nothing about when a unit assigns a bed, about planned patients' beds or about holding a bed. A hand sweep of every
document for the rung's own vocabulary (hold, held, book, assigned, bed meeting, reserve, Treatment Centre, theatre, recovery,
elective, arrive, empty) finds only "held" for where a record is stored, the field guide's existing `admitted_at` definition
("the minute the bed was assigned to the patient") and `outcome_at` line, the REC and source-location code lists, the episode
specification's admission methods, the terms of reference's scope sentence, and the network manager's existing belief about
Brackenford holding on to its beds; no document says a bed can be assigned ahead of a patient or names Stennock's lists.

Stage 3b re-run (2026-10-10, `--quiet`, pack byte-identical to loop 3): **REVIEW**, no LEAK; the same five sweep-4 lines at
the same term counts (board paper 4, CCRS specification 8, RDS specification 5, terms of reference 7, field guide 11), each
answered by its line below; sweeps 1 to 3 and 5 to 11 clean.

Stage 6 fix cycle 1 (2026-10-10, `--quiet`): **REVIEW**, no LEAK; sweeps 1, 2 and 5 to 11 clean; sweep 4's five lines the same
five documents (the field guide's new code list adds no stump term); one new sweep-3 line: the terms of reference carry 5 of 8
distinctive words of the shortened call ("place", "2027-28", "external review", "confirm", "deaths"), all the remit's own
title and judging vocabulary; it names no trust, code or count (Stennock and STN 0 times), so harmless.

Stage 3b re-run after fix cycle 1 (2026-10-10, `--quiet`, pack byte-identical): **REVIEW**, no LEAK; the same sweep-3 line on
the terms of reference and the same five sweep-4 lines at the same term counts (board paper 4, CCRS specification 8, RDS
specification 5, terms of reference 7, field guide 11), each answered by its line here; every other sweep clean.

Stage 6 fix cycle 2 (2026-10-10, `--asof 2026-10-02 --quiet`, rebuilt pack): **REVIEW**, no LEAK; the same sweep-3 line on the
terms of reference and the same five sweep-4 lines at the same term counts. The terms of reference's new scope sentence (a
patient who died still waiting more than four hours is inside the scope) names no trust, unit, bed state or order of admission;
the board paper's new closing line ("asked to approve the changes in sections 1 and 2") adds no term. Sweeps 1, 2 and 5 to 11
clean.

Stage 3b re-run after fix cycle 2 (2026-10-10, `--asof 2026-10-02 --quiet`, pack byte-identical, no document edited):
**REVIEW**, no LEAK; the same sweep-3 line on the terms of reference and the same five sweep-4 lines at the same term counts
(board paper 4, CCRS specification 8, RDS specification 5, terms of reference 7, field guide 11), each answered by its line
here; sweeps 1, 2 and 5 to 11 clean.

- `accn_board_paper_2023-11-21_level3_capacity.pdf`: the 2023 consolidation paper (Ellerdyke to level 2, Pellowham's
  winter beds, transfers continuing through the network's bed bureau); it says nothing about planned admissions, waits,
  own care or Stennock, and is the documentary organ of DV3 (DV6's until loop 2).
- `ccrs_migration_export_specification_rel2.3.pdf`: the legacy export's clock, level and bed-episode semantics and the
  bed-management feed's local time, the ask layer's organs; no sentence touches the platform era or the order in which a
  unit fills.
- `rds_apc_extract_specification.txt`: the episode extract's fields, its temporary-key linkage and the verified key, the
  organs of DV2, DV7 and (since loop 2) DV9; "admission" there is the hospital spell, not the unit.
- `review_terms_of_reference_2027-28.docx`: the remit's scope (transferred patients reviewed with the trust that referred
  them), judging rule and methodology note, the filed pins; it names no planned admission, occupancy, bureau or order of
  admission.
- `wenmarsh_acc_extract_field_guide.pdf`: the field definitions, where "planned" sits only in the admission_type code list
  beside the five other codes, "staffed" in beds_open and the bureau in the transfer audit's `bed_confirmed_at`; it states
  no rule about any of them and never says whose care a transfer is.

## Reopened

Retired on 2026-10-09 and reopened on 2026-10-10 under the author's single-solver rule: the build had used 2 of its three hardening loops, so it gets 1 more. One plain solver follows each loop; any answer other than the golden one sends it to the determinism judge and then to ship.

## Tried and rejected

- v1 (first draft, 2026-10-08, never registered): chains of spells linked across trusts on the regional patient key at a
  hand-over gap, each chain's death credited to the trust where it began against the first spell's modelled risk, pinned by a
  national retry log only the chain construction reproduced (34 of 34). Rejected at checkpoint A on 2026-10-09: recovering an
  unstored unit gated by reproducing published reviews repeats task109's and task120's architecture and cleared the guard only by
  relabelling Gate G to decomposition_attribution; the retry log refuted every trust-level screen (best 23 of 34), so the corpus
  showed a back-tester where to look; the risk-adjusted CUSUM and case-mix framing read as epidemiology; the asks answered other
  decisions (H18) and the chart named the construction.
- Stage 2, the draw's ask block (each trust's long waits, deaths after them and confirmable deaths on the latest four quarters):
  the census path and the decisive path agree on every trust but D, so the response that stops at G keeps 22 to 24 of the 24
  figures and the pair sits near 83, and the rows are the main call's own, so no device may sit on them. Moved to the whole record,
  where the legacy months carry the devices.
- Stage 2, the four-rung sketch (raw, morning return, census, allocation): under the 5-to-6-rung gate, and D third on rung 0 breaks
  the position rule. A structural rung (trusts holding level-3 beds, naming A) was added and D moved to fourth.
- Stage 2, device deltas of mixed sign with two devices on some figures: subsets of mishandlings cancelled back onto a golden, two
  catches recovered the small trusts' columns (pair up to 43.1), and on the census path G's and A's values landed on their goldens
  by one device offsetting the construction gap. Replaced by the parity rule (positive deltas even, the one negative device odd),
  three or more devices on every figure, DV1 at +4 on A's and G's confirmable column, and the grain hazard at +4 on G's (a
  confirmable total had cancelled, the identity device's minus 6 against the grain hazard's plus 6).
- Stage 2, D with three weekend capacity waits beside its allocation waits (24 of its 27 latest-year deaths confirmable): it
  contradicted the stump sentence approved at checkpoint A ("through every one of D's long waits D's unit was full only because it
  was admitting planned post-operative patients"). D's long waits now fall only on weekdays during the elective lists (27 of 27),
  and C's morning count rose to 34 so the 08:00-plus-allocation cells keep C ahead of D by 1.26x.
- Stage 3, the provisional names: Ostlebury, Brenhythe, Lessington, Gorrington, Pevenham, Kellow Bridge and Sandmere sat
  within two edits of, or contained, a real place (Owslebury, Hythe, Essington, Dorrington, Pavenham, Kelloe, Tangmere);
  Corringwell contained another card's Orrin and Fenwold sat two edits from another card's Keswold Road. Renamed from a
  screened pool.
- Stage 3, a 36-month capacity report: its legacy months recounted from the shipped log would miss the report by exactly
  the UTC-clock and parallel-run rows, verifying both repairs for free, and its 2023-24 occupancy rows would list the
  Ellerdyke and Pellowham level-3 units in a main-path paper. Cut to April 2024 onwards.
- Stage 3, HZ2 at two duplicated deaths for D: DV2 (-6), DV4 (+4) and HZ2 (+2) cancelled to zero on the confirmable total.
  Four duplicated deaths at D.
- Stage 3, separate organ files (legacy form guide, legacy export specification, legacy unit export note, go-live notice,
  G unit note, provenance note): 23 files, over the band. Consolidated to 19 with one primary's documentary organ per file.
- Stage 3, a CCRS specification stating every CCRS time as UTC with the unit rows inside it: it would read the legacy
  bed-management rows as UTC too and open a fork on the legacy census. The bed-management feed is described as local time.
- Stage 3, email sign-offs as a bare first name above the signature block: the persona sweep in `guard.py surface`
  read "Maria Maria", "Diana Diana", "Andrea Andrea" and "Sharon Sharon" across the blank line and blocked on
  people.inside. A `-- ` signature delimiter now separates the sign-off from the signature, in `docs.thread`.
- Stage 4, solver round 1 (plain), the five-rung ladder as built: the solver landed D at 27, G 15, gap 12 (proxy 83.8, main call landed by reading, 4 of 11 asks cracked, its confirmable column exact at 148). It went from rung 0 straight to rung 4 and never filed G: "A remit death is confirmable when the trust's own unit had a free bed during the wait, or admitted another patient (here always a planned surgical admission) during it." It built the allocation test as a work order from the remit's methodology sentence (own beds and staff are own care), not from the census, so the full-unit stop on rung 3 never happened.
- Stage 4 loop 1, the decisive rung built as a C1 convergence on code semantics (axis 19: during every long wait the only admissions to a referring trust's own unit were planned post-operative admissions from its own theatres, so any admission, any theatre admission and a planned own-theatre admission selected the same waits): the convergence turned the remit's methodology sentence into a work order with nothing behind it. The round-1 solver wrote its test straight from that sentence, "A remit death is confirmable when the trust's own unit had a free bed during the wait, or admitted another patient (here always a planned surgical admission) during it", never met the full-unit stop at rung 3 and filed D at 27; it died because the most literal operationalisation of "decisions about the use of its own beds" (any bed given to anyone while the patient waited) was exactly the decisive set, so no rung sat between the sentence and the answer.
- Stage 4 loop 1, DV7 as surviving repeat patients (two long waits under one verified key, 45 days or more apart, both survived): it moved only 3a, so 3b rested on the clock-change device alone, and a pair whose top responses computed waits in elapsed time with round 1's six catches measured 57.7 (61.2 with DV6 caught too). The pairs now die after the second wait, 8 to 13 days after the first, so a per-referral death count moves 3b at seven trusts and the same profiles measure 44.0 and 47.4.
- Stage 4 loop 1, a lethal repeat pair at Stennock (D) as well: every D long wait is confirmable, so the pair moved D's confirmable column by two and the confirmable total cancelled on three subsets ({DV2, HZ2}, {DV2, DV4, DV7}, {DV2, DV7, HZ2}: the identity device's minus six against plus six). No repeat pair at D; DV7 sits at the other seven trusts.
- Stage 4 loop 1, the rung-3 decoy as bureau transfers into Ristenholm's full unit (A at 37 on "any admission during the wait"): the second plain round (labelled round 2, plain; proxy 82.3, main call landed by reading, 4 of 11 asks cracked, confirmable total exact at 148) saw the rung and declined it in one column predicate: "Beds taken by inter-hospital transfers in (type 02) were excluded, because the network bed bureau allocates them and every such patient's decision to admit came before the waiting patient's." The `admission_type` code (02 against 04) on the unit stays partitions the bureau's placements from the trust's own without the interval join to the transfer audit, so the population gap at rung 3 to 4 is a row filter, and the solver's own confidence line names A at about 37 as the road not taken.
- Stage 4 loop 2 (opening line), axis 19 closed by C1 on the admission type (own placement read from the admitted patient's referring trust, from `admission_type` and from the bureau's audit selecting the same admissions in the window, asserted as a convergence): built to close a fork, it made the population gap at rung 3 to 4 a one-column filter, so the decline of rung 3 and the decisive set were the same row predicate. Round 2 plain wrote "Beds taken by inter-hospital transfers in (type 02) were excluded, because the network bed bureau allocates them and every such patient's decision to admit came before the waiting patient's" and kept "a planned local admission (type 04)", landing D at 27 without the interval join to the audit. The code has to disagree with who placed the patient in both directions, not be pinned louder.
- Stage 4 loop 2, DV8's near misses only at the trusts without level-3 beds (B, E, H): with round 2's own catches and DV8 and
  DV9 missed, 3a stayed right at A, C, D, F and G and the pair measured 47.4. Two dead near misses now sit at each trust holding a
  unit as well (a patient transferred out of a full unit), and the profile measures 38.8.
- Stage 4 loop 2, DV2's over-correction as "temporary-identity referrals dropped": once DV2a's deaths moved to DV9 it landed on
  the golden exactly (the repeat patient's second wait survives under the verified key). The stop is now every referral of a
  merged identity dropped (2,154 / 629 / 148).
- Stage 4 loop 2, a fixed 40-to-110-minute transit on every legacy transfer: background transfers allocated in the 70 minutes
  before 08:00, or just before a wait at the receiving trust, had no room for an arrival that neither spans 08:00 nor touches the
  wait, and four designed E waits ended ten minutes before a Brackenford morning vacancy. Such background beds go to the unit's
  own patients, and a held bed may run into a morning vacancy's opening.
- Stage 4 loop 2, the network-scope any-admission cell asserted as E at 1.2x or more: A's evening planned waits moved the
  world's random stream and the cell measured E 50 over A 42 (1.19x). Asserted as a two-wrong-trust cell with D at least 1.2x
  behind, the form the 08:00, own, any cell already had.
- Stage 4 loop 2, the decisive rung as the admitted patient's referring trust with `admission_type` disagreeing with placement in both directions (D's own planned transfers coded 03, the bureau's planned transfers into A coded 03): round 3 plain (proxy 72.6, main call landed by reading, 3 of 11 asks cracked) did the interval join and the audit join without effort and filed D at 27, G 15, gap 12: "A death counts if, during the wait, an open bed sat empty, or a freed bed went to a patient the trust itself chose: its own planned surgical or recovery admissions, or later own-trust patients. Beds the network bureau allocated to transfers from other trusts do not count." It read the methodology sentence as a work order and resolved who placed each patient from the audit (all 3,797 transfers matched), never stopping at G or A. Third consecutive round on D, the stopping rule's ceiling without appeal: the allocation driver is a computation for a plain solver, and the architecture is re-rooted at stage 1 with this card's driver moved into its lineage.
- 2026-10-09, retired: solved in all three solver rounds (83.8, 82.3, 72.6) after two hardening loops; the grader called a re-root under the design note's stopping rule. Under the author's standing rule a build still being solved after its hardening is retired rather than re-rooted, and the next note in its folder (AD11) takes the slot in a later wave.
- 2026-10-10, reopened: the retirement came before the three-loop limit, so the build continues under the single-solver rule with 1 hardening loop(s) left.
- Stage 4 loop 3 (opening line), the decisive rung as loop 2 built it (own placement read from the admitted patient's referring trust and the bureau's audit, the admission type disagreeing with placement in both directions), measured by round 3 plain (proxy 72.6, call landed): at path step 6 the solver wrote the methodology sentence as its test, "A death counts if, during the wait, an open bed sat empty, or a freed bed went to a patient the trust itself chose: its own planned surgical or recovery admissions, or later own-trust patients. Beds the network bureau allocated to transfers from other trusts do not count.", resolved who chose each patient from the audit (all 3,797 transfers matched on verified key and decision time) and filed D at 27 from rung 0, never stopping at G (rung 2) or A (rung 3). It died because the remit's sentence itself names whose decision a bed was, so every rung that only refines who placed the admitted patient is that sentence executed: the admission-type disagreement lengthened the step without leaving a place where the step completes on a wrong answer, and the audit join is schema-visible (key and decision time).
- Stage 6 fix cycle 1, workbook totals as SUM formulas (golden-realism): openpyxl writes a formula with no cached value, so any
  reader on cached values (pandas, the verifier, a grader) sees a blank total row; kept as typed totals computed from the rows.
- Stage 6 fix cycle 1, the card's shape moved from other to 07 to match metadata.json: task122, registered after this card, is
  shape 07, so the change would retro-fire the last-two shape ban on task122's card; the card keeps `other` and metadata.json
  names the shape.
- Stage 6 fix cycle 2, the wait spike check as each minute against the mean of the 100 to 239 band: the lognormal falls by
  a factor of four across that band, so the band mean flagged the natural mode (minute 102 at 87 against a mean of 31.7) and
  passed nothing; replaced by each minute against the median of its ten neighbours.
- Stage 6 fix cycle 2, the optional field-guide sentence that the bureau allocates a bed and the receiving unit does not choose
  the patient (judge finding 5): not added, because four shipped facts already close the Ristenholm reading and the sentence
  would disarm the rung-3 lure.
