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

A competent solver counts each trust's deaths after a wait of more than four hours for a level-3 bed, sets aside the
trusts holding no level-3 beds, rebuilds every unit's census from its stays and writes the remit's methodology sentence
as its test, a death being the trust's own care when its own unit held an empty staffed bed during the wait or gave a bed
to another patient during it, and sends the engagement to A, 37 deaths over D's 27; the step that lands it there is
reading every admission during a wait as the trust's own decision about its beds without asking who placed the patient:
every admission inside one of A's long waits was a patient transferred from a trust without level-3 beds, on a bed the
network's bed bureau allocated (the transfer audit's `bed_confirmed_at`, which the field guide defines as the bureau's
allocation), so those waits are the network's capacity and A keeps 2 deaths of its own, while through every one of D's
long waits D's unit admitted planned post-operative patients from D's own theatres, which makes D's 27 the largest number
the review can confirm. A solver who stops one step earlier, at the census, files G at 15.

## Decisive rung

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
every D long wait falls inside those hours; C's long waits start in the evening after its unit fills; G's start on weekend
afternoons; A's, B's, E's, F's and H's long waits pass in evenings and nights with every unit full. No planned admission at any unit falls inside a long wait at any trust but D, no long wait
overlaps an hour when a unit other than its own held an empty staffed bed, and physical beds equal staffed beds at the four units
through the latest four quarters. A bed that frees inside an A, C or G long wait goes to a patient referred earlier by a trust
without level-3 beds, placed by the network's bed bureau and logged in its transfer audit (117 such admissions inside A's waits
in the latest four quarters, 23 inside C's, 6 inside G's).

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

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Deaths within 30 days after a wait of more than four hours for a level-3 bed, by referring trust, latest four quarters | E, 56 over A 44 (1.27x) | The remit's own population counted exactly as filed, and the corpus reproduces all 34 reviews under it | The unit register: E holds no level-3 beds, so every E wait is for another trust's bed |
| 1 | Waits set aside on days the trust's own 08:00 return showed no empty staffed bed (trusts without level-3 beds carry none) | C, 34 over G 4 (8.50x) | A capacity check on the network's own published return, and C's waits survive it | The census rebuilt from C's stays: C's unit was full at every hour of every C long wait (it fills by midday, the waits start in the evening) |
| 2 | Waits set aside where the census shows the own unit full at every hour of the wait | G, 15 over A 2 (7.50x) | The exact occupancy through each wait, and G's waits passed beside its own empty staffed beds | The methodology note counts the trust's decisions about the use of its own beds, and the full units gave beds to other patients through 78 per cent of A's long waits and every one of D's |
| 3 | Waits through which the own unit held an empty staffed bed or admitted any other patient | A, 37 over D 27 (1.37x) | The methodology sentence applied as written: a bed given to another patient while this one waited | The transfer audit and the field guide's `bed_confirmed_at` line: every admission inside an A long wait was a patient referred earlier by a trust without level-3 beds, on a bed the network's bed bureau allocated, not A's decision |
| 4 | **Decisive:** waits through which the own unit held an empty staffed bed or admitted a patient the trust placed itself (its own planned or local admissions, never a bureau transfer) | **D, 27 over G 15 (1.80x)** | | |

- A solver who writes the methodology sentence as its test commits to A at rung 3, which is the stump sentence's wrong answer;
  one who stops at the census commits to G.
- Every rung names a different trust (E, C, G, A, D), asserted by name after every parameter change.
- Rung 4 carries the stump (#17), behind #6 at rung 3, #11 at rung 2 and #7 at rung 1.
- The structural reading (the raw count at the four trusts holding level-3 beds, A 44 over C 35, 1.26x) is the none/own cell of
  the grid, killed by A's 08:00 returns (no empty staffed bed on any of the 135 days A's referrals waited in the latest four
  quarters).
