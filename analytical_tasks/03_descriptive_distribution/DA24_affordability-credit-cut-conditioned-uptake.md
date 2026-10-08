# DA24 — Where to set the income cut so an affordability credit reaches exactly the 120,000 households it is budgeted for

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Demographic & Social Science · household income and affordability |
| Mirrors | Sizing an eligibility cut against a fixed budget when take-up depends on how each customer is reached (telecom and broadband discount tiers, subscription hardship plans, Google and Meta programme credits offered in-product) |
| Decision shape | An allocation under a cap: the cut on the income distribution at which forecast enrolled credits equal the funded number |
| Committed call | The Year-1 eligibility cut, as a whole percentage of the poverty guideline |
| Gap · Pattern | Gap 2 (population) over Gap 3 (objective) · Pattern E (conditioned yield), with G9 (the measured outcome is enrolment, not eligibility) |
| Gate G mechanism | binding_constraint, with decomposition_attribution |
| Measured traps engaged | #13 validates on one population, applies to another · #6 treats a mixed segment all one way · #14 coarsens the segment it was asked about |
| Calibration form | Pilot log: every eligible account offered the credit in the two pilot counties, with its outcome |
| Driving force | The pilot's enrolment rate is correct and applies to nobody. Enrolment is all-or-nothing by how an account is reached, not by income. Paper-billed accounts never enrolled; accounts reached digitally enrolled at 61%. The statewide account base and the pilot towns carry that channel mix in opposite income patterns. |

## 1. Situation

An electricity and broadband provider has budget for 120,000 monthly credits in Year 1 and must file an eligibility cut, a percentage of the
federal poverty guideline for household size, with the state commission. Last year's pilot in two counties offered the credit to every
eligible account and recorded who enrolled. The customer panel, a weighted survey of 6,000 accounts, carries household income bands and
sizes. The commission's staff expect the cut to be set so the budget is used, not exceeded.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the panel's weighted income distribution, the pilot's enrolment counts and the billing extract. Nothing
  anyone reports is overturned. The difficulty is which enrolment behaviour applies to the statewide eligible pool.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Remove every voice. The pilot's pooled rate still transports cleanly in arithmetic and still sets the wrong cut.
* **Instrument repair.** Perfect income measurement and a complete pilot log change nothing. The pilot is already complete, and the issue is
  transport across a channel mix.
* **Lens swap.** The pilot towns' accounts and the statewide account base are different populations. The answer is about the statewide
  base's forward enrolment.

## 3. The driving force

A strong solver builds the customer income distribution, applies the pilot's enrolment rate and solves for the cut. It may even refine the
rate by income band, because the pilot shows lower enrolment in upper bands. That band gradient is not about income. Enrolment depended
entirely on whether the offer reached the account digitally: 0 of 1,240 paper-billed eligible accounts enrolled, against 61.0% of
digitally-billed ones. The account-reach split was the same in every band. In the pilot towns paper billing concentrated in the upper
bands; statewide it concentrates in the lowest bands. The pooled rate and the band rates are both correct for the pilot and both wrong
for the state.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Cut on the survey distribution of all households in the territory, assuming every eligible household enrols | 112% of guideline | A public benchmark distribution, cleanly weighted | The credit is per customer account, and the panel is the account population |
| 1 | Cut on the panel's weighted account distribution, every eligible account enrolling | 121% | The right population, still at full take-up | The pilot shows not every eligible account enrols |
| 2 | Pilot enrolment by income band applied to the panel distribution | 128% | Refines the pooled rate by the obvious segment | Within every pilot band, enrolment splits 0% against 61% by bill delivery |
| 3 | **Decisive:** enrolment conditioned on bill delivery, with the statewide eligible pool's channel mix by band from the billing extract | **156%** | — | — |

* **Figure shape.** The answer is the maximum cell, so every partial application sets too low a cut and leaves budget unused.
* **Partial correction priced (L3).** A solver who conditions on channel but carries the pilot towns' channel mix lands at 129%, no closer than
  rung 2. The pooled pilot rate (43%) lands at 140%, the nearest wrong cell. The twin towns refute it, because no single rate reproduces both.
* **Grid.** Population (survey or panel) × enrolment (full, pooled, band, channel) × channel mix (pilot or state) gives 12 feasible cells.
  The nearest non-answer cell is the pooled rate at 140%, 16 points (10%) below the answer.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** No document says the offer reached accounts only digitally. The programme note says Year 1 runs on the pilot's
   process.
2. **The corpus pins the conditioning only through a join.** The pilot log carries account IDs, income band, household size and town. Bill
   delivery lives in the billing extract, so the log's own group-bys show a band gradient and no channel split.
