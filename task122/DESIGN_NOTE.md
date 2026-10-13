# task122 design note

Architecture v3 on the card (the second architecture built for this slot; v1 was a draft redrawn before
registration), re-rooted 2026-10-13 under the 10/10 rules. v2, a Dutch resale platform choosing which ranking
policy takes its home carousel's test slot, was retired after a Gate G send-back and is FAILED_TO_STUMP in the
author's backlog: its decisive step was a field read under a filed charter and its estimator was pinned by an
archive of certified tests. The slot is redrawn into a new domain, world, decision and quantity. v2's record is
kept at the end of this note; its pack, goldens and reports are removed from the tree and kept in history.

## Draw

| Axis | Value |
|---|---|
| Domain / task type | Biomedical & Clinical Research / longitudinal-outcomes-repeated-measures (serves Experiment & Causal in the client taxonomy; the domain has never been built, in any objective) |
| Objective | Experiment & Causal Analysis: the call is a causal claim read from a randomised trial, how far each dose of the drug moves eGFR against placebo after 36 months' treatment |
| Niche | a Copenhagen-area clinical-stage biotech chooses which of four once-daily doses of its oral aldosterone synthase inhibitor, VMK-4410, goes into the phase 3 kidney trial, from a 52-week multinational phase 2b in albuminuric chronic kidney disease whose protocol held background diuretics, RAS blockers and SGLT2 inhibitors unchanged for the first 12 weeks |
| Shape | 11 before and after with a control: each dose's eGFR difference from placebo after 12, 24 and 36 months' treatment (4 doses x 3 times), plus the call, the runner-up and the gap, a chart with named parts and the asks |
| Decision type / unit | pick one of four doses (named option); the graded figures are mL/min/1.73 m2 of eGFR against placebo |
| Gap / pattern / generators | time (what the 52-week trial measured against the 36 months the decision is scored on); no A to E pattern; G4 decisive (the one-off recovery after background diuretics are eased, at the turn from the acute phase to the chronic phase, attributed to the chronic slope), G13 (the 36-month horizon multiplies a slope read over 40 weeks), G16 (where the chronic phase is fitted from) |
| Gate G mechanism | method_or_model_selection: every laboratory value, visit and protocol rule is read correctly on the wrong route; the decision turns on the window the chronic eGFR slope is fitted over |
| Stump strategy | decomposition_attribution: the eGFR trajectory splits into the acute haemodynamic fall, a one-off recovery once diuretics are eased, and the chronic slope, and only the last is carried for three years |
| Decisive rule filed / decoys | the estimand is filed (the phase 3 synopsis: eGFR at month 36 against placebo, every randomised patient, as if each had stayed on the assigned dose); no official decoy (no filed slope method, knot or acute window anywhere in the pack), no validated decoy, no calibration corpus; the phase 2b's own results report is not shipped |
| Calibration form | none |
| Context artifact | other (the phase 3 synopsis that files the estimand, beside the phase 2b protocol) |
| Stakeholder | the head of clinical development, who recommends the dose to the chief medical officer, who signs it for the end-of-phase-2 meeting package (the prompt names no one) |
| Forum / forcing event / org family | line_manager_or_team / statutory_or_regulatory_filing (the end-of-phase-2 meeting package) / other (a clinical-stage biotech, not yet a manufacturer) |
| World | Varnmark Therapeutics (invented), Copenhagen area, DKK; phase 2b VMK-4410-202 at sites in Denmark, Sweden, Germany, Poland, Spain and the United Kingdom; personas drawn da_DK seed 122: Benedicte Laursen (head of clinical development), Nicolaj Lassen (biostatistics), Kirsten Eriksen (clinical pharmacology), Lene Dam (medical monitor) |
| Deliverables | `VMK-4410_phase3_dose_recommendation.pdf` (the call, each dose's eGFR difference from placebo after 12, 24 and 36 months' treatment, a chart of each dose's difference by month); `VMK-4410_phase2b_tables.xlsx` (the asks) |
| Guard | WARN only (answered below); registered 2026-10-13 |

**Data-native sentence.** The protocol held background diuretics steady for the first twelve weeks, so the
patients whose eGFR fell furthest on the higher doses, those already on a loop diuretic when the drug's
natriuresis added to it, had their diuretic eased only from week 12 and recovered part of the fall over the
following weeks; the eGFR record therefore turns from an acute fall to its chronic slope only around week 24, and
a chronic slope started at the field's usual three months carries that one-off recovery forward for three years.

**Mechanisms on file (Experiment & Causal), one line on the insight each spends.**
- task6: a non-randomised pilot read against each arm's own baseline once a hidden record stream is recovered.
- task12: an arm-correlated population captured in a second party's system, recovered by anti-join.
- task15: outcome rows missing for one arm after a client change, recovered from an independent log.
- task43: a pooled effect carried onto a cohort whose moderator mix is reversed, the moderator behind a join.
- task44: a pooled gain that mixes opposite effects split by a moderator in no column.
- task69: a capped set whose members' contributions overlap; an assignment rate that moved across periods.
- task83: an effect conditioned on each unit's own prior treatment history; allocation by single-peaked effect.
- task122 v1 and v2: a library-fill clause; outcomes the log records only before a session closes.
- task131: a randomised tariff's half-hourly effect at design-day heat, read on the maximum of the whole curve.
- None separates a transient from a long-run rate inside one arm's trajectory, and none is in nephrology.

**Sources, one line each.**
- The client's two-layer standard: the field's own method decides; here it is nephrology's acute-plus-chronic
  eGFR slope analysis, worked on where this trial's acute phase really ends, never a stated score or a window rule.
- The client's library (`biomedical-clinical-research/longitudinal-outcomes-repeated-measures`: MMRM over
  completers, baseline-adjusted change): both are lower rungs here; the pattern is our own,
  `own:egfr-chronic-slope-after-diuretic-recovery`.
