# FC11 — The batch capacity a compute cell can promise next quarter, when the platform's share is levied on totals that include it

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Supply Chain & Logistics · data-centre capacity planning |
| Mirrors | Committing a residual capacity guarantee when a shared platform's reservation is a share of totals that include itself (batch guarantees in Borg- and Kubernetes-style cells, AWS capacity reservations net of control-plane overhead, the infrastructure levy in internal chargeback at Meta and Google) |
| Decision shape | One figure committed at a date: the batch guarantee filed at the quarterly capacity review |
| Committed call | Cores of reservation guaranteed to batch training teams for next quarter, to the nearest 1,000 |
| Gap · Pattern | Gap 3 (objective) over Gap 4 (rule) · a self-referencing levy (a share computed on a total that contains it), recovered only by reproducing the cells' settled guarantees, whose budget ceilings bind only after the fixed point, graded on a residual (the sensitive root) |
| Gate G mechanism | binding_constraint, with forecasting support |
| Measured traps engaged | #22 solves a self-referencing rule in one pass · #6 treats a mixed segment all one way · #4 never tests its reading against the control |
| Calibration form | Settled-transaction ledger: the four sister cells' reservation ledgers, settled quarterly for six quarters at cell level (reservable capacity and the settled batch guarantee), beside each tenant's own reservation and budget in the reservation register |
| Driving force | Batch gets whatever reservable capacity is left after firm reservations. The policy levies a platform share of one quarter of each firm reservation, and the share is itself held in the tenant's name, so it sits inside its own base: a third of the own reservation, not a quarter. No document says so. Only that reading reproduces the 24 settled cell-quarter guarantees, and C-22's one budget quarter reproduces only when budgets cap own plus share. At a third, the five largest tenants cross budgets frozen at this quarter's level, their own reservations are cut to fit, and 23,430 cores return to batch. At a quarter, nobody reaches a budget. The guarantee is a small residual of large totals, so the base decides it. |

## 1. Situation

A compute cell's capacity review commits next quarter's batch guarantee, the reservation that batch training teams plan their quarter
around. The hardware plan fixes the cell at 5,180 machines of 96 cores, and the capacity memo sets next quarter's overcommit ratio at
1.45, so 721,056 cores are reservable. Eleven firm tenants reserve first: ten product services and the deadline-batch class. The
planning standard projects each tenant's own reservation from its last four quarters. Next quarter's budgets were frozen at this
quarter's level. The ledger settles each cell's quarter at cell level: reservable capacity and the batch guarantee delivered.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the hardware plan, the ledger, the reservation register, the policy, the glossary, the budgets and
  the job registry. No one's claim about their own numbers is overturned. The difficulty is a levy whose base contains itself, and
  ceilings that only that base reaches.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete both voices and the finance basis. The policy's "one quarter" applied to each tenant's projection still gives
  77,310 cores, with no budget in sight.
* **Instrument repair.** No file is suspect: the ledger settles at cell level and every settled guarantee is there, the register's
  platform row is the platform team's request and is labelled as one, and the registry's scheduling class is complete. Splitting the
  register's batch line by class moves rung 0 to rung 1's 81,060. Even a ledger that also settled each tenant's share would leave rung 2
  at 77,310, because the one-pass levy does not read the ledger, and the budget cut on own plus share would still be needed for 58,000.
* **Lens swap.** The naive read and the answer differ in moment and population: last quarter's reservations, when no tenant was near a
  budget, against next quarter's, in which five tenants are cut to theirs.

## 3. The driving force

A strong solver separates deadline batch from best-effort batch, projects each tenant and levies the platform share the policy states:
one quarter of the firm reservation. Read on the tenant's own reservation, that is 25%, and every tenant stays 1.6% under budget. Then it
tests the reading against the ledger. Each settled guarantee is reservable capacity less every firm tenant's own reservation less the
platform's levy, and at a quarter of own the reading over-predicts all 24 settled guarantees by a twelfth of own reservations. They
reproduce, all 24, only when the share is a quarter of a total that contains it: share = 0.25 × (own + share), a third of own. Sister
cell C-22's one budget quarter reproduces only when budgets cap own plus share as well. At a third, T1–T5 sit 5% over their frozen
budgets. The policy sends demand above a budget to the public cloud, so their own reservations shrink until own plus share equals the
budget, and 23,430 cores go back to the residual. The batch guarantee is 57,820 cores out of 721,056, so the levy's base decides it.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Reservable capacity minus projected service reservations minus the platform's standing request in the register; deadline batch left inside batch | 126,060, +118% | The register's own rows, rolled forward | **E29 (a mixed segment split through a join):** the job registry's scheduling class splits "batch" into deadline batch, which the policy treats as a firm tenant with a budget, and best-effort |
| 1 | The same with deadline batch reserved as a firm tenant | 81,060, +40% | Every firm reservation reserved, every class where the policy puts it | The policy: the platform's reservation is a levy on firm reservations, not its request |
| 2 | Each firm reservation levied at a quarter of its own reservation; budgets checked, none reached | 77,310, +34% | The policy's levy applied tenant by tenant, with every budget respected | The ledger: a quarter of own over-predicts all 24 settled cell-quarter guarantees by a twelfth of own reservations, 25,000 to 40,000 cores each |
| 3 | **Decisive:** the levy solved on a base that contains it (firm reservation = own ÷ 0.75), recovered by reproducing all 24 settled guarantees; T1–T5 cut to budget (own = 0.75 × budget); guarantee = capacity minus firm reservations | **57,820 → 58,000** | — | — |

