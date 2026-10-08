# OS18 — Which host pool gets the six-hour batch lane, when the deepest idle pool is held by a customer's failover reservation

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Product Analytics · cloud capacity products |
| Mirrors | Launching a harvest or spot-capacity product where measured idle capacity includes customers' paid-but-unused reservations (AWS Spot beside On-Demand Capacity Reservations, Google Cloud Spot VMs beside reservations, Azure Spot), so the deepest idle pool is the least sellable |
| Decision shape | Which of N gets one scarce thing, with the sizing kept as the graded figure: the batch lane launches on one of five host pools |
| Committed call | The host pool the lane launches on, and the cores it can guarantee, rounded down to a multiple of 8 |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join), over the six-hour window minimum and a coarsened segment (#14) |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #14 coarsens the segment it was asked about · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Gold-standard verification subsample: 400 six-hour test jobs placed at random start times on randomly sampled hosts, each recorded as completed or evicted |
| Driving force | Idle cores include cores a customer has reserved, pays for and is not using. A batch job cannot be promised a core that a reservation holder may claim at any minute, so a pool's sellable capacity is its six-hour guaranteed idle less its unused reserved cores. That is a pool-level quantity, built by joining the reservation ledger's contracts to pools. In e2's gen-6 pool a failover reservation holds 65% of the guaranteed idle. Reservations are sold only on gen-6 hardware and the verification harness sampled gen-5 hosts, so the subsample certifies the window method blind to them. |

## 1. Situation

A cloud provider will launch a "batch lane" that guarantees customers a number of cores for six-hour jobs on otherwise idle capacity. It
launches on one host pool (an availability zone and hardware generation), and the charter shortlists five: e1-gen6, e2-gen5, e2-gen6,
e1-gen5 and w1-gen6. The lane's SLA guarantees the cores at 95% of hourly start times. The capacity dashboard reports average idle
cores by availability zone. A month of five-minute host telemetry is in the pack, with the reservation ledger and the hardware inventory.
Last quarter the capacity team ran 400 six-hour test jobs on sampled hosts. The product manager points at e1, the biggest zone.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the dashboard, the telemetry, the test outcomes and the reservation ledger. Reserved cores really
  are idle. No stakeholder read is overturned. The difficulty is that idle cores held by a reservation cannot be sold, and nothing labels
  which idle cores those are.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the product manager's view and the dashboard. The telemetry's six-hour window minimum, certified by the test
  jobs, still names e2-gen6.
* **Instrument repair.** Sample telemetry every second and test a million jobs. The window minimum sharpens, and the reservation holder can
  still claim its cores mid-job.
* **Lens swap.** The naive read is idle cores; the answer is idle cores no contract can recall, a different population found in a
  different file.

## 3. The driving force

A strong solver drops the dashboard, because the charter names pools and each zone mixes generations. It sees that a six-hour job needs
the same cores for six hours, so it takes the minimum idle over each six-hour window and the level available at 95% of start times. The
test jobs confirm it: that rule predicts all 400 outcomes. e2-gen6, with deep and stable overnight idle, wins by a third. But 3,380 of
e2-gen6's 5,200 guaranteed idle cores belong to a retailer's failover reservation: paid for, never used in the month, and claimable within
minutes. A batch job on them would be evicted the moment the retailer fails over. Sellable capacity is guaranteed idle less unused reserved
cores, and w1-gen6, with no reservation, guarantees 3,896.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The dashboard's zone idle share × each pool's cores | A, e1-gen6 (8,560 cores) | The capacity team's own planning figure, on the hardware inventory | The charter launches on one pool and excludes gen-4 hosts, which lack local scratch disks; each zone's figure blends in e1's and w1's busy gen-4 pools |
| 1 | Each pool's average idle cores, from the telemetry | B, e2-gen5 (8,000, 1.25× over A) | The right grain, from the raw trace | The test jobs: average idle predicts 271 of 400 outcomes, and e2-gen5's idle is bursty |
| 2 | Each pool's idle available for six hours at 95% of start times | C, e2-gen6 (5,200, 1.33× over E) | Predicts all 400 test outcomes and matches the SLA | The reservation ledger: 3,380 of e2-gen6's guaranteed idle cores are an unused failover reservation |
| 3 | **Decisive:** six-hour guaranteed idle less unused reserved cores, by pool | **E, w1-gen6** (5th of 5 on rung 0), **3,896 cores** | — | — |

* **Position table.** w1-gen6 ranks 5th on rung 0, 5th on rung 1 and 2nd on rung 2 (1.33× behind e2-gen6), and leads only rung 3 (1.39×
  over e1-gen5).
* **Discriminator dominance.** e2-gen6 carries a 1.33× advantage into rung 3 (5,200 against 3,900). Its sellable share is 0.35 against
  w1-gen6's 1.00, an edge of 2.86×, 1.79 times the 1.60× floor. Product: 2.86 / 1.33 = 2.14.
* **Partial correction priced (L3).** Every half-applied construction names a wrong pool. A solver who subtracts reservations from
  average idle names e2-gen5 (8,000 against e1-gen6's 5,320, 1.50×). One who subtracts them from zone-level figures names e1-gen6 (7,880
  against 5,360 on average idle, 1.47×; 3,850 against 2,210 on the window, 1.74×). One who treats a reservation as releasable because it
  went unused all month lands back on e2-gen6 (5,200 against 3,900, 1.33×).
* **Grid.** Grain (zone, pool) × availability (average, six-hour window) × reservations (kept, subtracted) gives 8 cells. Zone cells name
  e1-gen6 (1.16× to 1.74×); pool cells name e2-gen5, e2-gen5, e2-gen6 and the answer. Only the answer cell names w1-gen6.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The reservation ledger records contracts, pools, reserved cores and use. No document says reserved idle is
   unsellable or links the ledger to the lane.
2. **Corpus blind for a computable reason.** *In every verified host the reserved share was zero, because reservations are sold only on
   gen-6 hardware and the harness, built for the gen-5 pilot, sampled gen-5 hosts only.* The window rule predicts 400 of 400 outcomes
   without any reservation term.
3. **No arithmetic symptom.** Telemetry reconciles to the dashboard's zone totals, the window minima tie to the test outcomes, and the
   ledger's reserved cores sit inside each pool's idle.
4. **Not a row predicate.** Unused reserved cores are summed per pool from contracts and hourly use, then subtracted inside each pool's
   six-hour window before the 95% level is taken.
5. **The enumeration is arithmetic.** No telemetry column marks a core as reserved; reservations are pool-level contracts.
6. **No cutover date.** Reservations ran unchanged through the month, and no series steps.
7. **Survives deletion.** Removing the dashboard and every voice leaves the test jobs certifying rung 2.

## 6. The calibration corpus

* **Form.** The 400 test jobs: host, pool, start time, and completed or evicted.
* **What it certifies.** The six-hour window at 95% of starts: 400 of 400 outcomes predicted. Average idle predicts 271, and its misses all
  predict completions that were evicted, so it fails in aggregate too.
* **What it is blind to.** Reserved capacity (above).
* **Twin pair.** Pools e3-gen6 and w2-gen6, outside the shortlist, are identical on cores (10,000), average idle and six-hour guaranteed
  idle (3,000). e3-gen6 carries a 1,500-core unused failover reservation, so it can sell 1,500 against w2-gen6's 3,000, 2.0× apart. Only the
  ledger join separates them.
* **Resemblance points at the decoy.** e2-gen6's deep, flat overnight idle most resembles the verified hosts with the most completions.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The charter: the lane launches on one host pool, named by zone and generation (gen-4 hosts, without local scratch disks,
  are excluded), and is sized on the cores it can guarantee to customers' jobs. The product sheet: jobs run six hours. The SLA: capacity
  is guaranteed at 95% of hourly start times. The pricing note: guaranteed cores are sold in blocks of 8.