- Gaps (stumping Part 1). Rung 0 to 1 opens the objective gap: deaths after a long wait are counted correctly and are not what
  the review is scored on. Rungs 1 and 2 move the moment at which the own unit's capacity is read (its 08:00 state, its state at
  every hour of the wait), each a measurement-time refinement on correct records; rung 3 reads the full unit's admissions during
  the wait. Rung 3 to 4 opens the population gap: who placed each admitted patient, a set that exists only as a relation between
  the waiting patient's interval, the admitted patient's referral and the bureau's audit. Decisive gap objective, reached
  through population, as the card files it.
- Survival properties of rung 4: written nowhere (the remit counts "decisions about the use of its own beds and staff" and
  names no planned admission, occupancy, transfer or order of admission; the field guide defines `bed_confirmed_at` as the
  bureau's allocation and states no rule about own care); no sweepable corpus nominates it (the corpus is blind, below); no
  arithmetic symptom (every rung partitions the same deaths, every total ties, the census is exact); not a row predicate (an
  interval join from each wait to the own unit's other admissions, then a join from each admitted patient to its referral or
  the transfer audit); no cutover date in the window (D's practice is steady through 36 months, and the CCRS-era coding of
  transfers sits in the ask layer before the window); survives deletion.
- Worth on the graded quantity: the leading count walks 56, 34, 15, 37, then 27. Rungs 1 and 2 set waits aside, rung 3 adds
  back every wait through which the own unit admitted anyone, and rung 4 keeps only the admissions the trust placed itself.

### Position table (asserted row by row)

| Rung | Leader | D's rank among the four trusts holding level-3 beds | D's count | D behind the leader by |
|---|---|---|---|---|
| 0 | E 56 | 4 of 8 overall | 27 | 2.07x |
| 1 | C 34 | last | 0 | (at zero) |
| 2 | G 15 | last | 0 | (at zero) |
| 3 | A 37 | 2 | 27 | 1.37x |
| 4 | D 27 | 1 | 27 | leads G by 1.80x |

D leads no intermediate rung and is second on one, rung 3, 1.37x behind A (the position rule allows one second place at
1.20x or more). No rung margin is under 1.15x; the thinnest is 1.27x at rung 0.

### Discriminator dominance

- Against A, the rung-3 decoy: A carries 37 against D's 27 into rung 4 (1.37x). On the decisive axis D keeps all 27 of its rung-3
  deaths (share 1.000) and A keeps 2 of 37 (0.054), an edge of 18.5x against the 1.64x required (1.2 x 1.37).
- The rung-2 decoy G carries no raw advantage into rung 4 (G 21 against D 27); D's decisive edge is 27 against 15, 1.80x.
- Against the raw leaders: E (56 against 27, 2.07x; share 0 against D's 1.0), A (44, 1.63x; share 0.045, an edge of 22x against
  the 1.96 required), C (35, 1.30x; share 0). Every product clears the 1.2 floor.

### Correction grid (asserted cell by cell)

Toggles: occupancy basis (none, 08:00 return, hourly census) by unit scope (own unit, whole network) by the reading of the unit's
admissions during the wait (ignored, any admission, admissions the trust placed itself), eighteen cells.

| Basis | Scope | Admissions | Names | Violates |
|---|---|---|---|---|
| none | own | any of the three | A 44 over C 35 (1.26x) | own care at the hour (A's unit full through every A wait) |
| none | network | any of the three | E 56 over A 44 (1.27x) | own care (E holds no level-3 beds) |
| 08:00 | own | ignored | C 34 over G 4 (8.50x) | own care at the hour of the wait (the 08:00 return describes the morning) |
| 08:00 | own | any | A 35, C 34, D 27 | as above; two wrong trusts within 1.2x of each other, D 1.30x behind |
| 08:00 | own | placed | C 34 over D 27 (1.26x) | as above |
| 08:00 | network | ignored | C 34 over D 24 (1.42x) | "its own beds" |
| 08:00 | network | any | E 54 over A 40 (1.35x) | "its own beds" |
| 08:00 | network | placed | E 48 over A 35 (1.37x) | "its own beds" |
| census | own | ignored | G 15 over A 2 (7.50x) | the methodology note: a full unit's own placements during the wait are the trust's decisions about its beds |
| census | own | any | A 37 over D 27 (1.37x) | the bed bureau allocates every transfer's bed (field guide, transfer audit): a transfer is not the trust's decision |
| census | own | placed | **D 27 over G 15 (1.80x)** | |
| census | network | ignored | G 15 over A 2 (7.50x), equal per trust to the own-unit cell (C1) | "its own beds" |
| census | network | any | E 54 over A 40 (1.35x) | "its own beds" |
| census | network | placed | E 47 over A 30 (1.57x) | "its own beds" |

Only the census, own-unit, own-placement cell names D. Partial applications: admissions read on the 08:00 basis name A or C;
own placement read from each admitted patient's referring trust, from the admission type (02 a transfer in) and from the
bureau's audit select the same admissions in the latest four quarters (C1, asserted: D's 133 planned own-theatre admissions,
type 04; A's 117, C's 23 and G's 6 transfers, type 02); any admission and own placement part only at A (37 against 2), C (6
against 0) and G (17 against 15), by bureau transfers. Window cells: the latest eight quarters (D 55 over G 32) and the whole
record (D 80 over G 46) name D, so no window moves the name; the counts are pinned by the remit's placement clause (C4).

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
| 19 | Code semantics | own care counts the admissions the trust placed itself (its planned and local admissions), never a transfer whose bed the bureau allocated | C1 in the window: inside every long wait the own unit admitted only planned own-theatre patients (D, type 04) or bureau transfers (A, C and G, type 02), so own placement read from the referring trust, from the admission type and from the transfer audit select the same admissions (asserted); any admission against own placement is the rung-3 fork, closed by the field guide's `bed_confirmed_at` line and the audit (C4: A 37 over D 27 against D 27 over G 15); before April 2024 the CCRS-era feed coded every unplanned admission 01, ask device DV6 |
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
every rung below 4; 3a under repeat patients counted per referral, the clock-change nights read on the clock, the legacy level,
the legacy clock or unmerged identities; 3b under those and a per-referral death count; 3c under the census path (A, C, D, G),
the any-admission path (A, C, G), the CCRS-era transfers read by their code (A, C, G), the current register (F, H), the legacy
feed's bed episodes read as admissions (A, C, G) and the devices on 3a and 3b.

### The ask ledger (supplemental-stumping Part 9)

Hardening loop 1 re-rooted the device layer: round 1's solver handled every stage-2 device and kept its confirmable column
exact, so each ask now carries a fresh silent primary (DV7 on 3a, DV5 on 3b, DV6 on 3c) and the stage-2 devices stay on as
hazards.

**Main call's declared row population.** Files: the referral log (decisions 1 July 2025 to 30 June 2026, every trust and level),
the unit stays at A, C, D and G overlapping 1 June 2025 to 30 June 2026 (the census lead-in), the daily bed returns for that span,
the transfer audit's rows in that span, the admitted patient care episodes of patients referred in the window (date of death),
the unit register rows in force in the window, the remit, the field guide and the capacity report. Columns: referral
`referral_id, patient_key, referring_trust, dta_at, level_of_care, outcome, outcome_at`; stays `unit_code, referral_id,
patient_key, admitted_at, discharged_at, admission_type, source_location`; returns `unit_code, return_date, beds_open,
beds_occupied_0800`; transfer audit `patient_key, from_trust, to_unit, bed_confirmed_at`; episodes `patient_key,
date_of_death`; register `unit_code, trust_code, care_level, valid_from, valid_to`. **Every device and hazard row sits outside
the latest four quarters**: the legacy months to 1 April 2024 (DV1, DV2, DV4, DV6, HZ1, HZ2, and DV3's register rows valid to
31 March 2024), the two spring clock-change nights (DV5: 30 March 2024 and 29 March 2025) and year 2 (DV7's repeat patients,
July 2024 to June 2025). The zero-counts inside the population are asserted per device; the call, its count, the runner-up and
the gap are recomputed with every device mishandled and asserted identical, and on the whole record D leads with the devices
handled or not.

| Ask | Figures, unit | Pool; construction layer | Device layer: primary; hazards | File path (causal) | Use, and how it enters the call (H18) |
|---|---|---|---|---|---|
| 1 Call furniture | the trust; its confirmable deaths in a year; the runner-up; the gap in deaths | A (the recommendation block); rung 4 | none (main path) | register, referral log, stays, returns, transfer audit, episodes, remit, field guide | component |
| 2 Chart | 5 parts | A (the call drawn); rung 4 | none | as ask 1 | component: the call at a glance |
| 3a Record: patients inside the remit | per trust, whole patients; total | B; none | **DV7** repeat patients (D6); hazards DV1 legacy clock (D8), DV2 temporary identities (D7), DV4 legacy level semantics (D3), DV5 | referral log, stays, CCRS level entries, key links, CCRS specification, episode specification, remit, field guide: 8 files, 14 columns | qualifier: the record behind the forward call, which lets one year stand for 2027-28 |
| 3b Record: deaths among them | per trust, whole deaths; total | B; none | **DV5** the spring clock change (D8); hazards DV1, DV2, DV4, DV7, HZ2 parallel-run copies (D1) | 3a plus episodes: 9 files, 16 columns | qualifier |
| 3c Record: deaths the reviewers could have confirmed | per trust, whole deaths; total | B, both layers; rung 4 (the census path misses A, C, D, G; the any-admission path A, C, G) | **DV6** CCRS-era transfers coded as local admissions (D3); hazards DV1, DV2, DV3 register vintage (D2), DV4, DV5, HZ1 legacy unit-feed grain (D6), HZ2 at D | 3b plus register, returns, the 2023 board paper, transfer audit: 13 files, 29 columns | qualifier |

Pool A is the call and its picture only (9 criteria, the cracker's by construction); every ask block is pool B. No primary family
repeats (D6, D8, D3).

**Primaries, organs and root causes.** Three root causes: the referral platform replacing the legacy system (CCRS) on 2 April
2024 after a six-week parallel run (RC1), the network's level-3 consolidation on 1 April 2024 (RC2) and the clock itself (RC3:
the platform and the bed-management feed record local time). Each primary's two organs sit in different files, the documentary
one in a document the main call does not read, and no file carries two primaries' documentary organs.

- **DV7, repeat patients (primary on 3a).** At seven trusts (all but D) two year-2 patients come back with a second long wait at
  the same trust under the same verified key: discharged alive from the first stay inside four days, referred again 8 to 13 days
  after the first decision, and dead after the second stay, inside 21 days of the first decision. They are one patient and one
  death each. Counting referral rows moves 3a by 3 at those trusts (the identity device's second waits count again too; E by 4,
  D by 1) and a per-referral death count moves 3b by 2. Organs: the referral log (two referrals under one verified key,
  structural) and the episode extract specification's verified-key line (documentary); the prompt's "every figure counts people"
  pins the unit. Over-correction stop: every patient with two long waits at one trust dropped (totals 2,140 / 615 / 148). Not at
  D, because every D long wait is confirmable and a pair there cancelled the confirmable total (`## Tried and rejected`).
- **DV5, the spring clock change (primary on 3b).** On the evenings before the clocks went forward in 2024 and 2025, 20 waits
  were decided at about 22:30 to 00:10 and given a bed after 02:00: 3h10 to 3h50 of elapsed time, 4h10 to 4h50 on the clock. Read
  on the clock they enter the remit: 3a +2 at A, B, C, E and G, +3 at F and H, +4 at D; 3b +2 at A, C, E, F and G, +3 at H, +4 at
  D (B's two survive); 3c +4 at D (two waits each night beside an empty staffed bed in D's unit), +2 at F and H. Organs: the CCRS specification's
  "the network bed-management feed records local time" (documentary) and the capacity report, whose referral waits reproduce from
  the referral log only in elapsed time (four trust-months differ on the clock readings, structural). Over-correction stop: every
  wait decided on a clock-change eve dropped (totals 2,157 / 627 / 147).
- **DV6, CCRS-era transfers coded local (primary on 3c).** Before 2 April 2024 the bed-management feed coded every unplanned
  admission 01, transfers included; the platform codes a transfer in 02. Own placement read from the admission type takes the
  legacy bureau transfers inside A's, C's and G's full-unit waits as the trust's own admissions: 3c +20 at A, +5 at C, +2 at G.
  Organs: the transfer audit (every transfer from July 2023 with its receiving unit and the bureau's allocation time, and the
  admitted patient's referral from another trust, structural) and the 2023 board paper's "Transfers will continue to be agreed
  through the network's bed bureau" (documentary). Over-correction stop: only platform-era admissions read as own placements
  (3c minus 20 at D, minus 3 at C, minus 2 at A, minus 1 at G; total 122). It bites only on the reading "not coded as a
  transfer"; a solver who reads own placement as a planned admission (04) alone handles it without seeing it, which makes DV6
  the weakest of the three primaries.
- **The stage-2 devices, now hazards.** DV4 legacy level semantics (3a +2 and 3b +2 at every trust, 3c +2 at D and H; organs the
  CCRS level entries and the CCRS specification's "requested by the referring team"; stop: legacy referrals with a level change
  dropped, 2,154 / 626 / 148). DV2 temporary identities (3a +1, E +2; 3b minus 1, E minus 3; 3c minus 1 at A, C, D, F, G and H;
  organs the key links and the episode specification's temporary-registration line; stop: temporary-identity referrals dropped,
  2,153 / 619 / 142). DV3 register vintage (3c minus 6 at F, minus 3 at H; organs the register's dates and the 2023 board paper;
  stop: F and H read as level 3 throughout, 3c 190, call unchanged). DV1 legacy UTC clock (3a +2, A and E +4; 3b +2; 3c +7 at A,
  +3 at C, +2 at D and F, +4 at G; organs the CCRS specification's "held in UTC" and the transfer audit's local decision times;
  stop: every legacy time shifted, 2,133 / 623 / 142). HZ1 legacy bed-episode rows (3c +2 at A and C, +4 at G; stop: stays of one
  patient within 24 hours merged, 3c 146). HZ2 parallel-run copies on a per-referral death count (3b +4 at every trust: two copies and
  DV7's two second waits at each trust but D, four copies at D, where 3c moves +4 too; stop: one referral per patient per day,
  2,157 / 627 / 148).

**No-cancel rule.** Asserted by enumeration rather than parity: no subset of the 511 combinations of mishandled devices lands any
touched figure or total on its golden, per trust and per total; on the census path no subset lands on the golden 3c at A, C, D
or G, and on the any-admission path none at A, C or G.

**Targets (record, July 2023 to June 2026).**

| Trust | 3a patients | 3b deaths | 3c confirmable | Natural path 3a / 3b / 3c | Census path 3c, devices handled / not | Any-admission path 3c, handled / not |
|---|---|---|---|---|---|---|
| A | 438 | 126 | 8 | 452 / 135 / 35 | 6 / 6 | 99 / 106 |
| B | 104 | 29 | 0 | 115 / 36 / 0 | 0 / 0 | 0 / 0 |
| C | 351 | 104 | 5 | 363 / 113 / 14 | 1 / 2 | 23 / 27 |
| D | 275 | 80 | 80 | 289 / 91 / 91 | 0 / 4 | 80 / 91 |
| E | 559 | 165 | 0 | 575 / 172 / 0 | 0 / 0 | 0 / 0 |
| F | 140 | 40 | 6 | 152 / 49 / 0 | 6 / 0 | 6 / 0 |
| G | 221 | 63 | 46 | 232 / 72 / 57 | 45 / 47 | 51 / 60 |
| H | 75 | 22 | 3 | 87 / 32 / 0 | 3 / 0 | 3 / 0 |
| Total | 2,163 | 629 | 148 | 2,265 / 700 / 197 | 61 / 59 | 262 / 284 |

By four-quarter year (golden): patients 695, 737, 731; deaths 204, 212, 213; confirmable 54, 50, 44 (D 25, 28, 27; G 14, 17, 15).
The confirmable figures split into empty-bed waits (A 6, C 1, F 6, G 45, H 3) and own-placement waits (A 2, C 4, D 80, G 1).
Every device alone moves exactly its designed deltas per trust per figure (asserted); every figure but B's and E's 3c sits under
three or more devices; the necessity matrix holds (each device moves a figure at every trust it is planted at).

**Referee (exactly one).** The network's inter-hospital transfer audit: 3,852 transfers, local decision times, verified keys and
the bureau's allocation time for every patient moved between trusts, all 36 months, no deaths, no levels, byte-clean. It is on
the main path for rung 3 (its rows in the window) and is the structural organ of DV6 and DV1 (its legacy rows). It covers
transfers only (36 per cent of long waits), so it hands over no column.

**Pair arithmetic (Part 0), planning weights 38 / 7 / 55, r = 5, 32 ask criteria at 1.72 points.** Cracker (files D):
recommendation 38, instruction-following 7, the chart's five parts and the structural zeros; mirror (files A from rung 3, or G
from rung 2): r 5, instruction-following 7, one chart part. With the hygiene battery applied and every device missed the pair
is **37.1** (the same with either mirror); every single and double catch leaves it at 37.1 or under, and the thinnest triple at
37.1. Named profiles, both top responses making the same catches (asserted and printed by the generator): round 1's six catches
with transfers read by their code 37.1, read by the referring trust 39.7; round 1's six and elapsed time 44.0; everything but DV5
41.4; everything but DV7 47.4; everything but DV6 73.2; everything 76.6. The layer holds the pair under 50 unless both top
responses compute waits in elapsed time across the clock change **and** count each repeat patient's death once; with those two
caught and DV6 missed the pair is 73.2. Reachability (A1): 5 of 32 ask criteria are reachable from the landed call. The pass
condition rests on the ladder holding the field to at most one response on D, and on DV5 or DV7 staying silent.

### Prompt (stage 2)

`prompt.md` written under guide-to-prompt after prompt-voice.md and prompt-economy.md. Opening move question-first (the last three
builds opened stakes-first, evidence-first and number-first); the role sits mid-paragraph; one belief clause (the chair, pointing at
E); the call is the context's last sentence ("Name the one trust the review should sit in."); the docx leads with the trust alone;
each later paragraph ties back to the call. No sentence fixes the basis, window, population or method (the remit carries all four),
no input file is named, and every figure is a count under one convention sentence. voice-check.py 119: 226 words, 20.5 words a
sentence, context 34.1 per cent, longest paragraph 77 words, a sentence under eight words, one rounding carrier with its convention,
no "because", no flagged carrier, no shared six-word run. Institutional nouns for H20: acute trusts, the regional health board, the
board funding one twelve-month engagement, quality surveillance.

### Assertion plan (54 at stage 2, as revised by hardening loop 1; generator then independent verifier)

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
12. Inside every long wait in the window the own unit admitted only planned own-theatre patients (D, type 04) or bureau transfers
    (A, C and G, type 02), and in the record only those two kinds; every such transfer was decided before the wait it falls in and
    is in the bureau's audit at its bed time; any admission and own placement part only at A, C and G.
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
55. Hardening loop 1: the clock-change nights carry exactly the designed waits (11 and 9) and none of them is long in elapsed
    time; the repeat patients are exactly the designed pairs (two at each trust but D); DV5, DV6 and DV7 have zero rows in the main
    population, their designed deltas, two organs each and one primary per documentary file; the any-admission path lands no
    subset on the golden; the named pair profiles are printed and the two round-1 profiles stay under 50.

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

### Stopping rule (written before any round)

- At ceiling: two consecutive rounds (in-house or portal) in which a response files D at 27 by the allocation route, or one round in
  which both top responses file D. The ladder is then a computation; re-root at stage 1.
- One more repair is licensed by a round whose top responses stop at G, C, A or E while the pair clears 40 through the asks: harden
  the device layer (supplemental-stumping Part 10), not the ladder.
- A response filing D without reading D's stays (by resemblance or by chance) is a shortcut to find and close before anything else.
- State after round 1 (2026-10-09): one round in which a response filed D at 27 by the allocation route, read straight off the
  methodology sentence; loop 1 makes that reading name A. A second consecutive round with a response on D by the placement route
  puts the ladder at ceiling.

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

Stage 3, 2026-10-09, rebuilt in hardening loop 1 the same day. Generator `task119/generator/`, seed 119: `build.py` (entry
point), `plan.py` (designed waits and device rows), `world.py` (day roles and every designed wait on the clock), `sim.py` (each
unit's events into stays), `people.py` (referrals, deaths, episodes), `legacy.py` (migrated rows, level entries, parallel-run
copies, bed-episode rows, transfer audit, key links), `extracts.py` (capacity report, ambulance and level-2 extracts),
`corpus.py` (review records), `docs.py` and `texts.py` (papers), `golden.py` (every figure from the shipped files), `checks.py`
(assertions). `verify.py` is the independent verifier (DuckDB joins, pandas time-zone conversion, numpy census over islands of
contiguous rows; imports nothing from the generator). `reproduce.py` builds twice and compares bytes.

**Gates (loop 1).** Generator: 137 assertions, 0 failed, on the build into the task folder. Verifier: 24 claims, 0 failed, on
`task119/target`. Two consecutive builds into the scratchpad byte-identical (20 files: 19 under `target/` plus `metadata.json`,
file times equal), and the task folder's pack byte-identical to them (a reporting line added to `checks.py` afterwards writes
nothing into the pack). Input gates: 19 files; 8 formats (csv, docx, eml, parquet, pdf, sqlite, txt, xlsx); referral log 30,785
rows; review database a SQLite file with five tables; distractors `level2_unit_bed_return_0800_2025-26.csv` and
`ambulance_handovers_hourly_2025-26.csv`, named in `metadata.json` only and each asserted unused (every figure unchanged with it
deleted). Goldens regenerated from the rebuilt pack byte-identical to the shipped ones.

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
bureau's transfer audit at their bed time; STN-ACC admitted planned post-operative patients through all 92 STN long waits.
Clean-data test (hourly return): rung names G 15, call D, naive E. Lens swap: no referral-log column or pair reproduces the
confirmable counts.

