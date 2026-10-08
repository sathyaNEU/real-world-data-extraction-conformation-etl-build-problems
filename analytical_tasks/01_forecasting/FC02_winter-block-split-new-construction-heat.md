# FC02 — How to split a capped winter firm-capacity block across four zone books, when this winter's new customers heat differently

| Field | Value |
|---|---|
| Objective | Forecasting & Predictive Modelling |
| Domain | Economics · retail electricity and energy risk |
| Mirrors | Splitting a capped capacity pool across regions when next season's growth is a different kind of user from the users the per-user rate was fitted on (cloud region capacity when a GPU-heavy tenant class arrives, edge and CDN capacity for a new device cohort, fulfilment capacity at Amazon for a new seller cohort) |
| Decision shape | An allocation under a cap: 400 MW of winter firm capacity placed in 5 MW lots across four zone books |
| Committed call | The four zone allocations (Coast, North Central, South Central, Far West), adding to 400 MW, for the December–February book |
| Gap · Pattern | Gap 2 (population) over Gap 1 (time) · S8, the pooled per-customer rate is correct and applies to nobody in the new book, with finer controls separating the replay constructions |
| Gate G mechanism | forecasting, with binding_constraint support |
| Measured traps engaged | #13 validates on one population, applies to another · #12 stops at the first control that passes · #4 never tests its reading against the control |
| Calibration form | Existing-book actuals: ten closed winters of the book's settled hourly load by zone, premise-level interval data for existing premises, and last year's risk report with its replay table |
| Driving force | The book's per-customer winter peak rate reproduces all forty closed zone-winters, because the book's heating mix never moved. This winter's growth in South Central is builder-programme premises, 80% all-electric against the book's 21%, and an all-electric home's 1-in-10 winter peak is 3.6× a gas-heated one's. No customer column says how a new premise heats; that comes from the distribution utility's new-construction report, by ZIP. |

## 1. Situation

A retail electricity provider serves homes and small businesses in four weather zones. Its risk committee has capped winter firm
capacity (call options for December–February) at 400 MW. The risk policy places the block in 5 MW lots, each on the zone book with the
largest remaining uncovered 1-in-10 winter exposure, which is the book's load at the 1-in-10 winter peak less its existing hedges. This
spring the company signed exclusive enrolment deals with three home builders in South Central.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: the settled book load, the premise interval data, the enrolment file, the hedge book, the
  distribution utility's reports and last year's risk report. No one's claim about their own numbers is overturned. The difficulty is that
  the customers being forecast are not the customers the rate was fitted on.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the trading head's view and the zone tool. The book's own per-customer replay still reproduces 40 of 40
  closed zone-winters and still carries the pooled rate onto the new premises.
* **Instrument repair.** Give every premise perfect interval data for ten winters. The new premises were built this year and have no
  winter at all, so no instrument of the past observes their winter peak.
* **Lens swap.** The naive read and the answer are different populations: the book that lived through the closed winters against the
  coming winter's book, 38% of whose South Central premises did not exist a year ago.

## 3. The driving force

A strong solver rejects the raw maxima, builds a per-customer replay that ties last year's report to the megawatt, de-duplicates the
enrolment file and multiplies by the coming book. Every step is right for the book that produced the history. The pooled rate is a
mixture: in South Central 21% of existing premises are all-electric, and at the 1-in-10 cold-morning peak they draw 7.6 kW against 2.1
kW for gas-heated homes. The mixture held still for ten winters because the company never enrolled new construction, so the pooled rate
and the subgroup rates reproduce the corpus equally well. The 46,300 builder-programme premises are 80% all-electric. Their heating type is
on no enrolment row. It comes from the distribution utility's new-construction report by ZIP, and the subgroup rates come from joining the
existing premises to that utility's premise file.

## 4. The ladder

