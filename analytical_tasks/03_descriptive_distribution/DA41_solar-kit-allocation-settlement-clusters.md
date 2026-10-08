# DA41 — How 40,000 solar home kits are split across eight districts, when only footprints inside settlements ever become households

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Economics · energy-access programme planning |
| Mirrors | Allocating capped resources on machine-detected counts when only part of the detections convert (map-detected businesses targeted by a sales team, model-flagged leads routed to reps, fraud alerts sent to a fixed pool of investigators), where conversion splits on a structural property no column carries |
| Decision shape | An allocation under a cap: 40,000 kits divided across eight districts in proportion to the eligible households each can enrol |
| Committed call | Kits per district, and the households the allocation electrifies, to the nearest 100 |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield, reached through a spatial construction), with a mixed segment split through a join at rung 2 |
| Gate G mechanism | binding_constraint, with method_or_model_selection |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #7 uses the ready-made measure |
| Calibration form | Retry or revision log: the field verification log of last year's pilot, every visit and revisit to every detected footprint in three districts with its outcome |
| Driving force | A detected footprint becomes an enrolled household only inside a settlement cluster, five or more footprints within 50 metres; the pilot's retry log shows 82% of clustered footprints enrolled after revisits and 0 of 4,120 isolated ones. Cluster membership is a spatial self-join, not a column. The three pastoral districts hold most of the isolated footprints (kraals, stores, pens and lone homesteads), so every count-based allocation sends them kits that cannot be placed. |

## 1. Situation

A rural electrification programme distributes 40,000 solar home kits this year across eight districts. Its manual allocates kits in
proportion to the eligible unelectrified households each district can enrol, counted from a machine-learning building-footprint layer
outside a 2 km buffer around the grid. Last year's pilot in three districts sent enumerators to every detected footprint. The pack holds the footprint
layer with confidence scores, the provider's precision and recall tables, the grid buffer, the utility's three-year extension plan, the
pilot's verification log, and the manual.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each footprint, each evaluation table, each corridor polygon and each logged visit. Nobody files an
  allocation and nothing reported is overturned. The difficulty is which detections are households.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the donor's basis and both voices. Precision-adjusted counts outside the buffer and the corridors still send
  15,600 kits to the pastoral districts.
* **Instrument repair.** Suspect: the footprint layer, whose detector misses some buildings and adds others (precision 0.61 to 0.88).
  Repaired to perfect detection, rung 0 returns rung 1's 35,050. Replaced by a register of every household outside the buffer, rungs 0
  and 1 electrify 36,000 and rung 2 35,600, because isolated homesteads are households too and none enrolled (0 of 1,320 in the pilot).
  The answer stays 40,000, and the cluster self-join is still needed.
* **Lens swap.** The naive base is every detected building outside the grid; the answer's base is the buildings in settlements, a
  different population, smallest exactly where the naive base is largest.

## 3. The driving force

A strong solver counts footprints outside the buffer, corrects them with the provider's district precision and recall, removes the
utility's extension corridors as the manual's eligibility clause requires, and allocates pro rata. Every step is right, and it sends 39% of
the kits to three pastoral districts. The pilot log tells a different story at the footprint grain. Enumerators visited every detected
footprint up to three times. Inside settlement clusters, 82% became enrolled households. Isolated footprints, more than 50 metres from
four neighbours, produced none in 4,120 attempts. Most are kraals, stores and seasonal shelters, as real and as well detected as houses,
and the 1,320 that are occupied homesteads enrolled no more than the rest.
The pastoral districts are 70% isolated footprints, while the pilot districts were 10%. Allocated on clustered footprints, the kits all
land in households: 40,000 against 33,850.

## 4. The ladder

| Rung | Construction | Allocates (pastoral share; households electrified) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Raw footprints at confidence 0.70 outside the grid buffer | 40%; 33,450 (−16%) | The layer the manual names, read as it comes | The provider's evaluation: precision at 0.70 runs 0.61 to 0.88 by district |
| 1 | Footprints adjusted by district precision and recall | 36%; 35,050 (−12%) | The textbook correction for detector error | The manual: households in the utility's extension corridors are ineligible |
| 2 | Adjusted footprints net of the extension corridors (a mixed segment split by the corridor plan) | 39%; 33,850 (−15%) | Correct, eligible and adjusted | The pilot log: 0 enrolments in 4,120 isolated footprints, 82% in clustered ones |
| 3 | **Decisive:** clustered footprints (five or more within 50 m), net of the corridors | **24%; 40,000** | — | — |

* **Allocation shape.** Every rung over-allocates the pastoral districts and leaves kits unplaced. The answer is the extreme cell, the
  only allocation that places all 40,000.
* **Partial correction priced (L3).** A solver who builds clusters at 100 metres sweeps kraal complexes into settlements, gives the
  pastoral districts 32% and electrifies 36,200 households (−9.5%). A solver who conditions on clusters but keeps the corridor households
  places 40,000 kits with 3,700 of them in households the utility will connect anyway, which the manual counts as ineligible: 36,300
  (−9.3%). Neither half produces the answer's allocation.
