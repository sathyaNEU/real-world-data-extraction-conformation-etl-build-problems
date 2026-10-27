> Architecture 2's report. It was taken on the 2027 adolescent literacy grants pack, which no longer
> exists: architecture 3 is a fresh world and a new bundle. Stage 4's judge run on the current pack is
> what counts for this build.

# determinism-check report, task464 (architecture 2, pass 2), 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (test linking), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium, scratch-only, Bash) recomputed the call from the bundle. The bridge file puts 15.73% of students at Level 1 on the new test. Retiring scores of 241 and below hold 14.6% and 249 and below hold 19.2%. Every linking convention tried (nearest cumulative, quantile, percentile rank, mean-sigma linear, both test-order subgroups) lands on 241. At 241 the counts reproduce: Elmorrow sixth at 368, Harlenbrook first out at 353, gap 15. The one live rival, regression of new on old (231 and below, 11.1% at Level 1), funds Harlenbrook and is refuted by the bridge file's own distribution.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Count-day spells, grades 9-10, 14 applicants | 33,797 | 33,797 (enrollment csv) | yes |
| Students with a grade 8 result | 31,896 | 31,896 | yes |
| Level 1 counts, all 14 applicants | Kessick 1,113 ... Ashgrove-Fenley 122 | identical | yes |
| Gap Elmorrow vs Harlenbrook | 15 | 368 - 353 = 15 | yes |
| Conformed levels L1-L4 | 5,764 / 12,448 / 8,700 / 4,984 | identical (cuts 241/300/342) | yes |
| Bridge Level 1 share, new test / regression | 15.7 / 11.1 | 15.73 / 11.14 | yes |
| Grade 7 Level 1 count and share, all 14 | e.g. Kessick 532 / 19.8% | identical, cut 2390, nonpublic rows removed | yes |

## Competing answers that survived
None on the main call. Residual minor forks, neither touching the call:
- Nonpublic-school grade 7 students in the "applicant's grade 7" ask: golden excludes them. Inclusion moves counts by up to about 6 and shares under 0.5 points (design fork SF12, closed by the registry).
- Conformed CSV Levels 2-4 boundaries for retiring scores (300, 342) are not filed; a "first score at or above the percentile" convention could shift L2/L3. The Level 1 column and the call are unaffected. Author may want a filed sentence or a note that the counts are insensitive.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | csv, pdf, xlsx | yes |
| Large file | 25,000+ rows | enrollment 90,635; results 72,240 and 72,108 | yes |
| Distractors in metadata.json, none named in a file | 2+ | district_expenditure_per_pupil_2025.csv, four_year_graduation_rates_2025.csv; no file name labels them | yes |
| Distractor weighs but is unused and answers nothing graded | relevant enough to weigh | both unused; neither bears on a graded quantity, so they are weak weights | weak, see findings |
| Deliverables | 1-3, all in golden | 2 (xlsx, csv) | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 14-row cuts, whole numbers and percentages to one decimal | yes |
| Prompt shape, rubric 25+ criteria | identifiable, 25+ | shape 01 identified; per-applicant figures (14 x 3) plus the call and the CSV levels give well over 25 gradable items; the generated rubric is not in the folder, so the count is unconfirmed | yes (inferred) |
| Reads as real, not LLM generated | yes | operational artifacts (crosswalk, spells, page break, code mismatch); judge found no tell | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 is the linking choice (concordance, not regression), stump class analytical, analyst test = regression lands on Harlenbrook 323 vs Elmorrow 315. These match, including the rival slate, the 231 and 241 cuts and the 15 margin. The declared distractors are not named as the surface read carrying the task; the rejected routes are regression, a classifier, cohort matching and the file's own levels, all in the design ladder. No mismatch. Gate H: domain pass (psychometric concordance from a single-group bridge study; noun swap loses the move), layers pass, decisive_step analytical. This agrees with the note's `## Three rules`.

## Stump power (Gate F)
Good per the thread. The easy routes (regression, per-score classifier, statewide cohort matching, the retiring test's own levels, the grade 7 file's performance level) all file a wrong funded set or wrong grade 7 counts, and the bridge file's distribution check is what refutes them. The 15 student margin holds across all 30 linking conventions.

## Findings, ranked
1. Residual: Level 2-4 conformed cuts (300, 342) are unfiled; harmless to the call, a possible stray miss on the CSV level counts. Optional fix.
2. Weak distractors: the two declared files do not bear on any graded quantity, so a reviewer may judge them irrelevant rather than weighing. Not a determinism issue; consider whether the spec gate is read strictly.
3. Design risk to watch (not a defect found): the decisive step is the choice of linking method with the rule silent on HOW. The thread found the data separate the candidates (the bridge file's own Level 1 share), which satisfies the literal-determinism standard.

## Next action for the author
Proceed to ship; optionally add one filed sentence on the Levels 2-4 placement for the conformed CSV or confirm its insensitivity in checks.py.
