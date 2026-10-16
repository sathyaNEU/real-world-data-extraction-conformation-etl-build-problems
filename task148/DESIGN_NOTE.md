# task148: Tavish County's FY2028 late-shift 911 staffing (architecture 2)

Private, never ships. Wave 4, numbered from seed FC19. Architecture 1 (Fenmore Savings Bank's CECL allowance on its
relief-era SBA 7(a) pool, priced on guarantor groups) was spent at stage 4; its identity is in the card's lineage, the
ledger's dead-architecture row and `## Tried and rejected`, and its files left the folder (they stay in history at
435395d). Architecture 2 leaves the seed's lending world behind: a county 911 center's forecast of its late shift's
answer-time compliance in fiscal 2028.

## Re-root

**Why architecture 1 is spent.** The determinism judge returned NOT_DETERMINISTIC and SEND_BACK
(underspecified_objective): implementing the write-up's own method (standing-alone failure rates by six-month band,
the group's first failure, the 91.8 per cent charge-off share) independently filed $11.7 million against the golden
$10 million, split 2.33, 3.59 and 5.77 against 2.0, 3.0 and 5.0; the micro-conventions of a hazard model by months on
book (age base, band edges, in-month ordering, what makes a loan alone, loans beside a defaulted sibling) moved the
booked million. Both asks were underdetermined: the Section 1112 detail's multi-instalment lines had no findable
allocation rule, and "net" charge-offs was undefined with 38 ledger rows carrying no master note number. The rule 3
audit read AT_RISK: executing the loan authorization's cross-default clause on the joined register gave most of the
move, leaving the member hazard's double count, at 1.19, as the only analytical margin; and the shell (domain, task
type, decision, role family, register artifact, the default path's wording, a servicing conversion) read as task133's.

**What architecture 2 has to do, and how this draw answers it.**
- A different subdomain, task type and spine: Urban & Regional Science, `municipal-service-demand-resource-allocation`,
  spine an ACD call-detail export (one row per 911 call), nothing of lending, allowances, loans or months on book.
