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

A competent solver counts each trust's deaths after a wait of more than four hours for a level-3 bed, rebuilds every unit's
staffed occupancy hour by hour from its admission and discharge times, sets aside every wait that passed while the unit was
full, and sends the engagement to G, whose ward referrals waited while its own unit held empty staffed beds; the step that lands
it there is taking a full unit as the end of the question, so it never asks how the unit filled: through every one of D's long
waits D's unit was full only because it was admitting planned post-operative patients from D's own theatres, which makes those
waits D's own care and D's deaths after them the largest number the review can confirm.

## Decisive rung

**#17 Guesses an attribution the data can settle** (`_measured.md`): decided 2 of 64 client tasks, both under 0.50, status
emerging. The records leave out whose decision a long wait was. Every solver who takes up the remit's "own care" question
attributes a wait at a full unit to capacity, the sensible heuristic, and the signal that settles each wait exactly sits in the
unit's own admission record: through each of D's long waits D's unit, full at every hour, was taking planned post-operative
patients from D's theatres. It is reached behind **#11 Beats the headline trap, misses the quiet one** (4 of 64, 2 under 0.50,
established): the solver who distrusts the morning bed return and rebuilds the census hour by hour has beaten the visible trap
and stops at G. **#7 Uses the ready-made measure** (5 of 64, 2 under 0.50) carries the rung below, where the 08:00 return stands
in for occupancy during the wait. #17's recipe ships a settled case that only the signal reproduces; this build ships none,
because a case that refutes the capacity reading would be a corpus built to refute the naive read, and the remit's methodology
note pins the attribution instead.

**Corpus blind for a computable reason (L1).** In every corpus case every wait over four hours passed while the reviewed trust's
own unit held an empty staffed bed, because the four neighbouring networks never ran full from 2021 to 2025, so counting every
long wait, counting waits on days the morning return showed a free bed, counting waits in hours the census shows a free bed and
counting waits the trust's own care could have shortened return the same deaths for all 34 reviews. Under the naive path (count
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
  (census); the corpus back-test reproduces under every reading; no series steps; every total ties.
- Objective: the call separates each trust's waits held by network capacity (the artifact) from the waits its own care made (the
  real event), and places the one review there; no forecast enters the call.

## Ladder sketch

The draw's four-rung sketch, kept as the draw record. Stage 2 replaces it with the five-rung ladder under `## Stage 2: design`
(a structural rung added, D moved to fourth on rung 0, E killed by the unit register).

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
   sits fourth on rung 0 and third on rung 1.
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
5. **Own unit against whole network.** They agree at the census and allocation bases by construction (no long wait overlaps an hour
   when another unit held an empty staffed bed or admitted a planned case). At the 08:00 basis they differ, because C reports empty
   beds on mornings before other trusts' patients wait, and the network reading names C: a wrong cell, mapped to "its own beds".
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
| A | Ostlebury Teaching Hospitals NHS Foundation Trust | 30 staffed, regional centre | rung 1 decoy: most deaths among trusts holding level-3 beds, all capacity |
| B | Tannerby Hospital NHS Trust | none (level-2 unit) | texture |
| C | Brenhythe Hospitals NHS Foundation Trust | 14 staffed at night, 16 by day | rung 2 decoy: empty staffed beds at 08:00 on most weekday mornings, full by midday with emergencies |
| D | Stennock University Hospitals NHS Foundation Trust | 18 staffed, surgical centre | the answer: weekday elective lists send planned post-operative patients to its unit |
| E | Lessington Hospitals NHS Trust | none (level-2 unit) | rung 0 decoy: most deaths after long waits, all for other trusts' beds |
| F | Ellerdyke Hospitals NHS Trust | level 3 until 31 March 2024, level 2 since | carries the register-vintage device |
| G | Gorrington Hospitals NHS Foundation Trust | 12 staffed | rung 3 decoy: holds staffed beds empty through weekend afternoons until a consultant review |
| H | Pevenham Hospitals NHS Trust | 3 winter level-3 beds, 4 December 2023 to 31 March 2024 | carries the register-vintage device |

