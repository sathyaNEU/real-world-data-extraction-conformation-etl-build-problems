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
| Shape | `other`: the call (one pool of six, and its Q1 peak-week shortfall to the nearest 10 GPUs) carried by two decoupled row-set asks, each pool's November GPU-hours out of service and longest stay (with the chart) and the stopgap's accepted GPUs and held-back nodes by rack; 28 criteria (the call 2, Ask A 12, the chart about 4, Ask B 8, the files 2) |
| Decision | `pick_one_of_n`, answer unit `named_option` (the pool), with the pool's Q1 peak-week shortfall in GPUs to the nearest 10 |
| Mechanism | gap population (decisive: what one unit of GPU work is for a report call; the host pool's per-request and per-token rates are earned by turns that re-send a document the session already holds) with time (the forward traffic is a class the closed quarter never served, bar one early-access tenant since October); generators G1 (the unit of value: requests and tokens sent against prompt tokens computed), G14 (Docs' pooled rate does not apply to report calls), G16 (the specification chosen on out-of-sample error at the early-access tenant); Gate G `forecasting`; strategy `forecast_method_backtest` (GPU time is stationary only per computed prompt token and per completion token, a constructed exposure no column carries) |
| Layer 2 family / pattern | `forecast_uncertainty` (model choice on out-of-sample error); `own:gpu-work-priced-on-computed-prompt-tokens-validated-on-an-early-access-onboarding` |
| Layer 1 | the rollout hours of 11 and 12 May tagged with both builds (`lc1-2025.11+lc2-2026.05`) in the rollup's model column; the rollup in UTC hours against the billing meter in Amsterdam business days across the 25 October clock change; billing by organisation, product and channel against pool totals that mix every tenant; the commitments ledger's tier codes resolved through the tier sheet, its early-access agreement and proposal beside the signed contracts, go-live dates staggered across January to March; the close-out's tables inside a PDF at three decimals; one product team's intake in requests per second at the busiest hour, the others in thousands; collector gaps in two pools' hours (chat-prod 14 August, voice-prod 3 March). Each with its writer and its asserted neutrality in `## Three rules` |
| Furniture | forum `operations_desk` (the fleet capacity desk assigns the stopgap under the policy), forcing event `other` (the leased cluster is handed over on Monday 4 January 2027 and must have a pool before then), organisation family `software_or_platform`, role family `capacity_planner`, context artifact `capacity_report` (the quarterly capacity close-out), calibration `pilot_log` (the early-access tenant's reports since 5 October), opening `question-first`, question form `which` |
| Spine | the fleet capacity rollup (`fleet_rollup_hourly_2026-01-01_2026-12-06.csv`), one row per GPU pool per UTC hour, 1 January to 6 December 2026, 48,956 rows (six pools, three collector-gap hours missing); constructed in the layout of a rollup that joins DCGM busy time to gateway counters |
| Deliverables | `stopgap_q1_2027.xlsx` (the assignment, its basis, and the two ask tables) and `pool_out_of_service_nov2026.png` (each pool's November GPU-hours out of service, decoupled from the decision quantity) |
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

Figures from `generator/calc.py` on the shipped files, asserted in `generator/checks.py` (L1, R3a) and recomputed by
`generator/verify.py` (V10).

1. Read the stopgap policy (`stopgap_assignment_policy_2026-11.pdf`): a pool's requirement for a week is the GPUs that
   carry its busiest hour at 70 per cent busy; the product team's figure is converted at the pool's GPU-seconds per
   request in the latest close-out; report-service contracts count at their contracted peak reports per hour from the
   Monday of the go-live week, each report at its tier's calls and limits; the shortfall is the requirement less that
   week's allocation, and the stopgap goes to the pool with the largest Q1 peak-week shortfall.
2. Cost each pool's busiest-hour requests in the Q1 intake at the pool's GPU-seconds per request in the Q3 close-out
   (as filed), divide by 2,520 GPU-seconds (3,600 at 70 per cent busy) and subtract the fleet plan's allocation week by
   week.
3. Add Docs' report-service contracts: each contract's contracted peak reports per hour times its tier's calls per
   report, from its go-live week, costed at Docs' GPU-seconds per request, the basis the policy files for the product
   team's requests (35.0 GPUs at full volume).
4. Take each pool's largest weekly shortfall and pick the largest: Code 299.3 (W13), Agents 151.0, Docs 124.3, Voice
   21.5, Chat and Batch in surplus (78.0 and 80.2 GPUs over).

Ends on: Code, 300 GPUs.

Golden: Docs, 340 GPUs (338.8: Docs' interactive requirement 745.4 GPUs in W13 at the close-out's 1.6297 and the eleven
contracts 249.4 GPUs at lc2's 0.248 GPU-milliseconds per computed prompt token and 1.85 per completion token, against
the 656 GPUs the fleet plan allocates Docs from 15 February).

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
- **Layer 1:** each item is how Slenk's own systems record the work, none is placed to be caught, and each mishandled
  leaves the call and its bin (asserted, `checks.py` R2a to R2e, D1, SF7): the rollout hours tagged with both builds,
  written by the rollup's model column while the upgrade rolled (kept in the lc2 fit: 339.6); billing's Amsterdam
  business days against the rollup's UTC hours (UTC days: the tenant check reads 0.980 and 0.216, the same separation);
  Voice's intake in requests per second (read as thousands: no change to the call); the staggered go-lives (every
  contract from W01: Docs still first, 340 bin); the collector gaps (outside docs-prod and batch-prod); the close-out's
  three-decimal rates in a PDF (the exact Q3 rates from the rollup instead: 338.8); the ledger's early-access agreement
  beside the signed contracts (ruled out by policy s3; counted, 347.3); billing's one session per report beside the
  gateway's one serving session per call. The lc1 to lc2 change is not Layer 1: pooling across it is the over-rung R5c
  (371.0, or 353.8 with an intercept), rejected by the fit's residuals by build.
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
- **Not rule application:** the policy files the requirement (the busiest hour at 70 per cent busy), the conversion of
  the product teams' requests (the pool's GPU-seconds per request in the latest close-out), the committed report volume
  (contracted peak reports at tier limits) and the shortfall; no filed rule says how a report call converts into GPU
  work, so executing every stated rule leaves the decisive conversion open, and carrying the filed per-request basis
  over to report calls files Code at 300.
