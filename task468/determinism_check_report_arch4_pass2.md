# determinism-check report, task468, 2026-10-20 (pass 2, the single re-judge after FIX_NOW)

Bundle: target.zip sha256 f511b179e6742bf8. One isolated judge thread (sonnet, medium) on a fresh unzip at /tmp/determinism-check-task468-20261020T091038/target/. Verdict file: /tmp/determinism-check-task468-20261020T091038/verdict.md.

## Verdict
DETERMINISTIC (SOLUTION_WRONG only in a cosmetic sense, two wording items in submission.md)
**Disposition:** FIX_NOW (wording only; no file, prompt or rerun change)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: yes (strict clean-data test; the Office's methods note discloses both error types, so it is not a hidden defect)

## Why
Every graded figure reproduces from the bundle: five losers (Brannock, Calloway, Mercy Valley, Northgate, Westover), all 14 bonus figures and the $7,073,300 total. The filed spec defines death as the member's actual death, the Office's note says links are both missed and false, and the bill-recorded deaths plus later-claims evidence of life measure both rates by identifier class. The union route and the repair-only route both file four (Varden in; Brannock and Mercy Valley out), and are not equally licensed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Index admissions | 34,500 | 34,500 | yes |
| Recorded deaths linked, SSN / single / two-part | 829/836, 44/48, 78/162 | same | yes |
| Alive after day 30, linked | 12/21,855, 20/1,179, 8/1,554 | same | yes |
| Brannock D/E | 84.9/67.9, 1.25 | 84.909/67.853, 1.251 | yes |
| Calloway | 190.6/143.8, 1.33 | 190.581/143.752, 1.326 | yes |
| Mercy Valley | 502.2/387.1, 1.30 | 502.229/387.079, 1.297 | yes |
| Northgate | 189.3/122.2, 1.55 | 189.280/122.177, 1.549 | yes |
| Westover | 260.3/179.9, 1.45 | 260.299/179.915, 1.447 | yes |
| Varden | 26.4/25.6, 1.03 | 26.361/25.605, 1.030 | yes |
| Highest keeper Fairhaven | 1.09 | 1.091 | yes |
| Network bonus total | $7,073,300 | $7,073,300 | yes |
| Five losers' bonus total | $2,824,700 | unrounded sum rounds to 2,824,700; rounded rows sum to 2,824,800 | yes, with a rounding ambiguity |
| 14 per-hospital bonus figures | per submission | match golden exactly | yes |

## Competing answers that survived
None defensible. Union of bill deaths and links gives 4; dropping contradicted links and adding bill deaths gives 4; pooling SSN against non-SSN gives a different five (Brannock out, Varden in); dividing by sensitivity ignoring false links gives 6. The data show sensitivity 0.92 against 0.48 between single and two-part surnames, so pooled estimators are wrong. Whole-class Rogan-Gladen and subtract-false-link-then-divide both return the same five.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, xlsx, pdf, txt (4) | yes |
| Large file | 25,000+ rows | service lines 324,402 (claims 65,122; enrollment 70,362) | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | HCHP_Quality_Dashboard_Readmissions_FY2026.xlsx, HCHP_Network_Hospital_Profiles_2026.pdf; names do not label them | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | readmission ratios on other stays and a services list; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 1 xlsx; golden holds it (sheets Determination, Linkage correction, Chart with 1 chart, Notes) | yes |
| Asks | multi-dimensional, unit and rounding stated | count plus names, per-hospital call and bonus, total, chart; nearest $100 stated in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable shape | shape 10 scorecard (14 hospitals x call and bonus, total, count, chart); criteria count plausible, not generated or checked here | yes (not counted) |
| Not LLM generated, goldens realistic | | judge saw no authoring leakage; mixed key formats read as system output | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect yes (strict). Design note and card: stump_class analytical, Layer 2 estimation_fit (linkage-error-corrected deaths by identifier class), decisive step the class-by-class correction. These agree on the mechanism and the decisive step. The declared distractors (readmission dashboard, profiles) rank nothing the call reads; the thread named neither as the surface read, so they are not too load-bearing. Two items to weigh: (1) sole_data_defect yes, because with perfect linkage the task reduces to O/E with index rules; the mitigant is that the Office's note discloses both error types and the rates are measured in the shipped data, so it is not a planted defect. (2) The note's "No decoy" claim holds on the judge's reading.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical (risk-adjusted 30-day mortality with outcome ascertainment error estimated and corrected by identifier class; Layer 1 is the CPS and platform replacement conventions, NPI change, encounter file and dispute log). Matches the card's analyst_test and domain_test and the note's Three rules. The correction is the field's method, but the thread reached the golden by measuring rates the data had to supply, not by executing a filed procedure.

## Stump power (Gate F)
Good per the thread: the easy and the careful-repair routes both file four with Varden in. Model-run tally not supplied. The correction is a recognised method (Rogan-Gladen style), so a strong solver may land it; the main thread should weigh that with the scored readers' result (library methods are textbook routes, stumping 1.3). Layer 1 conformation and the $100-exact bonus figures add independent ways to miss.

## Findings, ranked
1. Margin on Varden: point estimate 1.03 against 1.15, about 3 deaths under the line (26.4 against 29.4). A parametric resample of the four measured rates flips Varden to losing in about 25 percent of 300 draws, driven by the single-surname false-link rate (20 of 1,179). Every correct point estimator lands on the same side, so the thread treated it as thin but clean. Residual risk, no wording fix possible. Brannock never flips; Mercy Valley and Fairhaven are not near the line.
2. SOLUTION_STEPS step 8 is narrower than the golden. The same-day exclusion is worded for the CPS case (change equals the additional payment); the golden also excludes 163 platform replacements whose full amount equals original plus the additional payment. Applying it to the 49 CPS cases only gives $7,083,700, not $7,073,300. Wording fix: state that the exclusion covers any replacement paid on the day of the additional payment that already carries it (CPS change equal to it, or platform full amount equal to original plus it).
3. Critical component 4 gives $2,824,700 for the five losers; the five rounded rows sum to $2,824,800. Say it is the unrounded sum rounded to the nearest hundred, or drop the figure.
4. Housekeeping: the existing task468/determinism_check_report.md describes a different task (a pharmacist-caseload charter, "architecture 2", target.zip f9f35f57b4293ef0) and does not match task468's content. This is not a task468 verdict; the main thread should check how it got there.

## Next action for the author
Edit submission.md: reword step 8's same-day exclusion and critical component 4 as in findings 2 and 3, then re-save. No change to target/, the prompt or the golden. This was the single re-judge, so no second thread.