Timing, constructed and asserted: D's planned post-operative admissions arrive on weekdays from late morning to early evening, and
every D long wait falls inside those hours; C's long waits start in the evening after its unit fills; G's start on weekend
afternoons; A's, B's, E's, F's and H's long waits pass in evenings and nights with every unit full. No planned admission at any unit falls inside a long wait at any trust but D, no long wait
overlaps an hour when a unit other than its own held an empty staffed bed, and physical beds equal staffed beds at the four units
through the latest four quarters.

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
the decision to the assignment; its other 6 are capacity. A's 2 are waits with an hour of empty staffed bed at A. Long-wait
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
  (it is correct at its stated meaning) and replaced by an hourly return of occupancy against staffed beds; rung 2 then names G, the
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

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deaths within 30 days after a wait of more than four hours for a level-3 bed, by referring trust, latest four quarters | E, 56 over A 44 (1.27x) | The remit's own population counted exactly as filed, and the corpus reproduces all 34 reviews under it | The unit register: E holds no level-3 beds, so every E wait is for another trust's bed |
| 1 | The same count at the four trusts holding level-3 beds | A, 44 over C 35 (1.26x) | The own-care clause applied to the trust's structure: a trust whose patients can only wait for another trust's bed carries no waits of its own | A's 08:00 returns: A's unit reported no empty staffed bed on any day A's referrals waited |
| 2 | Waits set aside on days the trust's own 08:00 return showed no empty staffed bed | C, 34 over G 4 (8.5x) | A capacity check on the network's own published return, and C's waits survive it | The census rebuilt from C's stays: C's unit was full at every hour of every C long wait (it fills by midday, the waits start in the evening) |
| 3 | Waits set aside where the census shows the own unit full at every hour of the wait | G, 15 over A 2 (7.5x) | The exact occupancy through each wait, and G's waits passed beside its own empty staffed beds | Overtaken: D's stays during D's waits, planned post-operative admissions from D's theatres through every one of D's long waits (27 deaths) |
| 4 | **Decisive:** waits through which the referring trust's own unit held an empty staffed bed or admitted planned post-operative patients from the trust's own theatres | **D, 27 over G 15 (1.80x)** | | |

- A solver who does everything right up to rung 3 commits to G, which is the stump sentence's wrong answer.
- Every rung names a different trust (E, A, C, G, D), asserted by name after every parameter change.
- Rung 4 carries the stump (#17), behind #11 at rung 3 and #7 at rung 2.
- Gaps (stumping Part 1). Rung 0 to 1 opens the objective gap: deaths after a long wait are counted correctly and are not what the
  review is scored on. Rungs 1 to 3 move the moment at which the trust's capacity is read (its structure, its 08:00 state, its state
  at every hour of the wait), each a measurement-time refinement on correct records. Rung 3 to 4 opens the population gap: the waits
  the trust's own allocation made, a set that exists only as a relation to other patients' admissions. Decisive gap objective,
  reached through population, as the card files it.
- Survival properties of rung 4: written nowhere (the remit's note counts "decisions about the use of its own beds and staff" and
  names no planned admission, occupancy or order of admission); no sweepable corpus nominates it (the corpus is blind, below); no
  arithmetic symptom (every rung partitions the same deaths, every total ties, the census is exact); not a row predicate (an
  interval join from each wait to the referring trust's own unit's other admissions with their source); its class exists only as
  that join; no cutover date (D's practice is steady through 36 months; the only dated events, the 2024 platform cutover and
  consolidation, sit in the ask layer before the main window); survives deletion.
- Worth on the graded quantity: the leading count walks 56, 44, 34, 15, then 27. Rungs 1 to 3 each set waits aside and only rung 4
  adds waits back, so the decisive rung reverses the direction of every correction before it.

### Position table (asserted row by row)

| Rung | Leader | D's rank | D's count | D behind the leader by |
|---|---|---|---|---|
| 0 | E 56 | 4 of 8 | 27 | 2.07x |
| 1 | A 44 | 3 of 4 | 27 | 1.63x |
| 2 | C 34 | last | 0 | (at zero) |
| 3 | G 15 | last | 0 | (at zero) |
| 4 | D 27 | 1 | 27 | leads G by 1.80x |

D leads no intermediate rung and is second on none. No rung margin is under 1.15x; the thinnest is 1.26x at rung 1.

### Discriminator dominance

- The rung-3 decoy G carries no raw advantage into rung 4 (G 21 against D 27); D's decisive edge is 27 against 15, 1.80x.
- Against the raw leaders: E (56 against 27, 2.07x; attributable share 0 against D's 1.0), A (44, 1.63x; share 0.045, an edge of
  22x against the 1.96 required), C (35, 1.30x; share 0). Every product clears the 1.2 floor.

