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

Verdict against the registered corpus (task117, task118, task120 and task123 included): **PASS** (`guard.py check`, exit 0),
card at `<scratchpad>/cards/task119.json`, not registered.

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

## Tried and rejected

- v1 (first draft, 2026-10-08, never registered): chains of spells linked across trusts on the regional patient key at a
  hand-over gap, each chain's death credited to the trust where it began against the first spell's modelled risk, pinned by a
  national retry log only the chain construction reproduced (34 of 34). Rejected at checkpoint A on 2026-10-09: recovering an
  unstored unit gated by reproducing published reviews repeats task109's and task120's architecture and cleared the guard only by
  relabelling Gate G to decomposition_attribution; the retry log refuted every trust-level screen (best 23 of 34), so the corpus
  showed a back-tester where to look; the risk-adjusted CUSUM and case-mix framing read as epidemiology; the asks answered other
  decisions (H18) and the chart named the construction.
