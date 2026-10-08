# DS18 — What read load the feed cache will pass to the store next quarter, when the pods can power only half the hosts the plan adds

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · platform infrastructure capacity planning |
| Mirrors | Cache and CDN capacity planning when data-centre power caps what can actually be deployed (Meta's memcache tiers, Twitter's Twemcache clusters, managed in-memory cache services, CDN edge memory) |
| Decision shape | One figure at a date: the peak read load the feed cache will pass to the backing store next quarter, which the database team provisions against |
| Committed call | Next quarter's peak backend read load, in thousands of reads per second to the nearest five thousand |
| Gap · Pattern | Gap 1 (time) over Gap 3 (objective) · measured #10's architecture (a limit in an operational register, applied in the figure), with the quiet second trap (#11) at rung 2 |
| Gate G mechanism | binding_constraint, with forecasting |
| Measured traps engaged | #10 notes a binding limit as a risk · #11 beats the headline trap, misses the quiet one · #7 uses the ready-made measure · #4 never tests its reading against the control |
| Calibration form | Change-log natural experiments: seven past resizes of this cluster and two siblings, each with peak-hour hit ratios for the fortnight before and after |
| Driving force | The capacity plan grows the cluster from 48 to 80 hosts. The facilities standard requires each pod's peak load to fit on one of its two power feeds, and on that basis the four pods take only 16 more hosts, so next quarter's cluster holds 10.24 TB, not 12.8. A solver who beats the capacity model with the trace and strips the trace's post-restart warm-up has every number right at the planned memory and notes power as a risk. The figure moves only when the limit sets the memory, and the steady-state miss ratio there is 4.2%, not 3.1%. |

## 1. Situation

A social platform's feed cache sits in front of the timeline store. Every GET that misses reads the store once, and the database team must
provision the store for next quarter's peak, forecast at 5.0 million GETs a second. The cluster runs 48 hosts with 160 GB of usable memory
each, in four pods of one fabric block. The capacity model fits a Zipf law to object popularity and computes LRU hit ratios under
independent requests, and it sized next quarter's plan at 80 hosts (12.8 TB) to hold 95%. The team also has a one-day request trace from
last month, the change log of past resizes, the facilities register and the hardware catalogue. The database lead wants one number.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. That covers the capacity model's 95% (right under its
  assumptions), the trace, the change log's hit ratios, the facilities register's pod draws and feed ratings, and the plan's host count.
  The difficulty is that the cluster the plan describes cannot be built, and nothing in the plan says so.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the infrastructure lead's view and the capacity model. A trace-driven miss ratio at the planned 12.8 TB still
  gives a confident figure, and every pod still shows ample power against its two feeds.
* **Instrument repair.** No file the ladder uses is suspect: the trace records every request of its day, the restart's cold hours
  included, and the change log, the facilities register and the hardware catalogue are complete and exact. The nearest thing to a
  repair, a trace from a day without a restart, moves rung 1 to rung 2's 155 and leaves rung 0 at 250 and rung 2 at 155; exact power
  metering moves no pod's headroom. No rung below the decisive one gives 210, and the single-feed limit is still needed to set the memory.
* **Lens swap.** The naive read prices the cluster the plan describes. The answer prices the cluster next quarter can hold, a different
  host population at the moment the load arrives.

## 3. The driving force

A strong solver distrusts the capacity model, replays the trace through an LRU cache by bytes, and finds the real hit ratio higher, because
requests come in bursts. It notices that the trace day began with a rolling restart, and it measures the warm cache at the evening peak, as
the change log's resize records are measured. That curve reproduces every past resize. At 12.8 TB it gives a 3.1% miss ratio, or 155
thousand reads a second. Each step is competent. A power check against the facilities register looks clean too, since each pod has two 10 kW feeds
and draws 7.5 to 9.1 kW. But the facilities standard requires a pod's peak load to fit on one feed, so a failed feed can never drop the pod. On that
basis the four pods have room for 4, 2, 6 and 4 more hosts at 0.38 kW each: 16, not the plan's 32. The capacity policy says deployments
must fit the facilities register. Next quarter's cluster is 64 hosts holding 10.24 TB, where the steady-state miss ratio is 4.2%.

## 4. The ladder