- The client's measured drivers, held group: the decisive step sits upstream of every graded figure (each dose's
  36-month difference is built on the slope window) and the shortcut is the field's own convention.
- task131 (an effect read at design conditions): there the conditioning was on the weather the decision faces;
  here nothing is conditioned, the trajectory itself has three phases and only one is carried.
- task123 v2 (a total recorded over each unit's own interval, split onto calendar periods; same gap, pattern and
  Gate G): differentiated on the card; no interval allocation here.
- Field practice: GFR slope as a surrogate end point (acute effect over the first months, chronic slope after),
  the haemodynamic eGFR fall on starting a RAS blocker, SGLT2 inhibitor or aldosterone pathway drug, and the
  stable-background period phase 2 kidney protocols write in; the build carries the practice, not any trial's
  figures.

**WARNs answered.**
- repeat.gate_g and overuse.gate_g (method_or_model_selection; task449, task501 in the guard's order): the honest
  name for choosing the window a slope is fitted over; task449 sets a dial and task501 selects an estimator for a
  different quantity, and forecasting or decomposition_attribution would misname a model choice the trial's own
  record forces.
- repeat.decision (pick_one_of_n, task501): a phase 3 takes one dose, so the decision is a pick.
- repeat.question_form (which, task501): a pick asks which.
- The guard orders same-date cards by task number, so its bans read task448, task449 and task501; the card also
  clears the builds registered last on 2026-10-13 (task452, task453, task454) on every banned axis: shape 11
  against 01, 10 and 07; forum against committee_or_panel, minister_or_cabinet and customer_or_counterparty;
  forcing event against budget_or_appropriation, period_close and launch_or_rollout; strategy against other,
  population_selection and composition_mix; decisive pattern G4 against G14, G16 and C.

**Arithmetic on the arm means** (scratch `ladder2.py`, `search4.py`; visits at weeks 0, 2, 4, 8, 12, 16, 20,
24, 32, 40 and 52; diuretics eased at the week-12, 16 and 20 visits in 45, 35 and 20 per cent of the patients
eased; recovery time constant 2.5 weeks). Each dose's initial fall against placebo, the part that comes back
after easing, and the chronic benefit in mL/min/1.73 m2 a year: 5 mg 0.2, 0, 0.40; 10 mg 1.2, 0.05, 1.05; 20 mg
2.5, 0.2, 2.10; 40 mg 5.85, 1.2, 2.55. Month-36 differences by route: golden (the level each arm settles at plus
the chronic benefit over three years) 1, 2, 4, 3; two-slope with the chronic phase from week 4, 12 or 16, 40 mg
first (6.3, 6.0, 4.9 against 20 mg 4.5, 4.5, 4.3); from week 20, 20 mg by 0.2; from week 24 or 32, the golden
figures within 0.25; one slope through every visit, 20 mg on wrong figures (2.1, 0.6 for 40 mg); the week-52
difference, 5 mg (0.2 against -0.1 and -0.2); the chronic benefit alone, 40 mg (2.55 against 2.10).

**Shape arithmetic (shape 11).** 4 doses x 3 times = 12 graded differences from placebo, plus the call, the
runner-up and the gap (3), a chart with four named parts (4) and the two files (2): 21 before the ask layer, and
the asks add 5 arms x 4 measures = 20, for 41 in all. The decisive construction moves the 24- and 36-month cells
of 20 and 40 mg and the call; the 12-month cells are each dose's observed difference at week 52.

## Default path

1. Read the question: which dose, judged by how much higher eGFR would be than on placebo after 36 months'
   treatment, which the phase 3 synopsis files as the difference at month 36 for every randomised patient as if
   each had stayed on the assigned dose.
2. Take the central laboratory's eGFR (CKD-EPI 2021, reported beside each serum creatinine) at the scheduled
   visits from `lb.csv`, each patient's change from the baseline the protocol defines (the mean of the screening
   and day 1 values), and the mean change by arm and visit.
3. Fit nephrology's standard two-slope model on every randomised patient: an acute effect from baseline to month
   3 (week 12) and a chronic slope from week 12 to week 52, by arm, against placebo.
4. Carry each dose's chronic slope to month 36 from its level at week 12 and take the difference from placebo.
5. File the dose with the largest difference.

Ends on: 40 mg, about 6 mL/min/1.73 m2 above placebo at month 36 (20 mg about 4.5, 10 mg 2, 5 mg 1); on the
arm means the month-3 route gives 40 mg 5.97 and 20 mg 4.50, and the shipped figures are fixed at the design stage.

Golden: 20 mg, 4 mL/min/1.73 m2 above placebo at month 36, then 40 mg at 3, 10 mg at 2 and 5 mg at 1, with the
chronic slope taken from week 24, after the recovery, from the level each arm settled at.

