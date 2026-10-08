# FC12 — The warm-pool memory to reserve for next quarter, when an app's shared instance can go cold only after its sparsest function has

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Product Analytics · serverless platform capacity |
| Mirrors | Sizing a warm pool when the functions sharing an instance each set their own keep-alive (AWS Lambda and Google Cloud Run instances shared across routes, Azure Functions apps hosting many functions, Kubernetes pods held alive by their longest-lived container) |
| Decision shape | One figure committed at a date: the region's warm-pool memory reservation at the quarterly capacity cut-off |
| Committed call | Average warm-pool memory to reserve for next quarter, in TB to the nearest 1, under the new per-function keep-alive policy |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units: a shared instance is released only when every function it hosts has passed its own keep-alive, so an app's warm time follows its sparsest function, with a compaction rule validated only on short idles below it |
| Gate G mechanism | forecasting, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #2 counts file rows instead of the real unit · #7 uses the ready-made measure |
| Calibration form | Existing-book actuals: the book of apps with each closed month's measured warm-pool memory per host cluster, under the old fixed ten-minute keep-alive |
| Driving force | From next quarter each function stays warm for the 99th percentile of its own gaps between calls, and the functions of an app share the app's instances. A shared instance can be released only when every function it hosts has passed its own window, so an app with a busy endpoint and a nightly admin function stays warm four hours after the nightly call. Under the old policy every function's window was the same ten minutes, so every reading of "the app's window" reproduced every closed month. The functions an app hosts come from the deployment manifests, not from any registry column. |

## 1. Situation

A serverless platform reserves memory for its warm pool, the idle instances kept alive so the next call is not a cold start. From next
quarter one keep-alive policy replaces the old fixed ten minutes: each function's instances stay warm for the 99th percentile of that
function's own inter-arrival times over the training window, capped at 240 minutes. A function's window runs from that function's own last
call, and an instance shared by several functions is released when none of their windows is open. The runtime guide makes the app the unit
of scaling, so an app's functions run in the app's instances. Finance commits the region's average warm-pool reservation at the capacity
cut-off. Six closed months of warm-pool actuals were measured under the old policy.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the invocation logs, the deployment manifests, the app registry, the warm-pool actuals and the
  memory-management report. No one's claim about their own numbers is overturned. The difficulty is when a shared instance may go cold
  once its functions keep different windows.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The app-grain replay with one window per app still reproduces every closed
  month and still says 74 TB.
* **Instrument repair.** No file is suspect: the invocation logs hold every call by function and trigger, the manifests every function's
  app, and the actuals every closed cluster-month. On perfect records rungs 0–2 still return 230, 96 and 74 TB, because under the old
  policy every function had the same ten-minute window, so no closed month shows an instance held open by its sparsest function.
* **Lens swap.** The naive read and the answer differ in moment and rule: instances released ten minutes after an app's last call, against
  instances released only when each hosted function's own window has run out.

## 3. The driving force

A strong solver replays the logs under the new policy at the app grain, as the runtime guide requires, gives each app the window its merged
calls imply, and models memory the way the platform does: idle instances compacted to 40% after fifteen minutes. Every closed month
reproduces, because every function's window was ten minutes. Next quarter the windows are per function. A typical app has a busy endpoint,
whose gaps are seconds, and a few sparse functions: a nightly export, an hourly sync, an admin page, whose 99th-percentile gaps reach the
240-minute cap. The app's instance serves all of them, and the policy releases a shared instance only when none of its functions' windows
is open, each running from that function's own last call. The policy says no more than that. Composed with the calls, it keeps the instance
warm until the last of the per-function windows lapses, four hours after a nightly export. 2,400 apps host functions whose windows differ
by more than an hour. The function lists come from the manifests, and each function's window from its own calls.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Every function replayed under its own window with its own instances, at allocated memory, × the filed growth factor | 230 TB, +95% | The new policy read literally, function by function | The runtime guide: an app is the unit of scaling, and its functions share its instances |
| 1 | The app grain, each app warm for the 99th percentile of its merged inter-arrival times | 96 TB, −19% | The right unit, and a replay that reproduces all 72 closed cluster-months; in every one of them the merged window and "none open" were the same release | **E17 (validated on one population, applied to another):** the memory-management report compacts idle instances to 40% after 15 minutes, and no closed-month idle lasted that long |
| 2 | The same with idle time beyond 15 minutes at 40% of allocation | 74 TB, −37% | Memory modelled for long idles, every log replayed, and the closed months still reproduce exactly | The manifests against the policy's per-function windows: 2,400 apps host functions whose own windows differ by more than an hour, so on their shared instances "none open" outlasts the merged window by hours |
| 3 | **Decisive:** each app's instance held warm until every hosted function's own window since its own last call has lapsed, compacted after 15 minutes | **118 TB** | — | — |

