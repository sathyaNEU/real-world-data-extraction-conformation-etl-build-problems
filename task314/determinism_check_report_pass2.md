# determinism-check report, task314, pass 2, 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Order kept: the thread wrote derivation.md to disk before opening graded_blocks.md (the graded blocks were kept out of the brief), so this is the one valid re-judge after pass 1's FIX_NOW. Its blind figures matched every committed answer. target.zip sha256 ab3b1d3b059fe38111057b50b38b44ab39743d35a6f4d7b32572ab68e8d1ebe1, 16 files at the root. The pass-1 report is untouched and was not shown to the thread. Scratch: /tmp/determinism-check-task314-p2816201/.

## Why
The shipped bills force one price concept and one elasticity range. The Fenwick Mesa USD 14 charge (RES 2024-17) moves only the fixed part of the bill, and Fenwick use falls against the rest of the city in step with the whole-bill price per thousand gallons (about -0.31 to -0.33). The July 2023 restructuring, instrumented, gives -0.32 to -0.35 on the average price and about zero on the marginal price once both are in. Ranking C > B > A holds across the whole defensible estimate range, and every ask reproduces from the files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Baseline accounts / acre-feet | 4,341 / about 770 | 4,341 / 772.25 | yes |
| Option C saving | 19.44 (20) | 19.44 | yes |
| Option B saving | 10.86 (10) | 10.86 | yes |
| Option A saving | 0.70 (0) | 0.70 | yes |
| Gap C minus B | 8.58 (10) | 8.58 | yes |
| Fill station water, Jun to Sep (thousand gal) | 678, 717, 630, 682 | 677,943; 717,127; 629,773; 682,170 gal | yes |
| Tanks filled, Jun to Sep | 244, 258, 229, 240 | 244, 258, 229, 240 | yes |
| Facility use, Jun to Sep (AF) | 22.6, 29.7, 31.2, 23.7 | 22.564, 29.693, 31.214, 23.711 | yes |

## Competing answers that survived
None. Forks the thread raised, each closed by the files:
- Marginal block price, with the response estimated from the 2023 change alone: ranks A first at 22 to 39 AF. Ruled out by the 2024 Fenwick charge, which moves whole bills and no block price (+18.5 per cent whole-bill price, -4.6 per cent use; the thread's own difference-in-differences gives -0.33), and by the marginal coefficient being +0.00 to +0.02 when the whole-bill price is in the model. A wrong analysis, not a competing answer.
- Elasticity form (constant, linear, midpoint) and the Fenwick charge counted in or out of the base: C 20, B 10, A 0, gap 10 in every cell from -0.26 to -0.325. Only the corner of an elasticity of -0.36, linear, charge out, reaches C 25.3 and leaves the bin. That corner lies outside the range the data support (about -0.26 to -0.35).
- A fixed-point price solve instead of price at baseline use: C 19.1 to 21.0, B 10.1 to 11.0, A about -1.5 to -1.9, all in the same bins.
- Fill station water summed from the gallons column or the vendor workbook double counts the 121 restart rows. Ruled out by each restart row repeating the previous opening register and amount_usd charging only the increment.
- Tanks counted as rows or as truck-plus-trailer restart pairs give 280/285/259/268. Ruled out by register overlap. The thread flags mild residual risk for a row counter.
- Facility meters with WB-POOL counted as well as WB-PAV give 23.8/30.3/32.1/24.1. Ruled out by the pool's advances sitting inside the pavilion's at the same address.
- Choosing the later or the earlier of the same-day WB-FLD re-reads moves Aug and Sep by 0.011 AF and changes no rounding.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | 276,914-row bills csv | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | 3 named: weather csv, state_pws xlsx, conservation_rebates csv; no name says distractor | yes |
| Distractor behaviour | unused by the solution, relevant, none reproduces a graded quantity | thread found them unused and none answers a graded figure; the rebates and state use files are relevant enough to weigh | yes |
| Deliverables | 1 to 3, all in the golden | 3 (xlsx, docx, png), all three present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | savings and gap in acre-feet to the nearest 10, fill station in thousand gallons to the nearest thousand, facility use in acre-feet to one decimal; each monthly ask is a four-month by two or three-figure grid | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 07 grid of cells, design note says about 26 criteria; the criteria count is by design note only, not recounted here | yes (on the design note) |
| Reads as real | no LLM tells, goldens read as work products | thread found no authoring leakage; the golden realism read was not repeated here | yes (on the thread's hygiene read) |

## Gate G reconciliation
The thread says `method_or_model_selection`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The card says `gate_g: method_or_model_selection`, `stump_class: analytical`. The design note says the marginal block price is a correct record and not what the response is scored on. The mechanism matches the card and the design note.

The thread's easy route (marginal block price, estimated from the 2023 change, files Option A at 22 to 39 AF) matches the card's analyst_test (Option A at about 7 to 16 AF on the city's own block-price estimates, 50 AF on a literature elasticity). The two differ only in the elasticity assumed. `wrong_basis_distractors` is empty and the thread named none of the three declared distractors as carrying the task. No distractor is too load-bearing. Gate G passes.

## Stump power (Gate F)
Good. Option A is the obvious conservation lever, and the textbook block-rate view prices the marginal block. The easy route files the wrong top option, Option A. The thread classes the decisive step analytical, and not as a field's standard method reached with no judgment, because the data must settle which of two correct prices customers answer, through the fit nobody is prompted to run. The asks add independent sub-traps (restart double count, sub-meter, register changeouts, the CCF unit, the vendor report's inflated gallons).

Margins: June facility use is 22.564 AF, 0.014 AF (about 4,500 gal) above the 22.55 edge. It survives 325,851 against 325,900 gal per AF (22.560), CCF 748 against 748.052, and either duplicate-read choice. This is the thread's one thin margin. Other figures are at least 1.3 AF (savings, gap) or 0.06 (fill station) from an edge.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. This matches the card's domain_test and the design note's Three rules (No decoy, Not semantics, Not rule application). The design note says no field or definition separates the two prices. The thread finds the shipped rate history separates them, and the two views agree.

## Findings, ranked
1. Thin margin: June facility use 22.564 AF, 0.014 above the 22.55 edge. Robust to the unit and duplicate-read variants the thread tried; no action.
2. The only corner leaving a bin (an elasticity of -0.36, linear, charge out) lies outside the data-supported range. No action.
3. Mild residual risk that a row counter reads the tanks as 280/285/259/268. The register overlap rules it out and the prompt defines the count.
No blocking finding.

## Next action for the author
Proceed to ship stage. No repair and no rerun is needed.
