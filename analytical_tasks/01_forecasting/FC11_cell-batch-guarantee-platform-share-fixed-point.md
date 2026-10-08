# FC11 — The batch capacity a compute cell can promise next quarter, when the platform's share is levied on totals that include it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · data-centre capacity planning |
| Mirrors | Committing a residual capacity guarantee when a shared platform's reservation is a share of totals that include itself (batch guarantees in Borg- and Kubernetes-style cells, AWS capacity reservations net of control-plane overhead, the infrastructure levy in internal chargeback at Meta and Google) |
| Decision shape | One figure committed at a date: the batch guarantee filed at the quarterly capacity review |
| Committed call | Cores of reservation guaranteed to batch training teams for next quarter, to the nearest 1,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · a self-referencing levy (a share computed on a total that contains it) whose budget ceilings bind only after the fixed point, graded on a residual (the sensitive root) |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #6 treats a mixed segment all one way · #4 never tests its reading against the control |
| Calibration form | Settled-transaction ledger: the cells' internal reservation ledgers, settled quarterly for six quarters, with each tenant's own reservation, platform share, firm reservation and budget |
| Driving force | Batch gets whatever reservable capacity is left after firm reservations. The policy levies a platform share of one quarter of each firm reservation, and the glossary defines a firm reservation as the tenant's own reservation plus that share. So the share is a third of the own reservation, as the ledger has settled it every quarter, not a quarter of it. At a third, the five largest tenants cross budgets frozen at this quarter's level, their own reservations are cut to fit, and 23,430 cores return to batch. At a quarter, nobody reaches a budget. The guarantee is a small residual of large totals, so the reading decides it. |

## 1. Situation

A compute cell's capacity review commits next quarter's batch guarantee, the reservation that batch training teams plan their quarter
around. The hardware plan fixes the cell at 5,180 machines of 96 cores, and the capacity memo sets next quarter's overcommit ratio at
1.45, so 721,056 cores are reservable. Eleven firm tenants reserve first: ten product services and the deadline-batch class. The
planning standard projects each tenant's own reservation from its last four quarters. Next quarter's budgets were frozen at this
quarter's level.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the hardware plan, the ledger, the policy, the glossary, the budgets and the job registry. No
  one's claim about their own numbers is overturned. The difficulty is a levy whose base contains itself, and ceilings that only that
  base reaches.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The policy's "one quarter" applied to each tenant's projection still gives
  77,310 cores, with no budget in sight.
* **Instrument repair.** Make the ledger and every projection perfect; they are. The levy's base and the budget crossings are properties
  of next quarter's reservations, which no record of the past contains.
* **Lens swap.** The naive read and the answer differ in moment and population: last quarter's reservations, when no tenant was near a
  budget, against next quarter's, in which five tenants are cut to theirs.

## 3. The driving force

A strong solver separates deadline batch from best-effort batch, projects each tenant and levies the platform share the policy states:
one quarter of the firm reservation. If the base is read as the tenant's own reservation, that is 25%, and every tenant stays 1.6% under
budget. The glossary defines a firm reservation as own reservation plus platform share. So the share is a quarter of a total that contains
it: share = 0.25 × (own + share), which is a third of own. Every settled quarter in the ledger shows exactly that. At a third, T1–T5 sit
5% over their frozen budgets. The policy sends demand above a budget to the public cloud, so their own reservations shrink until own plus
share equals the budget, and 23,430 cores go back to the residual. The batch guarantee is 57,820 cores out of 721,056, so the reading of
one word decides it.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Reservable capacity minus projected service reservations minus the platform's last settled reservation; deadline batch left inside batch | 126,060, +118% | The ledger's own lines, rolled forward | **E29 (a mixed segment split through a join):** the job registry's scheduling class splits "batch" into deadline batch, which the policy treats as a firm tenant with a budget, and best-effort |
| 1 | The same with deadline batch reserved as a firm tenant | 81,060, +40% | Every firm reservation reserved, every class where the policy puts it | The policy: the platform reservation is a levy on firm reservations, not a fixed line |
| 2 | Each firm reservation levied at a quarter of its own reservation; budgets checked, none reached | 77,310, +34% | The policy's levy applied tenant by tenant, with every budget respected | The ledger: in all six settled quarters each share is exactly a third of own reservation, as the glossary's definition requires |
| 3 | **Decisive:** firm reservation = own ÷ 0.75; T1–T5 cut to budget (own = 0.75 × budget); guarantee = capacity minus firm reservations | **57,820 → 58,000** | — | — |