- **Analyst test:** a strong analyst who reads every rule correctly and costs each pool's planned busiest hour at its
  Q3 GPU-seconds per request, with Docs' report calls at Docs' own rate per request, per token or per session, files
  Code at 300 GPUs; only pricing each report call on the prompt tokens lc2 must compute for it, at rates from traffic
  that reuses nothing, gives Docs at 340.
- **Estimand:** the stopgap policy (`stopgap_assignment_policy_2026-11.pdf`, sections 2 to 5, with the conversion of
  ordinary traffic in section 3) fixes the population (each pool's
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

## Survivor anatomy

Actor: the property that decides is whether a request re-sends a document its session already holds; no file stores it, and it exists only as the relation between a pool's requests and its new sessions hour by hour, and for the report service as billing's one session per report against the gateway's one serving session per call.
Link: a report call's real cost is read from the Batch pool's single calls on lc2, a sibling pool whose traffic reuses nothing, and checked against the early-access tenant's billing rows set against Docs' rollup hours, billing's Amsterdam days against the rollup's UTC hours; no key joins billing to the rollup, and nothing asks for another pool's calls to cost Docs' work.
Reflex: the field's capacity-planning rate, the close-out's GPU-seconds per request, is rung 0 and files Code at 300 GPUs; the per-token, per-session and per-new-session rates on Docs' own traffic and the shared-pack reading file Code too.
Back-test: the textbook route validates: Docs' rate per request is the close-out's own Q3 figure, the policy files it for the product team's requests, and it reproduces Docs' busy time in the hours it was earned; only the tenant's realised time on its report days refutes it for report calls.
Second use: every file the step reads is in the pack for its own reason: the rollup carries every pool's requirement, the ledger the contracts the policy counts, billing the tenant's record, the close-out the rates the policy files.
Shock: nothing reads as an anomaly: the tenant's excess GPU time is spread across ordinary Docs hours in October and November, and Docs' series shows no jump a sort of the pools would surface.
Pins: the policy's sections 2 to 5 file the requirement, the busiest hour's traffic, the contracts' volume and the shortfall, and section 6 the out-of-service basis for Ask A; no filed sentence names a cost per computed token, a session, the prefix cache or the Batch pool's calls.

## Readability screen

Each rung against the six tests (`stumping` 2.1). R4 is the decisive rung.

| Rung | Filed sentence | Schema | Reflex | Control bench | Hygiene | Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R0 Docs' report calls at Docs' Q3 GPU-seconds per request (the default) | policy s3 files the close-out's figure for the product teams' requests; no sentence carries it to report calls | requests and calls are columns | the planning reflex | none needed | nothing to find | one product | readable |
| R1 report calls priced per token at Docs' rate (blended, or two rates fitted on Docs' raw prompt and completion tokens) | none | prompt and completion tokens are columns | the LLM-cost reflex | none | nothing to find | one ratio or one fit | readable |
| R2 per session, per new session, or at the Batch pool's GPU-seconds per request | none | sessions and the Batch pool are in the rollup | a reflex once calls are seen as sessions | none | nothing | one ratio | readable |
| R3 the early-access tenant's own cost per call, per report or per token | none | the tenant is in billing by organisation | the reference-class reflex | the tenant fits itself in sample | nothing | one ratio | readable |
| R3c the computed-prompt model with a report's calls sharing the pack through the prefix cache | none | no reuse column; billing counts one session per report | the serving expert's reflex (identical prefixes are cached), and billing's six calls a session | refuted only by a constructed excess on the tenant's days | nothing | a per-report sum | readable |
| R4 (decisive) every report call its own session computing its whole pack, priced at lc2's GPU-seconds per computed prompt token and per completion token read where nothing is reused, confirmed on the tenant out of sample | no sentence names reuse, computed tokens or how a call's work is priced | the rollup counts prompt tokens as sent; no cached or computed column; the model tag names a model, not reuse | every reflex above lands wrong (Code, or Docs at 350 to 390) | the tenant refutes R0 to R3c only once its excess over Docs' interactive work is built from billing and the rollup, day by day across the clock change; nothing ships that score | the battery (keys, duplicates, joins, fan-out) finds nothing | a two-rate fit on another pool, applied at tier limits per call, against eleven go-live weeks | silent |

## Semantic fork table

