# RC35 — Which cost control the platform team builds, when the biggest source of compute growth is the one its control cannot reach

| Field | Value |
|---|---|
| Objective | Root Cause Analysis |
| Domain | Supply Chain & Logistics · cloud capacity and cost management |
| Mirrors | FinOps control choice at cloud-heavy companies (AWS, Azure and Google Cloud customers, internal platforms at Meta, Netflix and Uber), where the largest driver of spend sits behind reservations, service-level floors and retention exemptions that its control cannot touch |
| Decision shape | Which of N root causes gets the fix: one engineering quarter, five controls, each aimed at one source of compute growth |
| Committed call | The one control the platform team builds next quarter, named in a sentence, with the week-4 core-hours each control would remove |
| Gap · Pattern | Gap 3 (objective) into Gap 2 (population) · Pattern C (serviceable share behind a join), with a quiet second trap below it: billed core-hours exclude deallocated time |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #10 notes a binding limit as a risk · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the cloud provider's acknowledgements of the platform team's 1,214 resize, deallocate, delete and scale-in requests in the pilot quarter |
| Driving force | Every source of growth is sized correctly. Once deallocated hours are taken out, upsized VMs are the largest. A resize can only touch VMs whose SKU family has a smaller size and whose cores are not pinned by a reservation in the reservation ledger, and 72% of the upsized cores are pinned. Autoscale sets stuck at their maximum grew less, but 95% of their excess sits on sets whose maximum the owning team chose rather than a service-level floor in the service catalogue. Serviceable core-hours rank the controls in reverse. |

## 1. Situation

A company's internal cloud platform burned 1.35M core-hours in week 4 of the month against 1.00M in week 1. Finance wants a hard quota on VMs
per subscription, because VM creations rose 80%. The platform team has one engineering quarter for one control: a VM-count quota,
a rightsizing programme, a lifecycle policy that deletes idle VMs, a fix that lets stuck autoscale sets scale in, or migration of
training jobs to spot capacity. The FinOps charter says the control built is the one that removes the most core-hours from the week-4
run rate. The platform lead believes VMs that never get deleted explain the growth.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct: the VM table, the power-state log, the SKU catalogue, the reservation ledger, the service
  catalogue, the exemption tags and the provider's acknowledgements. Finance's creation count is right, and so is the platform lead's count
  of long-lived VMs. Nothing is overturned. The difficulty is what each control can actually reach.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete finance's proposal and every voice. The stock-based decomposition still points at long-lived VMs, and with
  deallocation handled it points at upsized ones.
* **Instrument repair.** No file is suspect. The VM table records each VM's life and size correctly, a different attribute from billed time,
  and the power-state log, SKU catalogue, reservation ledger, service catalogue, exemption tags and scheduler configs are complete and
  current. Repair them anyway, down to a meter of billed core-seconds per VM. Rung 0 still names the quota, rung 1 moves from the lifecycle
  policy (150) to rightsizing (110), and rung 2 names rightsizing. What each control can remove is a join to pins and floors that no row
  records, so the decisive construction is still needed.
* **Lens swap.** The naive ranking sizes each control's target. The answer sizes what each control can remove next quarter, a different
  population inside each target.

## 3. The driving force

A strong solver throws out finance's creation count: short-lived VMs dominate creations and barely move core-hours. It rebuilds
consumption from active VMs and decomposes it, which points at long-lived VMs. Then it catches the quiet trap. The provider bills no
cores while a VM is deallocated, and the power-state log shows many "never deleted" dev VMs deallocated every night. On billed
core-hours, upsized VMs lead with 110k of the 350k growth. A careful solver would build rightsizing. But a resize needs a smaller size in
the VM's SKU family, which the SKU catalogue shows, and cores not pinned by a reservation, which the reservation ledger shows. Most
upsized VMs belong to teams that bought three-year reservations at the larger size, so rightsizing removes 31k. Stuck autoscale sets grew
by 60k. Only 5% of that excess sits on sets whose floor the service catalogue fixes for a service-level commitment, so the scale-in fix
removes 57k.

