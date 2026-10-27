# determinism-check report, task118 (architecture 2, pass 6), 2026-10-27

## Verdict
NOT_DETERMINISTIC (xlsx ask only; main recommendation and docx figures forced and reproduced). No SOLUTION_WRONG.
**Disposition:** FIX_NOW (one convention sentence for the xlsx ask; main call, ladder and docx stay frozen; re-judge once)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
Taxonomy label: underspecified_objective (unfiled save-type convention, data semantics). Judge ran as one isolated sonnet thread (medium) spawned by the main session; target.zip sha256 e97358e4...19a1.

## Why
The xlsx medians and counts turn on whether a CMS row with status=live and save_type=autosave is a live or published version. No shipped file defines autosave (confirmed by me: the corrections standard s7.3 to s7.8 never uses the word; it appears only as a save_type value in the CMS csv). s7.4 says "logged on the version that publishes the corrected headline" and "by a live save". Read literally, a status-live row is a live save. Counting autosave as live moves Local·metro to (86, 12, 5), Politics·national to (84, 15, 6) and Sport·national to (45, 24, 2): 3 of 6 desks. The golden (autosave excluded) is defensible, but a literal reading does not force it. Every other CMS rule (restored copies, entries part of the live blog, migrated articles excluded, put-back notes, the ten-minute window, scheduled go-live, timing on the headline save) is derivable from s7.3 to s7.8.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Business·national shrunk lift (archive csv, ML normal prior, 10,111 variants) | 2.00% | 2.00% (0.019994) | Yes |
| Untested own-page clicks Business·national (parquet) | 34,900,000 | 34,890,138 | Yes |
| Won clicks Business·national / Culture·national | 700,000 / 1,250,000 | 697.6k / 1,252k | Yes |
| Share new to Bightline B·n / Culture / Local·metro (page_performance csv) | 71.1 / 26.9 / 48.6% | 71.1 / 26.9 / 48.6% | Yes |
| Extra clicks B·n / Local·metro / Culture / Politics / Sport·national / Sport·metro | 500k / 400k / 350k / 300k / 300k / 50k | 496.1k / 392.5k / 336.4k / 317.6k / 324.7k / 47.1k | Yes (Sport·national 0.3k under the 325k midpoint) |
| Change-log share back-test (4 embeddings shown) | within 2% | 0.533 v 0.541, 0.364 v 0.359, 0.705 v 0.705, 0.566 v 0.561 | Yes |
| Shrunk-lift back-test against 7 realised holdback lifts | 7 of 7 within 2% | not re-run | Not recomputed |
| CMS medians, within-hour and over-3h counts, six desks | 86/14/7, 55/9/2, 89/10/6, 47/23/2, 102/12/6, 119/1/5 | identical, autosave excluded | Yes, under the golden's autosave reading only |

## Competing answers that survived
1. Autosave status. Answer A (golden): an autosave is not a published version, so it does not set go-live and headline changes on it are not corrections on a published version. Answer B (literal): a status-live row is a live save. A and B differ on Local·metro, Politics·national and Sport·national. Shipped rule meant to close it: s7.4 "the version that publishes the corrected headline". It does not define autosave, so it does not close the fork. OPEN.
2. Main call: raw lift gives Sport·metro, and no share gives Culture·national. Both closed by the shipped change log (winner's-curse shrinkage and the back-tested share), not by a filed sentence. This is the intended analytical layer, not a fork. Method choice (ML prior) is unfiled but the margin (103.6k unrounded) and the 50,000 rounding absorb alternatives; raw lifts with the share also keep Business·national ahead (581k v 526k).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | Yes |
| Formats | 3 or more | 6 (csv, pdf, xlsx, parquet, eml, docx) | Yes |
| Large file | 25,000+ rows | parquet 2,312,406 rows; CMS csv 266,633 | Yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | 5 named (syndication agreement, newsletter performance, dashboard export, panel monthly, panel reference workbook); file names carry no label | Yes |
| Distractors unused yet weighable | yes | judge: weighable and unused | Yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both present in golden/ | Yes |
| Asks unit and rounding | stated | clicks to nearest 50,000, minutes whole numbers | Yes |
| Asks multi-dimensional | yes | 6 desks x 3 measures | Yes |
| Rubric 25 or more criteria | 25+ | not verifiable here (rubric is generated); candidate and cell grid is 6 desks x 3 plus call items | Not verified |
| Reads as real work product, not LLM generated | yes | judge saw no authoring leakage; golden realism not re-read by me | Not verified beyond the judge |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The judge named no shipped artifact as the surface read carrying the task. Of the declared distractors, the dashboard export (blended vertical lifts) is called weighable and unused, not load-bearing. The design note's card/Three rules (domain test: share of won clicks new to the site from one minus page click-through, validated on holdbacks; Layer 2 the same share) agrees with the judge's mechanism (shrinkage plus incrementality share). Mismatch to record: the judge names winner's-curse shrinkage as the leading Layer 2 organ, the design note's Layer 2 line names the incrementality share; shrinkage is in the note's solution path, so I class this as consistent in substance, not a send-back mismatch. Gate G passes. The design note files the autosave as a deliberate silent device on the asks (fork row SF19, "not a published version"), closed only by s7.4 reading an autosave as no published version. The judge's literal reading shows that closure is not a filed sentence. Asks may carry devices, but the answer still has to be determinate from the shipped text, and here it is not.

## Gate H (Three rules)
domain: pass | layers: pass | decisive_step: analytical. Decoy absent, the main call is not data semantics, not rule application (shrinkage plus back-tested share). The unfiled autosave semantics sit in the asks only, which Rule 3 does not bind.

## Stump power (Gate F)
Strong for the main call per the judge: the easy route (raw lift times untested clicks) files Sport·metro, skipping only the share files Culture·national, and the right call needs shrinkage and the incrementality share both validated on the change log. Not a case of a textbook method applied with no judgment: the data separates the candidates. Caveat: the judge did not re-run the 7-of-7 shrunk-lift back-test, and Sport·national sits 0.3k from a rounding midpoint (rationale text only, not a graded figure). The autosave fork is an ask-side determinism defect, not stump power.

## Findings, ranked
1. (FIX_NOW) Autosave convention unfiled. 3 of 6 desks' xlsx rows move under the literal reading (up to 8 cells). Fix: one sentence in the prompt or in `editorial_standards_s7_corrections.pdf` saying a save typed autosave is not a published version (the WHAT of the population, not the method). Keep the main call, ladder and docx byte-identical; regenerate the xlsx golden and submission.md only if the convention changes; then re-judge once.
2. Note: if the sentence is added to the standards PDF, the "silent device" role of the autosave on the asks is gone by design; update the design note's fork row SF19 and ladder pair ceiling accordingly (the design note says the layer stands on one silent device). That is a rubric-side consequence for the main thread to weigh; asks are free of the no-hidden-rule ban, but determinism still wins.
3. Shrunk-lift 7-of-7 back-test not independently re-run (open for the next judge pass if it is a graded component).
4. Rubric criteria count (25+) not verified by this pass.

## Next action for the author
Add one sentence declaring a save typed autosave is (or is not, matching the golden: is not) a published version to the corrections standard or the prompt, rebuild, confirm the xlsx golden is unchanged, and re-judge once.
