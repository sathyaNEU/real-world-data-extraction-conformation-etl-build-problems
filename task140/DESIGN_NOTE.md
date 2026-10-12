# task140: Alisio Viajes, cell C-22's batch-training guarantee for 2027 Q1 (architecture 1)

Private, never ships. A new build (wave 2), numbered from seed FC11: the seed's world, decision and quantity are kept
(a compute cell's quarterly capacity review strikes the batch-training guarantee, the reservable cores left after the
firm tenants' reservations, at a 1.45 overcommit); its architecture (a platform levy of a quarter of each firm
reservation held inside its own base, recovered as a third from settled sister-cell ledgers, with budget ceilings
binding after the fixed point) is not used, because the decisive step there is a hidden rule recovered from certified
figures. The budget ceilings stay as a filed rule on a lower rung; the pitfall is re-found from how the cell's own
storage service burns CPU on the batch tier's dataset reads and checkpoints, so one of the reservations the guarantee
is struck after rises with the guarantee itself.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task140.json`, architecture v1, registered 2026-10-12 after task139's draw landed on main; `guard.py check` WARN (`overuse.objective`, answered below), no BLOCK; `guard.py validate` clean |
| Domain / task type | `supply-chain-logistics` (house domain; data-centre capacity planning, the supply side of compute) in client domain `general-statistics-data-science`, task type `regression-classification-model-diagnostics` (forecasting): the deciding statistical object is a regression of a dependent load on its two drivers, specified and solved forward, where a summary of the load's own history files another call |
| Objective | Forecasting & Predictive Modeling: the batch guarantee for 2027 Q1 (1 January to 31 March 2027), a window not yet open, struck from a forecast of the storage service's busiest hour in that quarter, which the history pins only through its drivers |
| Shape | `other`: the guarantee and the reservations it is struck after (the firm tenants' approved total, each platform service), the slide's named parts (the split of 726,624 reservable cores, title, axis), three asks on 2026 Q3 rows the call never reads (each batch team's redone core-hours and share, 12 figures; each month's machine-hours lost to hardware faults and to planned maintenance, 6 figures; each firm tenant's Q3 charge, 11 figures), the two files: about 44 criteria, arithmetic in `## Ask sheet` |
| Decision | `quantity_figure`, answer unit `count` (cores, the largest whole thousand that fits) |
| Mechanism | gap objective (decisive: the cores left after the firm reservations and the platform services carried at their own history are correctly computed, and the guarantee is scored on what the cell can carry once every batch core brings its storage load); pattern none, generators G1 (unit of value: a batch core costs the cell 1.20804 reservable cores, its own and the storage behind it) then G16 (method: the storage forecast built on its drivers, not on its history); Gate G `binding_constraint`; strategy `binding_constraint` (the limit is shared between the guarantee and a reservation that rises with it) |
| Layer 2 family / pattern | `allocation_constraints` (a fixed-point allocation: a deduction that depends on the residual being allocated); `own:residual-tier-drives-a-dependent-reservation` |
| Furniture | forum `line_manager_or_team`, forcing event `vote_or_meeting` (the quarterly capacity review, Tuesday 15 December 2026), organisation family `hospitality_or_tourism` (an online travel marketplace running its own data centres), role family `operations_director` (the head of compute operations), context artifact `capacity_report` (the cell's 2026 Q3 capacity report), calibration `none`, opening `question-first`, question form `how-many` |
| Spine | `c22_usage_hourly_2025-01-01_2026-12-13.csv`, the cell monitoring export: one row per tenant per hour, the tenant's average cores in use, 1 January 2025 to 13 December 2026 (UTC), 14 tenant series, 239,470 rows; constructed |
| Deliverables | `c22_capacity_2027q1.xlsx` (the guarantee, the reservations it is struck after, the three 2026 Q3 tables), `c22_capacity_review_2027q1.pptx` (one slide: how the quarter's 726,624 reservable cores divide between the firm tenants, the platform services and batch) |
| People | drawn with `guard.py names --geo Spain --seed 140 --n 40`, keeping names the guard clears: Alejandro Baena (head of compute operations, MAD1, the requester), Raúl Echevarría (head of infrastructure, signs CS-3 and the capacity memo), María Ayala (storage platform lead), Jordana Sala (batch training platform lead), Ruy Franco (MAD1 data-centre operations manager, the operations log), Esteban Madrigal (fleet and hardware, the hardware plan and the inventory), Georgina Quirós (technology controlling, the budgets, rate card and chargeback policy), Martina Pera (SRE, operations log entries); none appears in the prompt |

**Guard.** `guard.py check` on the registered card: WARN on `overuse.objective` (forecasting in 6 of the last 12): the
lane is forecasting and the seed's call is a forward guarantee, and the decisive gap (objective) and Gate G
(`binding_constraint`) differ from task137, task138 and task139 (time, time, population; forecasting, forecasting,
method selection). The bans ran against task137, task138 and task139, the three builds before this one by draw key.
Two scratch draws were refused before registration (see `## Tried and rejected`).

**Same-puzzle and same-driver tests.** Gap objective, decisive G1, decision `quantity_figure`, Gate G
`binding_constraint`: no build in the last twelve carries the gap, the G-code and the decision together (task184 is gap
objective with G1 on a pick, Gate G decomposition; task229 is gap objective with G7 on a date, binding constraint).
Older binding-constraint quantities (task32, task64, task79, task94) differ on the driver: an annual cap tested at
quarterly resolution, an orthogonal supply ceiling, a piecewise inverse past a capacity constant, a delivery on top of
held stock; none has a deduction that grows with the quantity being decided.

**Abstraction test.** Stripped of nouns, the driver is: the residual promised to the lowest tier is struck after every
higher reservation, and one of those reservations is a dependent service whose load rises with the very tier being
promised, so the residual has to be solved together with that dependency, estimated from the dependent's own use
against its two drivers. The three nearest drivers on file (task32 v3 lineage, an annual cap on a by-product binding
below a tier; task98 v1 lineage, a nightly residual of demand over open stock; task230 v2, a detection step whose hit
rate moves with the pool) share no latent structure, default path or correction with it. Measured trap 22 (a
self-referencing rule solved in one pass) is the seed's family; here no rule is stated, the dependency is a measured
load, and the one-pass solve is a lower rung.

**Data-native sentence.** C-22's storage service runs a daemon on every machine in service and serves the batch
training tier's dataset reads and checkpoint writes, so its hour-by-hour use is 2.9404 cores for each machine in service
plus 0.20804 cores for each batch core running (the two-driver least-squares fit on the 17,081 hours on file, residual
s.d. 13.0 cores on a 25,000-core load; the batch tier's pauses and the rack additions move the two drivers apart).
Through 2025 and 2026 racks were added as the firm tenants grew, so the guarantee moved only between 55,000 and
58,000 cores and the storage service's busiest hour tracked the machines; the December refresh's 580 machines lift
the reservable cores from 637,536 in 2026 Q4 to 726,624 while the firm tenants grow from 553,400 to 576,972, so the
guarantee nearly doubles and every core it adds brings 0.20804 cores of storage the storage service's own quarterly
history has never seen.

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
(ten product services and the deadline-batch class `settle-batch`), two platform services (`cell-store`, the cell's
storage service; `cell-ctl`, the scheduler and the monitoring agents) and the batch training tier (`batch-train`, run
for six teams). The Cell Capacity Standard CS-3 (rev. June 2026) governs the quarterly review. Technology controlling
charges the firm tenants monthly under the 2026 chargeback policy.

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
2. Reservable: 5,220 machines times 96 times 1.45, 726,624 cores.
3. Firm: each tenant's Q1 request against its January 2027 monthly budget (held at December 2026 by the freeze) at
   EUR 7.42 per core-month (the MAD1 reserved-core rate from 1 January 2027): `search-api`, `pricing` and `reco-serve`
   held to their budgets, the other eight at their requests; 576,972 cores.
4. Platform: each platform service's busiest hour in each of the last four quarters from the monitoring export, and
   the least-squares line through the four, one quarter on: `cell-ctl` 1,999.2 cores, `cell-store` 25,417.6 cores.
5. Guarantee: 726,624 less 576,972 less the two platform forecasts leaves 122,235.1 cores; the largest whole thousand.

Ends on: 122,000 cores (the default path's guarantee; asserted in `checks.py` and recomputed by `verify.py`).
Golden: 109,000 cores: `cell-store` forecast from its drivers, 2.9404 cores per machine in service and 0.20804 per batch
core running (the least-squares fit of its hourly use on the cell's machines in service and the batch tier's cores),
at the 5,220 machines of Q1 and the batch tier at its own guarantee, so the storage reservation and the guarantee are
solved together (109,492.0 before the whole thousand; `cell-store` 38,058.5, `cell-ctl` 1,999.2).

## Stump sentence

A competent solver approves the firm requests under their frozen budgets at the Q1 rate card, forecasts each
platform service's busiest hour as the line through its last four quarters and files 122,000 cores (Ends on); the step
that lands it there is carrying the storage service forward on its own history, when its busiest hour is set by the
machines in service and the batch cores running (2.9404 and 0.20804 cores each), so the guarantee has to be solved
together with the storage it brings: the golden is 109,000.

## Three rules

- **Task type:** `general-statistics-data-science` / `regression-classification-model-diagnostics` (forecasting): the
  call rests on a regression of the storage service's hourly use on its two drivers (machines in service, batch cores
  running), specified on the drivers rather than on time and read forward at the guarantee being decided; the house
  domain is supply-chain-logistics (data-centre capacity planning, the supply side of compute).
- **Domain test:** the deciding quantity is the storage service's CPU per machine in service and per batch core
  running, estimated from the cell's own hourly telemetry, where the batch tier's pauses and the rack additions move
  the two drivers apart; a compute capacity planner sizes a dependent infrastructure service from the workloads that
  drive it before striking a residual guarantee, and replacing that regression with a summary of the service's own
  history (its trend, its share of the cell) files 122,000 or 119,000 instead of 109,000.
- **Swap:** "C-22 can guarantee 109,000 cores to batch training in 2027 Q1, the reservable cores left after the firm
  tenants and the platform services, the storage service reserved at 2.9404 cores per machine in service and 0.20804
  per batch core" read with a hospital's nouns ("Ward 7 can promise 109 elective beds, the beds left after emergency
  admissions and support services") stops making sense: no support department occupies beds out of the pool it serves,
  and there are no reservable cores at an overcommit, machines in service or batch cores running for the dependency to
  be measured on; with the method swapped (the regression replaced by the load's own trend or share), the call moves to
  122,000 or 119,000.
- **Layer 1:** a monitoring export in UTC beside an operations log written in Madrid local time (CEST to 25 October,
  CET after), a collector outage on 19 August 2026 leaving seven hours with no rows for any tenant, tenant ids in the
  export and the ledger against cost-centre numbers in the finance budget workbook (joined through the tenant
  directory), budget lines for other cells and for storage beside the C-22 lines, a re-sent day of export rows in March
  2026, rack additions dated in the hardware plan and the machines series (installed beside in service); on the ask
  paths, an elastic training scheduler's resize log, checkpoint writes that never
  committed, a cluster manager that gives a re-imaged machine a new id and re-sent a day's removals after a restart, a
  hardware inventory carrying each asset's id history, spares that replace retired machines in the same rack, a quota
  service that applies changes in six-hourly reconciliation runs and ran none for three days after the August power
  event. Each is what these systems write; none decides the call.
- **Layer 2:** family `allocation_constraints` on a General Statistics regression: the shortcut forecasts the storage
  service as a tenant like the others (its trend, its last quarter, its share of the cell); the expert specifies its
  use on its drivers and reads the forecast at the decision's own value, solving the guarantee and the storage
  reservation together.
- **Decisive step:** specifying the storage service's busiest-hour load on what drives it (machines in service and
  batch cores running) instead of on its own history, and reading that model at the batch tier's new guarantee, so the
  guarantee and the storage reservation are solved as one fixed point: a capacity planner's dependent-load forecast,
  done with a two-driver regression on the cell's telemetry.
- **Not semantics:** every field the call reads means one thing and the easy route reads each correctly (cores in use
  per tenant per hour, machines in service per hour, requests, monthly budgets, the rate in force, the reservable
  cores); the fork table's rows are closed and none is the stump, and with every field read right the trend of the
  storage service's own busiest hours still files 122,000.
- **Not rule application:** CS-3 files the estimand (reservable cores, firm holds, platform services at the use forecast
  for their busiest hour, the largest whole thousand left, batch inside its guarantee) and leaves the forecast to the
  analyst; executing every filed rule with the default forecast files 122,000, and no rule, procedure or document
  performs the step that moves it to 109,000 (a model of the storage load on its drivers, read at the unknown guarantee).
- **Analyst test:** a strong analyst who approves every firm request under its frozen budget at the Q1 rate card, takes
  the hardware plan's 5,220 machines at the 1.45 overcommit and forecasts the platform services' busiest hours from
  their own last four quarters files 122,000 cores; with the last quarter's busiest hour 122,000, with storage scaled to
  the 5,220 machines 119,000, with storage fitted on the batch tier alone 111,000, and with the batch load applied once at
  the default's guarantee 106,000; only the storage reservation solved together with the guarantee gives 109,000.
- **Estimand:** CS-3 sections 2 to 5 (reservable cores, firm approvals, platform services at the use forecast for
  their busiest hour of the quarter, the guarantee as the largest whole thousand of cores the reservable cores leave,
  batch running inside it) with the prompt's question (the first quarter of 2027); CS-3 is the filed standard, the
  capacity memo and the hardware plan carry the quarter's overcommit and machines.
- **No decoy:** nothing is planted to be caught: no copied or backfilled block in any series (asserted), no hidden
  rule, and no memo, draft, briefing or stakeholder figure gives a 2027 Q1 guarantee, a storage forecast or a method;
  the platform team's past storage reservations are history in the ledger, the Q3 capacity report covers Q3 only, and
  the batch teams' H1 2027 demand note (a distractor) states demand, not a guarantee.
- **No certified replay:** the storage dependency is measured on the hourly telemetry (two drivers, 17,081 hours,
  residuals of about 13 cores); no certified or published figure has to be reproduced to find it, and the past
  guarantees in the ledger are the reviews' outcomes, which the golden never reads.
- **Lesson:** a deduction that rises with the quantity being decided has to be modelled on its drivers and solved
  together with that quantity; carrying it forward on its own history is safe only while the decision's own value
  stands still, as it did here from 2025 to 2026.

## Readability screen

Six tests per rung: 1 a filed sentence names it or makes the solver ask; 2 schema (a column, key or marker); 3 a
reflex of the opponent; 4 a control or corpus scores it; 5 the hygiene battery finds it; 6 linear (one subtraction,
ratio or half of a reported figure). Verdict last.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Control | 5 Hygiene | 6 Linear | Verdict |
|---|---|---|---|---|---|---|---|
| R-1 every firm request taken whole (no budget hold) | CS-3 section 3.2 names the hold | the budget workbook's 2027 columns | no | no | no | yes | readable |
| R0 every platform service on the line through its last four busiest hours (the default path) | no | no | yes (a tenant's busiest hour trended) | no | no | yes | readable |
| R0b the last quarter's busiest hour carried | no | no | yes | no | no | yes | readable |
| R1 `cell-store` scaled with the cell (per machine, or its share of the reservable cores) | no | the machines-in-service series | yes (overhead scales with the fleet) | no | no | yes | readable |
| R2 `cell-store` on batch alone (no machine term), or Q4's per-machine level held with the batch term added | no | the batch series beside it | no | no | no | no | readable |
| R2b the batch load applied once, at R0's guarantee | no | no | no | no | no | yes (once the dependency is seen, a single substitution) | readable |
| R3 (decisive) `cell-store` specified on machines in service and batch cores running from the hourly telemetry, reserved at its forecast busiest hour with the batch tier at its own guarantee, and the guarantee and the storage reservation solved together | no sentence names a driver, the batch tier's load on storage, a ratio or a joint solve; CS-3 section 4.1 says only "the use forecast for its busiest hour of the quarter" | no column holds storage per core, a driver or a share; the export is one series per tenant | no: the reflexes are R0 to R1, each files its own wrong guarantee | no closed record scores a forecast method: the ledger's past platform reservations were struck at guarantees between 55,000 and 58,000, and no past quarter's guarantee doubled | no | no: a two-driver fit read at the decision's own value, a linear system in the unknown guarantee | silent |

The decisive rung is silent because the storage service is a routine line: CS-3 files it beside the scheduler, the
ledger lists it like any tenant, and the default path forecasts it with the same line it would use on any series. The
pack never says what drives it; the telemetry does, to an analyst who asks.

## Semantic fork table

One row per term of the main ask and per convention the main computation needs. `checks.py` asserts each row (the
alternative computed and shown to move the call or its figures, or shown to converge). CS-3 is the Cell Capacity
Standard.

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "cores" | reservable cores, the unit every reservation and the guarantee is struck in | physical cores (the 501,120 behind them) | moves the call (no guarantee left, asserted) | CS-3 2.1 and 2.2 (reservable cores are machines times 96 times the overcommit; every reservation and the guarantee is counted against them) |
| SF2 | "guarantee" | the largest whole thousand of cores the reservable cores leave after the firm and platform reservations | the remainder to the nearest thousand | same call (asserted: 109,492.0 rounds to 109,000) | CS-3 5.1 |
| SF3 | "the first quarter of 2027" | 1 January to 31 March 2027 | (none) | n/a | the prompt; CS-3 1.2 (quarters are calendar quarters) |
| SF4 | the quarter's machines | 5,220 in service from 28 December 2026 | the 4,640 in service on the pull date; installed less a repair allowance | the pull date moves the call far (44,000, asserted); an allowance of the cell's 2026 average out of service (2.0 machines) gives the same call (asserted) | CS-3 2.1 (the hardware plan's machines in service at the start of the quarter); the plan's By quarter sheet |
| SF5 | the quarter's overcommit | 1.45 | (none) | n/a | the capacity memo |
| SF6 | a firm tenant's request | the request in the Q1 window, one per tenant | (none: one row per tenant) | n/a | the request file (asserted: eleven tenants, one row each) |
| SF7 | the budget a request is held to | the tenant's January to March 2027 monthly budget line for MAD1 C-22 (held at December 2026 by the freeze) | the 2026 average month; the Q4 total over three | the 2026 average moves the call (115,000, asserted); the Q4 total over three converges (Q4's months equal the 2027 ones, asserted) | CS-3 3.2 and 3.3 ("its monthly budget", the line for its reserved cores in the cell); the workbook's 2027 columns and the freeze note |
| SF8 | the rate card in force for the quarter | EUR 7.42 per core-month, MAD1 reserved cores, effective 1 January 2027 | EUR 7.70 (in force at the review, from 1 September 2026) | moves the call (120,000, asserted) | CS-3 3.2 ("in force for the quarter"); the rate card's effective dates |
| SF9 | what a budget pays for | the largest whole number of cores the monthly budget covers at the rate | rounded to the nearest core | converges (asserted: same call) | CS-3 3.2 ("the largest whole number of cores") |
| SF10 | the platform services | `cell-store` and `cell-ctl` | (none) | n/a | the tenant directory (class `platform`); CS-3 4.1 |
| SF11 | a service's use in an hour | the export's average cores in use over the hour | (none) | n/a | CS-3 4.2; the dictionary |
| SF12 | "its busiest hour of the quarter" | the hour of the quarter with the highest average use | the 99th percentile hour | same call (asserted: `cell-ctl` 1,988.1 against 1,999.2) | CS-3 4.1 |
| SF13 | the use forecast for `cell-store` | its use at the quarter's busiest hour from its drivers, with the batch tier at its own guarantee (R3) | its trend (R0), last value (R0b), share of the cell (R1), batch alone (R2), one pass (R2b) | each files its own guarantee (Ladder) | a method row, not a reading: CS-3 4.1 asks for a forecast and 5.2 runs batch inside its guarantee, so the busiest hour comes when batch fills it (asserted: in every quarter on file batch reached 99.9 per cent of its guarantee or more); each alternative is priced and refused by the telemetry's own fit |
| SF14 | the batch tier at its busiest | at its guarantee | at its historical average fill (98.9 per cent) | same call (asserted: 109,707.1 before the thousand) | CS-3 5.2 and the record (batch reached its guarantee in every quarter) |
| SF15 | the busiest hour's excess over the fitted line | not carried | the fit's largest residual (45.4 cores) carried | same call (asserted: 109,454.4 before the thousand, `cell-store` 38,103.9) | the records converge |
| SF16 | `cell-ctl`'s forecast | its busiest hour on the line through four quarters | last value; mean; fitted on the machines | same call (asserted: 1,991.4, 1,982.0, 2,078.5 cores, each 2,000 to the nearest thousand) | the records converge |
| SF17 | the order of the solve | the guarantee and the storage reservation solved together, the whole thousand taken last, `cell-store` reserved at the guarantee | `cell-store` read at the guarantee before the thousand | same guarantee; `cell-store` 38,160.8, the same thousand (asserted) | CS-3 5.1 and 5.2 (batch runs inside the whole-thousand guarantee) |
| SF18 | the remainder | unreserved (594.3 cores) | added to batch | n/a: the guarantee is a whole thousand | CS-3 5.2 |
| SF19 | a tenant's budget line | the cost-centre number in the tenant directory, matched to the workbook's CC and its MAD1 C-22 line | by cost-centre name | converges (asserted: every firm tenant has one cost centre and one C-22 line) | the tenant directory's `cost_centre`; CS-3 3.3 |
| SF20 | Ask A: training lost to a preemption | the preempted run's training from the state its resumption restarted from (the restored checkpoint's write start) to the preemption | from the run's own newest committed checkpoint | every team's figure (S2) | the ask's own terms (the training the preemption discarded); the runs file's `restore_checkpoint` |
| SF21 | Ask A: a checkpoint's training state | taken when its write started (`write_started_utc`); training carries on while it is written | the write's commit time | every redone figure (S3, asserted) | the dictionary ("When the trainer took the state at step and began writing it. Training carries on while the checkpoint is written.") |
| SF22 | Ask A: a run's cores over time | its cores at start, changed by each resize from the resize's time | its cores at start throughout | every figure (S1, asserted) | the resize log; the dictionary ("Cores held by the run from at_utc") |
| SF23 | Ask B: a machine that came back | the same asset back in service under any machine id | the same machine id | every figure (S1, asserted) | the ask's own terms ("machines that came back"); the inventory's cluster ids per asset |
| SF24 | Ask B: hours in a month | the hours of an outage falling in that month | the outage's whole length in the month it began | converges (asserted: no outage on file crosses a month boundary) | the records converge |
| SF25 | Ask C: the cores a tenant holds on a day | its reservation at 00:00 UTC that day, a change counting once the quota service has applied it to the cell's quotas | from the change's request time | every tenant (S1, asserted) | the chargeback policy 2.1 ("the cores the tenant holds in the cell at 00:00 UTC"); the dictionary ("The changes the run applied to the cell's quotas") |
| SF26 | Ask C: the month's rate | the rate card's rate in force on the day | Q3's opening rate throughout | every tenant's September charge (S2, asserted) | the chargeback policy 2.1 and 3.1; the rate card's effective dates |
| SF27 | Ask B: a retired machine replaced from spares | not a machine that came back (the spare is another asset: its own tag and serial) | the spare's registration taken as the return | every hardware-fault figure (S2, asserted) | the inventory (the retired asset's status, the spare's own tag) |
| SF28 | Ask A: whose core-hours | the core-hours the preempted run held on the training that was lost | the resumed run's core-hours spent getting back to where the preempted run stopped | every team's figure (asserted: the two differ where the runs' cores differ) | the ask's own terms ("the core-hours its runs held on training lost to a preemption": the redo's training is kept, not lost) |

The stump is none of these rows: every term is read the same way by a careful reader, and the default path reads them
all correctly. SF13 lists methods, not readings; each is priced and refused by the telemetry's fit. SF20 to SF27 are the
asks' readings (with SF28), each closed by the ask's wording, a dictionary line or a convergence.

## Ladder

Every rung is a complete pipeline on the same literal estimand (CS-3 sections 2 to 5), computed by `calc.ladder` from
the pack and asserted by name in `checks.py`; the default path and the golden are recomputed by `verify.py`.

| Rung | Guarantee before the thousand | Guarantee | Against the golden |
|---|---|---|---|
| R-1 no budget hold, storage on its four-quarter line | 119,007.1 | 119,000 | +9.2 per cent |
| R0 (default) both platform services on the line through their last four busiest hours | 122,235.1 | 122,000 | +11.9 per cent |
| R0b the last quarter's busiest hour carried | 122,298.1 | 122,000 | +11.9 per cent |
| R0c the line through all eight quarters | 122,117.0 | 122,000 | +11.9 per cent |
| R0e the line through the last four complete quarters | 122,324.1 | 122,000 | +11.9 per cent |
| R1 cell-store per machine at Q4's busiest hour, times 5,220 | 119,115.3 | 119,000 | +9.2 per cent |
| R1b cell-store as Q4's share of the reservable cores | 118,755.1 | 118,000 | +8.3 per cent |
| Monly cell-store fitted on machines alone | 120,796.6 | 120,000 | +10.1 per cent |
| R2e the two-driver fit read with batch at Q4's 56,000 | 120,620.5 | 120,000 | +10.1 per cent |
| R2 cell-store fitted on the batch tier alone (whole history) | 111,662.0 | 111,000 | +1.8 per cent |
| R2c Q4's per-machine level held, the batch term added | 110,999.0 | 110,000 | +0.9 per cent |
| R2d the two-driver fit at the 4,640 machines of the pull date | 110,903.7 | 110,000 | +0.9 per cent |
| LedgerFit the ledger's eight cell-store reservations fitted on machines and guarantees | 110,224.4 | 110,000 | +0.9 per cent |
| R2b the batch load applied once, at R0's guarantee | 106,840.8 | 106,000 | -2.8 per cent |
| O1 cell-store per batch core at Q4's ratio | 101,636.0 | 101,000 | -7.3 per cent |
| QmaxFit the eight quarterly busiest hours fitted on their machines and batch (converges) | 109,459.4 | 109,000 | +0.0 per cent |
| R3 golden | 109,492.0 | 109,000 | 0 |

- **Separation.** The golden is bracketed: the routes that carry `cell-store` on its own history or scale it with the
  cell file 118,000 to 122,000, the partial models file a neighbouring thousand on one side or the other (106,000 once at the
  default's guarantee; 110,000 from the ledger's reservations, 110,000 with Q4's level held or at the pull date's
  machines, 111,000 on batch alone), each by one error the telemetry or a filed fact refutes. Every wrong route sits at
  least 600 cores from the golden before the thousand (asserted). The batch-only fit files 111,000 on the whole
  history, 2026, the last two quarters and the last quarter, because the history's guarantee did not move with its
  machines.
- **Position.** The golden's unrounded guarantee sits 492 cores above 109,000; every converging convention (SF2,
  SF4, SF12, SF14 to SF17, the fit windows, the re-sent day, the gap, machines installed) keeps it inside the thousand
  (asserted). `cell-store` (38,058.5), `cell-ctl` (1,999.2), the firm total (576,972) and the platform total (40,057.7)
  sit at least 300 cores from their nearest-1,000 rounding edges (asserted).
- **Grid.** The four storage routes (R0, R1, R2b, R3) by the two firm readings (held, whole) by the two rate cards
  (Q1, the one in force at the review), 16 cells computed in `checks.py`: the golden cell alone files 109,000 (asserted);
  the nearest wrong cells file 106,000 and 103,000.
- **Worth on the graded figures.** R3 moves the guarantee, the storage reservation, the platform total and the slide's
  batch and platform parts; the firm total and `cell-ctl` are the same on every storage route.

## Closure table

| # | Axis | Reading and move |
|---|---|---|
| 1 | Population | the eleven firm tenants with a Q1 request (one row each, asserted), the two platform services in the tenant directory, the batch tier; members not yet observed: none, CS-3 3.1 admits a firm tenant only through the Q1 request window (closed 4 December) and the directory lists no platform service without a series in the export |
| 2 | Unit of account | reservable cores (CS-3 2.2); the guarantee in whole thousands (5.1); a tenant is a directory id |
| 3 | Attribution window | the quarter 1 January to 31 March 2027; a platform service's busiest hour within it (4.1) |
| 4 | As-of dating | machines in service at the start of the quarter per the hardware plan's 11 December revision (5,220 from 28 December); requests as filed at the window's close; budgets as frozen on 27 November; the export to 13 December 23:00 UTC |
| 5 | Version basis | the hardware plan's latest revision; one request per tenant; the rate card's MAD1 reserved-core row effective 1 January 2027 (SF8) |
| 6 | Denominator | the rate divides a monthly budget into cores (SF9); no rate is estimated on the call path |
| 7 | Weighting | none: the guarantee is a difference of totals; the regression weights every hour alike (the re-sent day of March 2026 kept twice moves the per-machine coefficient by 0.00001 and the call not at all, asserted) |
| 8 | Window length | the fit runs on every hour on file; fits on the last four quarters, on 2026 alone and from 2025 Q3 give 109,495.6, 109,495.6, 109,494.0 before the thousand (asserted: same guarantee) |
| 9 | Boundary inclusivity | "the largest whole thousand" (floor, SF2); "the largest whole number of cores" a budget covers (SF9) |
| 10 | Rounding path | carried unrounded to the guarantee's floor; the guarantee 109,492.0 sits 492 cores inside its thousand across every converging convention (asserted); the storage reservation, the platform total and the firm total each at least 300 cores from a nearest-1,000 edge (asserted) |
| 11 | Tie-break | none needed: one guarantee, one storage reservation |
| 12 | Maturity and censoring | none on the call: the Q1 requests are closed; the export's last day (13 December) is complete to 23:00 UTC; the seven hours of 19 August with no rows are missing for every series alike (asserted: interpolating them gives 109,491.9 before the thousand) |
| 13 | Order of operations | firm holds first (3.2), platform forecasts with batch at its guarantee (4.1 and 5.2), the whole thousand last (SF17) |
| 14 | Row order | file order changes nothing (asserted: the hours shuffled give the same coefficients) |
| 15 | Duplicate resolution | the re-sent day of 17 March 2026 in the export (every tenant's rows for that day written twice, byte-identical, 336 rows): deduplicated or not, the same guarantee (asserted, 109,491.9 before the thousand) |
| 16 | Identity normalisation | tenant ids in the export, the ledger and the requests; cost-centre numbers in the budget workbook, joined through the directory (asserted: every firm tenant matches one C-22 line) |
| 17 | Netting against gross | none: reservations add; the guarantee is what is left |
| 18 | Dimensional units | cores throughout; budgets in euros per month over a rate in euros per core-month gives cores (SF9) |
| 19 | Code and status semantics | tenant classes (`firm`, `platform`, `batch`) in the directory; the export's `cores_in_use` defined in the dictionary; machines in service against installed converge (asserted: 109,498.6 before the thousand) |
| 20 | Integerisation | the guarantee's whole thousand (floor); firm holds in whole cores (floor) |
| 21 | Clause scope | CS-3 3 applies to firm tenants, 4 to platform services, 5 to the batch tier (the directory's classes) |
| 22 | Forward window contents | the quarter's machines (the hardware plan), overcommit (the memo), firm requests and budgets (filed); the platform services' use, forecast from the export; the batch tier at its guarantee (5.2) |

## Literal reader

Executed word for word, the prompt and CS-3 define the guarantee as the largest whole thousand of reservable cores that
the quarter's 726,624 (2.1, the hardware plan's 5,220 machines and the memo's 1.45) leave after the firm tenants'
reservations (3.2: each Q1 request held to what its frozen budget line buys at the EUR 7.42 rate in force from
1 January) and the platform services' reservations (4.1: each at the use forecast for its busiest hour of the quarter),
with batch running inside its guarantee (5.2). Section 4.1 leaves the forecast to the analyst and names no method; the
only method the records support for `cell-store` is its fit on its two drivers, because its hourly use moves with the
batch tier's cores (every batch pause, every quarterly change of the guarantee) and with the machines in service (every
rack addition), and 5.2 puts the batch tier at its guarantee in the quarter's busiest hours, so the literal forecast
of `cell-store` contains the guarantee itself. Every term in the fork table resolves to one reading or converges; the
only step the text leaves open is how to forecast the platform services, which the records then settle.

## Oracles

- **None on the call path.** No file states a 2027 Q1 guarantee, a storage forecast, a driver, a ratio or a method.
  The ledger's past `cell-store` reservations are the platform team's own sizings of past quarters, struck at
  guarantees between 55,000 and 58,000; fitted on the machines and the guarantees they file 110,000 (their rounding
  up to the next 100 and their spare cores blur the batch term), and their trend files 122,000, so they score no
  forecast method for a quarter whose guarantee nearly doubles.
- **The Q3 capacity report** reports Q3 2026's reservable cores, reservations, busiest hours and the guarantee
  delivered: inputs every rung reads alike; it states no 2027 figure (asserted), and every figure in it recomputes from
  the export, the ledger and the hardware plan (asserted).
- **The ask paths** (batch runs, checkpoints and resizes; machine events and the inventory; quota changes, the
  reconciler's runs and the chargeback policy): no rung of the call reads them (asserted: the call is unchanged with
  every ask file deleted), and nothing in the pack states a team's redone core-hours, a month's machine-hours or a
  tenant's Q3 charge, so none ties only under the golden.

## Ask sheet

**Main call's declared row population:** every row of `capacity_requests_2027Q1.csv`, the hardware plan, the capacity
memo, CS-3, the budget workbook's C-22 lines, the rate card's MAD1 reserved-core rows, the tenant directory, the
ledger's `cell-store`, `cell-ctl` and `batch-train` rows, and the `cell-store`, `cell-ctl` and `batch-train` series of
the monitoring export with the cell's machines series. Device and hazard rows in it: 0 (asserted: the call's figures are
unchanged with every ask file, both distractors, the report and the log deleted). The asks read the batch runs,
checkpoints and resize log (Ask A), the cluster manager's machine events and the hardware inventory (Ask B), and the
quota change file, the quota service's reconciliation runs, the chargeback policy, the rate card's 2026 rows and the
ledger's firm rows for 2026 Q3 (Ask C). Each ask is a measure the cell's tiers carry that the call does not turn on;
none is keyed to the call, its construction or its figures; the three share no primary device and no primary file. No
sentence in the pack adjudicates a device: the dictionary describes each file's fields only, and the chargeback policy
states what a tenant pays for, not when a change takes effect.

**Ask A. For each batch training team, the core-hours its runs held in July to September 2026 on training lost to a
preemption, and that as a share of all the core-hours its runs held** (6 teams by 2 figures, 12: core-hours to the
nearest 100, per cent to two decimals).
- H18 home: the batch tier's account of what its 2026 Q3 guarantee bought (a measure every batch team carries that the
  Q1 guarantee does not turn on); use: the batch platform lead reads it beside the new guarantee.
- Construction: each run's core-hours from its start (or 1 July) to its end, its cores changed at each resize; for each
  run that ended preempted, the resumed run that names it in `resumed_from` carries the checkpoint it restarted from
  (`restore_checkpoint`); the preempted run's core-hours from that checkpoint's `write_started_utc` to its end (or from
  its own start, when the checkpoint is an earlier run's) are the training the preemption lost; summed by team.
- Primary device (D2, the record is the latest accepted, not the latest delivered): a resumption restarts from the
  newest checkpoint that passes validation on restore, and about a third of the time the preempted run's newest
  committed checkpoint fails it and the resumption takes the one before, or the predecessor run's when the preempted
  run committed nothing valid (65 of the 192 preemptions in the quarter, asserted); the checkpoint file
  carries no validation status, and the restore point sits only on the resumed run's row. Read from each preempted
  run's own newest committed checkpoint, every team's figure is low (S2).
- Hazards: HA1 (D6) elastic runs resize (1,161 resizes; the runs file's `cores` is at start); HA2 (D2) checkpoint
  writes that never committed (1,583 of 52,336, `committed_utc` blank); HA3 (shared cause) the 19 August power event
  and the 9 September scheduler upgrade preempted every running run; HA4 runs started in June (held core-hours clipped
  to 1 July; no redone training before 1 July, asserted).
- Converging readings (asserted): every preemption in the quarter is resumed in the file before 1 October; no restore
  checkpoint is later than its preempted run's end; every restore point is a committed checkpoint.
- Path (5 files, 14 columns): the runs file (`run_id`, `team`, `cores`, `started_utc`, `ended_utc`, `end_state`,
  `resumed_from`, `restore_checkpoint`), the checkpoints (`checkpoint_id`, `run_id`, `write_started_utc`,
  `committed_utc`), the resize log (`run_id`, `at_utc`, `cores_after`), the tenant directory's batch teams, the
  dictionary.
- Stops (each computed and asserted in `checks.py`): S1 natural (cores at start, each preempted run's own newest
  committed checkpoint); S2 resizes applied, own newest committed checkpoint; S2b resizes applied, own newest write
  started (committed or not); S3 the restore point followed, the commit time taken as the training state; each misses
  all 12 (asserted):
  - `ranking-ml`: golden 121,800 core-hours, 0.40 per cent; S1 66,700, 0.21; S2 64,000, 0.21; S2b 61,300, 0.20; S3 117,400, 0.38
  - `pricing-ml`: golden 80,500 core-hours, 0.37 per cent; S1 53,800, 0.24; S2 52,400, 0.24; S2b 50,500, 0.23; S3 76,100, 0.35
  - `fraud-ml`: golden 48,500 core-hours, 0.31 per cent; S1 38,000, 0.24; S2 38,300, 0.25; S2b 32,700, 0.21; S3 46,000, 0.30
  - `reco-ml`: golden 144,300 core-hours, 0.59 per cent; S1 87,700, 0.34; S2 86,900, 0.36; S2b 72,100, 0.30; S3 140,400, 0.57
  - `demand-ml`: golden 72,000 core-hours, 0.49 per cent; S1 45,500, 0.29; S2 44,800, 0.30; S2b 39,800, 0.27; S3 69,100, 0.47
  - `nlp-ml`: golden 134,900 core-hours, 0.77 per cent; S1 86,800, 0.48; S2 84,100, 0.48; S2b 72,100, 0.41; S3 131,800, 0.75
- Lazy delta: S1 wrong on 12 of 12.
- Realism: elastic trainers checkpoint every few hours while training carries on, and validate shards on restore; a
  scheduler records the restore point on the run that restored it.

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
- Hazards: HB1 (D1, texture) the cluster manager re-sent 19 August's removals after its restart (4 byte-identical
  rows, found by the battery; kept, they move August maintenance); HB2 assets retired after a fault (they never come back, rightly
  out); HB3 spares registered in the racks of retired machines (pairing an unmatched removal with the next new
  registration in its rack counts the retired machine as back, S2).
- Converging readings (asserted): no outage crosses a month boundary; every return is under exactly one id.
- Path (3 files, 11 columns): the machine events (`machine_id`, `event`, `time_utc`, `cause`, `rack`), the inventory's
  asset sheet (`Asset tag`, `Rack`, `Status`) and cluster ids (`Asset tag`, `Machine id`, `Registered (UTC)`), the
  dictionary.
- Stops (computed and asserted): S1 natural (matched on machine id) misses all 6; S2 over-cleaned (an unmatched removal
  paired with the next registration in its rack that no same-id return claims) misses the 3 hardware-fault figures and
  lands on the 3 maintenance figures, where re-images pair inside one rack and the pairing preserves each
  month's total:
  - July: hardware faults golden 750, S1 590, S2 1,470; planned maintenance golden 850, S1 570, S2 850
  - August: hardware faults golden 730, S1 570, S2 1,010; planned maintenance golden 910, S1 630, S2 910
  - September: hardware faults golden 660, S1 530, S2 820; planned maintenance golden 880, S1 630, S2 880
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
  power event; the change file carries only the request time, the runs file the changes each run applied (29
  changes, 355 runs). From the request time, every tenant's charge is off (each had a change requested after 18:05
  UTC or during the stop).
- Hazards: HC1 the rate card's 1 September 2026 adjustment (EUR 7.65 to EUR 7.70, seen and executed); HC2 releases and
  the transfer (negative changes, a transfer as two changes on one ticket, seen); HC3 the 19 August stop (part of the
  primary's mechanism, a shared cause with Ask A's HA3 and the export's outage).
- Converging readings (asserted): no change is applied at 00:00 UTC and no reconciliation run spans midnight; every
  change is applied exactly once.
- Path (6 files, 13 columns): the ledger's 2026 Q3 firm rows (`quarter`, `tenant`, `reserved_cores`), the quota
  changes (`change_id`, `tenant`, `delta_cores`, `requested_utc`), the reconciliation runs (`run_started_utc`,
  `changes_applied`), the rate card (`effective_from`, `eur_per_unit_month`), the chargeback policy, the dictionary.
- Stops (computed and asserted): S1 natural (changes from their request time), all 11 off; S2 changes from the
  application time but Q3's opening rate throughout, all 11 off:
  - `search-api`: golden EUR 2,653,000; S1 2,653,300; S2 2,647,200
  - `avail-cache`: golden EUR 2,148,200; S1 2,148,500; S2 2,143,500
  - `pricing`: golden EUR 1,594,300; S1 1,594,500; S2 1,590,800
  - `booking`: golden EUR 1,204,900; S1 1,205,200; S2 1,202,200
  - `payments`: golden EUR 696,700; S1 697,400; S2 695,200
  - `reviews`: golden EUR 506,800; S1 506,200; S2 505,700
  - `reco-serve`: golden EUR 1,104,100; S1 1,104,400; S2 1,101,600
  - `ads-listings`: golden EUR 822,900; S1 823,500; S2 821,100
  - `notify`: golden EUR 409,200; S1 410,100; S2 408,300
  - `partner-gw`: golden EUR 658,500; S1 659,200; S2 657,000
  - `settle-batch`: golden EUR 488,500; S1 489,500; S2 487,400
- Lazy delta: S1 wrong on 11 of 11.
- Realism: quota systems reconcile on a schedule, and a cell-local controller that stops in an incident leaves requests
  queued.

**Mid-bin.** Each ask figure sits at least 15 per cent of its bin from a rounding edge (asserted in `checks.py`);
three fixed stream offsets in `world.py` (`SALT`: the 2026 Q3 maintenance waves, the batch scheduler, the quota
changes) were chosen once against that criterion and the stops above.

**Hazard table**

| Hazard | Root cause | Moves | Per-ask delta |
|---|---|---|---|
| HA1 elastic resizes | the training scheduler | Ask A | every team, if ignored (S1) |
| HA2 uncommitted writes | trainers preempted mid-write | Ask A | every redone figure (S2b) |
| HA3, HC3 the 19 August power event | the hall 2 UPS transfer fault | Asks A and C (and the export's seven missing hours, neutral) | Ask A every team (a pause preempting every run), Ask C the changes queued to 22 August |
| HB1 re-sent removals | the cluster manager's restart on 19 August | Ask B, loud | August maintenance, if not deduplicated |
| HB3 spares in retired machines' racks | the fleet's spares process | Ask B | every hardware-fault figure under S2 |
| HC1 September rate | the energy adjustment | Ask C | every tenant's September, if ignored (S2) |

**Referee.** None needed: no designed disagreement between two systems is arbitrated by a third file.

**The cracker sheet.** The cracker filed the golden guarantee, ran the hygiene battery (keys unique, exact duplicates,
every join matched or explained, no fan-out, counts that tie) and executed every filed rule. Every ask row misses:

| Ask figures | The cracker's path | What keeps it wrong | Cracker result |
|---|---|---|---|
| Ask A, 6 lost core-hour figures | resizes applied; each preempted run's training lost from its own newest committed checkpoint | the resumption's restore point, on the resumed run's row, is often an earlier checkpoint | miss |
| Ask A, 6 shares | the same over each team's held core-hours | the same | miss |
| Ask B, 6 machine-hour figures | removals matched to registrations on machine id, duplicates removed | a re-imaged machine returns under a new id, tied to its asset only in the inventory | miss |
| Ask C, 11 charges | daily holdings from the ledger and the change file at request time, the rate by effective date | a change takes effect at the reconciliation run that applied it | miss |

The guarantee, the reservations and the slide's parts belong to the recommendation block, not to the asks, and are
carried by the main call. The mirror sheet (the same response stopped at R0) differs from the cracker sheet only on
the recommendation criteria, so no ask is coupled to the call.

Mirror leakage: 9 per cent of the ask weight (method credit on the ask paths, no figure; the over-cleaner's 3 Ask B
maintenance figures are not on the mirror's path, which matches on machine id).

**Pair arithmetic.** Planning weights 38 recommendation (the guarantee, the storage reservation, the platform total,
the firm total, the slide's parts), 7 instruction following (the two files, the slide's title and axis), 55 asks over
29 figures. The cracker keeps about 9 per cent of the ask weight: C = 38 + 7 + 5.0 = 50.0. The mirror (R0) keeps the
firm total and the slide's firm part, r about 7, and the same 5.0: S = 7 + 7 + 5.0 = 19.0.

Pair ceiling: 34.5

If a strong response cracks Ask C (11 of 29 ask figures, about 21 of 55 points), the cracker rises to about 66 and the
pair to about 42.5; Ask C's device is the one to watch at the leak read. A response that pairs Ask B's removals by rack
keeps 3 of its 6 figures (about 6 points). Recomputed from the generated rubric when it exists.

## Pins

| Pin | Authority | What it fixes | Never says |
|---|---|---|---|
| CS-3 sections 1 to 6 | 1, the standard signed by the head of infrastructure | quarters, reservable cores, firm holds to frozen budgets at the rate in force, platform services at their forecast busiest-hour use, the guarantee as the largest whole thousand left, batch inside its guarantee | how a platform service is forecast, any driver of storage, a 2027 figure |
| The capacity memo | 2 | the quarter's overcommit (1.45) and the machines from the hardware plan | storage, the batch tier's load |
| The hardware plan | 2 | machines in service by date; 5,220 from 28 December 2026 | anything about tenants |
| The finance freeze note and budget workbook | 2 | Q1 2027 monthly budgets held at December 2026 | any reservation |
| The rate card | 2 | EUR per core-month for MAD1 reserved cores by effective date | a reservation |
| The chargeback policy (asks only) | 2 | what a firm tenant pays: the cores it holds at 00:00 UTC each day at the rate in force | when a change takes effect |
| The dictionary | 4 | field semantics: cores in use, machines in service, run, checkpoint and resize fields, machine events, the inventory's cluster ids, quota change and reconciliation fields | what drives storage, how to follow a restore, that a re-image changes an id, when a change applies |

## Prompt

`prompt.txt`, gated by `voice-check.py` (in `precut.py`): the call with its unit and quarter, the workbook with the
reservations the guarantee is struck after and the three 2026 Q3 tables, the slide's named parts, and the rounding once
at the close.

## Build record

- Generator `task140/generator/` (common, world, records, docs, calc, deliver, checks, verify, metadata, postprocess,
  build): `python3 task140/generator/build.py` builds the pack, the goldens, `metadata.json` and `figures.json`, runs
  `checks.py` (every SF row, every rung by name, the grid, the asks' stops, the context artifact, the input gates, the
  realism sweep, the distractor deletions) and the independent `verify.py` (pandas, no shared code), then a second full
  build compared byte for byte, then cuts `target.zip`.
- The pack: 24 files in six formats (csv, pdf, docx, xlsx, json, txt); the spine 239,470 rows; distractors
  `mad1_cells_quarterly_summary_2025-2026.xlsx` and `batch_training_demand_2027H1.pdf`, declared in `metadata.json`,
  each deleted with the call and every ask unchanged (asserted).
- Built figures: the guarantee 109,000 (109,492.0 before the thousand), the firm tenants 576,972, `cell-store` 38,058.5,
  `cell-ctl` 1,999.2, the default path 122,000 (122,235.1).
- Stage 3 gates, 2026-10-12: `build.py` green (2,285 assertions in `checks.py`, the three-rules block R1 to R3c among
  them on the clean truth, `verify.py` agreeing on every graded
  figure, two builds byte-identical, `target.zip` cut); `precut.py` 47 checks, 0 FAIL; `figures_check.py` PASS (89
  figures); `voice-check.py` PASS; `leak.py --asof 2026-12-14` REVIEW, no LEAK (answered under `## Leak review`);
  `guard.py heart` WARN (`overuse.objective`, no BLOCK), `guard.py surface` 0 promoted pairs; the container audit
  (`scrub_producer_metadata.py`) clean on `target/` and `golden/`. Stage 4 (the leak reader and the determinism judge)
  is next.

## Leak review

`leak.py task140 --asof 2026-12-14`: REVIEW, no LEAK. Each REVIEW line:
- Sweep 2, "generator" in the Q3 capacity report and the operations log: the hall's standby generator in the
  19 August power event (the weekly generator test); in-world, harmless.
- Sweep 3, the committed call's words (C-22, guarantee, cores, batch, training, quarter) in CS-3, the memo, the README,
  the capacity report, the chargeback policy and the demand note: the domain's own nouns; no document carries the
  guarantee's figure or any 2027 reservation; harmless.
- Sweep 4, stump-paragraph terms in CS-3, the memo, the README, the capacity report, the operations log, the demand
  note and the prompt's rounding sentence: CS-3 4.1's "use forecast for its busiest hour" is the estimand, not the method,
  and "history" there is the revision history; the memo says only that Compute Operations prepares the platform
  reservations from the monitoring export; the report lists each tenant's busiest hour with no relation between them;
  no document names a driver of `cell-store`, the batch tier's load on it or a joint solve; harmless.
- Sweep 9, dates after 14 December 2026 in the hardware plan (the refresh racks in service from 28 December, the
  2027 Q1 row) and the rate card (rates effective 1 January 2027, published 1 December): forward-looking plan and rates,
  the only two files that carry such dates (asserted in `checks.py`); harmless.

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
- The first built history (the batch guarantee rising from 26,000 to 57,000 cores through 2025 and 2026 while racks
  were added): storage fitted on the batch tier alone landed inside the golden's thousand on the whole history and
  from 2025 Q3 (the history's machines rose with its guarantee, so the batch term carried the machine term forward);
  rebuilt the history so racks were added as the firm tenants grew and the guarantee moved only between 55,000 and
  58,000, which puts the batch-only fit at 111,000 on every window.
- Round storage coefficients (3.0 cores a machine, 0.2 a batch core) with no base load: the platform figures fell near
  their nearest-1,000 edges once the guarantee sat mid-thousand; the world now carries 2.94, 0.208 and a base of 37
  cores, with 5,220 machines in Q1 so the reservable cores' residue lets every graded figure sit mid-bin.
- Checkpoints written with training paused (the state taken at the write, no training during it): the span of training
  done again then started at the write or at the commit, a reading; the dictionary now says training carries on while
  a checkpoint is written, so the state is the write start's.
- Batch scheduler times with seconds on some events and not others (runs started at queue ticks inherited fractional
  submission times; a hit could preempt a run in its first minute): every scheduler time is now on the minute and a
  run is never preempted in its first ten minutes.
- Ask B's over-clean stop as first designed (pair an unmatched removal with the next registration in its rack) was
  claimed to miss all six; pairing inside a rack keeps each month's maintenance total, so it lands on the three
  maintenance figures and misses only the hardware-fault ones (spares in retired machines' racks); recorded as such.