* **Figure shape.** Every rung overstates the guarantee (+118%, +40%, +34%). The decisive rung's two parts pull opposite ways. The fixed
  point alone takes the guarantee to 34,390, and the five budgets it triggers return 23,430.
* **Partial correction priced (L3).** A solver who fits a levy of a third of own to the settled guarantees but checks budgets against own
  reservations, or against the one-quarter totals, sees no crossing and files 34,390 (−40.5%), further from the answer than rung 2. One
  who fits the levy with deadline batch still inside batch finds no constant rate that reproduces more than one settled guarantee, because
  deadline batch's share of own reservations moves between 8% and 12%; carrying the best-fitting rate (0.48 of the services' own
  reservations) without budgets gives 25,460 (−56%).
* **Grid.** Platform (standing request, a quarter of own, a quarter of firm) × budgets (checked on the levied total, ignored) × deadline
  batch (firm, batch) gives 8 distinct cells, because the budgets bind only under a quarter of firm: 126,060, 81,060, 133,560, 77,310,
  94,390, 34,390, 117,820 and the answer. The nearest wrong cell is rung 2 at +34%. No cell is within 30% of the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy says one quarter of the firm reservation, and the glossary defines a firm reservation only as
   capacity held in a tenant's name for the quarter. No sentence says the share is held in that name, that it is part of its own base,
   that budgets cap own plus share, or that a budget crossing returns capacity to batch.
