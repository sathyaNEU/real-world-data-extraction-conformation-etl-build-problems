# FC12 — The warm-pool memory to reserve for next quarter, when a host goes back to general compute only after the last instance placed on it has gone cold

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · serverless platform capacity |
| Mirrors | Sizing a warm pool kept in whole hosts when one idle instance holds its host (AWS Lambda and Cloud Run warm capacity on microVM hosts, Kubernetes node pools that scale a node down only when its last pod is gone, Borg machines held by a single long-lived task) |
| Decision shape | One figure committed at a date: the region's warm-pool memory reservation at the quarterly capacity cut-off |
| Committed call | Average warm-pool memory to reserve for next quarter, in TB to the nearest 1, under the new per-function keep-alive policy |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units: a host returns to general compute only when every instance placed on it has lapsed, recovered by replaying the closed months on the placement log, with a compaction rule validated only on short idles below it |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #2 counts file rows instead of the real unit · #8 papers over a failed reproduction · #13 validates on one population, applies to another |
| Calibration form | Existing-book actuals: the book of apps with their functions and assigned hosts, and each closed month's measured warm-pool memory per host cluster under the old fixed ten-minute keep-alive |
| Driving force | The new policy keeps each function's instances warm for that function's own window, up to four hours, and the runtime runs an app's instances on its assigned host. The warm pool is kept in whole hosts: a host goes back to general compute only when the last instance placed on it has lapsed. No document says so. Only that hold, replayed on the placement log, reproduces all 72 closed cluster-months to the host-hour; instance memory scaled by any ratio misses them. Under the old ten-minute windows a host drained minutes after its apps went quiet. Under the new windows an app with an hourly sync keeps its whole 256 GB host warm through the night, and a nightly export holds its host four hours after the call; 1,130 of the region's 1,300 hosts carry an app whose windows never lapse overnight: 300 TB held against 120 TB of warm instances. |

## 1. Situation

A serverless platform reserves memory for its warm pool, the idle instances kept alive so the next call is not a cold start. From next
quarter one keep-alive policy replaces the old fixed ten minutes: each function's instances stay warm for the 99th percentile of that
function's own inter-arrival times over the training window, capped at 240 minutes. A function's window runs from that function's own last
call, and an instance shared by several functions is released when none of their windows is open. The runtime guide makes the app the unit
of scaling: an app's functions share its instances, and they run on the app's assigned host. Finance commits the region's average
warm-pool reservation at the capacity cut-off. Six closed months of warm-pool actuals were measured under the old policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the invocation logs, the deployment manifests, the placement log, the warm-pool actuals and the
  memory-management report. No one's claim about their own numbers is overturned. The difficulty is what the warm pool holds once its
  instances keep different windows.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The instance build scaled by each cluster's closed ratio still fits every
  closed month within 6% and still says 192 TB.
* **Instrument repair.** No file is suspect: the invocation logs hold every call by function, the manifests every function's app, the
  placement log every app's host on every day of the six months, and the actuals every closed cluster-month's held memory, which is the
  attribute the reservation commits. Take the deepest repair anyway, a host-state log of every host's warm-pool membership minute by
  minute: rungs 0–2 still return 160, 120 and 192 TB, since none of them reads it, and next quarter's hold still has to be built from
  placement and the new windows for 300.
* **Lens swap.** The naive read and the answer differ in population: the memory of the warm instances, against the memory of the hosts
  they hold, each held until the last instance placed on it lapses.

## 3. The driving force

A strong solver implements the new policy as written: each function's window from its own calls, each app's shared instance released
when none of its functions' windows is open, idle instances compacted to 40% after fifteen minutes. That is 120 TB of warm instances. It
then back-tests against the closed months, and the instance replay falls short of every month's warm-pool actuals, by a ratio that moves
between 1.25 and 2.60. Scaling each cluster by its own ratio fits every closed month within 6% and says 192 TB. The ratio is not a
constant. The platform keeps the warm pool in whole hosts, and a host goes back to general compute only when the last instance placed on
it has lapsed. No document says so. It is recovered by replaying the placement log, under which the closed actuals reproduce to the
host-hour in 72 of 72 cluster-months. Under the old ten-minute windows a host drained minutes after its apps went quiet. Under the new
windows an app with an hourly sync keeps its host warm through the night, because each call lands inside the last call's window, and a
nightly export holds its host four hours after the call. 1,130 of the region's 1,300 hosts carry an app whose windows never lapse
overnight. A whole 256 GB host stays reserved for a few gigabytes of idle instances, and compaction frees none of it.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The policy and the runtime guide implemented literally: each function's window from its own calls, each app's shared instance warm until none of its functions' windows is open, at allocated memory, × the filed growth factor | 160 TB, −47% | Every filed sentence implemented, at the unit the runtime guide names | **E17 (validated on one population, applied to another):** the memory-management report compacts idle instances to 40% after 15 minutes, and no closed-month idle lasted that long |
| 1 | The same with idle time beyond 15 minutes at 40% of allocation | 120 TB, −60% | Memory modelled as the platform manages it, every log replayed | The closed actuals: the instance replay falls 20–61% short of every cluster-month's warm-pool memory, by a ratio that moves between 1.25 and 2.60 |
| 2 | The instance build scaled by each cluster's closed ratio of actuals to instance replay (mean 1.60) | 192 TB, −36% | Back-tested: each cluster's ratio fits its six closed months within 6% | The placement log: clusters C-03 and C-09 match on every replay column and differ 2.0× in actuals, and C-09's night-active apps sit one to a host where C-03's share eight hosts |
| 3 | **Decisive:** each host held whole from its first warm instance until the last instance placed on it lapses, placement from the placement log, instances under the new windows; compaction frees no host | **300 TB** | — | — |