* **Figure shape.** Every rung overstates the guarantee (+118%, +40%, +34%). The decisive rung's two parts pull opposite ways. The fixed
  point alone takes the guarantee to 34,390, and the five budgets it triggers return 23,430.
* **Partial correction priced (L3).** A solver who finds the third-share in the ledger but checks budgets against the one-quarter totals
  sees no crossing and files 34,390 (−40.5%), further from the answer than rung 2. Applying budgets to own reservations instead of firm
  ones also binds nobody and lands in the same place.
* **Grid.** Platform (flat line, a quarter of own, a quarter of firm) × budgets (checked on the levied total, ignored) × deadline batch
  (firm, batch) gives 10 feasible cells. The nearest wrong cell is rung 2 at +34%. The fixed point with budgets but deadline batch left
  inside batch sits at +104%. No cell is within 30% of the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says one quarter of the firm reservation, and the glossary defines that term in another document. No
   sentence says the share is part of its own base, or that a budget crossing returns capacity to batch.
2. **Corpus blind to the ceiling for a computable reason.** *In every settled quarter of this cell no tenant's firm reservation came within
   3% of its budget, because budgets carried 10% headroom until this quarter's freeze.* The ledger pins the third-share on 66 of 66
   tenant-quarters and shows no budget binding here; a quarter of own misses all 66.
3. **No arithmetic symptom.** Shares, firm reservations and the platform reservation tie, and reservations sum to capacity under every
   reading. Under the one-pass levy no reservation exceeds its budget.
4. **Not a row predicate.** The share solves an equation whose unknown is in its own base, and whether a budget binds depends on that
   solution, tenant by tenant, before the residual is taken.
5. **The enumeration is arithmetic.** Which tenants sit at budget is computed only after the fixed point. No column flags them.
6. **No cutover date.** The budget freeze is a level, not an event, and nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The settled reservation ledgers: six quarters for this cell and its three sister cells, with each tenant's own reservation,
  platform share, firm reservation, budget and the settled batch guarantee.
* **What it certifies.** The levy's base: every share is a third of own reservation (a quarter of firm), 66 of 66 tenant-quarters in this
  cell. It also certifies the projection standard: each tenant's four-quarter projection reproduces the next settled quarter within 1%.
* **Free training instance (O3).** In sister cell C-22, three tenants reached their budgets in one quarter, and the ledger shows their own
  reservations cut to 0.75 × budget and the guarantee raised to match. It is visible and harmless there, and it is the one place the
  levy and the budget are composed.
* **Twin pair.** Cells C-14 and C-22 in that quarter are identical on every cell-level column: reservable capacity, total own
  reservations, total budgets, tenant count and deadline batch. Their settled guarantees are 21,000 and 42,000 cores (2.0×), because in
  C-22 three tenants' budgets sat between a quarter and a third above their own reservations. Only the third-share with budgets
  reproduces both.
* **Resemblance points at the decoy.** Next quarter in this cell resembles its own settled quarters on every column, and in none of them
  did a budget bind.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity memo: overcommit 1.45 next quarter. The hardware plan: 5,180 machines of 96 cores. The policy: each firm
  reservation carries a platform share of one quarter of the firm reservation, and demand above a tenant's budget is served from the
  public cloud. The glossary: a firm reservation is a tenant's own reservation plus its platform share. The budget sheet: next quarter's
  budgets.
