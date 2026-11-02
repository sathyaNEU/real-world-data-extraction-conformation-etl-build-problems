# task307 design note

Architecture 2, a re-root drawn on 2026-11-02 in the same objective (Opportunity Sizing & Decision Support) and the
same number, at the orchestrating session's call. Architecture 1 (a metropolitan planning organisation's congestion
slot, decided by re-assigning trips to user equilibrium on each build network) was found spent at the 11-01 re-check:
its documentation 6.1 filed the HOW, so executing the scoring guidance gave the golden (rule application), and only
Actor held on the survivor anatomy. Its shipped pack stays at the portal, pending, untouched. This architecture moves to
another client domain, world, dataset and prompt shell, away from transport networks and trip assignment.

## Draw

- **Card.** `.claude/skills/fingerprint/cards/task307.json`, architecture v2, v1 moved into the lineage with its fate
  and shell. `guard.py check` at WARN only: `repeat.deliverables` (a board paper and its appraisal workbook is the set
  an NHS trust board takes, docx+xlsx, as task273 v5 did in another domain; answered here). The older same-puzzle and
  same-driver signatures (gap objective, decisive generator G1, pick one; Gate G binding constraint) are differentiated
  on the card against task118 v2 and v4, task184 v1, task198 v4, task472 v1 and task140, none of whose drivers is a
  two-pool shortage.
- **Pairing.** Healthcare Delivery & Health Economics (client domain) / `patient-flow-beds-workforce-optimization`
  (serves Opportunity Sizing in the taxonomy) / Opportunity Sizing & Decision Support. The headline is a sized
  opportunity, pool to realisable: the medical bed-days the 2025/26 winter lost to bay closures and to patients
  waiting to leave, and the share of them each scheme releases; it drives the call.
- **World.** Stourleigh Hospitals NHS Foundation Trust, an acute trust in the fictional county of Ellenmoor, England.
  The medical bed base at Stourleigh General Hospital is a set of wards built of six-bed bays and single side rooms;
  infection prevention and control (IPC) nurses infectious patients (norovirus and other diarrhoea and vomiting,
  influenza, COVID-19, RSV) in side rooms, and side rooms also hold patients at the end of life and known carriers of
  resistant organisms. Personas drawn with `guard.py names --geo UK --seed 307`: Hazel Doyle (head of patient flow and
  capacity, the appraisal's author), Kayleigh Howe (director of finance, the envelope's holder).
- **Decision and quantity.** One winter scheme for 2026/27 from the trust's candidate list: a modular ward of general
  beds, a same-day emergency care (SDEC) extension into evenings and weekends, a seven-day discharge team for simple
  discharges, and a palliative rapid-discharge partnership with the county hospice (hospice at home and fast-track
  continuing healthcare brokered within 24 hours of the decision). The trust's winter capacity framework files the
  WHAT: a scheme's benefit is the medical bed-days it would have released over the 2025/26 winter (1 December 2025 to
  31 March 2026) against the bed base as it ran, the slot goes to the largest benefit, and every scheme is reported
  with its benefit per £1,000 of winter cost. Forward facing: the scheme runs in the 2026/27 winter, appraised on the
  last complete winter as the framework's standard winter.
- **Shape.** 01, ranked list under the envelope: each scheme's released bed-days and bed-days per £1,000, the call,
  the runner-up and the gap, the chart's named bars, and the asks (`## Ask sheet`).
- **Strategy, Gate G, family.** `binding_constraint` (the side-room pool binds and removes the natural pick, as a
  removal that re-places nobody), Gate G `binding_constraint`, decisive generator G1 (what the bed base is limited by)
  then G7 (the moments the limit binds), Layer 2 family `allocation_constraints`, pattern
  `own:side-room-shortage-closes-bays-so-freed-side-rooms-release-bays`.