* **Empirical pins.** The window rule, from the test jobs. Unused reserved cores, from the ledger.
* **Voices.** The product manager: "e1 is our biggest zone and a quarter of it sits idle." The SRE lead: "Idle is idle. The scheduler will
  find it."
* **Licensed wrong basis.** The charter records that the finance review sizes new capacity products on the dashboard's average idle cores
  and will present that sizing.

## 8. Determinism by construction

* **Reservations.** Every reservation's use was zero throughout the month, so unused reserved cores are constant and subtract exactly
  inside every window.
* **Window.** Starts are hourly over 30 days (720 starts); no pool's 95% level sits within 8 cores of a block boundary.
* **Pools.** Every host belongs to one pool by its inventory record.
* **Telemetry.** No five-minute sample is missing in any shortlisted pool.
* **Rounding.** w1-gen6 guarantees 3,900 cores; rounded down to a block of 8 it sells 3,896.

## 9. Prompt sketch and deliverables

> We launch the six-hour batch lane on one host pool next quarter and I need to tell the launch review which, and how many cores we can
> promise, in blocks of 8. Our product manager wants it in e1, our biggest zone. Put the answer in a sentence and
> send `pool_sizing.xlsx`, a chart `pool_idle_layers.png`, and a one-page `launch_review.pdf`.