## Stump sentence

A competent solver fits each dose's eGFR with the field's two-slope model, an acute effect to month 3 and a
chronic slope after it, carries the chronic slope to month 36 and files 40 mg at about 6 mL/min/1.73 m2 above
placebo (the `Ends on:` figure); the step that lands it there is starting the chronic slope at month 3, when the
patients whose eGFR fell most on 20 and 40 mg had their loop diuretics eased only from week 12, at the week-12,
16 and 20 visits, and recovered part of the fall over the following weeks, so a slope from month 3 carries that
one-off recovery forward for three years; taken from week 24, after the recovery, the slope leaves 20 mg furthest
above placebo at month 36 (4) and 40 mg at 3.

## Three rules

Task type: longitudinal-outcomes-repeated-measures in Biomedical & Clinical Research, a task type that serves
Experiment & Causal Analysis in the client taxonomy: repeated eGFR measurements per patient in a randomised trial,
read as each dose's effect against placebo over time.

Domain test: the deciding quantity is each dose's eGFR difference from placebo after 36 months' treatment, and
nephrology estimates it by GFR slope analysis, an acute effect over the first months and a chronic slope after it,
the chronic slope projected; this trial's protocol and its patients' diuretics decide where the chronic phase
starts.

Swap: "Which dose leaves eGFR furthest above placebo after 36 months" with a school's nouns becomes "which tutoring
intensity leaves test scores furthest above the control group after three years"; there is no filtration fall that
a diuretic adds to, no background diuretic held fixed for twelve weeks and then eased, and no recovery of a
volume-related fall, so the step that decides has nothing to act on and the task stops making sense.

Layer 1: an SDTM-style laboratory extract from two central laboratories and local laboratories (unscheduled and
repeat samples, specimen-condition comments, creatinine in umol/L at some laboratories and mg/dL at others,
potassium in mmol/L and mEq/L), visits taken outside their windows, a dosing record with interruptions beside a
disposition record, concomitant medications with free-text doses and changes recorded as new rows, and urine
albumin-to-creatinine ratios in mg/g and mg/mmol by laboratory: the mess a CRO's data management and two central
laboratories produce, none of it placed to be caught and none of it on the decisive step.

Layer 2: estimation_fit: fitting the chronic eGFR slope over the stretch where the trajectory is chronic, after
the one-off recovery that easing background diuretics from week 12 produced, then carrying it to month 36 from the
level each arm settled at.

Decisive step: in the field's words, where the acute phase ends: the acute effect of VMK-4410 includes a
volume-related fall that partly recovers once diuretics are eased after week 12, so the chronic slope starts
around week 24, not at the conventional month 3.

Not semantics: every eGFR, creatinine, visit, unit, concomitant medication record and synopsis definition can be
read correctly and the month-3 two-slope route still files 40 mg; the difference between 40 and 20 mg is a choice
of model window, not the meaning of any field.

Not rule application: no filed rule, procedure or formula says where the chronic phase starts or how the slope is
fitted; the synopsis files the estimand only, and the protocol's twelve-week stable-background rule is a fact of
the trial's conduct that no sentence connects to the eGFR record.

Analyst test: with every laboratory value, visit and protocol rule read correctly, a strong analyst fits the
standard acute-plus-chronic eGFR model with the chronic phase from month 3, projects it to month 36 and files 40
mg (the `Ends on:` answer); the week-52 change the phase 2b protocol names as its primary end point files 5 mg
instead.

Estimand: the phase 3 synopsis (`VMK-4410-301_synopsis.pdf`) files it: the difference between each dose and
placebo in the change in eGFR (CKD-EPI 2021, central laboratory) from baseline to month 36, in every randomised
patient, as if each had stayed on the assigned dose; the prompt asks which dose and for each dose's difference
after 12, 24 and 36 months' treatment.

No decoy: nothing is planted to be caught; no document states a slope method, a knot, an acute window or a
projected figure, the phase 2b results report is not shipped, and no file ranks the doses on the 36-month
difference; the protocol's primary end point (the week-52 change) is the trial's own question, stated as such.

No certified replay: no certified, published or prior figure has to be reproduced to recover the method; the
method comes from the trial's own record (the shape of each arm's eGFR after week 12 and the diuretic changes
behind it).

Lesson: a model learns that the chronic phase of an eGFR response begins where the trajectory turns linear, which
a trial's conduct (here the background changes its protocol allowed only after twelve weeks) can push well past
the conventional three months, and that a slope fitted over a transient is multiplied by every year it is carried;
no build on file is in nephrology or separates a transient from a long-run rate inside one arm's trajectory.

## Tried and rejected

- First draft (v1, drafted 2026-10-08, never registered): every proposal failed a different launch condition and the test-calendar
  library-fill clause widened the choice to the registered library, where only E cleared all three. Died at checkpoint A because the
  decisive step was a written rule a strong solver follows once no proposal qualifies (measured trap #9 alone scored 0.58 in its
  nearest exemplar, so the stump leaned on lower rungs firing first, and the nearest dead shape is argmax under a stated rule over a
  filed candidate list, task36), and because its honest Gate G, binding_constraint, collided on (objective, G11, binding_constraint)
  with task106 and 13 older builds and passed only after the card relabelled it method_or_model_selection.
