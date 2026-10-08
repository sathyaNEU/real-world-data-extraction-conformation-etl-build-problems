# DA47 — How many reserved GPU nodes the platform can reclaim next quarter, when a node is idle only if every GPU is idle every hour

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Product Analytics · ML infrastructure capacity planning |
| Mirrors | Reclaiming reserved compute or licences that averages call idle (reserved cloud instances pinned by one service, enterprise seats used by one weekly job, internal GPU fleets at large AI labs), where one busy slot keeps the whole unit |
| Decision shape | One figure committed at a date: the nodes reclaimed into the shared pool in the capacity plan signed on 1 July |
| Committed call | Reserved nodes reclaimable next quarter, as a whole number |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · a minimum over sub-units (E30) recovered from the reclaim book, with a flag-suggested population corrected at rung 1 (measured #5) |
| Gate G mechanism | method_or_model_selection, with binding_constraint support |
| Measured traps engaged | #5 takes the population a flag suggests · #7 uses the ready-made measure · #4 never tests its reading against the control |
| Calibration form | Existing-book actuals: six past quarterly reclaim reviews, 1,820 node decisions with whether each reclaimed node was handed back on escalation |
| Driving force | Reclaims take whole nodes. A node stays reclaimed only if each of its eight GPUs sat below 10% utilisation in every hour of the 28-day window: one pinned inference GPU, or one nightly batch hour, brings the owning team back within the month. That is a minimum over GPU-hours, not an average; node averages have a flat loss curve on the book, and across the fleet the minimum leaves half the nodes averages call idle. |

## 1. Situation

An AI lab's ML platform team signs a capacity plan each quarter, and this quarter's plan commits a number of reserved GPU nodes to return to
the shared pool. Twelve teams hold reserved pools of 8-GPU nodes. The pack holds per-GPU hourly utilisation for the last 28 days, the
utilisation dashboard export, the reservation register with status flags, the contract register with reservation terms, the scheduler's
job log, the capacity charter, and the book of six past reclaim reviews with their outcomes.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each GPU-hour, each dashboard figure, each register entry and each past outcome. Nobody files a
  reclaim count and nothing reported is overturned. The difficulty is what idle means for a node.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the dashboard and both voices. Node-average utilisation over the window, built from the GPU samples, still
  commits 298 nodes.
* **Instrument repair.** Sample every GPU every second: the window's averages and its minimum both sharpen, and the book still says which
  one decides a reclaim. Next quarter's reclaim is a forward commitment no sample measures.
* **Lens swap.** The naive count takes nodes whose average is low; the answer takes nodes with no busy GPU-hour at all, a different set of
  nodes that is half the size.

## 3. The driving force

A strong solver ignores the dashboard's job-weighted figure, limits the count to pools whose reservations run through next quarter, and
counts nodes whose GPU-hour-weighted utilisation over the window is under 10%: 298. The book of past reviews does not bear that out. Of
the nodes reclaimed on low averages, 41% were handed back within 30 days after the owning team escalated. Every handed-back node had at
least one GPU-hour at or above 10%: an inference GPU pinned to one card, or a nightly evaluation job that runs for an hour. Every node
that stayed reclaimed had all 192 GPU-hours of each day below 10% for the whole window. Counted that way, the plan can commit 141 nodes.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Nodes in pools whose dashboard (job-weighted) utilisation is under 10% | 412, +192% | The figure finance and the dashboard both report | The contract register: 56 of those nodes sit in pools whose reservation ends before the quarter, which lapse rather than reclaim |
| 1 | The same, limited to pools reserved through next quarter (the register's active flag corrected by contract term) | 356, +152% | Only nodes the plan can actually reclaim | The charter: reclaims take whole nodes, judged on their own GPUs, not on the pool's job mix |
| 2 | Nodes whose GPU-hour-weighted utilisation over the window is under 10% | 298, +111% | The right grain and the right weighting | The book: 41% of nodes reclaimed on averages were handed back within 30 days |
| 3 | **Decisive:** nodes with every GPU below 10% in every hour of the window | **141** | — | — |

* **Figure shape.** Every correction walks the count down and the answer is the minimum cell, so a solver who stops anywhere commits nodes
  that come back.
* **Partial correction priced (L3).** A solver who takes the minimum over GPUs on daily averages misses the nightly hour and commits 205
  (+45%); one who takes the minimum over hours on the node's average across GPUs misses the pinned card and commits 230 (+63%).
* **Grid.** Population (flag or term) × aggregation (dashboard pool figure, node average, minimum over GPUs, minimum over hours, minimum
  over GPU-hours) = 10 cells. The nearest wrong cell is the full minimum on the flag's population, 163 (+16%), which counts 22 fully idle
  nodes whose reservations lapse anyway; on the term population the nearest is 205 (+45%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter sets the 10% threshold, the 28-day window and whole-node reclaims. It never says how a node's GPU-hours
   combine into one verdict.
2. **Pattern B, a law with a flat-loss field of rivals.** The GPU-hour minimum reproduces 1,820 of 1,820 book outcomes. The node average
   reproduces at most 1,410 at any threshold from 5% to 20%, and the minimum over GPUs or over hours alone at most 1,604. Every rival
   reclaims nodes that came back, so each overstates the book's kept count by 22% or more. The minimum is a construction: 8 GPUs × 672 hours
   per node, each tested, then a node-level all.
3. **No arithmetic symptom.** Samples tie to the dashboard's GPU-hours, nodes to the reservation register, and reclaim totals to the
   book's tallies.
4. **Not a row predicate.** A node's verdict depends on 5,376 GPU-hours, any one of which can keep it.
5. **The enumeration is arithmetic.** No column marks a node as fully idle.
6. **No cutover date.** The window is a fixed 28 days, with nothing stepping.
7. **Survives deletion.** With every voice removed, node averages still commit 298.

## 6. The calibration corpus

* **Form.** The reclaim book: six quarterly reviews, 1,820 node decisions, each node's window of GPU-hours, and whether a reclaimed node
  was handed back on escalation within 30 days.
* **What it certifies.** Whole-node reclaims and the 10% threshold, which every construction honours.
* **What pins the law.** The absolute split: no node with a busy GPU-hour stayed reclaimed, and no fully idle node came back.
* **Twin pair.** Pools Kite and Merlin match on nodes (60), average utilisation (4.1%), job counts and job-size mix. Their kept reclaims
  were 40 and 20 (2.0×): half of Merlin's nodes host one pinned inference GPU.
* **Resemblance points at the decoy.** On every dashboard column, the pools with pinned services resemble the pools the book reclaimed
  most.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the plan commits whole nodes reclaimable from pools reserved through the next quarter, judged on the last
  28 days at a 10% utilisation threshold.
* **Empirical pins.** The aggregation, from the book.
* **Voices.** The infrastructure lead: "A node averaging under 10% is a node we are wasting." The finance partner: "The dashboard's
  utilisation is the number leadership already trusts."
* **Licensed wrong basis.** The charter records that finance sizes reclaims on dashboard utilisation and will present that figure at the
  planning review.

## 8. Determinism by construction

* **Threshold.** No GPU-hour lies within 0.5 points of 10%, so inclusive and exclusive readings agree.
* **Samples.** Every GPU has all 672 hourly samples in the window.
* **Terms.** No reservation ends within three days of the quarter's start.
* **Nodes.** Every node has exactly eight GPUs and belongs to one pool.

## 9. Prompt sketch and deliverables

> I sign the capacity plan on 1 July and the infrastructure lead wants every node averaging under 10% back in the shared pool. Tell me how
> many reserved nodes we can reclaim next quarter, as a whole number, in the sentence that goes into the plan. Send `reclaim_build.xlsx`, a
> chart `node_idle_grid.png`, and a one-page `reclaim_note.pdf`.

* `reclaim_build.xlsx` — reclaimable nodes per pool under each rung, the job-size sheet (ask A), the queue sheet (ask B) and the book table
  (ask C).
* `node_idle_grid.png` — a heat map of one pool's nodes by GPU and hour across the window, with busy GPU-hours marked, each node's average
  in the margin, and the nodes the minimum keeps outlined.
* `reclaim_note.pdf` — the committed count, and the readings a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each pool, the share of GPU-hours by job size class (1, 2–4, 5–8, more than 8 GPUs).
  *Device:* preempted jobs resume under new job IDs linked by a resume ID, as the scheduler guide documents; counting records splits large
  jobs into smaller classes in seven pools.
* **Ask B (device-carried).** For each pool, the median queue wait. *Device:* jobs held at the user's request carry a hold interval that
  the scheduler guide excludes from wait; counting it overstates four pools.
* **Ask C (validity).** Reclaimable nodes per pool under rungs 2 and 3, and book outcomes reproduced by each aggregation law.
* **Decoupling.** Clearing the GPU-hour minimum changes no figure in asks A or B.

## 11. Rubric arithmetic

12 pools × 4 classes (ask A) + 12 pools (ask B) + 12 × 2 pool counts and 4 laws (ask C) + the committed count, the kept share and the
handed-back share + 5 named chart parts + 3 files ≈ 99 criteria.

## 12. World-building constraints

* Fleet: 1,460 reserved nodes in 12 pools, 70 of them in pools whose reservations lapse. Counts 412 / 356 / 298 / 141; partial cells
  205 and 230; the flag-population minimum 163.
* Book: 1,820 decisions; minimum 1,820, best rival 1,604, node average at most 1,410. Kite and Merlin match on every dashboard column.
* 157 of the 298 average-idle nodes carry a pinned inference GPU or a nightly job of one to two hours.
* Resume IDs and hold intervals never touch a GPU sample or a node.
