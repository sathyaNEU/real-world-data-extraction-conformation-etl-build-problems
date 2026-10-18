# determinism-check report, task261, 2026-10-18 (pass 3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (paired replicate SE of a difference) plus etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executed literally, the brief (older of reference person and partner, six groups, 1.96 x SE rule, neighbouring-run segments) and the user guide (median definition, five-implicate average, 200 replicates, imputation variance with 1.2 factor) give four boundaries apart and 65-74 / 75+ merged: five segments. The one rival reading, per-group SEs added in quadrature, gives 1.57 at 55-64 / 65-74 and four segments, but the guide re-estimates with replicate weights and the groups share survey areas (replicate correlation 0.70), so it is not licensed. All customer-book figures reproduce only under the filed reading, and each alternative moves them, so each rule is load-bearing and derivable from a shipped file.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Median NW, six groups | 69k/281k/534k/790k/1,048k/815k | 69,233/281,337/533,999/790,343/1,048,229/815,286 | yes |
| Adjacent SEs | 24k/45k/77k/95k/149k | 23.7k/45.4k/76.9k/95.2k/149.1k | yes |
| Ratios | 8.9/5.6/3.3/2.7/-1.6 | 8.94/5.57/3.34/2.71/-1.56 | yes |
| Independent-sum SE, 55-64/65-74 | 165k | 164.5k | yes |
| RIA households / balance / payments | 445, 1,169, 742; $210,509k, $521,126k, $249,685k; $11,589k, $30,350k, $18,003k | same | yes |
| Annuity households / income | 179, 468, 280; $3,653k, $9,041k, $5,510k | same | yes |

## Competing answers that survived
None on the main call. One soft spot, asks only: taking the second of two same-member rows with identical balance and payment once is stated in no document (inferable, since two accounts cannot match to the cent). It touches the combined balance and payment figures in xlsx ask 3 (about $5m across groups if summed), not the call. The six "former partner still named" reversionaries sit on contracts with living annuitants and change no count.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, docx) | yes |
| Large file | 25,000+ rows | household summary 29,940 rows | yes |
| Distractors in metadata.json | 2+, none labelled by file name | results bulletin (wrong basis), customer research PDF; names carry no label | yes |
| Distractor weighs but unused | yes | bulletin gives age by reference person in ten-year bands, ruled out by the brief's placement rule; not the stump | yes |
| Deliverables | 1 to 3, all in golden | 3 (docx, xlsx, svg), all present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | per-pair and per-group tables; the prompt's closing sentence rounds every dollar amount to the nearest thousand | yes |
| Rubric 25+ criteria | 25+ | not counted in this pass (rubric is generated; 5 groups x medians/SEs, 5 pairs x 4 fields and 3 groups x 6 fields exceed 25 on the face of the goldens) | assumed yes |
| Reads as real work product, not LLM generated | yes | judge found no toolchain leakage and coherent dates; golden realism not re-read here | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor plus etl_conformance, analytical_non_defect, surface_read no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical. The design note's Three rules decisive step is the standard error of a contrast between two domains of one clustered sample on the replicate weights rather than the quadrature combination (R3, golden ladder rung, 2.71 and 1.56 matching the thread). metadata.json declares the results bulletin as the wrong-basis distractor, ruled out by the brief; the thread did not name it as the surface read carrying the task, and no shipped figure ranks the boundary decision wrongly. Match: no mismatch.

## Stump power (Gate F)
The quadrature route is correct arithmetic from the guide's per-estimate recipe and reaches four segments, so a strong analyst can miss it; the replicate and ETL chain makes full marks on the asks hard. Per the thread, plausible for strong models; measured only by the portal.

## Findings, ranked
1. No blocking finding.
2. Minor: the duplicate-row single-count rule is inferred, not filed; asks only.

## Next action for the author
Proceed to ship; optionally file one sentence in the data dictionary that a member's repeated identical rows are one account (no change to the call).