**The asks (record, July 2023 to June 2026; patients / deaths / confirmable).** A 438 / 126 / 8; B 104 / 29 / 0;
C 351 / 104 / 5; D 275 / 80 / 80; E 559 / 165 / 0; F 140 / 40 / 6; G 221 / 63 / 46; H 75 / 22 / 3; total 2,163 / 629 / 148.
By four-quarter year: 695 / 204 / 54, 737 / 212 / 50, 731 / 213 / 44 (D 25, 28, 27; G 14, 17, 15). Confirmable split:
empty-bed waits A 6, C 1, F 6, G 45, H 3; own-placement waits A 2, C 4, D 80, G 1. Unchanged by loop 1.

**Device layer (measured, loop 1).** Natural path (every device mishandled): A 452 / 135 / 35, B 115 / 36 / 0,
C 363 / 113 / 14, D 289 / 91 / 91, E 575 / 172 / 0, F 152 / 49 / 0, G 232 / 72 / 57, H 87 / 32 / 0, total 2,265 / 700 / 197.
Census path 3c, devices handled / not: A 6 / 6, C 1 / 2, D 0 / 4, F 6 / 0, G 45 / 47, H 3 / 0, total 61 / 59. Any-admission
path 3c: A 99 / 106, C 23 / 27, D 80 / 91, F 6 / 0, G 51 / 60, H 3 / 0, total 262 / 284. Each device alone moves its designed
deltas exactly (asserted per trust per figure); no subset of the 511 lands a touched figure or total on its golden; no census-path
subset lands on the golden at A, C, D or G and no any-admission subset at A, C or G; zero device and hazard rows inside the main
call's declared population. Over-correction stops (totals): DV1 2,133 / 623 / 142; DV2 2,153 / 619 / 142; DV3 3c 190; DV4
2,154 / 626 / 148; DV5 2,157 / 627 / 147; DV6 3c 122; DV7 2,140 / 615 / 148; HZ1 3c 146; HZ2 2,157 / 627 / 148. Clock-change
nights: 11 waits on 30 March 2024 and 9 on 29 March 2025, none long in elapsed time. Repeat patients: 14 designed (two at each
trust but D) among 46 people with two long waits in the record (the rest identity-device rows and parallel-run copies). Hygiene
battery clean on the natural path. Pair simulation 37.1; every single and double catch 37.1 or under; thinnest triple 37.1;
named profiles 37.1 (round 1, transfers by code), 39.7 (by referring trust), 44.0 (round 1 and elapsed time), 41.4 (all but DV5),
47.4 (all but DV7), 73.2 (all but DV6), 76.6 (all). Referee: 3,852 transfers, verified keys, local decision times, 36 per cent of
long waits. Spans from the golden's code path: 3a 8 files / 14 columns, 3b 9 / 16, 3c 13 / 29.

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

