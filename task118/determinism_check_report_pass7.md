# determinism-check report, task118, 2026-10-27 (pass 7, the re-judge owed after pass 6's FIX_NOW)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor / method_or_model_selection (winner's-curse shrinkage and incrementality, validated on the change log), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged bundle: target.zip sha256 3f9e9efb04d1d7ab6244f8429e245a319d913bcf4ad8d735a8aa64d4a1cf4eed (fresh unzip at /tmp/determinism-check-task118-pass7/target/), prompt.txt (current, not legacy), submission.md graded blocks. One thread, one pass. Thread verdict: /tmp/determinism-check-task118-pass7/verdict.md.

## Why
Every committed answer reproduced from the 17 shipped files. The open method choices (winner's-curse shrinkage, share of won clicks new to Bightline) are pinned by the change log: both fit 7 of 7 closed embeddings within about 1.2%, while the raw lift misses by 30% to 100% and one flat 57% share fits 2 of 7. Business·national at 500,000 leads Local·metro at 400,000 (unrounded 496,091 vs 392,470; gap 103,620 also rounds to 100,000). The pass-6 autosave finding is closed: the thread tested autosave against publish time for the note and timing the fix at the publishing save, and the six xlsx rows reproduce exactly (all 18 values), stable across note windows of 9 to 20 minutes (15 also tested earlier; 30 begins to differ, outside any reasonable reading). Standards 7.3 and 7.4 license the publishing-save timing.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Variant packages (archive) | 10,111 | 10,111 non-control variants, 1 shipped per test | yes |
| BUS-N shrunk lift | 2.00% | 1.999% (raw 2.34% = dashboard) | yes |
| BUS-N untested own-page clicks | 34,900,000 | 34,890,138 | yes |
| BUS-N won clicks | 700,000 | 697,588 | yes |
| Share new: BUS-N / CUL-N / LOC-M | 71.1 / 26.9 / 48.6% | 71.12 / 26.86 / 48.57% | yes |
| Extra clicks BUS-N / LOC-M / CUL-N / SPT-N / POL-N / SPT-M | 500k / 400k / 350k / 300k / 300k / 50k | 496,091 / 392,470 / 336,400 / 324,740 / 317,629 / 47,129 | yes (rounded) |
| Gap | 100,000 | 103,620 unrounded | yes |
| Lift back-test (7 embeddings) | within 2%, raw 0 of 7 | +1.2, +1.0, +0.2, +0.5, -0.3, -0.7, -0.9% | yes |
| Share back-test | 7 of 7 within 2%; flat 57.0% fits 2 | implied shares match to the sheet | yes, with a caveat (below) |
| xlsx medians / within 1h / over 3h | POL-N 86/14/7, SPT-M 55/9/2, BUS-N 89/10/6, SPT-N 47/23/2, LOC-M 102/12/6, CUL-N 119/1/5 | identical (n = 43, 17, 37, 39, 31, 13, all odd) | yes, all 18 |

Caveat: the "within 2%" back-test claim holds with the embedding window as the calendar year of test start; a started-in-embedding-dates window gives 1% to 7%, still far better than raw. Not a fork on any graded figure.

## Competing answers that survived
None. Forks tested for the main call (binomial vs Poisson variance, shrink toward zero, web-only prior, per-desk prior, national home-page CTR for Brisbane desks) leave the winner and every rounded figure unchanged except the Local·metro cell, 404k under one variant, which still rounds to 400,000. For the xlsx, note window 9 to 20 minutes, autosave vs publish time for the note, and boundary ties at 60 or 180 minutes all give identical results. Fixed +10 offset is what the AEST column carries. Not applying the scheduled go-live rule gives clearly wrong values and is not a literal reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 6 (csv, pdf, xlsx, parquet, eml, docx) | yes |
| Large file | 25,000 rows or more | parquet 2,312,406; cms_revisions about 271k | yes |
| Distractors | 2 or more named, none labelled by file name | 5 in metadata.json (syndication agreement, newsletter performance, dashboard export, panel monthly, panel reference workbook); no file name labels one | yes |
| Distractors weigh yet unused; one answering a graded quantity reproduces and a shipped fact rules it out | as stated | dashboard raw lifts reproduce arithmetically (2.34% for BUS-N); ruled out by the change log (raw lift 0 of 7) | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (docx, xlsx); both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | as stated | xlsx: 6 desks x 3 measures; prompt states nearest 50,000 and whole minutes | yes |
| Prompt shape, rubric 25 or more criteria | identifiable shape, 25+ | 803 characters; shape is opportunity sizing with per-desk table. Criteria count not generated yet; the graded cells alone are 18 xlsx + 2 docx + 3 components + recommendation, on the border before instruction-following items | not verifiable here (flag) |
| Not LLM generated; goldens read as work products | as stated | judge found normal metadata, no authoring language; golden docx reads as a managing-editor brief with footnoted chart; xlsx has Desks, Click chain, Pages, Back-test sheets | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor / method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical; analyst_test names Culture·national at about 1,250,000 as the easy route (shrink, size on own-page clicks, net out tested headlines) and the missing step as the new-to-site share, one minus page click-through; the design note's Layer 2 says the same. The thread's easy routes match exactly (Culture·national 1.25M; raw lift plus share gives 600,000 on Business·national; shrink without share returns Culture·national). The thread did not name the declared distractor (dashboard export) as the surface read carrying the task: the dashboard is the Politics and Sport·metro raw-lift lure only. Match, no finding.
Gate H line from the thread: domain pass, layers pass, decisive_step analytical. Card domain_test (uplift sizing, incremental clicks, page-level click-through, holdback validation) and the note's Task type, Swap and Layer lines agree. Match.

## Stump power (Gate F)
Strong on paper. The decisive step is an estimand (the share of won clicks new to the site) validated out of sample, not a rule read. Method-selection note for the main thread: the thread reached the golden by testing the candidates against the change log, which is the filed selection criterion, so the standard-method caveat does not apply here; stump measurement stays with the portal. The xlsx timing layer is rule execution (asks are free of rule 3) and is an additional hard layer.

## Findings, ranked
1. None blocking. Pass-6 FIX_NOW is closed.
2. Minor: step 4's "within 2%" depends on the embedding window being the calendar year of test start; consider stating it if convenient (does not move any graded figure).
3. Minor: rubric criteria count to be confirmed when generated.

## Next action for the author
Proceed to ship; no regeneration, prompt change or file change is required. Run the free ship gates as usual.