- Redraw candidate, 2026-10-09, the leader outside the logger's reach: B's pinned listings fall outside the logger's per-session
  candidate pool on most new-buyer sessions, so its new-buyer guardrails are not identified and B cannot be certified (#13, G15,
  guard PASS). Dropped before registration: it fails Gate G's instrument repair (a logger able to draw B's rankings observes the
  decision's quantity directly and the task collapses, the 89 v6 dead shape), and it carries an arithmetic symptom, B's
  self-normalising weight sum at a fraction of the session count, visible to any solver who prints the normaliser or the
  unnormalised estimate beside the normalised one.
- Other decisive moves screened at the redraw and rejected on paper: carrying a correct pooled lift onto the Q1 traffic mix (the
  transport driver of task43 iteration A, task44 v2 and task83); habituation measured from each buyer's prior exposure count (task83's
  conditioning on each unit's own treatment history); shared unique listings depleted across buyers (task106's shared-pool driver);
  the Q1 control being a retrained incumbent (a dated release-calendar line that asks the question for the solver); and a test-power
  or clustering argument (G2 is banned against task120 and G17 is supporting only).
- Design stage, 2026-10-09, grading the draw's 48 guardrail cells as the shape's grid: rejected on the pair
  arithmetic. The guardrail read is on the main call's path and on the kept basis only B's row moves out of its
  bins, so the response that lands E keeps all 48 and the best response that stops at B keeps about 40; the pair
  sits above 50 on paper. The grid became each policy's fee income by cell, and the guardrail moved to hatching.
- Design stage, 90 per cent lower bounds as graded figures and as the lift condition: rejected. A delta-method bound
  and a bootstrap bound differ in the first decimal, and B's kept bound sat at +0.4 against a zero bar, a knife
  edge on the runner-up. All three conditions became point rules with stated margins.
- Design stage, a fee charged once per checkout and repeated on every order line (D6) as the grid's primary:
  rejected. Splitting a bundle's fixed fee between the carousel order and the other items in the same checkout is an
  allocation fork on every bundled cell.
- Design stage, refunds on cancelled orders as a fee-path device: rejected. Cancellations visible on the ask path
  invite taking cancelled orders out of the main call's lift, a fork on a graded figure.
- Design stage, the offers clock (UTC acceptance against local checkout at a 24-hour expiry) as a hazard: rejected on
  magnitude, about 0.4 per cent on a cell, inside the one-decimal bin.
- Design stage, shipping each archived session's follow-up orders so the archive is blind by construction in the
  pack: rejected. The column names the other outcome and hands route 1 over; the archive ships in-session orders
  only and the blindness is asserted in the generator with the hidden follow-ups.
- Design stage, a first-time-seller ask on a prior-account chain (D7): dropped for this pack. Its construction layer
  is level (B's brought-forward orders rarely go to first-time sellers) and its two files take the pack past 24;
  kept in reserve as an ask device for a hardening loop.
- Design stage, the draw's four-rung sketch (A, C, B, E) carried as the ladder: below the pipeline's five-rung floor,
  because replay and per-render weights both named A, so the two refused estimators were one rung. Split by giving
  the logger's D allocation to the pickup cities (replay over the render rows names D) and A its gain in long
  sessions (render weights name A); every leader is still a different policy.
- Build stage, 2026-10-09, the design's render-weights figures for B (8.31 in-session, 7.70 kept): infeasible.
  With B's session-weighted borrowing at 4.73, the render-weighted borrowing cannot fall below 4.73 x 150,400 /
  404,990 = 1.76 even with every borrowed order in a single-render session, so B's render-weighted kept could
  not exceed 6.55 and the render/eight-cells/kept grid cell would not name B by 1.15x over E. Repaired in the
  data rather than the ladder: B's added new-listing orders rise with session length in the new-buyer cells, so
  B's render-weighted in-session figure is about 9.0 and its render-weighted kept about 7.0 (1.20x over E), and
  A's render-weighted figure rises to about 11.0 to keep rung 1's margin at 1.22x over B.
- Build stage, 2026-10-09, the design's 90 per cent bound check (a bound above zero passes B, D and E and fails F):
  dropped. On the kept basis every policy's per-session outcome includes three weeks of orders, so a delta-method
  bound straddles zero for every policy and the sentence would be false; the charter's conditions are point rules
  and the charter says so, which is the closure, and no assertion claims a variance result.
- Build stage, 2026-10-09, organic watched-listing exposure for the five rankers that do not read saves (the design's
  "plus 0.03 of organic watched exposure" and borrowed 0.06 to 0.30 for A, C, D, E, F): dropped. Route 1 and route 2
  agree to the order and to the cent only if each (cell, ranker) group's in-session watched purchases are a
  multiple of eight with five in eight bought anyway; at an organic purchase rate of 0.1 to 2.3 per 1,000 a group
  of 400 to 3,000 sessions can only hold 0 or 8, so one octet put 3 borrowed orders per 1,000 into a single cell
  (F, web 30-179) and erased F's young-to-old spread that the restatement device needs. Now only the velocity
  boost's build shows a buyer's watched listings (every other ranker, archived ones included, draws from a pool
  that leaves them out, which is also why no archived test could see the borrowing); the other five policies' kept
  and in-session figures are equal, and the decomposition applied to B alone files E at 5.7, a cracker.

- Build stage, 2026-10-09, the design's assertion 13 as written (any segment's anyway rate, applied to every
  session, files the same kept figures): infeasible. B's kept lift moves about 7.5 per 1,000 per unit of the rate, so
  a segment 0.008 off the pooled 62.5 per cent (four-render sessions, 63.3) nets B to 3.25, across its bin edge, and
  no position of B inside its bin survives a spread of 0.01 either way. Replaced by the readings a solver actually
  runs: every segmentation netted stratum by stratum (cell, ranker, cell by ranker, platform, tenure band, renders,
  watch-list size, weekday, ISO week, half) and each natural sub-population's rate (incumbent arm, velocity arm,
  each platform, each half, one-render and up-to-two-render sessions) applied to every session, all filing E 5.7
  and B 3.3; the most extreme single segment applied everywhere is recorded as the thinnest boundary, not asserted.