- **Default path (written first, short form).** The bed model counts each scheme's beds or the bed-days it removes from
  the stays it touches, with the medical beds as one pool: the modular ward's twelve beds over its opening days, the
  SDEC admissions it avoids, the weekend days simple discharges wait, the days fast-track patients wait for their
  package. Ends on the modular ward. Golden: the palliative partnership, because the fast-track patients it moves hold
  side rooms, and a bay with one infectious patient in it closes to admissions whenever every medical side room is
  full.
- **Data-native sentence.** The bed movements record which bed every patient held and the bed register which beds are
  side rooms, the IPC closure log records each bay closure and how many patients were symptomatic when it closed, and
  the palliative team's register records each fast-track decision; only together do they show that every closure with
  one symptomatic patient began while every medical side room was occupied, and that fast-track patients past their
  24 hours held some of those rooms at most such moments.
- **Abstraction sentence (the one a reviewer would say of this build and its nearest approved one).** A unit of a
  small specialised pool is worth a block of the large pool it keeps open while the small pool is full. Not writable
  against any approved build: task106 shares a pool across candidates (double-booking), task303 removes a shared loss
  logged per unit, task308 values a unit by the outages it shares, task120 nets storage out of production, task127
  (same task type) splits one patient's concurrent waits; none values a scheme through a sub-pool whose shortage
  closes blocks of the main pool.