* **Grid.** Count basis (raw, adjusted, clustered at 50 m, clustered at 100 m) × corridors (kept or removed) = 8 cells, each a different
  allocation. The nearest wrong cell electrifies 36,300 eligible households (−9.3%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The manual counts the eligible households a district can enrol from the footprint layer. The provider's notes
   describe building detection, not dwelling status. No document mentions settlements or isolation.
2. **Pattern E, absolute in the retry log.** Clustered footprints enrolled at 82% (80% to 84% in every pilot district) and isolated ones at
   0 of 4,120 after up to three visits, with nothing in between. The pooled pilot rate of 74% fits no footprint. Clustering is a
   construction: a spatial self-join of footprints within 50 metres and a count per neighbourhood.
3. **No arithmetic symptom.** Footprints reconcile to the provider's tiles, corridors and the buffer overlay cleanly, and allocations sum
   to 40,000 under every rung.
4. **Not a row predicate.** A footprint's status depends on how many other footprints lie within 50 metres of it.
5. **The enumeration is arithmetic.** No column marks a footprint as isolated, and confidence, area and roof type are the same for
   isolated and clustered footprints.
6. **No cutover date.** One imagery vintage and one pilot round.
7. **Survives deletion.** With every voice removed, the adjusted count still sends 39% to the pastoral districts.

## 6. The calibration corpus

* **Form.** The verification log: 23,600 visits to 16,800 detected footprints in three pilot districts, each visit with its outcome
  (enrolled, not a dwelling, no one home, refused) and revisits up to three.
* **What it certifies.** That detections over-count households, and the pooled rate a solver will carry.
* **What pins the condition.** The absolute split by cluster status, the same in all three pilot districts and at every radius from 30 to
  70 metres; the 1,320 occupied isolated homesteads enrolled none, like the kraals and stores around them.
* **Twin pair.** Enumeration areas K-14 and P-07 match on detected footprints (412), mean confidence, mean area and roof mix. They enrolled
  338 and 169 households (2.0×): every K-14 footprint is in a cluster, and half of P-07's are isolated.
* **Resemblance points at the decoy.** On every visible footprint column, the pastoral districts resemble the pilot's highest-yield area.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The manual: 40,000 kits allocated in proportion to the eligible unelectrified households each district can enrol,
  counted from the footprint layer outside the 2 km grid buffer, with households in the utility's three-year extension corridors
  ineligible. Allocations round by largest
  remainder.
* **Empirical pins.** The settlement condition and its radius, from the retry log.
* **Voices.** The GIS lead: "Precision-adjusted footprints are the best household count we will ever get." The pastoral districts' liaison:
  "Our districts are the least served and should get the most kits."
* **Licensed wrong basis.** The manual records that the donor's results framework counts beneficiaries on raw footprints and will review
  the allocation on that basis.

## 8. Determinism by construction

* **Radius.** The split holds at every radius from 30 to 70 metres, so 50 metres converges with its neighbours.
* **Corridors.** No footprint lies within 10 metres of a corridor boundary.
* **Capacity.** Every district's clustered count times 0.82 exceeds its proportional allocation, so all 40,000 kits place.
* **Visits.** Yield is counted per footprint after its last visit, so attempt-grain and footprint-grain readings are both shipped and only
  the footprint grain reproduces the district enrolment totals.

## 9. Prompt sketch and deliverables

> The kit allocation goes to the district offices on 3 March, and the pastoral districts are pressing for the biggest share. Give me kits
> per district for the 40,000 and the households they will electrify, to the nearest 100, as the table we send. Send
> `kit_allocation.xlsx`, a map `settlement_clusters.png`, and a one-page `allocation_note.pdf`.

* `kit_allocation.xlsx` — the allocation under each count basis, the roof sheet (ask A), the road sheet (ask B) and the pilot tables
  (ask C).
* `settlement_clusters.png` — a map of footprints in two contrasting districts coloured by cluster status, with the grid buffer and
  extension corridors drawn, each district's allocation in the legend, and the twin enumeration areas outlined.
* `allocation_note.pdf` — the committed allocation, the households electrified, and why the count bases fail.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each district, the share of footprints with metal roofs. *Device:* the roof-material layer
  changed its codes between imagery vintages, and its note gives the mapping; mixing vintages misstates five districts.
* **Ask B (device-carried).** For each district, the median distance from footprints to the nearest all-weather road. *Device:* the road
  layer carries proposed roads with a status flag, which the layer note says to exclude; including them shortens four districts'
  medians.
* **Ask C (validity).** Each district's allocation under each of the four rungs, and pilot yield by cluster status and by visit versus
  footprint.
* **Decoupling.** Clearing the cluster construction changes no figure in asks A or B.

## 11. Rubric arithmetic

8 districts (ask A) + 8 districts (ask B) + 8 × 4 allocations and 4 yield figures (ask C) + 8 committed allocations and the households
electrified + 5 named chart parts + 3 files ≈ 69 criteria.

## 12. World-building constraints

* Outside the buffer: 96,000 detected footprints; 9,000 in corridors (mostly peri-urban); 31,000 isolated, 70% of the pastoral districts'
  footprints against 10% in the pilot districts, about a third of them occupied homesteads.
* A household register in place of the layer allocates 31% to the pastoral districts and electrifies 36,000 (35,600 net of corridors).
* Pastoral share and households electrified: 40% / 33,450; 36% / 35,050; 39% / 33,850; 24% / 40,000. Partial cells 36,200 and 36,300.
* Retry log: clustered 82%, isolated 0 of 4,120. K-14 and P-07 match on every footprint column.
* Roof codes and road status never touch a footprint's position or a corridor.