- Build stage, 2026-10-09, the two halves of the logged window stratified on in-session outcomes only: each
  policy's kept lift differed between the halves by up to 12 per 1,000 (B 9.4 against -2.8), because three weeks of
  background orders per session fell at random between the halves, which hands a solver who checks stability a
  reason to distrust route 1. Equal half sums of in-session and 21-day orders per (cell, ranker) then still left C
  and D 0.4 to 0.5 apart on the kept basis, because a group with an odd session count puts one more session in one
  half and a kept base of about 1.8 orders a session moves that half's mean. Now each group's halves hold the same
  mean of both counts to within one order, the odd orders and sessions placed by a search that matches each
  ranker's half gap to the incumbent's; every policy's halves agree within 0.09 on either basis.
- Build stage, 2026-10-09, placing the fee cells by whole-euro price moves on plain orders alone: could not carry
  the price-paid device out of the bin where the arm's accepted-offer discount per session matched the
  incumbent's (shifts of -0.008 to 0.034 in five cells), and in two cells the January row and the asking price
  cancelled. Replaced by three levers on the cell's own in-session orders, searched together: a plain order's price
  moves the figure and every reading alike, the asking price of an order bought on an accepted offer moves only the
  asking-price readings, and the price of an order paid in person moves only the readings that charge it; every
  one of the seven device combinations and the natural read now clears all 48 cells, the two under EUR 1.00 included.
