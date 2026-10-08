# DA43 — The Salmonella prevalence a spice importer files for its largest supplier, when a positive composite can hide several positive sacks

| Field | Value |
|---|---|
| Objective | Descriptive & Distribution Analysis |
| Domain | Supply Chain & Logistics · food import quality assurance |
| Mirrors | Estimating defect prevalence from pooled tests (composite sampling of inbound lots, pooled lab assays, batch review where a flagged batch may hold several violations), as retail and marketplace supply chains do for food and consumer safety |
| Decision shape | One figure committed at a date: the quarterly prevalence filed with the regulator's import review on 15 July |
| Committed call | Hesperia Spices' Salmonella prevalence for the quarter, per 10,000 sacks, to one decimal |
| Gap · Pattern | Gap 4 (rule) over Gap 2 (population) · finer controls separate constructions (measured #12), with a latent attribution marker at rung 1 (measured #17) |
| Gate G mechanism | method_or_model_selection, with decomposition_attribution support |
| Measured traps engaged | #12 stops at the first control that passes · #17 guesses an attribution the data can settle · #7 uses the ready-made measure |
| Calibration form | Counterparty acknowledgement file: the laboratory's acknowledgement of every composite, with sub-samples received, result, individual re-test counts, and its acknowledged prevalence for each lot of the four closed quarters |
| Driving force | The laboratory's quarterly composite positivity, the salient control, is returned by every estimator. Its acknowledged lot prevalences, the finer controls, are returned only by a likelihood that uses each composite's received sub-samples and the individual re-test counts for re-tested composites. Those re-tests show Hesperia's positive composites holding two or three positive sacks, which no composite-level estimator can see. |

## 1. Situation

A spice importer files a quarterly Salmonella prevalence for each supplier with the regulator's import review, and Hesperia Spices, its
largest supplier, is under review. Lots are sampled sack by sack and sub-samples are pooled into composites of nominally 30. The laboratory
tests composites, re-tests the individual sub-samples of a quarter of the positive ones, and acknowledges everything to the importer. The
pack holds the importer's sampling log, the laboratory's acknowledgement file, its methods sheet, the regulator's filing rule and four
closed quarters of acknowledged lot prevalences.

## 2. Gate G: why this is legal

* **Litmus.** Every figure is correct: each sampling record, each acknowledged result and re-test, each closed-quarter prevalence. Nobody
  files a wrong figure and nothing reported is overturned. The difficulty is which estimate the laboratory's figures are.
* **Flags.** surface_read_dependency: no · stumping_family: analytical_non_defect · sole_data_defect: no.
* **Deletion test.** Delete the association's figure and both voices. The pooled-test MLE on nominal sizes, a textbook estimator, still
  files 13.6 and reproduces the quarter's positivity.
* **Instrument repair.** Re-test every positive composite individually and the estimate tightens, but the current quarter's re-tests that
  exist must still be combined with the composites, and the accredited construction is still pinned only by the closed quarters.
* **Lens swap.** The naive figure counts positive composites; the answer counts the positive sacks the composites and re-tests imply,
  a different population per lot.

## 3. The driving force

A strong solver knows minimum prevalence (positive composites over sacks) understates when composites hold several positives. It assigns
the composites that arrived without lot numbers using the courier-batch sequence, fits a pooled-test MLE, and checks the laboratory's
quarterly positivity: it matches. Every estimator matches it, though, because positivity uses only composite results. The laboratory's
acknowledged lot prevalences for the closed quarters are finer, and the textbook MLE returns 11 of 60 of them. The laboratory's figures use
each composite's received sub-samples, often fewer than 30 after damaged sub-samples are rejected, and fold the individual re-tests into
the same likelihood. Hesperia's re-tested composites held 2.6 positive sacks on average. With them, its prevalence is 18.9 per 10,000
sacks, not 13.6.

## 4. The ladder

| Rung | Construction | Lands on | Why a careful analyst stops here | Killed by (one shipped fact) |
|---|---|---|---|---|
| 0 | Positive composites per sack sampled, composites without lot numbers dropped | 9.0, −52% | The industry's minimum prevalence, as filed for years | The sampling log: each courier batch lists its lots' composite counts in sequence, which places every unnumbered composite |
| 1 | The same, with unnumbered composites assigned by batch sequence | 10.4, −45% | Every composite attributed, exactly | The methods sheet: a positive composite may contain more than one positive sub-sample |
| 2 | Pooled-test MLE on nominal composite size 30 | 13.6, −28% | The textbook estimator, and it returns the laboratory's quarterly positivity | The acknowledged lot prevalences: this estimator returns 11 of 60 closed-quarter lots |
| 3 | **Decisive:** likelihood over received sub-samples per composite, with individual re-test counts folded in | **18.9** | — | — |

* **Figure shape.** Every correction walks the figure up and the answer is the maximum cell, so a solver who stops anywhere files too low a
  prevalence.
* **Partial correction priced (L3).** A solver who uses received sizes but ignores the re-tests lands at 16.4 (−13%); one who folds in the
  re-tests on nominal sizes lands at 16.9 (−11%). Each returns fewer than 30 of the 60 closed-quarter lots.
* **Grid.** Attribution (dropped or sequence) × estimator (minimum, MLE nominal, MLE received, combined nominal, combined received) = 10
  cells. The nearest wrong cell is the full construction with unnumbered composites dropped, 17.0 (−10%).

## 5. Why the decisive rung survives the opponent

1. **Written nowhere.** The filing rule says "estimated by the laboratory's accredited method". The methods sheet describes composites and
   re-testing separately and never says how they combine.
2. **Pattern B, finer controls only one construction returns.** The combined likelihood on received sizes returns 60 of 60 acknowledged
   lot prevalences to 0.1. Received-size MLE returns 27, the nominal MLE 11 and minimum prevalence none, and every rival reads low, so
   none ties the quarterly totals. The construction combines two record types per lot into one likelihood, which no menu of composite
   estimators contains.
3. **No arithmetic symptom.** Composites reconcile to the sampling log, received counts to the laboratory's receipt notes, and every
   estimator returns the salient positivity.
4. **Not a row predicate.** It needs a per-lot likelihood across composites of different sizes and individual results, maximised jointly.
5. **The enumeration is arithmetic.** No column reports a sack-level prevalence for the open quarter.
6. **No cutover date.** The method is the same in every quarter, and nothing steps.
7. **Survives deletion.** With every voice removed, the textbook MLE still files 13.6.

## 6. The calibration corpus

* **Form.** The acknowledgement file: 4,860 composites over four closed quarters and the open one, each with lot (where recorded),
  sub-samples received, result and any individual re-test counts, plus the laboratory's acknowledged prevalence for each of 60 closed lots.
* **What it certifies.** The quarterly positivity, which every construction returns.
* **What pins the construction.** The 60 lot prevalences, returned only by the combined likelihood on received sizes.
* **Twin pair.** Lots H-0412 and H-0588 match on sacks, composites (12), positive composites (4) and nominal sizes. Their acknowledged
  prevalences are 21.4 and 10.7 (2.0×): H-0412's re-tested composites held 2.4 positives each and H-0588's held 1.2.
* **Resemblance points at the decoy.** On composite counts and positivity, Hesperia resembles the suppliers whose filings sit near 13.

## 7. Pins, voices and the licensed wrong basis

* **Filed pins.** The regulator's rule: the importer files each supplier's quarterly prevalence per 10,000 sacks, estimated by the
  laboratory's accredited method, with every composite from the supplier's lots counted.
* **Empirical pins.** The construction, from the acknowledged lot prevalences; the attribution, from the batch sequence.
* **Voices.** The QA manager: "Positive composites over sacks is what we have always filed." The supplier liaison: "Composites without lot
  numbers aren't Hesperia's to answer for."
* **Licensed wrong basis.** The rule records that the importers' association reports minimum prevalence and will present it at the review.

## 8. Determinism by construction

* **Assignment.** Every courier batch's composite sequence matches its lots' logged counts exactly, so each unnumbered composite has one
  lot.
* **Likelihood.** The combined likelihood has a single maximum for every lot and for the supplier's pooled quarter.
* **Sizes.** Received counts are recorded for every composite; none is zero.
* **Rounding.** The answer sits mid-bin at 18.9.

## 9. Prompt sketch and deliverables

> Hesperia's quarterly prevalence goes to the import review on 15 July, and our QA manager would file it the way we always have. Give me
> the figure per 10,000 sacks to one decimal, as the sentence we file, with `hesperia_prevalence.xlsx`, a chart `estimator_check.png`, and
> a one-page `filing_note.pdf`.

* `hesperia_prevalence.xlsx` — the estimate for the open quarter, the moisture sheet (ask A), the release sheet (ask B) and the
  closed-lot table (ask C).
* `estimator_check.png` — acknowledged against estimated prevalence for the 60 closed lots under each construction as four scatter panels,
  with the identity line, each panel's match count, and the twin lots labelled.
* `filing_note.pdf` — the committed figure and the estimators a reviewer will raise.

## 10. The ask layer

* **Ask A (device-carried, decoupled).** For each of the 14 suppliers, the share of lots arriving above 11% moisture. *Device:* two meter
  models are in use, and the meter register gives model B a 0.4-point offset; ignoring it misclassifies lots for five suppliers.
* **Ask B (device-carried).** For each supplier, the median days from arrival to customs release. *Device:* lots held for re-testing carry
  a second release record, and the customs note makes the later one final; taking the first understates three suppliers.
* **Ask C (validity).** The open-quarter figure under each of the four rungs, and closed lots returned by each estimator.
* **Decoupling.** Clearing the combined likelihood changes no figure in asks A or B.

## 11. Rubric arithmetic

14 suppliers (ask A) + 14 suppliers (ask B) + 4 rung figures and 5 estimator match counts (ask C) + the committed figure, the composites
assigned by sequence and Hesperia's positive composites + 5 named chart parts + 3 files ≈ 49 criteria.

## 12. World-building constraints

* Hesperia's open quarter: 1,240 composites, 18% without lot numbers; received sizes average 26.4; re-tested positives average 2.6
  positive sub-samples.
* Rung figures 9.0 / 10.4 / 13.6 / 18.9; other cells 16.4, 16.9 and 17.0.
* Closed lots: combined received 60 of 60, received MLE 27, nominal MLE 11, minimum 0. H-0412 and H-0588 match on every composite column.
* Meter offsets and release records never touch a composite or a re-test.