Every term in the main ask and every convention the main computation needs. Each id is asserted in
`generator/checks.py`.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "serving pool" | the six pools of the fleet plan, one per product | product lines or models (Chat and Agents share l3) | same call | the policy, section 1: "one of the six product pools in the fleet plan" |
| SF2 | the stopgap "for the first quarter" | the whole cluster to one pool for ISO weeks 2027-W01 to W13 | split across pools | same call | policy section 1 ("The cluster goes whole to one of the six product pools... It is not split between pools") |
| SF3 | "peak-week shortfall" | the largest of the pool's thirteen weekly shortfalls | the shortfall in the week of the largest requirement | same call (both W13 for every pool), asserted | policy section 4 |
| SF4 | the busiest hour's traffic | the intake's busiest-hour requests for interactive traffic plus committed report volume | an average hour, or a percentile hour | same call under the policy | policy sections 2 and 3, the intake's column heading |
| SF5 | "70 per cent busy" and "busy" | busy GPU-seconds as the rollup counts them, 2,520 per GPU-hour carried | utilisation as GPUs allocated, or SM occupancy | same call | policy section 2 ("the busy GPU-seconds of that hour, as the fleet rollup counts them, divided by 2,520") |
| SF6 | committed report volume | each contract's contracted peak reports per hour in every hour from the Monday of its go-live week, each report at its tier's calls and its prompt and completion limits per call | Q1 committed reports spread over the quarter's hours | Code under the spread (Docs 121.8 at the golden's costing), golden under the policy | policy section 3 ("at its contracted peak reports per hour in every hour") |
| SF7 | the early-access agreement in Q1 | not counted: its status reads "Early access, ends 18 Dec 2026", its tenant on contract RC-2026-031 from 4 January | counted as well as RC-2026-031 | same call, same bin (342.0 against 338.8), asserted | policy section 3 ("A signed report-service contract counts... Proposals and ended agreements do not count") and the ledger's status |
| SF8 | "allocation" | the fleet plan's GPUs for the pool that week, Docs 608 to W06 and 656 from W07 | the opening allocation all quarter | same call, a different bin (386.8 against 338.8), so the week's figure is filed | policy section 4 ("the GPUs the Q1 fleet plan allocates the pool that week") |
| SF9 | weeks | ISO weeks 2027-W01 (Monday 4 January) to 2027-W13 (to Sunday 4 April), UTC | calendar months, or March 31 as the quarter's end | same call | policy section 1 ("ISO weeks 2027-W01 to 2027-W13") and the fleet plan's week columns (Mondays 4 January to 29 March) |
| SF10 | "GPUs" | the fleet's H100 80GB GPUs; the stopgap's are the same part | GPU-equivalents of another part | same call | policy section 1 (30 nodes of eight H100 SXM5 80GB GPUs) and the fleet inventory's gpu_model |
| SF11 | rounding | the shortfall to the nearest 10 GPUs, once, at the end | per week or per contract | same call, same bin, asserted | the prompt's last sentence; policy section 5 compares unrounded figures |
| SF12 | Docs' interactive GPU-seconds per request | the close-out's Q3 figure (1.6297), as policy s3 files it | October and November's pool figure with the tenant's calls left in | same call, same bin (343.7 against 338.8) | policy s3 ("at the pool's GPU-seconds per request in the latest quarterly capacity close-out") |
| SF13 | which model's costs | lc2, the build docs-prod and batch-prod serve from 12 May 2026 to the pull | the year's data pooled across lc1 and lc2 | Docs at 370 (371.2) or, with an intercept, 350 (353.9): another bin; a fit across a model change is not a reading but a misspecification | the rollup's model column, and the data: lc1's own rates sit 45 and 51 per cent above lc2's and a pooled fit under-predicts lc1 hours by 22 per cent and over-predicts lc2 hours by 15 (D5) |
| SF14 | Docs includes its report service | yes: report calls run on docs-prod | a separate pool | same call | policy section 3 ("counts on the pool of the product that sold it") |
| SF15 | the rate for the product teams' requests | each pool's GPU-seconds per request for Q3 as the close-out prints it (0.4419, 0.5889, 0.7335, 1.6297, 2.6095, 0.1203) | the rate in each pool's single busiest Q3 hour; the exact rollup rate | busiest hour: Code 344.5 against Docs 341.8 (a tie at the nearest 10, Code ahead); exact rate: same call, same bin (338.8, the printed rates agreeing to four decimals) | policy s3 ("The product team's figure is converted to busy GPU-seconds at the pool's GPU-seconds per request in the latest quarterly capacity close-out"), which names no report call |

## Ladder

Figures from `generator/calc.py` on the shipped files (`rungs()`, the product teams' requests at the close-out's printed
rates as policy s3 files), each asserted in `generator/checks.py` (L1 to L6, R3b), the default and three more rungs
recomputed by `generator/verify.py`. W13 is every pool's peak week on every rung. Code's shortfall is 299.3 on every
rung (no rung touches it).

