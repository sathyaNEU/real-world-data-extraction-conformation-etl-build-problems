# OS29 — How a fund splits $720M of wind repowering capital, when the turbines whose support is ending will keep turning anyway

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · infrastructure investment |
| Mirrors | Refresh capital allocated against an end-of-support notice read as end of life (network-equipment refresh at vendor end-of-support dates while third-party maintenance keeps fleets running, device trade-up programmes timed to an operating-system end of life, database migrations justified by a version's support date) |
| Decision shape | An allocation under a cap: $720M of repowering capital, in whole turbines, across nine candidate wind projects |
| Committed call | New turbines per project, and the incremental energy the split buys, in GWh a year averaged over the new turbines' 20-year life |
| Gap · Pattern | Gap 1 (time) over Gap 2 (population) · E24 (continuity across a closure: the end of manufacturer support changes the turbines' supplier, not their operation), with E17 below it (an energy model validated on flat-site repowers, applied to ridge sites) |
| Gate G mechanism | forecasting, with binding_constraint |
| Measured traps engaged | #23 reads a closure notice as a market exit · #13 validates on one population, applies to another · #10 notes a binding limit as a risk |
| Calibration form | Settled-transaction ledger: the fund's portfolio ledger of monthly settled energy sales and O&M payments by vendor, 31 operating projects since 2015 |
| Driving force | The manufacturer ends parts and service for the K-77 turbine on 31 March 2027, and every competent no-repower path stops those turbines there, which makes repowering the four K-77 projects look like pure gain. The ledger shows the southern K-77 fleet passing its own end of support in March 2022: manufacturer invoices stop, an independent service provider's start the next month, and settled energy runs on without a step. The no-repower path runs to each project's planning-consent end, and the K-77 increments shrink by 35% or more. |

## 1. Situation

An infrastructure fund co-invests with owners to repower old wind farms. Next build season it has $720M, enough for about 60 new 6 MW
turbines at $9–14M each, and nine partner projects want them. The investment policy scores repowering on incremental energy against each
project's no-repower path over the new turbines' 20-year life, and allocates whole turbines in order of value per dollar. Four of the nine
run the K-77 1.5 MW model, and the manufacturer has given notice that K-77 support in the northern region ends in March 2027. The fund's
own repower energy model has met its forecast on all five repowers completed so far.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the manufacturer's notice, the energy model's five validations, the interconnection and consent
  registers, and the ledger. The notice is true: support does end. Nothing is overturned. The difficulty is what the no-repower path is once
  support ends, which the notice does not say.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the origination lead's view and every voice. The dated notice and the policy's no-repower path still lead any
  careful analyst to stop the K-77s in 2027.
* **Instrument repair.** No file is suspect. The notice, the ledger, the consent and interconnection registers and the atlas are complete
  and current, and the notice records exactly what it claims, the end of manufacturer support. Rungs 0, 1 and 2 still name Bitter Creek,
  Antelope Flats and Fox Hollow. What the end of support means for operation is inferred from another fleet's history, and no better
  instrument of the forward projects records it.
* **Lens swap.** The answer moves the no-repower path of four projects across 14 future years, a different population of turbine-years
  from the one the notice describes.

## 3. The driving force

A strong solver builds each project's increment as new-turbine energy minus the no-repower path, calibrates the fund's model by terrain,
caps exports at each project's interconnection limit, and ranks by value per dollar. The no-repower path is where it trusts the pack most.
The notice dates the end of K-77 support, so the old turbines' energy stops in 2027 and repowering a K-77 site is worth almost its whole new
output. The notice is about the manufacturer. The ledger's southern rows show seven K-77 projects whose support ended in March 2022. In each,
the manufacturer's O&M invoices stop that month, an independent provider's start the next, and settled energy over the following twelve
months is within 1% of the twelve before. Run back across that date, the ledger says the end of support is a change of supplier. The
no-repower path therefore runs to each project's consent end in the consent register (2038 to 2043 for the K-77s), and Dunmore, a
supported-model site whose consent ends in 2029, becomes the best use of a dollar.

## 4. The ladder

| Rung | Construction (incremental MWh a year per $M) | Names (ranked first) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Fund energy model; no-repower path ends at the support date for K-77 sites, at consent end for the rest; greedy whole-turbine fill | A, Bitter Creek, 2,589 (1.19× Antelope Flats); 1,544 GWh a year, +67.7% | The validated model, the filed notice and the policy's own allocation rule | The wind atlas puts ridge-line shear at 0.05 against the 0.20 behind every validated repower, so ridge energy is 0.62 of the model's figure |
| 1 | Energy recalibrated by terrain class | B, Antelope Flats, 2,182 (1.19× Fox Hollow); 1,342 GWh, +45.7% | The model is now used only where it was validated | The interconnection register caps Antelope Flats' exports at 0.68 of its repowered output |
| 2 | Exports capped at each project's interconnection limit | C, Fox Hollow, 1,829 (1.16× Bitter Creek); 1,170 GWh, +27.0% | Terrain-correct, grid-feasible and filed-notice compliant | The ledger: the southern K-77 fleet's settled energy runs through its March 2022 support end without a step, on a successor provider's invoices |
| 3 | **Decisive:** K-77 no-repower paths run to consent end, so every project's path ends at its own consent | **E, Dunmore, 1,493 (1.24× Hatch Mesa)** (5th of 9 on rung 0) | — | — |

* **The answer.** Dunmore 26 turbines, Hatch Mesa 16 and Elk Run 15 ($719.0M), buying 920.9 GWh a year, committed as 920.
* **Position table.** Dunmore ranks 5th on rung 0, 4th on rung 1 and 3rd on rung 2, and leads only rung 3. It is never 2nd.
* **Discriminator dominance.** Fox Hollow carries a 1.225× lead into rung 3 (1,829 against 1,493). Under continuity it keeps 0.505 of its
  value and Dunmore all of it, an edge of 1.98×, which is 1.35 times the required 1.2 × 1.225 = 1.47.
* **Sign discipline.** Every rung below the answer over-states the capital's yield (+68%, +46%, +27%). The decisive move takes 21% off rung
  2, and the answer is the minimum cell of the grid.
* **Partial correction priced (L3).** Every half-applied path names Fox Hollow first. Replacing the hard stop with a five-year
  post-support decline, the usual rule of thumb, gives Fox Hollow 1,688 against Dunmore's 1,493 (1.13×) and 1,104 GWh (+19.9%). Running
  the K-77s only as far as the evidence runs, the southern provider's current contract to March 2029, gives Fox Hollow 1,716 (1.15×) and
  1,115 GWh (+21.1%). Each lands nearer rung 2 than the answer.
* **Grid.** Terrain (off, on) × interconnection cap (off, on) × no-repower path (support end, consent end) = 8 cells. Every non-answer
  cell names Bitter Creek, Antelope Flats or Fox Hollow. The nearest figure is terrain plus continuity without the export cap: 1,046 GWh
  (+13.6%), led by Antelope Flats. Reaching it means ignoring a filed export limit.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The notice ends support and says nothing about operation. The provider appears only as a vendor name on ledger
   rows, and no document mentions it.
2. **Corpus blind for a computable reason.** *In every one of the five completed repowers the retired turbines were a supported model, so
   the support-end and consent-end paths return identical increments for all five.* The five certify the energy model under both readings
   and cannot score the path.
3. **No arithmetic symptom.** The ledger ties to the settlement statements, and energy, capital and turbine counts reconcile on every
   rung. Ending the K-77s in 2027 breaks no total.
4. **Not a row predicate.** It needs the southern fleet's monthly settled energy aligned across its own support end, the vendor succession
   inside each project's O&M rows, and then each forward project's consent end from a separate register.
5. **The enumeration is arithmetic.** Each project's no-repower path is a built quantity (years to consent end × current settled output).
   No column says "continues".
6. **No cutover date.** The dated notice is the decoy. The decisive fact is that no series steps at the southern date.
7. **Survives deletion.** Removing every voice leaves the notice and the policy pointing at the K-77s.

## 6. The calibration corpus

* **Form.** The fund's portfolio ledger: monthly settled MWh and revenue per project, and O&M payments by vendor, for 31 projects since 2015.
  It includes the five completed repowers before and after, and the seven southern K-77 projects either side of March 2022.
* **What it certifies.** Current settled output per old turbine (the no-repower level) and the energy model on the five flat-site repowers,
  each within 2% of its forecast. A solver who back-tests rungs 0 to 2 is confirmed.
* **What it is blind to.** Terrain (all five repowers are flat) and the no-repower path (above).
* **Twin pair.** Southern K-77 projects Sandy Ford and Tor Hill are identical on model, vintage, capacity, wind class, pre-2022 settled
  energy and support end. Sandy Ford's consent runs to 2036 and it still generates on the provider's support; Tor Hill's consent ended in
  June 2024 and it was decommissioned. Their settled energy since April 2022 differs 2.0× (54 months against 27). The support-end reading
  makes both zero.
* **Resemblance points at the decoy.** Fox Hollow matches the five completed repowers on vintage, wind class and capex per turbine.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The investment policy scores repowering on incremental energy against the project's no-repower path over the new
  turbines' 20-year life, and allocates whole turbines in order of value per dollar until capital runs out. The interconnection register
  holds each project's export limit, and the consent register holds each consent's end date.
* **Empirical pins.** Ridge-site energy is 0.62 of the flat-model figure, from the atlas's terrain shear. Operation continues through
  support end, from the southern ledger rows.
* **Voices.** The origination lead: "The K-77s are finished in 2027; those owners have to repower and we should be first in." The asset
  manager: "Our repower model has hit every forecast we've made." That is true for five flat sites.
* **Licensed wrong basis.** The policy records that the co-investor's technical adviser measures increments against a no-repower path that
  ends at the manufacturer's support date, and will present that basis at the investment committee.

## 8. Determinism by construction

* **Consent ends.** The 20-year life starts at commissioning on 1 April 2026, and every consent ends on 31 March, as the support date
  does, so every path's length in whole years is exact.
* **Continuity window.** Southern settled energy in the 6, 12 and 24 months after March 2022 is within 1% of the same spans before, so the
  window choice cannot reopen the step.
* **Terrain class.** The atlas assigns every site a class, and no candidate sits on a class boundary.
* **Integer fill.** After whole turbines, $1.0M is left, below every project's capex per turbine, so no remainder rule changes the split,
  and 920.9 GWh sits 4.1 from the nearest rounding boundary.
* **Maturity.** Only closed settlement months are used, and the ledger carries no provisional rows for them.

## 9. Prompt sketch and deliverables

> Investment committee meets on the 14th to release $720 million of repowering capital for next build season, and our origination lead is
> sure the K-77 sites have to come first. Tell me how many new turbines each of the nine projects gets and the incremental energy that
> buys, in GWh a year to the nearest 10, in a form I can minute. Send `repower_allocation.xlsx`, a chart `repower_value.png`, and a
> one-page `ic_paper.pdf`.

* `repower_allocation.xlsx`: the nine projects' increments and the fill under the four rung bases, the royalty sheet (ask A) and the
  curtailment sheet (ask B).
* `repower_value.png`: value per $M by project as horizontal bars under the support-end and consent-end paths, the $720M fill drawn as a
  cut line, K-77 projects flagged, and the southern fleet's monthly energy across March 2022 as an inset.
* `ic_paper.pdf`: the committed split, the GWh figure and the K-77 comparison.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the nine projects, landowner royalties per settled MWh in each of the last three
  years. *Device:* royalties are paid quarterly in arrears, and annual true-ups post in the following quarter as separate rows flagged as
  true-ups, per the lease administration guide. Allocating by payment date shifts a quarter of each year into the next and misstates the
  rate at the six projects with true-ups.
* **Ask B (device-carried).** For each project, last year's curtailed energy and curtailment hours. *Device:* the grid operator revises
  instructions by issuing a new row with the same instruction number and a higher revision, and only the latest revision governs. Summing
  every row double-counts 23% of curtailed hours at the four congested projects.
* **Ask C (validity).** The split and GWh figure under each of the four rung bases, and the energy model's reproduction of the five
  completed repowers (5 of 5 within 2%).
* **Decoupling.** Clearing the continuity construction changes no figure in asks A or B.

## 11. Rubric arithmetic

9 projects × 3 years (ask A) + 9 × 2 (ask B) + 4 bases × 2 + 1 reproduction count (ask C) + 9 turbine counts, the GWh figure, the margin and
the K-77 comparison + 5 named chart parts + 3 files ≈ 74 criteria.

## 12. World-building constraints

* Per new turbine (flat-model MWh a year, capex $M): Bitter Creek 25,500 / 9.6 (ridge), Antelope Flats 23,500 / 10.5 (export share 0.68),
  Fox Hollow 21,500 / 11.4, Coyote Draw 19,800 / 13.4 (the four K-77 sites), Dunmore 20,800 / 13.0, Elk Run 23,000 / 11.0 (ridge), Grange
  Hill 19,300 / 12.8 (export share 0.90), Hatch Mesa 18,900 / 13.5, Iron Gap 20,000 / 10.8 (ridge). Three old turbines retire per new one.
* No-repower path lengths under consent end, as shares of 20 years: Bitter Creek and Antelope Flats 0.60, Fox Hollow 0.85, Coyote Draw
  0.65, Dunmore 0.15, Elk Run 0.35, Grange Hill 0.50, Hatch Mesa 0.30, Iron Gap 0.40. Under the support-end reading the K-77s run 0.05.
* Rung figures are 1,544 / 1,342 / 1,170 / 921 GWh a year, and no other cell of the 8-cell grid is within 12% of the answer.
* Seven southern K-77 projects end support in March 2022, with provider invoices from April 2022 and no step in settled energy. Sandy Ford
  and Tor Hill are identical on every asset-register column.
* Royalty true-ups and curtailment revisions never touch settled energy, capex or the consent register.
