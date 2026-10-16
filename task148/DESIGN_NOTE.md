# task148: Tavish County's FY2028 late-shift 911 staffing (architecture 2)

Private, never ships. Wave 4, numbered from seed FC19. Architecture 1 (Fenmore Savings Bank's CECL allowance on its
relief-era SBA 7(a) pool, priced on guarantor groups) was spent at stage 4; its identity is in the card's lineage, the
ledger's dead-architecture row and `## Tried and rejected`, and its files left the folder (they stay in history at
435395d). Architecture 2 leaves the seed's lending world behind: a county 911 center's forecast of its late shift's
answer-time compliance in fiscal 2028. Its first stage 4 (reader clean, judge APPROVE, rule 3 audit strength AT_RISK)
led to the hardening this note describes; the hardened pack's stage 4 (reader clean, judge APPROVE, rule 3 PASS) led to
the corrected residual and the callback desk's linkage sentence recorded below.

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
  out) and the arrival basis (the regional board's forecast); nothing filed says how a queue behaves, how patient a
  caller is or that callers differ by hour. The decisive step is an estimate the data force against the field's
  default (Erlang C): the late shift's own callers' patience, estimated over every one of its calls' waits with the
  answered calls censored, inside a queueing model with reneging (Erlang A).
- Determinism from the start: the golden is a closed-form stationary queue per forecast hour on two parameters measured
  on the agency's own calls; the arrivals are the board's filed forecast; every defensible construction (the analytic
  queue, a simulation of each night from cold or warm, the late shift's patience by the exponential likelihood, a
  Kaplan-Meier fit or the hang-up rate by band over any window of its calls, busy time over any window) is asserted to
  round the same, mid-bin, and to survive one sigma; the asks' bases are closed by cited sentences or asserted facts.

**Stage 4 and the hardening (2026-10-16).** The leak reader was clean and the determinism judge returned
DETERMINISTIC, APPROVE on the first pack (commit 027f6ff; `determinism_check_report.md`). The rule 3 audit passed the
decisive step but read the strength AT_RISK: in a world where every caller had the same patience (161 seconds), a
correction of Erlang C fitted to the history (a miss-rate factor about 0.75, the busy time fudged to 200 to 215
seconds, a logistic recalibration, an empirical curve on the four-call-taker hours) landed the golden's months,
because with every caller alike any correction fitted anywhere carries the right drain. The hardening, in one
generator pass:
- Patience by call mix, a Layer 2 structure in the data, nothing planted: the callers of Friday and Saturday nights
  from 22:00 to 06:00 (bar districts, disturbances, third parties who give up) hold on about two minutes (world 120
  seconds), the rest of the week's about ten (630 seconds by day, 580 in the evening, 540 at night). Nothing in the pack
  says so; the waits and hang-ups by hour show it to anyone who estimates patience by segment (asserted: no document says
  callers differ).
- The golden is Erlang A with the late shift's own patience, censored, 123.2 seconds on its 15,814 calls and 81
  hang-ups; one patience for every call (576.6 seconds) now files May to September, Erlang C May to September, the
  hang-ups' own waits no month, every correction of Erlang C fitted outside the late shift's own hours May to
  September under the cell-mean back-test, and the Poisson-mixed empirical curve on the four-call-taker hours May to
  September (each asserted).
- The residual, stated plainly (corrected after the second stage 4): a correction of Erlang C fitted to the history
  lands the golden's months whenever its back-test runs Erlang C on each historical hour's own count (a Jensen bias
  about the size of the abandonment effect), on every hour and on most of the late shift's windows; crude
  four-call-taker lookups land the same way; under the cell-mean back-test three of sixteen late-shift cells land by
  noise. The rule 3 re-audit puts one strong solver landing at about 0.25 and both of two at about 0.07; `## Ladder`
  gives the figures, each asserted or printed in `checks.py`.
- Critical components re-cut: the monthly compliance at four (every valid route produces it) and the late shift's own
  patience being short, on the order of two minutes (the hardened design makes it necessary); no precise patience is
  graded.
- The asks' readings pinned in the owner's voice, the alternatives asserted, a silent device kept alive in each
  (`## Ask sheet`): Ask A gains A4, the backup centre's records filed under the incident identifier; Ask B gains B4, the
  911 abandons that join an administrative-line task.

**Second stage 4 (2026-10-16).** On the hardened pack (commit eb89e4a) the leak reader was clean (decisive step
analytical, nothing planted), the determinism judge returned DETERMINISTIC and APPROVE with every main figure reproduced
(`determinism_check_report.md`; round 1 kept as `determinism_check_report_round1.md`), and the rule 3 re-audit passed and
recommended shipping the data as is with the record corrected. This pass:
- the residual is restated: the per-hour back-test family and the crude lookups are asserted in `checks.py` as recorded
  landing routes, and the cell-mean assertions carry their convention in their labels;
- the judge's April finding is closed by the README's callback sentence (a task is open from the abandon that opens it
  until it is dialled or closed), with the stamp-only reading asserted (April 51.5);
- the moment-matched patience (79.4 to 111.7 seconds by grouping) is asserted to keep the set, its figure exposure noted;
- the patience component is graded as short, on the order of two minutes, never as a precise figure.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task148.json`, architecture v2, registered 2026-10-16, updated for the hardening; `guard.py check` WARN only (repeat.gate_g, overuse.gate_g, repeat.question_form, answered below); the older same-driver signature (gap time, G16, method_or_model_selection) against task254 v2 and task501 v2 differentiated on the card, with lines against task133, task130, task146, task142 and task149 |
| Domain / task type | `urban-regional-science` (client domain), task type `municipal-service-demand-resource-allocation` (serves Forecasting): a county 911 center's demand and the call-takers it staffs against a response standard; the library's own line for the task type is "response standards are percentiles, not means", and the 15-second standard is one |
| Objective | Forecasting & Predictive Modeling: each month's late-shift answer-time compliance in fiscal 2028 (July 2027 to June 2028), a window not yet open, predicted from the agency's own call history and the board's arrival forecast |
| Shape | `02` forecast across periods: the twelve months of fiscal 2028, each an expected compliance, and the months that fall below 90 per cent (12 + 1 criteria), with the asks supplying the rest (counted in `## Ask sheet`) |
| Decision | `designation_set`: the months for which the FY2028 budget funds a seasonal fifth call-taker on the Friday and Saturday late shift |
| Mechanism | gap time (decisive: a caller's patience is a time to an event that the answer censors) and population (the patience that drains the late shift's queue is its own callers', not the week's); pattern none; generators G16 (method selection: a queue with reneging against the standard queue) and G12 (an answered call records no patience, only a lower bound); Gate G `method_or_model_selection`; strategy `other` (a queueing model with reneging calibrated on the censored waits of the segment it forecasts) |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:queue-with-reneging-censored-segment-patience`, with `estimation_fit` (censoring) and the right comparison group (the late shift's own callers) in the decisive step |
| Furniture | forum `board_of_directors` (the agency's board adopts the FY2028 budget), forcing event `budget_or_appropriation`, organisation family `local_government`, role family `field_unit_lead` (the operations manager runs the communications floor), context artifact `published_series` (the regional 911 board's hourly volume forecast), calibration `none`, opening `question-first`, question form `which` |
| Spine | the agency's ACD call-detail export, one row per 911 call presented to the ACD queue (presented, answered or abandoned, released, ready), January 2025 to September 2026: the legacy CSV to the 13 May 2025 NG911 cutover, then the i3 JSON Lines log, 416,621 911 calls, constructed |
| Deliverables | `late_shift_staffing_fy2028.xlsx` (a summary sheet with the months below 90 per cent and the case for them, each month's expected compliance, a model check with the out-of-sample test and the patience by segment, the two ask tables) and `late_shift_compliance_fy2028.png` (each month's expected compliance against the 90 per cent line, the three months marked); the format set rotates away from task146 (docx), task147 (pdf) and task149 (pptx) |
| People | drawn with `guard.py names --geo "United States" --seed 148 --n 40`, skipping architecture 1's five and first names already on file: Leon Carpenter (operations manager, brings the request), Regina Holder (quality assurance and data analyst, the ACD exports), William Braun (the regional 911 board's planner, the volume forecast), Carol Bender (finance director), Gary Dennis (training and callback supervisor); none in the prompt |

**Guard.** Re-run at stage 3 of the hardening: WARN `repeat.gate_g` (method_or_model_selection against task149) and
`overuse.gate_g` (5 of the last 12): task149 picks a hazard model's base by a filed walk-forward test; here the
selection is of the queueing model and of the population its patience is estimated on, forced by the data's structure
(hang-ups, waits the answer censors, callers who differ by night) with no filed criterion, and its validation is the
analyst's own out-of-sample check, so the class is honest and the mechanism different. WARN `repeat.question_form`
(which, task147): the decision is a designation of months, so the question asks which. The older same-driver signature
(gap time, G16, method_or_model_selection) matches task254 v2 (a time-to-event cut under a lock date's truncation) and
task501 v2 (a walk-forward pick of a pacing base); neither has a queue, reneging or a segment's own patience, and the
card carries both lines. Nearest drivers 0.08 (task500 v1 lineage) and under.

**Abstraction test.** Stripped of nouns, the driver: units waiting for a service leave when the wait outlasts their own
patience, so the queue each new unit meets is drained by those who give up; a model in which every unit waits until
served overstates every wait; the patience that sets the drain is seen in full only for the units that left, the
served ones showing only a lower bound, so it has to be estimated over every unit's wait; and the units arriving in the
window being forecast are not the history's average unit (they give up five times sooner), so it has to be estimated
on their own segment, where one pooled patience leaves the forecast as pessimistic as the standard queue. The nearest by mechanism: task254 v2 (truncated event times:
here the censoring is by service, inside a queue), task142 (a percentile built from arrivals and durations: here there
is a wait, a standard and units that give up), task147 (requests needing every unit of a run), task149 (a rate rising
with pace). None shares the latent structure.

**Same-puzzle test.** Against the last twelve builds and their lineage: task145 shares the time gap and G16 but
allocates a total by a back-tested forecast method (decision `allocation_to_total`, Gate G `forecasting`, strategy
`forecast_method_backtest`); task149 shares the time gap and Gate G `method_or_model_selection` but its generator is
G14, its decision a single figure and its strategy a filed back-test. No build in the window pairs the time gap, G16
and a designation, and nothing here files a back-test: the history's out-of-sample fit is the analyst's own check, not
a criterion in any shipped document. The older same-driver signature (task254 v2, task501 v2) carries the card's
differentiation lines.

**Data-native sentence.** Tavish County's ACD log times every 911 call from the moment it reaches the PSAP to its answer
or hang-up and marks which it was; an answered caller leaves only the time they had held on so far, and the callers
differ by when they call: on Friday and Saturday nights from 22:00 they would hold on about two minutes, the rest of the
week about ten, so the four call-takers' queue in fiscal 2028 is drained by the late shift's own impatient callers,
which a standard queue (nobody hangs up), one patience for the week (577 seconds) and the hang-ups' own waits (38
seconds) all miss.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (61 builds): no queue with reneging and
no censored patience; the waiting-adjacent builds (task142's arrivals and durations, task147's consecutive runs,
task119 and task127 on bed waits) carry other structures. `layer2-rigor-patterns.md`: municipal-service line 3
(response standards are percentiles) is the frame; patient-flow line 1 (size by blocking or queueing, not mean census)
the nearest method line, in another domain. `two-layer-task-design.md`: "the data's real structure such as censoring",
"the right comparison group" and "a forecast validated out of sample" are the client's families for the moves. task133's,
task130's and task146's cards for the differentiation the re-root asks for. The seed FC19 is not used beyond its number.

**World.** Tavish County (fictional) runs one consolidated 911 center, the Tavish County Emergency Communications
Agency, the primary PSAP for the county and its member cities; fire, EMS and sheriff dispatch sit behind it. The agency
moved from legacy CAMA trunks and ALI to NG911 (i3 over the regional ESInet) on 13 May 2025, wireline calls staying on
the legacy trunks to 16 May. Its board adopts the fiscal-year budget (1 July to 30 June) in May. Since July 2024 a
state 911 surcharge grant has paid a fifth call-taker on the Friday and Saturday late shift (22:00 to 02:00); the grant
ends on 30 June 2027 and the FY2028 budget funds four, and asks in which months a seasonal fifth is needed. A late-shift
sick call on those nights is backfilled on overtime, so the grant's fifth is always on the floor. Halvorsen Township, on
the Wexley County line, has had its 911 service from Wexley County Emergency Communications; its agreement ends on 30
June 2027 and from 1 July its calls come to Tavish County. Today a Halvorsen wireless call that reaches Tavish County
through a Tavish cell sector is answered and transferred to Wexley. The Tri-County Regional 911 Board publishes the
hourly volume forecast the region's PSAPs staff to; its FY2028 edition carries the Halvorsen move. The agency's standard
is the national one: 90 per cent of 911 calls answered within 15 seconds of presentation, calls abandoned within 5
seconds counted as misdials. Positions are on auto-answer. The callers of Friday and Saturday nights are another mix
from the week's: they hang up after about two minutes on average against about ten at other hours. Abandoned calls,
911 and administrative line alike, are dialled back from a callback desk staffed around the clock, one open task per
number; a caller who hangs up on the administrative line and then on 911 is dialled back once. During four planned
works in fiscal 2026 the agency answered from its backup centre, whose call-handling system files a call's location
records under the ESInet's incident identifier.

## Default path

1. Take the board's FY2028 forecast for the agency's Friday and Saturday late-shift hours (Friday and Saturday 22:00
   and 23:00, Saturday and Sunday 00:00 and 01:00) in each month.
2. Measure the busy time per answered call from the ACD log (answer to ready, about 3 minutes 47 seconds), across the
   legacy and i3 layouts.
3. Run Erlang C, the standard PSAP staffing model, for each forecast hour with four call-takers: the share answered
   within 15 seconds; weight the hours by their forecast calls into each month's compliance.
4. Mark the months below 90 per cent and fund the fifth call-taker for them.

Ends on: five months below 90 per cent, May to September (July 2027 83 per cent), a fifth call-taker from May to September.

Golden: July 2027, August 2027 and June 2028 below 90 per cent (88, 89 and 89 per cent; September 2027 and May 2028 91, the other months 93 to 95), a fifth call-taker for those three months.

## Stump sentence

Running the standard Erlang C staffing model on the board's FY2028 late-shift forecast with the measured busy time and
four call-takers puts five months, May to September, below the 90 per cent standard (July 2027 83 per cent) and asks
for a fifth call-taker from May to September; the step that lands it there is treating every caller as waiting until
answered, when the late shift's own callers hang up after about two minutes and those who hang up shorten the wait for
those who stay, so only June, July and August fall short (July 88 per cent); the patience has to be the late shift's
own, measured over every one of its calls' waits, because one patience for the whole week (577 seconds) puts May to
September short again and the hang-ups' own waits (38 seconds) leave no month short.

## Three rules

Written at the draw, brought to the design's figures at stage 2 and set on the hardened pack at stage 3.

- **Task type:** urban-regional-science, municipal-service-demand-resource-allocation (serves Forecasting): the county
  911 center's demand and the call-takers it staffs against the 15-second answer standard, forecast for each month of
  fiscal 2028 from its own call history and the regional board's arrival forecast.
- **Domain test:** the deciding quantity is each month's late-shift answer-time compliance under the call-answering
  standard with the funded call-takers, which a PSAP staffing analysis computes from a queueing model of its own calls;
  because 911 callers hang up, and the late shift's callers far sooner than the week's, the model is Erlang A with the
  late shift's own patience, estimated over every one of its calls' waits, censored where the call was answered.
- **Swap:** "how many hospital beds" keeps arrivals and stays, but a 15-second answer standard, a call-taker's busy time
  that runs to the CAD entry, 911 callers who hang up while they wait and hang up sooner on weekend nights, misdials
  under 5 seconds and a township whose 911 service moves between PSAPs have no counterpart, so what sets each hour's
  compliance stops making sense.
- **Layer 1:** the ACD export in two layouts across the 13 May 2025 cutover (the legacy CSV in local time to the
  second, the i3 JSON Lines log in UTC with milliseconds, wireline calls on the legacy trunks to 16 May and wireless
  calls on i3 from 13 May, so both files carry those days with different calls); transferred-in calls presented with
  their own arrival time; test calls answered by the i3 test responder in the same export; redials after hang-ups; the
  late shift crossing midnight and the daylight-saving nights; the floor roster dated by the evening a block starts,
  with its overtime backfill notes; the board's forecast as a long table for the region's four PSAPs by month, day and
  hour beginning, with a FY2027 sheet beside the FY2028 one; the i3 log carrying both ESInet identifiers. Each is what
  these systems write; none carries the stump (asserted, R2).
- **Layer 2:** `allocation_constraints` with `estimation_fit` inside it: the queue drains through callers who give up,
  so the standard queue's every-caller-waits assumption is wrong; the patience that sets the drain is a censored
  duration whose naive estimate from the hang-ups alone is badly short; and it has to be estimated on the right
  comparison group, the late shift's own callers, since the week's are five times as patient.
- **Decisive step:** model each forecast hour as a queue with reneging (Erlang A, M/M/4+M) on the board's arrivals, the
  measured busy time (226.9 seconds) and the late shift's own callers' patience estimated over every one of its calls'
  waits (the total time its 15,814 calls waited over the 81 that hung up, the exponential likelihood with answered
  calls censored, 123.2 seconds), and read each month's compliance under the standard's measure.
- **Not semantics:** every field (presented, answered, abandoned, released, ready, service type, the transfer fields)
  and the standard's definition are read the same way by the easy route; no field or definition says that hang-ups
  shorten the others' waits, how patient a caller is or that callers differ by night; the default path reads them all
  and still files five months short.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the prompt's question, SOP
  2.10's measure and its 5-second exclusion, the busy-time and shift definitions in the SOP and the README, the SOP's
  statement that staffing is planned on the board's forecast) are executed word for word on the clean truth in
  `checks.py` (the rule 3 block, ten sentences) and give no figure of their own: they say what is counted and what the
  arrivals are, never a queue, a wait, a patience or whose patience; the estimators they admit (Erlang C, the observed
  compliance carried forward, Erlang A on the hang-ups' waits, Erlang A with one patience for every call) each file a
  different set of months (asserted).
- **Analyst test:** a strong analyst who joins the legacy and NG911 ACD exports, reads the standard and the board's
  forecast correctly and runs Erlang C on each month's forecast late-shift hours with the measured busy time and four
  call-takers files five months below 90 per cent, May to September (July 2027 83 per cent), and a fifth call-taker
  for them; modelling the hang-ups with one patience estimated over every call in the history (576.6 seconds) files the
  same five months (July 85); the patience read off the hang-ups' own waits (37.6 seconds on the late shift, 68.2 over
  every call) files no month or July alone; carrying fiscal 2026's observed late-shift compliance forward (99.1 per
  cent with five call-takers) files none.
- **Estimand:** SOP 2.10 (the PDF) and the prompt: the answer-time compliance (calls answered within 15 seconds of
  presentation over calls presented less calls abandoned within 5 seconds of presentation) of the 911 calls presented to
  the agency in the Friday and Saturday late-shift hours (22:00 to 02:00) of each month of fiscal 2028, with the four
  call-takers the FY2028 budget funds, on the regional board's forecast arrivals (SOP 2.10 section 5); the population,
  outcome, window and unit are filed, the method is not.
- **No decoy:** no consultant's staffing study, prior-year staffing model, vendor estimate, board figure or certified
  table states or argues a compliance figure, a staffing level, a patience or a method, and no document says callers
  differ by hour, day or call mix (asserted); the board's forecast is of calls, not of answers.
- **No certified replay:** no certified or published compliance figure for fiscal 2028 ships and nothing graded is
  reproduced; the patience and the busy time are estimated from the raw ACD log.
- **Lesson:** in a service where the waiting give up, the wait every new arrival meets is shortened by those who left,
  so the standard queue is too pessimistic; how patient they are can only be estimated over every unit's wait, the
  served ones censored, and on the segment the forecast is for: a weekend night's callers who give up after two
  minutes are not the week's who hold on ten, and read off the leavers alone, or pooled over the week, the forecast
  misses either way; no build on file teaches a queue with reneging or a patience censored by service and estimated by
  segment.

## Readability screen

Six tests per rung (1 a filed sentence names it or sends the solver looking, 2 a column, key or marker makes it a
predicate or a header join, 3 an opponent reflex, 4 a control or corpus scores it, 5 the hygiene battery finds it, 6 one
subtraction, ratio or half of a figure). Figures are the hardened pack's (stage 3, 2026-10-16), as `checks.py` prints
them.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 Erlang C on the board's forecast with the measured busy time and four call-takers (May to September short, July 82.6) | no | no | yes (the PSAP staffing default) | no | no | no | readable |
| R1a no queue: fiscal 2026's observed late-shift compliance carried forward (no month short, July 99.1) | no | yes (the answer times give the observed share directly) | yes | no | no | yes | readable |
| R1b the analyst's own forecast from the history with the golden's queue (no Halvorsen move; no month short, July 93.4) | no | no | yes (forecast from history) | no | no | no | readable |
| R1c Erlang C corrected to the history (a miss-rate factor, a busy-time fudge, a logit offset, a fitted compliance curve): under the cell-mean back-test, on every hour, the daytime, the four-call-taker hours, the Sunday to Thursday late block or the late shift's whole history, May to September short (July 84.6 to 86.4); under the per-hour back-test, the golden's set (the residual in `## Ladder`) | no | no | yes (calibrate to history) | no | no | no | readable |
| R2 Erlang A with the hang-ups' own waits as the patience (37.6 seconds on the late shift: no month short, July 90.8; 68.2 over every call: July alone) | no | yes (the disposition marks the hang-ups and their wait is one subtraction) | yes (Erlang A's patience read as the mean time to abandon) | no | no | yes (a mean of one column) | readable |
| R2b Erlang A with one patience over every call, answered calls censored (576.6 seconds; May to September short, July 85.0) | no | no | yes (estimate on all the data there is) | no | no | no | readable |
| R3 (decisive) Erlang A with the late shift's own patience over every one of its calls' waits, answered calls censored (123.2 seconds; July, August and June short, July 88.1) | no (SOP 2.10 files the measure and the arrival basis; nothing names a queue, a wait, a patience or a segment) | no (no column holds a patience or marks a wait as censored; no column or document says callers differ by night) | no (the reflexes are Erlang C, a calibration to history, the mean time to abandon and the most data) | no (no compliance forecast, model output or staffing study ships) | no (the battery is clean on it) | no (a likelihood over one segment's waits inside a queue with reneging, per forecast hour) | silent |

## Semantic fork table

Every term of the main ask and every convention the main computation needs. Each row is asserted in
`generator/checks.py` under its id. Whose patience the queue runs on is the decisive step, a choice of comparison
group the data force (the late shift's 123 seconds against 529 to 628 elsewhere), never a reading: it is a rung
(R2b and the pools in `## Ladder`), not a row here.

| SF | Term or convention | Golden reading | Alternatives | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | fiscal 2028 | 1 July 2027 to 30 June 2028 | calendar 2028 | other months | the prompt ("fiscal 2028, July 2027 to June 2028") and SOP 2.10 section 1 |
| SF2 | the late shift | the hours 22:00 to 02:00 of each night that starts on a Friday or a Saturday: Friday and Saturday 22:00 and 23:00, Saturday and Sunday 00:00 and 01:00, local time | the calendar Friday and Saturday 00:00 and 01:00 | July alone (July 89.7) | the prompt ("Friday and Saturday late shift, 22:00 to 02:00"), the FY2028 budget's staffing table (nights starting Friday and Saturday) and SOP 2.10 5.2 (a block past midnight belongs to the day it starts) |
| SF3 | a night's month | the month the night starts, each of its hours on that month's forecast (the Friday 30 June 2028 night is June's) | each hour in its calendar month's table | same call (asserted) | SOP 2.10 6.1 (a shift's calls are reported in the month the shift starts); same call |
| SF4 | within 15 seconds | answer time less presentation time of 15 seconds or less | under 15 seconds | same call (the model is continuous; asserted) | SOP 2.10 3.3 |
| SF5 | presentation | the moment the call reaches the agency's ACD queue (the i3 queue entry, the legacy trunk seizure) | the moment it reaches a position | no difference (positions are on auto-answer; 93.5 per cent of i3 answered calls show no wait) | SOP 2.10 3.1 and 4.1; the README |
| SF6 | the measure's denominator | calls presented less calls abandoned within 5 seconds of presentation | all calls presented; calls answered only | all presented: each month 0.2 to 0.5 lower, the same set (asserted), August a point lower; answered only: ruled out | SOP 2.10 3.2 and 3.3, the compliance definition |
| SF7 | the arrivals | the board's FY2028 forecast for the agency, the Halvorsen move included | the analyst's own forecast from the history | no month short (R1b) | SOP 2.10 5.1 (staffing is planned against the board's published hourly forecast) |
| SF8 | the forecast's unit | average 911 calls presented per clock hour for that day and hour beginning in that month | the month's total for the cell | ruled out | the workbook's Read me sheet |
| SF9 | four call-takers | four positions taking 911 calls in every late-shift hour of every night | the supervisor or the callback desk taking overflow | ruled out | SOP 2.10 4.3 (the floor supervisor and the callback desk take no calls from the 911 queue) and the FY2028 budget's table |
| SF10 | busy time | answer to the position's return to Ready, the after-call work and CAD entry included | answer to release (talk only) | no month short (talk time 158.8 seconds) | SOP 2.10 4.2 (a position takes no new call until the call-taker sets Ready again after the after-call work and CAD entry) and the README |
| SF11 | the busy-time window | every answered 911 call in the history | the late shift's calls; fiscal 2026; January to June 2025; fiscal 2027's first quarter; one layout; transfers-in left out | same call (asserted: 225.5 to 227.1 seconds) | same call |
| SF12 | the patience window | the late shift's own 911 calls over the whole history | fiscal 2026; the last twelve months; the i3 layout; transfers-in left out; Friday and Saturday nights to 06:00 | same call (asserted: 109.2 to 123.1 seconds, and one sigma, 13.7 seconds either way) | same call |
| SF13 | the patience estimator | the exponential likelihood, answered calls censored | Kaplan-Meier on the late shift's waits with an exponential fitted to it; the hang-ups' rate over the total waiting time by 30-second band; the patience matched to the late shift's fiscal 2026 hang-up share (a method of moments) | same call (asserted: 118.8 and 123.2 seconds); the moment-matched patience, 79.4 to 111.7 seconds by grouping, files the same set (asserted), August and June printing 90 at the coarse groupings; a patience fitted so the queue reproduces the late shift's own observed compliance over its whole history (137 seconds) gives the same twelve figures (printed) | same call; the figure exposure is in `## Ladder` |
| SF14 | the queue in time | each forecast hour as a stationary queue | one continuous queue for each night, from empty or from the evening block's five call-takers | same call (asserted within 0.4: largest moves 0.28 and 0.17) | same call |
| SF15 | the hours of a shift | each hour on its own forecast | the shift's average rate for all four hours | same call (asserted) | same call |
| SF16 | a month's figure | the month's calls answered within 15 seconds over its calls presented less those abandoned within 5 seconds, over all its late-shift hours | the forecast-weighted mean of the hourly figures | same call (asserted) | same call |
| SF17 | transferred-in calls | in the population and in the estimates | left out | same call (asserted) | SOP 2.10 2.2 (transferred-in calls included) |
| SF18 | test calls | out (not 911 calls; the i3 test responder answers them) | in | same call (asserted: 226.0 and 123.8 seconds) | SOP 2.10 2.2 and the README; same call |
| SF19 | redials | each call presented counts, a redial included | one per callback number | ruled out | SOP 2.10 3.3 (calls presented); same call on the estimates (683 calls collapsed, 120.0 seconds; asserted) |
| SF20 | the two layouts | both, legacy local times read with the zone's rules and i3 UTC converted to local | one layout | same call on the estimates (asserted) | the README |
| SF21 | the daylight-saving nights | the 6 November 2027 night runs five clock hours, 01:00 twice; the 11 March 2028 night four | four hours every night | same call (asserted) | same call |
| SF22 | falls short | the unrounded compliance below 90 per cent | the rounded figure below 90 | same call (every month at least 1.03 from 90; asserted at 0.9) | same call |
| SF23 | rounding | each month's compliance to the whole per cent, once | hourly figures rounded first | same call (asserted) | the prompt |
| SF24 | the cutover days | 13 to 16 May 2025 in both exports, each call in one of them | either export alone | same call on the estimates (asserted: 305 legacy and 1,723 i3 calls on those days, none in both) | the README's cutover note |

## Ladder

The hardened pack's figures (stage 3, 2026-10-16); `checks.py` prints every value.

| Rung | Construction | Months below 90 | July 2027 | Dies to |
|---|---|---|---|---|
| 0 | Erlang C, the measured busy time (226.9 s), the board's forecast, four call-takers | July to September, May and June (5) | 82.6 | out of sample (January to June 2025's parameters, fiscal 2026 predicted hour by hour on its own call-takers) Erlang C files 93.8 against an observed 94.7 on the whole floor and predicts no hang-ups where 0.77 per cent of calls hung up (0.46 per cent on the late shift) |
| 1a | fiscal 2026's observed late-shift compliance carried forward (five call-takers) | none | 99.1 | the FY2028 budget's four call-takers and the board's Halvorsen move |
| 1b | the analyst's own forecast from the history (fiscal 2026 times growth, no Halvorsen), the golden's queue | none | 93.4 | SOP 2.10 5.1 and the workbook's Halvorsen column |
| 1c | Erlang C corrected to the history under the cell-mean back-test: a miss-rate factor (0.834 to 0.867), the busy time fudged (214.5 to 217.8 s), one patience fitted to the observed compliance (264 to 478 s), a logit offset, or the Poisson-mixed empirical compliance curve, over every hour, the daytime, the four-call-taker hours, the Sunday to Thursday late block, or the late shift's own hours at five over its whole history | July to September, May and June (a logit offset: none) | 84.6 to 86.4 (logit offset 95.1) | a correction fitted where the queue is light or the callers patient carries their drain into a four-call-taker shift whose callers give up after two minutes; under the per-hour back-test the same corrections land the golden's set (the residual below) |
| 2 | Erlang A with the hang-ups' own waits as the patience (late shift 37.6 s; every call 68.2 s) | none; July alone | 90.8; 89.4 | an answered call's wait is a lower bound on its caller's patience, not a missing value |
| 2b | Erlang A with one patience over every call, censored (576.6 s) | July to September, May and June (5) | 85.0 | the late shift's callers hang up five times sooner (123 s against 529 to 628 s at other hours, the segment table); out of sample one patience predicts 0.14 per cent hang-ups on the late shift against 0.46 observed (the late shift's own, 0.34) |
| 3 (decisive) | Erlang A with the late shift's own patience over every one of its calls' waits, censored (123.2 s) | July, August, June | 88.1 | the golden; out of sample the whole floor 94.5 against 94.7 observed, the late shift's hang-ups 0.34 against 0.46 |

Grid, queue model by arrivals (months below 90; July 2027):

| Arrivals | Erlang C | Erlang A, the late shift's hang-ups' waits | Erlang A, one patience for every call | Erlang A, the late shift's own patience |
|---|---|---|---|---|
| the board's FY2028 forecast | May to September; 82.6 | none; 90.8 | May to September; 85.0 | July, August, June; 88.1 (golden) |
| own forecast, no Halvorsen move | none; 91.1 | none; 94.7 | none; 92.0 | none; 93.4 |
| fiscal 2026 observed, carried forward | none; 99.1 | none; 99.1 | none; 99.1 | none; 99.1 |

Off the grid: Erlang C on the board's forecast with five call-takers files none (July 94.2). One patience pooled over
the late block of every night (359.4 s), over every night from 22:00 to 06:00 (351.0 s) or over Friday and Saturday
from 18:00 to 02:00 (522.1 s) files May to September, every month 0.3 or more from 90 (asserted).

**The residual landing routes, stated plainly** (corrected after the rule 3 re-audit of the second stage 4; every
figure below is printed or asserted by `checks.py`). A correction of Erlang C fitted to the history depends on how its
back-test runs Erlang C over the past hours.

- The per-hour back-test runs Erlang C on each historical hour's own count, weighted by calls. Erlang C's miss rate is
  convex in load, so the realised counts overstate the predicted misses (a Jensen bias). The bias is about the size of
  what the late shift's hang-ups take off fiscal 2028 at four call-takers (July: golden 11.9 per cent missed against
  Erlang C's 17.4). A correction fitted on this back-test lands the golden's set; this is the residual (asserted as
  recorded landing routes):
  - fiscal 2026, every hour: the miss-rate factor 0.739 (July 87.2), the logit offset +0.323 (86.8), the busy time
    209.1 s (86.5) and the free-slope logistic, slope 1.03 (86.9);
  - the whole history, every hour: 0.744 (87.1), +0.316 (86.7), 209.4 s (86.4) and slope 1.02 (86.8);
  - the late shift's own windows: 19 of 24 cells over six windows. The misses: fiscal 2026's factor (0.549, no month
    short) and logit offset (July alone), January to September 2026's factor and logit offset (July alone), and
    calendar 2025's logistic (May to September);
  - the landing cells' twelve figures: July 85.4 to 88.9, 0 to 10 of 12 matching the golden's, the every-hour cells 7
    to 9.
  This is a systematic coincidence, not noise. No reseed or small data change removes it without changing the world's
  loads (`## Tried and rejected`).
- The crude four-call-taker lookups skip the Poisson mixing over each forecast rate and land the same way:
  - the isotonic curve read at the forecast rate (July 88.0, 8 of 12 figures);
  - five-call bins (87.8, 7 of 12);
  - a logistic linear in the hour's rate (87.3, 9 of 12).
  The Poisson-mixed curve and a quadratic logistic file May to September (asserted).
- The cell-mean back-test (cells of year, month, hour, weekday and call-takers, each at its mean count) is the one
  under which every correction fitted outside the late shift's own hours files May to September (asserted under that
  label).
  - On the late shift's own history at five, three of sixteen scalar cells land by sampling: fiscal 2026's miss-rate
    factor (0.730; July 87.3; 9 of 12 figures), fiscal 2026's busy-time fudge (210.9 s; July 86.1; 5 of 12), and
    January to September 2026's miss-rate factor (0.776; July 86.5; 7 of 12).
  - The late shift at five leaves 46 to 184 missed calls per window. The factor's sampling error is about 0.08 (the
    re-audit's bootstrap over nights, 0.15), about 1.4 points on July, against a truth-model factor near 0.87.
  - A free-slope logistic over the cells lands when weighted by calls (slope 1.90; July 82.7; 2 of 12 figures) and
    files none when weighted by hour group.
- The rule 3 re-audit's estimate:
  - plain Erlang C (about 40 per cent of strong solvers) misses;
  - Erlang A with the hang-ups' waits or one pooled patience (about 20 per cent) misses;
  - the back-test-and-correct family (about 20 per cent) lands about half the time;
  - one strong solver lands with probability about 0.25 (0.2 to 0.35), both of two about 0.07 (0.04 to 0.12).
- Valid routes, not residual: the patience fitted to the late shift's own compliance or its hang-up share is the
  golden's model on the golden's population.
  - The compliance fit over the whole history (137 s) gives all 12 figures.
  - The patience matched to fiscal 2026's late-shift hang-up share (0.46 per cent, a method of moments) is 111.7 s on
    cells and 103.3 s on the month's hours (12 of 12 figures). On coarser groupings it is 79.8 and 79.4 s, where the
    set holds (August 89.84 and 89.85, June 89.89 and 89.90; asserted) but August and June print 90 (6 of 12
    figures).
  - That is a one-point exposure on two graded cells, recorded with no change: the likelihood is the principled
    estimate, and the fiscal 2026 late shift's 41 hang-ups against 32 to 39 expected at 123.2 s are within noise.

Position and margin: the golden's set is the only grid cell naming July, August and June. Every month's golden
compliance is at least 1.03 points from 90 (June 88.97, August 88.91, May 91.04, September 91.11) and at least 0.384
from its rounding edge, so a month flips only on moving a full point:
- August or June needs its arrivals 4.0 or 3.8 per cent lower, the patience under 73.9 or 75.6 seconds, or the busy
  time under 218.0 or 218.4;
- September or May needs its arrivals 4.7 or 4.4 per cent higher, the patience over 261.2 or 246.5 seconds, or the
  busy time over 237.3 or 236.7;
- July's rounded figure holds for a patience from 102.1 to 157.9 seconds and a busy time from 223.6 to 231.2, against
  estimates of 123.2 (13.7 standard error on 81 hang-ups) and 226.9 (0.35).

Same call at one sigma, asserted; every margin printed by `checks.py`.

Dominance: the decisive step moves July from 82.6 (rung 0), 84.6 to 86.4 (rung 1c, cell-mean) and 85.0 (rung 2b) up to 88.1,
and from 90.8 (rung 2) down to 88.1; it is the only construction between the hang-ups' waits and the pooled patience.
Worth: the decisive step carries the whole set (five
months at rungs 0 and 2b, none at rung 2, three at rung 3) and all twelve figures (every rung 0 figure 1.49 or more
below the golden's; rungs 2 and 2b 0 of 12 on the golden's).

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
| 8 | Window length | busy time over every answered call, patience over the late shift's own calls, each over the whole history | C3 (SF11, SF12: every window rounds the same) |
| 9 | Boundary inclusivity | 15 seconds and 5 seconds inclusive | filed (SOP 2.10, "within"); C1 (a continuous model) |
| 10 | Rounding path | once, each month's compliance to the whole per cent; the set on unrounded values | the prompt; asserted (SF22, SF23) |
| 11 | Tie-break | none: a set by a threshold | every month at least 1.03 from 90 (asserted at 0.9) |
| 12 | Maturity and censoring | the answered calls' waits are censored observations of patience, and the patience is the late shift's own: the HOW, not a convention; the history is complete to 30 September 2026 | the decisive step; no call is open at the export |
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
sentence says how a month's compliance follows from arrivals and staffing, nor whose patience governs: the queueing
model and the patience are HOW, and the data's structure forces them (0.8 per cent of 911 calls hang up while they
wait, the late shift's 81 of its 15,814; an answered call's wait is a lower bound on its caller's patience; the late
shift's callers give up after 123 seconds against 529 to 628 at other hours, a gap of more than ten standard
errors). The
history separates the candidates out of sample (parameters from January to June 2025, fiscal 2026 predicted): on the
whole floor Erlang C 93.8, Erlang A by segment 94.5, observed 94.7; on the late shift hang-ups 0 under Erlang C, 0.14
per cent with one patience, 0.34 with the late shift's own, 0.46 observed. The easy answer is an easy method on the
same literal estimand, never another reading; executing the filed sentences alone gives no figure, and the estimators
they admit (Erlang C, the observed compliance carried forward, Erlang A on the hang-ups' waits, Erlang A with one
patience for every call) each file a different set (asserted). Every estimator of the late shift's own patience the
data admit (the likelihood, Kaplan-Meier, the hang-up rate by band, the patience matched to its hang-up share at any
grouping, 79.4 to 123.2 seconds) files the same set (asserted); the figure exposure of the coarsest is in `## Ladder`.

## Oracles

- The ACD history itself (the back-test's target): raw calls, not a control figure; it states no compliance or
  patience, and the analyst builds every out-of-sample comparison and the patience by segment from it. No FY2028 figure
  exists to tie to.
- The board's FY2027 forecast sheet: calls, not answers; it ties to the history's growth under every basis.
- The floor roster: staffing by block and night, its overtime backfill notes included; no compliance figure.
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
carries no device: its incident identifier, transfer-target and callback-reference columns are read by the asks alone.
Neither ask is keyed to the call, its construction or its figures, and they share no primary device. Their calendar is
filed: SOP 2.10 1.2 sets the fiscal quarters (from 1 July, 1 October, 1 January and 1 April) and says the days, months,
quarters and years the agency reports are local (Central) calendar dates.

**Ask A. Halvorsen wireless calls that reached the agency in each quarter of fiscal 2026, and how many of them the agency
transferred to Wexley County Emergency Communications** (8 figures, whole numbers).
- Golden: Q1 (July to September 2025) 1,475 reached and 1,326 transferred; Q2 1,243 and 1,127; Q3 1,104 and 1,003; Q4
  1,253 and 1,160 (asserted equal to the world's own Halvorsen calls in every quarter).
- H18 home: the board's Halvorsen move is built from Wexley's counts; the planner reconciles it against the Halvorsen
  wireless calls that already reach the agency and are passed to Wexley. The golden workbook's Halvorsen sheet, in the
  planner's words ("placed from Halvorsen Township", "reached the agency", "transferred to Wexley"); the call does not
  turn on it (its arrivals are the board's).
- Construction: every i3 call with service type wireless presented in fiscal 2026 (local date), answered or not, its
  location records found under its `callId` or, for the backup centre's, its `incidentId`, placed by its last handset
  location inside the Halvorsen Township boundary (both parts, less the hole), by local quarter; of them, the calls whose
  transfer target is either of Wexley County Emergency Communications' URIs in the regional directory.
- Pins, each a sentence in the owner's voice, the alternative asserted as a stop:
  - The location record: the README, "The agency places a wireless call by the last handset location received for it
    (`device` or `gnss`)". The routing location, every call's first record (asserted), is stop S2, 8 of 8 off.
  - Wexley's transfers: the ESInet directory files both Wexley URIs (the primary and `alt07` at the state backup
    centre) under Wexley County Emergency Communications (asserted). The primary alone is stop S3, the 4 transferred
    figures off.
  - The calendar: SOP 2.10 1.2. Quarters by UTC date are stop S4, 8 of 8 off by 1 or 2 calls.
- Primary device A4 (D1, the same records under two key schemes):
  - The planned works: during 19 to 21 August 2025, 3 to 7 November 2025, 9 to 14 February 2026 and 12 to 14 May 2026
    the agency answered from its backup centre, whose call-handling system filed a call's location records under the
    ESInet incident identifier.
  - The split evidence: the i3 log carries both identifiers on every call and names one queue throughout (asserted, no
    marker). The README says only that `call_id` ties each record to its call in the i3 log.
  - Why it is silent: most of the county's wireless calls have no record in the north-east extract anyway, so a join
    on `callId` alone drops the backup centre's calls without a gap. The dropped calls are 39, 71, 57 and 30 a quarter
    (2.4 to 5.7 per cent), 33, 64, 54 and 27 of them transferred.
  - Fair: every record's key is one call's `callId` or `incidentId`, never both (asserted: 571 of 14,982 keys, 3.8 per
    cent, are incident identifiers).
- Device A1 (D5, out-of-scope rows known only by structure): the boundary is a MultiPolygon, the township's main part
  with an interior ring (the City of Tamsen, not part of the township) and a detached part across the reservoir.
  Reading the outer ring of the first part counts the city's calls and drops the detached part's: 395 to 457 city calls
  and 107 to 164 detached-part calls a quarter (asserted). Nothing in the pack names the city or the detached part. A
  MultiPolygon-aware library handles both; a hand-rolled ring test does not.
- Device A3 (D7, the true key elsewhere): Wexley's transfers land on its primary URI or, when that is in overflow, on
  its alternate at the state backup centre, a URI that does not name Wexley; alternates are 10.6 to 13.0 per cent of
  the transferred in every quarter (asserted at 8 to 15). A filter on URIs naming Wexley misses them; the directory
  join finds them.
- Hazards: HA1 the quarters by local date (the i3 log is in UTC); HC1 redials count as calls (one call per number drops
  1 to 5 a quarter); HC2 test calls are not wireless calls (asserted: none is).
- Stops (built, each a complete pipeline):
  - S1, the cracker's path (handset fixes, the first part's outer ring, URIs naming Wexley, the call identifier): 8 of 8
    off (Q1 1,701 and 1,004).
  - S2, the routing location: 8 of 8 off (Q1 1,610 and 1,059).
  - S3, the full geometry, URIs naming Wexley: the 4 transferred figures off (Q1 1,153).
  - S4, the quarters by UTC date: 8 of 8 off by 1 or 2 calls.
  - S5, every other step right, records joined on the call identifier alone: 8 of 8 off (Q1 1,436 and 1,293).
  - S6, full geometry, URIs naming Wexley, the call identifier alone: 8 of 8 off (Q1 1,436 and 1,127).
  - Lazy delta: S1 against the golden, every quarter.
- Span: the i3 log, the CHE location records, the boundary GeoJSON, the PSAP directory, the README and SOP 2.10 (6
  files); callId, incidentId, serviceType, presented, transferTo; call_id, seq, method, latitude, longitude; the
  geometry; uri, agency (12 columns and the geometry).
- Realism: an NG911 call-handling system stores the routing location delivered with the call and then each handset
  fix the location server returns; a backup centre running its own system files records under the ESInet's incident
  identifier; a township boundary carved around an incorporated city and split by a reservoir is ordinary county GIS; a
  PSAP's alternate site answers on its own URI.

**Ask B. The share of abandoned 911 calls dialled back within two minutes of the hang-up, each month from January to
June 2026** (6 figures, per cent to one decimal).
- Golden: January 55.2, February 45.1, March 56.8, April 52.6, May 50.3, June 51.4 per cent (53 of 96, 23 of 51, 63 of
  111, 51 of 97, 94 of 187 and 111 of 216; asserted equal to the world's own dial-backs in every month).
- H18 home: the callback desk's two-minute aim (SOP 2.10 7.1) for the callers who hang up, reported by the training and
  callback supervisor beside the staffing request; the golden workbook's callback sheet. The call does not turn on it.
- Construction: every 911 call the i3 log shows abandoned, by the local month of its hang-up; dialled back within two
  minutes when the desk's first dial to its callback number came at or after the hang-up and within 120 seconds of it,
  through whichever open task the abandon joined.
- Pins, each a sentence in the owner's voice, the alternative asserted:
  - The denominator: SOP 2.10 7.1, every abandoned 911 call is called back "however briefly the caller held on".
    Leaving out the abandons within 5 seconds moves all 6 months (57.3, 44.7, 59.1, 54.8, 51.1, 53.2).
  - The numerator: the README, "A task closed as `caller called in` was never dialled". Counting those tasks as dialled
    back moves all 6 (65.6 to 73.0).
  - The linkage: the README, "The desk works one open task per callback number, from the abandon that opens it until
    the task is dialled or closed: any later abandon from that number in that time joins the task and opens none of
    its own" (joins in every month, 4 to 9 a month, 4.5 per cent of abandons). Tasks keyed on their opening call move
    all 6, whether the unjoined count as not dialled back (51.0, 37.3, 54.1, 45.4, 48.7, 48.2) or are dropped (53.9,
    40.4, 56.1, 48.9, 50.0, 50.2). A task read as open only from its `created` stamp drops the one April abandon that
    hung up 4 seconds before its number's task was stamped: April 51.5, the other five months unchanged (asserted).
- Primary device B4 (D5, a category crossed by label):
  - The callers: some first hang up on the administrative line and then dial 911 and hang up again. The 911 abandon
    joins the open task the administrative-line abandon opened, a task whose `line` is `ADMIN`.
  - Why it is silent: keeping the desk's 911 tasks alone, the natural scope for "abandoned 911 calls", loses them: 2 to
    6 a month dialled back through an administrative-line task, all 6 months off (52.1, 39.2, 54.1, 47.4, 49.2, 48.6).
  - Nothing narrates it: the README says the desk works abandoned 911 and administrative-line calls and one task per
    number, never that a 911 abandon can join an administrative task.
- Device B2 (D8, an anchor on the current record): a task is stamped when the callback module takes the abandon, 1 to
  21 seconds after the hang-up; measuring two minutes from the stamp moves every month (S6: 59.4, 51.0, 58.6, 51.6,
  53.5, 55.1).
- Hazards: HB1 the callback log's local time without an offset across the 8 March 2026 change (read on a fixed offset,
  March falls to 16.2 per cent and April to June to 0); HB2 the desk's log carries the administrative line's tasks too
  (a task-side share with them reads 57.2 to 64.1); HC1 redials (each abandon counts; one per number a month drops 17
  and moves every month); HC3 abandoned calls transferred in from other PSAPs are in (14 of them; leaving them out moves
  five months).
- Stops (built): S1 tasks joined on the opening call, the unjoined counted as not dialled back: 6 of 6 off. S2 the
  unjoined dropped: 6 of 6 off. S3 joined on the opening call, two minutes from the task's stamp: 6 of 6 off. S4 the
  task log alone, tasks as the unit: 6 of 6 off. S6 two minutes from the stamp: 6 of 6 off. S7 the desk's 911 tasks
  alone (B4): 6 of 6 off. A matching window of 25, 45, 90 or 300 seconds for a task stamped after the hang-up gives
  the same figures. Lazy delta: S7 against the golden, every month.
- Span: the i3 log, the callback desk log, SOP 2.10 and the README (4 files); callId, disposition, ended, callbackRef,
  referredBy; task_id, line, created, call_ref, callback_number, first_dial, result (12 columns).
- Realism: callback modules fold a repeat abandon into the open task for that number whatever line it came on; a task
  is stamped when the module takes the event; a caller who gives up on the administrative line often dials 911.

**Hazard table** (built deltas, asserted in `checks.py`)

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 UTC against local quarters | the i3 log is in UTC | A | every quarter's two figures move by 1 or 2 calls (S4) |
| HB1 local time without an offset | the callback module's desktop clock | B | a fixed offset loses the matches from 8 March: March 16.2, April to June 0 |
| HB2 administrative-line tasks | one desk works both lines | B (task-side readers) | a task-side share with them reads 57.2 to 64.1, every month off |
| HC1 redials | callers redial after hanging up | A, B | A: one call per number drops 1 to 5 calls a quarter; B: one abandon per number a month drops 17 and moves every month |
| HC2 test calls | the i3 test responder | main, A | main: same call (asserted); A: none is a wireless call |
| HC3 transferred-in calls | other PSAPs transfer callers in | main, B | main: same call (asserted); B: 14 abandons, five months move without them |

**Referee:** the CHE's handset fixes and the README's placement sentence settle the location record, the boundary's
own geometry A1, the PSAP directory A3, and the i3 log's two identifiers A4; the callback numbers, the tasks' lines and
the first-dial times settle B4 and B2. None hands over a quarter's or a month's figure.

**Cracker sheet**

| Ask row | Figures | Cracker (landed the call, ran the battery, executed every filed rule) |
|---|---|---|
| Ask A, Halvorsen wireless calls reaching the agency, by quarter | 4 | miss |
| Ask A, of them transferred to Wexley County Emergency Communications, by quarter | 4 | miss |
| Ask B, abandoned calls dialled back within two minutes, by month | 6 | miss |
| the chart's monthly compliance and its 90 per cent line | 2 | outside |

The cracker's misses rest on devices a careful solver can resolve, measured here as built stops:
- Ask A: the join on `callId` alone (S5, S6). A solver who checks the location records left unmatched by the i3
  `callId` finds the incident identifiers and lands all 8 figures.
- Ask B: the 911-only task scope (S7). A solver who links every task by number, whatever its line, lands all 6.

Mirror leakage: 9 per cent of the ask weight (the chart's form and its 90 per cent line, the files; the mirror, off
the call, misses both asks and the chart's values).

Pair ceiling: 34 (C = 38 + 7 + 55 x 0.10 = 50.5 with the cracker keeping the chart; S = 5 + 7 + 55 x 0.09 = 17.0).
If the cracker also resolves A4 and B4, with the rest of each ask right, C rises to 100 and the pair to about 58: the
devices are the margin, the portal measures them, and the ceiling is rerun from the generated rubric when it returns.

## Build record

Stage 3 of the hardening complete on 2026-10-16. The second stage 4 (reader clean, judge APPROVE, rule 3 PASS) was
answered in one generator pass (`generator/build.py`, the sixth full build of the hardening). It changed one sentence
under `target/`, the README's callback-desk linkage, and paused for the coordinator's targeted re-read before ship.

- Pack: 14 files in `target/`, six formats (csv, geojson, jsonl, md, pdf, xlsx).
  - The legacy ACD CSV 78,676 rows and the i3 JSON Lines log 339,676 calls (the file over 25,000 rows), each i3 call
    with both identifiers; 416,621 911 calls, 3,407 abandoned, the late shift's 15,814 and 81.
  - The board's workbook 16,128 forecast rows on two sheets; the floor roster 3,829 blocks; the CHE location records
    39,720; the PSAP directory 8; the callback desk log 3,743 tasks; the CAD incidents 6,397; the administrative line's
    ACD 35,114; the QA extract log 12 rows.
  - SOP 2.10 and the FY2028 budget page as PDFs, the boundary GeoJSON and the README.
  - Distractors in `metadata.json`: the CAD incidents and the administrative line's ACD, read by neither the call nor
    the asks (asserted).
  - `target.zip`: 23,225,726 bytes, sha256 f7c143a8a5abe478f7fa14abfc8c68bbb9ddca128dc22f1affd6b3e21eff1661.
    Against the judged pack (eb89e4a, sha256 35bd9728...0b03) only `README.md` differs: the callback-desk sentence now
    reads "The desk works one open task per callback number, from the abandon that opens it until the task is dialled
    or closed: any later abandon from that number in that time joins the task and opens none of its own." The other 13
    files are byte-identical, and so is every graded figure.
- Goldens: `late_shift_staffing_fy2028.xlsx` (Summary, FY2028 late shift, Model check with the out-of-sample table and
  the patience by segment, Halvorsen FY2026, Callbacks Jan-Jun 2026) and `late_shift_compliance_fy2028.png` (opened:
  twelve bars, the 90 per cent line, the three months in red, the source line inside the frame); `submission.md` is
  written by `deliver.py` from the same objects.
- Gates:
  - `checks.py` 203 assertions, 0 failed. These include the margins, the cell-mean calibration, the per-hour residual,
    the crude lookups, the moment-matched patience, the back-test, the pins (the stamp-only linkage reading among them)
    and the devices;
  - `verify.py` recomputes every graded figure on its own code path; two builds byte-identical (target, golden,
    metadata.json, figures.json, submission.md, target.zip);
  - `figures_check.py` PASS (figures in blocks 1 to 4 all in `figures.json`); `precut.py` PASS; `voice-check.py` PASS;
  - `scrub_producer_metadata.py` clean on the pack (2024-01-01 to 2026-10-06) and the goldens (2026-10-01 to
    2026-10-16);
  - `leak.py --asof 2026-10-06` REVIEW, no LEAK (read below); `guard.py surface` 0 promoted pairs (the drawn personas
    found in the pack); `guard.py heart` WARN (answered under `## Draw`); `guard.py validate` clean.
- leak.py REVIEW, read:
  - (1) The FY2028 budget page shares words with the committed call because it carries the decision's frame (the board
    asks in which months of fiscal 2028 a seasonal fifth call-taker should cover the Friday and Saturday late shift); it
    names no month, no compliance figure and no method.
  - (2) The README's six terms (forecast, September, method, late-shift, second, regional) are its field notes: the
    regional board's forecast workbook, the export's last month, the CHE's `method` column, the late-shift block and
    times to the second. No queue model, no wait distribution, no patience, no censoring, nothing on callers differing
    by night.
  - (3) SOP 2.10's four terms (forecast, seconds, second, regional) are the filed estimand: the regional board's
    forecast as the arrival basis and the 15-second and 5-second measures. Nothing says how a month's compliance
    follows from them.
- House fixes (`reduce-house-fixes`):
  - H1 the container audit clean on the pack and the goldens; H2 every figure in this note is printed by `checks.py` or
    held in `figures.json`, the analytic expectations in `## Ladder` and `## Tried and rejected` excepted (scratch
    probes, named as such); H3 the write-up's counts come from the objects that made them;
  - H4 the zip's 14 members are the target files, no folder or OS entry, the chart opened; H8 every SOP citation
    resolves (1.2, 2.2, 3.1 to 3.3, 4.1 to 4.3, 5.1, 5.2, 6.1, 7.1); H9 the extract log lists the 12 data files and the
    README all 14; H11 one `submission.md` and one `prompt.txt` in the tree; H12 and H13 by `voice-check.py`;
  - H16 no call after 30 September 2026 and no document dated after 6 October 2026 but the forecast's fiscal 2027 and
    2028 rows and the boundary's in-service date, forward by nature; H21 the inventory file is the QA extract log, not
    the corpus's `export_manifest`; H23 both asks read with "none" stay grammatical; H24 the README is the QA team's
    compile note.
- Owed before ship: the coordinator's targeted re-read of the README's callback sentence; then target.zip from this
  build, the ledger row, the card and `pipeline.json` SHIPPED.

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
- One patience for every caller (161 seconds; architecture 2 to its first stage 4): the rule 3 audit found Erlang C corrected to the history landing the golden's months (a miss-rate factor about 0.75, the busy time fudged to 200 to 215 seconds, a logistic recalibration, an empirical curve on the four-call-taker hours), because with every caller alike any correction fitted anywhere carries the right drain; the world now gives the Friday and Saturday night callers about two minutes against about ten at other hours, and every correction fitted outside the late shift's own hours files May to September.
- The late shift's patience left at 161 seconds with the rest of the week at 400 to 900 (analytic, 2026-10-16): one patience pooled over the late block of every night (330 seconds) landed the golden's months, and a correction fitted on the late shift at five missed by 0.08 in expectation; with the rest at 900 the hang-ups' own waits over every call put July 0.01 from 90.
- A weekend-night patience of 90 or 100 seconds (analytic, 2026-10-16): at 90 the hang-ups' own waits over every call landed the golden's months (July 89.0, June 89.8); at 100 they filed July and August with June 0.04 from 90; 120 seconds keeps that rung on July alone, every month 0.15 or more from 90 (asserted).
- A history whose late shift ran six call-takers (analytic, 2026-10-16): a correction fitted on the late shift missed by about 0.8 in expectation, but the late shift kept only about 16 hang-ups in 21 months to estimate its own patience from, the golden's sampling error swamping its bins, and the grant pays a fifth, not a sixth.
- A larger Halvorsen move, about 29 per cent of the late shift's fiscal 2028 calls against about a fifth (analytic, 2026-10-16): the expected miss of a late-shift correction widened from about 0.4 to 0.7 points, a gain inside the correction's sampling error (about 1.4 points on July), while more of the call would rest on reading the forecast's Halvorsen column; the move stays about a fifth.
- Separating every late-shift correction of Erlang C (stage 3 of the hardening, 2026-10-16): the late shift at five leaves 46 to 184 missed calls per window, so the factor's sampling error (about 0.08) spans the landing edge (about 0.80) against an expectation near 0.83; three of sixteen window cells land (fiscal 2026 both, January to September 2026 the miss-rate factor) and are recorded in `## Ladder`; no data-native change tried moved the expectation clear, and reseeding to dodge the cells would be noise-shopping.
- A free-slope logistic recalibration of Erlang C over every hour (stage 3 of the hardening, 2026-10-16): weighted by calls its slope (1.90) lands the golden's months with July at 82.7 (2 of 12 figures), weighted by hour group none; a coincidence of the fit, recorded, not asserted.
- The 161.4-second patience over every call as a critical component (stage 4 instruction, 2026-10-16): a correct route on the hardened data need not compute it; the critical components are now the monthly compliance at four and the late shift's own patience at about two minutes.
- Ask A after the pins with its earlier devices alone (the geometry, Wexley's alternate URI, the local quarters; stage 3 of the hardening, 2026-10-16): a careful solver with a MultiPolygon-aware library who reads the directory lands all eight figures; A4, the backup centre's records under the incident identifier, now holds every figure against a join on the call identifier.
- The record's first residual (stage 3 of the hardening) counted only the cell-mean back-test's late-shift cells and its logistic. The rule 3 re-audit of the second stage 4 (2026-10-16) found the per-hour back-test landing the set too: Erlang C on each hour's realised count, with every correction, on every hour and on 19 of 24 late-shift cells (a Jensen bias about the size of the abandonment effect). It also found the crude four-call-taker lookups landing. No small data-native change removes it: a heavier late-shift history moves the true factor from 0.87 toward fiscal 2028's 0.68, inside the landing band, and a lighter one is noisier. So the data ship as is, the residual is recorded and asserted, and the re-audit's estimate stands (one strong solver lands about 0.25, both of two about 0.07).
- Closing the April 2026 callback edge with a generator change (second stage 4, 2026-10-16). One 911 hang-up came 4 seconds before the callback module stamped the task its number's earlier abandon had opened. Making the module stamp before any later abandon would have shortened the stamp lag that device B2 rests on, or tied each poll to the next abandon. Instead the README's callback sentence now says a task is open from the abandon that opens it until it is dialled or closed, and the stamp-only reading is asserted (April 51.5, the other five months and Ask A unchanged).
- The moment-matched patience (second stage 4, 2026-10-16). Matched to fiscal 2026's late-shift hang-up share, it is 79.4 to 111.7 seconds by grouping and keeps the set, but at the coarse groupings it prints August and June at 90. Recorded as a figure exposure with no change: the likelihood is the principled estimate, and 41 hang-ups against 32 to 39 expected is within noise.
