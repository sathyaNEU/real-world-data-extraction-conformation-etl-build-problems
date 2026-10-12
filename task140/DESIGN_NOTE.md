# task140: Alisio Viajes, cell C-22's batch-training guarantee for 2027 Q1 (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC11: the seed's world, decision and quantity are kept
(a compute cell's quarterly capacity review strikes the batch-training guarantee, the reservable cores left after the
firm tenants' reservations, at 5,180 machines of 96 cores and a 1.45 overcommit, 721,056 reservable cores); its
architecture (a platform levy of a quarter of each firm reservation held inside its own base, recovered as a third
from settled sister-cell ledgers, with budget ceilings binding after the fixed point) is not used, because the
decisive step there is a hidden rule recovered from certified figures. The budget ceilings stay as a filed rule on a
lower rung; the pitfall is re-found from how the cell's own storage service burns CPU on the batch tier's dataset
reads and checkpoints, so one of the reservations the guarantee is struck after rises with the guarantee itself.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task140.json`, architecture v1, registered 2026-10-12 after task139's draw landed on main; `guard.py check` WARN (`overuse.objective`, answered below), no BLOCK; `guard.py validate` clean |
| Domain / task type | `supply-chain-logistics` (house domain; data-centre capacity planning, the supply side of compute) in client domain `general-statistics-data-science`, task type `regression-classification-model-diagnostics` (forecasting): the deciding statistical object is a regression of a dependent load on its two drivers, specified and solved forward, where a summary of the load's own history files another call |
| Objective | Forecasting & Predictive Modeling: the batch guarantee for 2027 Q1 (1 January to 31 March 2027), a window not yet open, struck from a forecast of the storage service's busiest hour in that quarter, which the history pins only through its drivers |
| Shape | `other`: the guarantee and the reservations it is struck after (the firm tenants' approved total, each platform service), the slide's named parts (the split of 721,056 reservable cores, title, axis), three asks on 2026 Q3 rows the call never reads (each batch team's redone core-hours and share, 12 figures; each month's machine-hours lost to hardware faults and to planned maintenance, 6 figures; each firm tenant's Q3 charge, 11 figures), the two files: about 44 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (cores, the largest whole thousand that fits) |
| Mechanism | gap objective (decisive: the cores left after the firm reservations and the platform services carried at their own history are correctly computed, and the guarantee is scored on what the cell can carry once every batch core brings its storage load); pattern none, generators G1 (unit of value: a batch core costs the cell 1.2 reservable cores, its own and the storage behind it) then G16 (method: the storage forecast built on its drivers, not on its history); Gate G `binding_constraint` (the reservable cores bind on the batch tier and the storage it drives together); strategy `binding_constraint` (F3: the limit is shared between the guarantee and a reservation that rises with it) |
| Layer 2 family / pattern | `allocation_constraints` (a fixed-point allocation: a deduction that depends on the residual being allocated); `own:residual-tier-drives-a-dependent-reservation` (General Statistics has two library lines under the task type, influence and leave-out residuals; this build's statistical object is the specification of the dependent load on its drivers, read forward at the decision's own value) |
| Furniture | forum `line_manager_or_team` (the compute operations team publishes the guarantee to the batch teams after its own quarterly review; no formal forum), forcing event `vote_or_meeting` (the quarterly capacity review, Tuesday 15 December 2026, strikes the Q1 guarantee), organisation family `hospitality_or_tourism` (an online travel marketplace running its own data centres), role family `operations_director` (the head of compute operations runs the cells and publishes the guarantee), context artifact `capacity_report` (the cell's 2026 Q3 capacity report), calibration `none` (the ledger and the telemetry are the cell's own records, not an organ), opening `question-first`, question form `how-many` |
| Spine | `c22_usage_hourly_2025-2026.csv`, the cell monitoring export: one row per tenant per hour, the tenant's average cores in use, 1 January 2025 to 13 December 2026 (UTC), 14 tenant series; constructed |
| Deliverables | `c22_capacity_2027q1.xlsx` (the guarantee, the reservations it is struck after, the three 2026 Q3 tables), `c22_capacity_review_2027q1.pptx` (one slide: how the quarter's 721,056 reservable cores divide between the firm tenants, the platform services and batch) |
| People | drawn with `guard.py names --geo Spain --seed 140 --n 40`, keeping names the guard clears: Alejandro Baena (head of compute operations, MAD1, the requester), Raúl Echevarría (head of infrastructure, signs CS-3 and the capacity memo), María Ayala (storage platform lead), Jordana Sala (batch training platform lead), Ruy Franco (MAD1 data-centre operations manager, the operations log), Esteban Madrigal (fleet and hardware, the hardware plan and the inventory), Georgina Quirós (technology controlling, the budgets, rate card and chargeback policy), Martina Pera (SRE, operations log entries); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN on `overuse.objective` (forecasting in 6 of the last 12): the
lane is forecasting and the seed's call is a forward guarantee, and the decisive gap (objective) and Gate G
(`binding_constraint`) differ from task137, task138 and task139 (time, time, population; forecasting, forecasting,
method selection). The bans ran against task137, task138 and task139, the three builds before this one by draw key.
Two scratch draws were refused before registration: the first (context artifact `capacity_report`, forum
`line_manager_or_team`, forcing event `budget_or_appropriation`, a PNG beside the workbook) met task136 while task139 was
not yet on file; the second (`close_out_summary`, `executive_team`, role `capacity_planner`) met task139's card when it
landed. With task136 out of the window, the registered draw takes the capacity report, the requester's own team and the
review meeting; the requester is the head of compute operations (`operations_director`), the honest owner of the
guarantee, and the deliverables are a workbook and a slide (no recent build ships that pair).

**Same-puzzle and same-driver tests.** Gap objective, decisive G1, decision `quantity_figure`, Gate G
`binding_constraint`: no build in the last twelve carries the gap, the G-code and the decision together (task184 is gap
objective with G1 on a pick, Gate G decomposition; task229 is gap objective with G7 on a date, binding constraint).
Older binding-constraint quantities (task32, task64, task79, task94) differ on the driver: an annual cap tested at
quarterly resolution, an orthogonal supply ceiling, a piecewise inverse past a capacity constant, a delivery on top of
held stock; none has a deduction that grows with the quantity being decided.

**Abstraction test.** Stripped of nouns, the driver is: the residual promised to the lowest tier is struck after every
higher reservation, and one of those reservations is a dependent service whose load rises with the very tier being
promised, so the residual has to be solved together with that dependency, estimated from the dependent's own use
against its two drivers. The three nearest drivers (`guard.py check`: task32 v3 lineage 0.05, an annual cap on a
by-product binding below a tier; task98 v1 lineage 0.04, a nightly residual of demand over open stock; task230 v2
0.03, a detection step whose hit rate moves with the pool) share no latent structure, default path or correction with
it. Read by idea: task79 (conversion falls once a downstream capacity binds) is a capacity reached by the input; here
nothing saturates, the deduction scales linearly with the residual and the default never models it at all. Measured
trap 22 (a self-referencing rule solved in one pass) is the seed's family; here no rule is stated, the dependency is a
measured load, and the one-pass solve is a lower rung.

**Data-native sentence.** C-22's storage service runs a daemon on every machine in service and serves the batch
training tier's dataset reads and checkpoint writes, so its hour-by-hour use is 3.0 cores for each machine in service
plus 0.2 cores for each batch core running (asserted on the telemetry: a two-driver least-squares fit leaves residuals
of about 14 cores on a 25,000-core load, and the batch tier's pauses and the rack additions move the two drivers
apart); the 2027 Q1 guarantee more than doubles because the 580 machines of the December refresh add 80,736 reservable
cores while the firm tenants grow by 19,383, and every core it adds brings 0.2 cores of storage the storage service's
own quarterly history has never seen.

**Sources read, one line each.** `guard.py mechanisms --objective forecasting` (52 builds): a reservation driven by
the residual has no carrier; the nearest ideas are task79's capacity constant, task32's quarterly binding of an annual
cap, task64's orthogonal ceiling and task16's per-cell floors, each a limit on the quantity, none a deduction that rises
with it. `two-layer-task-design.md`: General Statistics' rule-1 swap is of the method (the regression against a generic
summary), and the house domain's swap is of the nouns; both are written under `## Three rules`.
`measured-drivers.md`: held tasks sit upstream of every graded figure and outside the solver's hypothesis space; the
storage forecast is a routine line the default path never models, and every guarantee figure inherits it. The seed's
header (FC11) for the world only.

**World.** Alisio Viajes, S.L. is an online travel marketplace (hotels, flights, packages) with its head office in
Barcelona and two data centres of its own, MAD1 at Alcobendas (Madrid) and BCN2 (Barcelona). MAD1 runs five compute
cells, C-21 to C-25, each a pool of identical 96-core machines under one scheduler. C-22 hosts eleven firm tenants
(ten product services: `search-api`, `avail-cache`, `pricing`, `booking`, `payments`, `reviews`, `reco-serve`,
`ads-listings`, `notify`, `partner-gw`; and the deadline-batch class `settle-batch`, the partner settlement and
invoicing runs), two platform services (`cell-store`, the cell's storage service; `cell-ctl`, the scheduler and the
monitoring agents) and the batch training tier (`batch-train`, run for six teams: `ranking-ml`, `pricing-ml`,
`fraud-ml`, `reco-ml`, `demand-ml`, `nlp-ml`). The Cell Capacity Standard CS-3 (rev. June 2026, signed by the head of
infrastructure) governs the quarterly review: reservable cores, firm approvals held to frozen budgets at the rate card
in force, platform services at their forecast busiest-hour use, and the batch guarantee as the largest whole thousand
of cores left, inside which batch runs. Technology controlling charges the firm tenants monthly under the 2026
chargeback policy.

As-of dates: the monitoring export runs to 13 December 2026 23:00 UTC and was pulled on 14 December; the Q1 request
window closed on 4 December; the budget freeze note is dated 27 November; the Q1 rate card took its value on
1 December; the capacity memo is dated 9 December and the hardware plan's revision 11 December (the 29 new racks in
service from 28 December 2026); the review is on Tuesday 15 December 2026; the three asks cover 2026 Q3 (1 July to
30 September, UTC), closed.

