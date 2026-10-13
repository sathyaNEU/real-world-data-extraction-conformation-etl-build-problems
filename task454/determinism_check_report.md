# determinism-check report, task454, 2026-10-13

Bundle judged: the fresh unzip of target.zip at /tmp/determinism-check-task454-stage4/target/ (12 files: csv, docx, pdf, xlsx; the 229,247-row claims extract). One sonnet thread at medium effort, the judge system prompt inlined verbatim, blocks from submission.md, KEY_ASSUMPTIONS empty. The verdict below is the thread's, unchanged; no rebuilt file was opened and no second thread was run. The prompt is prompt.txt (not the legacy .md).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (the thread: no rerun; one optional note on the Antiparkinson unrounded figure)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (borderline: the missing AAC rates are the survey's documented structure, not a planted defect)

## Why
The only call the shipped files force is Anticonvulsants ($43k vs Antipsychotics $30k), once the NDCs with no AAC rate are costed against comparable priced NDCs of the same product and package type (program terms C.5, rate file, drug file package descriptions). Priced cartons run 1.90 times the bottle of the same product (68 products, sd 0.02). A package-blind pool gives Antipsychotics $65k; cartons at the bottle rate gives Antiparkinson $47k. All twelve FY2026 workbook rows reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Extract rows on fills Apr 2026 to Mar 2027 | 224,851 of 229,247 | 224,851 of 229,247 | yes |
| Unpriced share of ingredient cost | 43% | 43.4% | yes |
| Carton share of unpriced cost | 86% | 86.2% | yes |
| Carton to bottle ratio | 1.90 | 1.8997 (product-month), 1.897 (product) | yes |
| Anticonvulsants spread | $43,097 / $43,000 | $43,093 | yes (rounded) |
| Antipsychotics spread | $30,124 / $30,000 | $30,102 | yes (rounded) |
| Dementia agents | $23,976 / $24,000 | $23,846 | yes (rounded) |
| Antiparkinson agents | $23,177 / $23,000 | $22,804 to $22,929 across variants | rounded yes; unrounded no (373 gap) |
| Other eight spreads (rounded) | $15k, 9k, 5k, 3k, 3k, 3k, 2k, 2k | 15,021; 9,016; 4,871; 3,184; 3,102; 2,798; 2,194; 1,834 | yes |
| FY2026 workbook, 12 rows (claims, units, cost) | e.g. C107 40,046 / 2,412,350 / $203,083 | exact match on all twelve (C107 203,082.75; C114 214,916.71) | yes |
| 1,265 late-paid FY2026 transactions added; 3,131 already in summary | as stated | confirmed via layout file | yes |

## Competing answers that survived
None on the call. Residual fork, low: no filed text says how acquisition cost is estimated for NDCs with no rate. The data separates the candidates, the call is invariant across all package-aware variants (median vs mean, monthly vs annual peers, ratio 1.80 to 2.00; top two always C107 then C114), and the asked figures are rounding-stable at ratio 1.90 (middle classes move at 1.80 or 2.00). The thread's pin if ever wanted: file the WHAT (units on NDCs without a rate are costed as comparable priced NDCs of the same product and package), never the HOW. The summary's class labels differ from the 2027 list on about 700 rows; the 8 March 2027 letter pins the 2027 list, so no fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, docx, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | 229,247 rows | yes |
| Distractors named, none labelled in a file name | 2 or more | mco_pharmacy_encounter_summary_2026.csv and state_pdl_status_2027-01.xlsx, named in metadata.json; names carry no label | yes |
| Distractors unused yet weighable | yes | thread: unused, relevant enough to weigh. I did not check that one answering a graded quantity reproduces arithmetically | partly checked |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12-class spreads and 36 FY2026 figures; the prompt states nearest thousand, nearest dollar, whole units | yes |
| Prompt shape and 25 or more criteria | shape 07, 25 or more | shape 07 per metadata; the design note's arithmetic gives about 57 (generated rubric not inspected) | yes (by design note) |
| Not LLM-generated; goldens read as real work products | yes | thread found no authoring or benchmark disclosure; golden realism not independently read here | not independently verified |

## Gate G reconciliation
The thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note and card (read after the verdict): Gate G method_or_model_selection, `stump_class: analytical`. Match. The declared distractors (the MCO encounter summary and the PDL status file) are not what the thread names as the surface read; the thread names the package-blind product-rate fill ($65,405 for Antipsychotics), which equals the note's default path and analyst test. No finding that a distractor is too load-bearing.

**Gate G:** pass, method_or_model_selection / analytical_non_defect, no surface-read dependency.
**Gate H:** domain pass, layers pass, decisive_step analytical (estimating acquisition cost of units on unpriced NDCs within product and package type). Note and card agree: `## Three rules` has Domain test, Layer 1, Layer 2, Decisive step, No decoy, Not semantics and Not rule application lines, with the same decisive step.

## Stump power (Gate F)
Moderate to good. Pooling unpriced NDCs across packages (or skipping them) is the natural route and files Antipsychotics at $65k. The 1.90 carton premium is reachable only by comparing priced cartons with priced bottles, and no document names it.

## Findings, ranked
1. Solution step 4 gives Antiparkinson unrounded $23,177. The thread recomputes $22,804 to $22,929 under every variant (373 lower than anything it got). The rounded $23,000 and the call are unchanged. Reconcile the text or the estimator; no rerun needed.
2. Low residual fork: the imputation method for unpriced NDCs is not filed, and the design note concedes this ("nothing filed says how a unit with no rate is costed"). The call is invariant. The rounded figures are stable at ratio 1.90 but would move for the middle classes at ratio 1.80 or 2.00. If a repair is wanted, file the WHAT only.
3. The thread found the unrounded figures for Dementia agents and Antiparkinson agents differ slightly from the solution text (23,846 vs 23,976; about 22.8k vs 23,177), all in the same direction. Related to finding 1, rounding-safe.

## Next action for the author
Reconcile the Antiparkinson (and Dementia) unrounded figures in submission.md step 4 with the generator's estimator, confirming that every rounded ask figure stays the same; otherwise ship.