3. **No arithmetic symptom.** Panel weights sum to the account base, pilot counts reconcile to offers, and every rung's enrolment total
   reconciles.
4. **Not a row predicate.** The answer needs channel-conditioned rates transported across a by-band channel mix, then an inverse solve on the
   cumulative distribution.
5. **The enumeration is arithmetic.** The forecast enrolled count at each cut is a sum over band × channel cells.
6. **No cutover date.** Nothing steps; the pilot is one closed window.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The pilot log: 6,400 eligible accounts in two counties, offered the credit, with the outcome (enrolled or not).
* **What it certifies.** That enrolment is far below full take-up. The pooled rate (43%) and the band rates are reproduced exactly by their
  own constructions on the pilot.
* **The absolute split (O2).** 0 of 1,240 paper-billed eligible accounts enrolled; 3,148 of 5,160 digitally-billed accounts enrolled
  (61.0%), in every band and town.
* **Twin pair.** Pilot towns Arden and Belcourt are identical on eligible accounts by band and household size and on pooled demographics.
  Enrolment differs 2.1× (paper share 12% against 52%), so no band- or town-level rate reproduces both.
* **Resemblance points at the decoy.** The statewide income distribution most resembles Belcourt, the town whose enrolment rate is lower.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The commission order fixes the cap (120,000 monthly credits), the eligibility basis (household income against the
  guideline for household size) and that the cut is filed as a whole percentage. The programme note fixes that Year 1 uses the pilot's
  enrolment process.
* **Empirical pins.** The channel split, from the pilot log joined to the billing extract.
* **Voices.** The regulatory lead: "Income is what drives take-up; the band rates are the careful version." The commission liaison: "Staff
  will look for the pilot rate in the filing."
* **Licensed wrong basis.** The commission order notes that intervenors will present a cut set on the survey distribution at full take-up.

## 8. Determinism by construction

* **Band interpolation.** The cut is solved on the panel's banded distribution with linear interpolation inside bands. The world puts the
  answer's crossing in the interior of a band, and Pareto interpolation gives the same whole percentage.
* **Household size.** The guideline varies by size. The panel carries size, and every rung uses size-specific guidelines, so no rung
  diverges on it.
* **Weights.** The panel's design weights are pinned in its codebook. An unweighted panel is a hazard that lands 11 points off.
* **Channel stability.** No account changed bill delivery during the pilot window, so the join resolves without a time convention.

## 9. Prompt sketch and deliverables

> The commission wants our Year-1 cut, and the 120,000 credits we funded should be used, not overrun. The regulatory lead is confident
> income drives take-up. Give me the cut as a whole percentage of the guideline, in one sentence I can file, plus `cut_build.xlsx` with the
> sheets below, `enrolment_curve.png`, and a one-page `filing_note.pdf`.

* `cut_build.xlsx` — the cut solve, the burden table (ask A) and the bill table (ask B).
* `enrolment_curve.png` — forecast enrolled credits against the cut under the four rung bases, with the 120,000 line, the chosen cut and the
  pilot's two towns marked.
* `filing_note.pdf` — the committed cut and the alternatives intervenors will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of 9 income bands × 3 household-size groups, the weighted share of accounts whose combined
  energy and broadband bills exceed 6% of income. *Device:* the open top band needs the panel codebook's Pareto midpoint convention, and
  using the band's lower bound inflates burden in the upper bands.
* **Ask B (device-carried).** The twelve-month median monthly bill per income band. *Device:* estimated-read bills are followed by true-up
  bills, as the billing guide documents. Summing both double-counts usage for 7% of accounts.
* **Ask C (validity).** The forecast enrolled credits at the filed cut under each of the four rung bases.
* **Decoupling.** Clearing the channel conditioning changes no figure in asks A or B.

## 11. Rubric arithmetic

27 cells (ask A) + 9 band medians (ask B) + 4 bases (ask C) + the committed cut, enrolled count at the cut and budget use + 5 named chart
parts + 3 files ≈ 50 criteria.

## 12. World-building constraints

* The pilot has 6,400 eligible accounts: 1,240 paper (0 enrolled) and 5,160 digital (3,148 enrolled). In the pilot towns paper billing
  rises with income band; statewide, among eligible accounts, it falls with income band.
* Rung cuts are 112% / 121% / 128% / 156%. The pooled-rate cell is 140%, and every other cell of the 12-cell grid sits at least 16 points (10%) from the answer.
* Arden and Belcourt are identical on every pilot-log column.
* Panel weights reconcile to the account base. No account changed channel during the pilot.
* The burden and bill devices touch no quantity in the cut solve.