- **Candidates screened at this draw (each with its default path, swap test, anatomy and bin test; the dead ones are
  also in `## Tried and rejected`).**
  1. *Collections (banking, collections-recovery): keep or sell charged-off segments, in-house recovery read with sold
     accounts censored.* Default: the life-table recovery curve with sales as censoring files keep-in-house for the
     card segment; swap passes (debt sale is collections' own); anatomy: Actor and Link fail (the sale tranche is a
     column); bin: the stratified life table is a grouping (stumping 1.1c). Dead: `ban.strategy` (population
     selection is task273's) and the grouping dichotomy.
  2. *Subscriptions (product analytics, churn-propensity-uplift): a payment-recovery upgrade credited with the voluntary
     cancellations a failed-payment notice triggers.* Default: the cancellation reason codes size the save offer
     first; swap passes; anatomy: Back-test fails (a pilot's retention ITT lands it); bin: without the pilot the
     triggered share is a model with a free baseline window. Dead on Gate C.
  3. *Anticoagulant switching (pharmacology, benefit-risk): the 2027 switch cohort sits in the early-bleeding months.*
     Default: annual rates per patient-year file the oldest group; swap passes; anatomy: Reflex fails (one-year
     cumulative incidence from past switchers lands the golden); bin passes. Dead on Gate F and on its honest label
     (composition by time since initiation, banned in the window).
  4. *Retention (product analytics or actuarial lapse): customers migrated at a system go-live only if active, so a
     curve from origin ignores delayed entry.* Default: Kaplan-Meier from start date files the loyalty programme; swap
     passes; anatomy holds on paper; bin passes (one estimator). Dead: honest label population selection (survivorship),
     banned in the window.
  5. *A clash cover (actuarial, reinsurance-capital): motor and home claims from one storm in two claims systems.*
     Default: per-line models with an annual correlation file the per-line cover; anatomy: Pins fail (the treaty's
     occurrence clause files the unit). Dead on the WHAT screen and on the dependence fork.
  6. *A long-short sleeve (quantitative finance, portfolio-construction-risk): shorts the prime broker cannot locate.*
     Default: the backtest's alpha files the small-cap sleeve; anatomy: Reflex and Second use fail (borrow cost is a
     quant default; the locate file exists only for the step). Dead.
  7. *A discharge lounge (healthcare, patient-flow): bed-hours released only count when an ED patient is waiting.*
     Default: bed-hours released one for one; anatomy: Reflex fails (boarding by hour is one group-by). Dead, and close
     to task127's world.
  8. *A booking line (healthcare, workforce): redials inflate offered calls in an Erlang sizing.* Dead on Gate C (a
     retrial queue carries a free persistence parameter).
  9. *Blood pressure programmes (epidemiology, health-burden): regression dilution in the cohort's slope.* Dead: the
     usual-BP relative risks of the literature land it, and the swap reads the same in any field with noisy exposures.
  10. *A ticketing tier (marketing, conjoint and choice): sold-out options narrow the observed choice sets.* Dead: the
      substitution is task302's, and the choice model's specification forks.
  11. *Delinquency (banking, collections): month-end snapshots hide episodes that cure inside the month.* Dead: the
      step is a grain reading.
  12. *A schools vaccination programme (epidemiology, health-burden): household secondary cases.* Dead: honest label
      causal design (spillover), task157's, banned in the window.
  13. *A side-room pod among the candidates (this world).* The mechanism kept, the candidate dropped: a scheme that
      adds side rooms names the step.
  The strongest, this draw, was prototyped in code before carding: across four seeds the bed model files the modular
  ward (12 beds over 107 opening days, 1,284 bed-days) with the palliative partnership last on its own waits (about
  400 to 470), while crediting each scheme with the single-patient closures it would have kept open files the
  partnership at about 1,550 to 2,140 (generator/checks.py carries the analyst test once the generator exists).

## Survivor anatomy

Written at the draw, measured again on the cut pack at stage 3.
Actor: whether a bay closure began while every medical side room was occupied, and which of those rooms a scheme would
have emptied by then, sits in no column of any file; it is a relation between the closure's start and the bed
movements of every side room at that moment.
Link: the IPC log names a closure by ward name and bay letter at a clock time, the bed movements carry bed codes, and
the palliative register carries the hospital number with its own decision time; the comparison of a closure's start
with side-room occupancy at that minute is one the bed model never asks for, and no key offers it.
Reflex: the field's own sizing, the bed model with the medical beds as one pool (added beds times days, bed-days taken
out of the stays a scheme touches), is rung 0 and files the modular ward.
Back-test: the capacity team's bed model, run on beds as one pool, reproduces the 2025/26 winter's occupancy at the
23:59 bed state, so the pack's own validation confirms the easy route (to be built and measured at stage 3).
Second use: the bed movements are the spine (occupancy and every ask's base), the bed register is the bed base, the
IPC log is the bed state's record of closed beds, and the palliative register is how the default path sizes the
partnership's own waits; none sits in the pack for the decisive step alone.
Shock: closures are ordinary winter events, about one every day and a half, spread across wards and months; the
partnership ranks last or next to last on every statistic the pack ships.
Pins: the framework files the WHAT (benefit, window, comparison, award rule, the per-£1,000 report); no filed sentence
names side rooms, isolation, closures or the moments the side-room pool is full.

## Default path

The route a capable analyst takes with every file read and every filed rule executed:

1. Reads the winter capacity framework: a scheme's benefit is the medical bed-days it would have released over the
   2025/26 winter against the bed base as it ran; the slot goes to the largest benefit; each scheme also with its
   benefit per £1,000.
2. Takes each scheme's specification from the scheme workbook and sizes it with the bed model, the medical beds as one
   pool: the modular ward as twelve beds over its opening days (about 1,280 bed-days); the SDEC extension as the
   bed-days of the short-stay ambulatory admissions it would have taken (about 700); the seven-day team as the days
   simple discharges ready at a weekend waited for a weekday (about 1,000); the palliative partnership as the days
   fast-track patients waited beyond 24 hours after the decision (about 420).
3. Divides by each scheme's winter cost and awards the largest benefit.

Ends on: the modular ward, about 1,280 bed-days.
Golden: the palliative rapid-discharge partnership, about 1,800 bed-days (its own waits plus the closed beds of the
bays that stay open because the rooms its patients held are free when every medical side room would otherwise be
full); the modular ward next.

## Stump sentence

A competent analyst sizes each scheme with the bed model, the medical beds as one pool, and funds the modular ward at
about 1,280 bed-days; the step that lands it there is counting a side room as a bed, when an infectious patient can be
nursed only in a side room, a bay with one in it closes to admissions whenever every medical side room is full, and the
palliative partnership empties side rooms held by fast-track patients, so it keeps those bays open and releases about
1,800.

## Three rules

Task type: healthcare-delivery-health-economics / patient-flow-beds-workforce-optimization (OS): one winter scheme for
the medical bed base, sized by the bed-days it releases.
Domain test: the deciding quantity is the medical bed-days a scheme releases over the winter, which bed planning
estimates by replaying the winter's bed use with the scheme in place; infection control makes side rooms a separate
pool that infectious patients alone may use and whose shortage closes a whole bay, so what a scheme releases turns on
the side rooms it frees at the moments that pool binds.
Swap: "fund the classroom scheme whose freed seminar rooms keep lecture halls open" keeps the sentence and loses
isolation, bays, infection control and end-of-life care; no other field closes a block of its main resource because a
small specialised pool is full.
Layer 1: patient-administration bed movements by bed code with ward codes renamed part way through the year, the IPC
closure log by ward name and bay letter, a 23:59 bed state that crosses the October and March clock changes,
microbiology results keyed by NHS number against the hospital number, the palliative register's decision times
entered after the fact, a scheme workbook in each sponsor's own units. Each is what a hospital's systems produce; none
moves the call (asserted in checks.py as the R2 block).
Layer 2: capacity under a binding sub-pool: a scheme's released bed-days are what the bed base gains with it in place,
and the side-room pool's shortage closes bays, so a scheme that empties side rooms at the moments they are all full
keeps bays open that the bed model never sees.
Decisive step: crediting each scheme with the closed bay beds it would have kept open, by checking each closure that
began with one symptomatic patient against side-room occupancy at that moment and the rooms the scheme would have
emptied by then, instead of counting a side room as a bed.
Not semantics: every room type, closure reason, symptomatic count and decision time can be read right and the bed model
still counts the partnership's own waits only; no field, code or definition says a closure followed from a full
side-room pool or that a scheme's patients held the rooms.
Not rule application: the framework files the estimand and the award rule and no document says how a closure arises or
how a scheme's benefit is built; executing every filed rule with the bed model files the modular ward. The enumerated
family (the bed model, the bed model with the ward's own closures netted, the partnership's own waits at the
brokerage's real start dates, crediting every closure in the IPC log to every scheme that frees a side room, the
closure-by-closure check) spreads the partnership from about 420 to about 2,300 bed-days and the call across two
schemes; the data's own absolute split (every single-patient closure began with every medical side room occupied,
every closure that began with a room free had two or more symptomatic patients) leaves the closure-by-closure check
standing, with a spread to be measured at stage 2 under the pool and timing conventions the fork table closes.
Analyst test: a strong analyst who reads every record and the framework correctly sizes each scheme with the bed model
and funds the modular ward at about 1,280 bed-days; the golden credits the bays each scheme keeps open and funds the
palliative partnership at about 1,800 (generator/checks.py, R3a, once the generator exists).
Estimand: the winter capacity framework (2026/27), section 3, files the population (the winter's medical bed base and
its patients as they ran), the outcome (medical bed-days released), the window (1 December 2025 to 31 March 2026),
the comparison (the bed base as it ran against the bed base with the scheme in place) and the unit (bed-days, and per
£1,000 of the scheme's winter cost); section 4 files the award rule.
No decoy: nothing is planted; the closures, rooms and decisions are the winter as the hospital ran it, and no memo,
sponsor figure or draft ranks the schemes.
No certified replay: no certified or published figure is reproduced to recover a hidden method; the framework states
the estimand and the records carry the evidence.
Lesson: a hospital's medical beds are not one pool when infectious patients may use only side rooms; a scheme is worth
the bays it keeps open by freeing side rooms when they are all full, which no bed count shows. No build on file teaches
a sub-pool shortage that closes blocks of the main pool.

## Tried and rejected

- 2026-10-27: OS09 (a mini-split rebate programme's net first-year savings) left at the draw: its honest
  stump labels were all held by the guard window and its furniture barred; moved to another domain.
- 2026-10-27: a resource adequacy design (cold-correlated forced outages, four capacity offers) prototyped
  and dropped before registration: task308's architecture 3 registered the same world and driver first.
- 2026-10-27: screening yield by time since the last screen dropped on paper as an echo of task301's
  yield-by-record-age driver.
- 2026-10-27: the planning time index ask (probe stamps marking the interval end as its silent device) dropped at
  stage 4: the judge read the stamp convention as an unfiled fork, and filing it hands the ask to every reader.
- 2026-11-01: architecture 1 found spent at the re-check under the new gates: executing guidance 2.1 with documentation
  6.1 (user equilibrium on the coded network) is the golden, so the analyst test fails and the decisive step is rule
  application (generator/analyst_test.py); the survivor anatomy holds only Actor. Not re-rooted on the orchestrating
  session's rule; the shipped pack stays at the portal, pending.
- 2026-11-02: re-rooted at the orchestrating session's call: architecture 1 died because 6.1 filed the HOW, so
  executing the guidance gave the golden, and only Actor held; architecture 2 moves to healthcare patient flow, a new
  world, dataset and shell, with no governing document filing the method.
- 2026-11-02: debt-sale censoring of an in-house recovery curve (collections) dropped at the draw: population selection
  is banned in the window (task273) and stratifying by the sale score is the grouping dichotomy.
- 2026-11-02: failed-payment notices triggering voluntary cancellations (subscriptions) dropped at the draw: a pilot's
  retention ITT lands it, and without one the triggered share is a model with a free baseline.
- 2026-11-02: an early-bleeding window for a 2027 anticoagulant switch cohort (pharmacology) dropped at the draw: the
  one-year cumulative incidence from past switchers is a reflex that lands it, and its honest label is banned.
- 2026-11-02: delayed entry at a system go-live (retention) dropped at the draw: its honest label, population
  selection, is banned in the window.
- 2026-11-02: cross-line common shocks for a clash cover (reinsurance) dropped at the draw: the treaty's occurrence
  clause files the unit (the WHAT screen) and the dependence model forks.
- 2026-11-02: short-borrow availability capping a long-short sleeve (quantitative finance) dropped at the draw: borrow
  cost is a quant default and the locate file would exist only for the step.
- 2026-11-02: bed-hours from a discharge lounge counted only when an ED patient waits (patient flow) dropped at the
  draw: boarding by hour is one group-by, and the world sits on task127's.
- 2026-11-02: redials inflating an Erlang sizing (a booking line) dropped at the draw: the retrial queue carries a free
  persistence parameter.
- 2026-11-02: regression dilution in a blood-pressure slope (health burden) dropped at the draw: the literature's
  usual-BP relative risks land it and the swap reads the same in any field.
- 2026-11-02: sold-out options narrowing observed choice sets (choice modelling) dropped at the draw: task302's
  substitution, and the choice model's specification forks.
- 2026-11-02: month-end snapshots hiding intra-month delinquency (collections) dropped at the draw: a grain reading.
- 2026-11-02: household secondary cases credited to a schools vaccination programme dropped at the draw: causal design
  (spillover) is banned in the window (task157).
- 2026-11-02: a care-home discharge-to-assess partnership as the scheme that frees side rooms, prototyped and replaced
  by the palliative partnership before carding: its vocabulary and world (care-home waits, medically optimised dates,
  discharge-to-assess) sit on task127's.
- 2026-11-02: a side-room pod as one of the candidate schemes dropped at the draw: a scheme that adds side rooms names
  the decisive step.
