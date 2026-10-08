# DS16 — Which inventories a $16M settlement reserve should clear, when the award model was proven only in the company's home venue

| Field | Value |
|---|---|
| Objective | Opportunity Sizing & Decision Support |
| Domain | Economics · corporate litigation finance |
| Mirrors | Settling liabilities from a capped reserve with a valuation model validated only in the home market (Meta, Google and Amazon legal and regulatory reserves across jurisdictions, marketplace refund and chargeback settlements across regions, cloud contract-dispute reserves) |
| Decision shape | An allocation under a cap: the $16M reserve across six plaintiffs' firms' inventory settlements |
| Committed call | The inventories settled, and the expected saving against litigating them, in $M to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · measured #13's architecture (an award model exact on the closed book, applied to a venue the book never held), with a saturated rating tie (#19) at rung 0 and claimant hygiene at rung 2 |
| Gate G mechanism | decomposition_attribution, with binding_constraint |
| Measured traps engaged | #13 validates on one population, applies to another · #19 breaks a big tie instead of questioning it · #2 counts file rows instead of the real unit · #15 follows the requester's hunch over the rule |
| Calibration form | Existing-book actuals: the company's 96 closed product-liability cases with dispositions, amounts and defence costs |
| Driving force | Outside counsel's award model reproduces all 41 adverse outcomes in the closed book within 5%. Every one of those cases was tried or settled in the company's home venue. Three of the six inventories sit in a second venue, where the state judiciary's verdict report puts product-liability awards at 2.2× the home venue's for every device type. A model that fits everything it can check overstates what settling the home-venue inventories saves relative to the second-venue ones, and the reserve goes to the wrong three. |

## 1. Situation

A medical-device maker's legal department has a $16M settlement reserve this year. Six plaintiffs' firms have offered inventory
settlements, each a fixed price for all of its claimants. The board's policy spends the reserve where expected saving per reserve dollar
is highest. Expected saving is the expected cost of litigating an inventory to the end (adverse dispositions at their expected awards,
plus remaining defence costs) less the settlement price. The department holds counsel's ratings and award model, the reserve methodology,
the claimant register, the closed-case book and the state judiciary's annual verdict report. The litigation chief wants the largest
inventories cleared first.

## 2. Gate G: why this is legal

* **Litmus.** Every reported number is correct and no stakeholder read is overturned. Counsel's ratings, the award model's fit to the book,
  the methodology, the register and the verdict report are all right. The difficulty is that the model's flawless record is a record of
  one venue, and half the decision sits in another.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the litigation chief's preference and counsel's ratings. Expected saving on the methodology's probabilities,
  with claimants counted once, still settles Hale, Ortiz and Liang, and every figure ties to the book.
* **Instrument repair.** Give counsel a perfect record of every closed case. It is still a record of home-venue cases, and the second
  venue's awards still run 2.2× higher.
* **Lens swap.** The naive valuation prices every claimant on the home venue's closed cases. The answer prices second-venue claimants on
  that venue's awards: a different population of outcomes, for cases that have not yet closed.

## 3. The driving force

A strong solver sets aside counsel's ratings, because five of the six inventories sit in the same top band. It values each inventory on the
methodology's probability (the share of closed cases of that device type that ended adversely) and the award model, then counts each
claimant once, because six of Kessler's claimants moved to Duarte's firm and appear in both inventories. Each step is competent. It settles
Hale, Ortiz and Liang for $8.05M of saving. But the award model's record is the closed book, and every closed case was in the company's
home venue. Duarte's, Kessler's and Moss's claimants filed in the second venue, where the judiciary's report shows awards 2.2× the home
venue's for hips, valves and catheters alike. Valued there, Duarte's inventory saves $7.2M and Moss's $5.4M. The reserve should clear Ortiz,
Duarte and Moss, for $15.1M of saving.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Counsel's ratings: five inventories tie at "probable" (#19), broken by the guideline's tie-break (largest inventory first) | Hale, Duarte, Kessler; reserve spent $16.0M | Counsel's own assessment and the department's own tie-break | The policy and the reserve methodology: inventories go on expected saving per dollar, with probability the share of closed cases of the device type that ended adversely |
| 1 | Expected saving per dollar on the methodology's probabilities and counsel's award model | Hale, Ortiz, Kessler; $9.05M (−40%) | A full expected-value case on the company's own record | The claimant register: six of Kessler's nine claimants are also in Duarte's inventory, and a claimant is resolved once |
| 2 | Claimants counted once (hygiene) | Hale, Ortiz, Liang; $8.05M (−47%) | Clean claimant counts, every figure reconciled | The judiciary's verdict report: second-venue awards run 2.2× the home venue's for every device type, and the book holds no second-venue case |
| 3 | **Decisive:** second-venue inventories valued at that venue's awards; reserve re-spent | **Ortiz, Duarte, Moss; $15.1M** | — | — |

