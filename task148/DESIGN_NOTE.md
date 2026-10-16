# task148: Calder Valley's FY2028 late-shift 911 staffing (architecture 2)

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
  out) and the regional board files the arrival forecast; nothing filed says how a queue behaves. The decisive step is
  an estimate the data force against the field's default (Erlang C): the callers' patience, estimated over every call's
  wait with the answered calls censored, inside a queueing model with reneging (Erlang A). The back-test on fiscal 2025
  and 2026 late shifts rejects Erlang C and the patience read off the hang-ups' own waits by a margin visible month by
  month.
- Determinism from the start: the golden is a closed-form stationary queue per forecast hour on two parameters measured
  on about a hundred thousand late-shift calls; the arrivals are the board's filed forecast; every defensible
  construction (the analytic queue, a simulation of it, a continuous simulation of each night, patience by the
  exponential likelihood or a Kaplan-Meier fit, busy time over any window) is asserted to round the same, mid-bin, and
  to survive one sigma; the asks' bases are closed by cited sentences or asserted data facts.
- Strength: Erlang C is the PSAP staffing default and the hang-ups' own waits are the natural patience; each files a
  different set of months and different shares. Only both moves together land.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task148.json`, architecture v2, registered 2026-10-16; `guard.py check` WARN only (repeat.gate_g, repeat.decision, repeat.question_form, answered below); the older same-driver signature (gap time, G16, method_or_model_selection) against task254 v2 and task501 v2 differentiated on the card, with lines against task133, task130, task146, task142 and task149 |
| Domain / task type | `urban-regional-science` (client domain), task type `municipal-service-demand-resource-allocation` (serves Forecasting): a county 911 center's demand and the call-takers it staffs against a response standard; the library's own line for the task type is "response standards are percentiles, not means", and the 15-second standard is one |
| Objective | Forecasting & Predictive Modeling: each month's late-shift answer-time compliance in fiscal 2028 (July 2027 to June 2028), a window not yet open, predicted from the agency's own call history and the board's arrival forecast |
| Shape | `02` forecast across periods: the twelve months of fiscal 2028, each a share answered within 15 seconds, and the months that fall below 90 per cent (12 + 1 criteria), with the asks supplying the rest (counted in `## Ask sheet`) |
| Decision | `designation_set`: the months for which the FY2028 budget funds a seasonal fifth call-taker on the Friday and Saturday late shift |
| Mechanism | gap time (decisive: a caller's patience is a time to an event that the answer censors) and population (the callers still waiting are the ones who did not give up); pattern none; generators G16 (method selection: a queue with reneging against the standard queue) and G12 (an answered call records no patience, only a lower bound); Gate G `method_or_model_selection`; strategy `other` (a queueing model with reneging calibrated on censored waits) |
| Layer 2 family / pattern | `allocation_constraints` (capacity and queueing); `own:queue-with-reneging-censored-patience`, with `estimation_fit` (censoring) in the second move |
| Furniture | forum `board_of_directors` (the agency's board adopts the FY2028 budget), forcing event `budget_or_appropriation`, organisation family `local_government`, role family `field_unit_lead` (the operations manager runs the communications floor), context artifact `published_series` (the regional 911 board's hourly volume forecast), calibration `none`, opening `question-first`, question form `which` |
| Spine | the agency's ACD call-detail export, one row per 911 call presented to the ACD queue (presented, answered or abandoned, released, ready), January 2023 to September 2026: the legacy CSV to the May 2025 NG911 cutover, then the i3 JSON log, about 1.4 million calls, constructed |
| Deliverables | `late_shift_staffing_fy2028.xlsx` (each month's compliance and the months that need a fifth call-taker, the ask tables) and `late_shift_board_note.pdf` (a one-page note with a chart) |
| People | drawn with `guard.py names --geo "United States" --seed 148 --n 40`, skipping architecture 1's five and first names already on file: Leon Carpenter (operations manager, brings the request), Regina Holder (quality assurance and data analyst, the ACD exports), William Braun (the regional 911 board's planner, the volume forecast), Carol Bender (finance director), Gary Dennis (training and callback supervisor); none in the prompt |

**Guard.** WARN `repeat.gate_g` (method_or_model_selection in task461 and task462): both are ETL builds choosing a
conformance or linkage method; here the selection is of a queueing model for a forecast, with no record-linkage or
inventory method in it. WARN `repeat.decision` (designation_set in task462): task462 designates emission sources in an
inventory; here the designation is the months a seasonal position covers, from a forecast. WARN
`repeat.question_form` (which, task462): the decision is a designation, so the question asks which months. The older
same-driver signature (gap time, G16, method_or_model_selection) matches task254 v2 (a time-to-event cut under a lock
date's truncation) and task501 v2 (a walk-forward pick of a pacing base); neither has a queue or reneging, and the card
carries both lines. Nearest drivers 0.08 (task500 v1 lineage) and under.

**Abstraction test.** Stripped of nouns, the driver: units waiting for a service leave when the wait outlasts their own
patience, so the queue each new unit meets is drained by those who give up; a model in which every unit waits until
served overstates every wait, and the patience that sets the drain is seen in full only for the units that left, the
served ones showing only a lower bound, so it has to be estimated over every unit's wait, not from the leavers' waits,
which make units look far less patient and the service better than it will be. The nearest by mechanism: task254 v2
(truncated event times: here the censoring is by service, inside a queue), task142 (a percentile built from arrivals
and durations: here there is a wait, a standard and units that give up), task147 (requests needing every unit of a run:
here no request spans several units), task149 (a rate rising with pace: here no rate is forecast). None shares the
latent structure.

**Data-native sentence.** Calder Valley's ACD log times every 911 call from the moment it reaches the PSAP to its answer
or hang-up and marks which it was; a caller who is answered leaves only the time they had held on so far, and the late
shift's callers hang up after about 40 seconds on average, which drains the queue for those who stay, so the shares a
standard queue gives are too low and the patience read off the hang-ups alone is too short.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (61 builds): no queue with reneging and
no censored patience; the waiting-adjacent builds (task142's arrivals and durations, task147's consecutive runs,
task119 and task127 on bed waits) carry other structures. `layer2-rigor-patterns.md`: municipal-service line 3
(response standards are percentiles) is the frame; patient-flow line 1 (size by blocking or queueing, not mean census)
the nearest method line, in another domain. `two-layer-task-design.md`: "the data's real structure such as censoring"
and "a forecast validated out of sample" are the client's families for the two moves. task133's, task130's and
task146's cards for the differentiation the re-root asks for. The seed FC19 is not used beyond its number.

**World.** Calder County (fictional) runs one consolidated 911 center, the Calder Valley Emergency Communications
Agency, the primary PSAP for the county and its towns; fire, EMS and sheriff dispatch sit behind it. The agency moved
from legacy CAMA trunks and ALI to NG911 (i3, ESInet) on 13 May 2025, with three days on both systems. Its board adopts
the fiscal-year budget (1 July to 30 June) in May; the FY2028 budget funds four call-takers on the Friday and Saturday
late shift (22:00 to 02:00) and asks whether a seasonal fifth is needed and in which months. The Calder Valley Regional
911 Board publishes the hourly volume forecast the agency staffs to; for fiscal 2028 it adds the wireless calls from
Bellmont Township that NG911 geo-routing moves from the neighbouring PSAP from July 2027. The agency's standard is the
national one: 90 per cent of 911 calls answered within 15 seconds; calls abandoned within 5 seconds are counted as
misdials. Abandoned calls are called back from a separate callback desk, not by the call-takers on the floor.

## Default path

1. Take the board's FY2028 forecast of calls for each Friday and Saturday late-shift hour (22:00 to 02:00) of each month.
2. Measure the call-takers' busy time per call from the ACD log (answer to ready), across the legacy and i3 layouts.
3. Run Erlang C, the standard PSAP staffing model, for each hour with four call-takers: the share answered within 15
   seconds; weight the hours by their forecast calls into each month's share.
4. Mark the months below 90 per cent and fund the fifth call-taker for them.

Ends on: eleven of the twelve months below 90 per cent (July 2027 about 72 per cent), a full-year fifth call-taker.

Golden: the summer months only below 90 per cent (July 2027 about 86 per cent; the shoulder and winter months 91 to 94),
a seasonal fifth call-taker; figures set at stage 3.

## Stump sentence

Running the standard Erlang C staffing model on the board's FY2028 late-shift forecast with the measured busy time and
four call-takers puts eleven of the twelve months below the 90 per cent standard (July 2027 about 72 per cent) and asks
for a full-year fifth call-taker; the step that lands it there is treating every caller as waiting until answered, when
Calder Valley's late-shift callers hang up after about 40 seconds and those who leave shorten the wait for those who
stay, so only the summer months fall short (July about 86 per cent), and the patience must be measured over every
call's wait, not from the hang-ups' own waits, which leave no month short.

## Three rules

Written at the draw; the figures are the design's and are set on the built pack at stage 3.

- **Task type:** urban-regional-science, municipal-service-demand-resource-allocation (serves Forecasting): the county
  911 center's demand and the call-takers it staffs against the 15-second answer standard, forecast for each month of
  fiscal 2028 from its own call history and the regional board's arrival forecast.
- **Domain test:** the deciding quantity is each month's late-shift answer-time compliance under the call-answering
  standard with the funded call-takers, which a PSAP staffing analysis computes from a queueing model of its own calls;
  because 911 callers hang up, the model is Erlang A calibrated on the agency's ACD log, with the callers' patience
  estimated over every call's wait, censored where the call was answered.
- **Swap:** "how many hospital beds" keeps arrivals and stays, but a 15-second answer standard, a call-taker's busy time
  that runs to the CAD entry, 911 callers who hang up within seconds of waiting, misdials under 5 seconds and an NG911
  re-routing that moves a township's wireless calls have no counterpart, so what sets each hour's compliance stops
  making sense.
- **Layer 1:** the ACD export in two layouts across the May 2025 NG911 cutover (legacy CSV in local time to the second,
  the i3 JSON log in UTC with milliseconds, three days in both); transferred-in calls presented with their own arrival
  time here; carrier test calls in the same export; the late shift crossing midnight and daylight-saving changes, so a
  Friday shift ends on Saturday; the call-takers' state log on its own keys; the board's forecast in its own workbook
  layout by month, day type and hour. Each is what these systems write; none carries the stump (asserted at stage 3).
- **Layer 2:** `allocation_constraints` with `estimation_fit` inside it: the queue drains through callers who give up,
  so the standard queue's every-caller-waits assumption is wrong for this center, and the patience that sets the drain
  is a censored duration whose naive estimate from the hang-ups alone is badly short.
- **Decisive step:** model each forecast hour as a queue with reneging (Erlang A, M/M/4+M) on the board's arrivals, the
  measured busy time and the callers' patience estimated over every call's wait (the total time all calls waited over
  the calls that hung up, the exponential likelihood with answered calls censored), and read each month's share
  answered within 15 seconds, calls abandoned within 5 seconds left out.
- **Not semantics:** every field (presented, answered, abandoned, released, ready, class of service, the transfer flag)
  and the standard's definition are read the same way by the easy route; no field or definition says that callers'
  hang-ups shorten the others' waits or how patient a caller is; the default path reads them all and still files
  eleven months short.
- **Not rule application:** the shipped sentences that bear on how the figure is computed (the prompt's question, the
  standard's measure and its 5-second exclusion, the busy-time and shift definitions in the SOP and the field notes,
  the board's statement that the agency staffs to its forecast) are executed word for word on the clean truth at stage
  3 and give no figure of their own: they say what is counted and what the arrivals are, never a queue, a wait or a
  patience; the estimators they admit (Erlang C, the observed shares carried forward, Erlang A with the hang-ups' waits)
  each file a different set of months.
- **Analyst test:** a strong analyst who joins the legacy and NG911 ACD exports, reads the standard and the board's
  forecast correctly and runs Erlang C on each month's forecast late-shift hours with the measured busy time and four
  call-takers files eleven of the twelve months below 90 per cent (Ends on) and a full-year fifth call-taker; with the
  hang-ups modelled on the patience their own waits give, no month falls short; carrying fiscal 2026's observed shares
  forward, no month falls short either, because the township's re-routed calls are not in them.
- **Estimand:** the agency's call-answering standard (SOP 2.10, the PDF) and the prompt: the share of 911 calls presented
  to the PSAP in the Friday and Saturday late-shift hours (22:00 to 02:00) of each month of fiscal 2028 that are answered
  within 15 seconds, calls abandoned within 5 seconds left out, with the four call-takers the FY2028 budget funds, on
  the regional board's forecast arrivals; the population, outcome, window and unit are filed, the method is not.
- **No decoy:** no consultant's staffing study, prior-year staffing model, vendor estimate, board figure or certified
  table states or argues a share, a staffing level or a method; the board's forecast is of calls, not of answers.
- **No certified replay:** no certified or published compliance figure for fiscal 2028 ships and nothing graded is
  reproduced; the patience and the busy time are estimated from the raw ACD log.
- **Lesson:** in a service where the waiting give up, the wait every new arrival meets is shortened by those who left,
  so the standard queue is too pessimistic, and how patient they are can only be estimated over every unit's wait, the
  served ones censored; read off the leavers alone, patience looks far shorter and the service better than it will be;
  no build on file teaches a queue with reneging or a patience censored by service.

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
