# task230 design note

Architecture 2 is current: drawn 2026-10-11 as task230's architecture 2 of 3, loops 0, after architecture 1
was spent at hardening loop 2 (its sections are kept under `## Architecture 1` below, and its identity sits in
the card's lineage). Phase A only: no data is cut and no generator file is edited. The card is guard-checked
and registered (see `## Coordination`). The H2 headings from `## Draw` to
`## Ask sheet` are the ones `precut.py` reads.

## Draw

- **Card**: task230, architecture v2, registered as `cards/task230.json` (drafted at
  `/home/user/orch/buildwork-task230/arch2/task230_card.json`), with architecture 1 moved into `lineage`.
- **Pairing.** Domain Human Factors & Ergonomics (a client domain), task type human-reliability-assessment,
  objective Data Quality Monitoring & Alerting. The object under analysis is the accuracy of the data a
  capture pipeline delivers, and the committed call is which client streams the centre's second
  verification control covers next month; the forward window is a forecast inside a monitoring call, so
  the tag stays Data Quality Monitoring (the taxonomy lists the task type under Forecasting).
- **Shape 07, grid of cells**: eleven client streams against four columns, the call and three
  device-carried figures. Criteria: the call (one set, or eleven rows if graded per stream), 11 second-pass
  hours, 11 credits at stake, 10 client-audited rates, the chart's series, order and title (3), the two
  files (2): 38 to 48. Shapes 01 and 10 are banned by task228 and task229.
- **Mechanism.** Gate G `method_or_model_selection`; gap time, then population; pattern A in its S4 form
  (the forward window runs under pool error rates no closed month reached); generators G14 (does the
  pooled rate apply to this pool), G13, G17; stump strategy `causal_design` (interference through a
  shared verifier pool); `stump_class` analytical; decisive rule filed (QCP-04 files the estimand, the
  rule and the records, never a method or a selection criterion: the design forces the method,
  `determinism-check` section 1 form 1); `official_decoy` false; `validated_decoy` false; calibration
  none (the blind re-key audit is the measurement, not a calibration organ).
- **Furniture.** The requester is the capture centre's head of operations, who runs both first-pass
  queues and signs the monthly second-pass verification plan that the service quality council approves
  (`operations_director`); context artifact `capacity_report`, the November operating plan the head of
  operations works from (stream routing, daily key fields by stream, the verifier roster, the October
  list); both redrawn at registration (see `## Coordination`); scoring unit per accepted item; decision
  type `designation_set`; forum
  `committee_or_panel` (the service quality council, in the pack, never in the prompt); forcing event
  `purchase_order_or_contract` (Hollings & Pryce's contract starts on 1 November); organisation family
  `professional_services`.
- **World.** Tamralipta Data Services, a business-process outsourcing firm's insurance-claims capture
  centre in Kolkata (INR internally; USD, GBP and AUD by contract), running US clients on a night queue
  and Australian and UK clients on a day queue, each queue one pooled first-pass verification queue.
  Clients: Kessington Benefit Administrators (two streams), Northgate Dental Services, Brightmoor Comp,
  Harbison Pharmacy Benefits, Wattlebird Health (two streams), Coolabah Income Protection, Whinfell Pet
  Cover, Thistlecombe Motor, and Hollings & Pryce (new). Every invented name was searched whole-word
  across the cards, the task folders and the clone cache with no hit; Calloway, Ridgeline, Ashdown,
  Pemberton, Fairhaven and Larchmere were dropped on hits. Personas, drawn with `guard.py names` (India
  locale, seed 230) and checked by hand against every card's `world.people`: Dipta Mukhopadhyay (head of
  operations), Raghav Bajwa, Vasana Reddy; they appear in the pack only.
- **Why the Drumlee world was not kept.** Its organisation family (`hospital_or_health_provider`)
  repeats task181 inside the three-draw window (guard BLOCK `ban.org_family`), Sandra was a BLOCK on
  `people.first`, and the domain-coupling rule asks for the field's own method, which the patient-app
  world no longer offered once comparison pools were spent.
- **Data-native sentence.** This capture centre's first-pass verifiers work one pooled queue per shift,
  interleaving every client stream on that shift, so the error rate each verifier meets is set by the
  whole pool's mix, and the November plan changes that mix in both pools at once: the motor claims
  leaving for nights and the new client's typed claim forms dilute the day pool, and the motor claims
  enrich the night pool.
- **Guard.** On the merged checkout (main at 3966e83, task182 included) and on a scratch folder holding
  task228's branch card (2e502d1, architecture v2) and task229's rework-branch card (702f3d5,
  architecture v1, paused before its draw): `check` WARN in both, no BLOCK (`repeat.gate_g` against
  task228 v2, `repeat.decision` against task229; NOTE `test.same_driver_older` differentiated against
  task114 and task33); `heart` WARN, nearest 0.05 (task33 lineage, task83, task92 v4 stump), nothing at
  0.12 or above. At registration, on a scratch folder holding main's cards (e89a676) and task229's
  registered design-2 card: `check` BLOCK on `ban.role` (`compliance_or_audit`) and `ban.artifact`
  (`operations_log`) against task229 v2, both redrawn; then `check` WARN, no BLOCK (`repeat.gate_g`
  against task228 v2 and task229 v2, `repeat.decision` against task229 v2, the same NOTE) and `heart`
  WARN, nearest 0.05 (task33 ledger row, task92 v4 stump); on this branch `check` WARN, no BLOCK, and
  `register` filed the card. WARN answers are in `## WARN answered`.

**What each library source teaches, and how this build differs.**

- *County Domestic Migration* (exemplar, 0.19): the averaging basis decides, a mean of county rates
  against the resident-weighted rate, and the model misses because the ready-made measure looks right.
  Here no ready-made measure exists: the deciding quantity, each shift's pool error rate, is built from
  every stream's audited errors on that shift.
- *Internal Migration Statistics* (0.54): the largest mover fails a filed reliability threshold, so a
  filed rule applied correctly decides. Here the filed rule (forecast over the limit) is the easy part;
  the forecast is the difficulty.
- *Pipeline Custody Transfer Measurement* (0.35): size against share under a filed comparison basis.
  Here the basis is filed (errors per 1,000 key fields) and every route uses it.
- *Electric Power Productivity Statistics* (0.53): a restated basis changes eligibility. Here nothing is
  restated; every figure in the pack is final.
- `layer2-rigor-patterns.md`: Human Factors has no patterns of its own, so the pattern is own (pooled-queue
  error prevalence sets human detection), learned from the field (signal detection's low-prevalence
  effect; the inspection literature's defect-rate effect on inspectors), not from a listed pattern.
- `_measured.md` traps 7 (uses the ready-made measure) and 2 (counts file rows instead of the real unit)
  both tempt here (each stream's measured miss rate; the document row) and neither decides. Trap 13
  (validates on one population, applies to another) is the nearest measured habit: a clean back-test
  feels like proof. Here the streams and verifiers are the same; what changes is the condition they work
  under.
- `proven-in-production`: S4 (the forward window under a regime the closed window never reached) is this
  build's home, and L7 (the naive basis empirically excellent on the closed record) is met by the default
  path's clean monthly back-test.
- Shipped ledger task107 v1 (a data-quality monitor licensed for eight of thirty feeds, retired): its
  decisive rung carried a loud row-count symptom and a careful solver executed it. Here the wrong path
  leaves every count, total and monthly back-test clean.

## Default path

The pipeline a competent analyst builds from the prompt's words, QCP-04 and the files' grain:

1. Read QCP-04 4.1 to 4.3, the quality schedules' limits and the November operating plan (routing, daily
   key fields by stream, the roster).
2. Sessionise the first-pass log (a timed-out screen's later submission counts), attribute night screens
   to the shift's start date, and resolve reissued verifier IDs through the effective-dated register.
3. Join the blind re-key audit to the screens and count, by stream, field type, verifier, shift and day,
   the audited OCR errors and the first-pass misses among them.
4. Fit miss models on the attributes the rows carry (stream, field type, verifier or tenure band, shift,
   time on shift, workload, day of week), keep the best-fitting, and back-test it month by month: clean
   on every stream-month.
5. Forecast each stream's November residual from the chosen model under the plan: the motor claims take
   the night queue's terms, Hollings & Pryce its pilot terms, and the roster's moves (experienced night
   verifiers to days for the go-live, new hires to nights) enter through the verifier and tenure terms.
6. Put every stream whose forecast exceeds its limit on second pass (4.2).

Ends on: second pass for Kessington's institutional and professional claims, Northgate, Brightmoor, Harbison and Thistlecombe's motor claims (N1, N2, N3, N4, N5, D5)
Golden: second pass for Brightmoor, Wattlebird's extras claims, Coolabah, Whinfell and Hollings & Pryce (N4, D2, D3, D4, D6)

## Stump sentence

A competent solver dedupes the timeout re-verifications, measures each stream's first-pass misses from the
blind re-key audit, models detection on verifier, stream, field type, tenure, shift, time on shift,
workload and day of week, takes the best-fitting of those models on a clean month-by-month back-test, and applies it
to the November plan (the motor claims on nights, Hollings & Pryce on days, the roster moves), keeping
Kessington's two streams, Northgate, Brightmoor, Harbison and the motor claims on second pass and the day
streams off; the step that lands it there is treating detection as a property of the verifier, stream,
shift or day when it rises and falls with the error rate of the shift's whole pool, which the plan cuts on
the day queue (about 4.3 to 1.9 per cent) and raises on the night queue (about 2.5 to 5.0).

## Three rules

Domain test: The deciding quantity is each stream's first-pass residual next month, which human reliability assessment estimates as a verification task's non-detection probability under the conditions it will run in, and the condition that moves is target prevalence (signal detection's low-prevalence effect: observers shift their criterion and miss more when targets are rare, so detection measured in one pool does not travel to a pool with a different error rate); a generalist's corrections (stratify by stream, shift, verifier or tenure, reweight to the new mix, control for time on shift, workload and day of week) treat detection as a fixed property of an attribute and never construct the pool's error rate, and with an automated validation rule in place of the verifiers there is no criterion shift and the task stops reading the same.
Analyst test: A strong analyst who sessionises the log, dedupes the timeout re-verifications, resolves reissued verifier IDs, reads QCP-04 and every quality schedule correctly, and models first-pass detection on every visible attribute (verifier, stream, field type, tenure, shift, time on shift, workload, day of week), taking the best-fitting of them on a clean month-by-month back-test, still keeps the four night streams and the motor claims on second pass and leaves the day streams and Hollings & Pryce off.
Layer 1: Realistic mess from a capture platform, a workforce system, a QA tool, client systems and billing: on the main path, timeout second events, night shifts crossing midnight, reissued verifier IDs and the audit's re-key and adjudication rounds (texture, asserted unable to move the call); on the ask paths, session minutes repeated on every document line, a stored billing tier taken before November's volumes, late forecast revisions, client calendars and units, client audit exports stamped in UTC, client reason codes and re-reviews, form versions effective mid-month.
Layer 2: Detection modelled as a fixed property of the verifier, stream, shift or day, when it follows the error rate of the pool the verifier works, which the plan moves in both queues.

- **Litmus: no.** Every figure in the pack is correct (the third quarter's audited misses, each client's
  audit, the plan's volumes) and no stakeholder conclusion is overturned; the difficulty is forecasting
  November's first-pass residual under pools the plan changes. Mechanism `method_or_model_selection`
  with forecasting, `statistical_rigor` supporting. `surface_read_dependency: no`.
  `stumping_family: analytical_non_defect`. `sole_data_defect: no`.
- **Deletion tests.** Delete every wrong number: there is none, and the task stays hard because the
  deciding quantity is on no row. Clean-data test: repairing every main-path file (timeouts collapsed,
  IDs resolved, shift-days stamped) leaves the answer and the default path's answer unchanged and
  different (asserted per suspect file). Lens swap: the default answer and the golden are not the same
  population at the same moment under two lenses; they are two forecasts of one November under two
  detection models. Identity test: no identity over shipped quantities closes the call; the forecast
  needs a fitted dose-response. Corpus direction: the closed quarter reproduces the default path at the
  monthly grain. First moves: the one-period group-by, the pilot's own decomposition and the monthly
  back-test all land on the default path's set.
- **Against the spent list.** Not a comparison pool: there is no control group; the pool is the verifiers'
  own work, and its error rate is a performance-shaping condition. Not clustered errors: the shift-day
  correlation is the signal, a predictable driver the plan moves, not a variance to correct. Not
  transport: the same verifiers and streams, inside the closed quarter's shift-day range. Not a forecast
  method chosen by back-test: nothing filed selects or scores a method (the design forces it,
  `determinism-check` section 1 form 1), and the monthly back-test the default path runs is clean on
  every attribute model. Not selection into observation: the audit is a random
  sample. No regression to the mean: stream detection is measured on tens of thousands of audited fields.

## Readability screen

| Rung | 1 filed sentence | 2 schema | 3 reflex correction | 4 control bench | 5 hygiene battery | 6 linear arithmetic | Verdict |
|---|---|---|---|---|---|---|---|
| R0, the third quarter as measured | fires: 4.1 asks for November's forecast over the plan's routing | no | no | no | no | no | readable |
| R1, the default path (stump) | fires: 4.1 and 4.3, the closed quarter's records under the plan's routing and roster lead here | no | fires: controls for shift, day, workload, tenure | no | no | no | readable |
| R2, the day pool only | no | no | no | no | no | no | silent |
| R3, both pools with the new client at its pilot rate | no | no | no | no | no | no | silent |
| R4 (decisive), detection on the shift-day pool's error rate in both pools for every stream | no: no sentence names the pool's rate or says one client's volume moves another's accuracy, and none names or selects a method | no: no column carries it; it is an aggregate of every stream's audited errors per shift-day, a different entity from the stream | no: the reflexes (stratify, control, reweight, shrink, decompose) act on the stream's own attributes | no: nothing filed scores candidate models, every attribute model ties the closed quarter month by month, and the shift-level misfit reads as audit noise (overdispersion about 1.3) | no: counts tie and the audit reconciles on the wrong path | no: the forecast is a fitted dose-response read at the plan's pool rates, not a ratio of reported figures | silent |

The decisive rung's honest exposure is test 4 on the solver's own initiative: an attribute model's
residuals, checked shift-day by shift-day, are overdispersed (about 1.3), and they line up with the pool's
rate only once that rate is built. Nothing filed asks for shift-level validation any more (the filed
back-test that did is in `## Tried and rejected`). The data keep the attribute models' shift-level misfit
inside what audit sampling produces on most shifts, while over the quarter the separation the design rests
on holds by the asserted margins (`## The estimand, the rule and the records`).

## Semantic fork table

| Id | Term or convention in the main ask or computation | Golden reading | Alternative reading | Call under the alternative | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "second-pass verification for November" | a stream is on second pass for the whole month when its forecast exceeds its limit | second pass from a mid-month date (a go-live or a form version) | not a call 4.2 can express | QCP-04 4.2, "for the month" |
| SF2 | the residual compared with the limit | key fields wrong after first pass, before any second pass | the delivered residual after second pass | streams on second pass in October read as under | QCP-04 4.1, "value after first pass" |
| SF3 | "forecast" | a first-pass detection model fitted to the closed quarter's records and applied to the plan's November routing, volumes and roster, one method for every stream (4.3) | the third quarter's measured residual carried forward | R0's set | QCP-04 4.1, "every document the November operating plan routes to the stream's queue", and 4.3, "the operating plan of record for the month" |
| SF4 | "exceeds its limit" | strictly greater, unrounded | at or above, or compared after rounding to the limit's precision | same call | same call: no forecast within 0.10 of its limit (asserted) |
| SF5 | the limit | the client's quality schedule, errors per 1,000 key fields | an accuracy percentage some schedules also print | same call | same call: the schedules print both forms of one number |
| SF6 | "key field" | the fields each client's quality schedule lists as key | every captured field | not computable: the audit re-keys key fields only | the quality schedules and the audit design |
| SF7 | November's days | shift-days 1 to 30 November by the shift's start date | calendar days | same call | same call (asserted) |
| SF8 | "stream" | the stream register's eleven streams (Kessington and Wattlebird two each) | one row per client | not a call on eleven streams | the quality schedules set limits per stream; QCP-04 4.1, "each stream" |
| SF9 | "the last closed quarter" (4.3) | July to September 2026 | the latest three months | October is not closed in the audit export | QCP-04 4.3 and the audit export's quarter |
| SF10 | November's shift-days in the forecast | each shift-day's mix from the plan's daily key fields by stream | the month's average mix in each queue | same call | same call (asserted; closure axis 22) |
| SF11 | the misses a detection fit counts | audited key fields whose first-pass value the blind re-key adjudicates as wrong (4.1) | first-pass corrections from the edit log over every key field, with the audit's misses | same call | same call (asserted) |
| SF12 | the roster | the plan's November roster | the third quarter's roster | same call | same call (asserted) |
| SF13 | Hollings & Pryce | one of the eleven streams from 1 November | left out until its volume settles | the answer without D6 | the plan routes it from 1 November; QCP-04 4.1, "every document the plan routes" |
| SF14 | verifier-introduced errors | counted (any value after first pass that differs from the image) | OCR misses only | same call | same call: about 0.1 per 1,000 (asserted) |
| SF15 | the divisor | key fields first-pass verified | documents | not the limit's unit | QCP-04 4.1, "per 1,000 key fields first-pass verified" |

The stump is none of these readings: R1 executes every golden reading and differs only in the detection
model. SF10 and SF11 replace the rows on the dropped criterion's wording ("each shift left out",
"closeness") with two conventions the forecast itself depends on.

## Ladder

Paper values at the truth slope (0.6 on the miss logit per unit of log pool error rate, inside the field's
measured range); the generator sets the error rates and limits and asserts every margin. Ratio = November
first-pass forecast over the limit.

| Code | Stream | Family | Queue Q3, Nov | Key fields a weekday | OCR error | Limit per 1,000 | Q3 measured | R1 default | R2 day only | Answer |
|---|---|---|---|---|---|---|---|---|---|---|
| N1 | Kessington, institutional claims | printed | night, night | 26,000 | 1.40% | 1.8 | 1.13 | 1.16 | 1.13 | 0.78 |
| N2 | Kessington, professional claims | mixed | night, night | 14,000 | 3.20% | 5.0 | 1.10 | 1.13 | 1.10 | 0.76 |
| N3 | Northgate, dental claims | handwritten | night, night | 8,000 | 4.20% | 7.5 | 1.17 | 1.21 | 1.17 | 0.83 |
| N4 | Brightmoor Comp, workers' compensation | handwritten | night, night | 4,000 | 5.60% | 7.2 | 1.63 | 1.68 | 1.63 | 1.15 |
| N5 | Harbison, pharmacy claim forms | printed | night, night | 10,000 | 1.70% | 2.3 | 1.07 | 1.10 | 1.07 | 0.74 |
| D1 | Wattlebird, hospital claims | printed | day, day | 40,000 | 1.50% | 3.6 | 0.45 | 0.44 | 0.70 | 0.70 |
| D2 | Wattlebird, extras claims | mixed | day, day | 30,000 | 2.90% | 4.7 | 0.80 | 0.77 | 1.22 | 1.22 |
| D3 | Coolabah, income protection | handwritten | day, day | 14,000 | 4.00% | 8.3 | 0.78 | 0.75 | 1.16 | 1.16 |
| D4 | Whinfell, pet claims | mixed | day, day | 24,000 | 3.10% | 4.9 | 0.82 | 0.79 | 1.25 | 1.25 |
| D5 | Thistlecombe, motor claims | handwritten | day, night | 35,000 | 9.50% | 18.0 | 0.85 | 1.14 | 1.11 | 0.78 |
| D6 | Hollings & Pryce, typed claims | typed | pilot, day | 60,000 | 0.60% | 0.8 | 0.75 (pilot) | 0.72 | 1.15 | 1.15 |

Pools (key-field OCR error rate of each queue's whole pool): day 4.27 per cent in the third quarter, 1.87
in November (the motor claims leave, Hollings & Pryce's typed claims arrive); night 2.49, then 5.02 (the
motor claims arrive). Detection on a mixed field: day 0.870 falls to 0.803, night 0.829 rises to 0.881.

| Rung | Route | Set | Killed by | Why a good analyst stops here |
|---|---|---|---|---|
| R0 | each stream's third-quarter measured residual against its limit (Hollings & Pryce at its pilot, the motor claims at their day rate) | N1 to N5 | 4.1: the forecast covers the documents the plan routes, and the plan moves the motor claims and adds Hollings & Pryce | the October list and the audit agree stream by stream, and every figure recomputes |
| R1 | the default path | N1 to N5, D5 | detection on the same verifier's same field type rises and falls with the shift-day pool's error rate in both queues; the night and Saturday terms are the pools' gaps | clean monthly back-test, the best-fitting of its candidates, routing and roster honoured |
| R2 | the pool effect found and applied where the headline change lands: the day queue diluted, the night queue left at its third-quarter terms | N1 to N5, D2 to D6 | the motor claims raise the night pool's rate, and the night queue's own third-quarter shift-days show the same dose-response | the mechanism is found and applied to the new client's queue |
| R3 | both pools, Hollings & Pryce kept at its measured pilot rate | N4, D2, D3, D4 | 4.3 forecasts every stream, the new client's included, by the same method, and the pilot's own typed fields (six weeks across Saturdays and the 31 August bank holiday) sit on the slope the other field families share | the one figure measured directly is kept |
| R4 | both pools rebuilt from the plan, detection on the pool's rate within verifier and field type, every stream forecast with the selected model | N4, D2, D3, D4, D6 | | |

- "A solver who does everything right up to R1 commits to N1, N2, N3, N4, N5 and D5." Every rung names a
  different set; every rung's ratios sit at least 0.07 from 1.00 on paper (R1 0.10, R3 and R4 0.15).
- Position: D2, D3, D4 and D6 are four of the six lowest ratios on R0, and no intermediate rung names the
  answer's set. Sign discipline: R0 to R1 moves day streams down (experience into days) and night streams
  up; only the pool's rate reverses both.
- Grid: four toggles (roster terms, day-pool effect, night-pool effect, the new client inside the model),
  sixteen cells. The roster toggle moves margins and never a set; the other three give six distinct sets:
  R1 (no pool effect), N4 alone (the night effect only), N1 to N5 with D2 to D5 (the day effect with the
  new client at its pilot), R2, R3, and the answer, reached only with both pool effects and the new client
  inside the model. Every cell files a feasible set. Asserted cell by cell.
- Survival: no shipped sentence writes the step; no sweepable corpus nominates it (nothing filed scores
  candidates, and the monthly back-test ties); no arithmetic symptom (counts tie, the audit reconciles to
  the edit log and the client
  audits, the monthly back-test is clean); not a per-row predicate (a property of the shift's whole pool,
  aggregated across streams); its enumeration is a fit and a forward run; no cutover date in the closed
  window (the identifying variation is diffuse: weekday mix, Saturdays without UK paper, US holidays on 3
  July and 7 September, the UK bank holiday on 31 August, ordinary day-to-day volume; the pilot moves the
  day pool by under a tenth of a point; no surge week); it survives the deletion.
- Rigorous variants that must agree, every ratio at least 0.10 from 1.00 (asserted): logit miss on log pool
  rate (the golden); linear probability in the pool's rate; the rate in deciles with interpolation; the
  verifier's own experienced rate over its last 500 fields in place of the shift-day pool's; a signal
  detection fit (sensitivity per verifier, criterion moving with the log odds of the pool's rate, hits and
  false alarms together); misses from the audit sample alone or from the edit log plus audited misses;
  with or without tenure, time on shift, time of night, workload, day of week and shift terms; fitted on
  both queues together or within each; November's pools as a monthly average or day by day from the plan.
  Slope corridor: the set holds across the slope's 95 per cent interval, asserted at both ends. Support:
  at least ten closed shift-days at or below November's day rate and ten at or above November's night
  rate, with every roster verifier who worked the closed quarter observed on both sides (November's new
  hires enter at the closed quarter's terms for new verifiers).

## The estimand, the rule and the records (QCP-04, written at the build)

- **4.1 Estimand.** For each stream, the first-pass residual key-field error rate for November 2026: key
  fields first-pass verified on shift-days 1 to 30 November whose value after first pass differs from the
  image as the blind re-key adjudicates it, per 1,000 key fields first-pass verified, over every document
  the November operating plan routes to the stream's queue (none observed at the as-of date).
- **4.2 Rule.** A stream is on second pass for the month when its forecast exceeds its contract limit
  (errors per 1,000 key fields, in the client's quality schedule); a forecast equal to the limit stays off.
- **4.3 Records.** Every stream's forecast, a new client's included, is made by the same method, from the
  last closed quarter's first-pass log and blind re-key audit and from the operating plan of record for
  the month. No method, model or selection criterion is filed.
- **Audit design.** A random share of each stream's documents on every shift is re-keyed blind and
  adjudicated; the adjudicated value is the image's value. Quality reporting runs by shift-day.
- **Never in the pack:** pool, prevalence, the queue's error rate, vigilance, criterion, or any sentence
  that one client's volume moves another client's accuracy.

**How the method is forced (`determinism-check` section 1, form 1).** The estimand and the data's own
structure leave one method standing. 4.1 asks for November under the plan, and the plan moves the pool's
error rate in both queues (day 4.27 to 1.87 per cent, night 2.49 to 5.02). The closed quarter's shift-days
show that rate setting detection: within each queue, misses on the same verifier's same field type move
with it, with one slope on both queues and across field families, and the attribute models' night and
Saturday terms are its gaps (the night term, 0.32 on the miss logit, is 0.6 times the log of 4.27 over
2.49) and vanish once it is in. A fixed-detection model therefore forecasts November at the third
quarter's pools, which is not 4.1's quantity. November's two rates sit inside the closed shift-days' range
(the support counts), so the forecast interpolates. Every candidate, what rules it out and its margin
(paper figures; each asserted at the build):

| Candidate method | November set | Ruled out by | Margin |
|---|---|---|---|
| R0: the third quarter's measured residual carried forward, Hollings & Pryce at its pilot (or the flat months trended) | N1 to N5 | 4.3 rests the forecast on the plan of record and 4.1 on the documents the plan routes: the motor claims run on nights, Hollings & Pryce's documents are November's, and both pools move | 8 of 11 designations differ |
| R1: detection fixed by attribute (stream, verifier, field type, tenure, shift, time on shift, workload, day of week; alone or together; fixed or random effects) | N1 to N5, D5 | the closed quarter's shift-days: within each queue the misses move with the shift-day pool's error rate, and the night, Saturday and holiday terms are that rate's gaps | 9 of 11 differ; the slope's 95 per cent interval clear of zero in each queue (about five standard errors on paper: the attribute models' overdispersion of 1.3 over the quarter's 78 to 92 shift-days a queue, taken up by one regressor); held-out shift-days at least 15 per cent worse in squared error |
| Detection tied to the stream's own error rate | as R1 | a stream's own rate barely moves across its shift-days, while its misses move with the pool's | as R1 |
| R2: the pool effect on the day queue only | N1 to N5, D2 to D6 | the plan doubles the night pool's rate (the motor claims arrive), and the night queue's own shift-days carry the same slope | 5 of 11 differ; the night slope's interval clear of zero and holding the day slope |
| R3: both pools, Hollings & Pryce at its pilot | N4, D2, D3, D4 | 4.3, the same method for every stream, a new client's included; the slope is common across field families within verifier, the pilot's typed fields inside it | 1 of 11 differs: D6 at 1.15 against 0.75 |
| Detection on the pool's mix in place of its rate (stream or form-family shares, or a stream's own share) | no forecast inside the data | the shares add nothing once the rate is in (the rate is the share model with each share weighted by its stream's error rate, and that tie holds on the closed quarter); November's full mix lies outside every closed shift-day's (Hollings & Pryce 36 per cent of the day's key fields, the motor claims 36 per cent of the night's) while its two rates lie inside | the support counts: at least ten closed shift-days at or below 1.87 and ten at or above 5.02 |
| The rigorous family (the ladder's list) | N4, D2, D3, D4, D6 | converges | every ratio at least 0.10 from 1.00; the set holds at both ends of the slope's 95 per cent interval |

Form 2 does not apply: no governing standard in this world states a general method for forecasting a
verification step's accuracy, and human reliability assessment's general method (an error probability
under the conditions the task will run in) is met as well by the attribute models, which carry the plan's
shift, roster and client changes; a sentence that separated them would name the pool's condition, which
the pack never carries. Form 3 is not needed, and it cost: the filed back-test sent every solver to the
shift grain where the pool's rate shows, and task446, newest on main, files a leave-one-out back-test of
its own.

## Closure table

| # | Axis | Reading and closure |
|---|---|---|
| 1 | Population | every key field first-pass verified on documents the plan routes in November (4.1); the fit population is every audited field of the closed quarter; C1: timeouts kept twice or collapsed give the same set (asserted) |
| 2 | Unit of account | the key field (4.1, per 1,000 key fields); C1: document-weighted fits give the same set |
| 3 | Attribution window | the shift's start date (the register's shift-day); November is shift-days 1 to 30; C1: calendar-day attribution gives the same set |
| 4 | As-of dating | tenure as at each shift-day from the effective-dated register; the November roster as the plan files it; C1 |
| 5 | Version basis | one operating plan of record and the audit's adjudicated value; pinned at authority (QCP-04 4.3, the plan's version block) |
| 6 | Divisor | key fields first-pass verified (4.1), not documents and not fields after second pass; C4: the after-second-pass reading breaks 4.1 |
| 7 | Weighting | field-weighted over the stream's November shift-days (4.1); C1: day-weighted gives the same set |
| 8 | Window length | the last closed quarter (4.3); C3: fits on any two of its months give the same set |
| 9 | Boundary | a forecast equal to the limit stays off (4.2); no forecast within 0.10 of its limit under any rigorous variant (C4 margin) |
| 10 | Rounding path | unrounded forecasts against limits (4.2); ask figures rounded once at the end |
| 11 | Tie-break | none arises: nothing ranks methods, and the rigorous family gives one set with every ratio at least 0.10 from 1.00 (asserted) |
| 12 | Maturity | every closed-quarter shift's audit is adjudicated in the export (asserted zero open items) |
| 13 | Order of operations | model per field then aggregate per stream, or aggregate then model; C1 |
| 14 | Row order | no dependence (asserted on two shuffles) |
| 15 | Duplicates | a timed-out screen's later submission counts (the log's dictionary); C1 as axis 1 |
| 16 | Identity | reissued verifier IDs resolved by effective date; C1: a naive ID join gives the same set |
| 17 | Netting | verifier-introduced errors count (4.1 counts any value that differs from the image); C1: about 0.1 per 1,000, the set unchanged without them |
| 18 | Units | every rate and limit per 1,000 key fields on the main path; currencies and billing units appear only on ask paths |
| 19 | Codes | the audit's outcome codes defined once in its dictionary; client reason codes are ask-only |
| 20 | Integerisation | none on the call |
| 21 | Clause scope | 4.3 makes every stream's forecast, a new client's included, by the same method (closes R3; R2 falls to the night queue's own slope); 4.2 applies per stream |
| 22 | Forward window | the plan's November shift-days and daily volumes (Saturdays, US Thanksgiving on 26 November); C1: monthly-average pools give the same set |

## Literal reader

Executing the prompt and QCP-04 4.1 to 4.3 word for word, a reader forecasts every stream's November
first-pass residual by one method from the last closed quarter's records and the plan of record, and puts
on second pass every stream whose forecast exceeds its limit. The text names no method, and the design
forces one (form 1, `## The estimand, the rule and the records`): the closed quarter's shift-days rule out
every fixed-detection model, R2 falls to the night queue's own slope, the mix models add nothing once the
pool's rate is in, and the rigorous family converges on the golden (asserted). R0 and R3 each break a
quotable sentence (for R0, 4.1's "routes to the stream's queue" and 4.3's "the operating plan of record";
for R3, 4.3's "by the same method"), every row of the semantic fork table is ruled out or converges, and
the default path's answer comes from an easy method on the same literal estimand: detection fixed by
attribute, which never contains the pool's rate.

## Oracles

- The closed quarter's audit: on the wrong path it reproduces every stream-month (the attribute models
  back-test clean month by month); it ties under both models at the monthly grain, refutes fixed detection
  at the shift-day grain only once a solver builds the pool's rate, and cannot generate that candidate.
- The edit log's field corrections against the screens' counts: tie on every path.
- Each client's own third-quarter audit: reconciles with the centre's audit on capture errors under every
  handling of the main call (ask C's device lives in its clock, not in its totals).
- The October second-pass list in the plan: correct for October and labelled so; it reproduces R0's set
  for October and answers no November question.
- The Hollings & Pryce pilot report: the pilot's measured residual (0.75 of the limit), a correct past
  figure that reproduces the default path's off for the new client; no forecast, no recommendation.
- No control total, published figure or corpus ties only under the golden basis.

## Ask sheet

| Ask | Use (H18) | Primary device (silent) | Hazards | Span (causal files) |
|---|---|---|---|---|
| A. Second-pass hours November would take, every stream (whole hours) | the capacity beside the call; operations staffs the second-pass team from it, for any stream the council signs | D6, an event's quantity repeated on every covered line with the grain unstated: the second-pass workflow export writes one line per document worked in a session and repeats the session's productive minutes on every line; the over-cleaning half is real, since a session crossing the shift handover is split into two lines under one session id, each with its own part's minutes, so a blanket dedupe on session id drops real minutes. Every form family carries both shapes | H3 form versions effective mid-November (key fields per document; the plan gives key fields and second-pass rates run per document) | plan, stream register, form specifications, second-pass session export, workforce register, labour planning note, holiday calendar, pilot report (the pilot's second-pass sessions) |
| B. Credit at stake if the stream broke its limit in November, every stream (contract currency, whole units) | the exposure beside the call | D2, the version of record is the latest accepted, not the latest delivered: most clients sent a forecast revision after the plan's cut-off; nothing names the accepted one, and only the plan's key fields, read back through each form version's key fields per claim, show which revision the plan used. A stored label taken before a silent switch adds to it: the billing register keeps each account's October volume band, and the account's November volume across its streams moves Kessington, Wattlebird and Hollings & Pryce to another band | H1 units set per source (Harbison forecasts claim lines, Thistlecombe first notifications, Hollings & Pryce bundles); H2 client calendars (US weeks from Sunday, Australian fiscal weeks) cut to November; H5 anniversary indexation part-way through November (Coolabah 9, Whinfell 16, Brightmoor 20) | client forecast files (five or more), rate cards, quality schedules (credit percentage), billing register, stream register, plan, form specifications, Australian fiscal calendar |
| C. Third-quarter residual as each client's own audit counted it, ten streams (errors per 1,000 key fields, one decimal) | the trail that audits the measure behind the limits; account managers bring it to the council | D8, a clock against a filed cutoff: the quality schedules count claims delivered in the quarter by the client's local date, and the client audit exports stamp delivery in UTC with no zone marker; only the delivery manifests (IST with offsets) show it, so late-June and late-September deliveries move in or out of the quarter on every stream | H4 client reason codes (capture errors beside eligibility, coverage and duplicate-claim rejections); H6 a re-reviewed finding supersedes the first; H3 form versions within the quarter (key fields per audited claim) | client audit exports (four or more, in their own formats), quality schedules (codes, measurement clause), delivery manifests, form specifications, stream register |

**Hazard table.** H1 moves B; H2 moves B; H3 moves A and C; H4 moves C; H5 moves B; H6 moves C. Each
hazard's per-ask delta and every subset of mishandlings is composed and asserted outside the bin.

**Off path.** Every device row sits in a file the main call never reads (session export, billing register,
client forecasts, rate cards, client audit exports, delivery manifests, form specifications); the shared
files (plan, stream register) carry no device row inside the main call's declared population (zero-count
asserted). **Referee**: the delivery manifests, byte-clean, arbitrate ask C's clock and hand over no level.
No filed rule adjudicates a primary; no column isolates a primary's rows.

**Cracker sheet.** The response that landed the call, ran the hygiene battery, executed every filed rule
and reconciled every control:

| Ask row | What the cracker does | Against the golden | Cracker |
|---|---|---|---|
| A, hours for the eleven streams | the battery flags repeated session ids; it dedupes on session id (or, without the battery, sums every line) | dedupe drops the split sessions' second parts and sums inflate multi-document sessions, so every family's rate is off and every stream's hours fall outside the bin | miss |
| B, credit at stake for the eleven streams | takes each client's latest delivered revision, executes the filed units, calendars and indexation dates, prices at the billing register's band | the revision and the stored band move every stream's November invoice outside the bin | miss |
| C, client-audited rates for the ten streams | filters capture codes, takes re-reviews, reads the export stamps as the client's local date | boundary deliveries land in the wrong quarter on every stream; every rate is off by more than its decimal | miss |
| Chart series (hours against credit at stake) | plots its own A and B values | every point off | miss |
| Chart order (by credit at stake) | orders by its B values | the order differs from the golden's (asserted) | miss |
| Chart title (the stream carrying the most credit at stake) | names its own leader | names another stream (asserted) | miss |

**Mirror sheet.** The response on R1 files the same ask values as the cracker (every ask is decoupled from
the call); its sheet differs only in the recommendation criteria.

Pair ceiling: 34.5 (the one-cracker case, r about 6 for Brightmoor's yes and Wattlebird hospital's no if the rubric grades per stream, ask leakage 0.10 for each top response: (38 + 7 + 5.5 + 6 + 7 + 5.5) / 2; at the ask gate's 0.2 each it is 40.0)

**Returned-task revision readiness.** The asks' data lives in ask-only files, so an ask-only revision
changes no byte the main call reads.

## The pack (provisional)

About twenty files in five formats. Main path: `first_pass_verifications_2026q3.parquet` (the spine,
about 2.1 million document screens), the first-pass edit log (field grain), the blind re-key audit (field
grain), the workforce register, the stream register, the November operating plan (xlsx: routing, daily key
fields by stream, roster, the October list), QCP-04 (docx), the clients' quality schedules (pdf), the
Hollings & Pryce pilot report (docx: dates, volumes, measured accuracy, no forecast). Ask paths: the
second-pass session export, the labour planning note, form specifications, the client forecast files, the
billing register, the rate cards, the client audit exports, the delivery manifests. Distractors (named in
`metadata.json`): the OCR engine's confidence summary by stream and field (a tempting error proxy; the
audit is the measure) and the verifier keystroke telemetry (fields per hour, a tempting workload signal).
Dictionary and provenance in the organisation's own idiom. `prompt.txt` is the architecture 2 draft (it
passes `voice-check.py`); `prompt.md` is architecture 1's and goes with the old pack at the build.

## What the generator must add or change

Architecture 2 replaces the Drumlee generator's content module by module; nothing of the patient-app
world is kept, and the generator rebuilds the pack from scratch.

- `world.py`: Tamralipta's clients, eleven streams, form families and versions, contracts (limits per
  1,000, credit percentages, rate cards, bands, anniversaries), the four calendars (US, UK, Australian,
  Indian), about thirty verifiers with hire dates, reissued IDs and shift assignments, the November plan
  and roster.
- `sim.py`: daily volumes per stream per shift-day (weekday pattern, Saturdays without UK paper, the
  holidays above, ordinary noise); documents and key fields per document by form version; OCR errors per
  field by stream and field type; pooled dispatch per shift; the detection truth (miss logit = constant
  minus 0.6 times the log of the shift-day pool's rate, plus field family, verifier skill, small time on
  shift and time of night terms); small false alarms; timeouts; the audit sample and its adjudication; the
  Hollings & Pryce pilot (six weeks at low volume across Saturdays and the bank holiday); second-pass
  sessions with multi-document and handover-split shapes; client audits with reason codes, re-reviews and
  UTC stamps; forecast revisions and billing bands; the November forward truth for assertions only (never
  shipped).
- `docs.py`: QCP-04 with 4.1 to 4.3 (estimand, rule and records, with no method and no selection
  criterion) and the audit design, the quality schedules, the pilot report, the labour planning note, the
  form specifications, the operating plan, the rate cards, the billing register, the client forecasts in
  their own formats, the dictionaries, the distractors.
- `variants.py`: R0 to R4, the default path's attribute family (best fit, clean monthly back-test), the
  own-stream-rate and mix models, the rigorous variants, every ask stop.
- `tune.py`: error rates, limits and volumes so every margin holds (monthly pool stability, the November
  pools, the ratios, the slope corridor, the form 1 separation, the support counts).
- `checks.py` asserts: the monthly pool bands (day 4.2 to 4.4 per cent, night 2.4 to 2.6); the support
  counts; every default-path model's clean monthly back-test and its November set R1; the form 1
  separation: the pool-rate slope's 95 per cent interval clear of zero within each queue with the attribute
  terms in, the two queues' slopes inside each other's intervals, one slope across field families within
  verifier (the pilot's typed fields inside it), every attribute model and the own-stream-rate model at
  least 15 per cent worse than the pool-rate model in squared error on held-out shift-days, the mix models'
  shares adding nothing once the rate is in, and November's full mix outside every closed shift-day's on
  both queues; the shift, Saturday, holiday and tenure terms collapsing once the pool's rate is in;
  R0 to R4 by name and the grid by cell; every rigorous variant on the answer with every ratio at least
  0.10 from 1.00 and across the slope corridor; every SF row (SF1 to SF15); main-path texture unable to
  move the set; zero device rows in the main call's population; the clean-data test per suspect file and
  the lens-swap test; ask goldens, stops, deltas, bin distances, the per-cell device incidence and the
  necessity matrix; the cracker and mirror sheets; the input gates; two builds byte-identical; no pack
  sentence carrying pool, prevalence, vigilance or criterion, and none naming, selecting or scoring a
  forecast method; no em dash.
- `verify.py`: recomputes the call, the form 1 separation and every ask figure from the bundle alone.
- `golden.py`: `november_second_pass_plan.xlsx` and `second_pass_november.pptx`.
- `pack.py`, `postprocess.py`, `deliver.py`, `make.py`, `build.py`: the new file list, `metadata.json`
  with the distractors, `target.zip`.

## Coordination

DRAW REGISTERED 2026-10-11. task229's design 2 (perssathya/task229-rework) registered first and sorts
before task230; its card holds `compliance_or_audit` and `operations_log`, which BLOCKed this card on
`ban.role` and `ban.artifact`, so the requester was redrawn from the head of quality to the centre's head
of operations (`operations_director`) and the context artifact to the November operating plan
(`capacity_report`), with the stakes, the call, the pack, the ladder and the stump unchanged; the scratch
`check` and `heart` then returned WARN with no BLOCK, the card was registered on this branch, and
`pipeline.json` moved to stage 3 (build next). task228 was checked at its architecture v2 (2e502d1); an
architecture 4 filed later also sorts before task230, so `heart` re-checks this card's furniture against
it. Against task229 v2: its decisive step is a count that resets the record it reads, not a human's
detection (driver similarity 0.02, no `test.same_driver`); its decision type and Gate G mechanism
are the two WARNs answered below; its organisation family, forum and forcing event differ. Main has
since merged task446 (e89a676): it shares Gate G `method_or_model_selection` and gap time and population,
its driver carries a screen's error rates across a moving base rate, and it files a leave-one-out back-test.
This note files no criterion (form 1), so the organ does not repeat, and `guard.py check` on the merged
tree at the form 1 pass returned the draw's WARN set unchanged and nothing against task446 (nearest drivers
0.05, task446 not among them).

## WARN answered

- `repeat.gate_g` (method_or_model_selection, task228 v2 and task229 v2): task228 chooses among estimators
  of each sensor's own random error against a signal nothing observes, and task229's design 2 among
  estimators of a record's standing accuracy from counts that reset it; here the choice is between a fixed
  detection model and one where a human verifier's detection follows the error rate of the pool it works,
  settled by the closed quarter's shift-day dose-response, which forces the method with nothing filed to
  select it.
- `repeat.decision` (designation_set, task229 v2): task229's design 2 designates the distribution centres
  whose pick-face records clear a peak accuracy gate, built from what each record accrues since its own
  last count; here the set is client streams put on a second verification pass from forecast human
  detection.
- `test.same_driver_older` (task33, task114): differentiated on the card (task33's forward yield stops at a
  filed intervention recovered from closed actions; task114's demand exists only where two parties share a
  site; here nothing is recovered from closed actions and every record is exact).

## Stopping rule

Architecture 2 of 3. Three hardening loops; a round that lands the call (the five streams) sends it back
to design with a brief and the default path rewritten; a round that misses the call but leaks the asks
rebuilds the ask layer; a third loop that still lands re-roots task230 to architecture 3; a third spent
architecture retires the number. A draw that fails `precut.py` twice on the default path is re-rooted
before any data is cut.

## Build (architecture 2)

Built 2026-10-11 from the committed design; no rung, pin or decisive step changed. `generator/make.py` builds
the pack, runs 172 assertions (`checks.py`), writes the goldens, `figures.json` and `metadata.json`, runs
`verify.py` (own joins, own likelihood fit, rate cards parsed from the PDF), rebuilds byte-identical and cuts
`target.zip`.

- **Pack as built**: 27 files in seven formats (parquet, csv, xlsx, docx, pdf, json, md); spine
  `first_pass_verifications_2026q3.parquet` (1.26 million screens; the audit, the largest file, 2,381,352 rows), field edits, the blind re-key audit (field
  grain), workforce register, stream register, the November plan, QCP-04, quality schedules, pilot report,
  September second-pass sessions, labour note, form specifications, five client forecast files, billing
  register, rate cards, four client audit returns, delivery manifests, MIS notes. Distractors in
  `metadata.json`: `ocr_confidence_summary_2026q3.csv`, `verifier_keystroke_telemetry_2026q3.parquet`.
- **Sets as built** (ratio of forecast to limit): golden N4, D2, D3, D4, D6 (1.22, 1.26, 1.25, 1.26, 1.22; the
  other six 0.73 to 0.80; margin 0.20). R0 N1 to N5 (margin 0.106); R1, the best-fitting attribute model by
  AIC (A6), N1 to N5 and D5 (margin 0.08), every family-coded attribute model the same set; R2 N1 to N5 and
  D2 to D6 (0.104); R3 N4, D2, D3, D4 (0.106). Grid: six distinct sets, the roster toggle moves none, the
  answer only with both effects and the new client inside.
- **Rigorous family**: every variant on the golden set, every ratio at least 0.112 from 1.00 (linear
  probability 0.112, within each queue 0.114, the day-type and shift terms added 0.121, the rest 0.16 to
  0.21), both ends of the slope's interval included.
- **Form 1 separation**: pooled slope 0.63 (se 0.032); within queue day 0.60 (se 0.070), night 0.50 (se
  0.077); attribute models 1.52 to 1.81 times the golden's squared error on held-out shift-days, the
  own-stream-rate model 1.59; the shares test p 0.06; support 11 day and 14 night shift-days; the night term
  (z 18 without the rate) and the day Saturday term (z 6.5) collapse once the rate is in.
- **Asks**: the cracker (dedupe on session id, latest delivered revision at the stored band, UTC stamps read
  as local dates) misses all 35 ask and chart rows; pair ceiling 30.6 measured, 34.5 at the design's 0.10
  allowance.
- **Builder's choices inside the design** (none moves a rung): night audit share 30 per cent and a full
  re-key of the pilot, so the shift-day rate is measured tightly enough at night and on typed forms; the
  Hollings & Pryce limit printed to two decimals (0.77) because one decimal could not hold the D6 margin; the
  month-by-month back-test is the in-sample stream-month check in standard errors inflated by the model's own
  overdispersion (worst 2.13); the holiday day-type terms (three days) are reported, not asserted; the client
  audit device is tuned in the generator (boundary-batch findings and clean sampled claims) until every
  stream moves by more than its decimal under the UTC reading and every golden rate sits off its rounding
  edge; hours and credits are kept off their rounding edges by a document or a bundle in the accepted
  forecast's first full November week; the chart orders streams by credit converted at the plan's budget
  rates (the plan's Budget rates sheet files the convention), and the leader is the same at nominal values.

**leak.py REVIEW lines answered (final cut, sha256 in `pipeline.json`).**

- Sweep 3, 4.3 in QCP-04: the clause number 4.3, not the third-quarter day rate.
- Sweep 3, 5.2 in the quality schedules: Kessington professional's limit, a contract figure, not the night rate.
- Sweep 3, 0.80 in the rate cards: Thistlecombe's Plus-band price, not a ratio.
- Sweep 3, 3.9 in the rate cards: Whinfell's indexation percentage, not a client-audit rate.
- Sweep 4, QCP-04, the MIS notes, the pilot report: the shared words (forecast, method, quarter, shift-day,
  closed) are the procedure's own vocabulary; no sentence names the shift-day rate, a dose-response or one
  client's volume moving another's accuracy, and none names or scores a method (asserted in `checks.py`).
- Sweep 9, dates after 28 October in the form specifications, the plan, the stream register and the
  forecasts: November effective dates, shift-days and forecast weeks, which a plan for November carries.

## Architecture 1 (spent at hardening loop 2 of 3, 2026-10-11)

The series-break flag after the 7.0 tracker swap, as hardened at loop 1 and cut for round 2; rounds 1 and 2 landed the call and loop 2 found no rung on paper. Kept as the record; nothing below binds architecture 2.

### DRAW

| | |
|---|---|
| Seed territory | DQ03 (an event-volume drop read as an instrumentation incident or a mix shift toward a new client version), drawn in the seed's own territory: product-analytics, metric-definition-measurement-science. The guard allows the pairing again since task228 re-rooted to physical-environmental-sciences; no later seed in this block (task231 to task252) sits in this task type. |
| Pairing | product-analytics (client domain) / metric-definition-measurement-science x Data Quality Monitoring & Alerting |
| Niche | a public hospital group's patient app whose 7.0 build swaps the analytics SDK, reaches frequent users first and cannot run on older phones, as the winter season lifts traffic; which KPI series carry a series-break flag in the quarterly return to the programme that funds the app |
| Committed call | the set of patient-app KPI series that carry the break flag in the Q4 return (forward: the flag marks the Q4 series, ISO weeks 40 to 53, and from 1 December 6.8 is refused at sign-in, so every patient using the app is on the new tracking for the rest of the quarter) |
| Shape | 07, grid of cells: ten KPI rows, each with its settled change (whole per cent) and its flag, plus its Q4-to-date value (a flagged series on the new basis, NPAP-STD-07 5.2); the weekly active patients for weeks 40 to 46 and those on the new tracking from week 41 |
| Card | gap population, time; pattern none, G6 decisive with G17; gate_g method_or_model_selection; stump_strategy causal_design; calibration none; artifact monitoring_export; role research_desk; forum funder_or_donor; forcing other (a funder's mid-quarter pre-notification deadline, re-keyed from statutory_or_regulatory_filing at the heart check); org hospital_or_health_provider; Ireland; layer2 estimand_identification, own:not-yet-switched-pool-held-to-units-able-to-switch (loop 0's product-analytics/observational-causal-inference/1 kept in `lineage`) |
| Guard | registered at WARN: repeat.decision (designation_set against task229), answered below; NOTE test.same_driver_older against task68, differentiated on the card. At the heart check task135 (drawn the same day, regulator filing) had entered the window: the forcing event is re-keyed to `other` (a funder's mid-quarter pre-notification deadline, which is not a statutory or regulatory filing), heart WARN; repeat.deliverables (pdf+xlsx against task135) answered below. Hardening loop 1 re-keyed the driver, the stump and the Layer 2 pattern (the decisive rung moved); check and heart re-run with the live task228 and task229 cards copied in for the run only (verdicts under WARN answered) |
| Nearest exemplars (idea seeds only) | Paid User Acquisition (mean 0.58: the model rejected the dated bid switch by a difference against never-switched campaigns 4 of 4, so a plain before-and-after is no stump here); E-commerce Contribution Margin Diagnostics (mean 0.41) |
| Personas (guard names, Ireland, seed 230) | Sandra Fitzpatrick (head of digital analytics, the prompt's "I"), Erica Phayre (programme data lead, the request email), Lesley Ahearne (identity and access, the service account register); the three on the card's `world.people` |
| Loop | architecture 1, spent at hardening loop 2 of 3 (on paper, `## Hardening loop 2, on paper`): round 1 landed the call on its step 6 (the trend held within CRM engagement segment, now R4) and round 2 on its steps 6 and 7 (the same pool held to phones that can take 7.0, the answer R5); re-root pending |

**Stump sentence.** A competent solver drops the non-patient accounts, takes each patient's handover week from the first
Dunnock row, and carries each switched patient's reference level into every settled week by the movement of patients
still on 6.8 in the same CRM engagement segment (the conditional-parallel-trends difference-in-differences of a staggered
rollout), then confirms it against never-switched patients and a group-rate index; the step that lands it there is
taking everyone still on 6.8 in the segment as patients who have not switched yet, when a patient active on 6.8 after the
release either declined the update or has a phone that cannot run 7.0 (iOS 16 and Android 10 are its minimum), and inside
every segment the pool fills week by week with those older handsets (22 to 25 per cent of each segment's pool in W42,
28 to 49 per cent by W46), whose appointment, change-request, results and notification traffic climbs 10 to 21 points
faster into the winter than other patients' of the same segment. The segment trend flags appointment change requests
(-6.0) and notification opens (-4.0), which measure inside the line, and clears appointment views (+1.0) and test result
views (+0.5), which break at +5; it files five flags with two wrong and two missing, misses all ten whole-per-cent cells,
and its never-switched, additive, group-rate, reweighted, Poisson and finer-strata siblings land on the same five flags
within a point of it. Held within segment and to phones that can run 7.0, the five flags are appointment views, test
result views, clinic letter views, waiting list checks and digital check-ins.

**Data-native sentence.** This dataset's switch arrives through an app update that each patient meets at their next
sign-in and that only a phone at or above 7.0's minimum OS can take, so frequent patients switch first and, inside every
engagement segment, the patients still on 6.8 in a settled week are a mix of those who have not taken the update yet and
those who never can; the second group grows week by week as the first one switches, and its own winter use is not what
the switched patients' would have been.

**The two layers.**
- Layer 1, realistic mess and the systems that produce it: one warehouse table holding every account the app touched
  (patients, dependant profiles a carer manages, second-site registrations the patient index merged in November, staff
  test accounts on the 7.0 betas from W38, training and store-review logins, new registrations since 28 September,
  lapsed patients returning in the winter), two rows for an account in the week it changed tracker, a merge register
  whose chains need walking, a service account register whose staff-domain rule sits on its second sheet, a continuity
  standard that restates a flagged series' quarter on the new basis, and the exports' grains stated once in the
  warehouse notes.
- Layer 2, the shortcut the stump rests on: reading the switch against everyone still on 6.8 in the same engagement
  segment (conditional parallel trends on what orders adoption) when the update can only reach phones at or above 7.0's
  minimum and the patients it cannot reach move differently in the winter; an expert compares like with like on
  eligibility to switch, holding the not-yet-switched pool inside each segment to patients whose phones can take 7.0.

**The three rules.**
- Domain (`domain_test`): the deciding quantity is the change a tracking-SDK swap makes to each patient-app KPI's
  events per weekly active patient, estimated from an app-update rollout that frequent users take first and that phones
  below the build's minimum OS cannot take, against patients not yet updated within the same engagement segment who
  could update: product analytics measurement science (metric continuity across client releases, update adoption and
  device support, per-active-user KPIs). With ward, meter or school nouns there is no app update met at sign-in, no
  minimum OS gating the switch, no engagement segment ordering it and no tracking SDK, and the task stops reading the same.
- Both layers: named above.
- Decisive step class: analytical (`analyst_test`): a strong analyst who drops the non-patient accounts, maps the
  handover weeks, reads NPAP-STD-07 correctly and carries each switched patient's reference level by the movement of
  patients still on 6.8 in the same engagement segment, with a never-switched control and a group-rate index agreeing,
  still flags appointment change requests and notification opens and clears appointment views and test result views,
  because inside each segment the pool still on 6.8 drifts toward phones that cannot take 7.0. Reading
  `last_sign_in_os` and `minimum_os` correctly does not move the answer; choosing the comparison pool does.

### GATE G

- Litmus: nothing in the pack reports a settled change, ranks the KPIs on the break question or states a flag for Q4;
  every file is correct about what it describes (the Q3 return's "No" flags are Q3's, when nothing changed). The task
  overturns no reported number. `surface_read_dependency: no`, `stumping_family: analytical_non_defect`,
  `sole_data_defect: no`.
- Mechanism: `method_or_model_selection` (the comparison pool that carries the counterfactual trend).
- Delete every wrong number from the pack: still hard, because nothing wrong is in it; the segment comparison is built
  by the solver from correct rows.
- Lens-swap test: the segment and the segment-and-eligibility routes take the same A (the same switched patients'
  new-tracking events in the same settled weeks) and estimate the same filed B; they differ only in which patients'
  movement models B. That is a choice of estimator for one fixed estimand, not two lenses on one population.
- Clean-data test: no file on the main path is incomplete, stale, superseded, delta-shaped or filtered (the segment
  file is the one snapshot taken before the release; the warehouse table is complete to W46, extracted the Monday
  after; the register's `last_sign_in_os` is the phone every cohort account signed in on, and no account below the
  minimum ever has a Dunnock row). Nothing to repair, so `answer(repaired) == answer(shipped)` holds trivially and is
  asserted as "call unchanged with every non-cohort row deleted".

### The estimand, and what rules out the segment trend

NPAP-STD-07 3.1 defines the settled change as A / B - 1, with A the new tracking's events for the switched patients in
their settled weeks, all taken together, and B "the KPI events the same patients would have recorded in the same weeks
if the old tracking had stayed in place". 3.2:

> "The estimate starts from each switched patient's own KPI events per active week in the reference period, and carries
> that level forward to each of the patient's settled weeks by the movement the patient's own use would have shown over
> those weeks with the recording unchanged. Movement that has nothing to do with the recording, whether seasonal,
> operational or in the way patients use the app, belongs in B, so that A and B differ by the change of tracking alone."

The standard names no estimator, no segment, no device and no comparison group, and this loop added no word to 3.1 or
3.2. The segment trend carries each level forward by the movement of everyone still on 6.8 in the segment, which is the
movement "the patient's own use would have shown" only if those patients are the ones who would have switched later.
The shipped rows say they are not. Every line below is an assertion in checks.py (block "the data's own case"), and
verify.py recomputes the call, the segment-only pool and the segment x phone class x volume pool on its own long-table
path.

1. The switch never reaches a phone below 7.0's minimum: no account whose `last_sign_in_os` sits below the 7.0.0 store
   rows' `minimum_os` (iOS 16, Android 10) has a Dunnock row (0), and no switched patient's settled week is on one (0).
   12.9 per cent of the cohort's phones are below it.
2. Inside every segment the 6.8 pool's share on those phones climbs every week from W42 to W46: occasional 22.2 to 27.6
   per cent, regular 24.1 to 38.2, frequent 25.2 to 48.9; the switched patients' settled weeks hold none.
3. On the old tracking, W42 to W46, patients on those phones outrun other patients of the same segment: appointment
   views by 10.5 to 16.4 points, appointment change requests 13.1 to 21.2, test result views 10.2 to 16.8, notification
   opens 9.7 to 15.9, digital check-ins 7.6 to 8.8 (each segment's own figures in checks_out).
4. Before the winter the two groups move together (W33-36 to W37-39, every KPI and segment within 2.9 points) and their
   reference-period levels match within 1.7 per cent, so nothing in the reference period or a pre-trend check over weeks
   33 to 40 separates them.
5. Placebo on every eventual switcher's own old-tracking weeks from W42 to the week before its handover, predicted from
   patients with no handover by W46: the whole 6.8 pool misses appointment views, change requests, test result views
   and notification opens by 6.2 to 6.6 per cent, the pool within segment by 3.2 to 4.0 (adding reference volume changes
   nothing), the pool within segment and to phones that take 7.0 by 0.2 to 0.5 (every KPI within 1.5).
6. Inside segment and phone class the switch is flat across reference-volume quintiles and activity bands (occasional
   46.8 to 50.0 per cent switched by W46, regular 71.9 to 73.0, frequent 82.4 to 84.6), and the share of phones below
   the minimum is flat across volume quintiles (86.1 to 87.9 per cent able to take 7.0 in every cell of 300 or more).
7. Nested: the segment crossed with reference volume, reference activity, the CRM sign-in weeks or the phone's platform
   stays on the segment trend's five flags without the phone class, and returns the answer within 0.06 points with it.

So 3.2's "the patient's own use" rules out any pool whose share of phones that cannot switch differs from the switched
patients' (none), whatever else it is matched on; a pool held within segment and to phones that can take 7.0 gives the
five flags under every refinement tried.

#### Why the segment still matters (the lower rungs)

The loop-0 closure stands one rung down. Among patients whose phones take 7.0 and who never switched, occasional
patients' appointment views, test result views and notification opens climb 40.2, 42.9 and 37.7 per cent by W42 to W46
against frequent patients' -2.0, -2.1 and -2.5; the switched patients' settled weeks are 16.4 / 39.6 / 44.1 per cent
occasional / regular / frequent against the pool's 32.6 / 38.3 / 29.0; and the eligibility pool without the segment
(R3e) lands on the segment trend's own five flags. Patients first signed in during W40 (1,874 accounts, 684 with a
settled week) hold no 1 October segment; every handling returns the same five flags and ten cells within 0.2 points
(left out, the golden; their own stratum; read as occasional, regular or frequent; new registrations and returners as
two strata). No convention is filed.

### ENTITY, DECISION, ANSWER

- Entity: a KPI series (ten), scored on its settled change in per cent; three quantities that read as "the change":
  against everyone still on 6.8, against everyone still on 6.8 in the same engagement segment, and against patients
  still on 6.8 in the same segment whose phones can take 7.0. They flag different series because adoption runs by
  segment, the season runs by segment, and the pool inside each segment fills with phones that cannot switch.
- Decision: the subset of the ten series that carries the break flag (|settled change| > 3 per cent, NPAP-STD-07 4.1).
- Answer: appointment views (+5.16, reported +5), test result views (+4.86, +5), clinic letter views (+7.17, +7),
  waiting list checks (-7.18, -7), digital check-ins (-9.12, -9). The five continuous series: appointment change
  requests -1.14 (-1), messages sent -0.21 (0), repeat prescription requests -0.13 (0), pre-assessment forms -0.17 (0),
  notification opens -0.15 (0).
- Margin: the nearest series to the line are appointment change requests (1.86 points inside) and test result views
  (1.86 outside); across 18 defensible variants the nearest is test result views at +4.70 with the W40 newcomers read as
  frequent, 1.70 outside.

### LADDER

Every rung is computed from the shipped files by golden.py or checks.py and asserted by its flag set.

| Rung | The analysis | Settled change (appt views, appt changes, results, letters, msgs, rx, waiting list, check-ins, forms, notifications) | Flag set | Why a good analyst files it | Killed by |
|---|---|---|---|---|---|
| R0 | the series itself: events per active account-week, weeks 42 to 46 against the reference period | +8.3, +4.0, +6.9, +1.9, -3.8, -3.3, -3.7, -0.6, -0.3, +3.8 | appt views, appt changes, results, msgs, rx, waiting list, notifications | it is the number the programme will publish | NPAP-STD-07 3.1 (A and B are the same patients) |
| R1 | same weeks, accounts on 7.0 against accounts on 6.8 | +16.0 ... +10.5 | nine series | it is the version comparison every dashboard draws | the 7.0 accounts are the frequent users (selection) |
| R2 | switched patients' settled weeks against their own reference level | +11.7, +4.1, +10.7, +8.8, +1.5, +0.9, -4.8, -4.7, +2.5, +4.9 | appt views, appt changes, results, letters, waiting list, check-ins, notifications | own baseline, no other patients involved | 3.2: seasonal movement belongs in B |
| R3 | staggered difference-in-differences against every patient not yet switched | -3.8, -9.4, -4.2, +4.4, -1.9, -2.3, -9.5, -15.0, -2.8, -8.2 | as R2 | the textbook design for a staggered rollout, pre-trends flat in weeks 33 to 40 | the switch and the winter movement run by segment; the pool is a lighter mix (above) |
| R3' | the same against never-switched patients, or pooled Poisson | never-switched adds forms (-3.15); Poisson -2.12, -7.88, -2.57, +4.95, ..., -6.67 | as R3 (+ forms); Poisson as R4 | the "clean control" or the regression version of R3 | as R3 |
| R3b | R3 within quintiles of reference-period volume | -0.8, -7.2, -1.4, +5.6, -1.1, -1.3, -8.2, -12.8, -1.6, -5.6 | appt changes, letters, waiting list, check-ins, notifications | matching on pre-period outcome level is a standard robustness move | the switch and the winter movement run by segment inside every volume quintile |
| R3e | R3 held to phones that can take 7.0, no segment | -1.3, -5.9, -1.6, +5.3, -1.3, -1.5, -9.1, -13.5, -2.3, -5.9 | as R3b | drops the patients who cannot switch | the segment mix (above) |
| R4 (the stump; round 1's step 6) | R3 within engagement segment (counterfactual movement from same-segment patients still on 6.8) | +1.02, -6.00, +0.48, +5.80, -1.10, -1.27, -8.05, -11.72, -1.28, -4.00 | appt changes, letters, waiting list, check-ins, notifications | conditional parallel trends on what orders adoption, and every robustness check beside it agrees | 3.2 "the patient's own use": inside each segment the 6.8 pool fills with phones that cannot switch, whose winter runs harder (the data's own case, 1 to 7) |
| R4' | R4's siblings: never-switched pool, additive carry-forward, group rates by handover cohort, whole pool reweighted to the switched segment mix, Poisson with patient and segment-by-week effects, segment crossed with volume, sign-in weeks or platform | within 1.0 point of R4 on every series (Poisson furthest: +1.8 ... -3.3) | as R4, every one | the robustness checks round 1 ran (never-switched, group rates) and the ones it could | as R4 |
| R5 (answer) | R4 held within segment and to phones that can take 7.0 | +5.16, -1.14, +4.86, +7.17, -0.21, -0.13, -7.18, -9.12, -0.17, -0.15 | appt views, results, letters, waiting list, check-ins | | |

- "A solver who cleans perfectly, maps handover weeks, conditions the staggered comparison on the engagement segment and
  checks it against never-switched patients and a group-rate index commits to five flags: appointment change requests,
  clinic letter views, waiting list checks, digital check-ins and notification opens."
- Five distinct flag sets across seventeen rungs (asserted at five or more). R4's set is also where R3b, R3e and the
  pooled Poisson land, so every partial correction short of the phone class files the stump's set; R2 and R3 share a
  set with opposite signs on every seasonal series. The segment trend misses every whole-per-cent cell of the grid (10
  of 10, asserted), so a response on it loses the grid as well as the call.
- Sign: R2 errs upward on the seasonal series (+5.9 to +6.6 points on appointment views and results), R3 errs downward
  (-8.9 to -9.1), R4 still downward (-4.1 to -4.4); each correction walks the same way and only the phone class reaches
  the answer.
- Pre-trends: the season starts in week 40, so a pre-trend check over weeks 33 to 40 passes on every rung (eventual
  switchers against never-switched patients within 1.5 points on every KPI, and phones below the minimum against the
  rest within 2.9, both asserted); the evidence against R4 is
  the post-release pool composition and the old-tracking movement by phone class, which the solver has to look for.

### Determinism

**Rigorous variants, all asserted to give the same five flags and the same ten whole per cents, each at least 0.12 from
a rounding edge:** segment x phone class x not-yet-switched pool (the golden), the same against never-switched
patients, the additive (shift) carry-forward against each, handover-cohort x segment x phone class group rates (no
patient levels), the pool of phones that take 7.0 reweighted once to the switched segment mix, Poisson with patient and
segment x phone class x week effects, and segment x phone class x exact sign-in weeks. Largest spread on any KPI 0.59
points (digital check-ins, never-switched against Poisson). The 3 per cent line is tested on 18 defensible variants
(those eight, the five W40 handlings, person-level merges, dependants credited to carers, and segment x phone class
crossed with reference volume, reference activity and platform): nearest 1.70 points from the line,
smallest whole-per-cent margin 0.134, and on every one the flag on the whole per cent equals the flag on the unrounded
change.

**22 axes.**

| # | Axis | Reading, and the move that closes it |
|---|---|---|
| 1 | Population | switched patients per 2.6; the golden takes the 1 October cohort (reference activity, a settled week) and the call is asserted unchanged with every non-cohort row deleted. The comparison pool is held to phones at or above 7.0's minimum, read from the register's `last_sign_in_os` against the release history's 7.0.0 `minimum_os`; the classification is exact (no account below the minimum ever has a Dunnock row, every cohort account in the table has a recorded phone), C1. C3: 1,874 accounts without a segment signed in during W40, 684 of them reach a settled week; every handling moves no settled change by more than 0.2 points, same cells and flags |
| 2 | Unit of account | the patient. C3: read at person level, the second-site registrations join their owners' settled weeks and move no settled change by more than 0.05 points; dependants' events credited to their carers (definitions 3.1 through STD-07 2.8) move none by more than 0.06 (both asserted within 0.1, same cells and flags); no merged-away account holds a segment (0); for the asks the person is filed (definitions 2.1, 2.2) |
| 3 | Attribution window | settled weeks follow the handover week (2.4, 2.5), filed; handover weeks out of A and B (3.4) |
| 4 | As-of dating | one segment snapshot (1 October, before release), C1; merges as the index stands at preparation, every week (definitions 2.2), filed; the phone as at the latest sign-in, and no phone in the cohort changes class inside the window, C1 |
| 5 | Version basis | one vintage of every export, C1 |
| 6 | Divisor | A and B over the same patient-weeks (3.3), so per event and per weekly active patient coincide, C1; Q4 values divide by the sum of weekly active patients (definitions 3.2), filed |
| 7 | Weighting | ratio of totals, "all of them taken together" (3.1), filed; the rival weightings converge within 0.59 points, C3 |
| 8 | Window length | reference period eight weeks (2.3), measurement window to the last complete week (2.7), filed |
| 9 | Boundary inclusivity | "more than 3 per cent" strict; nearest value 1.86 points from the line on the golden route and 1.70 across the 18 defensible variants (asserted 1.5 or more), C3 |
| 10 | Rounding path | whole per cent, sign kept (4.2); flag on the unrounded value, which gives the same flags as the whole per cent on every defensible variant (asserted); every variant 0.13 or more from a bin edge, C3; Q4 values placed 0.0010 to 0.0017 under their two-decimal centre, and restating by the unrounded change gives the same two-decimal values (5.2's "as reported" converges), C3; counts exact |
| 11 | Tie-break | none arises |
| 12 | Maturity, censoring | a W46 handover has no settled week (2.5); W46 complete at the Monday extract, C1 |
| 13 | Order of operations | level per active week, carried, then totals; the group-rate and Poisson variants that reorder it converge, C3 |
| 14 | Row order | group-bys only, C1 |
| 15 | Duplicate resolution | the table is unique on account, week and tracker (asserted); events counted once per event id upstream (notes), C1 |
| 16 | Identity normalisation | one account_ref namespace across the three exports and the service register, C1 |
| 17 | Netting | "either direction" (4.1), filed |
| 18 | Dimensional units | all counts of events or patients |
| 19 | Code and status semantics | tracker, sign_ins, account_type, status, merged_into, last_sign_in_os defined once in the warehouse notes; minimum_os per platform in the release history |
| 20 | Integerisation | none |
| 21 | Scope of a clause | 3.4 applies to A and B; 2.3 counts from the release week of 2.2, which excludes staff betas and store review builds, filed; 5.2 restates flagged series only and only the old tracking's events, filed |
| 22 | Forward window | the flag marks the Q4 series (4.1); the settled change measured to W46 is what the standard uses for the quarter, filed |

**The decisive fork** (the segment pool against the segment pool held to phones that can take 7.0) is not a convention:
3.2 defines B as the patients' own movement, and the shipped rows show the segment pool's movement is not theirs (the
data's own case, 1 to 7). Every rival conditioning set a solver might build inside the segment (reference volume,
reference activity, the CRM sign-in weeks, the phone's platform) stays on the segment trend's flags until the phone class
is added, and returns the answer within 0.06 points once it is.

**7.0.1.** The letter viewer fix (rotation on tablets, published 20 and 21 October, inside W43) changes no recording:
clinic letter views' settled change is +6.36 on W42 alone and +7.34 on W44 to W46, and the same five series flag on
either side of it (asserted).

**Flip conditions.** Test result views leaves the flag only if its settled change falls by 1.86 points, appointment views
by 2.16; appointment change requests joins only if it falls by 1.86; notification opens joins only if it falls by 2.85 or
rises by 3.15; the whole-per-cent cells need a 0.13-point move under the least favourable variant.

### The ask sheet

The grid's settled changes and flags are the main construction. The Q4-to-date block carries the construction's output
on the whole quarter (NPAP-STD-07 5.2 restates a flagged series' old-tracking events by its reported settled change)
through device-carrying rows the call never reads; the weekly block is device-carried (separation zero-counts below).

| Ask | Figures | Construction layer | Primary device | Hazards | Use |
|---|---|---|---|---|---|
| A. Weekly active patients, W40 to W46 | 7 integers | the handover mapping only (none of the counterfactual) | D7 merges: second-site registrations the patient index merged into the first account on 12 to 15 November, 70 of them chained (a later registration merged into an earlier one first) | H1 service accounts, H2 dependant profiles | the activity line the programme weights its national series by |
| B. Q4-to-date value per KPI | 10, two decimals | the flags and the reported settled changes, applied to every old-tracking event of the quarter (W40 included) for the five flagged series, as recorded for the other five (STD-07 5.2) | D5 scope: events on dependants' records count (definitions 3.1) though their rows carry no sign-in | H1, H3 (A's devices in the denominator) | the series level the flag applies to, on the basis the programme publishes it |
| C. Weekly active patients on the new tracking, W41 to W46 | 6 integers | the switch at person grain | D6 grain: an account changing tracker mid-week has two rows; "all sign-ins on 7.0" is a person-week property | H1 (beta testers and store review on Dunnock), H3 merges | how much of each week's series the new tracking carries |

The weekly block cannot carry the counterfactual without asking for a count of patients whose phones cannot take 7.0,
which would name the population the decisive step turns on; it stays on the device layer and its weight is counted as
leakage below.

**Hazard table.**

| Hazard | Organ (documentary / structural) | Moves |
|---|---|---|
| H1 service accounts | definitions 2.3 / service register sheet 1 (training, store review) and its Notes sheet's staff-domain rule (sheet 2) with the register's email_domain | A all 7 weeks (listed and staff halves move different weeks), B 4 of 10 at two decimals, C |
| H2 dependant profiles | definitions 2.1 (sign-in) and 3.1 (records) / sign_ins 0 rows, account_type | A (counting every account), B 10 of 10 (primary), C (counting Dunnock rows) |
| H3 merges and chains | definitions 2.2 / merged_into, status | A (primary), B 10 of 10 (denominator), C (persons) |
| H4 the restatement | STD-07 5.2 / the tracker column, the flags | B: as recorded moves 5 of 10, W40 left as recorded 5, every series restated 1, the segment trend's flags and changes 7, the pooled route's 7 |

**Stops (asserted, values from the build).**
- A: answer 87,189 / 88,577 / 89,973 / 91,503 / 92,888 / 94,803 / 95,957. S1 every account in the table 89,862 to
  99,160; S2 signed-in accounts 87,466 to 96,739; S3 listed service accounts only out 87,237 to 96,004; S3b staff
  domain only out (equals the answer in W45 and W46, when no training or review login was used); S4 no merges 87,386 to
  96,692; S5 one hop only (equals the answer in W40, before any chain existed) 88,580 to 95,976 from W41; over-cleaner,
  cohort accounts only, 85,512 to 89,380.
- B: answer 5.66, 0.92, 4.75, 2.32, 1.38, 1.43, 1.42, 1.11, 0.83, 6.06. As recorded 5.5050, 4.6194, 2.2319, 1.4795,
  1.1719 on the flagged five; the segment trend's flags and changes 5.5050, 0.8867, 4.6194, 2.3061, 1.4096, 1.0875,
  5.9203 where they differ; without dependants 5.6131 ... 6.0302; service kept 5.6811 ... 6.0830; accounts in the
  denominator 5.6253 ... 6.0232. Every value moves under at least three independent mishandlings (asserted at two), and
  restating by the unrounded change gives the same two-decimal values.
- C: answer 15,560 / 27,974 / 37,045 / 44,405 / 50,862 / 55,940 (W41 to W46). Accounts with any Dunnock row 35,061
  to 64,863; signed-in Dunnock accounts 34,395 to 63,292; service out but handover weeks counted 34,313 to 63,245;
  accounts not persons 15,671 to 56,428; listed service accounts only out 15,613 to 55,987. Each stop differs from the
  answer in at least four of six weeks (asserted).

**Separation.** Main-call row population: warehouse rows of the 170,000 accounts in the 1 October segment file. Device
rows inside it: service accounts 0, dependant profiles 0, merged-away accounts 0 (asserted). Every cohort row is a
signed-in week (asserted). No device sits in `last_sign_in_os` (every cohort account in the table has one, asserted).

**Spans.** Each ask crosses five files (warehouse table, account register, service register, return definitions,
warehouse notes), and B a sixth (the standard's 5.2), over eight to ten columns. That is under the eight-file floor; the
pack's main path is five files and the asks cannot honestly reach further without a source of identity facts the
hospital would not keep separately. Recorded as a realism-over-span choice.

**Part 0, the pair (planning weights 35 / 7 / 58 as grade.py scores them; rubric not yet generated).** About 47 ask
criteria: ten settled changes, ten flags, ten Q4 values, seven weekly counts, six new-tracking counts, the note's first
sentence and the chart's parts.
- A response that lands the call and handles the devices the way round 1 did keeps nearly all of them: C near 100.
- The best response off the call, on R4 with the devices handled, keeps six of ten flags, no settled change, the three
  Q4 values of series unflagged on both routes (messages, prescriptions, forms), all thirteen weekly counts and one of
  the chart's parts: about 23 of 47, a leakage near 0.49, so S is about 5 + 7 + 28 = 40. On R3 it keeps eight flags
  and the same Q4 and weekly cells, S about 41.
- With no response on the call the pair sits near 40, the target. With one response on the call it sits near 70, far
  over the bar, and no ask repair inside the 1,000-character prompt reaches it: the build rests, as it did at loop 0,
  on the main ladder keeping every top response off the call. This loop moved ten criteria (the Q4 block) from
  device-only to construction-carried, which cost the mirror about seven of them; the thirteen weekly counts are the
  remaining leak, and the solver round measures the call.

**Referee.** None shipped for the asks: the Q3 return carries a 13-week average weekly active patients figure the pack
cannot reproduce (weeks 27 to 32 are not in it), so it confirms nothing.

### The pack

| Role | File | Main path | Asks |
|---|---|---|---|
| spine (1,295,697 rows) | app_kpi_weekly_by_account.parquet | yes | A, B, C |
| segment snapshot | crm_engagement_segments_20261001.csv | yes | |
| account register (phone of the latest sign-in) | patient_app_accounts.parquet | yes (`last_sign_in_os`) | A, B, C |
| service account register | service_accounts_register.xlsx | | A, B, C |
| release history (minimum OS per release and platform) | app_release_history.csv | release week, `minimum_os` | |
| the standard | npap_std07_kpi_series_continuity.pdf | yes | B (5.2) |
| return definitions | npap_return_definitions_2026.docx | | A, B, C |
| warehouse notes | warehouse_export_notes.md | grains | A, B, C |
| forcing event | npap_prenotice_request.eml | | |
| distractor | npap_q3_2026_return_drumlee.xlsx | | |
| distractor | store_ratings_2026w33_w46.csv | | |
| distractor | tallyfield_order_form_2023.pdf | | |

Twelve files, seven formats (parquet, csv, xlsx, pdf, docx, md, eml). Distractors named in metadata.json and asserted
unused (every answer unchanged with them removed). Producer signatures scrubbed in the generator after each save (H1),
then every Office file laid out the way Office saves it. The register also holds accounts the weekly table never sees,
drawn on their own stream so no graded figure moves (1,316 patients last seen in weeks 27 to 32, 237 dependant profiles
no carer has opened since August, 37 old duplicates the November index run also merged, 57 registrations never
confirmed and five service logins closed in 2025), each with the phone its last sign-in recorded (none for a dependant
or an unconfirmed registration). The `minimum_os` column was already in the release history at loop 0 (6.x needs iOS 15
or Android 8, 7.0 needs iOS 16 or Android 10); this loop added the register's `last_sign_in_os` (one line in the
warehouse notes), the standard's 5.2, and took the Notes-sheet sentence about the registration form out of the service
register (round 1's deferred list).

### The prompt

Stakes-first (the cost of a wrong flag), role mid-paragraph ("under my name"), the question at the end of the first
paragraph; 964 characters and 167 words by voice-check, under the 1,000-character ceiling, ECONOMY clean. This loop
changed one clause: "the forced update on 1 December moves everyone else across" became "the forced update on 1
December retires 6.8", because phones below 7.0's minimum cannot move across and the old clause would have been false
in the requester's own voice. No ask, unit or rounding changed; the Q4-to-date value's new-basis rule lives in the
standard (5.2), not the prompt. No colleague belief, no closing role line, no chart title, nothing marked on the chart,
no runner-up. Criteria off shape 07: ten KPIs by three cells, seven weekly counts and six new-tracking counts, the note's
first sentence and the chart's parts, about 50.

### Leak check

Loop 0 (rounds 1 to 3 of the stage 4 reader, all with questions 1 to 4 answered "none"): the realism tells of read 1
were fixed in the generator, the main-call fork read 2 named (whose old-tracking movement stands in for 3.2's "own use")
was closed by the data, and read 3 deferred one soft question-3 tell, the Notes-sheet sentence about the registration
form refusing drumleehg.ie addresses, which this loop removed.

Loop 1, `leak.py` on the rebuilt cut (as-of 2026-11-16): REVIEW, no LEAK, five lines, every one answered here; container
metadata clean; the earlier reads stay in the report under `## Solver's-eye read`.

- `npap_return_definitions_2026.docx` (15 of 20 words of the call) and `warehouse_export_notes.md` (14 of 20): the ten
  KPI names, which the definitions list in 3.3 and the notes map to warehouse columns, none marked or ranked; harmless.
- `npap_return_definitions_2026.docx` (appointment, waiting, check-ins, requests, accounts): KPI names and the account
  rules in 2.2 and 2.3; nothing on movement, segments, phones or comparisons; harmless.
- `npap_std07_kpi_series_continuity.pdf` (cannot, movement, switch, switched, season, reference): 3.2's definition of B
  ("B cannot be observed", seasonal movement belongs in it) and the defined terms of section 2; it names no comparison
  group, segment, device or estimator, and the new 5.2 speaks only of restating a flagged series' quarter. Kept, because
  it is the estimand definition that makes the segment pool a different quantity.
- `warehouse_export_notes.md` (segment, appointment, waiting, check-ins, requests, frequent): the KPI-to-column map and the
  CRM file's own bands; the new `last_sign_in_os` line describes a register column and says nothing about 7.0, adoption,
  season or comparison; harmless.

Reader round 4 (Sonnet, isolated) is staged on this cut; the prompt and the register changed, so it reads before the
solver round. Its answers go under `## Solver's-eye read` in leak_check_report.md.

### Realism debts

- The winter movement among occasional patients is large (+38 to +43 per cent on appointment, results and notification
  traffic per active week by weeks 42 to 46 on phones that take 7.0): forced because adoption is only moderately skewed
  (settled weeks 44 per cent frequent against the pool's 29) and the segment rung has to clear the 3 per cent line with
  room. Mitigation: the frequent segment's slight fall (elective activity curtailed in winter) carries part of the gap.
- 12.9 per cent of the cohort's phones are below 7.0's minimum (iOS 16, Android 10), and their old-tracking traffic
  climbs 10 to 21 points faster than other patients' of the same segment on appointments, change requests, results and
  notifications (-1 to +9 points on the other series): forced because the segment rung has to land two series on each side
  of the 3 per cent line with room while the phones that cannot switch are at most half of any segment's pool.
  Mitigation: phones too old for a 2026 build sit with older patients, and the winter respiratory season brings older
  patients more clinic contact; their reference-period levels match everyone else's within 1.7 per cent, so the
  difference is the season's, not the phone's.
- Phones below the minimum stay on 6.8 until 1 December, when 6.8 is refused at sign-in; they never take Dunnock inside
  the window, which is what makes the phone class exact.

### Stopping rule

A solver round that lands the call sends the build back to the ladder with a hardening brief; after the third loop, a
re-root. Rounds 1 and 2 landed it, and loop 2 found no rung on paper, so architecture 1 is spent and task230 re-roots
(architecture 2 of 3) without a third loop.

### Two-layer check

1. Domain: settled change of app KPIs across an analytics SDK swap that phones below the build's minimum OS cannot take,
   product analytics measurement science; the swap test breaks it (no app update met at sign-in, no minimum OS, no
   tracking SDK).
2. Inputs: one warehouse table holding seven kinds of account, a merge register with chains, a two-sheet service
   register, two trackers' rows in handover weeks, a standard that restates flagged series; none is a defect.
3. Flip: the comparison pool for the counterfactual trend, a methodological choice; no field reading or rule flips the
   call (the standard defines B and names no estimator, no segment and no device).
4. Analyst test: the segment-conditioned staggered difference-in-differences, with its never-switched and group-rate
   checks agreeing, files five flags, two wrong and two missing.
5. Estimand: NPAP-STD-07 3.1 and 3.2 define population, outcome, window, unit and comparison; every rival pool (the
   whole 6.8 pool, the segment pool, pools matched on volume, activity, sign-in weeks or platform) is ruled out by the
   data's own structure (the data's own case, 1 to 7), and every handling of the unsegmented W40 patients converges.
6. No decoy memo, staff draft or briefing.
7. No method recovered from certified figures (the Q3 return cannot be reproduced and is not used).
8. The lesson (a not-yet-treated pool inside a stratum fills with units that can never be treated, so hold the comparison
   to units able to take the treatment) is not taught by an earlier task: task68 matches identities, task124 transports
   an effect, task129 decomposes a mix, task229's paused design weighted observed locations by their chance of being
   observed (selection into observation, where this is selection into treatment timing).

### WARN answered

repeat.deliverables: the workbook is the programme's pre-notification template and the cover note goes in front of a
board paper, so xlsx and pdf are what this organisation sends; the format pair is common (five builds) and PDF is rare in
the recent window.

repeat.decision: task229's set was the firmware builds a read-health alert fires on, cut by a test whose error is built
over comms nodes; this set is the KPI series a tracking swap breaks, cut by a difference-in-differences estimate held
within segment and to phones able to switch, against a filed three-per-cent line.

Loop 1 re-key (driver, driver_concrete, stump, analyst_test, domain_test, layer2_pattern, lineage, differentiation), with
the live task228 (architecture 2) and task229 cards copied in for the run and restored afterwards: `guard.py check` and
`register` WARN, `heart` WARN. The slot's own loop-0 lineage collides on gap, pattern, decision and Gate G and on its
driver (0.50), cleared by the differentiation line {task230}: the decisive step moved from conditioning on the segment to
holding the pool inside it to phones able to switch. The nearest other driver or stump on file is task119's stump at
0.06, task129 at 0.05.

repeat.gate_g (new at loop 1): task228's architecture 2 also carries method_or_model_selection, but on an estimator that
separates a sensor's error from two comparators sharing an input; this build's selection is the comparison pool for a
staggered switch, held to units able to take it.

`guard.py surface` promotes the same two pairs as at loop 0 (task229 back to back on gap and decision type, task68 on the
same-driver signature), both adjudicated Track B clean at the loop-0 pre-flight; the driver changed at this loop, so the
adjudicated clone-check pre-flight is owed on this cut.

### Hardening loop 2, on paper

Round 2 landed the call on its steps 6 and 7: each switched patient's reference level carried by the movement of patients
still on Tallyfield in the same CRM segment, with phones below 7.0's minimum left out of that pool ("the old-OS group was
excluded because its use rose faster from W41"), and the result unchanged under site, OS and exact CRM sign-in week strata
and a never-switched pool. Across the two rounds the solver held the comparison pool to every attribute it could see and
test (the segment, then eligibility to switch), so a further pool attribute is the same insight again and is not drawn.
Three other directions were worked against the estimand (STD-07 2.4 to 3.4) and the shipped world.

**The candidate rung, the strongest of the three: 7.0 as a bundle.** The 7.0.0 rows of the release history already list a
new home screen beside the tracker swap, and this world gives it no effect on use. The rung would give it one (the next
appointment and the latest result on the first screen move appointment, result and letter traffic), and 3.2 puts that
movement in B.
- Stump sentence: a competent solver maps handover weeks and carries each switched patient's reference level by the
  movement of patients still on 6.8 in the same segment whose phones can take 7.0, confirmed by a never-switched pool,
  site, OS and CRM-week strata and a placebo on switchers' own pre-switch weeks; the step that lands it wrong is reading
  the whole difference between patients on 7.0 and on 6.8 as recording, so it flags series the screen moved and clears
  series whose recording change the screen offset.
- Why round 2's steps 6 and 7 complete and still land wrong: every check it ran compares patients on 6.8 with patients on
  6.8 (pool against pool, stratum against stratum, switchers' pre-switch weeks against the pool), and no 6.8 pool, however
  matched, can show a movement that exists only on 7.0; the placebo passes because the screen does not exist before the
  switch.
- Data-native sentence: the tracker change arrives inside a major release that patients meet as a new home screen, so the
  switch moves both what patients do and what the tracker counts, and the standard asks for the second alone. Analyst
  test: passes in form (a strong analyst who cleans perfectly and reads every clause still files R5 by reading the
  release's whole effect as recording).
- Rigorous variants: none inside the pack. The screen and the tracker reach the same patients in the same weeks, so no
  comparison among patients separates them. The only separating evidence is a record of the same actions that the client
  does not make (the API gateway's requests, or the hospital systems' own transaction and audit records), and with it
  every rigorous variant collapses to one within-patient ratio of tracked events to recorded actions, new tracking against
  old, with no comparison pool at all.
- What pins it without naming a method: 3.2 already does ("in the way patients use the app" belongs in B); what is missing
  is an estimator, not a pin.
- Dead three ways. Without the record, B is not identified: the screen's share is an assumption and rigorous solvers split
  (Gates C and D; no C1 to C4 closure exists, since a C3 corridor means the screen moves nothing). With it, a solver that
  reconciles to a system of record by habit (round 2 reconciled weekly actives to the Q3 return) computes the ratio as its
  first cross-check, the ratio steps at every handover (an arithmetic symptom, survival property 3), the record is a file
  that exists to settle the answer (leak question 3), and R2 to R5 become decoration. And a screen effect built so that a
  new record can overturn R5 is a rung made to trip this solver's path.

**The sign-in trigger.** The update prompt is shown at a sign-in on 6.x, so a patient meets it more often in a busy week.
If use came in spells (a hospital contact driving two or three weeks of results, letters and check-ins), switchers would
enter their settled weeks inside a spell while the 6.8 pool in a given week leans toward spell starts, because anyone
active earlier was prompted and most accepted. Dead: as built, activity has no week-to-week persistence beyond the segment
and the prompt is accepted per active week (sim.py), so the spells would be added for the purpose; every repair holds the
pool to the same post-release activity history (decliners prompted in the same week, a match on lagged sign-ins, an
event-time alignment), which is one more pool attribute and the solver's own reflex (round 2 stratified on exact CRM
sign-in weeks); spells large enough to move a flag make those repairs disagree (each carries its own decay), and spells
small enough for them to agree move nothing; and selection on a transient high sits beside the regression-to-the-mean
family task228's architecture 3 is drawing.

**What the estimand asks over its window and population.** 2.5 to 2.7, 3.1 and 3.3 fix the population (switched
patients), the window (settled weeks to W46), the unit (events per weekly active patient) and the aggregation (all of them
taken together), and round 2's construction delivers each exactly; the only estimated element is B's movement, which is
the two directions above. The forward reading (from 1 December the Q4 series covers the whole base, whose phone, segment
and update-path mix differs from the early switchers') is the transport insight already rejected (task124 BLOCK; task43,
task83, task129), and 2.6 and 4.1 pin the switched patients anyway. A 7.0 change to the sign-in flow that moves weekly
actives is the bundle again, on the denominator: its size rests on whether the added sign-ins carry actions, which nothing
in the pack observes.

**Decision: SPENT.** No rung deepens the analysis away from the comparison pool, plants nothing and is forced to one flag
set by agreeing rigorous variants. Architecture 1 is spent at hardening loop 2 of 3, and task230 re-roots in Data Quality
Monitoring & Alerting (pipeline.json `lineage` and `reroot`). A re-root that keeps this world inherits one open question:
the 7.0.0 notes' new home screen against 3.2's "in the way patients use the app", which the new estimand has to leave
inert or close.

## Tried and rejected

- Physical & Environmental Sciences sensor calibration, an errors-in-variables gain for low-cost PM2.5 sensors against noisy BAM references (draft, never registered): task228's architecture 2 took physical-environmental-sciences x Data Quality Monitoring and the comparator-error family (triple collocation), and task251 is a later seed on errors in both instruments.
- Transporting the switch's effect from the early updaters to the whole base through an effect modifier (operating-system age) whose mix differs (draft, never registered): guard BLOCK test.same_driver (population, E, forecasting) against task124, and the transport insight is already spent in task43, task83 and task129.
- The seed as written, a within-segment decomposition under an incident policy that defines a loss as a within-segment fall: the decisive step would be rule application, and decomposing by client version is the opponent's reflex.
- An equivalence reading of a canary's confidence interval: with the evidence standard filed it is rule application, and the easy wrong route (event-level errors) is the clustered-error family task229 owns.
- A size-biased audit sample (sessions pulled through randomly sampled events): honestly keyed pattern D, banned against task229.
- Forward loss of open tracking incidents under version adoption (pattern A): reads as Opportunity Sizing, and the projection method is a fork unless a filed fact pins it, which turns the decisive step into a reading.
- Settled change reported to one decimal: five rigorous estimators of the same B spread up to 0.33 points on the shipped rows, so one-decimal cells would split rigorous solvers; reported to the nearest whole per cent, every variant sits 0.12 or more inside its bin.
- A season starting in week 38: a pooled pre-trend check over weeks 33 to 40 would have shown the pool rising 2 to 4 per cent faster, handing the decisive evidence to the most routine diagnostic; the season now starts in week 40.
- Effects on three seasonal streams only: the pooled route then matched the answer to the whole per cent on the seven other streams, so a response on R3 kept most of the grid; every stream now carries some winter movement and R3 misses all ten cells.
- No phones blocked from 7.0: the never-switched frequent pool was too thin and the never-switched variant drifted up to 0.8 points from the golden on low-volume streams.
- A raw session-service export for the weekly active patients ask, with UTC timestamps across the 25 October clock change: about a million rows and 12 to 19 MB on its own; the person and service-account devices on the warehouse table carry the ask without it.
- Weekly active patients asked by engagement segment: it would point every solver at the segment file, which is the decisive conditioning variable.
- Larkspur as the in-house tracking product's name: task84 (Larkspur Labs) and task31 (a supplier) already use it, an Idiom finding at the clone pre-flight; renamed Dunnock after a whole-word search of every card, task folder, target.zip and the clone cache returned nothing.
- A what-pin in NPAP-STD-07 3.2 naming whose movement carries B (patients of the same engagement): a method sentence that hands the solver the decisive step; the data rule the whole 6.8 pool and R3b out instead (the fork closure under the estimand).
- A filed CRM convention for patients first signed in during W40 (leak read 2's fork): not needed, since every handling of them returns the same flags and cells within 0.12 points; a convention would only add a line about the segment file's role.
- Architecture 1 loop 0, the counterfactual trend held within CRM engagement segment as the answer (now R4): solver round 1 landed the call on its step 6, verbatim "Baseline = each patient's events per active week in W33-40; trend index by crm_engagement_segments_20261001.csv segment and week from patients still on Tallyfield (occasional index rises to about 1.6 by W46, frequent stays about 0.98)", and its step 8 found a never-switched control and a group-rate index within 0.5 points with no flag changing. It died because, once the pooled route is refuted, the segment pool is the refinement a strong solver reaches unprompted, and nothing in the loop-0 world made the patients still on 6.8 inside a segment differ from the ones who switched; the segment is now a lower rung and the decisive step sits inside it (patients whose phones cannot take 7.0).
- Auto-update at 40 per cent with the older-handset extra at 0.012 a week: the eligible not-yet-switched pool thinned, the never-switched rigorous variant drifted 0.52 points, and the segment trend's siblings split on notification opens (-2.84 against -3.27 never-switched), so round 1's own robustness check would have disagreed and pointed at the pool; kept 25 per cent and 0.018.
- Older handsets at 14 per cent with the extra at 0.015 a week on the season's own scale: the segment trend put appointment change requests at -2.91, on the line, with its never-switched sibling at -3.44; at 13 per cent and 0.018 on the season's scale the never-switched rigorous variant put change requests 1.37 points from the line. The extra's scale on change requests is 1.4 (winter illness reschedules appointments), which keeps every sibling on one side and the answer's own variants 1.7 points or more inside.
- Notification opens' target at -0.34: the group-rate variant sat 0.07 from a whole-per-cent edge and the W40 newcomers read as frequent crossed it; at -0.15 every defensible variant clears its edge by 0.13 or more. The Poisson variant then needed appointment change requests at -1.14, messages at -0.21, check-ins at -9.12 and forms at -0.17 to share every whole per cent.
- Q4-to-date values centred either side of their two-decimal centre at random: pre-assessment forms moved under one device mishandling only; every value now sits 0.0010 to 0.0017 under its centre, where the denominator devices push.
- The weekly block cut by phone class, or a count of patients whose phones cannot take 7.0: it would name the population the decisive step turns on, so the weekly block stays device-carried and its weight is counted as leakage in Part 0.
- Architecture 1 loop 1, the segment trend held to phones that can take 7.0 as the answer (R5): solver round 2 landed the call on its steps 6 and 7, verbatim "Control = active patients on all-Tallyfield in week w whose OS supports 7.0 (Android 10+ / iOS 16+); the old-OS group was excluded because its use rose faster from W41", unchanged under site, OS and exact CRM-week strata and a never-switched control. It died because the solver holds the comparison pool to every attribute it can see and test (the segment in round 1, eligibility to switch in round 2), so a pool-composition rung falls to the same reflex that finds the segment.
- Hardening loop 2 on paper, 7.0 as a bundle (the 7.0.0 notes' new home screen given a use effect, which 3.2 puts in B, so every 6.8 pool reads the release's whole effect as recording): without a record of the same actions that the client does not make, B is not identified and rigorous solvers split; with one (API gateway requests, the hospital systems' transaction records), the within-patient ratio of tracked to recorded actions is the answer, a reconciling solver computes it first, and R2 to R5 are decoration.
- Hardening loop 2 on paper, the sign-in trigger (busy weeks meet the 6.x update prompt more often, so with spells of use switchers enter settled weeks mid-spell while the 6.8 pool leans to spell starts): activity as built has no week-to-week persistence, so the spells would be added for the purpose; every repair holds the pool to the same post-release activity history (one more pool attribute, the solver's reflex); spells big enough to move a flag split the repairs; and it sits beside task228's regression-to-the-mean draw.
- Hardening loop 2 on paper, what the estimand asks over its window and population: 2.5 to 2.7, 3.1 and 3.3 pin population, window, unit and aggregation and round 2 delivers them exactly; the forward reading (the whole base from 1 December) is the rejected transport insight, and a 7.0 sign-in change that moves weekly actives is the bundle on the denominator, sized by nothing the pack observes. Architecture 1 is spent at loop 2 of 3.
- Architecture 2 draw, a vigilance clock (detection decaying with continuous time on one task and resetting at a task switch, so a routing change that removes switching moves the forward residual): the domain-clock family is spent across six (time, A, forecasting) builds and task46's service-exposure clock is the same driver; replaced by the pool's error rate, a condition of the shared work rather than a clock.
- Architecture 2 draw, G16-keyed candidates: task228's architecture 2 holds G16 as its decisive key inside the three-draw window (ban.pattern), so no G16 draw was taken.
- Architecture 2 draw, laboratory QC rule selection by sigma metric: the rule choice is a filed procedure (rule application), and false rejections over repeated QC runs sit in the repeated-looks family (task228 architecture 1).
- Architecture 2 draw, reagent on-board stability (a calibration drifting with days since opening): a time-since-event clock, the same spent family as the vigilance clock.
- Architecture 2 draw, selective editing in a statistical office (score functions choosing records for manual review): the score function is a filed method (rule application), and its anticipated-value pitfall is regression to the mean (spent with task130 v3).
- Architecture 2 draw, risk-limiting audits: sample size and stopping are filed statistics, and the pitfall is sequential looks (task228 architecture 1; seeds task248 and task250).
- Architecture 2 draw, monetary unit sampling: selection proportional to size is the size-biased sample already rejected under architecture 1 (pattern D, held by task229), and its evaluation is a filed formula.
- Architecture 2 draw, item parameter drift in a testing programme: flagging drifted anchor items rests on comparator independence (task228 architecture 2, seed task251).
- Architecture 2 draw, age heaping in a census return: the decisive step reads a digit-preference index and applies a filed smoothing (data semantics and rule application).
- Architecture 2 draw, the Drumlee patient-app world kept and recast for a monitoring call: its organisation family (hospital_or_health_provider) repeats task181 inside the three-draw window (guard BLOCK ban.org_family) and Sandra blocked on people.first; a new world in human factors instead.
- Architecture 2 draw, a capture centre in Cebu: Faker's Philippine locales return US-style names, so the personas would not fit the geography; Kolkata with the India locale instead.
- Architecture 2 paper, the first pool numbers (night 3.9 to 4.4 per cent, day 3.2 to 1.8): the night side moved detection too little for the pharmacy stream's flip to clear the rigorous variants (about 7 per cent of margin) and left the motor claims near their line on nights; the night pool now starts at 2.5 per cent and the motor claims raise it to 5.0.
- Architecture 2 paper, an answer keeping the three US handwritten streams on second pass: it shared three designations with the textbook set, so a wrong-path response kept most of the per-stream credit; the limits now put the night streams over in the third quarter and under in November, Brightmoor excepted.
- Architecture 2 paper, the tenure confound as a rung (new hires on the low-rate night pool inflating the tenure term): with a shift term in the model the confound is absorbed and the roster moves no designation; tenure stays a supporting term (G17), and the roster only widens the textbook route's distance from the answer.
- Architecture 2 paper, a full-volume Hollings & Pryce pilot or a motor surge week in the closed quarter: either is a dated event whose step in the day queue's misses an event study finds (survival property 6); the pilot runs at low volume and the identifying variation stays diffuse.
- Architecture 2 paper, each stream's November forecast asked as a graded figure (per 1,000 key fields, one decimal): an inheriting ask that hands the response on the call eleven criteria and spreads across rigorous variants near bin edges; the call is asked as one set and no forecast is graded.
- Architecture 2 paper, the forecast method left unfiled (any model the analyst prefers): two defensible methods would survive the literal-reader test (determinism-check section 1); QCP-04 4.3 files the shift-by-shift leave-one-out criterion and never the method.
- Architecture 2 paper, a slide charting each stream's November forecast against its limit with the second-pass streams marked: a visual built on the decision quantity, which the cracker banks (supplemental-stumping 1.4); the slide charts the asks' own quantities instead.
- Architecture 2 paper, weekly calibration sessions marked by a calibration register as ask A's primary: the register isolates the device rows in one join (a marker, supplemental-stumping 1.2 ban 2); replaced by session minutes repeated on every document line, with handover-split sessions as the over-cleaning half.
- Architecture 2 paper, the accepted forecast revision named in a column of the plan: a marker that hands ask B's primary over; the plan carries key fields only, so the revision of record shows only through each form version's key fields per claim.
- Architecture 2 paper, the service quality council and QCP-04 named in the prompt: a meeting and a standard by acronym, both outside the prompt rules; the prompt asks the question and names the files, and the council and the procedure live in the pack.
- Architecture 2 paper, QCP-04 4.3 as a filed selection criterion (the detection model that, fitted with each closed-quarter shift left out, comes closest to that shift's audited misses), written to PR #43's rule that an open method stands only behind one: dropped at the PR #44 pass for form 1, because the design forces the method (within each queue the misses move with the shift-day pool's error rate, the night and Saturday terms are its gaps, and the plan moves it inside the closed shift-days' range), because the criterion was the decisive rung's main exposure (it sent every solver to the shift grain, where the pool's rate shows), and because task446, newest on main, files a leave-one-out back-test of its own; the earlier line rejecting an unfiled method read the rule before PR #44, and 4.3 now files the records and one method for every stream, never a selection.
- Architecture 2 draw, the head of quality as requester (`compliance_or_audit`) working from an operations log (`operations_log`): task229's design 2, registered first and sorting before task230, holds both (guard BLOCK `ban.role` and `ban.artifact`); redrawn to the centre's head of operations (`operations_director`), who runs both first-pass queues and signs the same plan, working from the November operating plan (`capacity_report`).
- Architecture 2 build, the Hollings & Pryce limit at one decimal: the golden-to-pilot multiplier is about 1.4 (the pilot's Saturdays already carry low-rate days) and a 0.1 step at a limit near 0.8 is 12 per cent, so no one-decimal limit kept R0 under 0.90 and every rigorous variant over 1.10; the newest contract states its limit to two decimals.
- Architecture 2 build, a leave-one-month-out back-test as the default path's clean check: the group rota moves each verifier between queues month to month, so the attribute models miss single stream-months by up to four binomial standard errors; the in-sample month-by-month check in overdispersed standard errors is what an analyst runs and it is clean.
- Architecture 2 build, three delivery batches a shift-day with even volumes and untuned client findings: one boundary batch held so few sampled claims that most streams moved by under 0.01 per 1,000 under the UTC reading; the end-of-shift sweep carries 58 per cent of a day and the generator places boundary findings until each stream moves by more than its decimal.
- Architecture 2 build, a 10 per cent night audit share and a 60 per cent pilot audit: the night slope came out at 0.38 to 0.42 (the noisy measured rate attenuates it) and the typed family rested on about 17 misses, so the within-queue and Hollings & Pryce margins failed; 30 per cent at night and the full pilot re-key instead.
