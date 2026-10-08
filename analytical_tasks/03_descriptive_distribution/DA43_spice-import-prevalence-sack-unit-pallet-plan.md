# DA43 — The Salmonella prevalence a spice importer files for its largest supplier, when a large sack is sampled twice

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · food import quality assurance |
| Mirrors | Counting defective units when inspection samples are drawn per position rather than per unit (multi-pack items sampled per pick face, pallets inspected per layer, parcels scanned per label), as retail and marketplace supply chains do for food and consumer safety |
| Decision shape | One figure committed at a date: the quarterly prevalence filed with the regulator's import review on 15 July |
| Committed call | Hesperia Spices' Salmonella prevalence for the quarter, per 10,000 sacks, to one decimal |
| Gap · Pattern | Gap 2 (population) over Gap 4 (rule) · finer controls separate constructions (measured #12), the sack built from sub-samples through the pallet plan, with a latent attribution marker at rung 1 (measured #17) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #12 stops at the first control that passes · #17 guesses an attribution the data can settle · #2 counts file rows instead of the real unit |
| Calibration form | Counterparty acknowledgement file: the laboratory's acknowledgement of every composite and every sub-sample re-test, with its acknowledged prevalence for each lot and its positive-sack count for each of four closed quarters |
| Driving force | The laboratory's quarterly composite positivity, the salient control, is returned by every construction. Its acknowledged lot prevalences, the finer controls, count positive sacks, and a 50 kg sack is sampled top and bottom into two sub-samples, joined to one sack only through the sampling points and the warehouse's pallet plan. Hesperia ships mostly 50 kg sacks, often contaminated in both halves, so positive sub-samples counted against sacks file its prevalence 14% high. |

## 1. Situation

A spice importer files a quarterly Salmonella prevalence for each supplier with the regulator's import review, and Hesperia Spices, its
largest supplier, is under review. Lots are sampled at every point of a pallet plan and the sub-samples are pooled into composites of 30.
The laboratory tests composites, re-tests every positive composite sub-sample by sub-sample, and acknowledges everything to the importer.
The pack holds the importer's sampling log, the warehouse's pallet plans, the laboratory's acknowledgement file and methods sheet, the
regulator's filing rule, and four closed quarters of acknowledged lot prevalences.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each sampling record, each composite and re-test, each closed-quarter prevalence. Nobody files a
  wrong figure and nothing reported is overturned. The difficulty is what one sack is in a log of sub-samples.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the association's figure and both voices. Positive sub-samples from the re-tests, counted per sack sampled,
  still file 21.5 and return the quarter's positivity.
* **Instrument repair.** Suspect: the sampling log's composite records, 18% of them without a lot number. Repaired with every lot number
  filled, rung 0 returns rung 1's 10.0 and rung 2 stays 21.5. Every positive composite was re-tested and each result records what it
  claims; a sack is a unit built from its sub-samples through the sampling points and the pallet plan, which no row claims to record. The
  answer stays 18.9 and the sack construction is still needed.
* **Lens swap.** The naive figure counts positive sub-samples; the answer counts positive sacks, a different population in which two
  sub-samples can be one sack.

## 3. The driving force

A strong solver knows positive composites understate when a composite holds several positives. It assigns the composites that arrived
without lot numbers using the courier-batch sequence, reads every positive composite's re-tests, and counts 73 positive sub-samples: 21.5
per 10,000 sacks, and the quarterly positivity ties. The laboratory's acknowledged lot prevalences for the closed quarters disagree with
that count in 51 of 60 lots, always lower, and only in lots with 50 kg sacks. The pallet plan explains it. A 50 kg sack spans two
sampling points, top and bottom, so it gives two sub-samples, often to different composites. Hesperia ships mostly 50 kg sacks, and nine
of its positive sacks were positive top and bottom. Counted as sacks through the sampling points and the pallet plan, its prevalence is
18.9.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Positive composites per sack sampled, composites without lot numbers dropped | 8.3, −56% | The industry's minimum prevalence, as filed for years | The sampling log: each courier batch lists its lots' composite counts in sequence, which places every unnumbered composite |
| 1 | The same, with unnumbered composites assigned by batch sequence | 10.0, −47% | Every composite attributed, exactly | The acknowledgement file: 41% of positive composites held more than one positive sub-sample on re-test |
| 2 | Positive sub-samples from the re-tests, per sack sampled (the filing's unit) | 21.5, +14% | Every positive counted exactly, and the quarterly positivity ties | The acknowledged lot prevalences: this count returns 9 of 60 closed lots, every miss high, all in lots with 50 kg sacks |
| 3 | **Decisive:** positive sacks per sack sampled, each sub-sample joined to its sack through its sampling point and the pallet plan | **18.9** | — | — |

* **Figure shape.** Rungs 0 to 2 walk the figure up, past the answer, and the decisive rung reverses them: a solver who stops at rung 2
  files 14% high.
* **Partial correction priced (L3).** A solver who pairs adjacent sampling points into sacks without the pallet plan joins neighbouring
  25 kg sacks and lands at 16.8 (−11%). One who counts positive sacks but divides by sub-samples lands at 11.8 (−38%). One who builds
  sacks but drops the unnumbered composites lands at 15.8 (−16%).
* **Grid.** Attribution (dropped or sequence) × numerator (composites, sub-samples, sacks by adjacent points, sacks by pallet plan) ×
  denominator (sacks or sub-samples) = 16 cells. The nearest wrong cell is adjacent-point pairing, 16.8 (−11%); sub-sample prevalence
  lands at 13.5 (−29%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The filing rule says "per 10,000 sacks, by the laboratory's accredited method". The sampling plan says a
   sub-sample is drawn at every point of the pallet plan. No document says a 50 kg sack spans two points or that the laboratory counts
   sacks.
2. **Pattern B, finer controls only one construction returns.** Positive sacks per sack returns all 60 acknowledged lot prevalences and
   all four quarterly positive-sack counts. Adjacent-point pairing returns 41 lots, positive sub-samples per sack 9, sub-sample prevalence 6
   and composite counts none, and each rival misses the quarterly counts too. The construction is a two-hop join, sub-sample to sampling
   point to sack, and a distinct count, not a menu of estimators.
3. **No arithmetic symptom.** Composites reconcile to the sampling log, re-tests to composites, and every construction returns the salient
   quarterly positivity.
4. **Not a row predicate.** A sack's status is the union of its sub-samples' results across composites, reached through the pallet plan.
5. **The enumeration is arithmetic.** No column gives a sack's status or the open quarter's prevalence.
6. **No cutover date.** The sampling plan and the pallet layouts are the same in every quarter, and nothing steps.
7. **Survives deletion.** With every voice removed, positive sub-samples per sack still file 21.5.

## 6. The calibration corpus

* **Form.** The acknowledgement file: every composite over four closed quarters and the open one, with lot (where recorded), result and
  each positive composite's sub-sample re-tests, plus the laboratory's acknowledged prevalence for each of 60 closed lots and its
  positive-sack count for each closed quarter.
* **What it certifies.** The quarterly composite positivity, which every construction returns.
* **What pins the construction.** The 60 lot prevalences and the four quarterly counts, returned only by positive sacks per sack.
* **Twin pair.** Lots H-0412 and H-0588 match on sacks, composites (12), positive composites (4), positive sub-samples (8) and sack sizes.
  Their acknowledged prevalences are 21.4 and 10.7 (2.0×): H-0412's eight positives sit in eight sacks, and H-0588's in four 50 kg sacks
  positive top and bottom.
* **Resemblance points at the decoy.** On composite counts and positivity, Hesperia resembles the suppliers whose filings sit near 21.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's rule: the importer files each supplier's quarterly prevalence per 10,000 sacks, by the laboratory's
  accredited method, with every composite from the supplier's lots counted. The sampling plan: a sub-sample at every point of the pallet
  plan.
* **Empirical pins.** The sack unit, from the acknowledged prevalences; the attribution, from the batch sequence.
* **Voices.** The QA manager: "Positive composites over sacks is what we have always filed." The supplier liaison: "Composites without lot
  numbers aren't Hesperia's to answer for."
* **Licensed wrong basis.** The rule records that the importers' association reports minimum prevalence and will present it at the review.

## 8. Determinism by construction

* **Assignment.** Every courier batch's composite sequence matches its lots' logged counts exactly, so each unnumbered composite has one
  lot.
* **Sacks.** Every sampling point maps to one sack in the pallet plan; a 50 kg sack spans exactly two points and a 25 kg sack one.
* **Re-tests.** Every positive composite was re-tested sub-sample by sub-sample, and every re-test found at least one positive.
* **Rounding.** The answer is 18.88, mid-bin at 18.9.

## 9. Prompt sketch and deliverables

> Hesperia's quarterly prevalence goes to the import review on 15 July, and our QA manager would file it the way we always have. Give me
> the figure per 10,000 sacks to one decimal, as the sentence we file, with `hesperia_prevalence.xlsx`, a chart `sack_count_check.png`,
> and a one-page `filing_note.pdf`.

* `hesperia_prevalence.xlsx` — the figure for the open quarter, the moisture sheet (ask A), the release sheet (ask B) and the closed-lot
  table (ask C).
* `sack_count_check.png` — acknowledged against computed prevalence for the 60 closed lots under four constructions as panels, with the
  identity line, each panel's match count, lots with 50 kg sacks coloured, and the twin lots labelled.
* `filing_note.pdf` — the committed figure and the counts a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 suppliers, the share of lots arriving above 11% moisture. *Device:* two meter
  models are in use, and the meter register gives model B a 0.4-point offset; ignoring it misclassifies lots for five suppliers.
* **Ask B (device-carried).** For each supplier, the median days from arrival to customs release. *Device:* lots held for re-testing carry
  a second release record, and the customs note makes the later one final; taking the first understates three suppliers.
* **Ask C (validity).** The open-quarter figure under each of the four rungs, and closed lots returned by each of six constructions.
* **Decoupling.** Clearing the sack construction changes no figure in asks A or B.

## 11. Rubric arithmetic

14 suppliers (ask A) + 14 suppliers (ask B) + 4 rung figures and 6 construction match counts (ask C) + the committed figure, the positive
sacks and the positive sub-samples + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Hesperia's open quarter: 33,900 sacks (13,560 of 25 kg, 20,340 of 50 kg), 54,240 sub-samples in 1,808 composites, 18% without lot
  numbers; 34 positive composites, 73 positive sub-samples, 64 positive sacks (nine 50 kg sacks positive top and bottom).
* Rung figures 8.3 / 10.0 / 21.5 / 18.9; other cells 16.8, 15.8, 13.5 and 11.8.
* Closed lots returned: sacks by pallet plan 60, adjacent-point pairing 41, sub-samples per sack 9, sub-sample prevalence 6, composite
  counts 0. H-0412 and H-0588 match on every composite column.
* Meter offsets and release records never touch a composite, a sub-sample or a sack.
