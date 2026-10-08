# FC13 — How 700 contract technician visits are split across four data centres, when an ageing cohort's failures arrive in the same pods

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · storage-fleet maintenance |
| Mirrors | Booking maintenance capacity when work arrives in visits that can carry several repairs (hyperscaler data-centre technician dispatch, Amazon and Apple field-service truck rolls, telecom tower maintenance where one climb fixes several faults) |
| Decision shape | An allocation under a cap: 700 contract technician visits placed across four data centres for one quarter, under a filed top-up rule |
| Committed call | Contract visits for DC1–DC4 next quarter, adding to 700, booked before the quarter opens |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S6, a correct per-drive share of a fixed allowance (the visit) carried onto a denser forward book, with a saturated priority tie below it |
| Gate G mechanism | forecasting, with binding_constraint support |
| Measured traps engaged | #19 breaks a big tie instead of questioning it · #2 counts file rows instead of the real unit · #13 validates on one population, applies to another |
| Calibration form | Parallel-run overlap: one quarter in which the old per-drive planning model and the new work-order system both recorded every replacement and every visit |
| Driving force | A technician visit to a pod replaces every drive that failed in it that week, so the visit is a fixed allowance and "0.83 visits per failed drive" is that allowance's correct share for a book where failures arrive alone. Next quarter DC2's 2021 cohort reaches wear-out, and its failures land in the same 40 all-original pods week after week, at 2.1 drives per visit. Carrying the per-drive share onto that book repays the visit once per drive and books DC2 twice the visits it will use. |

## 1. Situation

A storage provider replaces failed drives with in-house technicians and a contract crew. The contract for next quarter caps contract
visits at 700. The contract schedule places them DC by DC, in descending order of each data centre's share of wear-out pods (pods whose
every drive is at least 36 months old), with ties going to the larger fleet. Each DC is topped up to its 90th-percentile visit
requirement above in-house capacity before the next gets any. In-house capacity is 300, 250, 350 and 300 visits for DC1–DC4.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the daily drive snapshots, the asset register, the swap log, the work-order records and the
  planning model. No one's claim about their own numbers is overturned. The difficulty is a unit of work whose share per drive changes
  when failures stop arriving alone.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. Age-specific hazards with the per-drive visit share still send 650 visits
  to DC2.
* **Instrument repair.** Suspect: the asset register, which dates pods, not drives. Give every drive its own install date from the swap
  log. Rung 0 then returns rung 1's 0 · 390 · 310 · 0 and rung 2 still 0 · 650 · 50 · 0; failures in the parallel quarter still arrived
  alone, so pod-week batching is still a construction the answer needs.
* **Lens swap.** The naive read and the answer differ in moment: an unclustered closed quarter against a quarter in which one cohort's
  failures share pods.

## 3. The driving force

A strong solver ages every drive from the swap log rather than its pod's install date, fits age-specific hazards and sees DC2's 2021
cohort climbing into wear-out. It multiplies the forecast failures by the planning model's 0.83 visits per drive. That share is
exact for the parallel quarter: the old model and the work-order system agree on every DC's visits to the unit. But a visit is a fixed
allowance. It replaces every drive that failed in that pod that week, and in the parallel quarter almost every pod-week held one failure.
DC2's cohort sits in 40 pods built entirely from the 2021 purchase. As it reaches wear-out, those pods average 1.7 failures a week, and
a visit carries 2.1 drives. The forecast has to count pod-weeks with a failure, not failures. No visit column exists for a quarter that
has not happened. It comes from the hazard model run per pod and per week.

## 4. The ladder

