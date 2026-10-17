# task158: Slenk's 240-GPU stopgap for the first quarter of 2027 (architecture 1)

Private, never ships. A new build (wave 5), numbered from seed FC29. The seed (which of six AI products gets a 240-GPU
stopgap cluster for the first quarter, and that product's Q1 peak-week GPU shortfall to the nearest 10 GPUs) was read at
its header and Situation only (`status.py task158`). Its world, decision and quantity are kept. Its capacity-policy
referral of any shortfall above twice the stopgap to the build programme is dropped: on every route priced below, no
pool's shortfall comes near 480 GPUs, so the clause would add a rule to execute and decide nothing. Its close-out
allocation mechanism (a per-request cost that is a share of a session's prefill) ships as nothing: the close-out
reports GPU-seconds per request as plain arithmetic, no document says how a session's work divides across its
requests, and the pitfall is re-found from how the serving fleet does the work: a model computes only the prompt
tokens its session cache does not already hold.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task158.json`, architecture v1; `guard.py check` WARN (`repeat.decision`, `repeat.question_form`, answered below), one NOTE (`test.same_driver_older`, differentiated against task151 on the card); nearest driver 0.05 (task228 v2, lineage) |
| Domain / task type | `general-statistics-data-science`, task type `regression-classification-model-diagnostics` (serves Forecasting): the deciding quantity is a fitted cost model's prediction for a traffic class outside its fit (GPU busy time against the prompt tokens the model computes and the tokens it generates), its specification judged on out-of-sample error at the one earlier arrival of that traffic |
| Objective | Forecasting & Predictive Modeling: each pool's GPU requirement in the busiest hour of each ISO week 2027-W01 to 2027-W13, a window not begun at the as-of date (Monday 7 December 2026, the rollup closed at 23:59 UTC on Sunday 6 December) |
| Shape | `other`: the call (one pool of six, and its Q1 peak-week shortfall to the nearest 10 GPUs) carried by decoupled row-set asks on the stopgap's acceptance, the fleet's GPUs in service against plan and the close-out's tenant appendix against billing; criteria counted in `## Ask sheet` |
| Decision | `pick_one_of_n`, answer unit `named_option` (the pool), with the pool's Q1 peak-week shortfall in GPUs to the nearest 10 |
| Mechanism | gap population (decisive: what one unit of GPU work is for a report call; the host pool's per-request and per-token rates are earned by turns that re-send a document the session already holds) with time (the forward traffic is a class the closed quarter never served, bar one early-access tenant since October); generators G1 (the unit of value: requests and tokens sent against prompt tokens computed), G14 (Docs' pooled rate does not apply to report calls), G16 (the specification chosen on out-of-sample error at the early-access tenant); Gate G `forecasting`; strategy `forecast_method_backtest` (GPU time is stationary only per computed prompt token and per completion token, a constructed exposure no column carries) |
| Layer 2 family / pattern | `forecast_uncertainty` (model choice on out-of-sample error); `own:gpu-work-priced-on-computed-prompt-tokens-validated-on-an-early-access-onboarding` |
| Layer 1 | the Docs and Batch pools moved from model lc1 to lc2 in a rolling upgrade on 11 and 12 May 2026 (the rollup's model tag changes and every cost with it); the rollup in UTC hours against the billing meter in CET business days across the 25 October clock change; billing by organisation, product and channel against pool totals that mix every tenant; the commitments ledger's tier codes resolved through the tier sheet, go-live dates staggered across January to March; the fleet plan's node move from Batch to Docs on 15 February; the close-out's tables inside a PDF; one product team's intake in requests per second at the busiest hour, the others in thousands of requests per busiest hour |
| Furniture | forum `operations_desk` (the fleet capacity desk assigns the stopgap under the policy), forcing event `other` (the leased cluster is handed over on Monday 4 January 2027 and must have a pool before then), organisation family `software_or_platform`, role family `capacity_planner`, context artifact `capacity_report` (the quarterly capacity close-out), calibration `pilot_log` (the early-access tenant's reports since 5 October), opening `question-first`, question form `which` |
| Spine | the fleet capacity rollup, one row per GPU pool per UTC hour, 1 January to 6 December 2026, about 49,000 rows (six pools); constructed in the layout of a rollup that joins DCGM busy time to gateway counters |
| Deliverables | `stopgap_q1_2027.xlsx` (the assignment and the ask tables) and `pool_headroom_nov2026.png` (a chart decoupled from the decision quantity); settled at the ask sheet |
| People | drawn with `guard.py names --geo "Netherlands" --seed 158` and checked against the corpus at register: Janne Muijs (fleet capacity lead, owner of the stopgap policy), Casper Heijmans (capacity analyst, author of the Q3 close-out), Louise Hekker (report service product manager, owner of the commitments ledger), Mart Bosch (infrastructure, the stopgap lease and acceptance); the requester is in no file and not in the prompt |
| World | Slenk (checked: no AI company, model provider or Dutch technology firm trades under the name), an Amsterdam company that trains its own models and serves them through six products from its own GPU fleet in two colocation halls in North Holland: Chat (consumer assistant, model l3), Code (IDE assistant, c2), Agents (agent platform, l3), Docs (document Q&A for enterprises, lc2), Batch API (asynchronous summarisation, lc2), Voice (s2) |

**Guard.** The first card (generators G14 first, context artifact `close_out_summary`, forum `line_manager_or_team`,
forcing event `purchase_order_or_contract`) met six BLOCKs after the pull brought task267 and task182: `ban.pattern`
and `ban.artifact` and `ban.forum` against task267, `ban.forcing_event` against task182 v2, `test.same_puzzle`
(population, G14, pick_one_of_n) against task267, and two older same-puzzle and same-driver blocks. Each was a true
repeat, so each axis was redrawn, not relabelled: the decisive generator is G1 (the unit of GPU work is the computed
prompt token, which is what the rung turns on; G14 is the frame), the stakeholder's artifact is the quarterly capacity
report, the desk that assigns the stopgap is the fleet capacity desk, and the forcing fact is the handover date of a
lease already signed. `test.same_driver_older` (population, G1, forecasting) remains against task151 and is
differentiated on the card.

**WARNs answered.** `repeat.decision`: the stopgap goes whole to one pool for the quarter, so the decision is a pick
by construction; the second graded figure (the pool's shortfall in GPUs) is a forecast quantity, and the decision type
of task267 (a referral rule chosen from six) shares nothing else. `repeat.question_form`: the form is taken from the
decision (a pick asks which), as `guide-to-prompt` rules.

**Same-puzzle and same-driver tests.** Gap population, G1, `pick_one_of_n`: no build in the last twelve carries the
triple. Gap population, G1, Gate G `forecasting`: task151 (a stepped payout priced from the spread of appearances that
units planned alike make, read at the new lineup slot's rate), differentiated on the card. None prices a unit of work
on how much of its input the resource must compute.

**Abstraction test.** Stripped of nouns: the work each new call does is priced at the rates the resource shows on
traffic that brings nothing it has seen before, because the host traffic's per-call and per-unit rates are earned by
calls that re-send input the resource still holds from earlier in their own exchange, while every new call opens its
own exchange and computes all of its input; the one earlier arrival of such calls, which every host-based rate and the
shared-input assumption under-predict, confirms the price out of sample. Against `guard.py nearest`: task228 (a
unit's own random error against an unobserved signal), task111 (a failure's originating delay in an earlier system),
task229 (a convex conversion of a daily mean); none maps onto it. Against task67, the nearest driver by shape though
not by text (a fixed-plus-variable loop recovered exactly from per-drop shares that sum to it, carried onto a denser
day): here no share sums to anything, the cost driver is estimated from telemetry against traffic that reuses nothing,
and the rival this build's decisive rung rejects is the expert's own reflex (a report's calls sharing the pack through
the prefix cache), settled out of sample.

**Kinship, answered (the builds the brief names, and every compute card).**
- task140 (the nearest by world: a shared compute cell's batch guarantee struck after reservations, with a storage
  service whose CPU rises with the batch cores) solves a residual jointly with a dependent reservation. Nothing here is
  solved jointly and nothing is a residual: one pool's new traffic is priced on the work the model does for it, and the
  decision compares six pools' shortfalls against their own allocations.
- task156 (paid moderators sized from a shrinking volunteer pool whose capacity shows only when it fell short) is a
  binding supply constraint; here supply is the fleet plan, filed, and the forecast is of demand-side work per call.
- task153 (yard fuel loads, segment by segment between visits, capped at a tankful) builds a quantity from a
  vehicle's visit geometry; here no visit structure caps anything, and the split is in what the server recomputes.
- task148 (a 911 queue drained by abandonment, patience censored for the served) models waiting; nothing here waits
  or is censored: the busiest hour is carried at a filed 70 per cent busy.
- task155 (my own build in flight, the same which-of-N shape: a take-up rate conditioned on whether an open shift
  adjoins the casual's own) conditions a human choice on schedule adjacency; here the conditioning is mechanical and
  on the serving side, and the rival is rejected on a past onboarding's realised GPU time, an organ task155 does not
  carry.
- task141 (a pretrial release tier read from magistrate leniency) and task142 (Hospital in the Home visits) share
  nothing; no other card on file is a GPU, accelerator or serving world.

**WHAT screen (stumping 1.2).** The decisive step prices one report call's GPU work; it settles none of the
estimand's five parts, each filed in the shipped text: population (each pool's planned busiest-hour traffic in the
product team's intake, plus the eleven report-service contracts at their contracted peak reports per hour from the
Monday of each go-live week, each report at its tier's calls per report and its tier's prompt and completion limits per
call: members not yet observed are in it by construction, since none of the eleven has gone live), outcome (the GPUs
that carry the pool's busiest hour at 70 per cent busy, busy as the fleet rollup counts it), window (the thirteen ISO
weeks 2027-W01 to 2027-W13), unit (GPUs, the shortfall to the nearest 10) and comparison (the GPUs the Q1 fleet plan
allocates the pool that week; a pool's Q1 peak-week shortfall the largest of its thirteen). No shipped sentence says
how traffic converts into GPU work.

**Data-native sentence.** Slenk's session-affine router keeps a document conversation on the replica that holds its
prefix, so a Docs follow-up re-sends the whole document and the replica computes only the new question, and Docs' GPU
time per request and per token prices almost no prefill; the report service opens a fresh session for every section
call of a report and fans the sections out together, so each call computes its whole source pack; the rollup counts
prompt tokens as sent, so the reuse shows in no column, only in GPU time set against sessions, requests and prompt
lengths, in the Batch pool's single calls on the same model, and in the early-access tenant's reports since October.

**Sources read, one line each.**
- Seed FC29 header and Situation (`status.py task158`): the world, the six products, the 240-GPU stopgap for one
  quarter, the eleven bulk report tenants and the shortfall quantity; nothing else of the seed is read or kept.
- `guard.py mechanisms --objective forecasting`: the forecasting drivers on file price units, cohorts, queues, capacity
  residuals, hazards and conditioned yields; none prices a unit of work on the input its resource must compute.
- `two-layer-task-design.md`: "validating a forecast properly (testing it only on data it was not built on)" is the
  frame: the cost model is fitted where the history lives and judged where the new traffic first appeared.
- `layer2-rigor-patterns.md`, general statistics, regression diagnostics pattern 2 (leave-out residuals for misfit):
  learned, not copied; here the leave-out set is a new traffic class and the misfit is a specification, not a point.
- `strategies.md` F6 (task46, a rate stationary only in a constructed exposure): the exposure here is the computed
  prompt token, constructed from session structure and a second pool, never logged.
- `guide-to-prompt/references/examples.md` 1 (task133, the divisor no sentence names): the stump is a step a careful
  analyst takes by default, here the per-request planning figure every pool's intake is costed with.

## Default path

Figures from the design prototype (`scratchpad/b158/proto/ladder2.py`), to be replaced by `generator/calc.py` on the
shipped files and asserted in `generator/checks.py`.

1. Read the stopgap policy: a pool's requirement for a week is the GPUs that carry its busiest hour at 70 per cent
   busy; report-service contracts count at their contracted peak reports per hour from the Monday of the go-live week,
   each report at its tier's calls and limits; the shortfall is the requirement less that week's allocation, and the
   stopgap goes to the pool with the largest Q1 peak-week shortfall.
2. Cost each pool's busiest-hour requests in the Q1 intake at the pool's GPU-seconds per request in the Q3 close-out,
   divide by 2,520 GPU-seconds (3,600 at 70 per cent busy) and subtract the fleet plan's allocation week by week.
3. Add Docs' report-service contracts: each contract's contracted peak reports per hour times its tier's calls per
   report, from its go-live week, costed at Docs' GPU-seconds per request (about 34 GPUs at full volume).
4. Take each pool's largest weekly shortfall and pick the largest: Code (about 299 in W13), Docs about 121, Agents
   about 119, Voice about 22, Chat and Batch in surplus.

Ends on: Code, 300 GPUs.

Golden: Docs, 340 GPUs (Docs' interactive requirement about 743 GPUs in W13, the eleven contracts about 250 GPUs at
lc2's cost per computed prompt token and per completion token, against the 656 GPUs the fleet plan allocates Docs from
15 February).

## Stump sentence

A competent solver costs every pool's planned busiest hour at the Q3 close-out's GPU-seconds per request, adds Docs'
contracted report calls at Docs' own rate per request (or per token, per session, per new session, at the early-access
tenant's cost per call or per report, or with a report's sections sharing the pack through the prefix cache) and sends
the stopgap to Code, 300 GPUs short; the step that lands it there is pricing report calls at rates earned by Docs turns
that re-send a document the session already holds, when every report call is its own session and computes its whole
source pack, which at lc2's cost per computed prompt token and per completion token leaves Docs 340 GPUs short.

## Three rules

- **Task type:** `general-statistics-data-science` / `regression-classification-model-diagnostics`, which serves
  Forecasting: the deciding object is a fitted cost model's prediction for a traffic class outside its fit, and its
  specification is judged on out-of-sample error.
- **Domain test:** the quantity that decides the call is the GPU work of one report call, the prediction of a
  regression of GPU busy time on the prompt tokens the model computes and the tokens it generates, fitted on the Batch
  pool's single calls on lc2 and judged against the early-access tenant's realised GPU time out of sample; replacing it
  with a generic summary (the close-out's mean GPU-seconds per request, a blended rate per token) moves the call to Code.
- **Swap:** "which ward gets the agency nurses, when the new day-case list is costed at the ward's nursing minutes per
  patient" reads as a case-mix question, but nothing in a ward makes a repeat visit nearly free because the ward still
  holds what the first visit computed; the reason the host rate understates the new work, and the fix (the rate on input
  the server must compute, read from traffic that reuses nothing), has no counterpart outside model serving.
- **Layer 1:** the lc1 to lc2 upgrade of 11 and 12 May (the rollup's model tag and every cost change), UTC rollup hours
  against CET billing days across the October clock change, billing by organisation and channel against pool totals,
  tier codes resolved through the tier sheet, staggered go-live weeks, the February node move, the close-out's tables
  in a PDF, one intake in requests per second; each is how Slenk's own systems record the work, and none is placed to
  be caught or moves the call.
- **Layer 2:** `forecast_uncertainty`: the cost model's specification (GPU work on computed prompt tokens and on
  completion tokens, the rates read where nothing is reused) chosen because it alone predicts the early-access
  tenant's realised GPU time out of sample, against per-request, per-token, per-session, per-new-session and
  shared-pack rivals that each under-predict it.
- **Decisive step:** pricing each report call at lc2's cost per computed prompt token and per completion token, every
  call its own session computing its whole pack, rather than at Docs' rates, which are earned by turns that re-send a
  document the session cache already holds.
- **Not semantics:** no field, code or definition names the reuse: the rollup counts prompt tokens as sent, not as
  computed, the close-out's GPU-seconds per request are correct arithmetic, and reading every column right still prices
  report calls at a Docs rate and files Code.
- **Not rule application:** the policy files the requirement (the busiest hour at 70 per cent busy), the committed
  volume (contracted peak reports at tier limits) and the shortfall; no filed rule says how traffic converts into GPU
  work, so executing every stated rule with the close-out's figures files Code at 300.
- **Analyst test:** a strong analyst who reads every rule correctly and costs each pool's planned busiest hour at its
  Q3 GPU-seconds per request, with Docs' report calls at Docs' own rate per request, per token or per session, files
  Code at 300 GPUs; only pricing each report call on the prompt tokens lc2 must compute for it, at rates from traffic
  that reuses nothing, gives Docs at 340.
- **Estimand:** the stopgap policy (`stopgap_policy_2026-11.pdf`, sections 2 to 5) fixes the population (each pool's
  intake busiest-hour traffic plus the report-service contracts at contracted peak from the go-live Monday, at tier
  limits), the outcome (GPUs carrying the busiest hour at 70 per cent busy, busy as the rollup counts it), the window
  (ISO weeks 2027-W01 to 2027-W13), the unit (GPUs, compared to the nearest 10) and the comparison (that week's fleet
  plan allocation, the largest weekly shortfall).
- **No decoy:** nothing is planted to be caught: the close-out's per-request figures are correct for Q3 and rank
  nothing on Q1, no memo or thread argues for Code, the early-access tenant's traffic is the real traffic of a tenant
  that went live in October, and no stakeholder figure is wrong so the task can overturn it.
- **No certified replay:** the method is not hidden and then recovered by reproducing certified figures: the
  close-out certifies no Q1 figure, and the early-access tenant is raw rollup and billing data against which a
  forecast is tested, not a published number a method must hit.
- **Lesson:** a cost per unit measured on traffic that re-sends input the server already holds does not transfer to
  traffic that brings fresh input every call; price new work on what the server must compute, from traffic that
  reuses nothing, and test the price where the new traffic first arrived; no build on file teaches serving-side reuse.

## Tried and rejected

- Seed referral clause (shortfalls above twice the stopgap go to the build programme): dropped before the prototype;
  on every route priced, including the overstating ones, no pool comes near 480 GPUs, so the clause decided nothing.
- Prefix-cache hit tokens in the rollup (the vLLM counter): rejected at the draw; a column of computed prompt tokens
  makes the cost model a subtraction the schema hands over, and the reuse would be read, not inferred.
- A dedicated report lane with its own pool row: rejected at the draw; its own telemetry would price report calls per
  token directly and the host product's rates would never be in play.
- Docs' busiest hours richer in new sessions than its average hour (work per request at the busiest hour above the
  quarter's mean): rejected at the prototype; a literal reader costing the intake at the close-out's GPU-seconds per
  request would file a second figure for the same filed estimand, a fork on the graded number.