| Rung | Construction | Figure (k reads/s) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Capacity model (Zipf, independent requests) at the planned 12.8 TB: 95.0% hits | 250 | The model the plan was sized with | The change log: the model mispredicts every past resize, by 40–60% of the measured gain |
| 1 | Trace-driven LRU by bytes at 12.8 TB, hit ratio over the whole trace day (96.3%) | 185 | Real requests, real sizes, and the loud decoy beaten | The change log: the trace day opens with a rolling restart at 03:10, and every resize's hit ratios are peak-hour figures on a warm cache |
| 2 | Same replay, warm cache measured at the evening peak (96.9%), the power limit noted as a risk (#10) | 155 | The curve reproduces all seven past resizes, and the facilities register shows two feeds per pod with room to spare | The facilities standard: a pod's peak load must fit on one feed, which leaves room for 16 new hosts, not 32 |
| 3 | **Decisive:** deployable memory from single-feed headroom (64 hosts, 10.24 TB), then the warm peak-hour miss ratio there (4.2%) | **210** | — | — |

* **Walk and reversal.** The corrections walk one way, 250 → 185 → 155 (offsets −65 and −30), as the trace and then the warm window raise
  the hit ratio. The decisive move reverses them by +55, because the memory that sets the hit ratio shrinks by a fifth.
* **Partial correction priced (L3).** Applying the power limit on both feeds' rating leaves the plan intact and lands on 155 (−26%).
  Applying the single-feed limit but keeping the whole-day replay lands on 237.5 (+13%). Applying it to the capacity model lands on 320
  (+52%). The warm replay without the limit is rung 2 (−26%).
* **Grid.** Model (capacity model, whole-day replay, warm peak-hour replay) × memory (planned 12.8 TB, deployable 10.24 TB) gives 6
  cells: 250, 185, 155, 320, 237.5 and 210. The nearest wrong cells are the whole-day replay at the planned memory (185, −11.9%) and at the
  deployable memory (237.5, +13.1%); each costs one omission, the limit or the warm window.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The plan lists 80 hosts, eight new ones per pod, and says nothing about power. The single-feed requirement sits in the
   facilities standard's redundancy chapter, and no document converts it into hosts or memory.
2. **No sweepable corpus nominates it.** *In every resize in the change log the deployed memory equalled the planned memory, because every
   past resize swapped hosts one for one or removed hosts.* No closed resize ever met a pod's single-feed headroom, so the change log
   certifies the curve and is silent on the limit.
3. **No arithmetic symptom.** Every pod's draw is under its two-feed rating, the plan's host count is internally consistent, and the
   replay reproduces every resize.
4. **Not a row predicate.** It needs each pod's single-feed headroom, a floor division by the catalogue's peak draw, a sum over the fabric
   block's pods, and a fresh read of the miss-ratio curve at the memory that results.
5. **The enumeration is arithmetic.** No file states 64 hosts or 10.24 TB; both fall out of the register and the catalogue.
6. **No cutover date.** The constraint is a standing standard, and nothing in any outcome series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The change log: seven past resizes of this cluster and two siblings, each with its date, hosts before and after, and the
  peak-hour hit ratio averaged over the fortnight before and the fortnight after.
* **What it certifies.** The warm peak-hour replay reproduces all seven measured changes to within 0.05 points. The whole-day replay gets
  every change's direction right but every level 0.5–0.6 points low. The capacity model misses every change by 40–60% of its size.
* **What it is blind to.** Deployability (property 2).
* **Twin pair.** Resizes R3 and R6 are identical on every change-log column: 40 to 48 hosts, 6.4 to 7.68 TB, 95.9% before, the same
  request rate. Their measured gains are +0.8 and +0.4 points (2.0×). The capacity model predicts +0.6 for both; only each cluster's own
  warm replay separates them, because R3's working set had a knee just above 6.4 TB.
* **Every rule exercised.** Two resizes fell in weeks with a rolling restart and five did not, so the warm window is tested both ways. One
  resize removed hosts, so the curve is tested in both directions.
* **Resemblance points at the decoy.** The planned growth (48 to 80 hosts) resembles last year's sibling resize, which deployed in full in
  a fabric block with newer pods.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity policy: deployments must fit the facilities register. The facilities standard: a pod's peak load must fit
  on one feed, budgeted at the hardware catalogue's peak draw. The network standard: a cluster's hosts stay within one fabric block. The
  traffic forecast: 5.0 million GETs a second at next quarter's peak. One sentence each.
* **Empirical pins.** The warm peak-hour curve, from the change log.
* **Voices.** The infrastructure lead: "Memory is cheap; the plan already holds 95%." The site reliability lead: "Our hit ratio has never
  fallen after a resize." The database lead: "Give us one number and we'll build for it."
* **Licensed wrong basis.** The capacity policy records that the quarterly infrastructure review reads clusters on the capacity model's hit
  ratio at planned memory and will see that basis.

## 8. Determinism by construction

* **Replay.** LRU by bytes over the cluster's memory; keys hash evenly across identical hosts, so per-host caches and one pooled cache agree
  to within 0.02 points.
* **Warm window.** The restart ends at 03:40 and the cache is full by 09:00, so any peak window from 18:00 to 23:00 gives the same ratio.
* **Headroom.** Every pod's single-feed headroom sits mid-way between whole multiples of 0.38 kW (4.50, 2.50, 6.50 and 4.45 hosts), so
  rounding the draw changes no host count.
* **Reads per miss.** The client library reads through, one store read per GET miss, with no negative caching.
* **Rounding.** The figure is filed to the nearest five thousand (210), and no other cell lies within 11%.

## 9. Prompt sketch and deliverables

> The database team needs one number from us: the peak read load our feed cache will pass to the timeline store next quarter. Our
> infrastructure lead says memory is cheap and the plan already holds 95%. Give me that peak load in thousands of reads a second, to the
> nearest five thousand, in a line I can send the database lead. Send `cache_load.xlsx`, a chart `miss_curve.png`, and a one-page
> `load_note.pdf`.

* `cache_load.xlsx` — the six model × memory cells, the latency sheet (ask A), the client sheet (ask B) and the resize sheet (ask C).
* `miss_curve.png` — the capacity model's curve, the whole-day replay and the warm peak-hour replay against cluster memory, with the planned
  12.8 TB and the deployable 10.24 TB as labelled vertical lines and the committed miss ratio marked, plus an inset of the four pods'
  single-feed headroom in hosts.
* `load_note.pdf` — the committed load, the deployable host count, and why the plan's cluster cannot be built.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Weekly p99 GET latency at the client over the last twelve weeks. *Device:* the client library logs
  one row per multi-get batch with a key count, as its telemetry guide documents. Taking percentiles over rows instead of keys understates
  the p99 in the six busiest weeks.
* **Ask B (device-carried).** Distinct client services calling the cluster, by month, over the last six months. *Device:* a service
  renamed in the platform migration appears under both identifiers, linked in the service registry's alias table. Counting identifiers
  double-counts nine services.
* **Ask C (validity).** The six model × memory loads, and each past resize's predicted change under the three models against its measured
  change.
* **Decoupling.** Clearing the single-feed limit and the warm window changes no figure in asks A or B. Latency rows and service identifiers
  never enter a miss ratio or a host count.

## 11. Rubric arithmetic

6 model × memory cells + 7 resizes × 3 models (ask C) + 12 weekly latencies (ask A) + 6 monthly service counts (ask B) + the committed load,
the deployable hosts and memory, and the miss ratio + 5 named chart parts + 3 files ≈ 57 criteria.

## 12. World-building constraints

* Peak 5.0 million GETs a second. Miss ratios: capacity model 5.0% (plan) and 6.4% (deployable); whole-day replay 3.7% and 4.75%; warm
  peak-hour replay 3.1% and 4.2%. Loads 250, 320, 185, 237.5, 155 and 210 thousand reads a second.
* Pods draw 8.29, 9.05, 7.53 and 8.31 kW at peak on two 10 kW feeds; new hosts draw 0.38 kW at peak and hold 160 GB. Single-feed
  headroom fits 4, 2, 6 and 4 hosts; both feeds would fit all 32 the plan adds.
* The trace day's rolling restart runs 03:10–03:40. The warm replay reproduces all seven resizes within 0.05 points; R3 and R6 are
  identical on every change-log column with gains 2.0× apart.
* Latency rows and service aliases never touch the trace, the change log or the facilities register.