* **Figure shape.** The corrections walk the figure down (+95%, −19%, −37%) and the decisive rung turns it back up by 59%. A solver who
  stops short of it under-reserves.
* **Partial correction priced (L3).** Giving each app its longest function window after every call, against the policy's own-last-call
  anchor, keeps instances warm through every busy afternoon: 138 TB (+17%). Giving it the average of its functions' windows releases
  instances while a sparse function's window is still open: 92 TB (−22%).
* **Grid.** Grain (function, app) × window law at the app grain (merged calls, average of functions, every function's own expiry,
  longest window after any call) × idle memory (allocated, compacted) gives 10 cells: 230, 154, 96, 74, 130, 92, 180, 118, 220 and 138
  TB. The nearest wrong cell is the average window at allocated memory, 130 TB (+10%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy states the release rule in its own words: a function's window runs from its own last call, and a
   shared instance is released when none of its functions' windows is open. The runtime guide shares instances per app. No document says
   what the two do to an app whose busy and sparse functions share an instance: that its warm time follows its sparsest function, that a
   nightly export holds it four hours after the call, or how much memory that holds. The closed months cannot show it.
2. **Corpus blind for a computable reason.** *In every closed month every function's window was the same ten minutes, because the old
   policy was fixed, so an instance's release ten minutes after its last call satisfied every function at once.* The app-grain replay
   reproduces all 72 cluster-months within 0.5% under every window law.
3. **No arithmetic symptom.** Calls tie to the front end and the queue service, the replay ties to the actuals, and every function maps
   to one app in the manifests, under every rung.
4. **Not a row predicate.** An app's warm time is a maximum over its functions of each function's last call plus its own window, each
   window an order statistic of that function's gaps, then compacted. No row or flag carries it.
5. **The enumeration is arithmetic.** Which apps a sparse function holds open, and for how long, is computed from manifests and calls. The
   registry carries no function count.
6. **No cutover date in any closed series.** The policy starts next quarter, and no closed month steps; the held-open memory exists only
   in the forward window.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The existing book: every app in the region, with six closed months of measured warm-pool memory per host cluster, every call
  by function, the manifests and the registry's memory sizes.
* **What it certifies.** The app-grain replay with compaction rules as the platform applies them: 72 of 72 cluster-months within 0.5%.
  The function-grain replay overshoots every one. A back-tester is confirmed at rungs 1 and 2.
* **What it is blind to.** Window laws: with every window at ten minutes, the merged, averaged, every-function and longest-window readings
  give identical closed months.
* **Twin pair.** Apps A-20817 and A-33092 are identical on every registry and app-level log column: 1.5 GB, two functions, the same
  calls per day within one, busy from 09:00 to 13:00. A-20817's second function is a nightly export, and A-33092's is called with the
  first. Their forward warm memory differs 2.0× (eight warm hours a day against four), and in every closed month it was the same.
* **Resemblance points at the decoy.** The multi-function apps resemble the book's single-function apps on every app-level column, and
  for those apps every window law gives the same forward memory.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The policy: from next quarter each function's instances stay warm for the 99th percentile of its own inter-arrival
  times over the training window, capped at 240 minutes; a function's window runs from that function's own last call, and an instance
  shared by several functions is released when none of their windows is open. The runtime guide: an app is the unit of scaling, and its
  functions share its instances. The planning sheet: a growth factor of 1.05. The memory-management report: idle instances are compacted
  to 40% of allocation after 15 minutes.
* **Empirical pins.** Each function's window, from its own calls. Each function's app, from the manifests. The replay, confirmed on the
  closed months.
* **Voices.** The platform lead: "An instance goes cold when its app's traffic stops; that's how it has always worked." The finance
  partner: "The old policy's actuals are the best guide we have; scale them."
* **Licensed wrong basis.** The capacity memo records that finance sizes the reservation on the closed months' actuals scaled by the ratio
  of new-policy to old-policy replays, and will present that figure at the cut-off.

## 8. Determinism by construction

* **Windows.** Every sparse function's 99th-percentile gap exceeds 240 minutes under inclusive, exclusive and nearest-rank conventions,
  so it sits at the cap, and every busy function's window is under two minutes under all three.
* **Release.** The policy's release clause admits one release time for a shared instance: the latest of its functions' expiries, each
  counted from that function's own last call. It rules out the merged-gap reading, whose single window is an order statistic of the
  app's merged calls run from the app's last call of any function, and the longest-window reading, which runs the longest function window
  from the app's last call of any function; both anchor a window on other functions' calls. The average-window reading fails the same
  test.
* **Compaction.** The report's rule is the platform's, and the replay applies it per idle interval; no idle interval sits within a minute
  of the 15-minute threshold.
* **Growth.** The filed factor applies uniformly, so it moves no rung relative to another.
* **Maturity.** Billing and logs for the closed months are final, and the training window is complete.

## 9. Prompt sketch and deliverables

> I sign the warm-pool reservation for next quarter at the capacity cut-off, and once the policy change lands it has to hold. Give me one
> figure, average terabytes, to the nearest one. Our finance partner would like to scale up the old policy's actuals. Send me
> `warm_pool_reservation.xlsx`, a chart `warm_pool_build.png`, and a one-page `reservation_note.pdf`.

* `warm_pool_reservation.xlsx` — the reservation build by app and window law, the cold-start sheet (ask A) and the billing sheet
  (ask B).
* `warm_pool_build.png` — stacked bars (active, idle at allocation, idle compacted) under the four rung constructions, the committed
  reservation as a labelled line, multi-function apps shaded, and an inset of one app's day with each function's window drawn.
* `reservation_note.pdf` — the committed reservation, the memory held open by sparse functions, and the basis finance will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 12 host clusters, last month's cold starts and their 95th-percentile latency.
  *Device:* a cold start that fails and retries posts two start events, the first with a failure status, and the runtime guide counts one
  cold start per successful start. Counting events overstates cold starts at five clusters and drags their latency percentile down.
* **Ask B (device-carried).** For each host cluster, last month's billed GB-seconds and the share from apps that changed plan during the
  month. *Device:* a mid-month plan change splits the app-month into two prorated billing rows, as the billing dictionary documents.
  Counting rows as apps doubles the plan-change share at four clusters. The replay never reads billing rows.
* **Ask C (validity).** The reservation under each of the four rung constructions, with each one's reproduction of the 72 closed
  cluster-months.
* **Decoupling.** Replacing the every-function release with one window per app changes no figure in asks A or B.

## 11. Rubric arithmetic

12 clusters × 2 (ask A) + 12 clusters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed reservation, the held-open memory and the
count of apps it comes from + 5 named chart parts + 3 files ≈ 67 criteria.

## 12. World-building constraints

* Components (TB): active 30 (50 at the function grain); single-function apps' idle 40 at allocation, 28 compacted; multi-function apps'
  idle by window law at allocation and compacted: merged calls 26/16, average 60/34, every function's expiry 110/60, longest window after
  any call 150/80, function grain 140/76.
* Rung figures 230 / 96 / 74 / 118 TB; partial cells 138 and 92; nearest grid cell 130.
* 2,400 apps host functions whose windows differ by more than an hour; sparse functions sit at the 240-minute cap.
* A-20817 and A-33092 are identical on every registry and app-level log column.
* No closed-month idle interval exceeds ten minutes. Retried cold starts and prorated plan rows never touch calls, manifests or windows.
