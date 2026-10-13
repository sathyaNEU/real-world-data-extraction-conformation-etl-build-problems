# determinism-check report, task259, 2026-10-13

Pass: r2 (current pack). Earlier pass r1 (/tmp/determinism-check-task259-r1/verdict.md): DETERMINISTIC / APPROVE, on the pack before the stage-4 leak fixes. r2 judged the rebuilt pack (policy 3.2 and 4.3 reworded, people-data readme pay_zone and ATS lines, employer display names, extra out-of-scope crosswalk rows, privacy-withdrawn reports, offers count). After r2, two data-only realism fixes were rebuilt (more varied employer display names, per-employer crosswalk effective_from dates 2019 to 2021); no document, prompt or graded figure changed (87 checks, verifier and figures.json unchanged), and they were not re-judged. The judge's optional lever (file "movement in pay at a fixed level across filing dates" in policy 4.3) was declined by the author: it files the HOW and turns the decisive step into rule application.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Policy 4.2 to 4.4 fixes the population (US, full time, data-engineering family with focus data pipelines and platforms, crosswalk row in effect on the filing date, each respondent once), the statistic (P25, median, P75 to the nearest $1,000) and the read date (1 Oct 2026, "the base pay a job and level commands on that date"). Literal execution requires carrying each report to that date. The one estimated input is the market's rate at a fixed level; the level-fixed cross-sectional slope gives 1.7 per cent a year, stable under experience and experience-squared controls (1.71 per cent). Every committed answer reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Matched n, DE I to IV | 788 / 1,234 / 1,366 / 844 | same (4,232 total; all 260 normalised names resolve) | yes (extract, profiles, crosswalk) |
| Level-fixed slope | 1.7 %/yr | 0.01713 (1.73 %) | yes |
| Midpoints DE I to IV | 117k / 143k / 168k / 201k | 116,979 / 142,836 / 168,024 / 200,914 | yes |
| DE III P25 / P75 | 155k / 182k | 155,116 / 182,057 | yes |
| Employed 1 Oct 2026 by level and zone | DE1 19/6/5, DE2 29/12/10, DE3 27/14/14, DE4 14/6/3 (159) | same | yes (hris, pay_zones) |
| Open requisitions | 3 / 5 / 8 / 3 (19) | same | yes (ats) |
| Rounding margin | n/a | at least about 0.4k on every figure, so the exact rate is not load-bearing | n/a |

## Competing answers that survived
| Reading | DE III midpoint | Status |
|---|---|---|
| No ageing (raw median) | $164k | contradicts policy 4.3 (read as in effect on the benchmark date); a wrong-path answer |
| Pooled slope, no level intercept (2.4 %) | $170k | composition-confounded by level mix |
| Within-person same-level raise (4.75 %) | $175k | the declared easy path; carries in-level progression |
| Within-person raise, all previous_ rows (6.8 %) | $180k | includes promotions |
| Level-fixed cross-sectional slope | $168k | golden |

Residual fork (judge: low risk, not zero): the policy files no rate, so a purely literal reader can reach $164k or $175k. The design takes this as the Layer 2 stump (rate identification), closed by "a job and level" in policy 3.1 and 4.3 and by the data. Counting postings instead of requisitions would change the open count, but the prompt asks for requisitions. Recorded pay_zone differs from the zone in force in 65 of 159 records; pay_zones_2026.csv with dates governs and the readme says the recorded zone is "as written". Leave counts as employed; contingent workers excluded by worker_type.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 4 (csv, md, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | tallyband_extract and profiles, 35,851 rows each | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | tallyband_offers_extract, oews_database_architects_2025; names do not label them | yes |
| Distractor quality | unused by solution, relevant, ruled out by a shipped fact | offers (offers not current pay), OEWS (wrong occupation and basis); neither is read by the golden | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | level x zone counts, requisitions by level, percentiles; "Round pay to the nearest thousand dollars" | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | card shape 07; criteria count not inspected here (rubric is generated downstream) | not verified by me |
| Reads as real work product | no LLM tells | judge saw none; golden realism not re-read by me | judge pass |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical. Design note and card: decisive step is ageing by the level's movement across filing dates against the re-reporters' growth ($175k) or no ageing ($164k); `## Three rules` lines present with No decoy, Not semantics and Not rule application each argued; card `decisive_rule_filed: false`, `official_decoy: false`. The two declared distractors (offers, OEWS) were not named by the thread as carrying the task, and neither was the surface read. The previous_ columns, which the design treats as the easy path, are a shipped ordinary record rather than a declared distractor; the judge found no ranked wrong answer in the pack. Match, with no mismatch. Watch point: the note's Not rule application line says the ageing rule is left open by the filed text, which is the same fact the judge records as the residual fork; this is the intended stump, not a determinism failure, but it is the likeliest portal send-back reason.

## Stump power (Gate F)
Good, per the thread. A strong analyst who cleans names and applies the crosswalk can still file $164k (skips ageing) or $175k/$180k (reads movement from the previous_ columns, which the methodology page highlights). The counts add independent ask-level difficulty.

## Findings, ranked
1. Residual fork on the rate (low): policy 4.3 gives no rate or method. Author declined the "movement in pay at a fixed level across filing dates" wording because it files the HOW. Accepted; if the portal flags it, file the WHAT only.
2. The two post-r2 data-only rebuilds were not re-judged. The author reports no document, prompt or graded figure changed.
3. Rubric criteria count (25 or more) and golden realism not verified in this pass.

## Next action for the author
Proceed to ship (stage 5). The pack is DETERMINISTIC / APPROVE on r2; no FIX_NOW re-judge is required.