* **Figure shape.** The corrections walk the figure down (−11% from rung 1 to rung 2), and the decisive move reverses them (+87%). Rung 0's
  set is worth $11.5M at true values (−23%).
* **Discriminator dominance.** Hale carries a 6.8× saving-per-dollar advantage over Duarte into rung 3 (0.64 against 0.094). Venue
  valuation multiplies Duarte's by 12.0 and leaves Hale's unchanged. Product: 12.0 / 6.8 = 1.76, so Duarte ends ahead (1.12 against 0.64).
* **Partial correction priced (L3).** Valuing the second venue correctly but skipping the claimant register settles Kessler, Duarte and Moss,
  claiming $21.2M (+41%). The inflated Kessler inventory leads at 2.4 per dollar. Using a national venue ratio of 1.5 in place of the
  report's 2.2 settles Hale, Ortiz and Moss for $8.9M (−41%), because Hale stays 1.10× ahead of Moss. Applying the venue valuation to rung
  2's three without re-spending delivers $8.05M (−47%). No half-application settles the answer's three.
* **Grid.** Valuation (ratings, saving) × claimants (raw, once) × venue (home model, national ratio, report ratio) gives 7 feasible cells.
  Only the full cell settles Ortiz, Duarte and Moss. The national ratio without the register settles rung 0's three, and it is the nearest
  wrong figure at $12.4M (−18%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The model's validation note says it reproduces the closed book. No document says the book is one venue, or that the
   model should be re-levelled for the other.
2. **No sweepable corpus nominates it.** *Every closed case in the book was tried or settled in the home venue, because second-venue filings
   are recent and none has closed.* So the award model reproduces all 41 adverse outcomes, and the book cannot show a second-venue award.
3. **No arithmetic symptom.** Claimants, prices and the reserve reconcile, the model ties to every closed amount, and nothing in the open
   docket fails a check.
4. **Not a row predicate.** It needs the venue of each inventory joined to the judiciary's report by device type, an award re-levelled per
   claimant, an inventory sum, and a capped selection.
5. **The enumeration is arithmetic.** No column carries a venue-adjusted award. Each one is built from the report.
6. **No cutover date.** The second venue's award level is a standing difference in a published aggregate, and no outcome series steps.
7. **Survives deletion.** No wrong number exists to delete.

## 6. The calibration corpus

* **Form.** The closed book: 96 cases over nine years, each with device type, disposition (dismissal, defence judgment, settlement or
  verdict), amount and defence costs.
* **What it certifies.** The methodology's probabilities (hips 0.42, valves 0.30, catheters 0.55) and the award model, 41 of 41 adverse
  outcomes within 5%. A solver who back-tests rungs 1 and 2 is confirmed.
* **What it is blind to.** Second-venue awards (above).
* **Twin pair.** The valve and catheter cohorts are identical on every column counsel's rating reads: four tried cases each, all lost, the
  same injury mix and filing years. Their shares of closed cases ending adversely are 0.30 and 0.55 (1.8×). Only the methodology's
  all-dispositions rule separates them, so no rating transfers.
* **Every rule exercised.** One closed case was refiled after dismissal under a new number, which tests the claimant-once rule.
* **Resemblance points at the decoy.** Hale's inventory (hips, home venue, the largest) resembles the book's costliest closed cohort.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The board policy: the reserve settles inventories in order of expected saving per reserve dollar, up to $16M. The reserve
  methodology: a probability is the share of the company's closed cases of the device type that ended adversely. The settlement terms: a
  claimant is resolved once, by whichever inventory settles first. One sentence each.
* **Empirical pins.** Venue award ratios, from the judiciary's report. The probabilities, from the book.
* **Voices.** The litigation chief: "Clear the biggest inventories first; that's where the claims are." Outside counsel: "Our model has
  never missed a closed case by more than five per cent." The general counsel: "Five of these are rated probable; the ratings settle it."
* **Licensed wrong basis.** The policy records that the external auditor reviews the reserve on counsel's ratings and will see that basis.

## 8. Determinism by construction

* **Venue ratios.** The report gives 2.1, 2.2 and 2.3 for the three device types. The pooled 2.2 and the type ratios select the same three
  inventories, and the figure moves by under 2%.
* **Claimants.** The register links each claimant across firms by claimant ID, with no fuzzy matching.
* **Defence costs.** $0.15M per claimant remaining, filed in the methodology, and identical across venues.
* **Selection.** The reserve's best three are the unique optimum by exhaustive check. The next-best feasible set is worth $14.3M.

## 9. Prompt sketch and deliverables

> We have a $16 million settlement reserve this year, and six plaintiffs' firms have offered inventory settlements. Our litigation chief
> wants to clear the biggest inventories first. Tell me which inventories we settle and what we save against litigating them, in millions
> to one decimal, as the line for the audit committee. Send `reserve_plan.xlsx`, a chart `saving_per_dollar.png`, and a one-page
> `committee_note.docx`.

* `reserve_plan.xlsx` — the six inventories under each construction, the docket sheet (ask A), the counsel-spend sheet (ask B) and the book
  sheet (ask C).
* `saving_per_dollar.png` — the six inventories' saving per reserve dollar under the four constructions as a dot plot, the $16M budget line
  on a cumulative-price axis, the settled three highlighted, and the venue of each inventory marked.
* `committee_note.docx` — the three inventories, the saving, and why Hale is not among them.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each inventory, the median days since each claimant's last docket entry. *Device:* a case
  transferred between courts gets a new docket number, with the original in a "transferred from" field. Dating from the new docket alone
  understates two inventories by four to seven months.
* **Ask B (device-carried).** For each inventory, last year's outside-counsel spend. *Device:* work spanning several inventories is billed
  to an umbrella matter, which the billing guideline allocates by recorded hours. Leaving umbrella invoices unallocated understates three
  inventories by 15–25%.
* **Ask C (validity).** Each device type's adverse share on tried cases and on all dispositions, the book's 41 adverse outcomes against the
  award model (hits), and each inventory's saving per dollar under each rung.
* **Decoupling.** Clearing the venue valuation changes no figure in asks A or B. Docket numbers and invoices never enter a probability, an
  award or a price.

## 11. Rubric arithmetic

6 inventories (ask A) + 6 inventories (ask B) + 3 × 2 shares + 1 hit count + 6 × 4 rung values (ask C) + the three settled inventories,
the saving and Hale's exclusion + 6 named chart parts + 3 files ≈ 52 criteria.

## 12. World-building constraints

* Inventories (claimants, venue, device, price $M): Hale 12, home, hip, 6.0; Ortiz 9, home, valve, 4.8; Kessler 9 (6 shared with Duarte),
  second, catheter, 3.6; Duarte 10, second, catheter, 6.4; Liang 8, home, catheter, 3.9; Moss 6, second, hip, 4.4.
* Awards per adverse claimant (home model, $M): hip 1.6, valve 2.2, catheter 1.0, × 2.2 in the second venue. Probabilities 0.42 / 0.30 /
  0.55. Defence $0.15M per claimant.
* Sets and figures: rung 0 {Hale, Duarte, Kessler}; rung 1 $9.05M; rung 2 $8.05M; answer {Ortiz, Duarte, Moss} $15.06M.
* The book holds no second-venue case. The twin cohorts are identical on every rating input.
* Docket transfers and umbrella invoices never touch claimants, awards or prices.
