# determinism-check report, task486, 2026-10-26 (pass 2, architecture 3)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (wording only in the Final Recommendation prose).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (small-area apportionment, also etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread ran once (sonnet, medium) from /tmp/determinism-check-task486-r1/ only; verdict at /tmp/determinism-check-task486-r1/verdict.md.

## Why
Executed word for word from the files, with floor area times single-site staff per m2 by description, the answer is the golden's 15 centres. The data separates the candidate allocations (single-site density R1 0.063, O1 0.072, R3 0.044, R2 0.027, R4 0.014, W1 0.010 staff per m2). The 15-centre call holds under pooled density, 2022 density for both years and live postcodes only; the nearest centre to the 8 per cent line is 1.65 points away.
Two defects, neither moving a graded figure:
1. Final Recommendation says every qualifying centre "lost 10 per cent or more" and every other "6 per cent or less". Ingmouth and Fenmoss are -9.9 unrounded and TC01, 03, 05, 06 are -6.1 to -6.4 unrounded. True only after rounding. Reword.
2. Ask A (empty premises): 110 shop entries at 31 March 2022 (153 at 2026) have no rates account on the day and the golden counts them as occupied. No shipped file states this (the design note says the evidence is structural only). Counted empty, Rookgate 2022 reads 127, not 100, and every district moves. This is an open term on an ask, not on the main call; asks may turn on semantics, but the literal judge flags it. Pin it in the field guide (the WHAT, a shop with no account on a day carried no liability and was in occupation) without touching the stump.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Retail employers Mar 2022 / Mar 2026 (paye csvs) | 3,545 / 3,319 | 3,545 / 3,319 | yes |
| Multi-site retail employers | 45 / 45 | 45 / 45 | yes |
| Their employees | 10,279 / 10,990 | 10,279 / 10,990 | yes |
| Centres total, nearest thousand | 27,000 / 25,000 | 27,046 / 25,288 | yes |
| Eligible set | 15 centres | same 15 (TC02,04,08,10,11,12,14,16,20,23,25,27,28,30,31) | yes |
| 31 schedule rows (nearest 50, whole %) | per golden | all match | yes |
| Vacancy annex, 12 district-date figures and totals | 321/195, 429/305 | exact | yes |
| Rival area-share list | 19 centres | exact (adds TC01,03,05,06,09, drops TC16) | yes |

## Competing answers that survived
- Fork 1, allocation of multi-site staff (prospectus says "counted at the premises where they work", no rule filed). Alternatives: floor-area share 19 centres; equal split 12; description density only 11; PAYE postcode 15 but a different set. The thread judged the golden forced by single-site calibration (6x density spread by description), not an open term; residual risk that a literal grader reads it as a competing defensible answer. Design note rates it the intended analytical step.
- Fork 2, no-account shops in the vacancy annex (above). Unclosed by a shipped rule. Fix by one sentence.
- Terminated postcode LW14 3JE (TC15) touches only a non-eligible centre.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | csv 8, xlsx 2, pdf 3, json 1 (4) | yes |
| Large file | 25,000 rows or more | paye 27,497 and 27,349; footfall 76,974 | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | footfall csv, labour force survey xlsx; names are neutral | yes |
| Distractor relevant but unused, ruled out by a shipped fact | each | both unused by the solution (thread). I did not myself test that footfall or the LFS reproduce a graded quantity; the LFS carries no premises or centre (design note) | yes, unverified depth |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | each | schedule x 31 centres x 2 years, district x 2 dates x 2 measures; nearest 50, whole per cent, whole premises stated | yes |
| Vacancy annex completeness | all districts | 6 districts in schedule and golden annex, all present | yes |
| Prompt shape, rubric 25 or more | identifiable; 25+ | eligibility schedule with 31 centres and 12 district figures gives well over 25 gradable items; rubric itself not generated yet | yes (by count) |
| Not LLM generated, goldens realistic | | thread found no authoring language in the files; golden has Eligibility, Vacancy annex and Notes sheets | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, stump is calibrating multi-site staff placement on single-site densities, default path area share names 19. Match. Declared distractors (footfall, LFS) are not the surface read carrying the task; the rivals are area share and PAYE postcode, both derived, none shipped. Gate G passes (no shipped artifact ranks the centres wrongly).

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the note's Three rules (decisive step: employees placed at premises by floor area times description density from single-site employers). No mismatch.

## Stump power (Gate F)
Likely to bite: area share and PAYE postcode both look reasonable and need the single-site density calibration to catch. The thread classes the step analytical, and it reached the golden by applying the field's standard apportionment, so this is also a textbook route a strong solver may take once the PAYE address is recognised as not the workplace (stumping 1.3). The main thread should weigh this against the scored readers. Margin from the line is 1.6 to 2 points either side; matching about 3,500 employers across six council layouts is heavy work.

## Findings, ranked
1. Ask A: no-account shops counted occupied, unfiled (Fork 2). Moves every district figure if read the other way.
2. Final Recommendation wording "10 per cent or more" and "6 per cent or less" is false on unrounded figures.
3. Residual literal-reader risk on Fork 1 (allocation not stated as a rule); by design.
4. Stump power: standard method, see above.

## Next action for the author
In one pass in the generator: add one sentence to rating_list_extract_guide.pdf that a shop entry with no rates account on a day carried no liability and was in occupation (no figure moves), and reword the Final Recommendation to "about 10 per cent or more" / "about 6 per cent or less", or give the rounded figures. Re-judge once.
