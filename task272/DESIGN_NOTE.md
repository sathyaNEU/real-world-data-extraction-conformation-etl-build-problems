# task272 design note: a hospital pharmacy's batch-compounded doses against their volume tolerance (architecture 3)

Architecture 3, drawn 2026-10-31 after architecture 2 (the Vellacott Health Foundation's coaching grants) was spent at
stage 4 and retired again by the batch audit. Earlier architectures' sections are retired; their records and their
lessons stand below and in Tried and rejected.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task272.json`, architecture v3, registered 2026-10-31 after a
  fast-forward to main, guard WARN only: `people.first` (Cynthia, an older build's first name), `repeat.gate_g`
  and `repeat.deliverables` against task172. The structural signature (population, G7, method_or_model_selection)
  repeats three lineage architectures and is differentiated against each (task271 v2, task308 v1, task471 v1); the
  nearest ideas are differentiated too (task229 v2 at 0.08, task482 v8, task252, task274).
- **Pairing.** Client domain general-statistics-data-science, task type
  exploratory-data-analysis-distribution-assessment (which serves Descriptive & Distribution Analysis), objective
  Descriptive & Distribution Analysis: each product's distribution of delivered dose volumes over 2026 is assessed
  against its volume tolerance, and the tail beyond the tolerance decides the call.
- **Niche.** Ashcombe Valley Health, a regional hospital in Ontario, batch-compounds ready-to-administer syringes and
  bags for its wards and theatres in the pharmacy's sterile compounding unit on three peristaltic compounders (PC-1 to
  PC-3), a syringe-driver compounder (PC-4) and a gravimetric compounder that weighs every dose (GC-1). Each set is
  calibrated gravimetrically at set-up; the unit's procedure weighs the first dose of each batch and then every
  hundredth syringe or twentieth bag; a weighed dose outside tolerance stops the batch, every dose made since the last
  conforming check is weighed (a quarantine sort) and the set is replaced. The procedure lets a set carry further
  batches of one product inside 24 hours of its set-up. The IV workflow system goes live on 5 April 2027 and weighs
  every dose of the products configured for gravimetric verification at cutover.
- **Decision.** Which batch-compounded products are configured for 100 percent gravimetric verification at the
  cutover (a designation set). Forward facing: the configuration governs every dose from April 2027; the policy reads
  it on the last full calendar year, so the estimate is of 2026 and the reason is filed in the policy.
- **The quantity.** The pharmacy's quality policy files the WHAT: a product goes onto verification of every dose
  where its out-of-tolerance doses in the last full calendar year exceeded 10 in every 100,000 doses made, an
  out-of-tolerance dose being one whose delivered volume lay outside the product's volume tolerance, whether or not
  it was weighed or quarantined.
- **Data-native sentence.** Each set's delivered volume falls with the litres its tubing has pumped since the set-up
  calibration, and the procedure lets a set carry consecutive batches of one product, so the doses at the end of the
  sets that carried a third batch sit furthest below target, after that batch's last weighed dose; a capability study
  of the weighed doses reads them as one stationary spread.
- **Default path.** A capability study of each product's 2026 weighed doses: the overall mean and standard deviation
  of the delivered volume and the normal tails beyond the tolerance, the reflex of a process performance study.
- **Golden.** Each dose placed on its set: the product's loss per litre pumped and the set's start (varying from set
  to set about its mean) read from the weighed doses, each dose's probability of lying outside the tolerance at the
  litres its set had pumped, summed over every dose made and stated per 100,000: cefazolin 2 g, cefoxitin 2 g,
  phenylephrine and midazolam.
- **Shape.** 14, cuts of a distribution: each product's distribution of delivered volumes cut at its tolerance
  limits, the share outside per 100,000 doses made, charted against the line of 10.
- **Shell.** Question form which (the corpus quota WARN), deliverables pdf and csv (WARN against task172), forum the
  Director of Pharmacy (`line_manager_or_team`), forcing event the IV workflow cutover (`cutover_or_migration`),
  organisation family `hospital_or_health_provider`, context artifact the unit's gravimetric check register
  (`register`), all clear of the last three builds.
- **Personas** from `guard.py names --geo "Canada" --seed 272`: Cynthia Underwood (Director of Pharmacy), Erin
  Stewart (the unit's quality pharmacist), Jacob Burgess (the unit's lead technician), Spencer Frank (the IV
  workflow project lead).
- **Screens, run as code before the pack was cut.** In units of the dose-to-dose scatter, sets changed before the
  loss reaches the band leave the textbook normal fit at hundreds per million against truths near zero, while the
  rare long runs carry truths far above anything the weighed share or the sorts see. The built world was then screened
  across eighteen seeds: the call held on every one under every member of the family, the capability study filed the
  bags on every one, and the seed was chosen where the pooled Johnson fits, the weighed share and the sorts each file
  a wrong set too (seed 27267); `generator/checks.py` asserts each rung's set on the cut pack.

## Default path

1. Read PH-QP-07 sections 2 and 3.1: each product filled on PC-1 to PC-4 is configured for gravimetric verification
   of every dose where its 2026 out-of-tolerance rate exceeded 10, the rate being the doses made outside the
   product's volume tolerance, weighed or not, per 100,000 doses made.
2. Conform the check register: each weighed dose's delivered volume (the gross weight less the container tare to 30
   June, the net weight from 1 July, divided by the specific gravity) as a per cent of the labelled volume.
3. Count each product's completed fills in the server's dose log, the denominator.
4. Run the capability study each product's weighed doses invite, the field's way of turning in-process weights into a
   nonconforming rate: the overall mean and standard deviation of the per cent deviation and the normal tails beyond
   the tolerance, the rate a Ppk implies, per 100,000 doses made.
5. Configure the products over 10.

Ends on: P0431, P0610, P0614, P0618 and P0702 (cefoxitin 2 g, the three bags and midazolam)
Golden: P0412, P0431, P0507 and P0702 (cefazolin 2 g, cefoxitin 2 g, phenylephrine and midazolam)

## Stump sentence

The default path runs the textbook capability study on each product's 2026 weighed doses and configures P0431, P0610,
P0614, P0618 and P0702, the three bag products whose sets start high and lose about four per cent over a batch among
them, while cefazolin 2 g (P0412) and phenylephrine (P0507) read near zero; the step that lands it there is reading
the weights as one stationary spread, when every dose's volume falls with the litres its set has pumped since its
set-up and the sets that carried a third batch end below the limit after their last weighed dose, so only the doses
rebuilt set by set name P0412, P0431, P0507 and P0702.

## Three rules

Task type: exploratory-data-analysis-distribution-assessment (General Statistics & Data Science), which serves Descriptive & Distribution Analysis: each product's distribution of delivered volumes over every dose made in 2026, assessed against its tolerance.
Domain test: the quantity that decides is each product's share of doses outside its tolerance, the tail a process performance study estimates, read through the process's own structure (each set's volume falling with the litres it has pumped and resetting at the next set-up) rather than a normal fit to pooled weights; with a school's or a utility's nouns there is no set, no litres pumped and no tolerance band, and the task stops reading the same.
Swap: "which schools put more than 10 pupils in 100,000 below a line" has no instrument that wears between resets and no run to place a reading on, and "which feeders breached a limit" has no sparse weighed sample of a continuous output, so the task does not read the same with another field's nouns.
Layer 1: the server's dose log in UTC with no zone marker beside the register's local times, the event export keyed by serial with a re-seated set logged twice, PC-3 replaced in July under a new serial, the register's weights gross until 30 June and net after, products named in the register and numbered in the logs, aborted fills in the dose log; each is what the systems that hold it produce and none is placed to be caught.
Layer 2: estimation_fit: the out-of-tolerance tail of a drifting process sampled sparsely: each product's volume modelled as its set's start plus a loss per litre pumped, the start varying from set to set, and every dose's chance of lying outside taken at its own litres pumped, weighed or not.
Decisive step: placing every completed dose and every weighed dose on its set through the compounders' set-up events, reading the loss per litre and the start's spread from the weighed doses, and summing every dose's chance of lying outside the tolerance at the litres its set had pumped.
Not semantics: reading every field, code and the policy correctly still leaves the tail to estimate; no column stores a dose's set or its litres pumped, and the capability study, the weighed share and the quarantine sorts all read every field right and file the wrong set.
Not rule application: PH-QP-07 files the estimand (out-of-tolerance doses per 100,000 doses made, weighed or not) and SC-SOP-12 the checks and the reaction plan; no clause says how the doses nobody weighed are estimated, and executing every filed rule leaves the capability study, the weighed share or the sorts as the estimate, each wrong.
Analyst test: a strong analyst conforms the dose log, the event export and the register, reads PH-QP-07 and every tolerance right, runs the capability study on each product's weighed doses and configures P0431, P0610, P0614, P0618 and P0702; every field is read and every rule executed, and the set is wrong because the weights are not one stationary spread.
Estimand: PH-QP-07 sections 2 and 3.1: population, each product filled on PC-1 to PC-4; outcome, a dose made outside the product's volume tolerance, weighed or not (an aborted fill is not a dose made); window, calendar 2026 in Ontario local time; unit, out-of-tolerance doses per 100,000 doses made; comparison, more than 10.
No decoy: nothing is planted to be caught; no memo, draft list or vendor recommendation argues any product, and no shipped file states a rate, a capability index or a list.
No certified replay: no certified or published figure reproduces any route; GC-1's every-dose weights cover only the two products GC-1 fills, which PH-QP-07 3.2 keeps out of scope.
Lesson: a rate a policy files over every dose made, for a process that wears between resets and is weighed one dose in a hundred, is read from each dose's place in its run, not from the spread of the weighed doses; the long runs end where nobody weighs.

## Survivor anatomy

Actor: the deciding property, each dose's litres pumped on its set, has no column: it is a relation between the dose log's rows (the earlier completed fills on the same set) and the event export's set-ups, and the set itself is a column in neither the dose log nor the register.
Link: the comparison that finds the call places the register's weighed doses (local time, product names) on the dose log's fills (UTC, product numbers) and both on the event export's set-ups (serial and time), a join no key offers and no sentence invites; the capability study needs only the register.
Reflex: the field's way of turning in-process weights into a nonconforming rate, a capability study's normal tails (the Ppk figure), is rung 0 and files P0431, P0610, P0614, P0618 and P0702.
Back-test: the textbook route validates on the record: on GC-1, which weighs every dose, the normal fit to potassium chloride's and norepinephrine's weights predicts their every-dose record (well under one dose out of tolerance expected, none recorded), and not one of cefazolin 2 g's, phenylephrine's or midazolam's 2026 weighed doses was out of tolerance.
Second use: every file the decisive step reads has its own reason to be in the pack: the register is the unit's checks, the dose log the doses made (Ask A), the event export the sets (Ask B), the product master the tolerances and the equipment register the stations.
Shock: the movement the step recovers is the ordinary loss every set shows; the four are no interval of the products sorted on doses made, batches, sets, weighed doses, failed checks, sorts, mean, spread, Ppk, sets carrying more than one batch, the longest set or the labelled volume (asserted, S); the one sort that orders them first, each product's lowest weighed dose, files no rate and is recorded as a WARN in the Readability screen.
Pins: the WHAT sits in PH-QP-07 sections 2 and 3.1 (population, outcome, window, unit, comparison) and no filed sentence names a set's litres, wear, drift or a model (asserted, L); deleting section 2's "whether or not it was weighed or quarantined" unforces only the population of unweighed doses, and that clause names no step.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 capability study (normal, overall) | PH-QP-07 2 files the population, not the estimate | the register's weights | the field's reflex | GC-1's every-dose record agrees with it | the battery runs it | one mean and one spread | none | readable |
| 1 the spread within batches (Cpk) | none | the register by batch | a quality engineer's variant | none | yes | one spread | none | readable |
| 2 the weighed doses' out-of-tolerance share | "weighed or not" points away from it | the register's Result | a literal count | none | yes | one share | none | readable |
| 3 the quarantine sorts' rejects | SC-SOP-12 5.1 | the quarantine register | a records count | none | yes | one sum | none | readable |
| 4 a pooled bounded fit (Johnson SB, SU) | none | the register's weights | a statistician's repair for non-normal weights | none | yes | one fitted shape | none | readable |
| 5 (decisive) every dose rebuilt on its set | none names a set's litres, wear or a model | no column holds a dose's set or litres | not the reflex | none | no battery item | not affine in a shipped column | the event export is the compounders' own log | silent |

WARN (the one-dimensional law): each product's lowest weighed dose orders the four first (cefoxitin -5.86, midazolam
-4.93, cefazolin 2 g -4.59, phenylephrine -4.48, then ampicillin -3.39); a closest approach files no rate per 100,000, and
the cut that would separate them is nowhere in the pack.

## Semantic fork table

| SF | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | a dose made | a completed fill | an aborted fill too (each a partial fill, out of tolerance) | every product crosses 10 (asserted) | PH-QP-07 2 (an aborted fill is not a dose made) |
| SF2 | out of tolerance | delivered volume outside the product's tolerance, weighed or not | the weighed doses only | rung 2 (asserted) | PH-QP-07 2 |
| SF3 | the year | 2026 in Ontario local time | the UTC year | same call (asserted) | PH-QP-07 2 |
| SF4 | a set | a set lot on its device, a re-seat the same set | a re-seat restarting the litres | same call (asserted) | the event export's lots |
| SF5 | litres pumped | the programmed volumes of the set's earlier completed fills | delivered volumes, or aborted fills' volume counted | same call (asserted) | none needed |
| SF6 | the start | varying from set to set about its mean | fixed per set, shrunk, a slope per set | same call (asserted, the family) | none needed |
| SF7 | the register's weights | gross less the container tare to 30 June, net from 1 July | every weight as net | the first half's doses read 40 to 80 per cent heavy, not a reading | the register's own headers, Gross wt (g) and Net wt (g) (asserted) |
| SF8 | the products in scope | the twelve filled on PC-1 to PC-4 | GC-1's two as well | same call, both under 10 (asserted) | PH-QP-07 3.2 |
| SF9 | exceeded 10 | more than 10 per 100,000 | 10 or more | same call (every product off the list under 3, every product on it over 40, asserted) | PH-QP-07 3.1 |
| SF10 | Ask A's doses and months | completed fills by Ontario-local month, a compounder its station across serials | UTC months, a serial each | moves Ask A (asserted) | PH-QP-07 2 and the equipment register |
| SF11 | Ask B's sets | a distinct lot on its device, its product the doses filled on it | each SET_UP row | moves Ask B (asserted) | the event export's lots |

## Ladder

| Rung | Construction | Files | Dies to |
|---|---|---|---|
| 0 | the capability study on each product's weighed doses (normal, overall mean and SD) | P0431, P0610, P0614, P0618, P0702 | the bags' sets start 2.2 to 2.4 per cent high and lose about four per cent over a batch, so their weights spread wide (183, 110 and 309 per 100,000) though no bag dose comes near the limit; cefazolin 2 g (0.4) and phenylephrine (3.1) hide their tails after the last weighed dose of the sets that carried a third batch |
| 1 | the spread within batches about the overall mean (Cpk) | P0431, P0610, P0614, P0618, P0702 | the same |
| 2 | the weighed doses' out-of-tolerance share | P0431 | one syringe in a hundred is weighed; not one of cefazolin 2 g's, phenylephrine's or midazolam's weighed doses was out of tolerance |
| 3 | the quarantine sorts' rejects per dose made | P0431 | a sort opens only on a failed check |
| 4 | a pooled Johnson SU fit to the weights | P0412, P0431, P0507, P0610, P0614, P0618, P0702 | an unbounded shape gives the flat bag weights tails |
| 4b | a pooled Johnson SB fit to the weights | P0431, P0507, P0702 | a bounded shape fitted to the weighed doses alone stops above the limit for cefazolin 2 g (0.4), whose low doses nobody weighed |
| 5 (decisive) | every completed dose rebuilt on its set: start varying about its mean, one loss per litre, the dose's chance outside at its litres | P0412 131.4, P0431 451.2, P0507 266.6, P0702 43.7 | the golden |

- **Margins on the cut pack** (asserted in checks.py, T2): every member of the family (the start fixed per set, shrunk
  per set, a slope per set) files the four; the lowest of the four under any member is 43.6 (midazolam, the start shrunk
  per set), the highest of the other eight 1.6 (heparin, the start fixed per set).
- **Separation.** On the clean truth the four are the products over 10 (cefazolin 2 g 78.5, cefoxitin 504.1,
  phenylephrine 188.3, midazolam 106.6, every other product 0.0) and the capability study on the true deviations of the
  weighed doses files the default path's set (T1).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the twelve products filled on PC-1 to PC-4 | filed (PH-QP-07 3.1, 3.2) |
| 2 Unit of account | the dose made | filed (PH-QP-07 2) |
| 3 Attribution window | calendar 2026, Ontario local time | filed (PH-QP-07 2) |
| 4 As-of dating | the server export of 18 January 2027 | the request and the files' dates |
| 5 Version basis | one record per fill; an aborted fill is not a dose made | SF1 |
| 6 Denominator | the product's doses made in 2026 | filed (PH-QP-07 2) |
| 7 Weighting | every dose once | C1 |
| 8 Window length | the year | filed |
| 9 Boundary inclusivity | outside the tolerance is beyond it; exceeded 10 is more than 10 | SF9 |
| 10 Rounding path | rates compared unrounded; the asks whole numbers | C1 |
| 11 Tie-break | none needed | C1 |
| 12 Maturity and censoring | the year closed on 31 December; every dose made is in the export | C1 |
| 13 Order of operations | conform, place on sets, fit, sum | C1 |
| 14 Row order | none: set operations by serial and time | C1 |
| 15 Duplicate resolution | a re-seated set is the same set (its lot) | SF4, SF11 |
| 16 Identity normalisation | serials to stations through the equipment register; register names to product numbers through the master | SF10 |
| 17 Netting against gross | gross weights less the container tare | SF7 |
| 18 Dimensional units | per cent of the labelled volume; mL, g and specific gravity from the master | the master |
| 19 Code and status semantics | COMPLETE and ABORTED; SET_UP, CAL_OK and ALARM_OCCLUSION; PASS and FAIL | the files' own codes |
| 20 Integerisation | whole doses and whole sets | C1 |
| 21 Clause scope | SC-SOP-12's checks decide what is weighed, not the estimand | filed scope |
| 22 Forward window contents | the configuration governs every dose from 5 April 2027 | filed (PH-QP-07 3.1, the request) |

## Literal reader

Executed word for word, PH-QP-07 asks for each product's out-of-tolerance doses made in 2026 per 100,000 doses made,
weighed or not. Read literally, the weighed doses are one syringe in a hundred and one bag in twenty after each batch's
first, so the doses nobody weighed have to be estimated; the record's own structure (every set's volume falling with
the litres it has pumped since its set-up and resetting at the next) gives each unweighed dose's expected volume, and
summing every dose's chance of lying outside its tolerance names P0412, P0431, P0507 and P0702. The asks, read
literally on the dose log's completed fills by Ontario month and on distinct set lots, give the figures in
figures.json.

## Oracles

None on the main call: no file carries a rate, a capability index, a draft list or a recommendation; GC-1's
every-dose weights cover only its two products, out of scope under PH-QP-07 3.2. The asks have no oracle either: no
file states a monthly count of doses or a count of sets.

## Ask sheet

Two asks on the conformed record, each read through a reconstruction across two systems that no sentence states.

**Ask A, each compounder's doses made in each month of 2026 (60 figures).**
- Files: the dose log and the equipment register.
- Primary (the clock): the server writes each fill's end time in UTC with no zone marker, and every weekday's last
  batch runs on the evening shift after 19:00, so read as local time the evening fills of each weekday month end fall
  into the next month; the unit's hours in SC-SOP-12 and the register's local times beside the same doses make UTC
  unmistakable.
- Hazards: PC-3's two serials (the equipment register); aborted fills.

**Ask B, the sets each product filled on PC-1 to PC-4 used in 2026 (12 figures).**
- Files: the event export and the dose log.
- Primary (the real unit): a set re-seated after an occlusion alarm is logged as a second SET_UP on the same lot, so
  counting SET_UP rows counts it twice; and the export carries no product, so each set's product is the product of the
  doses filled on it, read from the dose log by serial and time.
- Hazard: PC-3's two serials.

| Ask figures | Cracker (lands the call, runs the battery, executes every filed rule) | Mirror (stops at rung 0) | Verdict |
|---|---|---|---|
| A, 60 monthly figures | reads the fill times as local time | the same | miss |
| B, 12 product figures | counts each SET_UP row as a set | the same | miss |

Pair ceiling: 36.8 (the cracker on the call at 53.3, the mirror off it at 20.3, each keeping 11 of 73 ask criteria:
the 10 monthly figures no evening boundary moves and the chart)
Mirror leakage: 15.1 per cent of the ask weight
Measured by: generator/ceiling.py (run on the cut pack, target.zip 81176264)

## Leak sweep

`leak.py task272 --asof 2027-01-18` on target.zip 81176264: REVIEW, no LEAK; each line ruled.
- Sweep 3 on the policy and the procedure (3.1, and 100 inside "per 100,000"): harmless; section numbers and the
  policy's own unit of the rate, which is the filed WHAT.
- Sweep 4 on the policy and the procedure (weighed, register, tolerance, volume, outside, calendar): harmless; the
  policy files the estimand and the procedure the checks and the reaction plan, and neither says anything of a set's
  volume changing as it is used, of litres pumped, or of how the doses nobody weighed are estimated (asserted, L).
- Sweep 11 (the shell quota, question form which): the corpus WARN, answered at the draw.
- Fixed before this run: the serial column's name in the dose log and the event export (now `compounder_sn`), and
  metadata.json's source line, which carried the task number.

## Pre-ship check

1. Three rules: the decisive step (every dose rebuilt on its set at the litres it had pumped) is analytical; nothing
   planted, read or executed decides (the Three rules lines).
2. Determinism: PH-QP-07 sections 2 and 3.1 file the WHAT; the family (the start varying about its mean, fixed per
   set, shrunk per set, a slope per set) files the same four, with the lowest of them at 43.6 and the highest of the
   others at 1.6, and the forks are closed (SF1 to SF11, asserted).
3. Gates on the final cut (target.zip 81176264): generator checks 53 of 53 (one WARN, the lowest weighed dose's
   ordering), the independent verifier on every graded figure (85), two byte-identical builds, figures_check 128 of
   128, precut, voice-check PASS with the shell quota WARN, leak.py REVIEW with no LEAK, guard surface and heart below;
   the leak reader and the determinism judge run from the main thread, since a fork cannot spawn them.
4. Watch item for stage 4: the pooled Johnson SB fit misses cefazolin 2 g on this cut (0.4) but filed the golden four
   on 4 of the 10 seeds screened (Tried and rejected); a reader or judge who reaches it is the signal to deepen the
   long sets' unweighed stretch in the generator.

## Architecture 2 record (spent 2026-10-21)

- Draw: the Vellacott Health Foundation's FY2027 Decision Coaching Grants, one per Fair Assistance Collaborative hospital where at least six percent of its counsellors' 2025 first reviews on households within the free-care limit, on their income over the twelve months before applying, left the household owing more than half of its balance. Golden: 16 grants ($1,024,000), H02, H08, H10, H11, H12, H14, H15, H17, H20, H22, H23, H24, H26, H28, H29 and H30, each application's three-month income put on a twelve-month basis through its region's calendar for its kind of work; the 2025 policy's quarter times four files 5, a calendar pooled across regions or across kinds of work 10.
- Build: stage 3 green on target.zip 66ca10c7 (checks 0 failed, the independent verifier PASS, two byte-identical builds, figures_check 85 of 85, precut 51, leak.py REVIEW answered, heart WARN), committed PAUSED at e59482a0 and 90d43a79.
- Stage 4, two isolated scored readers (`score_reader.py --call-key call.qualify --call-key call.count`): both landed the call with the golden set. Reader C (r272c) fitted a smoothed seasonal profile for each hospital and kind of work by month received and checked it on households seen twice (predicted and observed ratios correlating at about 0.98); reader D (r272d) estimated profiles by kind of work, hospital group and month and validated them on the households that applied more than once (their log spread fell from 0.58 to 0.10). Each quoted criteria 2.3's twelve months against the guide's three months times four as the decisive sentence. Asks: neither kept an Ask A figure (both summed every write-off line once exact duplicates were dropped, 602,632.9 thousand against 299,646.9); Ask B 1 of 31 each, the H20 tie (code 1 for the whole year).
- Judge (the isolated thread's verdict): DETERMINISTIC, APPROVE; the 16 reproduced with the calendars fitted on either year or both, per hospital, on medians or geometric means (the qualifiers at 7.04 or above, the others at 5.05 or below); the easy route files 5, one calendar per kind of work 10; Gate G method_or_model_selection and analytical_non_defect; Gate H pass; findings on the asks (the repeated write-off and its credit to the household's last approval, the renumbered reason list), watch items, and one on a rival clause: "one calendar for each region" files 10 only with the seasonal kinds pooled per region and the year-round kinds left flat, while pooling every kind files 4, so a rival construction is stated exactly or not at all.
- Fate: Gate F failed at both readers, so the architecture is spent. A three-month figure beside a filed twelve-month window is a gap the documents state outright, and seasonal work named on every application hands over the correction: a reader who sees the gap estimates the calendar at the finest cell the data supports, which is the golden family. Both ask devices held against both readers.

## Architecture 1 record (spent 2026-10-21)

- Draw: the Vellacott Health Foundation's FY2027 Decision Coaching Grants, one per Fair Assistance Collaborative hospital whose financial-assistance counsellors are at least six points less likely to approve right after an approval than right after a denial on the same working day, on 2025 determinations pooled from three billing hubs. Golden: 11 grants ($704,000), H03, H06, H09, H10, H17, H19, H20, H21, H22, H26 and H31, from the within-day contrast less its expectation with each counsellor-day's determinations in every order; the counsellor-day fixed-effects slope files 23 and the pooled contrast 2.
- Build: stage 3 green on target.zip 90774da6 (checks 0 failed, the independent verifier PASS, two byte-identical builds, figures_check 82 of 82, precut 51, leak.py REVIEW answered, heart WARN), committed PAUSED at a84ba0db and 24b56b9e.
- Stage 4, two isolated scored readers (`score_reader.py --call-key call.qualify`): both landed the call with the golden set. Reader 1 (r272a) corrected each within-day contrast by shuffling the day's determinations and kept no ask figure (every FAWO line summed, 816,026.2 thousand; code 1 read for the whole year). Reader 2 (r272b) fitted counsellor-day fixed effects, named their bias at about 19 determinations a day unprompted and subtracted the null of 150 within-day permutations per hospital; it kept every Ask A figure (31 of 31: the write-off once per application, the twice-loaded lines dropped on adjustment_id, reversals per account) and no Ask B figure (code 1 for the whole year).
- Judge (the isolated thread's verdict.md, `determinism_check_report.md`): DETERMINISTIC, FIX_NOW on documentation only: every figure reproduced (197,939 determinations, the 11, $704,000, all 62 ask figures); the one live main-call reading is the uncorrected within-day contrast (23), which is the stump itself; the two ask conventions (the write-off once per application, the 1 July 2025 renumbering) recoverable from the data and unstated. Gate G method_or_model_selection and analytical_non_defect; Gate H pass.
- Fate: Gate F failed at both readers, so the architecture is spent. The small-sample bias of conditioning on the previous outcome inside a short sequence (the Miller and Sanjurjo hot-hand correction) is a named reflex for these readers: criteria that compare "the chance" within the same working day, beside queues of about 19, hand over the within-day permutation null. Ask B's renumbering held against both readers; Ask A's repeated write-off held against one.

## Tried and rejected

- The seed's own quantity (the Medicaid gap on the "would recommend" top-box rate across a state report's hospitals), every route screened at the draw: composition and patient mix settle the comparison population (WHAT screen); shrinkage of small cells repeats task253; design weighting repeats task264's lesson and task268 v2's reflex; nonresponse either fails determinacy or repeats the inverse-probability weighting of task264, task267 and task268; survey mode effects belong to Experiment & Causal Analysis; misclassification is the spent sensitivity-and-specificity family; nowcasting the late returns repeats task181; telescoping sits next to task453.
- A race-probability (BISG) regression for the equity gap (prototype `p1.py`): a strong ladder, but the same linear unmixing of a mixed population as task263, a clone of its driver.
- Traffic count factor groups for an annual average (prototype `t1.py`): count differences of one or two units at tiny margins, and the ground overlaps task474.
- The sequence effect at queues of 4 to 14 determinations with effects of 2 to 13 points (`s1.py`, `s2.py`): the two corrected estimators (the excess over reordering by counts, the held-day slope less its reordering expectation) disagreed on 1 to 3 hospitals a seed, with the closest margins 0.01 to 0.3 points; the queues were lengthened and the effect hospitals separated from the line.
- Effects of 12 to 17 points (`s4.py`, `s5.py`): the family agreed, but the day's rate without the pair as a control landed 10 or 11 of the 11 hospitals, its bias of 3 to 5 points smaller than the gap to the line; the effects were lowered to 9.5 to 12.5 with a wider day mix (`s6.py`), where it lands 9.
- Ask B as presumptive approvals with nightly re-runs replayed under fresh application numbers (D1): dropped at stage 2, because no asking sentence makes the count determinate without naming the device (a replay is a fresh application record, so "each application once" counts it, and any wording that excludes it narrates the re-run); replaced by the reason list renumbered on 1 July 2025 (D2).
- Queues of 6 to 28 a day with counsellors sitting on 55 percent of working days: the held-day route filed 28 of 31, an answer a reader distrusts on sight; queues of 8 to 32 on 48 percent of days put it at 23 with the family still closed (1.81 points).
- Effects of 9.5 to 12.5 points with the day's rate over the other determinations as a reflex: it landed the golden set (the others' count is the day's sufficient statistic), so it was moved into the family and the construction made every member agree, rather than the world bent to break it.
- Architecture 1 (each counsellor's sequence effect measured against the reordering of each working day's own determinations): spent at stage 4, both scored readers corrected the within-day contrast for the short-queue bias by permuting each day's determinations and landed the 11; a decisive step that is a named small-sample bias correction falls to a reader who knows the bias by name, however the ladder below it is tuned.
- The outcome "did not get free care in full" (a denial or any discount below 100 percent): noise in the year-round households' calendars inflated the shares at the 200 percent line, where the 2025 policy's full-care boundary sits on the eligibility line; the outcome moved to owing more than half of the balance (a denial or a 25 percent discount), whose policy boundary at 300 percent no year-round household's pay crosses.
- Households timing their applications to a low quarter (selection on the quarter): dropped in the prototype, no separation the seasons did not already give.
- Every hospital's designed share at 7.5 or 4.5 percent (the first build of this architecture): under the golden calendars 13 hospitals landed between 7.50 and 7.56 percent and 8 between 4.50 and 4.54, a cluster that confirms the golden route to a reader trying several calendars and reads as made in the chart; the designed shares were spread to irregular values, and the three set below what misassessment alone gives them (H04, H07 and H27, which then denied almost no one for documents) were raised to 4.29 to 4.68.
- Flat pay for year-round households and a fixed seasonal shape (the first builds of this architecture): a household's repeat applications carried the same three-month total to the cent, which reads as made; pay now rises unevenly from year to year and varies month to month, a household reapplies when its work takes its pay down (the season it knows) rather than on a month's luck, and the fixed-effects member falls back to a cell's month means where the cell does not identify its own calendar (the Olympic Peninsula's resort households: left unadjusted there, it had read H28 at 6.31; the reapplication change did not move that figure, the missing cell did).
- Also weighed at the re-root draw and dropped before any prototype, no reasons written down at the time: CGM, cash fills, TTR, a hungry-judges time-of-day effect, and heaping (already on file as spent in this lane).
- Architecture 2 (each household's twelve-month income rebuilt from the 2025 policy's quarter through its region's calendar for its kind of work): spent at stage 4, both scored readers read criteria 2.3's twelve months against the guide's three months times four, fitted a seasonal profile per hospital or region and kind of work and landed the 16; a decisive step that answers a gap the documents state outright falls to a reader who reads both documents, however finely the calendar has to be cut.
- Screens run at the architecture 3 draw on 2026-10-21, each set aside with its record. None cleared, so the number retires.
  - Demand censored at a stock or a capacity: task18, task108, task147, task168, task133, task141, task120 and task179 record it as spent.
  - Event times known only between periodic inspections, or at a single inspection: task476's leak starts, and the onsets set aside at task270's draw.
  - A share past a line taken from model predictions with their error added back, as in poverty mapping or an exposure model's Berkson error: task123 records it as task253's insight, task185 measured the exceedance route dead on the lever against the plug-in, and task143 records a strong analyst adding the stated validation error by reflex.
  - Realised variance against microstructure noise: task270 and task271.
  - A hot deck whose donor cells leave out the grouping variable, pulling each group's imputed earnings toward the other groups': dropping the allocated values is the filter route the partial-coverage screen kills, and reweighting the respondents within cells is task253 v1's nonresponse adjustment within classes.
  - Immortal time, and the period-analysis estimate of current survival: both are delayed entry into the risk set, task265's lesson.
  - A point-in-time count's elapsed durations turned into a year's flow: length bias, task264's size-biased sampling.
  - Recall decay across a survey's recall period: the latest month is a filter route and the decay form forks; telescoping sits next to task453.
  - Persistence beyond a panel's span by a mover-stayer chain: mover-stayer, latent Markov and second-order chains extrapolate apart.
  - Bunching below the free-care line: the counterfactual density's degree, window and bin width are open.
  - The own-children estimate of fertility, and extinct-generation old-age death rates: named methods, each with an open adjustment; the second was set aside at task271's re-root.
  - A closing auction's own impact net of the liquidity its imbalance drew: task197's design, abandoned there on the taxonomy; here, which offsetting orders were responsive is a judgment no record settles.
  - Roll-call ideal points: task269 and task270.
  - The tail of a sum of correlated parts by simulation: each unit's recorded totals are a filter route.
  - Minimum-night-flow leakage through the night-day factor: no utility task type serves Descriptive & Distribution Analysis.
  - Medication persistence, pharmacology's one Descriptive task type, set aside at task270 and task271: the reverse waiting time forks, and the new-user washout is a WHAT.
  - The Fair Assistance world itself: its quantities are filed rules once its two estimation hooks (a counsellor's sequence effect, a season inside a quarter) are spent. Its presumptive-screen incomes are the Berkson case above, and take-up through verified applicants is the transported error-rate family (task192, task267).
- Architecture 2 retired by this session's batch audit (2026-10-31), short of the survivor anatomy the approved builds share: its actor had a column (every application named the main earner's kind of work) and its link was stated outright (the criteria's twelve months against the guide's three months times four), so only the field's-method rung held; it is re-rooted, not repaired, so the portal sees one strong build.
- 2026-10-31, at the architecture 3 draw: a clinic medication refrigerator's product temperature rebuilt from the
  building system's air probe through each model's thermal response, calibrated on pilot units carrying a buffered
  probe (the card first drafted): the same insight as task482 v8 (a slow quantity carried through a lag measured on a
  short overlap), spent there at stage 4 because two records of one unit side by side are compared on reflex.
- 2026-10-31, at the architecture 3 draw: the drift-between-resets stump in a precision machining plant (inserts
  wearing between tool changes, hand checks at intervals, containment sorts): the guard banned the organisation
  family (manufacturer, task482 v16 in the last three builds) with the context artifact and the forcing event; the
  hospital pharmacy's compounding unit carries the same structure honestly.
- 2026-10-31, at the architecture 3 draw, set aside before any prototype: an assay's drift between calibrations read
  from quality control (task274's calibration-specific bias on an immunoassay sits too close); hypochlorite decaying
  between deliveries at small water works (operators' grab samples land in most low spells, so the sampled share
  files nearly the golden); a dental milling centre's burs (every crown is seated on its die before release, so the
  checks are not sparse); medication adherence, roll-call ideal points and small-area opinion (rules, spent, or an
  open model specification); low-depth genotype calls (a named reflex).
- 2026-11-01, at the build: weighing every fortieth dose: the long sets' tails were weighed and caught, so the
  weighed share and the sorts filed nearly the golden; the procedure weighs the first dose of each batch and then every
  hundredth syringe or twentieth bag, and the long sets' tails fall after the third batch's last weighed dose.
- 2026-11-01, at the build: the start fixed per set as the golden: one or two weighed doses per set make the start
  noisy and inflate the tails (piperacillin-tazobactam crossed 10 at 20.4 against a truth of zero); the golden takes
  the start as varying about its mean, and the bag sets start high so that no member of the family puts a bag near
  the line.
- 2026-11-01, at the build: a third ask, each product's mean delivered volume in each quarter: the gross and net
  weights are in the register's own headers and the specific gravity in the procedure, so a careful solver banks it;
  dropped, and Ask A moved to months, whose fill times carry no zone.
- 2026-11-01, at the build: bag sets ending lower (a start of 2.05 and a five per cent loss) to break the
  lowest-weighed-dose ordering: ampicillin crossed 10 under the golden and the family split; reverted, and the
  ordering is recorded as a WARN in the Readability screen.
- 2026-11-01, at the build: seeds where a pooled Johnson SB fit to the weighed doses files the four (27203, 27235,
  27251, 27259 of the ten screened): the seed was chosen where it does not (27267, cefazolin 2 g at 0.4); a bounded
  fit lands only when the long sets' third batches leave a visible shoulder in the weighed doses, so this is the rung
  to watch at stage 4.