| Rung | Docs' report contracts at full volume (GPUs) | Docs' Q1 peak-week shortfall | Pool filed | Dies to |
|---|---|---|---|---|
| R0 Docs' GPU-seconds per request (the default, the filed per-request basis carried over) | 34.9 | 124.3 | Code 300 | the tenant: Docs' rate prices its calls at about a fifth of their GPU time (0.219) |
| R1a Docs' blended rate per token | 66.3 | 155.7 | Code 300 | the tenant, and lc2's prompt cost on the Batch pool, several times Docs' per token |
| R1b two rates fitted on Docs' raw tokens | 92.3 | 181.7 | Code 300 | the same; the prompt rate is diluted by tokens the session cache holds (predicts 0.543 of the tenant's excess) |
| R2a Batch's GPU-seconds per request | 56.0 | 145.4 | Code 300 | report calls carry three to eight times Batch's prompt |
| R2b per new session (Docs' session-start cost) | 148.1 | 237.5 | Code 300 | report packs are larger than a Docs document |
| R2c per session (Docs' GPU-seconds per session) | 172.9 | 262.3 | Code 300 | a session's several turns are not a report call |
| R3a the tenant's cost per report (per billed session) | 128.1 | 217.5 | Code 300 | the contracts' tiers have more and longer calls |
| R3b the tenant's cost per call | 159.8 | 249.2 | Code 300 | the contracts' calls carry larger packs |
| R3c the pack shared across a report's calls (billing's six calls a session read as one served session) | 72.0 | 161.4 | Code 300 | the tenant's excess is its full prompts, not one pack a report (predicts 0.452 of it); the gateway counted a session per call |
| R4 (decisive) computed prompt tokens and completion tokens at lc2's rates, every call its own session | 249.4 | 338.8 | Docs 340 | (the golden) |
| R5a Batch's blended rate per token | 277.5 | 366.9 | Docs 370 | the blend carries Batch's prompt-to-completion mix onto calls with a larger share of prompt |
| R5b the tenant's blended rate per token | 297.9 | 387.3 | Docs 390 | the blend carries the RS-6 mix onto RL-12 and RM-8 calls |
| R5c lc2 and lc1 hours pooled in the Batch fit | 281.6 | 371.0 | Docs 370 | the model column and the fit's residuals by build (D5) |
| R5d the same with an intercept | 264.4 | 353.8 | Docs 350 | the same |

- **Position:** the default ranks Docs third (124.3, behind Code 299.3 and Agents 151.0); the golden ranks it first.
  `dataset-generation` §6.2 asks for fourth or fifth at rung 0: Docs' interactive traffic alone is the third-largest
  shortfall in this fleet, and moving it lower would mean shrinking Docs' own growth, which the intake files; recorded
  as a deviation, harmless to stump power since rung 0 lands on Code by 175 GPUs.
- **Margins:** golden over Code 39.5 GPUs (1.13x, under §6.2's 1.2x): Code's figure depends on no costing of report
  calls, so no defensible construction moves it (asserted, M7 and D1), and the margin is four bins. The nearest
  under-rung (R2c, 262.3) sits 37 under Code; the nearest over-rung (R5d, 353.8) is one bin above the golden.
  **Dominance:** only R4 and the over-rungs put Docs first, and each over-rung files another bin.
- **Determinism variants (D1, D2, D4, O8):** the exact Q3 rates 338.79; an intercept 338.83; windows June to November
  338.82, September to November 338.79, Q3 338.84; weighted fit 340.39; the rollout hours kept 340.93; a daily fit
  341.55; one standard error on both rates 337.70 to 339.93; lc2's rates rescaled to the tenant's whole-period excess
  339.64 (Amsterdam days), 339.68 (UTC days), 340.41 (the exact rate). Every one keeps at least 2.70 GPUs inside 335
  to 345 (worst 3.45 among the fits).
- **Ruled out by a filed sentence or by the data (D3, D3b, D5, D6, SF7, SF12, SF15):** the busiest-hour rates (Code
  344.5 against Docs 341.8) and October and November's Docs rate with the tenant (343.7), both by policy s3's pin; the
  early-access agreement counted (347.3) by policy s3's "ended agreements do not count"; lc1 and lc2 hours pooled
  (371.0, 353.8 with an intercept) by the build change the data show.
- **Grid:** the routes multiply by allocation (week or opening) and the early-access agreement (in or out): under R4
  every cell with the week's allocation and the agreement out lands in the 340 bin; the opening allocation files 386.8,
  so SF8 is filed, not left to the grid.
- **Worth:** R4 alone reverses the call; every correction below it walks Docs up but leaves it under Code, and every
  correction above it overshoots by at least one full bin.
- **Stop rules, written now:** two exact portal solves by different routes re-root the decisive step; a solve through
  the tenant's blended rate (R5b) landing in the bin means the tiers' mixes are too close and is repaired by moving the
  tiers, never by hiding the tenant.

## Closure table

| Axis | Reading and closure |
|---|---|
| 1 Population | intake traffic plus contracts at contracted peak from the go-live Monday, members not yet observed included (none of the eleven is live); policy sections 2 and 3, C1 |
| 2 Unit of account | GPUs per pool per week; the call names the pool; SF1, SF10 |
| 3 Attribution window | ISO weeks in UTC; every go-live a Monday 00:00 UTC, so no contract straddles a week (C1) |
| 4 As-of dating | rollup to 6 December 23:00 UTC, billing to 6 December (Amsterdam days), the ledger exported 4 December, the plan issued 1 December, the pull on 7 December; nothing dated later except forward-dated plan and contract entries (go-lives, the February move) |
| 5 Version basis | the fleet plan issue v3 (1 December, `fleet_plan_2027Q1.xlsx`) is the only Q1 issue shipped, its About sheet naming what v2 differed in; the ledger is one export; the close-out is the October issue |
| 6 Denominator | busy GPU-seconds over 2,520 per GPU at 70 per cent busy (policy section 2); the product teams' requests converted at the latest close-out's GPU-seconds per request (policy section 3) |
| 7 Weighting | not used: each pool's requirement is a sum of its own traffic; the cost fit weights hours equally, and weighted (340.53) and daily (341.69) fits stay in the bin with OLS (338.95) (C3, asserted D1, D2) |
| 8 Window length | the cost fit on lc2 hours: June to November, September to November and Q3 windows give 338.93 to 338.98 (C3, asserted D1); a window reaching back across the build change is rejected by the data (D5) |
| 9 Boundary inclusivity | go-lives on Mondays, the node move on Monday 15 February (W07) whole-week (C1) |
| 10 Rounding path | unrounded weekly figures, the shortfall rounded once to 10 GPUs (prompt; policy section 5) |
| 11 Tie-break | none needed: Docs leads Code by 39.5 GPUs under the golden and by at least 38 under every defensible variant |
| 12 Maturity and censoring | none: the forward window holds no partial periods; the tenant's first fortnight (ramp) sits inside the validation and moves its per-call cost by nothing |
| 13 Order of operations | sum the busiest hour's work, then convert, then subtract, then the max: linear until the max, which is W13 on every route (C1) |
| 14 Row order | none of the computation depends on file order: sums, least-squares fits and maxima only |
| 15 Duplicate resolution | the rollup has one row per pool-hour and the ledger one row per contract (asserted, X14) |
| 16 Identity normalisation | pools named identically in the rollup, plan and intake; the tenant's organisation id in billing matches the ledger's account id (asserted, X14) |
| 17 Netting against gross | a pool's surplus nets nothing elsewhere: each pool's shortfall is its own (policy section 5) |
| 18 Dimensional units | the Voice intake in requests per second at the busiest hour (times 3,600), the others in thousands per busiest hour; GPU-seconds throughout; Voice is far from the call either way |
| 19 Code and status semantics | the ledger's status (Signed, "Early access, ends 18 Dec 2026", "Proposal sent") and tier codes resolve through the tier sheet; never the stump (counting the early-access agreement stays in the bin, SF7) |
| 20 Integerisation | GPUs compared unrounded; nodes of eight only in the allocation, already integral |
| 21 Clause scope | the 70 per cent applies to every pool and every week (policy section 2) |
| 22 Forward window contents | the intake (busiest-hour requests per week per pool), the ledger (contracts, tiers, go-lives) and the fleet plan (allocations per week) cover every Q1 week; the cost of report calls is the one quantity the analyst forecasts |

## Literal reader

Executing the prompt and the policy word for word: the six pools' thirteen weekly requirements are the intake's
busiest-hour traffic and the contracts at their contracted peaks from the go-live Mondays at tier limits, carried at
2,520 busy GPU-seconds per GPU, less the fleet plan's allocation that week, the largest weekly shortfall per pool
compared, the product teams' requests converted at the close-out's GPU-seconds per request (policy s3). Silent: how a
report call converts into busy GPU-seconds. Every option for that conversion is priced on the ladder; every conversion
files the same Code figure and differs only on Docs; the one that also predicts the early-access tenant's GPU time on
its own days (R4) is the golden, and the easy answer (Code) comes from an easy conversion on the same literal estimand
(the filed per-request basis carried over to report calls), never from another reading (SF1 to SF15).

## Oracles

- The Q3 close-out (per-pool GPU-hours, requests and GPU-seconds per request): true on every rung, since Q3 carried no
  report traffic; it confirms R0 for Docs' interactive traffic and nothing about report calls. Ties on every basis.
- The Batch pool's lc2 hours: confirm lc2's prompt and completion rates on traffic that reuses nothing; blind to report
  calls (no report traffic runs on it) and to whether a report's calls share a pack. Not an oracle for the call.
- The early-access tenant (billing rows for its organisation, the rollup's docs-prod hours since 5 October): ties only
  under a computed-prompt model with every call computing its own pack, by design the out-of-sample check the forecast
  is chosen on (the caller's brief and the client's "testing it only on data it was not built on"). It is not an answer
  key for the figure: its calls are one tier (RS-6) with one prompt-to-completion mix, so it fixes the per-call cost of
  such calls and cannot separate the prompt and completion rates the RM-8 and RL-12 tiers need (asserted: a two-rate fit
  on the tenant's days alone is ill-conditioned, its rates off by more than half), and nothing ships its excess, which
  must be built from billing and the rollup across the October clock change.
- Billing totals: reconcile with the rollup's docs-prod requests on Amsterdam days (asserted, X2); arbitrate nothing.
- **The tenant check's precision, stated honestly.** The tenant's excess is a residual: Docs' busy time on its days
  less Docs' own requests at the Q3 rate, about 1 per cent of Docs' busy time a day since the tenant runs at its
  contract's size. Over the 43 days lc2's rates predict 0.994 of it at the exact Q3 rate, 0.997 at the close-out's
  four-decimal 1.6297 (0.996 on UTC days); Docs' rate per request predicts 0.219, Docs' own two-rate fit 0.543, a pack
  shared per report 0.452. A one-scalar rescale of lc2's rates to the tenant files 339.6 to 340.4 (O8). The write-up
  states the bound that holds on every basis (2 per cent, F1b, V14).
- **Sessions.** Billing bills the report service one session per report (six calls); the gateway's `sessions_new` in
  the rollup counts one serving session per call, so on the tenant's days the rollup's Docs sessions exceed billing's
  app and API sessions by the tenant's calls (O6, V17). The shared-pack reading of billing (R3c) is refuted two ways:
  that reconciliation, and the tenant's excess.

## Ask sheet

**Main call's declared row population:** the rollup's docs-prod and batch-prod rows (hour, pool, model, busy
GPU-seconds, requests, new sessions, prompt and completion tokens), the close-out's per-pool table, the Q1 intake, the
Q1 fleet plan, the commitments ledger and its tier sheet, the early-access tenant's billing rows, the policy. Device and
hazard rows in it: 0 (asserted: the call recomputed with every ask file deleted and the rollup's gpus_in_service and
TTFT columns blanked is unchanged to the GPU; the call reads no other pool's hours).

**Ask A. For each pool, the GPU-hours its GPUs were out of service in November 2026 and the longest any one of its
nodes stayed out** (12 figures: GPU-hours to the nearest 10, hours to one decimal), with the chart.
- H18 home: an audit trail of the allocations the call consumes, what an allocated GPU actually delivered in the last
  full month; the call compares requirements with the plan and reads no maintenance record.
- Use: the workbook's out-of-service table and `pool_out_of_service_nov2026.png`.
- Basis (filed in the stopgap policy's section 6, Reporting with the assignment; until the 10-31 reship in the capacity desk's notes): "Out of service: a node's GPUs are out of
  service from the node's cordon until its uncordon. A node cordoned again while it is cordoned is out once. Hours fall
  in the month (UTC) they are spent in, and go to the pool the node belonged to at the time."
- Golden: chat-prod 3,630 and 57.4; code-prod 1,110 and 33.7; agents-prod 1,470 and 57.0; docs-prod 1,260 and 57.1;
  batch-prod 810 and 56.0; voice-prod 1,250 and 55.9 (every figure at least a quarter bin from an edge, A1 and A2).
  Every pool's longest stay is a weekend failure (Saturday night, Code's Sunday night) completed by hand on Monday
  morning, so both console devices move every longest figure (A5, A5b).
- Primary A1 (D4 and D7, an uncordon under another action and key): when an automated driver upgrade fails, fleetctl
  leaves the node cordoned and its job open; the engineer who repairs it the next working morning completes the job
  from the ops console, which logs `fleetctl.job.complete` against the job id (detail: "completed by hand; ran
  remaining step: uncordon <node>") in its own audit export, not a fleetctl uncordon step and not a `node.uncordon`.
  Every pool has at least two console-closed stays in November (A8). Read by action name, each of those stays runs on
  to the node's next cordon or the export's end. Fair: the console row names the node and the
  step it ran, and the rollup's `gpus_in_service` shows the node back at that hour. Silent: the job log is complete for
  every step fleetctl ran, and no shipped sentence links the console to the job log (A9).
- Secondary A2 (D4, a channel): engineers' hardware cordons and uncordons are console-only (`node.cordon`,
  `node.uncordon`), absent from the job log.
- Hazards: HA1 the rollup's gpus_in_service is a sample at the hour's close (short cordons never show); HA2 the console
  export's times are Amsterdam local time (CET in November) under a header that says so, the job log's UTC with a Z;
  HA3 stays across 31 October and 30 November (clipped to November; no pool's longest moves whichever way a crossing
  stay is read, V20); HA4 four Agents nodes moved to Chat on 16 November (the inventory's dated membership); HA5 19
  re-cordons of a node already cordoned (a drain that failed and was retried).
- Stops (measured, `checks.py` A3 to A7): the job log alone misses 12 of 12, and with unpaired cordons dropped 12 of
  12; the console's times read as UTC miss 12 (every longest stay an hour long, every GPU-hour figure); the
  hand-completed jobs missed (both logs, times converted, dated membership, cordon and uncordon by action name) miss
  12; today's pool for every hour misses 2 (Chat and Agents GPU-hours); the rollup's samples miss all six GPU-hour
  figures and give no stay length.
- Span: the job log, the console export, the fleet inventory, the rollup, the stopgap policy (5 files, 11 columns).
- Realism: maintenance automation logs its own steps and an ops console its own actions; an engineer who rescues a
  failed upgrade finishes the job from the console.

**Ask B. For each of the stopgap's four racks, how many of its GPUs passed acceptance at the 4 December review, and any
of its nodes held back** (4 counts in whole GPUs and the held-back nodes).
- H18 home: a component of the call's case, what the chosen pool actually receives on 4 January; the policy assigns
  the cluster whole, so acceptance moves no shortfall.
- Use: the workbook's acceptance table.
- Basis (`lease_schedule3_acceptance.pdf`, section 3.2): "A node passes acceptance when each of its eight GPUs has
  passed burn-in and the node's eight-GPU all-reduce has reached 360 GB/s bus bandwidth on its last run. A node that
  does not is held back, and none of its GPUs counts as accepted." and "Burn-in counts on the GPU fitted at the review".
- Golden: R11 48 (held nx7-2638), R12 40 (nx7-2653, nx7-2654), R13 48 (nx7-2662), R14 64 (nx7-2645); 200 of 240.
- Units, filed in the tool's own voice: the provider's fabric harness moved from nm-fabcheck 3.8.4 to 4.0.1 on 1
  December, and the export carries each run's `harness` and `bw_unit` (GB/s before, Gbit/s from 1 December), so the
  Gbit/s runs are determinate from the file (B5); reading the figures without the unit column is a stop (B2), not a
  device.
- Primary B4 (D2, the latest run, not the highest number): the new harness numbers each node's runs from 1 again. Two
  nodes ran below the line under 3.8.4 and cleared under 4.0.1: nx7-2649 (R12, two runs on 30 November, clear on 1
  December) and nx7-2673 (R14, two runs on 25 November, clear on 2 December after a transceiver swap). Each one's last
  run passes, while its highest run number is a November failure. Fair: every run carries its start and finish time.
  Silent: no note says the numbering restarts (B6); two nodes of thirty show it (B7).
- Primary B9 (D8, a clock against a filed cutoff): Schedule 3.3 holds the review at 14:00 on 4 December, Amsterdam
  time; the export, received that day, carries two held nodes' re-runs after repair, nx7-2638 (R11) and nx7-2662
  (R13), finished at 13:49 and 13:55 UTC, after the review and before 14:00 UTC, both above the line. Fair: the
  export's times are UTC by name and the schedule's are Amsterdam's by text (B10). Silent: nothing marks the two runs.
- Secondary B3 (D7, an attribute at the wrong vintage): the provider re-racked three nodes before the review (two from
  R11 to R14, one from R12 to R11); the burn-in results carry each node's rack at test time, the handover inventory of
  4 December its rack at the review. Silent: no ticket or note names the move (B6).
- Hazards: HB1 two GPUs swapped under RMA and burned in again (keyed by node and slot the same result, B8); HB2 a GPU
  that failed burn-in once and passed on rerun.
- Stops (measured, B2 to B4, B9): the unit column ignored misses all four racks (56, 56, 56, 72); racks as the burn-in
  results record them miss R12 and R14 (48, 48, 48, 56); the highest run number read as the last run misses R12 and
  R14 (32 and 56); the review ignored, or its 14:00 read as UTC, misses R11 and R13 (56 and 56).
- Span: the burn-in results, the fabric results, the handover inventory, the acceptance schedule (4 files, 13 columns).
- Realism: a test harness release that changes a reported unit and restarts its run counter, a provider that re-runs
  repaired nodes on review day and sends the export afterwards, and a provider that re-racks nodes before handover are
  all ordinary.

**The chart** (`pool_out_of_service_nov2026.png`): each pool's November GPU-hours out of service, one bar per pool,
each labelled with its value at the bar's end, titled with the pool that lost the most; graded on its content (Ask A's
six GPU-hour figures) and its parts.

**Hazard table.**

| Hazard | Asks moved | Per-ask delta |
|---|---|---|
| Clocks (job log UTC with Z, console local time, fabric runs UTC against the review's Amsterdam 14:00) | A, B | A: every figure with the console read as UTC; B: R11 and R13 with the review read as UTC |
| Identity (dated pool membership, re-racked nodes, swapped GPUs) | A, B | A: Chat and Agents GPU-hours; B: R12 and R14 |
| Sampling and units (end-of-hour samples; the unit column from 1 December) | A, B | A: four pools' GPU-hours; B: all four racks if the unit column is ignored |
| Versions (the harness release restarting its run numbers) | B | B: R12 and R14 |

**Referee.** The policy's section 6 basis and the console export (Ask A); the acceptance schedule and the handover
inventory (Ask B); neither hands over a level.

**Cracker sheet** (the cracker landed the call, ran the hygiene battery, executed every filed rule and matched every
control):

| Ask figures | The cracker's route | Device that holds | Verdict |
|---|---|---|---|
| A, six pools' November GPU-hours out of service | both logs, console times converted, dated membership, the basis executed on cordon and uncordon actions | A1 the hand-completed jobs' uncordons under `fleetctl.job.complete` | miss |
| A, six pools' longest stay out | the same | A1: every pool's longest is a hand-completed weekend stay, so all six miss however a stay running past 30 November is read | miss |
| B, four racks' accepted GPUs and the held-back nodes | the schedule executed with the unit column read, GPU serials fitted, racks from the handover inventory, the last run taken as the highest run number, every run in the export | B4 the renumbered runs (R12, R14) and B9 the runs after the 14:00 review (R11, R13) | miss |

**Mirror sheet.** The mirror stops at R0 or R2c on the main call and meets the same devices; it keeps the chart's parts
and no Ask A or B figure unless it cracks a device.

Mirror leakage: 9.5 per cent of ask weight (the chart's layout and labels, 2 of 21 ask criteria; no Ask A or Ask B figure).

Pair ceiling: 33.7 (the cracker at 50.2, 38 + 7 + 55 x 2/21, keeping the chart's layout and labels and no ask figure; the mirror at 17.2, 5 + 7 + 55 x 2/21).

Measured by: `generator/ceiling.py` on the cut pack (Ask A without the hand-completed jobs' uncordons, Ask B on the highest run number with every run read).
Rerun from the generated rubric at stage 4.

## Build record

- **Stage 3, round 3, 2026-10-17.** `generator/build.py`: 112 checks, 0 FAIL; `verify.py` (pandas, its own code path,
  the close-out's rates read from the PDF) 30 checks, 0 FAIL; two consecutive builds byte-identical (target, golden,
  figures, submission); `figures_check.py` 0 absent; `leak.py --asof 2026-12-07` REVIEW (answered below);
  `guard.py surface` and `heart` WARN only; `precut.py` exit 0; `voice-check.py` PASS; container audit clean.
- **Stage 4, round 1 (the coordinator's run).** Judge: DETERMINISTIC, FIX_NOW (`determinism_check_report_round1.md`):
  every committed answer reproduced; finding 1, the rate for ordinary traffic unpinned (each pool's busiest Q3 hour
  gives Code 344.5 against Docs 341.8); finding 2, the Gbit/s switch inferable but unstated. Rule 3 audit: PASS, with
  P(one) about 0.25 to 0.3 and P(both) about 0.10 to 0.15, billing's session per call a field reading of the decisive
  fact, the close-out's lc2 sentence pointing at the fit cohort, and the all-year Batch fit with an intercept at 344.2.
  Leak reader: no leak.
- **Round 2 fixes, one generator pass.** Policy s3 files the conversion of the product teams' requests (the latest
  close-out's GPU-seconds per request) and nothing about report calls (D3, SF15); the golden now costs the intake at the
  close-out's printed rates (four decimals from round 3, 338.8; no graded figure moved). Billing bills the report service one session per
  report; the gateway's sessions show one per call (O5, O6). The close-out's sentence on Docs and Batch serving lc2 is
  gone; the build shows only in the rollup's model column. lc1's rates now sit 45 and 51 per cent above lc2's, so the
  all-year fits land at 371.2 and 353.9 and the residuals by build reject them (D5, D6). The fabric export states its
  harness and unit on every run, so the Gbit/s runs are determinate; the silent devices on Ask B are now the new
  harness numbering runs from 1 again (R12, R14: B4, B7) and two repaired nodes re-run after the 14:00 Amsterdam review
  that Schedule 3.3 now files (R11, R13: B9, B10). Ask A's devices were spread to every row: Code, Batch and Voice each
  gained a weekend-night upgrade wave whose first job failed, so every pool's longest November stay is a hand-completed
  failure and the console-time and hand-completion devices each move all twelve figures (A5, A5b). Ask A's figures
  moved (chat-prod 3,630 and 57.4, code-prod 1,110 and 33.7, agents-prod 1,470 and 57.0, docs-prod 1,260 and 57.1,
  batch-prod 810 and 56.0, voice-prod 1,250 and 55.9); Ask B's and the call's did not.
- **Strength, re-estimated.** P(Docs): a strong solver must refuse the filed per-request basis for report calls, refuse
  billing's six calls a session as a shared pack, and find the no-reuse lc2 cohort through the model column alone,
  about 0.3. P(340 given Docs): the lc2-only two-rate fit against the blended (367.0, 391.3) and pooled (371.2, 353.9)
  routes, about 0.55. P(one) about 0.15 to 0.2; P(both), with the auditor's correlation between two strong responses,
  about 0.06 to 0.09. The optional Batch template reuse was not added.
- **Pair ceiling, two ways.** On the cracker-sheet basis (each device row missed by the cracker) it stays 33.5. Taking
  a strong solver's chance of handling each device instead (hand completions 0.35, console time 0.85, dated membership
  0.85, the review's clock 0.4, the renumbered runs 0.5), it keeps about 39 per cent of the ask weight (9.4 of 24
  criteria): about 34 for a pair both on Code, about 50 in a draw where one of the two lands the call, about 38.5
  averaged over the draws (one of two landing about 0.3). Making
  the Gbit/s runs determinate cost Ask B its strongest silent device; the spread devices win most of it back.
- **Round 3, the tenant check (rule written before the ratio was read).** The judge's soft spot: priced at the
  close-out's printed 1.630, the tenant's whole-period excess sits 5 per cent under lc2's prediction, and a one-scalar
  rescale (0.952) files 327. Diagnosis: the excess is a residual of about 0.3 per cent of Docs' busy time on the
  tenant's days, so (a) the three-decimal rounding of Docs' rate (1.630 against 1.6297) removes about 7 per cent of it,
  and (b) Docs' hourly busy-time noise gives the summed excess a standard error of about 90 thousand GPU-seconds, 4 per
  cent of a 2.2 million GPU-second signal. Neither is structural to the cost model. Rule, fixed before any ratio is
  computed: the close-out prints GPU-seconds per request to four decimals, as an analyst prints a rate near one; and
  the early-access tenant ran at the size of the contract it converted to, its busiest hour in a full week at
  RC-2026-031's contracted 400 reports an hour (base 339 reports an hour against the hour shape's 1.18 peak), the
  ramp, hours, pause, call sizes and every random draw unchanged, its early-access agreement contracted at 400. The
  ratio that rule produces is the one shipped, inside or outside 1.5 per cent; no seed is searched.
- **Round 3, what the rule produced.** lc2's rates predict 0.997 of the tenant's whole-period excess at the
  close-out's 1.6297 (0.996 on UTC days, 0.994 at the exact rate): inside 1.5 per cent on every basis (O7). A
  one-scalar rescale to the tenant files 339.6 to 340.4, the 340 bin (O8, V14b); Docs' rate per request still predicts
  0.219 and Docs' own two-rate fit 0.543 (O9). The tenant's calls (894,042), its excess and the write-up's bound (2 per
  cent) moved; the call, every critical component, both asks' answers and every rung's pool did not.
- **Ship, 2026-10-17.** The targeted re-check of the tenant figures HOLDS (`determinism_check_report_tenant_recheck.md`:
  Docs 338.8 against Code 299.3, ratio 0.9967, rescale 339.6, the bin holding for rescales of about 0.985 to 1.025).
  Write-up only, then one plain ledger note: step 4 states its bound with the bases it holds on (Amsterdam or UTC
  days, the close-out's or the exact rate, 2 per cent against a worst 0.65), block 1 argues the shared-pack rival from
  the gateway's sessions and the tenant's busy time, not from a share of the prompt nothing files, and the commitments
  ledger's Notes sheet says Q1 committed reports are each contract's minimum (the tenant's 149,007 pilot reports
  against RC-2026-031's 148,700). checks 113, verify 30, three builds with one target.zip hash (bfa825af).
- **Leak REVIEW lines, each harmless.** `capacity_desk_notes.md` "the model": the rollup's column note (the model
  build a pool served). `capacity_closeout_2026Q3.pdf` 57.4: Batch's September busy GPU-hours in thousands, a
  coincidence with Chat's longest stay in hours, another quantity in another unit; 57.1 likewise (Batch's August busy
  GPU-hours in thousands against Docs' longest stay). The policy carrying the call's
  words: the policy defines the stopgap, the six pools and the shortfall for every pool alike and ranks nothing. The
  close-out, desk notes, schedule and policy carrying stump-paragraph terms (prompt, tokens, session, report, capacity,
  computed): column names and filed estimand words; none names reuse, computed tokens or how a report call's GPU work
  is priced (R1b, R1c). Dates after the as-of in the fleet plan (the 15 February move) and the ledger (go-lives in Q1):
  forward-dated by nature, the plan and the contracts are about Q1.
- **Surface and heart.** `surface` promotes task151 on card axes only (gap population, G1, Gate G forecasting, the
  same domain and objective), text surface 0.075; differentiated on the card. `heart`: nearest 0.05, WARN for the
  question form (`which`, taken from the pick).
- **Invented names (H21).** Slenk, Noordermeer Compute and the twelve ledger accounts searched on 2026-10-17: no firm
  trades under any of them. Noordermeer is a real hamlet (geography, texture); "Kroes" appears in a real notary's name
  (Diemer Notariaat Kroes+ Mokkum), a common surname, neither name contains the other. The 160 billing organisations
  are surname-and-trade compounds drawn by the generator, not searched one by one. `nm-fabcheck` is the provider's own
  tool name.
- **Golden realism.** The workbook's sheets carry finding titles, a basis block from the pack's own conventions,
  precision by quantity, frozen headers and a cluster total that ties to the rack rows; the chart is one hue, labelled
  bars, units on the axis and a finding title. No figure moved (checks F3 to F5, verify V24 to V26).
- **Residual weaknesses, for the reader and the judge.** The early-access check is a residual of under half a per cent
  of Docs' busy time a day (see `## Oracles`); its level moves to 1.05 on the close-out's printed rate, its separation
  of the costings does not. Ask B's unit is now filed, so B holds through the renumbered runs (R14) and the burn-in
  racks (R12, R14) only. The final margin is 1.13x, under §6.2's 1.2x, held by Code's figure being independent of
  every costing.

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
- Prototype fit on every hour tagged lc2 (rates 0.0002501 and 0.001815): the rollout hours of 11 and 12 May mixed both
  builds; the rollup now tags them with both builds and the fit reads the lc2 tag alone, recovering 0.248 and 1.85.
- The golden at 382.7 after the organisation names moved the random stream: the Docs intake path was re-set before any
  rung was read (W13 1,152.6 thousand), golden 338.8; no seed was searched.
- Voice's month-crossing stay as its longest: shortened to 9.2 hours so no pool's longest turns on how a crossing stay
  is read (V20).
- Hardware cordons landing inside upgrade stays: drawn only on nodes with no stay within three hours, so the union rule
  is exercised by the automation's own re-cordons and never by accident.
- Ask A figures centred to exact round values: replaced by a draw within two GPU-hours of the bin centre and a longest
  stay within 0.015 hours of the grid.
- The ledger note "one section at a time": read as sequential calls, which they are not; now "section by section".
- The close-out's closing line on September's busiest hours above 70 per cent: a claim no check computed; replaced by
  the intake and plan dates.
- The early-access status "Ended 18 Dec 2026" in an export of 4 December: a date after the export; now "Early access,
  ends 18 Dec 2026".
- Model build tags dated 2026.01 to 2026.03 served from 1 January 2026: anachronistic; now 2025 builds.
- `fleet_plan_2027Q1_v3.xlsx`: leak sweep 1 (`_v3`); renamed `fleet_plan_2027Q1.xlsx`, the issue on its About sheet.
- `trt-llm` in the spec register: leak sweep 2 (`llm`); now `tensorrt_llm`, the package's own name.
- Console detail "marked complete by hand; remaining step: uncordon": reads as the step still remaining, a fork on
  Ask A; now "completed by hand; ran remaining step: uncordon".
- Write-up claim "within 2 per cent" on the tenant: true at the exact rate (1.9) but 5.0 at the close-out's printed
  1.630; the bound is now derived over day and rate bases with half a point of margin (6 per cent).
- The close-out's Table 1 on a portrait page: headers broken mid-word; set landscape.
- Round 1 left the rate for the product teams' requests unfiled: each pool's single busiest Q3 hour gave Code 344.5
  against Docs 341.8 (judge finding 1); filed in policy s3 as the latest close-out's GPU-seconds per request.
- Billing's report channel with one session per call: "each call is its own session" read off a field (rule 3 audit);
  billing now counts one session per report, the gateway's sessions still one per call.
- The close-out's sentence that Docs and Batch both serve lc2: it pointed at the fit cohort; removed.
- lc1's rates 16 and 25 per cent above lc2's: the all-year Batch fit with an intercept filed 344.2, inside the bin by
  0.8; lc1 now 45 and 51 per cent above, the pooled fits at 371.2 and 353.9.
- The Gbit/s switch with no unit in the export (judge finding 2): stated by the export's own harness and unit columns;
  the silent device moved to the new harness restarting its run numbers.
- Ask B with the units filed and only the renumbered run as its silent device (R14 alone): a careful reader kept most of
  the ask; the renumbering spread to R12 and a review-day cutoff added for R11 and R13.
- Ask A with three pools' longest stays plain hardware or weekday stays: the hand-completion and console-time devices
  moved only three of six longest figures; weekend failures added for Code, Batch and Voice.
- The tenant at its early-access size (a busiest hour near 130 reports): a residual of 0.3 per cent of Docs' busy time,
  5 per cent off at the close-out's three-decimal rate, so a calibrating analyst filed 330 (re-judge soft spot); the
  close-out now prints four decimals and the tenant ran at its contract's 400 reports an hour, the size chosen by rule.
- Step 4's "a source pack computed once per report predicts under half": true only when the whole prompt is the pack,
  a share nothing files (0.45 at all of it, 0.72 at half); the rival is argued from sessions and the tenant's busy time.
- 2026-10-31, re-check under the 10-30 gates: `leak.py` LEAK on the capacity desk's notes (section 3: they glossed every rollup column and listed the folder). Removed. Ask A's out-of-service basis is filed as the stopgap policy's section 6, Reporting with the assignment; every other file already names its zone, and billing's day column now does too (usage_day_amsterdam); `metadata.json`'s title and subdomain narrated the step and disclosed counts and were cut. The prompt drops its counts and asks what. Every graded figure unchanged (114 checks).