### Correction grid (asserted cell by cell)

Toggles: occupancy basis (none, 08:00 return, hourly census) by unit scope (own unit, whole network) by allocation (ignored, read),
twelve cells.

| Basis | Scope | Allocation | Names | Violates |
|---|---|---|---|---|
| none | own | ignored or read | A 44 over C 35 | own care at the hour (A's unit full through every A wait) |
| none | network | ignored or read | E 56 over A 44 | own care (E holds no level-3 beds) |
| 08:00 | own | ignored | C 34 over G 4 | own care at the hour of the wait (the 08:00 return describes the morning) |
| 08:00 | own | read | C 34 over D 27 (1.26x) | as above |
| 08:00 | network | ignored | C 34 over E 21 (1.62x) | "its own beds" |
| 08:00 | network | read | C 34 over D 27 (1.26x) | "its own beds" |
| census | own | ignored | G 15 over A 2 | the methodology note: D's decisions about the use of its own beds are D's own care |
| census | network | ignored | G 15 over A 2 | as above |
| census | own | read | **D 27 over G 15** | |
| census | network | read | **D 27 over G 15**, equal per trust to the own-unit cell (C1) | |

Only the two census-and-allocation cells name D. Partial applications: allocation read on the 08:00 basis names C; allocation
counted from any admission, any theatre admission or a planned admission inside the first four hours of the wait selects the same
waits (C1, asserted). Window cells: the latest eight quarters (D 55 over G 32) and the whole record (D 80 over G 46) name D, so no
window moves the name; the counts are pinned by the remit's placement clause (C4).

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
  structural, 08:00, census and decisive constructions therefore return the same deaths on all 34 (asserted twice: zero corpus long
  waits with the reviewed unit full at any hour, and every rung re-run review by review).
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
  August 2026.
- **Empirical, the corpus.** The yield equals the count (34 of 34).
- **Counter-pins: none.** The capacity report is labelled in-file (occupancy is the 08:00 return; referrals waiting over four hours
  are counted from receipt, the network's operational standard; it ranks no trust). The network manager's notes state facts (D's
  unit is full every morning) and beliefs (C could take its own patients), never a rule that a full unit is capacity. The stage-3
  sweep greps every shipped document for quotable sentences near capacity, full, own, planned, theatre and elective.

### Fork grid: the 22-axis closure table (determinism-check A.5)

| # | Axis | Reading chosen | Closure |
|---|---|---|---|
| 1 | Population | adult ward and ED referrals whose decision to admit was for a level-3 bed, waiting more than four hours to the bed's assignment; deaths within 30 days of the decision | filed (remit); C1: since 2 April 2024 the level on every referral is the decision's level; C2: the corpus confirms 34 of 34 |
| 2 | Unit of account | one patient, one death | C1: no patient holds two long waits in the latest four quarters, so patient and referral counts agree (asserted); in the record they differ only on device rows, where the ask's own word (patients) governs |
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
| 18 | Dimensional units | local time throughout the platform era and the unit feed | C1; the legacy UTC clock is ask hazard DV1 |
| 19 | Code semantics | the stay's source; own care counts planned post-operative admissions from the trust's own theatres | C1: during long waits in the window the only admissions to a referring trust's own unit are planned post-operative admissions from its own theatres, so any admission, any theatre admission and planned own-theatre admission select the same waits (asserted) |
| 20 | Integerisation | none | n/a |
| 21 | Scope of a stated clause | own care governs every wait; "own unit" scope | C1 at the census and allocation bases (no wait overlaps another unit's empty staffed bed or planned admission, asserted); at the 08:00 basis the network reading names C (C4, violates "its own beds") |
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
every rung below 4; 3a under the legacy level, the legacy clock or unmerged identities; 3b under those and a per-referral death
count; 3c under the census path (A, C, D, G), the current register (F, H), the legacy feed's bed episodes read as admissions (A, C,
G) and the devices on 3a and 3b.

### The ask ledger (supplemental-stumping Part 9)

**Main call's declared row population.** Files: the referral log (decisions 1 July 2025 to 30 June 2026, every trust and level),
the unit stays at A, C, D and G overlapping 1 June 2025 to 30 June 2026 (the census lead-in), the daily bed returns for that span,
the admitted patient care episodes of patients referred in the window (date of death), the unit register rows in force in the
window, the remit and the capacity report. Columns: referral `referral_id, patient_key, trust_code, dta_at, level, outcome,
outcome_at`; stays `unit_code, referral_id, patient_key, admitted_at, discharged_at, source`; returns `unit_code, return_date,
staffed_beds, occupied_0800`; episodes `patient_key, date_of_death`; register `unit_code, trust_code, care_level, valid_from,
valid_to`. **Every device and hazard row sits before 2 April 2024**, and the zero-counts inside the population are asserted per
device (DV1 July to October 2023; DV2, DV4 and HZ1 July 2023 to 1 April 2024; HZ2 19 February to 1 April 2024; DV3's register rows
valid to 31 March 2024). The call, its count, the runner-up and the gap are recomputed with every device mishandled and asserted
identical, and on the wrong window (the whole record) D leads with the devices handled or not.

| Ask | Figures, unit | Pool; construction layer | Device layer: primary; hazards | File path (causal) | Use, and how it enters the call (H18) |
|---|---|---|---|---|---|
| 1 Call furniture | the trust; its confirmable deaths in a year; the runner-up; the gap in deaths | A (the recommendation block); rung 4 | none (main path) | register, referral log, stays, returns, episodes, remit, field guide | component |
| 2 Chart | 5 parts | A (the call drawn); rung 4 | none | as ask 1 | component: the call at a glance |
| 3a Record: patients inside the remit | per trust, whole patients; total | B; none | **DV4** legacy level semantics (D3); hazards DV1 legacy clock (D8), DV2 temporary identities (D7) | referral log, stays, legacy referral events, legacy referral form guide, platform go-live notice, legacy export specification, identity merges, transfer audit (referee), remit, field guide: 10 files, 13 columns | qualifier: the record behind the forward call, which lets one year stand for 2027-28 |
| 3b Record: deaths among them | per trust, whole deaths; total | B; none | **DV2** temporary identities (D7); hazards DV1, DV4, HZ2 parallel-run copies on a per-referral count (D1) | 3a plus episodes and the episode field guide: 12 files | qualifier |
| 3c Record: deaths the reviewers could have confirmed | per trust, whole deaths; total | B, both layers; rung 4 (the census path misses A, C, D, G) | **DV3** register vintage (D2); hazards DV1, DV2, DV4, HZ1 legacy unit-feed grain (D6) | 3b plus register, returns, the 2024 consolidation paper, the legacy unit export note: 15 files, over 15 columns | qualifier |

Pool A is the call and its picture only (9 criteria, the cracker's by construction); every ask block is pool B. No primary family
repeats (D3, D7, D2); the hazards are D8, D6 and D1.

**Primaries, organs and root causes.** Two root causes, both in spring 2024: the referral platform replacing the legacy system on 2
April 2024 after a six-week parallel run (RC1), and the network's level-3 consolidation on 1 April 2024 (RC2). Each device's two
antidotes sit in different files, neither of them a document the main call reads, and no file carries the documentary organ of two
primaries.

- **DV4, legacy level semantics (primary on 3a).** On referrals migrated from the legacy system, `level` is the level the referring
  team requested; the platform has held the level the decision was made for since go-live. De-escalated legacy referrals (level 3
  requested, level 2 decided) read as level-3 waits on the natural path: 3a +2 at every trust, 3b +2, 3c +2 at D and H. Organs: the
  legacy referral events export (structural, the level changes before each legacy decision) and the legacy referral form guide
  ("level of care: the level requested by the referring team"). Over-correction stop: every legacy referral with a level change
  dropped.
- **DV2, temporary identities (primary on 3b).** A patient first registered under a temporary identity carries that key on the legacy
  referral; later episodes, and the date of death linked to them, sit under the verified key. The natural join finds the index episode
  and misses a death recorded later, and a later long wait under the verified key counts as a second patient: 3b minus 1 at every trust
  but E (minus 3), 3a +1 (E +2), 3c minus 1 at A, C, D, F, G and H. Organs: the temporary-identity merge file (structural) and the
  episode field guide's line on temporary registrations (documentary). Over-cleaning stop: every temporary-identity referral dropped
  (3a minus 21, 3b minus 6, 3c minus 2).
- **DV3, register vintage (primary on 3c).** F's unit held level-3 beds until 31 March 2024 and H ran three winter level-3 beds from 4
  December 2023 to 31 March 2024; the current register reads both as level-2 units throughout, which removes their own-care waits (F 6
  to 0, H 3 to 0). Organs: the register's effective dates (structural) and the 2024 consolidation paper (documentary).
  Over-correction stop: F and H read as level-3 units across the record (3c +5; the call, its count, the runner-up and the gap
  unchanged, asserted, since F's 13 and H's 7 latest-year deaths stay under G's 15).
- **DV1, legacy clock (hazard).** The legacy system held its timestamps in UTC; the platform and the unit feed are local. From July to
  October 2023 a legacy decision time sits an hour early against the unit's assignment time, so true waits of three to four hours
  read as long and some waits' intervals shift onto an empty bed or a planned admission: 3a +2 (A and E +4), 3b +2, 3c +2 at C, D and
  F, +4 at A and G. Organs: the legacy export specification (documentary) and the transfer audit's local decision times (structural,
  the referee). Over-correction stop: every legacy time shifted, winter months included (3a minus 9, 3b minus 3).
- **HZ1, legacy unit-feed grain (hazard).** Before April 2024 the unit feed held one row per bed episode, each carrying the stay's
  source, so a planned patient moved between beds during a ward patient's wait reads as a planned admission during it: 3c +2 at A
  and C, +4 at G, on the allocation reading (D's long waits are all allocation waits, so the hazard cannot move D). Organs: the
  legacy unit export note and the contiguous rows of one patient in one unit. Over-cleaning stop: stays of one patient within 24
  hours merged (3c minus 2).
- **HZ2, parallel-run copies (hazard).** From 19 February to 1 April 2024 wards entered referrals on both systems and the migration
  loaded the legacy copies beside the platform's, minutes apart and under two id schemes: 3b +2 at every trust on a per-referral death
  count, neutral on a patient count. Genuine same-day re-referrals (stood down and referred again) are the over-cleaning half. Organs:
  the go-live notice's parallel-run paragraph and the pair structure. Over-cleaning stop: one referral kept per patient per day (3a
  minus 6, 3b minus 2).

**No-cancel rule.** On every figure the positive deltas are even and the one negative device is odd, so no subset of mishandlings
lands on a golden (asserted over every subset, per trust and per total); DV3 zeroes a trust's own care, which never equals its golden.
On the census path no subset lands on the golden at A, C, D or G (asserted).

**Targets (record, July 2023 to June 2026).**

| Trust | 3a patients | 3b deaths | 3c confirmable | Natural path 3a / 3b / 3c | Census path 3c, devices handled / not |
|---|---|---|---|---|---|
| A | 438 | 126 | 8 | 445 / 131 / 13 | 6 / 9 |
| B | 104 | 29 | 0 | 109 / 34 / 0 | 0 / 0 |
| C | 351 | 104 | 5 | 356 / 109 / 8 | 1 / 2 |
| D | 275 | 80 | 80 | 280 / 85 / 83 | 0 / 0 |
| E | 559 | 165 | 0 | 567 / 168 / 0 | 0 / 0 |
| F | 140 | 40 | 6 | 145 / 45 / 0 | 6 / 0 |
| G | 221 | 63 | 46 | 226 / 68 / 53 | 45 / 48 |
| H | 75 | 22 | 3 | 80 / 27 / 0 | 3 / 0 |
| Total | 2,163 | 629 | 148 | 2,208 / 667 / 157 | 61 / 59 |

By four-quarter year (golden): patients 695, 737, 731; deaths 204, 212, 213; confirmable 54, 50, 44 (D 25, 28, 27; G 14, 17, 15).
The confirmable figures split into empty-bed waits (A 6, C 1, F 6, G 45, H 3) and allocation waits (A 2, C 4, D 80, G 1). Per-trust
stops (each device handled alone, each over-correction) are asserted off the golden at every trust they touch.

**Hazard table.** DV1 moves 3a, 3b, 3c and the three totals at all eight trusts; HZ1 moves 3c at three; HZ2 moves 3b at eight on a
per-referral count. Necessity matrix: every device moves at least one figure at every trust it is planted at.

**Referee (exactly one).** The network's inter-hospital transfer audit: local decision times and verified identities for patients
moved between trusts, all 36 months, no deaths, no levels, byte-clean. In summer 2023 a transferred legacy patient's decision time in
the audit is an hour later than on the referral, and a transferred temporary-identity patient appears under the verified key. It
covers transfers only (about a fifth of the long waits), so it hands over no column.

**Pair arithmetic (Part 0), planning weights 38 / 7 / 55, r = 5, 32 ask criteria at 1.72 points.** Cracker (files D): recommendation
38, instruction-following 7, the chart's five parts and the two structural zeros (B's and E's 3c), device-blind on the rest: 57.0.
Mirror (files G from rung 3): r 5, instruction-following 7, one chart part and the two zeros: 17.2. Pair **37.1**. Every single and
every double catch among the six devices leaves the pair at 37.1, because every figure sits under three or more devices. The layer's
thinnest point is the triple catch of DV1, DV2 and DV4: 53.4 if both top responses make it (it also completes D's 3c, which
carries no grain hazard), 45.7 if only the cracker does. Reachability (A1): 5 of 32 ask criteria are reachable from the landed call. The pass condition rests on the ladder holding the field
to at most one response on D, and on the three silent wait-and-death devices staying silent.

### Prompt (stage 2)

`prompt.md` written under guide-to-prompt after prompt-voice.md and prompt-economy.md. Opening move question-first (the last three
builds opened stakes-first, evidence-first and number-first); the role sits mid-paragraph; one belief clause (the chair, pointing at
E); the call is the context's last sentence ("Name the one trust the review should sit in."); the docx leads with the trust alone;
each later paragraph ties back to the call. No sentence fixes the basis, window, population or method (the remit carries all four),
no input file is named, and every figure is a count under one convention sentence. voice-check.py 119: 226 words, 20.5 words a
sentence, context 34.1 per cent, longest paragraph 77 words, a sentence under eight words, one rounding carrier with its convention,
no "because", no flagged carrier, no shared six-word run. Institutional nouns for H20: acute trusts, the regional health board, the
board funding one twelve-month engagement, quality surveillance.

### Assertion plan (54, generator then independent verifier)

1. Rung 0 leader E, margin at least 1.20 (1.27).
2. Rung 1 leader A, margin at least 1.20 (1.26).
3. Rung 2 leader C, margin at least 1.20 (8.5); the mixed reading (network for trusts with no level-3 beds) also names C (1.62).
4. Rung 3 leader G, margin at least 1.20 (7.5).
5. Rung 4 leader D, margin at least 1.50 (1.80).
6. Five distinct leaders.
7. D 4th on rung 0, behind by at least 1.5x.
8. D never first or second on rungs 1 to 3.
9. Dominance against G, E, A and C, both ratios and the product.
10. Twelve grid cells by name; exactly the two census-and-allocation cells name D.
11. Own and network scope equal per trust at the census basis, with and without allocation.
12. Any admission, any theatre admission and planned own-theatre admission select identical waits during long waits in the window.
13. Every allocation wait holds a planned admission inside its first four hours.
14. Every own-empty wait holds the empty staffed bed from decision to assignment; no capacity wait shows an empty staffed bed at
    minute grain or at hourly snapshots.
15. No long wait at a trust without level-3 beds overlaps any unit's empty staffed bed or planned admission.
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
7. **Every device in nine legacy months.** A platform migration concentrates exactly this mess, and the clean months after it are
   what a cutover looks like.

### Stopping rule (written before any round)

- At ceiling: two consecutive rounds (in-house or portal) in which a response files D at 27 by the allocation route, or one round in
  which both top responses file D. The ladder is then a computation; re-root at stage 1.
- One more repair is licensed by a round whose top responses stop at G, C, A or E while the pair clears 40 through the asks: harden
  the device layer (supplemental-stumping Part 10), not the ladder.
- A response filing D without reading D's stays (by resemblance or by chance) is a shortcut to find and close before anything else.

### Pack plan (provisional; dataset-generation builds against it)

Spine `critical_care_referrals_202307_202606.csv` (about 42,000 referrals, both levels); unit stays (parquet); daily 08:00 bed returns
(csv); admitted patient care episodes with the linked date of death (about 900,000 rows, parquet); unit register (effective-dated,
csv); the network's monthly capacity report (xlsx, context artifact); the remit (docx, governing); the field guide (pdf); the
programme's review log (xlsx) with its review records (sqlite); the device organs (legacy referral events, legacy referral form guide,
legacy export specification, legacy unit export note, temporary-identity merges, platform go-live notice, 2024 consolidation paper);
the transfer audit (csv, referee); a short G unit note; correspondence (eml); the provenance note. Distractor candidates: the level-2
units' daily returns and an ambulance handover extract. Stage 3 consolidates into the 10-to-19 band in the organisations' own idiom,
without merging any device's two organs into one file and without one file holding two primaries' documentary organs.

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