| Rung | Construction | Lands on (Coast · NC · SC · FW, MW) | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | The policy's words on the book's own settled data: P90 of each zone book's ten winter maxima, less hedges, levelled | 160 · 200 · **10** · 30 | It applies the 1-in-10 definition literally, and the most recent winter matches last year's report exactly | Last year's replay table: 36 earlier-winter cells at last year's book that raw maxima of a smaller book cannot reproduce |
| 1 | **E16 (finer controls):** per-customer replay of ten winters' maxima at the coming enrolled book, pooled rate per zone | 95 · 160 · **145** · 0 | It reproduces all 40 cells of the replay table to the MW, not just the salient recent winter | The enrolment file's ESI IDs: 9,200 South Central rows resubmit a premise already enrolled, and the resubmission supersedes |
| 2 | Hygiene: the same replay on the de-duplicated book, which now ties to the distribution utility's switch confirmations | 105 · 170 · **125** · 0 | Clean counts, a validated model, every reconciliation passing | The new-construction report: 80% of South Central's new premises are all-electric, against 21% of the book |
| 3 | **Decisive:** subgroup replay: existing premises at their own heating subgroup's rates, new premises at their ZIP's all-electric share, then levelled | **55 · 120 · 225 · 0** | — | — |

* **Figure shape.** South Central's block is graded with the other three. The answer is the grid's extreme cell (the largest South Central
  block), so every partial application under-places it: −96%, −36% and −44% at rungs 0–2.
* **Discriminator dominance.** At rung 2 North Central's uncovered exposure leads South Central's by 1.16× (320 against 275 MW). The new
  premises' subgroup rate is 1.99× the pooled rate on 38% of South Central's book, which lifts its exposure 1.55× (425 against 275). 1.55
  exceeds 1.2 × 1.16 = 1.39, so the last rung moves the largest block.
* **Partial correction priced (L3).** A solver who sees that new homes differ but gives every new premise the all-electric rate places
  260 MW in South Central (+16%). One who gives new premises the existing book's 21% all-electric share places 140 MW (−38%), further away
  than rung 1.
* **Grid.** Maxima basis (raw, per-customer) × counts (enrolled, de-duplicated) × new-premise rate (pooled, ZIP-calibrated subgroup, all
  all-electric) gives 7 distinct cells: 10, 145, 270, 305, 125, 225 and 260 MW for South Central. The nearest wrong cells are
  all-electric everywhere (+16%) and the subgroup replay without de-duplication (+20%); each needs one omission.

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The policy defines exposure and the lot rule. No document says new premises heat differently or that the
   per-customer rate depends on heating.
2. **Corpus blind for a computable reason.** *In every closed winter each zone book's new-construction share was under 2%, because the
   company first enrolled through builders this spring.* The pooled and subgroup replays both reproduce 40 of 40 zone-winters within 0.5%.
3. **No arithmetic symptom.** De-duplicated counts tie to switch confirmations, replayed maxima tie to settlement, and the lots sum to 400
   under every rung.
4. **Not a row predicate.** New premises carry no heating field. Their mix comes from a ZIP-level report, and the rates from existing
   premises joined to a different file's heating attribute, recombined at each zone's coming mix.
5. **The enumeration is arithmetic.** The subgroup exposure is a weighted sum of fitted per-premise rates over ten replayed winters. No
   column holds it.
6. **No cutover date.** The builder deals stepped no closed series; the new premises have no winter yet.
7. **Survives deletion.** No wrong number exists to delete. Without the voices and the zone tool, rung 1 is the natural start.

## 6. The calibration corpus

* **Form.** Ten closed winters of the book's settled hourly load by zone, premise-level interval data for existing premises, and last
  year's risk report with its 40-cell replay table (each zone's ten winters replayed at last year's book).
* **What it certifies.** The per-customer replay: 40 of 40 replay-table cells to the MW. Raw maxima reproduce only the 4 most-recent-winter
  cells, the salient control that every construction passes.
* **What it is blind to.** The heating mix of premises that have never seen a winter (above).
* **Twin pair.** ZIP clusters SC-07 and SC-12 are identical on every customer-file column: 2,140 premises each, annual usage, summer peak
  per premise, plan mix and premise age band. Their closed 1-in-10 winter peaks per premise are 6.17 and 2.59 kW (2.4×), because 74% of
  SC-07's premises are all-electric against 9% of SC-12's. The heating field lives in the distribution utility's premise file. The pooled
  zone rate gives the twins one figure, and only the subgroup rates reproduce both.
