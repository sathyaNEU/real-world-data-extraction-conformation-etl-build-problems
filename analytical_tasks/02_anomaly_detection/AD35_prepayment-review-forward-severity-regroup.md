# AD35 — Which hospital and DRG family gets next year's prepayment review team, when the biggest excess is one the coming grouper will remove by itself

| Field | Value |
|---|---|
| Objective | Anomaly Detection & Diagnostics |
| Domain | Policy & Education · public insurance claims review |
| Mirrors | Sending reviewers where an anomaly will keep costing money rather than where it cost most last year (ads-integrity enforcement at Meta and Google after a policy change already neutralises one abuse pattern, seller fee-abuse reviews at Amazon after a fee-schedule change, cloud billing-anomaly teams after a pricing change) |
| Decision shape | Which of N gets one scarce thing: the contractor's single prepayment medical review team goes to one of six flagged hospital × DRG-family cells for the coming fiscal year |
| Committed call | The cell placed under 100% prepayment review from 1 October, and the improper payment the review is expected to deny over the following twelve months |
| Gap · Pattern | Gap 1 (time: last year's excess against next year's yield) over Gap 3 (objective) · Pattern A (past exceedance against forward yield) with the moderator in how the coming year's severity table treats a code, and a quiet add-on-payment contamination below it |
| Gate G mechanism | forecasting, with decomposition_attribution support |
| Measured traps engaged | #11 beats the headline trap, misses the quiet one · #13 validates on one population, applies to another · #7 uses the ready-made measure |
| Calibration form | Prior-period close-out: the close-out summaries of nine prepayment reviews (FY2021–FY2025), each with the selected cell, its selection-year excess and the improper payment denied over its review year |
| Driving force | Every candidate's excess is measured correctly. Most of C's is cases grouped to the "with MCC" DRG on the strength of a single secondary diagnosis that the FY2027 severity table demotes to a CC, so from 1 October those cases pay at the CC rate whatever C codes, and a review there has little left to deny. Only regrouping each candidate's claims under next year's table, a join from every claim's secondary diagnoses to each code's next-year severity, separates excess that persists (E's, built on MCCs that stay MCCs) from excess the calendar removes. |

## 1. Situation

A regional claims contractor for the public insurer has one prepayment medical review team for FY2027 (1 October to 30 September). The team
reviews every claim in one hospital × DRG-family cell before payment and denies what the record does not support. The review charter sends
the team where it will deny the most improper payment over the twelve months after selection, on the selection year's volume. The
contractor's two-way model of FY2026 payments flagged six cells. It holds the FY2026 claims with secondary diagnoses and add-on payments,
the hospital summaries, the published FY2027 final rule with its severity tables, and the close-out summaries of past reviews. The medical
director thinks academic centres overbill everywhere.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the payments, the two-way residuals, the add-on payments, the close-out denials and the final rule's
  tables. The medical director is right that A's payments are high. Nothing is overturned; the difficulty is which excess will still be
  there to deny next year.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the director's view and the old z-score list. A two-way model net of add-ons, the build every close-out
  confirms, still names C.
* **Instrument repair.** Make every claim and every residual exact. C's FY2026 excess stays real; what changes it is how FY2027 groups the
  same coding, which no better record of FY2026 contains.
* **Lens swap.** The naive basis is FY2026 claims as they grouped then; the answer is the same coding as FY2027 will group it, a different
  population of payments at a different moment.

## 3. The driving force

A strong solver discards the within-DRG z-score (A is expensive everywhere), fits the two-way log model, strips add-on payments that the
review manual puts outside review scope, and confirms on nine close-outs that the add-on-net excess predicted every review's denials within
10%. Every step is correct, and every step assumes next year pays like last year. C's excess sits almost entirely on heart-failure cases
whose only MCC is a malnutrition code. The FY2027 final rule's severity table lists that code as a CC from 1 October, so the same cases
group to the CC DRG and pay about $6,100 less each, which removes 84% of C's excess before anyone reviews a chart. E's excess sits on
respiratory-failure coding, which stays an MCC. Seeing it means regrouping each candidate's FY2026 claims under the FY2027 table, a join
from every secondary diagnosis to its next-year severity, and recomputing the excess that survives.

## 4. The ladder

| Rung | Construction | Names | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Within-family z-score of average payment × volume ($k excess): A 2,400, B 1,950, C 1,700, D 1,400, E 1,250, F 1,100 | A | The contractor's old list and the medical director's instinct | The hospital summary: A's payments are 1.6× the national level in every family it bills |
| 1 | Two-way log-additive residual (hospital and family effects) × volume: B 1,880, C 1,520, D 1,200, E 1,100, F 1,050, A 600 | B | The standard way to remove each hospital's level | The claim detail's add-on field: 72% of B's excess is new-technology add-on payment, outside review scope |
| 2 | Two-way residual on payments net of add-ons: C 1,450, E 1,060, D 900, F 900, A 560, B 520 | C | Reproduces all nine close-outs' denials within 10% | The FY2027 severity table: C's excess rests on a code that groups as a CC from 1 October |
| 3 | **Decisive:** regroup each cell's FY2026 claims under the FY2027 table and recompute the add-on-net excess that survives: E 980, D 690, A 400, F 330, B 300, C 230 | **E** (5th of 6 on rung 0) | — | — |

* **Position table.** E ranks 5th on rung 0, 4th on rung 1 and 2nd on rung 2 (C leads it by 1.37×), and leads only rung 3. Rung leaders beat
  their runners-up by 1.23×, 1.24×, 1.37× and 1.42×.
* **Discriminator dominance.** C carries a 1.37× excess advantage into rung 3. E's edge on the decisive axis is the share of excess that
  survives the regrouping, 0.92 against 0.16 (5.75×), 3.5× the required 1.2 × 1.37 = 1.64×, so the net is 5.75 / 1.37 = 4.2×.
* **Partial correction priced (L3).** A solver who notices the final rule but discounts every candidate by the family's average share of
  malnutrition-only cases, instead of regrouping each cell's own claims, cuts C to 730 and E to 690 but barely touches the sepsis family,
  where D and F sit level at 860, 1.18× C: a tie between two wrong cells, with E fourth. A solver who regroups but keeps add-on payments
  names B, 1,800 against E's 1,020 (1.76×).
* **Grid.** Level removal (z-score or two-way) × add-ons (kept or stripped) × grouping (FY2026 or FY2027) = 8 cells: A, A, B, C under
  FY2026 grouping and A, A, B, E under FY2027, so only two-way, add-on-net and regrouped names E.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The final rule lists severity changes as a table of codes for grouping purposes. No document connects any change to
   review targeting or to a candidate cell.
2. **Corpus blind for a computable reason.** *In every closed review, no code carrying the selected cell's excess changed severity during
   the review year, because the malnutrition code was an MCC throughout FY2021–FY2026 and no other severity change touched a selected
   cell.* The close-outs certify rung 2 to within 10% on all nine and cannot see a period that groups the same coding differently.
3. **No arithmetic symptom.** Claims tie to the hospital summaries, residuals sum to zero within each hospital and family, and add-on
   payments tie to the payment detail.
4. **Not a row predicate.** It needs every claim's secondary diagnoses joined to next year's severity table, the claim's tier recomputed
   from its most severe surviving code, repricing at the new DRG's weight, and the two-way excess recomputed per cell.
5. **The enumeration is arithmetic.** Which claims move tier is computed from codes; no column flags them.
6. **No cutover date in the data.** The reclassification takes effect after the window closes, so no FY2026 series steps; the moderator
   lives only in the forward year.
7. **Survives deletion.** Remove both voices and the old list: the add-on-net two-way model is still the natural build.

## 6. The calibration corpus

* **Form.** Close-out summaries of nine prepayment reviews (FY2021–FY2025): the selected cell, its selection-year excess on each basis, and
  the improper payment denied over its review year.
* **What it certifies.** Add-on-net excess predicts denials within 10% in all nine; the raw two-way residual misses the three cells with
  add-on payments by 35% or more and the z-score misses six of nine, all overstating, so neither reconciles on the total.
* **What it is blind to.** Severity reclassification (above).
* **Twin pair.** D and F are identical on every rung 2 column: add-on-net excess ($900k each), volume, family, MCC rate and hospital type. D's
  excess rests on respiratory-failure coding and F's on the malnutrition code, so their forward yields are $690k and $330k, 2.1× apart,
  separated only by the regrouping.
* **Resemblance points at the decoy.** By hospital type, family and excess, C most resembles the two closed reviews with the largest denials.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The review charter: the team goes where it will deny the most improper payment over the twelve months after selection, on
  the selection year's volume. The review manual: new-technology add-on payments are lawful and outside review scope. The FY2027 final
  rule, shipped as published. One sentence each.
* **Empirical pins.** Denials track add-on-net excess, from the close-outs; each claim's FY2027 tier, from the severity table.
* **Voices.** The medical director: "Academic centres overbill in everything they do; start with A." The analytics lead: "The two-way residual
  is the national standard; trust it."
* **Licensed wrong basis.** The charter records that the program-integrity oversight contractor ranks cells on the two-way residual and will
  present its list at the selection meeting.

## 8. Determinism by construction

* **Tier assignment.** A claim's FY2027 tier is set by its most severe secondary diagnosis under the new table; claims with the malnutrition
  code and another MCC stay in the MCC tier, so no grouper edge case decides a candidate.
* **Volume.** The charter values the review on the selection year's volume, so no forecast of FY2027 admissions is needed.
* **Model fit.** Weighted and unweighted two-way fits, and alternating means or least squares, give the same residual ranking at every rung.
* **Rounding.** The committed denial figure is given to the nearest $10,000; E's $980k sits mid-bin.

## 9. Prompt sketch and deliverables

> From 1 October our one prepayment review team can sit on a single hospital and DRG family for a year, and six cells came up in the
> model. Our medical director wants the academic centres. Tell me which cell gets the team and how much improper payment it should deny over
> the year, to the nearest $10,000, in a line for the selection meeting. Send `review_case.xlsx`, a chart `excess_survival.png`, and a
> one-page `selection_memo.pdf`.

* `review_case.xlsx` — the six cells under each rung's basis (ask C), the cost-ratio sheet (ask A) and the payer-mix sheet (ask B).
* `excess_survival.png` — for each cell, FY2026 add-on-net excess as a bar with the part surviving FY2027 grouping overlaid, the survival share
  labelled on each bar, the selected cell highlighted and the denial figure in the title.
* `selection_memo.pdf` — the committed cell, its expected denials and why each other cell falls away.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each candidate hospital, the operating cost-to-charge ratio in effect on 1 October 2025, 1
  April 2026 and 1 October 2026. *Device:* the provider-specific file keeps a record per change with an effective date, and a correction
  can carry the same effective date with a later file date; the file guide says the latest file date wins. Reading the first record misstates
  four of the eighteen values. The review build never uses cost-to-charge ratios.
* **Ask B (device-carried).** For each candidate hospital, its FY2026 share of inpatient days covered by private-plan enrolees, from the cost
  reports. *Device:* cost reports run on each hospital's own fiscal year, recorded in the report index, and the federal year needs proration
  across two reports for four hospitals; reading the latest report alone misstates them.
* **Ask C (validity).** Each cell's figure under each of the four rung bases.
* **Decoupling.** Clearing the regrouping and the add-on stripping changes no figure in asks A or B.

## 11. Rubric arithmetic

6 hospitals × 3 dates (ask A) + 6 × 2 (ask B) + 6 cells × 4 bases (ask C) + the committed cell, its expected denials, the runner-up and the
margin + 5 named chart parts + 3 files ≈ 66 criteria.

## 12. World-building constraints

* Rung figures as in the ladder; E is 5th, 4th, 2nd (1.37× behind C) and 1st.
* C's add-on-net excess: 84% on cases whose only MCC is the malnutrition code. E's: 92% on MCCs unchanged in FY2027. B's raw excess: 72%
  add-on payments.
* The nine close-outs touch no code that changes severity in their review years.
* D and F are identical on every rung 2 column, both in the sepsis family. Family-average malnutrition-only shares: heart failure 0.50,
  respiratory 0.35, sepsis 0.04.
* Cost-to-charge records and cost-report payer mix never touch the claims, the residual model or the severity tables.