* **Figure shape.** Every lower rung counts instances, not held hosts, and sits 36–60% under the answer, which is the largest cell of the
  grid. Compaction lowers the instance figure, the closed ratio lifts it back, and only the host hold reaches 300.
* **Partial correction priced (L3).** A solver who finds the hold but lets compaction release a host once every instance on it is
  compacted gets 175 TB (−42%). One who holds hosts but assumes the scheduler consolidates idle instances overnight gets 150 TB (−50%).
  Carrying the closed months' hold forward at the filed growth factor gives 154 TB (−49%). Reading the policy function by function, each
  function on its own instances, gives 230 TB at allocation (−23%).
* **Grid.** Memory (allocated, compacted) × accounting (instance memory, instance memory × each cluster's closed ratio, instances packed
  into whole hosts, host hold on the placement log) gives 8 cells: 160, 120, 256, 192, 168, 126, 300 and 300 TB. Compaction frees no held
  host, so both host-hold cells are the answer. The nearest other cell is the closed ratio on allocated memory, 256 TB (−15%), which is
  also the finance basis.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the per-function windows and the release of a shared instance, and the runtime guide puts an
   app's instances on its assigned host. No document says the warm pool is kept in whole hosts, or that a host returns to general compute
   only when the last instance placed on it has lapsed.
2. **The reproduction numbers.** The host hold on the placement log reproduces 72 of 72 closed cluster-months to the host-hour. The
   instance replay reproduces none, each cluster's own ratio none exactly (it fits within 6%), and instances packed into whole hosts none.
   The rule is a construction: the placement log's app-to-host assignments joined to each app's instance intervals, the latest lapse per
   host, held hours × host memory. It means nothing without the placement join, and no ratio or packing sweep reaches it.
3. **No arithmetic symptom.** Calls tie to the front end and the queue service, every function maps to one app and every app to one host,
   and the actuals tie to the platform's capacity statement under every rung.
4. **Not a row predicate.** A host's hold is a maximum over the instances placed on it, each instance's warm interval a union of its
   functions' windows, joined through the manifests and the placement log. No row carries it.
5. **The enumeration is arithmetic.** Which hosts an app keeps warm overnight, and for how long, is computed from placement and calls. No
   column says "held".
6. **No cutover date in any closed series.** The policy starts next quarter and no closed month steps. The whole-host hold applied in
   every closed month; the new windows only lengthen what it holds.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The existing book: every app in the region with its functions (manifests) and assigned host (placement log), every call by
  function, and six closed months of measured warm-pool memory per host cluster.
* **What it pins (Pattern B).** The whole-host hold, 72 of 72 cluster-months to the host-hour. Each cluster's ratio of actuals to
  instance replay fits its own months within 6%, which is why rung 2 feels confirmed.
* **Free training instance (O3).** In every closed month the 140 night-batch apps, called every few minutes through the night, kept
  their hosts warm until dawn. The hold is visible there and harmless, because they sit on few hosts.
* **Twin pair.** Clusters C-03 and C-09 in the same closed month are identical on every column of the instance replay: host count, app
  count, calls by hour, allocated and compacted instance memory (7.6 TB). Their actuals were 9.8 and 19.6 TB (2.0×), because C-09's
  80 night-active apps sit one to a host and C-03's share eight hosts. The instance replay and any common ratio give both one figure;
  only the host hold reproduces both.
* **Resemblance points at the decoy.** Next quarter's instance build resembles the busiest closed months on every replay column, and their
  ratio of actuals to instance memory was the book's mean, 1.60.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The policy: from next quarter each function's instances stay warm for the 99th percentile of its own inter-arrival
  times over the training window, capped at 240 minutes; a function's window runs from that function's own last call, and an instance
  shared by several functions is released when none of their windows is open. The runtime guide: an app is the unit of scaling, its
  functions share its instances, and they run on the app's assigned host. The planning sheet: a growth factor of 1.05 on calls. The
  memory-management report: idle instances are compacted to 40% of allocation after 15 minutes. The capacity memo: the reservation is the
  region's average warm-pool memory over the quarter.
