# determinism-check report, task233, 2026-10-16 (run r2, architecture 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (medium) saw only the fresh unzip and the extracted blocks. All 24 flags, 24 headline rates and 4 band rows reproduce from the bundle under a literal reading of QS-4, the methodology and the follow-up report. The open item is the shape of "the departure": the follow-up's own cases fix it (logit-scale slope 0.99 NEET, 1.03 HE; points gap grows with allocation; district and band heterogeneity tests not significant). Per-band odds ratios and a linear calibration give identical flags; only the flat-gap and pooled-ratio shapes differ, and the data rejects both.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Comparable follow-up cases | 3,134 | 3,134 (3,617 - 125 F99 - 358 with a form) | Yes |
| Nonrespondents / leavers 2026 | 7,641 / 47,734 | same | Yes |
| Odds ratio NEET / HE | 2.46 / 0.41 | 2.462 / 0.407 | Yes |
| Logit calibration slope | 0.99 / 1.03 | 0.99 / 1.03 | Yes |
| Shift range | 0.34 to 3.72 | 0.338 (ED06 NEET) to 3.723 (ED03 NEET) | Yes |
| Flags | 5 suppressed, 5 standard, 14 caution | same pattern | Yes |
| 24 headline rates | ask 1 | all match to one decimal, none within 0.01 of a rounding edge | Yes |
| Band table | AB1-AB4 | 11,331 / 14,483 / 12,699 / 9,221 and rates match (final points band) | Yes |
Closest flag margin 0.39 points from a threshold (ED07 NEET 0.63, ED04 HE -0.69).

## Competing answers that survived
None on the flags. Residual (rates only, no flag): build-7 online returns read in the 2025 edition's order is inferable from the activity-code header, absence of code 8 on 7.3.2 returns and the 2025 final file's code-to-destination pairs, but no document states it. Reading 2026 order moves published rates (e.g. ED01 NEET 27.2 vs 28.2). Optional pin: a DATA_DICTIONARY line on form_build (a rerun would follow if added).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | Yes |
| Formats | 3+ | csv, pdf, xlsx, md | Yes |
| Large file | 25,000+ rows | 47,734 (frame), 47,734 (points), 46,493 | Yes |
| Distractors in metadata, none named in a file | 2+ | 3 (LFS regional NEET, 2025 release table, careers contacts); no file name labels one | Yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | regional/2025-year/contact data are other populations or years; stated in README and dictionary | Yes (judged by reading; thread flagged unused) |
| Deliverables | 1 to 3, all in golden | 1 xlsx | Yes |
| Asks multi-dimensional, unit and rounding stated | yes | 24 flags+rates, 4 band rows x 3 values; percent, one decimal | Yes |
| Prompt shape, 25+ criteria | yes | shape 07 grid of cells; 24 + 24 + 12 cells + components | Yes |
| Not LLM-looking, realistic goldens | yes | thread saw no authoring language; golden realism not re-judged here | Yes |
| License/source metadata | recorded | CC0 original, recorded in metadata.json | Yes |

## Gate G reconciliation
Gate G: PASS. The thread named the pooled flat points gap (14.5 / -11.1) and a pooled ratio as the surface read, both derived by the solver from the follow-up, not shipped artifacts; no shipped file ranks or flags the statistics. The declared distractors were not the surface read. Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read no, sole_data_defect no; design note stump sentence (carry departure as fixed points instead of odds scale, 11 of 24 flags wrong) and card stump_class analytical match. The judge measured the flat-gap route as 9 districts changed against the note's 11 flags; the discrepancy is counting unit (districts vs flags) and does not alter the finding.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the note's Three rules and the card's analyst_test and domain_test. Watch item: the note says no filed sentence names the scale of the departure; the judge accepted that as method left open and forced by the data (calibration slope ~1), which the contract allows.

## Stump power (Gate F)
Good. Cleaning, reading QS-4 and getting rates right leads to the pooled flat gap, which files 9 districts (11 flags) wrong; a pooled ratio changes ED09 and ED12. Only a solver who validates the departure shape on the follow-up reaches the golden. Asks add quiet traps (build-7 code order, revised-points bands).

## Findings, ranked
1. Minor: build-7 code order unstated (rates only). Optional dictionary pin.
2. Minor: method of the departure not literally filed; pinned by data, alternatives agree.

## Next action for the author
Proceed to ship; optionally add the form_build pin to DATA_DICTIONARY.md (would need a rebuild and a re-judge).