## Default path

1. Read CS-3: reservable cores are the machines in service at the start of the quarter (hardware plan) times 96
   times the quarter's overcommit (capacity memo); each firm tenant's reservation is its request held to what its
   monthly budget pays for at the rate card in force for the quarter; each platform service is reserved at the use
   forecast for its busiest hour of the quarter; the guarantee is the largest whole thousand of cores left.
2. Reservable: 5,180 machines times 96 times 1.45, 721,056 cores.
3. Firm: each tenant's Q1 request against its December 2026 monthly budget (held for Q1 by the freeze note) at
   EUR 7.42 per core-month (the rate card from 1 January 2027): `search-api`, `pricing` and `reco-serve` held to their
   budgets, the other eight at their requests; 565,683 cores.
4. Platform: each platform service's busiest hour in each of the last four quarters from the monitoring export, and
   the least-squares line through the four, one quarter on: `cell-ctl` 2,46x cores, `cell-store` 25,04x cores.
5. Guarantee: 721,056 less 565,683 less the two platform forecasts leaves 127,8xx cores; the largest whole thousand.

Ends on: 127,000 cores (the default path's guarantee; asserted in `checks.py` and recomputed by `verify.py`).
Golden: 114,000 cores: `cell-store` forecast from its drivers, 3.0 cores per machine in service and 0.2 per batch core
running (the least-squares fit of its hourly use on the cell's machines in service and the batch tier's cores), at
the 5,180 machines of Q1 and the batch tier at its own guarantee, so the storage reservation and the guarantee are
solved together (114,4xx before the whole thousand; storage 38,3xx, `cell-ctl` 2,46x).

## Stump sentence

A competent solver approves the firm requests under their frozen budgets at the Q1 rate card, forecasts each
platform service's busiest hour as the line through its last four quarters and files 127,000 cores (Ends on); the
step that lands it there is carrying the storage service forward on its own history, when its busiest hour is set by
the machines in service and the batch cores running (3.0 and 0.2 cores each), so the guarantee has to be solved
together with the storage it brings: the golden is 114,000.

## Three rules

- **Task type:** `general-statistics-data-science` / `regression-classification-model-diagnostics` (forecasting): the
  call rests on a regression of the storage service's hourly use on its two drivers (machines in service, batch cores
  running), specified on the drivers rather than on time and read forward at the guarantee being decided; the house
  domain is supply-chain-logistics (data-centre capacity planning, the supply side of compute).