## 4. The ladder

| Rung | Construction | Names (week-4 core-hours, k) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | VM creations by week, finance's reading | VM-count quota (creations +80%) | The most visible metric, and it grew fastest | The VM table: 70% of the new VMs lived under a day and add 20k core-hours of the 350k |
| 1 | Active-VM stock decomposed by count, size and duty, existence counted as consumption | Lifecycle policy (150, 1.67×) | The stock-and-flow correction, censoring handled | The power-state log: deallocated VMs hold no cores, and the long-lived dev VMs sat deallocated most nights |
| 2 | Hygiene of the quiet trap: billed core-hours, with deallocated time removed | Rightsizing (110, 1.29×) | Exact billing basis, and the provider's acknowledgements confirm the rule | The reservation ledger and SKU catalogue: 72% of upsized cores are pinned at their size for the reservation term |
| 3 | **Decisive:** each control's serviceable core-hours, its target minus the parts pinned by reservations, service-level floors, exemption tags and non-checkpointing jobs | **Autoscale scale-in fix (57 against spot 47)**, 5th on rung 0 | — | — |

* **Position table.** The scale-in fix ranks 5th, 3rd and 4th on rungs 0 to 2 and leads only rung 3. Margins are 1.67, 1.29 and 1.22.
* **Discriminator dominance.** Rightsizing carries a 1.83× lead (110 against 60) into rung 3. The fix's serviceable share is 0.95 against
  rightsizing's 0.28, an edge of 3.39×, above 1.2 × 1.83 = 2.20.
* **Partial correction priced (L3).** A solver who checks the SKU catalogue but not the reservation ledger leaves rightsizing at 68k,
  1.19× the scale-in fix, and builds it. One who counts every training job as spot-ready, not only those that checkpoint, puts spot
  migration at 85k, 1.49× the scale-in fix. Neither half names the scale-in fix.
* **Grid.** Consumption basis (existence or billed) × serviceability (none, partial joins, all joins) = 6 cells. Only billed core-hours with
  every join names the scale-in fix. On existence the same joins name the lifecycle policy, because deallocated dev VMs swell its target.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The charter says "removes the most core-hours". The reservation ledger, the service catalogue and the exemption tags
   are finance, reliability and compliance records, and none mentions a control.
2. **Corpus blind for a computable reason.** *Every request in the acknowledgement file touched a VM the platform team itself owns, and
   platform-owned VMs carry no reservations, no service-level floors and no exemption tags, so every acknowledged request took full effect.*
   The file certifies each control's mechanics and the deallocation rule, and it shows serviceability of 100% everywhere.
3. **No arithmetic symptom.** Core-hours, power states, SKUs and acknowledgements reconcile on every rung, and the 350k growth is invariant.
4. **Not a row predicate.** Serviceable share is a separate join per control: VM to SKU family, cores to reservation term, scale set to
   service to floor, VM to tag, job to scheduler checkpoint config. Each one is then applied to that control's growth.
5. **The enumeration is arithmetic.** No VM row carries "removable". Each share comes out of its join.
6. **No cutover date.** Growth accrued across the month, and reservations were bought in earlier years.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The provider's acknowledgement file: 1,214 platform requests in the pilot quarter (resizes, deallocations, deletions, scale-ins
  and spot moves), each with its effective time and billing change.
* **What it certifies.** Mechanics and billing. A resize lowers billed cores by the size ratio, a deallocation stops cores immediately, a
  scale-in removes instances, and every acknowledged change matches the billing records 1,214 of 1,214.
* **What it is blind to.** Serviceability (property 2).
* **Twin pair.** The data-platform and search teams' upsized clusters are identical on SKU family, growth (+12k core-hours each),
  utilisation (31%) and response history. Rightsizing removes 11k from one and 5k from the other (2.2×), because 55% of search's cores sit
  under a three-year reservation.