- Rule 3 strict on the main call: no filed clause or procedure produces the move. The agency's call-answering standard
  files what is measured (calls answered within 15 seconds of reaching the PSAP, calls abandoned within 5 seconds left
  out) and the arrival basis (the regional board's forecast); nothing filed says how a queue behaves. The decisive step
  is an estimate the data force against the field's default (Erlang C): the callers' patience, estimated over every
  call's wait with the answered calls censored, inside a queueing model with reneging (Erlang A). Out of sample
  (parameters from January to June 2025, fiscal 2026 predicted across the agency's hours) Erlang C under-predicts the
  observed compliance by 1.5 points (93.7 against 95.2, below it in all twelve months) and predicts no hang-ups where
  1.7 per cent of calls hung up, and the patience read off the hang-ups' own waits over-predicts compliance by 1.1
  points (96.4, above it in all twelve months) and hang-ups by more than half again (2.8 per cent); the censored
  estimate lands within 0.1 (95.3, hang-ups 1.7 per cent).
- Determinism from the start: the golden is a closed-form stationary queue per forecast hour on two parameters measured
  on 417,086 calls; the arrivals are the board's filed forecast; every defensible construction (the analytic
  queue, a simulation of each night from cold or warm, patience by the exponential likelihood or a Kaplan-Meier fit
  over any window, busy time over any window, the shift's average rate for its hours) is asserted to round the same,
  mid-bin, and to survive one sigma; the asks' bases are closed by cited sentences or asserted data facts.
- Strength: Erlang C is the PSAP staffing default and the hang-ups' own waits are the natural patience; each files a
  different set of months and different shares. Only both moves together land.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task148.json`, architecture v2, registered 2026-10-16; `guard.py check` WARN only (repeat.gate_g, repeat.decision, repeat.question_form, answered below); the older same-driver signature (gap time, G16, method_or_model_selection) against task254 v2 and task501 v2 differentiated on the card, with lines against task133, task130, task146, task142 and task149 |
| Domain / task type | `urban-regional-science` (client domain), task type `municipal-service-demand-resource-allocation` (serves Forecasting): a county 911 center's demand and the call-takers it staffs against a response standard; the library's own line for the task type is "response standards are percentiles, not means", and the 15-second standard is one |
| Objective | Forecasting & Predictive Modeling: each month's late-shift answer-time compliance in fiscal 2028 (July 2027 to June 2028), a window not yet open, predicted from the agency's own call history and the board's arrival forecast |
| Shape | `02` forecast across periods: the twelve months of fiscal 2028, each an expected compliance, and the months that fall below 90 per cent (12 + 1 criteria), with the asks supplying the rest (counted in `## Ask sheet`) |
| Decision | `designation_set`: the months for which the FY2028 budget funds a seasonal fifth call-taker on the Friday and Saturday late shift |
| Mechanism | gap time (decisive: a caller's patience is a time to an event that the answer censors) and population (the callers still waiting are the ones who did not give up); pattern none; generators G16 (method selection: a queue with reneging against the standard queue) and G12 (an answered call records no patience, only a lower bound); Gate G `method_or_model_selection`; strategy `other` (a queueing model with reneging calibrated on censored waits) |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:queue-with-reneging-censored-patience`, with `estimation_fit` (censoring) in the second move |
| Furniture | forum `board_of_directors` (the agency's board adopts the FY2028 budget), forcing event `budget_or_appropriation`, organisation family `local_government`, role family `field_unit_lead` (the operations manager runs the communications floor), context artifact `published_series` (the regional 911 board's hourly volume forecast), calibration `none`, opening `question-first`, question form `which` |
| Spine | the agency's ACD call-detail export, one row per 911 call presented to the ACD queue (presented, answered or abandoned, released, ready), January 2025 to September 2026: the legacy CSV to the 13 May 2025 NG911 cutover, then the i3 JSON Lines log, about 420,000 calls, constructed |
| Deliverables | `late_shift_staffing_fy2028.xlsx` (a summary sheet with the months below 90 per cent and the case for them, each month's expected compliance, the two ask tables) and `late_shift_compliance_fy2028.png` (each month's expected compliance against the 90 per cent line, the three months marked); the format set rotates away from task146 (docx), task147 (pdf) and task149 (pptx) |
| People | drawn with `guard.py names --geo "United States" --seed 148 --n 40`, skipping architecture 1's five and first names already on file: Leon Carpenter (operations manager, brings the request), Regina Holder (quality assurance and data analyst, the ACD exports), William Braun (the regional 911 board's planner, the volume forecast), Carol Bender (finance director), Gary Dennis (training and callback supervisor); none in the prompt |

**Guard.** Re-run at stage 2 after task147 and task149 shipped: WARN `repeat.gate_g` (method_or_model_selection
against task149) and `overuse.gate_g` (5 of the last 12): task149 picks a hazard model's base by a filed walk-forward
test; here the selection is of the queueing model, forced by the data's structure (hang-ups, waits the answer
censors) with no filed criterion, and its validation is the analyst's own out-of-sample check, so the class is honest
and the mechanism different. WARN `repeat.question_form` (which, task147; at the draw, task462): the decision is a
designation of months, so the question asks which. WARN `repeat.deliverables` (pdf and xlsx, task147): answered by
moving to a workbook and a chart image. The older same-driver signature (gap time, G16, method_or_model_selection)
matches task254 v2 (a time-to-event cut under a lock date's truncation) and task501 v2 (a walk-forward pick of a pacing
base); neither has a queue or reneging, and the card carries both lines. Nearest drivers 0.08 (task500 v1 lineage) and
under. At the draw the WARNs were `repeat.gate_g` (task461, task462), `repeat.decision` (designation_set, task462) and
`repeat.question_form` (task462): ETL builds choosing a conformance or linkage method and designating emission
sources, neither a forecast or a queue.

**Abstraction test.** Stripped of nouns, the driver: units waiting for a service leave when the wait outlasts their own
patience, so the queue each new unit meets is drained by those who give up; a model in which every unit waits until
served overstates every wait, and the patience that sets the drain is seen in full only for the units that left, the
served ones showing only a lower bound, so it has to be estimated over every unit's wait, not from the leavers' waits,
which make units look far less patient and the service better than it will be. The nearest by mechanism: task254 v2
(truncated event times: here the censoring is by service, inside a queue), task142 (a percentile built from arrivals
and durations: here there is a wait, a standard and units that give up), task147 (requests needing every unit of a run:
here no request spans several units), task149 (a rate rising with pace: here no rate is forecast). None shares the
latent structure.

**Same-puzzle test.** Against the last twelve builds and their lineage: task145 shares the time gap and G16 but
allocates a total by a back-tested forecast method (decision `allocation_to_total`, Gate G `forecasting`, strategy
`forecast_method_backtest`); task149 shares the time gap and Gate G `method_or_model_selection` but its generator is
G14, its decision a single figure and its strategy a filed back-test. No build in the window pairs the time gap, G16
and a designation, and nothing here files a back-test: the history's out-of-sample fit is the analyst's own check, not
a criterion in any shipped document. The older same-driver signature (task254 v2, task501 v2) carries the card's
differentiation lines.

**Data-native sentence.** Tavish County's ACD log times every 911 call from the moment it reaches the PSAP to its answer
or hang-up and marks which it was; a caller who is answered leaves only the time they had held on so far, and the
agency's callers would hold on about 160 seconds on average, so the few who hang up drain the queue for those who
stay and the compliance a standard queue gives is too low, while the patience read off the hang-ups alone (46
seconds) is far too short.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (61 builds): no queue with reneging and
no censored patience; the waiting-adjacent builds (task142's arrivals and durations, task147's consecutive runs,
task119 and task127 on bed waits) carry other structures. `layer2-rigor-patterns.md`: municipal-service line 3
(response standards are percentiles) is the frame; patient-flow line 1 (size by blocking or queueing, not mean census)
the nearest method line, in another domain. `two-layer-task-design.md`: "the data's real structure such as censoring"
and "a forecast validated out of sample" are the client's families for the two moves. task133's, task130's and
task146's cards for the differentiation the re-root asks for. The seed FC19 is not used beyond its number.

**World.** Tavish County (fictional) runs one consolidated 911 center, the Tavish County Emergency Communications
Agency, the primary PSAP for the county and its member cities; fire, EMS and sheriff dispatch sit behind it. The agency
moved from legacy CAMA trunks and ALI to NG911 (i3 over the regional ESInet) on 13 May 2025, wireline calls staying on
the legacy trunks to 16 May. Its board adopts the fiscal-year budget (1 July to 30 June) in May. Since July 2024 a
state 911 surcharge grant has paid a fifth call-taker on the Friday and Saturday late shift (22:00 to 02:00); the grant
ends on 30 June 2027 and the FY2028 budget funds four, and asks in which months a seasonal fifth is needed. Halvorsen
Township, on the Wexley County line, has had its 911 service from Wexley County Emergency Communications; its
agreement ends on 30 June 2027 and from 1 July its calls come to Tavish County, with location-based routing sending its
wireless calls straight to the agency. Today a Halvorsen wireless call that reaches Tavish County through a Tavish cell
sector is answered and transferred to Wexley. The Tri-County Regional 911 Board publishes the hourly volume
forecast the region's PSAPs staff to; its FY2028 edition carries the Halvorsen move. The agency's standard is the
national one: 90 per cent of 911 calls answered within 15 seconds of presentation, calls abandoned within 5 seconds
counted as misdials. Positions are on auto-answer, so a call delivered to a ready position is answered at once. Abandoned
calls are dialled back from a callback desk staffed around the clock, not by the call-takers on the floor.

## Default path

1. Take the board's FY2028 forecast for the agency's Friday and Saturday late-shift hours (Friday and Saturday 22:00
   and 23:00, Saturday and Sunday 00:00 and 01:00) in each month.
2. Measure the busy time per answered call from the ACD log (answer to ready, about 3 minutes 47 seconds), across the
   legacy and i3 layouts.
3. Run Erlang C, the standard PSAP staffing model, for each forecast hour with four call-takers: the share answered
   within 15 seconds; weight the hours by their forecast calls into each month's compliance.
4. Mark the months below 90 per cent and fund the fifth call-taker for them.

Ends on: five months below 90 per cent, May to September (July 2027 84 per cent), a fifth call-taker from May to September.

Golden: July 2027, August 2027 and June 2028 below 90 per cent (88, 89 and 89 per cent; September 2027 and May 2028 91, the other months 93 to 95), a fifth call-taker for those three months.

## Stump sentence

Running the standard Erlang C staffing model on the board's FY2028 late-shift forecast with the measured busy time and
four call-takers puts five months, May to September, below the 90 per cent standard (July 2027 84 per cent) and asks
for a fifth call-taker from May to September; the step that lands it there is treating every caller as waiting until
answered, when Tavish County's callers would hold on about 160 seconds on average and those who hang up shorten the
wait for those who stay, so only June, July and August fall short (July 88 per cent), and the patience must be
measured over every call's wait, not from the hang-ups' own waits (46 seconds), which leave no month short.

## Three rules

Written at the draw, brought to the design's figures at stage 2 and set on the built pack at stage 3.

- **Task type:** urban-regional-science, municipal-service-demand-resource-allocation (serves Forecasting): the county
  911 center's demand and the call-takers it staffs against the 15-second answer standard, forecast for each month of
  fiscal 2028 from its own call history and the regional board's arrival forecast.
- **Domain test:** the deciding quantity is each month's late-shift answer-time compliance under the call-answering
  standard with the funded call-takers, which a PSAP staffing analysis computes from a queueing model of its own calls;
  because 911 callers hang up, the model is Erlang A calibrated on the agency's ACD log, with the callers' patience
  estimated over every call's wait, censored where the call was answered.
- **Swap:** "how many hospital beds" keeps arrivals and stays, but a 15-second answer standard, a call-taker's busy time
  that runs to the CAD entry, 911 callers who hang up while they wait, misdials under 5 seconds and a township whose 911
  service moves between PSAPs have no counterpart, so what sets each hour's compliance stops making sense.
- **Layer 1:** the ACD export in two layouts across the 13 May 2025 cutover (the legacy CSV in local time to the
  second, the i3 JSON Lines log in UTC with milliseconds, wireline calls on the legacy trunks to 16 May and wireless
  calls on i3 from 13 May, so both files carry those days with different calls); transferred-in calls from other PSAPs
  presented with their own arrival time; test calls answered by the i3 test responder in the same export; redials
  after hang-ups; the late shift crossing midnight and the daylight-saving nights; the floor roster dated by the evening
  a block starts; the board's forecast as a long table for the region's four PSAPs by month, day and hour beginning,
  with a FY2027 sheet beside the FY2028 one. Each is what these systems write; none carries the stump (asserted at
  stage 3).
- **Layer 2:** `allocation_constraints` with `estimation_fit` inside it: the queue drains through callers who give up,
  so the standard queue's every-caller-waits assumption is wrong for this center, and the patience that sets the drain
  is a censored duration whose naive estimate from the hang-ups alone is badly short.
- **Decisive step:** model each forecast hour as a queue with reneging (Erlang A, M/M/4+M) on the board's arrivals, the
  measured busy time (227.0 seconds) and the callers' patience estimated over every call's wait (the total time all
  calls waited over the calls that hung up, the exponential likelihood with answered calls censored, 161.4 seconds),
  and read each month's compliance under the standard's measure.
- **Not semantics:** every field (presented, answered, abandoned, released, ready, service type, the transfer fields)
  and the standard's definition are read the same way by the easy route; no field or definition says that callers'
  hang-ups shorten the others' waits or how patient a caller is; the default path reads them all and still files five
  months short.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the prompt's question, SOP
  2.10's measure and its 5-second exclusion, the busy-time and shift definitions in the SOP and the README, the SOP's
  statement that staffing is planned on the board's forecast) are executed word for word on the clean truth in
  `checks.py` (the rule 3 block, ten sentences) and give no figure of their own: they say what is counted and what the
  arrivals are, never a queue, a wait or a patience; the estimators they admit (Erlang C, the observed compliance
  carried forward, Erlang A with the hang-ups' own waits) each file a different set of months (asserted).
- **Analyst test:** a strong analyst who joins the legacy and NG911 ACD exports, reads the standard and the board's
  forecast correctly and runs Erlang C on each month's forecast late-shift hours with the measured busy time and four
  call-takers files five months below 90 per cent, May to September (July 2027 84 per cent), and a fifth call-taker
  for them; with the hang-ups modelled on the patience their own waits give (46 seconds), no month falls short (July
  91); carrying fiscal 2026's observed late-shift compliance forward (about 98.5 per cent with five call-takers), no
  month falls short either.
- **Estimand:** SOP 2.10 (the PDF) and the prompt: the answer-time compliance (calls answered within 15 seconds of
  presentation over calls presented less calls abandoned within 5 seconds of presentation) of the 911 calls presented to
  the agency in the Friday and Saturday late-shift hours (22:00 to 02:00) of each month of fiscal 2028, with the four
  call-takers the FY2028 budget funds, on the regional board's forecast arrivals (SOP 2.10 section 5); the population,
  outcome, window and unit are filed, the method is not.
- **No decoy:** no consultant's staffing study, prior-year staffing model, vendor estimate, board figure or certified
  table states or argues a compliance figure, a staffing level or a method; the board's forecast is of calls, not of
  answers.
- **No certified replay:** no certified or published compliance figure for fiscal 2028 ships and nothing graded is
  reproduced; the patience and the busy time are estimated from the raw ACD log.
- **Lesson:** in a service where the waiting give up, the wait every new arrival meets is shortened by those who left,
  so the standard queue is too pessimistic, and how patient they are can only be estimated over every unit's wait, the
  served ones censored; read off the leavers alone, patience looks far shorter and the service better than it will be;
  no build on file teaches a queue with reneging or a patience censored by service.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Figures are the built pack's (stage 3, 2026-10-16), as `checks.py` prints
them.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 Erlang C on the board's forecast with the measured busy time and four call-takers (May to September short, July 83.6) | no | no | yes (the PSAP staffing default) | no | no | no | readable |
| R1a no queue: fiscal 2026's observed late-shift compliance carried forward, or scaled by the forecast's growth (no month short, July 98.5) | no | yes (the answer times give the observed share directly) | yes | no | no | yes | readable |
| R1b the analyst's own forecast from the history with the right queue (no Halvorsen move; no month short, July 93.5) | no | no | yes (forecast from history) | no | no | no | readable |
| R1c Erlang C with the busy time scaled until it reproduces fiscal 2026 (210.1 seconds against the measured 227.0; July, August and June short, each a point below the golden's figure, 9 of 12 figures on the golden's) | no | no | yes (calibrate to history) | no | no | no | readable |
| R2 Erlang A with the hang-ups' own waits as the patience (45.6 seconds; no month short, July 90.8) | no | yes (the disposition marks the hang-ups and their wait is one subtraction) | yes (Erlang A's patience read as the mean time to abandon) | no | no | yes (a mean of one column) | readable |
| R3 (decisive) Erlang A with the patience estimated over every call's wait, the answered calls censored (161.4 seconds; July, August and June short, July 88.1) | no (SOP 2.10 files the measure and the arrival basis; nothing names a queue, a wait or a patience) | no (no column holds a patience or marks a wait as censored; an answered call's wait looks complete) | no (the reflexes are Erlang C, a calibration to history and the mean time to abandon) | no (no compliance forecast, model output or staffing study ships) | no (the battery is clean on it) | no (a likelihood over every wait inside a queue with reneging, per forecast hour) | silent |