- **Domain test:** the deciding quantity is the storage service's CPU per machine in service and per batch core
  running, estimated from the cell's own hourly telemetry, where the batch tier's pauses and the rack additions move
  the two drivers apart; a compute capacity planner sizes a dependent infrastructure service from the workloads that
  drive it before striking a residual guarantee, and replacing that regression with a summary of the service's own
  history (its trend, its share of the cell) files 127,000 or 124,000 instead of 114,000.
- **Swap:** "C-22 can guarantee 114,000 cores to batch training in 2027 Q1, the reservable cores left after the firm
  tenants and the platform services, the storage service reserved at 3.0 cores per machine in service and 0.2 per batch
  core" read with a hospital's nouns ("Ward 7 can promise 114 elective beds, the beds left after emergency admissions
  and support services at 3.0 per ward and 0.2 per elective bed") stops making sense: no support department occupies
  beds out of the pool it serves, and there are no reservable cores at an overcommit, machines in service or batch cores
  running for the dependency to be measured on; with the method swapped (the regression replaced by the load's own
  trend or share), the call moves to 127,000 or 124,000.
- **Layer 1:** a monitoring export in UTC beside an operations log written in Madrid local time (CEST to 25 October,
  CET after), a collector outage on 19 August 2026 leaving seven hours with no rows for any tenant, tenant ids in the
  export and the ledger against cost-centre names in the finance budget workbook (joined through the tenant directory),
  a re-sent day of export rows in March 2026, rack additions dated in the hardware plan and the machines-in-service
  series, a budget workbook with monthly columns and a freeze column, an effective-dated rate card; on the ask paths, an
  elastic training scheduler's resize log, checkpoint writes that never committed, a cluster manager that gives a
  re-imaged machine a new id, a hardware inventory carrying each asset's id history, a quota service that applies
  changes in six-hourly reconciliation runs and stopped for three days after the August power event. Each is what
  these systems write; none decides the call.
- **Layer 2:** family `allocation_constraints` on a General Statistics regression: the shortcut forecasts the storage
  service as a tenant like the others (its trend, its last quarter, its share of the cell); the expert specifies its
  use on its drivers and reads the forecast at the decision's own value, solving the guarantee and the storage
  reservation together.
- **Decisive step:** not a plant (the storage service, its daemons on every machine and its load from the batch
  tier's reads and checkpoints are how a cell's storage works, and nothing in the pack was placed to be caught), not a
  field read (every column is read the same on the default path: cores in use, machines in service, reservations), not
  a stated rule (CS-3 says a platform service is reserved at its forecast busiest-hour use and leaves the forecast to
  the analyst; no sentence names a driver, a ratio or the batch tier in it).
- **Analyst test:** a strong analyst who approves every firm request under its frozen budget at the Q1 rate card, takes
  the hardware plan's 5,180 machines at the 1.45 overcommit and forecasts the platform services' busiest hours from
  their own last four quarters files 127,000 cores; with the last quarter's busiest hour 128,000, with storage scaled to
  the 5,180 machines 124,000, and with the batch dependency applied once at the default's guarantee 111,000; only the
  storage reservation solved together with the guarantee gives 114,000.
- **Estimand:** CS-3 sections 2 to 5 (reservable cores, firm approvals, platform services at the use forecast for
  their busiest hour of the quarter, the guarantee as the largest whole thousand of cores the reservable cores leave,
  batch running inside it) with the prompt's question (the first quarter of 2027); CS-3 is the filed standard, the
  capacity memo and the hardware plan carry the quarter's overcommit and machines.
- **No decoy:** no memo, draft, briefing or stakeholder figure gives a 2027 Q1 guarantee, a storage forecast or a
  method; the platform team's past storage reservations are history in the ledger, the Q3 capacity report covers Q3 only,
  and the batch teams' Q1 roadmap (a distractor) states demand, not a guarantee.
- **No certified replay:** the storage dependency is measured on the hourly telemetry (two drivers, about 16,000 hours,
  residuals of about 14 cores); no certified or published figure has to be reproduced to find it, and the past
  guarantees in the ledger are the reviews' outcomes, which the golden never reads.
