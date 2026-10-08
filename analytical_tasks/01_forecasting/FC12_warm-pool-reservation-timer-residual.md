# FC12 — The warm-pool memory to reserve for next quarter, when part of the traffic arrives through a path no invocation log records

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · serverless platform capacity |
| Mirrors | Sizing a warm pool or cache when part of the traffic arrives by a path no request log records (scheduled events beside API traffic at AWS Lambda, minimum instances on Google Cloud Run, timer triggers on Azure Functions, internal cron fleets at Meta) |
| Decision shape | One figure committed at a date: the region's warm-pool memory reservation at the quarterly capacity cut-off |
| Committed call | Average warm-pool memory to reserve for next quarter, in TB to the nearest 1, under the newly unified keep-alive policy |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S2, a population that is a residual between two correct records, made decisive by a forward policy that changes what those executions are |
| Gate G mechanism | forecasting, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #4 never tests its reading against the control |
| Calibration form | Existing-book actuals: the book of apps with each closed month's measured warm-pool memory per host cluster and billed executions per app-hour |
| Driving force | Timer-fired executions appear in neither the HTTP log nor the queue log. They show up only as billed executions minus logged ones, app-hour by app-hour. Until now they ran in one-shot containers released on completion, so they hold no warm memory in any closed month. Next quarter's policy keeps every app warm for the 99th percentile of its own gaps. A timer that fires every 30 minutes has a 30-minute gap, so it never goes cold, and those apps become the largest block of idle memory in the pool. |

## 1. Situation

A serverless platform reserves memory for its warm pool, the idle instances kept alive so the next call is not a cold start. From next
quarter one keep-alive policy covers every app: an app's instances stay warm for the 99th percentile of its inter-arrival times over the
training window, capped at 240 minutes. Finance commits the region's average warm-pool reservation at the capacity cut-off. Six closed
months of warm-pool actuals were measured under the old fixed ten-minute policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the HTTP and queue invocation logs, the billing meter, the app registry, the warm-pool actuals and
  the memory-management report. No one's claim about their own numbers is overturned. The difficulty is a population no log contains, and
  which next quarter's policy changes into something else.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The logs replayed under the new policy still reproduce every closed month
  when run under the old one, and still leave out the timer apps.
* **Instrument repair.** Make every log complete for what it records; they are. A perfect HTTP log still records no timer, and a perfect
  closed month still shows timers holding no memory, because they did not.
* **Lens swap.** The naive read and the answer differ in population and moment: the logged apps under an old policy against every app,
  timers included, under the new one.

## 3. The driving force

A strong solver replays both logs under the new policy at the app grain and models memory the way the platform does. Idle instances are
compacted to 40% of their allocation after fifteen minutes, which never happened under a ten-minute policy. Every step reproduces the
closed months, because the closed months contain no long idle and no warm timer. The platform runs a third kind of execution. Timer
triggers fire on a schedule, are logged by neither the HTTP front end nor the queue service, and appear only in the billing meter. Billed
executions minus the two logs, per app-hour, leaves a residual of exactly 2, 4 or 12 an hour for 3,180 apps. These are timers firing
every 30, 15 or 5 minutes. They used to run in one-shot containers. Under the unified policy each such app's window equals its period,
so its instance is warm all quarter. After compaction they add 88 TB, more than everything the logs explain.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Both invocation logs replayed under the new policy, each function with its own instances, at allocated memory, × the filed growth factor | 132 TB, −19% | The adopted policy applied to every logged arrival | The runtime guide: an app is the unit of scaling, and its functions share its instances |
| 1 | The same at the app grain | 100 TB, −38% | The right unit; under the old policy this replay reproduces all six closed months | **E17 (validated on one population, applied to another):** the memory-management report shows idle instances compacted to 40% after 15 minutes, and no closed-month idle ever lasted that long |
| 2 | The same with idle time beyond 15 minutes at 40% of allocation | 74 TB, −54% | Memory modelled for long idles, every log replayed, and the closed months still reproduce exactly | The billing meter: billed executions exceed logged ones by a constant 2, 4 or 12 an hour for 3,180 apps |
| 3 | **Decisive:** add the residual population (billed minus logged executions), with windows equal to each timer's period, warm all quarter, compacted after 15 minutes | **162 TB** | — | — |

* **Figure shape.** Three corrections walk the figure down (−19%, −38%, −54%), and the decisive rung reverses them past the starting
  point. A solver who stops anywhere short under-reserves.
* **Partial correction priced (L3).** Scaling rung 2 by the closed months' ratio of actuals to replay returns 74 TB unchanged, since that
  ratio is exactly 1. Finding the residual but running timers one-shot, as every closed month did, adds only their 4 TB of active memory:
  78 TB (−52%), essentially where rung 2 stood. Finding them but keeping their idle at full allocation gives 218 TB (+35%).