## Semantic fork table

Every term of the main ask and every convention the main computation needs. Each row is asserted in
`generator/checks.py` under its id.

| SF | Term or convention | Golden reading | Alternatives | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | fiscal 2028 | 1 July 2027 to 30 June 2028 | calendar 2028 | other months | the prompt ("fiscal 2028, July 2027 to June 2028") and SOP 2.10 section 1 |
| SF2 | the late shift | the hours 22:00 to 02:00 of each night that starts on a Friday or a Saturday: Friday and Saturday 22:00 and 23:00, Saturday and Sunday 00:00 and 01:00, local time | the calendar Friday and Saturday 00:00 and 01:00 | lower arrivals, other months | the prompt ("Friday and Saturday late shift, 22:00 to 02:00"), the FY2028 budget's staffing table (nights starting Friday and Saturday) and SOP 2.10 5.2 (a block past midnight belongs to the day it starts) |
| SF3 | a night's month | the month the night starts, each of its hours on that month's forecast (the Friday 30 June 2028 night is June's) | each hour in its calendar month's table | same call (asserted) | SOP 2.10 6.1 (a shift's calls are reported in the month the shift starts); same call |
| SF4 | within 15 seconds | answer time less presentation time of 15 seconds or less | under 15 seconds | same call (the model is continuous; asserted) | SOP 2.10 3.3 |
| SF5 | presentation | the moment the call reaches the agency's ACD queue (the i3 queue entry, the legacy trunk seizure) | the moment it reaches a position | no difference (positions are on auto-answer; 95.1 per cent of i3 answered calls show no wait) | SOP 2.10 3.1 and 4.1; the README |
| SF6 | the measure's denominator | calls presented less calls abandoned within 5 seconds of presentation | all calls presented; calls answered only | all presented: each month 0.2 to 0.4 lower, same set and same rounding (asserted); answered only: ruled out | SOP 2.10 3.2 and 3.3, the compliance definition |
| SF7 | the arrivals | the board's FY2028 forecast for the agency, the Halvorsen move included | the analyst's own forecast from the history | no month short (R1b) | SOP 2.10 5.1 (staffing is planned against the board's published hourly forecast) |
| SF8 | the forecast's unit | average 911 calls presented per clock hour for that day and hour beginning in that month | the month's total for the cell | ruled out | the workbook's Read me sheet |
| SF9 | four call-takers | four positions taking 911 calls in every late-shift hour of every night | the supervisor or the callback desk taking overflow | ruled out | SOP 2.10 4.3 (the floor supervisor and the callback desk take no calls from the 911 queue) and the FY2028 budget's table |
| SF10 | busy time | answer to the position's return to Ready, the after-call work and CAD entry included | answer to release (talk only) | no month short (talk time 158.9 seconds) | SOP 2.10 4.2 (a position takes no new call until the call-taker sets Ready again after the after-call work and CAD entry) and the README |
| SF11 | the busy-time window | every answered 911 call in the history | the late shift's calls; fiscal 2026; January to June 2025; fiscal 2027's first quarter; one layout | same call (asserted: 226.5 to 227.2 seconds) | same call |
| SF12 | the patience window | every 911 call's wait in the history | the late shift's calls; fiscal 2026; January to June 2025; fiscal 2027's first quarter; one layout | same call (asserted: 155.1 to 165.7 seconds, one sigma included) | same call |
| SF13 | the patience estimator | the exponential likelihood, answered calls censored | Kaplan-Meier on the same waits with an exponential fitted to it; the hang-ups' rate over the total waiting time by 30-second band; the patience calibrated so the queue reproduces fiscal 2026's or January to June 2025's observed compliance, or fiscal 2026's hang-up share | same call (asserted: 161.2 and 161.4 seconds; calibrated, 165.8, 174.0 and 164.2 seconds) | same call |
| SF14 | the queue in time | each forecast hour as a stationary queue | one continuous queue for each night, from empty or from the evening block's five call-takers | same call (asserted within 0.4: largest moves 0.29 and 0.19) | same call |
| SF15 | the hours of a shift | each hour on its own forecast | the shift's average rate for all four hours | same call (asserted) | same call |
| SF16 | a month's figure | the month's calls answered within 15 seconds over its calls presented less those abandoned within 5 seconds, over all its late-shift hours | the forecast-weighted mean of the hourly figures | same call (asserted) | same call |
| SF17 | transferred-in calls | in the population and in the estimates | left out | same call (asserted) | SOP 2.10 2.2 (transferred-in calls included) |
| SF18 | test calls | out (not 911 calls; the i3 test responder answers them) | in | same call (asserted: 226.1 and 161.5 seconds) | SOP 2.10 2.2 and the README; same call |
| SF19 | redials | each call presented counts, a redial included | one per callback number | ruled out | SOP 2.10 3.3 (calls presented); same call on the estimates (1,553 calls collapsed, 161.8 seconds; asserted) |
| SF20 | the two layouts | both, legacy local times read with the zone's rules and i3 UTC converted to local | one layout | same call on the estimates (asserted) | the README |
| SF21 | the daylight-saving nights | the 6 November 2027 night runs five clock hours, 01:00 twice; the 11 March 2028 night four | four hours every night | same call (asserted) | same call |
| SF22 | falls short | the unrounded compliance below 90 per cent | the rounded figure below 90 | same call (every month at least 1.03 from 90; asserted at 0.9) | same call |
| SF23 | rounding | each month's compliance to the whole per cent, once | hourly figures rounded first | same call (asserted) | the prompt |
| SF24 | the cutover days | 13 to 16 May 2025 in both exports, each call in one of them | either export alone | same call on the estimates (asserted: 306 legacy and 1,728 i3 calls on those days, none in both) | the README's cutover note |

## Ladder

The built pack's figures (stage 3, 2026-10-16); `checks.py` prints every value.

| Rung | Construction | Months below 90 | July 2027 | Dies to |
|---|---|---|---|---|
| 0 | Erlang C, the measured busy time (227.0 s), the board's forecast, four call-takers | July to September, May and June (5) | 83.6 | out of sample (parameters from January to June 2025, fiscal 2026 predicted across the agency's hours) Erlang C files 93.7 against an observed 95.2, below it in all twelve months, and predicts no hang-ups where 1.7 per cent of calls hung up |
| 1a | fiscal 2026's observed late-shift compliance carried forward (five call-takers) | none | 98.5 | the FY2028 budget's four call-takers and the board's Halvorsen move |
| 1b | the analyst's own forecast from the history (fiscal 2026 times growth, no Halvorsen), the right queue | none | 93.5 | SOP 2.10 5.1 and the workbook's Halvorsen column |
| 1c | Erlang C with the busy time scaled to reproduce fiscal 2026 (210.1 s) | July, August, June | 87.1 | the ACD's own busy time (227.0 s, standard error 0.4); it predicts no hang-ups; its July, August and June each round a point below the golden's (87, 88, 88), 9 of 12 figures on the golden's |
| 2 | Erlang A with the hang-ups' own waits as the patience (45.6 s) | none | 90.8 | out of sample it files 96.4 against 95.2, above it in all twelve months, and 2.8 per cent hang-ups against 1.7; an answered call's wait is a lower bound on its caller's patience, not a missing value |
| 3 (decisive) | Erlang A with the patience over every call's wait, answered calls censored (161.4 s) | July, August, June | 88.1 | the golden; out of sample 95.3 against 95.2, hang-ups 1.7 per cent against 1.7 |

Grid, queue model by arrivals (months below 90; July 2027):

| Arrivals | Erlang C | Erlang A, hang-ups' waits | Erlang A, censored |
|---|---|---|---|
| the board's FY2028 forecast | July to September, May, June; 83.6 | none; 90.8 | July, August, June; 88.1 (golden) |
| own forecast, no Halvorsen move | none; 91.8 | none; 94.85 | none; 93.5 |
| fiscal 2026 observed, carried forward | none; 98.5 | none; 98.5 | none; 98.5 |

Off the grid: Erlang C on the board's forecast with five call-takers files none (July 94.6); the calibrated Erlang C is
rung 1c. Calibrating the patience instead (so the queue with hang-ups reproduces fiscal 2026's or January to June
2025's observed compliance, or fiscal 2026's hang-up share) gives 165.8, 174.0 or 164.2 seconds and the golden's call
(asserted).

Position and margin: the golden's set is the only grid cell naming July, August and June; every month's golden
compliance is at least 1.03 points from 90 (June 88.97, August 88.92, May 91.04, September 91.11) and at least 0.37 from
its rounding edge, so a month flips only on moving a full point: August or June needs its arrivals 3.9 or 3.7 per cent
lower, the patience under 92.9 or 95.3 seconds or the busy time under 218.3 or 218.7; September or May its arrivals 4.5
or 4.2 per cent higher, the patience over 382 or 356 seconds or the busy time over 237.1 or 236.5. July's rounded
figure holds for a patience from 131.6 to 212.6 seconds and a busy time from 223.8 to 231.2, against estimates of 161.4
and 227.0 with standard errors of 1.8 and 0.4 on the whole history (20.9 on the late shift's 63 hang-ups alone, same
call at one sigma, asserted; every margin printed by `checks.py`). The off-grid calibration (1c) is the one construction that names the golden's set; it
gets there by moving the measured busy time 7.4 per cent, predicts no hang-ups, and its July, August and June round a
point below the golden's. Dominance: the corrections below rung 3 (no queue, own forecast, calibration, the hang-ups'
waits) each move July by 1.0 to 10.5 points in one direction or the other; the decisive step moves it from 90.8 to 88.1
against rung 2 and from 83.6 to 88.1 against rung 0, and it is the only move that reverses the direction rung 2 took.
Worth: the decisive step carries the whole set (none at rung 2, three months at rung 3) and all twelve figures (every
rung 2 figure 0.98 or more above the golden's, every rung 0 figure 1.22 or more below, so none rounds the same).

## Closure table

| # | Axis | Reading | Closure |
|---|---|---|---|
| 1 | Population | the 911 calls presented to the agency's ACD in the Friday and Saturday late-shift hours of each FY2028 month, calls not yet made and the Halvorsen calls the board forecasts included | filed (the prompt; SOP 2.10 sections 2 and 3; the workbook's Read me); C1 on transfers and test calls (SF17, SF18) |
| 2 | Unit of account | the call | filed (SOP 2.10 section 3) |
| 3 | Attribution window | a night's hours count in the month the night starts | filed (SOP 2.10 section 6); C1 (SF3) |
| 4 | As-of dating | the history runs to 30 September 2026; the forecast is the board's FY2028 edition | filed (the workbook; the README's file list and the QA extract log) |
| 5 | Version basis | the FY2028 sheet; the FY2027 sheet is the year before | filed (the prompt's fiscal 2028; the sheet names) |
| 6 | Denominator | calls presented less calls abandoned within 5 seconds | filed (SOP 2.10 section 3); C4 (SF6) |
| 7 | Weighting | each month's calls: the forecast per hour times its nights | filed (the measure is a ratio of calls); C1 (SF16) |
| 8 | Window length | estimation over the whole history | C3 (SF11, SF12: every window rounds the same) |
| 9 | Boundary inclusivity | 15 seconds and 5 seconds inclusive | filed (SOP 2.10, "within"); C1 (a continuous model) |
| 10 | Rounding path | once, each month's compliance to the whole per cent; the set on unrounded values | the prompt; asserted (SF22, SF23) |
| 11 | Tie-break | none: a set by a threshold | every month at least 1.03 from 90 (asserted at 0.9) |
| 12 | Maturity and censoring | the answered calls' waits are censored observations of patience: the HOW, not a convention; the history is complete to 30 September 2026 | the decisive step; no call is open at the export |
| 13 | Order of operations | the hourly figures, then each month's ratio | C1 (SF16) |
| 14 | Row order | the export's order | C1 (asserted over a shuffled read) |
| 15 | Duplicate resolution | the cutover days carry different calls in each export | C1 (no call in both; asserted, SF24) |
| 16 | Identity normalisation | the main call needs no join across systems | not applicable |
| 17 | Netting against gross | none | not applicable |
| 18 | Dimensional units | legacy local time to the second, i3 UTC to the millisecond; durations in seconds | the README; C1 (SF20) |
| 19 | Code and status semantics | the legacy and i3 dispositions and service codes | the README's code lists; never the stump |
| 20 | Integerisation | four call-takers, whole | not applicable |
| 21 | Clause scope | the 15-second standard covers every 911 call presented | filed (SOP 2.10 section 2) |
| 22 | Forward window contents | the board's forecast for every FY2028 hour; four call-takers every late-shift night | filed (the workbook; the FY2028 budget) |

## Literal reader

Executing the prompt and every filed sentence word for word fixes the population (the prompt; SOP 2.10 sections 2 and
3), the outcome and its denominator (SOP 2.10 section 3), the window and each night's month (the prompt; SOP 2.10
sections 1 and 6), the staffing (the prompt; the FY2028 budget) and the arrivals (SOP 2.10 section 5; the workbook),
and each term has one reading or readings that file the same months and the same rounded figures (the fork table). No
sentence says how a month's compliance follows from arrivals and staffing: the queueing model and the patience are HOW,
and the data's structure forces them (1.7 per cent of calls hang up while they wait; an answered call's wait is a lower
bound on its caller's patience), while the history separates the candidates out of sample (parameters from January to
June 2025, fiscal 2026 predicted): Erlang C 93.7, Erlang A on the hang-ups' waits 96.4, Erlang A on the censored waits
95.3, observed 95.2; hang-ups 0, 2.8 and 1.7 per cent against 1.7. The easy answer is an easy method on the same literal
estimand, never another reading; executing the filed sentences alone gives no figure, and the estimators they admit
(Erlang C, the observed compliance carried forward, Erlang A on the hang-ups' waits) each file a different set
(asserted).

## Oracles

- The ACD history itself (the back-test's target): raw calls, not a control figure; it states no compliance, and the
  analyst builds every out-of-sample comparison from it. No FY2028 figure exists to tie to.
- The board's FY2027 forecast sheet: calls, not answers; it ties to the history's growth under every basis.
- The floor roster: staffing by block and night; no compliance figure.
- The CAD incident export and the administrative-line ACD export (the distractors): no 911 compliance figure; the CAD
  export's call times tie to the ACD under every basis.
- No compliance forecast, staffing study, model output or published compliance figure for fiscal 2028 ships: none for
  the call.

## Ask sheet

**Main call's declared row population:** the two ACD exports (every 911 call's presentation, answer, release, ready,
disposition and service type), the floor roster, the board's workbook, SOP 2.10 sections 1 to 6, the FY2028 budget and
the README. Device and hazard rows in it: 0. The asks' devices sit in the CHE location records, the boundary file, the
PSAP directory and the callback desk log (asserted in `checks.py`: the call computed from the main files alone is the
golden; the asks computed without the roster, the workbook and the documents are the asks). The i3 log is shared and
carries no device: its transfer-target and callback-reference columns are read by the asks alone. Neither ask is keyed
to the call, its construction or its figures, and they share no primary device. Their calendar is filed: SOP 2.10 1.2
sets the fiscal quarters (from 1 July, 1 October, 1 January and 1 April) and says the days, months, quarters and years
the agency reports are local (Central) calendar dates.

**Ask A. Halvorsen wireless calls that reached the agency in each quarter of fiscal 2026, and how many of them the agency
transferred to Wexley County Emergency Communications** (8 figures, whole numbers).
- Golden: Q1 (July to September 2025) 1,473 reached and 1,304 transferred; Q2 1,249 and 1,126; Q3 1,104 and 1,001; Q4
  1,265 and 1,154 (asserted equal to the world's own Halvorsen calls in every quarter).
- H18 home: the board's Halvorsen move is built from Wexley's counts; the planner reconciles it against the Halvorsen
  wireless calls that already reach the agency and are passed to Wexley. The golden workbook's Halvorsen sheet, in the
  planner's words ("placed from Halvorsen Township", "reached the agency", "transferred to Wexley"); the call does not
  turn on it (its arrivals are the board's).
- Construction: every i3 call with service type wireless presented in fiscal 2026 (local date), answered or not,
  placed by its handset location (the CHE's handset fixes; the routing location set aside) inside the Halvorsen
  Township boundary (both parts, less the hole), by local quarter; of them, the calls whose transfer target is either
  of Wexley County Emergency Communications' URIs in the regional directory.
- Primary device A1 (D5, out-of-scope rows known only by structure): the boundary is a MultiPolygon, the township's
  main part with an interior ring (a city inside it that is not part of the township) and a detached part across the
  reservoir. Reading the outer ring of the first part counts the city's calls and drops the detached part's: 397 to 458
  city calls and 100 to 166 detached-part calls a quarter (asserted). Nothing in the pack names the city or the
  detached part: the geometry alone carries them.
- Second device A2 (D2, the record is the latest accepted, not the first delivered): a direct wireless call's first
  location record is its routing location (the serving sector's location, asserted for every call); the handset fix
  follows seconds later. Placing calls by the first record moves calls across the township line both ways in every
  quarter. Every handset fix of a call lies on the same side of the boundary and none within 126 metres of an edge
  (asserted at 40), so the first, last and most precise handset fix agree.
- Third device A3 (D7, the true key elsewhere): Wexley's transfers land on its primary PSAP's URI or, when that is in
  overflow, on its alternate, hosted at the state backup centre under a URI that does not name Wexley; the regional
  directory maps both to Wexley County Emergency Communications. Alternate transfers are 11.6 to 12.0 per cent of the
  transferred in every quarter (asserted at 8 to 15).
- Hazards: HA1 the quarters by local date (the i3 log is in UTC; SOP 2.10 1.2 files the local calendar); HC1 redials
  count as calls; HC2 test calls are not wireless calls (asserted: none is).
- Stops (built, each a complete pipeline): S1 the cracker's path (handset fixes, the first part's outer ring, transfers
  whose URI names Wexley, local quarters): 8 of 8 off (Q1 1,755 and 1,018). S2 the routing location with the full
  geometry and the directory: 8 of 8 off (Q1 1,568 and 980). S3 the full geometry, handset fixes, transfers by the
  URI's name: the 4 transferred figures off (Q1 1,153). S4 everything right but the quarters by UTC date: 8 of 8 off,
  each by 1 or 2 calls. Lazy delta: S1 against the golden, every quarter.
- Span: the i3 log, the CHE location records, the boundary GeoJSON, the PSAP directory and the README (5 files);
  callId, serviceType, presented, disposition, transferTo; call_id, method, lat, lon, radius_m; the geometry; uri,
  agency (14 columns).
- Realism: an NG911 call-handling system stores the routing location delivered with the call and then each handset
  fix the location server returns; a township boundary carved around an incorporated city and split by a reservoir is
  ordinary county GIS; a PSAP's alternate site answers on its own URI.

**Ask B. The share of abandoned 911 calls dialled back within two minutes of the hang-up, each month from January to
June 2026** (6 figures, per cent to one decimal).
- Golden: January 54.9, February 55.3, March 51.4, April 53.6, May 48.3, June 51.6 per cent (117 of 213, 78 of 141,
  126 of 245, 118 of 220, 183 of 379 and 256 of 496; asserted equal to the world's own dial-backs in every month).
- H18 home: the callback desk's two-minute aim (SOP 2.10 7.1) for the callers who hang up, the population the queue
  model's patience is about, reported by the training and callback supervisor beside the staffing request; the golden
  workbook's callback sheet. The call does not turn on it.
- Construction: every 911 call the i3 log shows abandoned, by the local month of its hang-up; dialled back within two
  minutes when a callback-desk task on its callback number made its first dial at or after the hang-up and within 120
  seconds of it, the task it joined included; the population is every abandoned 911 call (the prompt's "all"; SOP 2.10
  7.1, "however briefly the caller held on").
- Primary device B1 (D1, a resubmission that opens no second case): a repeat abandon from a number whose task has not
  dialled yet joins that task, opening no task and leaving no call reference. Joining tasks to calls on the call that
  opened them leaves the repeats unmatched. Repeats in every month, 6 to 23 a month and 4.2 per cent of abandons
  (asserted).
- Second device B2 (D8, an anchor on the current record): a task is stamped when the callback module takes the abandon,
  1 to 21 seconds after the hang-up (the module polls every 20 seconds); measuring two minutes from the stamp moves
  every month (S6, 3.2 to 5.9 points).
- Third device B3 (D5, a repair right for one population only): the callback module queues abandons that hung up
  within 5 seconds behind the others, so misdials are dialled back later; carrying the standard's 5-second exclusion
  over to this ask moves every month by 1.4 to 3.1 points (S5). SOP 2.10 7.1 files the population (every abandoned 911
  call is called back, however briefly the caller held on); nothing files the queueing.
- Hazards: HB1 the callback log's local time without an offset across the 8 March 2026 change (read on a fixed offset,
  March falls to 10.2 per cent and April to June to 0); HB2 the desk's log carries the administrative line's abandoned
  calls too (a task-side share with them reads 59.2 to 63.5); HC1 redials (each abandon counts; one per number a month
  drops 100 and moves every month); HC3 abandoned calls transferred in from other PSAPs are in (29 of them; leaving them
  out moves four months).
- Stops (built): S1 the cracker's path (tasks joined on the opening call, the unjoined counted as not dialled back):
  6 of 6 off, 1.8 to 5.2 points low. S2 the unjoined dropped: 6 of 6 off. S3 joined on the opening call, two minutes
  from the task's stamp: 6 of 6 off. S4 the task log alone, tasks as the unit: 6 of 6 off, 2.7 to 6.2 points high. S5
  merges resolved, misdials left out: 6 of 6 off. S6 merges resolved, two minutes from the stamp: 6 of 6 off. A
  matching window of 25, 45, 90 or 300 seconds for a task stamped after the hang-up gives the same figures. Lazy
  delta: S1 against the golden, every month.
- Span: the i3 log, the callback desk log, SOP 2.10 and the README (4 files); callId, disposition, ended, callbackRef,
  referredBy; task, created, call_ref, callback_number, first_dial, line (11 columns).
- Realism: callback modules fold a repeat abandon into the open task for that number; a task is stamped when the module
  takes the event; very short abandons are queued behind the rest as likely misdials.

**Hazard table** (built deltas, asserted in `checks.py`)

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC against local quarters | the i3 log is in UTC | A | every quarter's two figures move by 1 or 2 calls (S4) |
| HB1 local time without an offset | the callback module's desktop clock | B | a fixed offset loses the matches from 8 March: March 10.2, April to June 0 |
| HB2 administrative-line tasks | one desk works both lines | B (task-side readers) | a task-side share with them reads 59.2 to 63.5, every month off |
| HC1 redials | callers redial after hanging up | A, B | A: one call per number drops 5 to 11 calls a quarter; B: one abandon per number a month drops 100 and moves every month |
| HC2 test calls | the i3 test responder | main, A | main: same call (asserted); A: none is a wireless call |
| HC3 transferred-in calls | other PSAPs transfer callers in | main, B | main: same call (asserted); B: 29 abandons, four months move without them |

**Referee:** the CHE's handset fixes settle A2 and the boundary's own geometry A1; the PSAP directory settles A3; the
callback numbers and first-dial times settle B1 and B2, and the dial delays by hang-up length show B3. None hands over a
quarter's or a month's figure.

**Cracker sheet**

| Ask row | Figures | Cracker (landed the call, ran the battery, executed every filed rule) |
|---|---|---|
| Ask A, Halvorsen wireless calls reaching the agency, by quarter | 4 | miss |
| Ask A, of them transferred to Wexley County Emergency Communications, by quarter | 4 | miss |
| Ask B, abandoned calls dialled back within two minutes, by month | 6 | miss |
| the chart's monthly compliance and its 90 per cent line | 2 | outside |

Mirror leakage: 9 per cent of the ask weight (the chart's form and its 90 per cent line, the files; the mirror, off
the call, misses both asks and the chart's values).

Pair ceiling: 35 (C = 38 + 7 + 55 x 0.10 = 50.5 with the cracker keeping the chart; S = 5 + 7 + 55 x 0.09 = 17.0;
rerun from the generated rubric once the portal returns it).

## Build record

Stage 3 complete on 2026-10-16 (`generator/build.py`, the tenth full build of architecture 2), paused for the stage 4
reader and judge.

- Pack: 14 files in `target/`, six formats (csv, geojson, jsonl, md, pdf, xlsx). The legacy ACD CSV 78,758 rows, the i3
  JSON Lines log 340,059 calls (the file over 25,000 rows), the board's workbook 16,128 forecast rows on two sheets, the
  floor roster 3,829 blocks, the CHE location records 39,486, the PSAP directory 8, the callback desk log 4,565 tasks,
  the CAD incidents 6,241, the administrative line's ACD 35,036, the QA extract log 12 rows; SOP 2.10 and
  the FY2028 budget page as PDFs, the boundary GeoJSON and the README. 417,086 911 calls, 7,651 abandoned. Distractors in
  `metadata.json`: the CAD incidents and the administrative line's ACD, read by neither the call nor the asks
  (asserted). `target.zip` 20,063,313 bytes, sha256 c4d814559820840c41dbadc4fe765698cbed088b176eb3158d29146392cdaa92.
- Goldens: `late_shift_staffing_fy2028.xlsx` (Summary, FY2028 late shift, Model check, Halvorsen FY2026, Callbacks
  Jan-Jun 2026) and `late_shift_compliance_fy2028.png` (opened: twelve bars, the 90 per cent line, the three months in
  red, the source line inside the frame); `submission.md` is written by `deliver.py` from the same objects.
- Gates: `checks.py` 146 assertions, 0 failed (the margins and hazard blocks and the calibrated patience included);
  `verify.py` recomputes every graded figure on its own code path; two builds byte-identical (target, golden,
  metadata.json, figures.json, submission.md, target.zip); `figures_check.py` PASS (93 figures); `precut.py` PASS;
  `voice-check.py` PASS; `scrub_producer_metadata.py` clean on the pack (2024-01-01 to 2026-10-06) and the goldens
  (2026-10-01 to 2026-10-16); `leak.py --asof 2026-10-06` REVIEW, no LEAK (four lines, read below); `guard.py surface`
  0 promoted pairs (the drawn personas found in the pack); `guard.py heart` WARN (answered under `## Draw`); `guard.py
  validate` 189 cards, 0 invalid.
- leak.py REVIEW, read: (1) the FY2028 budget page shares 16 of 24 words with the committed call because it carries the
  decision's frame (the board asks in which months of fiscal 2028 a seasonal fifth call-taker should cover the Friday
  and Saturday late shift); it names no month, no compliance figure and no method. (2) The README's terms are its field
  notes (the forecast workbook, the CHE's `method` column, service types, seconds in a time format, the late-shift
  block, presentation as the queue entry): no queue model, no wait distribution, no patience, no censoring. (3) SOP
  2.10's terms (forecast, seconds, presented, measured, the August date of revision 3) are the filed estimand, what is
  counted and against which arrivals, never how a month's compliance follows from them. (4) The board's workbook names
  the three answer months beside numbers because every month of fiscal 2028 is there beside forecast calls per hour; it
  ranks nothing on compliance and states no staffing figure (Gate G clean).
- House fixes (`reduce-house-fixes`): H1 the container audit clean on the pack and the goldens; H2 every figure in this
  note is printed by `checks.py` or held in `figures.json`; H3 the write-up's counts come from the objects that made
  them; H4 the zip's 14 members are the target files, no folder or OS entry, the chart opened; H8 every SOP citation
  resolves (1.2, 2.2, 3.1 to 3.3, 4.1 to 4.3, 5.1, 5.2, 6.1, 7.1); H9 the extract log lists the 12 data files and the
  README all 14; H11 one `submission.md` and one `prompt.txt` in the tree; H12 and H13 by `voice-check.py`; H16 no call
  after 30 September 2026 and no document dated after 6 October 2026 but the forecast's fiscal 2027 and 2028 rows and the
  boundary's in-service date, forward by nature; H21 the draw's first place names (Calder Valley, Bellmont, Ashford) sat
  near real ones and were replaced, the inventory file's corpus name (`export_manifest`, 46 builds) became the QA extract
  log; H23 both asks read with "none" stay grammatical; H24 the README is the QA team's compile note.
- Stage 4 owes: the leak reader and the determinism judge on this pack, spawned together; every finding fixed in the
  generator in one pass.

## Tried and rejected

- The seed's paused repayment clock (a payment holiday stopping the seasoning clock for some loans): not built; it
  re-aligns the loan-age axis, close kin to task133's delayed entry.
- The payment burden of variable-rate loans as the decisive step (each loan's hazard on its scheduled payment against
  the payment it was underwritten on, prime re-amortised at quarterly resets): prototyped on 2026-10-16. With prime held
  at its reserve-date level the textbook pooled rate missed by 6 to 14 per cent and the latest year's rates by 4 to 10,
  because the history already carries the 2023 to 2026 burden at the same months on book and a 10-year loan's payment
  moves little late in life; burden models with and without calendar or vintage effects scattered 3.5 to 4.8 against a
  truth of 4.5; 25-year loans made the textbook land within 1 per cent; a filed rising-rate outlook would have been a
  signpost and a stress test a change of decision.
- The guarantor-group world with large blocks and steady add-ons (prototypes 6 and 7, 2026-10-16): the group's size as a
  covariate and the latest year's rate times the count landed within a bin of the golden, because the history already
  held groups whose loans were the pool loan's age; rebuilt with blocks of one to four units and add-ons only after
  rates fell in fiscal 2026.
- Add-ons by single-unit operators at the same rate as multi-unit operators: the business rate taken from guarantors
  with one loan ever came out 5 per cent above the golden (the operators who survived went on to expand), outside one
  sigma; add-on rates now follow the operator's units in service.
- Section 1112 months flagged in the servicing history: the flag would have referred Ask A's amounts to a main-call file;
  the paid months stay unflagged and a business that failed while SBA paid shows it when the payments stop.
- Failures deferred while SBA paid (a business that failed during its Section 1112 months shown only when the payments
  stopped): taking those months out of the risk sets (SF13) landed at the bin edge; failures during paid months now
  close within the month like any other.
- The module switch by posting date (every receipt posted from 3 April 2023 gross): netting SBA's share from every
  receipt and adding the Treasury offset shares landed 9 of the 12 Ask B cells; the convention now follows the case,
  so every stop misses every cell.
- More single-loan borrowers to steady the standing-alone rate: the double count the union at per-loan rates carries
  fell to 9 per cent, inside a bin of the golden; singles and operators now scale together and relief-era blocks run
  to five units.
- Two entity guarantors sharing a base name and the last four of their EIN: the guarantor-by-name-and-TIN reading
  (SF16) merged groups the Party No keeps apart; an entity's TIN digits are now unique to its base name.
- A world drawn from streams whose shape followed the parameters: one parameter change re-drew every loan and moved
  the margins between builds; every draw is now keyed by group, unit, month and purpose.
- The earlier, more frequent transient delinquency: the roll-rate reading of delinquency at the reserve date moved
  the allowance 4.7 per cent, outside one sigma; transient delinquency is rarer and failures close faster.
- Open defaults counted as not charged off in the charge-off share: a construction no longer, ruled out as SF18 by
  policy 2.3 (a default still in liquidation is not resolved).
- Architecture 1 (cross-default group pricing): SEND_BACK, the golden did not reproduce and two asks were underdetermined; rule 3 AT_RISK, the clause's execution does most of the move; the shell reads as a task133 template.
- Architecture 2's first parametrisation (patience about 40 seconds, busy time 105 seconds, prototyped 2026-10-16): the summer months could not sit 1.5 points under 90 while the hang-ups' own waits left them above it without a 12 per cent seasonal gap the board's forecast would not carry; the busy time and patience moved to about 227 and 160 seconds and the bins to the whole per cent, each month at least 1.0 from 90.
- A history whose Friday and Saturday late shift ran four call-takers (prototyped 2026-10-16): an observed-compliance curve against volume from the four-call-taker nights, extrapolated to fiscal 2028, landed within a point of the golden; the late shift now runs five through the state grant across the whole history, so fiscal 2028's four are a configuration the history never ran there.
- A lightly staffed history (about 98 per cent overall, prototyped 2026-10-16): the Erlang C calibration missed, but a patience fitted to the observed compliance came out at 250 seconds against a 158-second likelihood estimate, moving July a whole per cent, and the out-of-sample margins fell to a few tenths; the history now runs about 95 per cent overall.
- Redials after 45 per cent of hang-ups within about a minute (prototyped 2026-10-16): the redials' own compliance (about 40 per cent) put the out-of-sample Erlang A half a point above the observed and pulled a compliance-fitted patience to 254 seconds; redials now follow a quarter of hang-ups after about a minute.
- Connect latency on answered i3 calls (built 2026-10-16): the likelihood counted the second or two between delivery and connection as waiting, and the patience came out at 186 seconds against the callers' 161; positions are on auto-answer (SOP 2.10 4.1) and a call delivered to a Ready position is connected on presentation.
- The integer-centred golden (built 2026-10-16): every month's compliance within a hundredth of its whole per cent read as set; each month now sits at its own offset inside its bin, every one at least 0.37 from a rounding edge.
- The Halvorsen move at about 9.5 per cent of the late shift's fiscal 2028 calls (built 2026-10-16): the analyst's own forecast with Erlang C, two errors together, filed the golden's set and 10 of 12 figures; the move is now about a fifth of the late shift's calls, and that cell files no month short (July 91.8).
- A callback desk dialling within about a minute with few repeat abandons (built 2026-10-16): joining tasks on the opening call (S1) and anchoring on the task's stamp left months on the golden; the desk is now slower overnight, the module stamps a task 1 to 21 seconds after the hang-up, and every stop misses every month.
- Ask B's truth with first dials near a member's hang-up or its two-minute mark (built 2026-10-16): the golden and the world's dial-backs parted on a few calls; every first dial now clears each member's hang-up by 2 seconds and its two-minute mark by 1.5 (the two-minute clearance asserted).
- A callback share at exactly 50.0 per cent in one month (built 2026-10-16): read as set; the desk's draws are keyed per task and a realism assertion keeps every share off a whole number.
- The asks' quarters and months left to the reader's calendar (stage 3 audit, 2026-10-16): the i3 log's UTC dates gave a second reading of every quarter and month; SOP 2.10 1.2 now files the fiscal quarters and the local calendar.
- Redials after 35 per cent of hang-ups within about half a minute (built 2026-10-16, for Ask B's repeat abandons): the redials' own congestion put the queue with hang-ups 0.23 above fiscal 2026's observed compliance, and a patience calibrated to that compliance came out at 214 seconds and rounded July, August and June a point low (87, 88 and 88, the calibrated Erlang C's figures); with no redials the misfit turned to 0.21 below. Redials now follow one hang-up in five: the fit to fiscal 2026 is within 0.03, a patience calibrated to fiscal 2026's or to January to June 2025's compliance (166 or 174 seconds) files the same call (asserted), and Ask B keeps repeat abandons in every month.