| Rung | Construction | Lands on (DC1 · DC2 · DC3 · DC4 visits) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Flat AFR per model × drives × 0.83 visits per drive; wear-out share from pods' install dates, so DC2 and DC3 tie at 100% and DC3 (larger) goes first | 0 · 230 · 470 · 0 | The planning model on the provider's published rates, with the schedule's own tie-break | **E21 (a saturated tie):** the swap log dates every like-for-like replacement, and the lowest share consistent with it and the register puts DC3 at 68% and DC2 alone at 100% |
| 1 | The same with drive ages from the swap log, so DC2 goes first | 0 · 390 · 310 · 0 | The priority as the schedule defines it, every drive aged from the files of record | The daily snapshots: failure rates climb steeply with age, and DC2's 2021 cohort enters wear-out next quarter |
| 2 | Age-specific hazards per model × age band (drive-days of exposure), × 0.83 visits per drive | 0 · 650 · 50 · 0 | The reliability standard's own method, and the parallel quarter reproduces to the unit | The work-order records: a visit carries every drive failed in its pod that week, and DC2's wear-out failures will share 40 pods |
| 3 | **Decisive:** visits as pod-weeks with at least one forecast failure, from the hazard model run per pod and week; P90 by convolution; then the top-up rule | **100 · 310 · 290 · 0** | — | — |

* **Figure shape.** DC2's allocation, the headline, walks up through the corrections (230, 390, 650) and the decisive rung reverses it
  to 310. That frees the capacity that reaches DC1. A solver who stops short over-books DC2 or starves it.
* **Partial correction priced (L3).** Treating all 120 of DC2's model-X pods as clustered, including the 80 with younger like-for-like
  replacements, spreads the batching too thin: DC2 450 (+45%). Batching by pod-month instead of pod-week, which no visit record supports,
  gives DC2 230 (−26%). Neither is closer than rung 1.
* **Grid.** Ages (pod install, swap log) × hazard (flat, age bands) × visit unit (per-drive share, pod-week) gives 8 cells and five
  allocations. Without the swap log the hazard model also over-ages DC3, which then goes first: 0 · 250 · 450 · 0. The nearest wrong
  value of the headline is 19% away.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The planning model states 0.83 visits per drive as a parameter. The work-order manual describes visits, but no
   document says how many drives a visit will carry next quarter or that the share depends on clustering.
2. **Corpus blind for a computable reason.** *In the parallel quarter 88% of pod-weeks with a failure held exactly one, because no cohort was
   in wear-out.* The per-drive share and the pod-week construction both reproduce every DC's 12 weeks of visits to the
   unit.
3. **No arithmetic symptom.** Visits tie to work orders, failures to snapshots, and allocations to 700 under every rung.
4. **Not a row predicate.** Visits are a count of pod-weeks with at least one failure, each pod's weekly failure probability built from
   its own drives' ages and model hazards, then convolved into a quarterly 90th percentile.
5. **The enumeration is arithmetic.** Which pods will batch, and how heavily, is computed. No column marks DC2's 40 pods as clustered.
6. **No cutover date.** The cohort ages smoothly into its steep band. No closed series steps; the clustering lives in the forward quarter.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The parallel run: one quarter in which the planning model and the work-order system both recorded every failed drive and
  every visit, by pod and week, in all four data centres.
* **What it certifies.** Both models reproduce all 48 DC-weeks of visits exactly. The work orders also show the visit rule: every visit's
  drives failed in the same pod-week, without exception, so weekly batching is pinned.
* **What it is blind to.** Dense pod-weeks (above).
* **Twin pair.** Pods P-2207 and P-3114 are identical on every register and snapshot column: model, install date, data centre, 60 slots
  and six failures in the quarter. They took six and three visits (2.0×), because P-3114's failures came in pairs within the same week.
  The per-drive share gives both five; only pod-week counting reproduces both.
* **Resemblance points at the decoy.** Next quarter's DC-level profile (drive counts, model mix, in-house capacity) matches the parallel
  quarter's within 2%, and there the per-drive share was exact.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The contract: 700 visits, placed by the top-up rule above, ties to the larger fleet. The contract defines a wear-out
  pod as one whose every drive is at least 36 months old. The reliability standard: hazards per model × six-month age band on drive-days,
  P90 of the quarter's visits by exact convolution. The work-order manual: a technician visits a pod at most once a week.