- Build stage, 2026-10-09, the slot-total placement as first written scored distance from the round hundred, which
  pushed the totals toward the bin edges (A's orders sat 14 from one). Now scored on distance to the edges, 20 to
  45, with every wrong reading of every total at least 5 outside its hundred.
- Build stage, 2026-10-09, the pooled-lift stop on ask 2 (one pooled kept lift times the planned total) against a
  planned Q1 cell mix that matched the logged summer mix: it filed the same hundred as the cell-by-cell total for
  B, C, E and F (4 to 23 orders apart). The weekly table now carries a January new-buyer surge in both years (the
  0-29 band peaks 8 points above its base share in early January, the 30-179 band 4 points), which puts the pooled
  and cell-by-cell totals at least 138 orders apart for every policy before placement.
- Solver round 1 (plain, 2026-10-09), the five-rung build as shipped: LANDED, proxy 89.8, asks 6 of 8. The solver walked every
  rung without friction and executed the decisive one at its step 6 as a work order: "Lift outcome: all orders by the buyer (any
  channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days. HC-33 pins watch-list
  listings in tiles 1-2, which cannibalises favourites/alerts orders in the 180+ tenure cells, so its net log-mix lift is 3.30
  against a gross carousel lift of 7.96." The charter's lift definition (orders during the test, every channel) plus a shipped
  all-channel order file keyed by buyer makes the any-channel window the default outcome, so the netting is never a construction.
  It also kept every ask figure (48 fee cells, 12 totals), and it weighted the headline to 5.8 on the slot mix against the
  golden's 5.7 on the logged mix while using the slot mix for the totals, a determinism finding on the headline basis.
- Harden loop 1, diagnosis of round 1 (the borrowed-order netting as the decisive rung; P1 in-person pickups, P2 the R2
  restatement, HZ1 the deferred tariff, HZ2 the price paid and HZ3 the app gating as the ask devices): the decisive quantity
  was the charter's own observable, so the solver never had to think of borrowing at all. Its "Lift outcome: all orders by
  the buyer (any channel) within 7 days of session start, from orders_enrolled_buyers. The result is identical at 14 days"
  is charter 2.2 executed on the one extract that already holds every order by buyer, and the netting of B fell out of it as
  a by-product ("which cannibalises favourites/alerts orders in the 180+ tenure cells"). Every ask device died the same way:
  each organ sits in a file the ask's own path opens with its rule beside it ("recomputed at the 1 Sep 2026 tariff ...
  because KB-2027-01 was deferred", "Pickup orders paid directly carry no fee", "R2 restatement 2026-W01..W12 (it matches the
  account-service tenure), app only from W03 because of the release 27.1 gate"). Dead: a decisive rung whose correct basis
  is the definition's own observable on a shipped extract, and an ask device whose rule is filed in a document the ask path
  reads anyway. What the trace holds fixed without checking is that the logger's in-session columns measure the charter's
  quantities whenever the charter is not about orders over the test (its guardrail is read "from ordered_tiles"), which is
  where loop 1 goes. Harden loop 1 of 3 on this architecture.
- Harden loop 1, the come-back orders credited to the session the tile was in (home_session_id = the logged session): the
  habitual tie between ordered_tiles and the carousel orders credited to each session then failed in 202 sessions, every one
  outside C, an arithmetic symptom on the wrong path that points straight at the device. Now each come-back is credited to
  the session it was placed in, the tie holds in all 150,400 sessions, and the field reference's seven-day rule lets the
  listing alone attribute the order to its tile.
- Harden loop 1, no come-back orders at all under C: one zero in a by-arm count reads as a marker; C now comes back at 0.15
  of the others' rate (3 orders, none in app 0-29).
- Harden loop 1, charter 2.4 as written ("its orders placed from a home carousel tile"): it also admits every carousel order
  by the arm's buyers in a window, a reading under which C passes and is filed; 2.4 now counts the orders placed from the
  carousel tiles the arm served.
- Harden loop 1, the January new-buyer surge at 8 and 4 points (built for the pooled stop on ask 2): it put the slot-mix
  headline at 5.8 against the logged window's 5.7, round 1's determinism finding. Cut to 2 and 1 points, the headline
  converges (5.716 against 5.697) and the pooled totals fall 14 to 41 orders from the cell-by-cell ones for B and E, which
  no placement can carry out of the hundred, so the pooled stop is retired: pooled readings are placed at least 5 from the
  edges on either side and recorded.
- Harden loop 1, every fee reading as a stop on ask 2: B with only P1 mishandled and F on the first release alone sit 25
  and 14 euros from their golden totals, under the 25 a stop needs with the golden 20 from its edges; both are carried as
  either-side readings at least 5 from the edges (both inside) and the placement reached 6.4 of slack.
- Harden loop 1, fee cells placed anywhere from 0.35 to 0.65 of the bin: 7 of 48 landed within 0.003 of the round
  one-decimal value (7.0001, -14.5997 and so on), a receipt; the window now leaves out the middle tenth.
- Harden loop 1, a fresh silent device for the order totals (the logger slice held out of slot arms, a weekly table
  counting home sessions rather than carousel sessions, Easter falling in the slot's last week, staff and monitor
  accounts in the weekly table): each needs a new organ on the traffic path or a rate the pack cannot pin, or reads as
  sabotage; the order half keeps P2 and HZ3 and the pair arithmetic counts it as leaking to both sheets.
- Harden loop 1 as built, graded in the re-run of round 1 (labelled "round 2, plain", 48.7, call missed, 3 of 8 items):
  the tile count held the call (the solver filed C at 9.8 with E as runner-up, its step "Guardrail on the in-session
  carousel order rate: the only breach is HC-31 in web 730+" never sees rung 3), but the ask layer leaked exactly as the
  stated exposure said: "This reconciles exactly to the Finance Q3 sheet (the 6,147 July shipped orders missing from
  payments supply EUR 8,205.17)". Reading the referee settled F1 (VAT out) and F2 (balance purchases charged), so all 48
  fee cells and all twelve totals landed. A referee that ties to the cent only under the golden fee basis is a recipe
  the solver reconciles to, not a silent organ; the fee devices cannot rest on the referee going unread.
- Harden loop 2, diagnosis of round 2 (loop 1's ask layer: F1 fee income net of VAT and F2 balance purchases charged as the
  silent primaries, P1, HZ1 and HZ2 stacked on every fee figure, P2 and HZ3 on the totals, and Finance's Q3 statement as the one
  referee, tying to the cent only under the golden fee basis): the tile count held the call, and every fee figure fell to one
  reconciliation, in the solver's words at its step 7, "Fee income is taken excl. 21% VAT. This reconciles exactly to the Finance
  Q3 sheet (the 6,147 July shipped orders missing from payments supply EUR 8,205.17)". A statement scoped to the extract's own
  buyers that ties to the cent under exactly one fee basis arbitrates all five fee devices at once and hands over the level,
  which is the oracle law 8 bans, not a referee; every device it did not settle was a filed rule the path reads ("KB-2027-01 was
  deferred by the 6 Oct pricing committee", "uncaptured pickups were paid directly and carry no fee", "app uses W03 to W12
  because the first app release on or after 4 Jan 2027 is 27.1"). Dead: a fee device whose correct handling is also the only
  basis on which the logged window's statement ties. Harden loop 2 of 3.
- Harden loop 2 build, the in-person price lever as single-euro moves within plus or minus 30: it moves only the full-cover
  half of a cell, and F app 730+ (23 in-person orders) could then clear its bin by no more than 0.0035; the lever now moves
  up to 3 euros an order over plus or minus 60 units, applied round robin across the cell's orders.
- Harden loop 2 build, traffic readings within 30 of a hundred's edge treated as stops: B's fee total with only the cover
  change mishandled sits 6.3 inside its hundred and no set of traffic factors carried every stop out (the placement score
  stayed negative); the near band is 40 and the readings in it are either-side readings, B's FX-alone total among them
  (recorded as kept by round 2's path).
- Harden loop 2 build, every fee reading at least 0.03 outside its bin: D app 0-29 with only the January row applied can
  sit no further than 0.0246 outside, because the two tariffs differ too little on that cell's orders for the price
  levers to widen it; the floor is 0.02.
- Harden loop 2 build, VAT taken off order by order converging without a lever: on an early placement one B web cell's
  per-order rounding fell 0.0031 outside the golden bin; a pair lever (plus and minus one euro on two plain orders, which
  moves only the per-order rounding) was added, and on the final placement it needed no pairs (0.0227 inside at the
  nearest).
- Harden loop 2 as built, graded in the re-run of round 1 (labelled "round 3, plain", token proxy 51.1, call missed, 4 of 8
  items by token; read-corrected about 23 to 31, because notebook items 1 and 2 and image items 2 to 4 were credited on HC-37,
  5.7, HC-33 and HC-34 named in the solver's screen-out and negation sentences): the tile count held the call for the second
  round running (C filed at 9.8, E runner-up at a gap of 4.1, at the same step, "Condition (b), each cell's carousel order rate
  against HC-24: HC-31 web 730+ is -2.74% and fails. All other policies' cells are within -1.5% (HC-34 app 0-29 -0.96%)"), but
  loop 2's ask layer leaked whole again: all 48 fee cells and all six policies' twelve-week totals landed, at its step 8, "covered
  orders are shipped orders plus pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee
  excl. VAT exactly ... Tariff for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01", and at
  step 9 it read P2, HZ3 and the 1 March cover change straight off the filed notes. Dead: a fee basis that still ties Finance's
  Q3 statement to the cent (the referee survived loop 2 as an oracle under a new cover rule) and traffic and tariff devices whose
  rule sits in a document the ask path opens. Harden loop 3 of 3 on this architecture is the last before a re-root.
- Harden loop 3, diagnosis of round 3 (loop 2's ask layer: FX, the 1 March 2027 checkout change in the capacity note's
  overlaps section, as the fresh primary on all 48 cells and the six fee totals; F1 VAT, F2 balance purchases, HZ1 the
  deferred January row and HZ2 the price paid stacked on every fee figure; P2 the R2 restatement and HZ3 the app release
  gate on the totals; Finance's Q3 statement as the one referee, still tying to the cent on the logged window's cover): the
  call held at the tile count, and the whole ask layer fell to two habits the solver runs by default. It reconciled its fee
  model to the referee, which still ties the logged window under the golden's own per-purchase basis and so settles VAT,
  balance purchases and in-person pickups in one pass, in its words at step 8, "covered orders are shipped orders plus
  pickup orders captured by card or iDEAL, which reproduces Finance's protected orders and fee excl. VAT exactly ... Tariff
  for 2027 stays 0.80 + 5%, because the pricing committee minutes of 6 Oct defer KB-2027-01 even though the tariff register
  lists it"; and it executed every rule filed on the traffic path as a work order, at step 9, "The app arm starts 18 Jan
  2027 (release 27.1 after the code freeze), so app runs W03-W12 and web W01-W12 ... From 1 Mar 2027 (W09-W12) every
  pickup order is paid at checkout and carries the fee", so FX, built to sit off the fee path, was read in the same pass as
  HZ3 because both sit in the capacity note. Dead: a referee whose figure the golden's fee basis reproduces on the logged
  window (whatever changes for the slot, the statement hands over every logged-window device at once), and any device whose
  rule is a dated, named sentence in a document the ask path opens (the minutes, the release log, the capacity note), because
  the solver reads every note on its path and carries out what it says. Harden loop 3 of 3.
- Harden loop 3 build, the either-side band at 40 (a wrong total under 40 from its golden placed on whichever side of the
  edge it falls): infeasible on this pack. E's fee total has two compound readings on the twelve-week app traffic, one 52
  above the golden and one 55 below, and no placement keeps the golden 20 from the edges while carrying both out of a
  hundred-wide bin by 5 (best score -0.03 after refinement). The band is 56, which adds only those two readings.
- Harden loop 3 build, the traffic placement with every first-release total scaled linearly by the placement factors: the
  restatement's moves were counted on the placed table, so a placed cell's first-release sessions were not the factor times
  the unplaced cell's, and B's fee total on the first release with balance purchases uncharged and the logged checkout
  landed 0.21 inside its hundred's edge in the files against at least 5 predicted (the build stopped on
  ask2.every_reading_clear_of_the_edges.B). The moves are now counted on the unplaced table and added to the placed one, so
  a first-release total is the placed table's plus a constant and the placement is exact.
- 2026-10-10, retired: it passed both solver rounds after three hardening loops, but the determinism judge sent it back on Gate G: the answer wins only by reading the charter's outcome definitions in place of the logger's in-session reads (a single conceptual flip), and the shipped planning thread ranks the candidates. Under the author's standing rule a Gate G send-back is retired like a dead build, and DS11 takes the slot in a later wave.
- 2026-10-13, re-root under the 10/10 rules (v2 to v3): v2 is FAILED_TO_STUMP in perssathya's backlog. Its
  decisive step, the logger's in-session order column read against the charter's count of every order placed from
  the tiles an arm served, is a field read under a filed charter condition (data semantics plus rule application),
  and its estimator was pinned by nine certified archived tests (a validated decoy); a redesign inside the world
  would keep the carousel's nouns, and with app or retail nouns the slot question reads the same. The slot moves to
  Biomedical & Clinical Research, a domain never built.
- Re-root candidate, pharmacoepidemiology (new users of inhaled COPD treatments, time in hospital that the
  dispensing record cannot see): dropped on paper. The answer turns on the grace period and how inpatient days
  count against a supply, conventions a filed sentence would have to fix, and once fixed the step is rule
  application.
- Re-root candidate, protopathic bias with a long prodrome (a drug started for the early symptoms of the outcome
  it is then blamed for): dropped. The lag that decides is a convention the field disputes, so determinism rests on
  a pinned lag, and a solver who knows the drug class's literature reaches the answer from priors.
- Re-root candidate, criminology (reporting falls in hot-spot patrol areas): dropped; one obvious move (use calls
  from the public, not officer-initiated records), close to reading a field.
- Re-root candidate, assessment-time bias (progression found sooner in an arm scanned more often): dropped; the
  interval-censored estimate (NPMLE) is not unique and a solver's method choice moves the graded figures.
- Re-root candidate, eGFR off-treatment decomposition (the phase 3 end point read four weeks after the last dose,
  part of the early fall at the top dose not coming back): dropped as the decisive step. The natural construction
  (the week-56 off-treatment difference plus two more years of chronic slope) lands the golden, so it sits inside a
  strong solver's hypothesis space; with monotone dips and slopes, the one-year view and the slope-only view
  bracket the three-year answer, so in a pick of three one simple view always lands the call.
- Re-root candidate, a titration step at week 12 for the top dose (its further fall after the field's month-3
  knot read as a steeper chronic slope): dropped as the decisive step. The step is in the protocol and is a
  4.6 mL/min drop in one arm between two visits, a visible symptom a solver investigates; it also penalises the
  top dose in the same direction as the golden's dip, so the margins the conventional route needs are thin.
- Re-root candidate, slow drug accumulation (a long half-life, the haemodynamic fall deepening for five months):
  dropped. An exponential approach that is half done at month 3 is not finished by month 12, so no clean chronic
  window remains in 52 weeks, and one that finishes by month 6 leaves too little after month 3 to move the call.
- Re-root candidate, anti-drug antibodies (loss of response lagging antibody onset, so a 24-week maintenance read
  overstates week 52): kept in reserve, not drawn. The arm curves do not show the coming loss, which is its
  strength, but the projection rests on the loss distribution after onset estimated from a few early converters,
  and in a pick of three "fewest antibodies" or "the balanced regimen" lands the call by heuristic.
- Re-root candidate, detection bias through organ volume (a drug that shrinks the prostate makes biopsy more
  sensitive): dropped; the setting is the textbook case (the 5-alpha-reductase prevention trials), so a frontier
  solver recalls the resolution, and the adjustment's detection model is a fork.
- Re-root candidate, leaky against all-or-none vaccine protection carried to a high-transmission setting: dropped;
  the invariant-under-base-rate insight is task446's and task230's family, and the mechanism is identified only
  through a model of exposure.
- Re-root candidate, HbA1c lag (a 16-week dose-ranging read before glycation catches up): dropped on the swap
  test; the decisive move, the steady state of a lagged average, reads the same with a trailing business metric.

## Architecture v2 record (spent 2026-10-13)

Realised analytical_tasks note DS01 (carousel test slot); registered 2026-10-09 after checkpoint A, built, three
harden loops and five solver rounds, retired 2026-10-10 after a Gate G send-back, never submitted, then put in the
author's backlog as FAILED_TO_STUMP and re-rooted here.

| Axis | Value |
|---|---|
| Domain / subdomain | Product Analytics / experimentation-measurement |
| Objective | Experiment & Causal Analysis |
| Niche | a Dutch peer-to-peer second-hand fashion platform (Vouwlijn) choosing which of six registered ranking policies takes its home carousel's Q1 2027 A/B test slot, every policy scored off-policy on randomised carousel logs |
| Shape | 07 grid of cells |
| Decision type / unit | pick one of six policies (named option) |
| Gap / pattern / generators | time, rule, population; none, B; G13, G9, G16, G2, G11 |
| Gate G mechanism | decomposition_attribution |
| Stump strategy | decomposition_attribution; decisive rule filed, official decoy, validated decoy (nine archived tests pinned the estimator) |
| Calibration form | pilot_log |
| Stakeholder / forum / forcing / org family | head of marketplace science / executive_team / vote_or_meeting / software_or_platform |
| Deliverables | `carousel_slot_q1_2027.ipynb`, `carousel_slot_q1_2027_cells.png` |
| Answer | E, the sequence ranker with the fresh-listing interleave (HC-37), 5.7 extra orders per 1,000 carousel sessions |

Stump (harden loop 1 onward): a solver who scores the six policies with the session-weighted estimator that alone
reproduced the nine archived tests and reads the cell guardrail on the render log's in-session ordered tiles
commits the slot to C, the session-sequence model; the charter counts every order placed from the tiles an arm
served, and buyers under every other ranker come back to order from a tile left on screen after the session
closes, so C fails the guardrail in app 0-29 and E is the largest lift that clears every condition.

Fate: solver rounds 2 to 5 held below 52 after round 1 cracked the draw's rung; the determinism judge sent it back
on Gate G (the answer wins only by reading the charter's outcome definition in place of the logger's in-session
read, a single conceptual flip, and the shipped planning thread ranked the candidates). Under the 10/10 rules the
decisive step is data semantics and rule application, so the architecture is spent.