* **Empirical pins.** Each function's window, from its own calls. Each function's app, from the manifests. Each app's host, from the
  placement log. The whole-host hold, from the closed actuals.
* **Voices.** The platform lead: "The warm pool is the instances in it. Size the instances and you have sized the pool." The finance
  partner: "The old policy's actuals are the best guide we have; scale them."
* **Licensed wrong basis.** The capacity memo records that finance sizes the reservation on the closed months' actuals scaled by the ratio
  of new-policy to old-policy instance replays, and will present that figure at the cut-off.

## 8. Determinism by construction

* **Windows.** Every sparse function's 99th-percentile gap exceeds 240 minutes under inclusive, exclusive and nearest-rank conventions,
  so it sits at the cap, and every busy function's window is under two minutes under all three.
* **Release.** The policy's release clause fixes each instance's warm interval: the latest of its functions' expiries, each counted from
  that function's own last call. It rules out the merged-gap, longest-window and average-window readings of an app's window, which
  anchor a window on other functions' calls.
* **Hold.** The closed actuals pin the hold to the host-hour: a host is held from the first instance placed on it until the last lapses.
  No warm instance moved between hosts in six months, so no overnight consolidation applies.
* **Placement.** Next quarter's placement is the log's at the cut-off. The log moves an app only when its host is retired, and the
  hardware plan retires none next quarter.
* **Compaction and growth.** Compaction changes the instance rungs only; no idle interval sits within a minute of the 15-minute threshold.
  The hold moves by under 1% between growth factors of 1.00 and 1.10, because night holds are set by placement, not call volume.
* **Maturity.** Billing, logs and placement for the closed months are final, and the training window is complete.

## 9. Prompt sketch and deliverables

> I sign the warm-pool reservation for next quarter at the capacity cut-off, and once the policy change lands it has to hold. Give me one
> figure, average terabytes, to the nearest one. Our finance partner would like to scale up the old policy's actuals. Send me
> `warm_pool_reservation.xlsx`, a chart `warm_pool_build.png`, and a one-page `reservation_note.pdf`.

* `warm_pool_reservation.xlsx` — the reservation build by cluster and construction, the cold-start sheet (ask A) and the billing sheet
  (ask B).
* `warm_pool_build.png` — stacked bars (active instances, idle instances, held host memory beyond instances) under the four rung
  constructions, the committed reservation as a labelled line, hosts held overnight counted per cluster, and an inset of one host's day
  with each placed app's warm intervals drawn.
* `reservation_note.pdf` — the committed reservation, the host memory held beyond warm instances, and the basis finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 host clusters, last month's cold starts and their 95th-percentile latency.
  *Device:* a cold start that fails and retries posts two start events, the first with a failure status, and the runtime guide counts one
  cold start per successful start. Counting events overstates cold starts at five clusters and drags their latency percentile down.
* **Ask B (device-carried).** For each host cluster, last month's billed GB-seconds and the share from apps that changed plan during the
  month. *Device:* a mid-month plan change splits the app-month into two prorated billing rows, as the billing dictionary documents.
  Counting rows as apps doubles the plan-change share at four clusters. The replay never reads billing rows or start events.
* **Ask C (validity).** The reservation under each of the four rung constructions, with each one's reproduction of the 72 closed
  cluster-months.
* **Decoupling.** Replacing the host hold with instance memory scaled by the closed ratio changes no figure in asks A or B.

## 11. Rubric arithmetic

12 clusters × 2 (ask A) + 12 clusters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed reservation, the held memory beyond warm
instances and the count of hosts held overnight + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Region: 1,300 warm-pool hosts of 256 GB in 12 clusters, about 55 apps placed on each host.
* Closed months (old policy): instance replay 92 TB on average, actuals 147 TB; ratio of actuals to instance replay 1.25–2.60 by
  cluster-month, mean 1.60, each cluster within 6% of its own mean.
* Next quarter: instances 160 TB at allocation and 120 TB compacted; host hold 300 TB, with 1,130 hosts carrying an app whose windows keep
  an instance warm through every night. Partials 175, 150, 154 and 230 TB; grid cells 256, 168 and 126 TB.
* C-03 and C-09 are identical on every replay column in one closed month (7.6 TB of instances; actuals 9.8 and 19.6 TB).
* No warm instance moves between hosts. Retried cold starts and prorated plan rows never touch calls, manifests, placement or actuals.