* **Grid.** Grain (function, app) × idle memory (allocated, compacted) × residual (omitted, one-shot, warm) gives 12 cells. The answer is
  the only cell at the app grain with compaction and warm timers. The nearest wrong cell is the function grain with compaction and warm
  timers (186 TB, +15%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy covers "every app". No document mentions timers, says some executions bypass the logs, or says how
   timer executions used to run.
2. **Corpus blind for a computable reason.** *In every closed month timer executions held no warm memory, because they ran in one-shot
   containers released on completion.* The log replay under the old policy reproduces all 72 cluster-months of warm-pool actuals exactly.
3. **No arithmetic symptom.** Logged invocations tie to the front end and queue service, the replay ties to the actuals, and nothing
   fails. The billing meter is reconciled to revenue, never to the logs.
4. **Not a row predicate.** The population is a difference between two records at different grains (billed executions per app-hour,
   logged invocations per function-minute), aggregated to the app before subtracting.
5. **The enumeration is arithmetic.** Which apps carry timers, and at what period, is read from the residual's regularity. No column flags
   them.
6. **No cutover date in any closed series.** The policy starts next quarter. No closed month steps, and the timers' memory exists only
   in the forward window.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The existing book: every app in the region, with six closed months of measured warm-pool memory per host cluster, billed
  executions per app-hour and the app registry's memory sizes.
* **What it certifies.** The app-grain replay under the old policy: 72 of 72 cluster-months to within 0.5%. The function-grain replay
  overshoots every one. A back-tester is confirmed at rungs 1 and 2, since compaction never triggered.
* **What it pins (the residual).** For 3,180 apps the hourly residual is exactly 2, 4 or 12 in every hour of every month, which fixes
  their periods. For every other app it is exactly zero.
* **Twin pair.** Apps A-20817 and A-33092 are identical on every registry and log column: 1.5 GB, the same logged invocations to the
  minute, the same function count and region. Their forward warm memory differs 2.0× because A-20817's residual is 2 an hour, a 30-minute
  timer that keeps its instance warm between sparse logged calls.
* **Resemblance points at the decoy.** The timer apps resemble the book's quiet HTTP apps on every logged column, and those apps' forward
  warm memory is small.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The policy: from next quarter every app's keep-alive window is the 99th percentile of its inter-arrival times over the
  training window, capped at 240 minutes. The runtime guide: an app is the unit of scaling. The planning sheet: a growth factor of 1.05.
  The memory-management report: idle instances are compacted to 40% of allocation after 15 minutes.
* **Empirical pins.** Timer periods, from the residual. Memory sizes, from the app registry. The replay, confirmed on the closed months.
* **Voices.** The platform lead: "The logs are every invocation we serve." The finance partner: "The old policy's actuals are the best
  guide we have; scale them."
* **Licensed wrong basis.** The capacity memo records that finance sizes the reservation on the closed months' actuals scaled by the ratio
  of new-policy to old-policy replays of the logs, and will present that figure at the cut-off.

## 8. Determinism by construction

* **Periods.** Every timer's residual is constant per hour, and periods are 5, 15 or 30 minutes, all below the 240-minute cap, so each
  timer app's window is its period under any percentile convention.
* **Mixed apps.** Apps with both timers and logged traffic take their window from the merged arrival sequence; every such app is warm all
  quarter under either merge order.
* **Compaction.** The report's rule is the platform's, and the replay applies it per idle interval. No idle interval sits within a minute
  of the 15-minute threshold in the replay.
* **Growth.** The filed factor applies uniformly, so it moves no rung relative to another.
* **Maturity.** Billing for the closed months is final, and the logs are complete for the training window.

## 9. Prompt sketch and deliverables

> I sign the warm-pool reservation for next quarter at the capacity cut-off, and once the policy change lands it has to hold. Give me one
> figure, average terabytes, to the nearest one. Our finance partner would like to scale up the old policy's actuals. Send me
> `warm_pool_reservation.xlsx`, a chart `warm_pool_build.png`, and a one-page `reservation_note.pdf`.

* `warm_pool_reservation.xlsx` — the reservation build by app and population, the cold-start sheet (ask A) and the billing sheet (ask B).
* `warm_pool_build.png` — stacked bars by population (logged apps, timer residual) under the four rung constructions, the committed
  reservation as a labelled line, compacted idle memory shaded, and an inset of one 30-minute timer app's warm cycle.
* `reservation_note.pdf` — the committed reservation, the residual population's size, and the basis finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 host clusters, last month's cold starts and their 95th-percentile latency.
  *Device:* a cold start that fails and retries posts two start events, the first with a failure status, and the runtime guide counts one
  cold start per successful start. Counting events overstates cold starts at five clusters and drags their latency percentile down.
* **Ask B (device-carried).** For each host cluster, last month's billed GB-seconds and the share from apps that changed plan during the
  month. *Device:* a mid-month plan change splits the app-month into two prorated billing rows, as the billing dictionary documents.
  Counting rows as apps doubles the plan-change share at four clusters. The hourly execution meter has no plan rows.
* **Ask C (validity).** The reservation under each of the four rung constructions, with each one's reproduction of the 72 closed
  cluster-months.
* **Decoupling.** Dropping the residual population changes no figure in asks A or B.

## 11. Rubric arithmetic

12 clusters × 2 (ask A) + 12 clusters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed reservation, the residual app count and
the timers' share + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Logged apps under the new policy: 38 TB active and 62 TB idle at allocation, 74 TB after compaction. Timer residual: 4 TB active and
  140 TB idle at allocation, 84 TB after compaction.
* Rung figures 132 / 100 / 74 / 162 TB. Partial cells 74, 78 and 218 TB; the function-grain cell with warm timers is 186 TB.
* 3,180 apps carry a residual of exactly 2, 4 or 12 an hour; every other app's residual is zero. A-20817 and A-33092 are identical on
  every registry and log column.
* No closed-month idle interval exceeds ten minutes, and timers held no warm memory in any closed month.
* Retried cold starts and prorated plan rows never touch logs, the execution meter or the registry.