* **Resemblance points at the decoy.** The builder enrolments resemble the existing South Central book on every enrolment column (the
  builder's usage estimate, plan mix, deposit class), which is the book the pooled rate fits.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The committee minute: the winter block is 400 MW. The risk policy: winter exposure is the coming winter's book load at
  the 1-in-10 winter peak (the 90th percentile across the ten most recent winters' weather, inclusive interpolation), less hedges, and lots
  of 5 MW go one at a time to the largest remaining exposure. The enrolment dictionary: a resubmission carries the original ESI ID and
  supersedes it.
* **Empirical pins.** Subgroup rates per zone, from existing premises' interval data joined to the premise file. New-premise heating
  shares, from the new-construction report by ZIP.
* **Voices.** The load-planning lead: "A new customer in a zone is just another customer in that zone." The head of trading: "Coast has
  always been where our winter risk sits."
* **Licensed wrong basis.** The risk policy records that the company's lenders review winter exposure on the zone-share basis (the book's
  energy share of each weather zone's published 1-in-10 peak) and will see it in the covenant pack.

## 8. Determinism by construction

* **Winter and clock.** December–February in Central Prevailing Time, hour-ending, as the policy states. No winter maximum falls on a
  daylight-saving day.
* **Subgroup coincidence.** In every closed winter both heating subgroups peak in the zone book's maximum hour (a cold morning), so
  coincident and non-coincident subgroup rates agree.
* **Coverage.** Every new premise's ZIP appears in the new-construction report, and every existing premise has a heating attribute.
* **Levelling.** The answer's remaining exposures level at exactly 200 MW, so lot-by-lot placement and the continuous water level give
  the same split, and the tie-break order is never used.
* **Maturity.** Every closed winter is settled at true-up before the extract. The coming book is the enrolled book at the extract date,
  and switch confirmations close the count.

## 9. Prompt sketch and deliverables

> The risk committee capped winter firm capacity at 400 MW, and on Friday I have to tell it how the 5 MW lots split across our four zone
> books, as four numbers that add to 400. Our head of trading is convinced Coast is still where our winter risk sits. Send me
> `winter_block_split.xlsx`, a chart `winter_levelling.png`, and a two-page `committee_paper.pdf` with the split I should defend.

* `winter_block_split.xlsx` — the exposure build and split, the churn sheet (ask A) and the plan sheet (ask B).
* `winter_levelling.png` — the four zones' uncovered exposures as paired bars (pooled and subgroup), the water level as a labelled line,
  each zone's allocated lots shaded, and South Central's new-construction premises annotated.
* `committee_paper.pdf` — the committed split, the water level and the bases the lenders and the trading desk will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each zone, customers lost to switching in each of the last four quarters and the quarterly
  churn rate. *Device:* a customer who moves house posts as a drop and an add sharing a transfer reference, as the enrolment dictionary
  documents. Counting those drops as churn overstates Coast and North Central churn by about a third. Transfers net to zero in the counts.
* **Ask B (device-carried).** For each zone, the share of customers on time-of-use plans at the end of last winter and their share of the
  zone's winter energy. *Device:* a mid-month plan change splits that customer-month into two rows with a proration factor, as the billing
  dictionary documents. Counting rows as customers inflates the time-of-use share by 6–9 points in two zones, and unweighted energy
  double-counts the switch month.
* **Ask C (validity).** Each zone's uncovered exposure and allocated block under each of the four rung constructions, with each
  construction's hits on the 40-cell replay table.
* **Decoupling.** Replacing the subgroup rates with the pooled rate changes no figure in asks A or B.

## 11. Rubric arithmetic

4 zones × 4 quarters × 2 (ask A) + 4 zones × 2 (ask B) + 4 zones × 4 constructions + 4 hit counts (ask C) + the four committed blocks,
the water level and South Central's exposure + 5 named chart parts + 3 files ≈ 74 criteria.

## 12. World-building constraints

* Hedges: Coast 250, North Central 300, South Central 120, Far West 40 MW. Answer exposures 255 / 320 / 425 / 120 MW, levelling at 200.
* South Central: 74,865 existing premises (21% all-electric) and 46,300 de-duplicated new premises (80% all-electric). At the 1-in-10
  peak an all-electric premise draws 7.6 kW and a gas-heated one 2.1 kW. 9,200 raw enrolment rows are resubmissions.
* South Central's block is 10 / 145 / 125 / 225 MW across the rungs; the nearest wrong cells are 260 and 270 MW.
* In every closed winter each book's new-construction share is under 2%. SC-07 and SC-12 are identical on every customer-file column.
* Transfers and plan-change prorations never touch premise interval data, heating attributes or hedge positions.