* **Empirical pins.** The share's base, from the ledger. Projections, from the planning standard confirmed on the ledger. Deadline batch,
  from the job registry's scheduling class.
* **Voices.** The cell's capacity lead: "The platform line barely moves; carry it." The batch programme manager: "Last quarter we got
  about eighty thousand cores, and nothing big has changed."
* **Licensed wrong basis.** The capacity memo records that finance's chargeback model levies the platform at one quarter of each tenant's
  own reservation and will present the guarantee on that basis at the review.

## 8. Determinism by construction

* **Fixed point.** The levy equation has one solution per tenant (own ÷ 0.75). Capped tenants resolve to own = 0.75 × budget with no
  iteration across tenants, because a share depends only on its tenant's reservation.
* **Budget margins.** Each capped tenant's one-pass firm reservation sits 1.6% under its budget and its fixed-point reservation 5.0% over,
  and every uncapped tenant sits at least 6% under its budget under both readings, so projection conventions cannot change the set.
* **Projection.** Every tenant has four full quarters of growth in the ledger, and the standard's mean of four ratios is unambiguous.
* **Capacity.** Reservable capacity is filed arithmetic, machines × cores × overcommit, with no maintenance reserve, as the memo states.
* **Rounding.** The unrounded 57,820 rounds to 58,000. The nearest wrong cell is 19,000 cores away.

## 9. Prompt sketch and deliverables

> At Thursday's capacity review I commit the batch guarantee for next quarter, and the training teams plan their quarter on it, so give
> me one number, to the nearest thousand cores. Our capacity lead thinks the platform line barely moves from quarter to quarter. Send me
> `batch_guarantee.xlsx`, a chart `cell_reservation_stack.png`, and a one-page `capacity_review_note.pdf` with the figure.

* `batch_guarantee.xlsx` — the reservation build tenant by tenant, the usage-ratio sheet (ask A) and the delivery sheet (ask B).
* `cell_reservation_stack.png` — next quarter's reservable capacity as stacked bars, the one-quarter and one-third readings side by side:
  own reservations by tenant, platform share, deadline batch and the guarantee, with budgets marked on T1–T5 and the guarantee labelled.
* `capacity_review_note.pdf` — the committed guarantee, the tenants at budget and the finance basis the review will see.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the eleven firm tenants, last quarter's peak 5-minute usage-to-reservation ratio and
  the number of windows above 90%. *Device:* an instance in live migration reports from both machines for the overlapping window, as the
  migration log documents. Summing per window without de-duplicating by instance ID overstates peaks for the four tenants that migrate
  most.
* **Ask B (device-carried).** For each of the six settled quarters, batch core-hours delivered against the guarantee. *Device:* best-effort
  work running on reclaimed capacity above the guarantee is tagged as reclaimed, and the batch agreement excludes it from delivery.
  Counting it puts delivery above 100% in four quarters, against true ratios of 91–98%.
* **Ask C (validity).** The guarantee under each of the four rung constructions, with each one's hits on the 66 settled shares.
* **Decoupling.** Replacing the third-share with a quarter of own reservation changes no figure in asks A or B.

## 11. Rubric arithmetic

11 tenants × 2 (ask A) + 6 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed guarantee, the tenants at budget and the
platform's reservation + 5 named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Projected own reservations (thousand cores): T1 120, T2 90, T3 60, T4 55, T5 45, T6 40, T7 25, T8 20, T9 10, T10 5, deadline batch 45.
  Budgets for T1–T5 at 1.27 × own (152.4, 114.3, 76.2, 69.85, 57.15); all others at least 6% above own ÷ 0.75.
* Rung figures 126,060 / 81,060 / 77,310 / 57,820. The fixed point without budgets is 34,390. The platform reservation at the answer is
  165,810.
* Every settled share in this cell is a third of own reservation, and no budget ever bound here. C-22's budget quarter and the C-14/C-22
  twin quarter sit in the sister cells' ledgers.
* Migration duplicates and reclaimed-capacity tags never touch reservations, shares or budgets.