2. **The reproduction numbers, and a ceiling the cell has never met.** The levy solved on its own base, with deadline batch firm and
   budgets on own plus share, reproduces 24 of 24 settled cell-quarter guarantees to the core. A quarter of own reproduces none, a third
   of own with deadline batch inside batch none, and a third without budgets 23 (it misses C-22's budget quarter by 21,000 cores). The
   rule is a construction: firm tenants from the registry's scheduling class, the levy solved on a base containing itself, budgets
   applied to the solved total, the guarantee as the residual; no ledger line holds a share. *In every settled quarter of this cell no
   tenant's firm reservation came within 3% of its budget, because budgets carried 10% headroom until this quarter's freeze.*
3. **No arithmetic symptom.** Reservations sum to capacity under every reading, the settled guarantees tie to delivered capacity, and
   under the one-pass levy no reservation exceeds its budget.
4. **Not a row predicate.** The share solves an equation whose unknown is in its own base, and whether a budget binds depends on that
   solution, tenant by tenant, before the residual is taken.
5. **The enumeration is arithmetic.** Which tenants sit at budget is computed only after the fixed point. No column flags them.
6. **No cutover date.** The budget freeze is a level, not an event, and nothing steps in any series.
7. **Survives deletion.** No wrong number exists to delete. Without the voices, rung 2 is where a careful build stops.

## 6. The calibration corpus

* **Form.** The settled reservation ledgers of this cell and its three sister cells: six quarters each, with each cell-quarter's
  reservable capacity and settled batch guarantee, beside the register's own reservations and budgets for every tenant.
* **What it certifies.** The levy's base, as a residual: in all 24 cell-quarters, capacity less the guarantee is exactly four thirds of
  own reservations with deadline batch counted firm, except C-22's budget quarter. It also certifies the projection standard: each
  tenant's four-quarter projection reproduces its next settled own reservation within 1%.
* **Free training instance (O3).** In sister cell C-22, three tenants reached their budgets in one quarter, and the settled guarantee
  rose by the cores their cuts released. It is visible only to a solver who reproduces that quarter, harmless there, and the one place
  the levy and the budget are composed.
* **Twin pair.** Cells C-14 and C-22 in that quarter are identical on every cell-level column: reservable capacity, total own
  reservations, total budgets, tenant count and deadline batch. Their settled guarantees are 21,000 and 42,000 cores (2.0×), because in
  C-22 three tenants' budgets sat between a quarter and a third above their own reservations. Only the solved levy with budgets on own
  plus share reproduces both.
* **Resemblance points at the decoy.** Next quarter in this cell resembles its own settled quarters on every column, and in none of them
  did a budget bind.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The capacity memo: overcommit 1.45 next quarter. The hardware plan: 5,180 machines of 96 cores. The policy: each firm
  reservation carries a platform share of one quarter of the firm reservation, and demand above a tenant's budget is served from the
  public cloud. The glossary: a firm reservation is capacity held in a tenant's name for the quarter, whether or not it is used. The
  budget sheet: next quarter's budgets, each the most a tenant's firm reservation may reach. The register: each tenant's settled own
  reservation by quarter, and the platform team's standing request of 125,000 cores.
* **Empirical pins.** The share's base, by reproducing the settled guarantees. Projections, from the planning standard confirmed on the
  register. Deadline batch, from the job registry's scheduling class.
* **Voices.** The cell's capacity lead: "The platform line barely moves; carry it." The batch programme manager: "Last quarter we got
  about eighty thousand cores, and nothing big has changed."
* **Licensed wrong basis.** The capacity memo records that finance's chargeback model levies the platform at one quarter of each tenant's
  own reservation and will present the guarantee on that basis at the review.

## 8. Determinism by construction

* **Fixed point.** The levy equation has one solution per tenant (own ÷ 0.75). Capped tenants resolve to own = 0.75 × budget with no
  iteration across tenants, because a share depends only on its tenant's reservation.
* **Reproduction.** Guarantees are settled to the core. The solved levy reproduces all 24 exactly, and every rival reading misses every
  cell-quarter it misses by at least 21,000 cores, so no rounding convention changes the count.
* **Budget margins.** Each capped tenant's one-pass firm reservation sits 1.6% under its budget and its fixed-point reservation 5.0% over,
  and every uncapped tenant sits at least 6% under its budget under both readings, so projection conventions cannot change the set.
* **Projection.** Every tenant has four full quarters of growth in the register, and the standard's mean of four ratios is unambiguous.
* **Capacity.** Reservable capacity is filed arithmetic, machines × cores × overcommit, with no maintenance reserve, as the memo states.
* **Rounding.** The unrounded 57,820 rounds to 58,000. The nearest wrong cell is 19,000 cores away.

## 9. Prompt sketch and deliverables

> At Thursday's capacity review I commit the batch guarantee for next quarter, and the training teams plan their quarter on it, so give
> me one number, to the nearest thousand cores. Our capacity lead thinks the platform line barely moves from quarter to quarter. Send me
> `batch_guarantee.xlsx`, a chart `cell_reservation_stack.png`, and a one-page `capacity_review_note.pdf` with the figure.

* `batch_guarantee.xlsx` — the reservation build tenant by tenant, the usage-ratio sheet (ask A) and the delivery sheet (ask B).
* `cell_reservation_stack.png` — next quarter's reservable capacity as stacked bars, the one-quarter and solved readings side by side:
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
* **Ask C (validity).** The guarantee under each of the four rung constructions, with each one's hits on the 24 settled cell-quarter
  guarantees.
* **Decoupling.** Replacing the solved levy with a quarter of own reservation changes no figure in asks A or B.

## 11. Rubric arithmetic

11 tenants × 2 (ask A) + 6 quarters × 2 (ask B) + 4 constructions × 2 (ask C) + the committed guarantee, the tenants at budget and the
platform's reservation + 5 named chart parts + 3 files ≈ 53 criteria.

## 12. World-building constraints

* Projected own reservations (thousand cores): T1 120, T2 90, T3 60, T4 55, T5 45, T6 40, T7 25, T8 20, T9 10, T10 5, deadline batch 45.
  Budgets for T1–T5 at 1.27 × own (152.4, 114.3, 76.2, 69.85, 57.15); all others at least 6% above own ÷ 0.75.
* Rung figures 126,060 / 81,060 / 77,310 / 57,820. The fixed point without budgets is 34,390. The platform reservation at the answer is
  165,810. The platform's standing request (125,000) differs from its settled levy by 20–30% in every quarter.
* The ledger carries no share or firm-reservation line. In every settled cell-quarter, capacity less the guarantee is four thirds of own
  reservations with deadline batch firm, except C-22's budget quarter; no budget ever bound in this cell. Deadline batch is 8–12% of own
  reservations, varying by quarter. C-14 and C-22 are identical on every cell-level column in C-22's budget quarter.
* Migration duplicates and reclaimed-capacity tags never touch reservations, budgets or guarantees.