- **Lesson:** a deduction that rises with the quantity being decided has to be modelled on its drivers and solved
  together with that quantity; carrying it forward on its own history is safe only while the decision's own value
  stands still. No build on file has a residual whose size drives one of its own deductions (nearest: task79's
  capacity constant, task32's annual cap).

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 every firm request taken whole (no budget hold) | CS-3 section 3 names the hold | the budget workbook's freeze column | no | no | no | yes | readable |
| R0 every platform service on the line through its last four busiest hours (the default path) | no | no | yes (a tenant's busiest hour trended) | no | no | yes | readable |
| R0b the last quarter's busiest hour carried | no | no | yes | no | no | yes | readable |
| R1 `cell-store` scaled with the cell (per machine, or its share of the reservable cores) | no | the machines-in-service series | yes (overhead scales with the fleet) | no | no | yes | readable |
| R2 `cell-store` on batch alone (no machine term), or held at Q4's per-machine level with the batch term added | no | the batch series beside it | no | no | no | no | readable |
| R2b the batch dependency applied once, at R0's guarantee | no | no | no | no | no | yes (once the dependency is seen, a single substitution) | readable |
| R3 (decisive) `cell-store` specified on machines in service and batch cores running from the hourly telemetry, reserved at its forecast busiest hour with the batch tier at its own guarantee, and the guarantee and the storage reservation solved together | no sentence names a driver, the batch tier's load on storage, a ratio or a joint solve; CS-3 section 4 says only "the use forecast for its busiest hour of the quarter" | no column holds storage per core, a driver or a share; the export is one series per tenant | no: the reflexes are R0 to R1, each files its own wrong guarantee | no closed record scores a forecast method: the ledger's past platform reservations are the platform team's own sizings, and no past quarter's guarantee doubled | no | no: a two-driver fit read at the decision's own value, a linear system in the unknown guarantee | silent |

The decisive rung is silent because the storage service is a routine line: CS-3 files it beside the scheduler, the
ledger lists it like any tenant, and the default path forecasts it with the same line it would use on any series. The
pack never says what drives it; the telemetry does, to an analyst who asks.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move the call or its figures, or shown to converge). CS-3 is the Cell Capacity
Standard; CM the capacity memo; HP the hardware plan.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "cores" | reservable cores, the unit every reservation and the guarantee is struck in | physical cores (the 497,280 behind them) | moves the call | CS-3 section 2 (reservable cores are machines times 96 times the overcommit; reservations and the guarantee are in reservable cores) |
| SF2 | "guarantee" | the largest whole thousand of cores the reservable cores leave after the firm and platform reservations | the remainder to the nearest thousand | same call when the remainder sits mid-thousand (asserted: 114,4xx) | CS-3 section 5 |
| SF3 | "the first quarter of 2027" | 1 January to 31 March 2027 | (none) | n/a | the prompt; CS-3 section 1 (quarters are calendar quarters) |
| SF4 | the quarter's machines | 5,180 in service from 28 December 2026 | the 4,600 in service on the pull date; installed less a repair allowance | 4,600 moves the call far; a repair allowance of the cell's 2026 average (about 10 machines) moves it by under 30 cores (asserted, same call) | CS-3 section 2 (the hardware plan's machines in service at the start of the quarter); HP's Q1 sheet |
| SF5 | the quarter's overcommit | 1.45 | (none) | n/a | CM |
| SF6 | a firm tenant's request | the request in the Q1 window, one per tenant | (none: one row per tenant) | n/a | the request file (asserted: eleven tenants, one row each) |
| SF7 | the budget a request is held to | the tenant's December 2026 monthly budget, held for Q1 by the freeze note | the 2026 average month; the Q4 total over three | the 2026 average lifts two caps (moves the call); the Q4 total over three converges (Q4's months are equal under the freeze, asserted) | CS-3 section 3 ("its monthly budget"); the finance freeze note (Q1 2027 months held at December 2026) |
| SF8 | the rate card in force for the quarter | EUR 7.42 per core-month, effective 1 January 2027 | EUR 7.81 (from 1 September 2026) | moves two caps and the call | CS-3 section 3 ("in force for the quarter"); the rate card's effective dates |
| SF9 | what a budget pays for | the whole cores the monthly budget buys at the rate (rounded down) | rounded to the nearest core | converges (asserted: no budget over rate sits within a core of a half) | CS-3 section 3 ("what its monthly budget pays for") |
| SF10 | the platform services | `cell-store` and `cell-ctl` | (none) | n/a | the tenant directory (class `platform`); CS-3 section 4 |
| SF11 | a service's use in an hour | the export's average cores in use over the hour | (none) | n/a | the dictionary |
| SF12 | "its busiest hour of the quarter" | the hour of the quarter with the highest average use | the 99th percentile hour | the 99th percentile moves `cell-store` by under 60 cores and the call not at all (asserted) | CS-3 section 4 |
| SF13 | the use forecast for `cell-store` | its use at the quarter's busiest hour from its drivers, with the batch tier at its own guarantee (R3) | its trend (R0), last value (R0b), share of the cell (R1), batch alone (R2), one pass (R2b) | each files its own guarantee (Ladder) | a method row, not a reading: CS-3 section 4 asks for a forecast and section 5 runs batch inside its guarantee, so the busiest hour comes when batch fills it (asserted: in every quarter on file batch reached 99.8 per cent of its guarantee or more); each alternative is priced and refused by the telemetry's own fit |
| SF14 | the batch tier at its busiest | at its guarantee | at its historical average fill | average fill files 115,000 (asserted) | CS-3 section 5 ("batch runs inside its guarantee") and the record (batch reached its guarantee in every quarter) |
| SF15 | the busiest hour's excess over the fitted line | carried (the largest residual of the fit, about 45 cores) | none | converges (asserted: the guarantee 114,4xx with it, 114,4xx without, the storage reservation within 60 cores) | the records converge |
| SF16 | `cell-ctl`'s forecast | its busiest hour on the line through four quarters | last value; mean | converges (asserted: within 30 cores, same call) | the records converge |
| SF17 | the order of the solve | the guarantee and the storage reservation solved together, the whole thousand taken last | the whole thousand taken before the storage reservation is sized | converges (asserted) | CS-3 section 5 (the guarantee is what the reservable cores leave after the platform reservations) |
| SF18 | the remainder | unreserved (the reservable cores left after the whole-thousand guarantee) | added to batch | n/a: CS-3 section 5 makes the guarantee a whole thousand | CS-3 section 5 |
| SF19 | a tenant's budget line | the tenant's cost centre in the finance workbook, joined through the tenant directory | by tenant name | converges (asserted: every firm tenant's cost centre is unique in the workbook) | the tenant directory's `cost_centre` |
| SF20 | Ask A: a preempted run's training it had to do again | from the training state its resumption restarted from (the restored checkpoint's write start) to the preemption | from the run's own last committed checkpoint | every team's figure (S2) | the ask's own terms (what was done again); the runs file's `restore_checkpoint` |
| SF21 | Ask A: a checkpoint's training state | taken when the trainer paused at that step to write it (`write_started_utc`) | the write's commit time | every redone figure (S3, asserted) | the checkpoint file's dictionary entry ("the trainer pauses at `step` and writes; `committed_utc` is when the write became readable") |
| SF22 | Ask A: a run's cores over time | its cores at start, changed by each resize from the resize's time | its cores at start throughout | every figure (HA1) | the resize log; the dictionary ("cores held by the run from `at_utc`") |
| SF23 | Ask B: a machine that came back | the same asset back in service under any machine id | the same machine id | every figure (S1) | the ask's own terms ("machines that came back"); the inventory's id history per asset |
| SF24 | Ask B: hours in a month | the hours of an outage falling in that month | the outage's whole length in the month it began | converges (asserted: no outage on file crosses a month boundary) | the records converge |
| SF25 | Ask C: the cores a tenant holds on a day | its reservation at 00:00 UTC that day, a change counting once the quota service has applied it | from the change's request time | every tenant (S1) | the chargeback policy ("the cores a tenant holds at 00:00 UTC"); the quota service's reconciliation runs |
| SF26 | Ask C: the month's rate | the rate card's rate in force on the day | Q3's opening rate throughout | the September figures (HC1) | the chargeback policy; the rate card's effective dates |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all correctly. SF13 lists methods, not readings; each is priced and refused by the telemetry's fit. SF20 to SF26 are the
asks' readings, each closed by the ask's wording, a dictionary line or a convergence.

## Ladder

Every rung is a complete pipeline on the same literal estimand (CS-3 sections 2 to 5), computed by `checks.py` from
the pack and the default path and golden again by `verify.py`. Provisional figures from the prototype (seed 140); the
build record states the built ones.

| Rung | Firm (cores) | `cell-store` (cores) | Guarantee before the thousand | Guarantee | Against the golden |
|---|---|---|---|---|---|
| R-1 no budget hold | 572,950 | 25,04x (trend) | 120,6xx | 120,000 | +5.3 per cent |
| R0 (default) four-quarter line | 565,683 | 25,04x | 127,8xx | 127,000 | +11.4 per cent |
| R0b last quarter | 565,683 | 24,83x | 128,0xx | 128,000 | +12.3 per cent |
| R0c eight-quarter line | 565,683 | 27,3xx | 125,6xx | 125,000 | +9.6 per cent |
| R1 per machine (share of the cell) | 565,683 | 27,96x | 124,9xx | 124,000 | +8.8 per cent |
| R2 batch alone, whole history | 565,683 | 10,11x + 0.258 G | 113,4xx | 113,000 | -0.9 per cent |
| R2c batch term, Q4's per-machine level held | 565,683 | 13,75x + 0.2 G | 115,9xx | 115,000 | +0.9 per cent |
| R2b one pass at R0's guarantee | 565,683 | 41,11x | 111,7xx | 111,000 | -2.6 per cent |
| R3 golden | 565,683 | 38,3xx | 114,4xx | 114,000 | 0 |
| O1 storage per batch core at Q4's ratio | 565,683 | 0.452 G | 105,3xx | 105,000 | -7.9 per cent |

- **Separation.** The golden is bracketed: every route that does not model storage's load on batch files more
  (120,000 to 128,000), and every partial model files a neighbouring thousand on one side or the other (111,000,
  113,000, 115,000), each by one error the telemetry refutes (no machine term, the new machines' daemons left out, a
  single substitution). The asserted floors: R0 and R0b at least 10 per cent over, R1 at least 7, R-1 at least 4, R2,
  R2b and R2c off the golden's thousand by at least 450 cores before rounding.
- **Position.** The golden's unrounded guarantee sits about 440 cores above 114,000 and 560 under 115,000 across every
  converging convention (SF15, SF16: the corridor 114,4xx to 114,4xx, asserted between 250 and 750); the storage
  reservation's corridor sits inside one thousand (38,3xx to 38,3xx) and the platform total inside one (40,8xx).
- **Grid.** The four storage routes (R0, R1, R2b, R3) by the two firm readings (held, whole) and the two rate cards
  (Q1, September), 16 cells computed in `checks.py`: the golden cell alone files 114,000 (asserted); the nearest wrong
  cell is R3 with the September rate (113,000 or 115,000, asserted), two rule errors' worth away from the default.
- **Worth on the graded figures.** R3 moves the guarantee, the storage reservation, the platform total and the slide's
  batch and platform parts; the firm total and `cell-ctl` are the same on every rung.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | the eleven firm tenants with a Q1 request (one row each, asserted), the two platform services in the tenant directory, the batch tier; members not yet observed: none, CS-3 section 3 admits a firm tenant only through the Q1 request window (closed 4 December) and the directory lists no platform service without a 2026 series |
| 2 | Unit of account | reservable cores (CS-3 section 2); the guarantee in whole thousands (section 5); a tenant is a directory id |
| 3 | Attribution window | the quarter 1 January to 31 March 2027; a platform service's busiest hour within it (section 4) |
| 4 | As-of dating | machines in service at the start of the quarter per the hardware plan's 11 December revision (5,180 from 28 December); requests as filed at the window's close; budgets as frozen on 27 November; the export to 13 December 23:00 UTC |
| 5 | Version basis | the hardware plan's latest revision; one request per tenant; the rate card's row effective 1 January 2027 (SF8) |
| 6 | Denominator | the rate divides a monthly budget into cores (SF9); no rate is estimated on the call path |
| 7 | Weighting | none: the guarantee is a difference of totals; the regression weights every hour alike (a re-sent day in March 2026 doubles 24 hours and moves no coefficient beyond the fourth decimal, asserted) |
| 8 | Window length | the fit runs on every hour on file (2025 and 2026); fits on the last four quarters or on 2026 alone converge (asserted: same guarantee) |
| 9 | Boundary inclusivity | "the largest whole thousand" (floor, SF2); "held to what its budget pays for" (whole cores, rounded down, SF9); no budget over rate within a core of a whole number (asserted) |
| 10 | Rounding path | carried unrounded to the guarantee's floor; the guarantee 114,4xx sits between 250 and 750 cores inside its thousand across every converging convention (asserted, distances printed); the storage reservation, the platform total and the firm total each inside one thousand (asserted) |
| 11 | Tie-break | none needed: one guarantee, one storage reservation |
| 12 | Maturity and censoring | none on the call: the Q1 requests are closed; the export's last day (13 December) is complete to 23:00 UTC; the seven hours of 19 August with no rows are missing for every series alike and the fit never needs them (asserted: dropping or interpolating them moves nothing) |
| 13 | Order of operations | firm holds first (section 3), platform forecasts with batch at its guarantee (sections 4 and 5), the whole thousand last (SF17) |
| 14 | Row order | file order changes nothing (asserted: the export shuffled files the same coefficients and guarantee) |
| 15 | Duplicate resolution | the re-sent day of 17 March 2026 in the export (every tenant's rows for that day written twice, byte-identical): deduplicated or not, the same guarantee (asserted) |
| 16 | Identity normalisation | tenant ids in the export, the ledger and the requests; cost-centre names in the budget workbook, joined through the directory (asserted: every firm tenant matches one cost centre) |
| 17 | Netting against gross | none: reservations add; the guarantee is what is left |
| 18 | Dimensional units | cores throughout; budgets in euros per month over a rate in euros per core-month gives cores (SF9) |
| 19 | Code and status semantics | tenant classes (`firm`, `platform`, `batch`) in the directory; the export's `cores_in_use` defined in the dictionary (field semantics, never the stump) |
| 20 | Integerisation | the guarantee's whole thousand (floor); firm holds in whole cores (floor) |
| 21 | Clause scope | CS-3 section 3 applies to firm tenants, section 4 to platform services, section 5 to the batch tier (the directory's classes) |
| 22 | Forward window contents | the quarter's machines (the hardware plan), overcommit (the memo), firm requests and budgets (filed); the platform services' use, forecast from the export; the batch tier at its guarantee (section 5) |

## Literal reader

Executed word for word, the prompt and CS-3 define the guarantee as the largest whole thousand of reservable cores that
the quarter's 721,056 (section 2, the hardware plan's 5,180 machines and the memo's 1.45) leave after the firm tenants'
reservations (section 3: each Q1 request held to what its frozen December budget buys at the EUR 7.42 rate in force
from 1 January) and the platform services' reservations (section 4: each at the use forecast for its busiest hour of the
quarter), with batch running inside its guarantee (section 5). Section 4 leaves the forecast to the analyst and names
no method; the only method the records support for `cell-store` is its fit on its two drivers, because its hourly use
moves with the batch tier's cores (every batch pause, every quarterly change of the guarantee) and with the machines in
service (every rack addition), and section 5 puts the batch tier at its guarantee in the quarter's busiest hours, so the
literal forecast of `cell-store` contains the guarantee itself. Every term in the fork table resolves to one reading or
converges; the only step the text leaves open is how to forecast the platform services, which the records then settle.

## Oracles

- **None on the call path.** No file states a 2027 Q1 guarantee, a storage forecast, a driver, a ratio or a method.
  The ledger's past `cell-store` reservations are the platform team's own sizings of past quarters, each made after
  that quarter's guarantee was known; they agree with the two-driver fit (they were sized on the same load) and with
  the trend over the last four quarters (the guarantee moved little in 2026), so they score no forecast method for a
  quarter whose guarantee doubles.
- **The Q3 capacity report** reports Q3 2026's reservable cores, reservations, busiest hours and the guarantee delivered:
  inputs every rung reads alike; it states no 2027 figure.
- **The ask paths** (batch runs, checkpoints and resizes; machine events and the inventory; quota changes, the
  reconciler's runs and the chargeback policy): no rung of the call reads them, and nothing in the pack states a team's
  redone core-hours, a month's machine-hours or a tenant's Q3 charge, so none ties only under the golden.

## Ask sheet

**Main call's declared row population:** every row of `capacity_requests_2027Q1.csv`, the hardware plan's Q1 sheet,
the capacity memo, CS-3, the budget workbook's December 2026 and Q1 2027 columns, the rate card's 2027 row, the tenant
directory's platform and firm entries, the ledger's `cell-store`, `cell-ctl` and `batch-train` rows, and the
`cell-store`, `cell-ctl` and `batch-train` series of the monitoring export with the cell's machines-in-service series.
Device and hazard rows in it: 0 (asserted: the call's figures are unchanged with every ask file deleted, and no ask
reads a main row a device sits on). The asks read the batch runs, checkpoints and resize log (Ask A), the cluster
manager's machine events and the hardware inventory (Ask B), and the quota change file, the quota service's
reconciliation runs, the chargeback policy, the rate card's 2026 rows and the ledger's firm rows for 2026 Q3 (Ask C).
Each ask is a measure the cell's tiers carry that the call does not turn on; none is keyed to the call, its
construction or its figures; the three share no primary device and no primary file. No sentence in the pack
adjudicates a device: the dictionary describes each file's fields only, and the chargeback policy states what a
tenant pays for, not when a change takes effect.

**Ask A. For each batch training team, the core-hours its runs held in July to September 2026 on training they had to
do again after a preemption, and that as a share of all the core-hours its runs held** (6 teams by 2 figures, 12:
core-hours to the nearest 100, per cent to two decimals).
- H18 home: the batch tier's account of what its 2026 Q3 guarantee bought (a measure every batch team carries that the
  Q1 guarantee does not turn on); use: the batch platform lead reads it beside the new guarantee.
- Construction: each run's core-hours from its start (or 1 July) to its end, its cores changed at each resize; for each
  run that ended preempted, the resumed run that names it in `resumed_from` carries the checkpoint it restarted from
  (`restore_checkpoint`); the preempted run's core-hours from that checkpoint's `write_started_utc` to its end (or from
  its own start, when the checkpoint is an earlier run's) are training done again; summed by team.
- Primary device (D2, the record is the latest accepted, not the latest delivered): a resumption restarts from the
  newest checkpoint that passes validation on restore, and about a third of the time the preempted run's newest
  committed checkpoint fails it (missing shards) and the resumption takes the one before, or the predecessor run's
  when the preempted run committed nothing valid; the checkpoint file carries no validation status, and the restore
  point sits only on the resumed run's row. Read from each preempted run's own newest committed checkpoint, every
  team's figure is low (S2).
- Hazards: HA1 (D6) elastic runs resize (about a quarter of runs, once or twice; the runs file's `cores` is at start);
  HA2 (D2) checkpoint writes that never committed (`committed_utc` blank); HA3 (shared cause) the 19 August power event
  preempted every running run at 01:40 UTC; HA4 runs started in June (held core-hours clipped to 1 July; no redone
  training before 1 July, asserted).
- Converging readings (asserted): no run of 2026 Q3 is resumed after 30 September; every preempted run is resumed; no
  restore checkpoint is later than its preempted run's end.
- Path (5 files, 14 columns): the runs file (`run_id`, `team`, `cores`, `started_utc`, `ended_utc`, `end_state`,
  `resumed_from`, `restore_checkpoint`), the checkpoints (`checkpoint_id`, `run_id`, `write_started_utc`,
  `committed_utc`), the resize log (`run_id`, `at_utc`, `cores_after`), the tenant directory's batch teams, the
  dictionary.
- Stops (each computed and asserted in `checks.py`): S1 natural (cores at start, each preempted run's own newest
  committed checkpoint), all 12 off; S2 resizes applied, own newest committed checkpoint, all 12 off; S2b resizes
  applied, own newest write started (committed or not), all 12 off; S3 the restore point followed, the commit time
  taken as the training state, all 12 off; answer.
- Lazy delta: S1 wrong on 12 of 12.
- Realism: elastic trainers checkpoint every few hours and validate shards on restore; a scheduler records the restore
  point on the run that restored it.

**Ask B. For each month from July to September 2026, the machine-hours C-22 lost to hardware faults and to planned
maintenance on machines that came back into service** (3 months by 2 causes, 6 figures: machine-hours to the nearest
10).
- H18 home: the fleet's account of the quarter's machine availability (a measure the cell carries that the Q1
  guarantee, struck on the hardware plan's machines, does not turn on); use: the fleet lead reads it beside the
  refresh.
- Construction: each removal (cause `hw_fault` or `maintenance`) of an asset that came back, from the removal to the
  asset's next registration in the cell under any machine id (the inventory's id history), summed by cause and month.
- Primary device (D7, the true key elsewhere): the cluster manager gives a re-imaged machine a new machine id (every
  boot-disk replacement after a fault and every OS re-image in the maintenance waves), so its return registers as a new
  machine; only the hardware inventory's id history ties the new id to the asset. Matched on machine id, those outages
  never end and drop out as if retired (S1, every figure low).
- Hazards: HB1 (D1, texture) the cluster manager re-emitted 19 August's removal events after its restart
  (byte-identical rows, found by the battery); HB2 assets retired after a fault (they never come back, rightly out);
  HB3 the quarter's rack additions register as new machines in the same rows (over-cleaning by rack pairs them with
  re-imaged machines, S2).
- Converging readings (asserted): no outage crosses a month boundary; every return is under exactly one id.
- Path (3 files, 11 columns): the machine events (`machine_id`, `event`, `time_utc`, `cause`), the inventory's asset
  sheet (`asset_tag`, `row`, `rack`, `status`) and id history (`asset_tag`, `machine_id`, `from_utc`), the dictionary.
- Stops (computed and asserted): S1 natural (matched on machine id), all 6 off; S2 over-cleaned (an unmatched removal
  paired with the next registration in its rack), all 6 off; answer.
- Lazy delta: S1 wrong on 6 of 6.
- Realism: re-imaging under a new identity and an asset inventory that tracks each identity are how fleets are run.

**Ask C. What each firm tenant owes for July to September 2026 under the chargeback policy** (11 figures, euros to the
nearest 100).
- H18 home: technology controlling's quarter-end charge (a measure every firm tenant carries that the Q1 guarantee,
  struck on Q1 budgets, does not turn on); use: the tenants' Q3 charges sit beside their Q1 holds in the review.
- Construction: each tenant's reservation at 00:00 UTC on each day of the quarter (its 1 July level from the ledger plus
  every change the quota service had applied by then), times the rate in force that day divided by the days of its
  month, summed.
- Primary device (D8, a settlement time for the event time): the quota service applies a requested change at its next
  reconciliation run (00:05, 06:05, 12:05, 18:05 UTC), and ran none from 19 August 01:40 to 22 August 12:05 after the
  power event; the change file carries only the request time, the runs file the changes each run applied. From the
  request time, every tenant's charge is off (each had a change requested after 18:05 UTC or during the stop).
- Hazards: HC1 the rate card's 1 September 2026 adjustment (EUR 7.65 to EUR 7.81, seen and executed); HC2 releases and
  transfers (negative changes, a transfer as two changes on one ticket, seen); HC3 the 19 August stop (part of the
  primary's mechanism, a shared cause with Ask A's HA3 and the export's outage).
- Converging readings (asserted): no change is applied at exactly 00:00 UTC; no change's request and application
  straddle a month boundary in a way the two readings price alike (each month's figure moves under S1).
- Path (6 files, 13 columns): the ledger's 2026 Q3 firm rows (`quarter`, `tenant`, `reserved_cores`), the quota
  changes (`change_id`, `tenant`, `delta_cores`, `requested_utc`), the reconciliation runs (`run_started_utc`,
  `changes_applied`), the rate card (`effective_from`, `eur_per_core_month`), the chargeback policy, the dictionary.
- Stops (computed and asserted): S1 natural (changes from their request time), all 11 off; S2 changes from the
  application time but the September rate ignored, at least the eight tenants with a September change off; answer.
- Lazy delta: S1 wrong on 11 of 11.
- Realism: quota systems reconcile on a schedule, and a cell-local controller that stops in an incident leaves requests
  queued.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 elastic resizes | the training scheduler | Ask A | every team, if ignored |
| HA2 uncommitted writes | trainers preempted mid-write | Ask A | every redone figure (S2b) |
| HA3, HC3 the 19 August power event | the hall 2 UPS transfer fault | Asks A and C (and the export's seven missing hours, neutral) | Ask A every team (a pause preempting every run), Ask C the changes queued to 22 August |
| HB1 re-emitted removals | the cluster manager's restart on 19 August | Ask B, loud | the August figures, if not deduplicated |
| HB3 rack additions | the 2026 Q3 racks | Ask B | every figure under S2 |
| HC1 September rate | the energy adjustment | Ask C | every September day, if ignored |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker filed the golden guarantee, ran the hygiene battery (keys unique, exact duplicates,
every join matched or explained, no fan-out, counts that tie) and executed every filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 6 redone core-hour figures | resizes applied; each preempted run's training redone from its own newest committed checkpoint | the resumption's restore point, on the resumed run's row, is often an earlier checkpoint | miss |
| Ask A, 6 shares | the same over each team's held core-hours | the same | miss |
| Ask B, 6 machine-hour figures | removals matched to registrations on machine id, duplicates removed | a re-imaged machine returns under a new id, tied to its asset only in the inventory | miss |
| Ask C, 11 charges | daily holdings from the ledger and the change file at request time, the rate by effective date | a change takes effect at the reconciliation run that applied it | miss |
| The slide and the guarantee's figures (recommendation block, not asks) | from the call | carried by the main call, scored with it | outside |

The mirror sheet (the same response stopped at R0) differs from the cracker sheet only on the recommendation criteria,
so no ask is coupled to the call.

Mirror leakage: 9 per cent of the ask weight (method credit on the ask paths, no figure; allows for one Ask B figure a
device moves by less than its bin, which the build asserts against).

**Pair arithmetic.** Planning weights 38 recommendation (the guarantee, the storage reservation, the platform total,
the firm total, the slide's parts), 7 instruction following (the two files, the slide's title and axis), 55 asks over
29 figures. The cracker keeps about 9 per cent of the ask weight: C = 38 + 7 + 5.0 = 50.0. The mirror (R0) keeps the
firm total and the slide's firm part, r about 7, and the same 5.0: S = 7 + 7 + 5.0 = 19.0.

Pair ceiling: 34.5

If a strong response cracks Ask C (11 of 29 ask figures, about 21 of 55 points), the cracker rises to about 66 and the
pair to about 42.5; Ask C's device is the one to watch at the leak read. Recomputed from the generated rubric when it
exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| CS-3 sections 1 to 5 | 1, the standard signed by the head of infrastructure | quarters, reservable cores, firm holds to frozen budgets at the rate in force, platform services at their forecast busiest-hour use, the guarantee as the largest whole thousand left, batch inside its guarantee | how a platform service is forecast, any driver of storage, a 2027 figure |
| The capacity memo | 2 | the quarter's overcommit (1.45) and the machines from the hardware plan | storage, the batch tier's load |
| The hardware plan | 2 | machines in service by date; 5,180 from 28 December 2026 | anything about tenants |
| The finance freeze note and budget workbook | 2 | Q1 2027 monthly budgets held at December 2026 | any reservation |
| The rate card | 2 | EUR per core-month by effective date | a reservation |
| The chargeback policy (asks only) | 2 | what a firm tenant pays: the cores it holds at 00:00 UTC each day at the rate in force | when a change takes effect |
| The dictionary | 4 | field semantics: cores in use, machines in service, run, checkpoint and resize fields, machine events, the inventory's id history, quota change and reconciliation fields | what drives storage, how to follow a restore, that a re-image changes an id, when a change applies |

## Prompt

`prompt.txt`, gated by `voice-check.py` (in `precut.py`): the call with its unit and quarter, the workbook with the
reservations the guarantee is struck after and the three 2026 Q3 tables, the slide's named parts, and the rounding once
at the close.

## Tried and rejected

- The seed's architecture (a platform levy of a quarter of each firm reservation held in the tenant's name, so a third
  of its own reservation, recovered from 24 settled sister-cell guarantees, with budget ceilings binding after the
  fixed point): a hidden rule recovered from certified figures, banned as the decisive step; dropped at the draw, the
  budget ceilings kept as a filed rule on a lower rung.
- A power-capped guarantee (batch training at full tilt bound by the hall's power envelope at the firm peak, marginal
  watts per busy core against average): the marginal-against-average insight is task67's fixed-plus-variable carry in
  other nouns; dropped at the draw.
- A failover holdback sized by the worst single sister-cell loss, with the lost cell's load routed by user proximity as
  measured in past drains: the resilience standard's own wording sends the solver looking for where a lost cell's load
  goes (readable), and the routing estimate needed a measured share per sister whose noise threatened the thousand;
  dropped at the draw.
- Memory as the binding resource for batch (CPU overcommitted at 1.45, memory one to one): a whether-question a strong
  solver asks once the register shows memory beside cores, then one division and a minimum (readable, linear); dropped.
- A guarantee backed by physical cores at the firm tenants' coincident busiest hour (batch uses its cores fully, the
  overcommit assumes it does not): the estimand would have to say "physical" or "running", which names the step;
  dropped.
- Two scratch draws' furniture (task136's capacity report, own team, budget round and PNG while task139 was not on file;
  then task139's close-out, executive team and capacity planner once it landed): redrawn before registration to the
  capacity report, the requester's own team, the review meeting, the head of compute operations and a slide.