* **Resemblance points at the decoy.** The platform's own clusters in the file, every one resized successfully, most resemble the
  data-platform team's upsized clusters.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The FinOps charter: "The control built is the one that removes the most core-hours from the week-4 run rate." The
  provider's billing terms: deallocated VMs accrue no compute charges. The reservation terms: a reservation applies to its size for its
  term.
* **Empirical pins.** Each serviceable share comes from its join. The deallocation rule is confirmed by the acknowledgements.
* **Voices.** Finance controller: "Developers spin up VMs like there's no tomorrow; cap them." Platform lead: "It's the VMs nobody ever
  deletes." Reliability manager: "Bigger instances are the price of the latency targets we were given."
* **Licensed wrong basis.** The charter records that the cost committee reviews spend by its largest driver in the provider's cost
  explorer and will see the proposal on that basis.

## 8. Determinism by construction

* **Weeks and states.** Weeks are days 0–6 and 21–27 of the trace, and power-state intervals are exact to the second. No VM changes state at
  a week boundary.
* **Joins.** Each VM has one SKU family, each reserved core has one term, each scale set maps to one service, and no job's checkpoint flag
  changed during the month.
* **Overlapping controls.** No VM is targeted by two controls, because each VM's growth is assigned to exactly one cause in the
  decomposition annex.
* **Spot readiness.** A training job is spot-ready only if its scheduler config checkpoints. The config file covers every job.
* **Maturity.** Week 4 is complete, and no VM's billing is still provisional at the extract.

## 9. Prompt sketch and deliverables

> I have one engineering quarter for one cost control, and finance wants a cap on VMs because creations are up 80%. Tell me which control
> we build, as a sentence for the cost committee, with the week-4 core-hours each of the five controls would take out, in thousands. Send
> `control_case.xlsx`, a chart `removable_core_hours.png`, and a one-page `control_decision.pdf`.

* `control_case.xlsx` — the five controls on every basis, the egress sheet (ask A), the storage sheet (ask B) and the acknowledgement
  back-test (ask C).
* `removable_core_hours.png` — for each control, a bar of the growth it targets with an inner bar of what it can remove. Reservation-pinned,
  floor-bound and exempt parts are hatched in the legend, and the title names the funded control.
* `control_decision.pdf` — the named control and why each other control removes less.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** Week-4 network egress in terabytes for each of six regions and four services. *Device:* cross-region
  replication is logged at both the source and destination regions with a direction flag, and the billing guide charges the source only.
  Summing both sides double-counts replication in the three regions that replicate. Egress never enters core-hours.
* **Ask B (device-carried).** This month's storage cost for each of eight business units across three tiers. *Device:* snapshots bill on
  changed blocks, while the inventory lists each snapshot's provisioned size. Pricing the inventory overstates snapshot cost about fivefold
  for the two units with daily snapshots.
* **Ask C (validity).** For each of the five request types in the acknowledgement file, the core-hours they removed beside what your
  construction predicts for those requests.
* **Decoupling.** Clearing the serviceability joins changes no figure in asks A or B. Ask C covers only platform-owned VMs.

## 11. Rubric arithmetic

6 regions × 4 services (ask A) + 8 units × 3 tiers (ask B) + 5 request types × 2 (ask C) + the named control, five removable figures and the
winning margin + 5 named chart parts + 3 files ≈ 73 criteria.

## 12. World-building constraints

* Week 1 burned 1.00M core-hours and week 4 1.35M. Targets on existence are lifecycle 150, rightsizing 90, scale-in 50, spot 40 and quota 20.
  On billed core-hours they are 70 / 110 / 60 / 85 / 30.
* Serviceable shares are rightsizing 0.28 (0.62 with the SKU join alone), lifecycle 0.40, scale-in 0.95, spot 0.55 and quota 0.50.
* Creations rose 80%, and 70% of new VMs lived under a day.
* The twin clusters are identical on every VM-table column, and 55% of search's cores are reserved.
* All 1,214 acknowledged requests touched platform-owned VMs.
* Replication flags and snapshot billing never touch VMs, power states or reservations.