* `pool_sizing.xlsx` — each pool on four bases, the window build and the reservation subtraction, the failure sheet (ask A) and the power
  sheet (ask B).
* `pool_idle_layers.png` — a script-rendered layered bar per pool: average idle, six-hour guaranteed idle, and sellable idle nested inside
  it, the unused reservation drawn as a hatched slice, and the committed pool highlighted.
* `launch_review.pdf` — the committed pool, its guaranteed cores, and why e2-gen6 falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each shortlisted pool, last quarter's host failures per 1,000 host-days and the median hours
  to repair. *Device:* a host that fails again within 24 hours of repair is logged as one incident with two fault events, and the SRE guide
  counts incidents. Counting fault rows overstates failures in the two pools with most repeat faults.
* **Ask B (device-carried).** For each pool, the average overnight power draw per host. *Device:* every rack draws on two power feeds, and
  the facilities guide gives host power as the sum of both. Reading one feed halves the draw in every pool and reorders two.
* **Ask C (validity).** Each pool's guaranteed cores under each of the four rung bases, and test outcomes predicted (of 400) by average idle
  and by the six-hour window.
* **Decoupling.** Ignoring reservations changes no figure in asks A or B. Failure logs and power telemetry touch neither the idle telemetry's
  core counts nor the reservation ledger.

## 11. Rubric arithmetic

5 pools × 2 (ask A) + 5 pools and the fleet (ask B) + 5 pools × 4 bases and 2 test counts (ask C) + the committed pool, its cores, the
runner-up and the margin + 5 named chart parts + 3 files ≈ 50 criteria.

## 12. World-building constraints

* Pools (cores, average idle, six-hour guaranteed idle, unused reserved; thousands): e1-gen6 34 / 6.4 / 3.6 / 1.08; e1-gen5 10 / 5.2 / 2.8
  / 0; e2-gen6 11 / 6.1 / 5.2 / 3.38; e2-gen5 11 / 8.0 / 2.6 / 0; w1-gen6 8 / 4.4 / 3.9 / 0. Busy gen-4 pools: e1 10 / 2.0, w1 16 / 1.6.
* Rung leaders A, B, C, E at 1.22×, 1.25×, 1.33×, 1.39×; w1-gen6 5th, 5th, 2nd, 1st.
* Reservations exist only on gen-6 pools; every test host is gen-5.
* e3-gen6 and w2-gen6 match on every telemetry column.
* Failure logs and power telemetry never touch idle cores or reservations.