## Leak review

`leak.py task119 --asof 2026-10-02`, re-run in hardening loop 1 against the loop-1 stump sentence and again at the stage-3
re-run (2026-10-09, same pack): **REVIEW**, no LEAK; sweeps 1 to 3 and 5 to 11 clean. The five REVIEW lines are sweep 4 (generic stump-paragraph words), each read in full:

- `accn_board_paper_2023-11-21_level3_capacity.pdf`: the 2023 consolidation paper (Ellerdyke to level 2, Pellowham's
  winter beds, transfers continuing through the network's bed bureau); it says nothing about planned admissions, waits,
  own care or Stennock, and is the documentary organ of DV3 and DV6.
- `ccrs_migration_export_specification_rel2.3.pdf`: the legacy export's clock, level and bed-episode semantics and the
  bed-management feed's local time, the ask layer's organs; no sentence touches the platform era or the order in which a
  unit fills.
- `rds_apc_extract_specification.txt`: the episode extract's fields, its temporary-key linkage and the verified key, the
  organs of DV2 and DV7; "admission" there is the hospital spell, not the unit.
- `review_terms_of_reference_2027-28.docx`: the remit's scope (transferred patients reviewed with the trust that referred
  them), judging rule and methodology note, the filed pins; it names no planned admission, occupancy, bureau or order of
  admission.
- `wenmarsh_acc_extract_field_guide.pdf`: the field definitions, where "planned" sits only in the admission_type code list
  beside the five other codes, "staffed" in beds_open and the bureau in the transfer audit's `bed_confirmed_at`; it states
  no rule about any of them and never says whose care a transfer is.

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