* **Empirical pins.** Drive ages, from the swap log and the snapshots. The weekly batching, from the parallel run's work orders.
* **Voices.** The operations manager: "A failed drive is a visit. That's been true for years." The reliability engineer: "DC2's 2021
  drives are the whole story next quarter."
* **Licensed wrong basis.** The contract's cover note records that the contractor prices the crew on the planning model's visits per
  drive and will present its staffing on that basis.

## 8. Determinism by construction

* **Ages.** Every drive installed before the snapshots began has a swap-log or register date, and no pod's minimum drive age sits within
  a month of 36.
* **Weeks.** Visits are counted in ISO weeks, and no forecast failure probability changes within a week, so week alignment cannot move a
  count.
* **P90.** Exact convolution of independent pod-week indicators, as the standard states. A normal approximation gives the same whole
  number for every DC.
* **Top-up.** The rule is sequential and deterministic, and under the answer all of DC2's and DC3's needs fit inside the cap, so the
  DC2-DC3 order cannot change the answer's allocation.
* **Maturity.** The snapshots run to the extract date, and the swap log is complete through it.

## 9. Prompt sketch and deliverables

> The contract crew's visits for next quarter have to be split across our four data centres before the quarter opens, and the
> contract caps them at 700. Our operations manager is sure every failed drive means a visit. Give me the four numbers, and send
> `contract_visit_split.xlsx`, a chart `pod_week_visits.png`, and a one-page `visit_booking_note.pdf`.

* `contract_visit_split.xlsx` — the visit build by DC, pod and week, the rebuild sheet (ask A) and the RMA sheet (ask B).
* `pod_week_visits.png` — for DC2's 40 all-original pods, forecast failures and visits per week (bars and line), the per-drive-share
  visits as a dashed line, the 2.1 drives-per-visit ratio labelled, and the four DCs' allocations as an inset.
* `visit_booking_note.pdf` — the committed split and the contractor's basis it departs from.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each data centre, last quarter's median and 95th-percentile rebuild duration after a drive
  replacement. *Device:* a rebuild interrupted by a second failure in the same vault is restarted under a new rebuild ID, and the storage
  runbook measures duration from the first start to the final completion. Per-ID durations understate the 95th percentile at three DCs.
* **Ask B (device-carried).** For each drive model, last year's warranty returns and the share credited by the vendor within 60 days.
  *Device:* the vendor's credit file posts a return rejected and resubmitted as two lines under one RMA number. Counting lines overstates
  returns for four models and halves their credit share. Returns never enter the hazard model.
* **Ask C (validity).** The allocation under each of the four rung constructions, with each one's reproduction of the parallel quarter's
  48 DC-weeks.
* **Decoupling.** Replacing pod-week counting with the per-drive share changes no figure in asks A or B.

## 11. Rubric arithmetic

4 DCs × 2 (ask A) + 9 models × 2 (ask B) + 4 constructions × 4 DCs (ask C) + the four committed allocations and DC2's forecast visits +
5 named chart parts + 3 files ≈ 55 criteria.

## 12. World-building constraints

* P90 visits needed (DC1–DC4): 520/640/820/480 at rungs 0–1, 480/900/640/470 at rung 2, 480/560/640/470 at the answer. In-house
  capacity 300/250/350/300.
* Wear-out share: DC2 100%, DC3 68% with swap-log ages (100% on pod install dates), DC1 55%, DC4 20%.
* DC2's 40 all-original pods average 1.7 forecast failures per pod-week and 2.1 drives per visit; in the parallel quarter 88% of
  pod-weeks with a failure held exactly one (1.2 drives per visit).
* P-2207 and P-3114 are identical on every register and snapshot column.
* Interrupted rebuilds and resubmitted RMAs never touch snapshots, the swap log or work orders.
