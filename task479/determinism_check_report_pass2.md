# determinism-check report, task479, 2026-11-01 (pass 2)

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: statistical_rigor (credibility / small-group variance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The memo (renewal review PDF, s.2 and s.3) tests "expected 2027 retained claims per member per month" against the elected claims component. It names the evidence (the trust's 2023 to 2025 experience, trended 7 per cent for every employer) but never says how an employer's expected claims are read from it. Executed word for word, the answer is each employer's own trended three-year PMPM, which surcharges CR104, CR109, CR136, CR167 and CR176. The golden (CR113, CR118, CR131, CR149, CR167, CR176) holds only under Buhlmann-Straub credibility against the trust's level, which no shipped file states or forces. This is underspecified_objective (competing_defensible_answer) on the main call and on ask 1. The design note's own Analyst test and "Not rule application" lines concede that the literal route files the other set. The method is therefore open with nothing in the pack separating the candidates. The prompt dropping a count and the two describing files leaving the pack do not touch this finding.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Six surcharged employers (credibility) | CR113, 118, 131, 149, 167, 176 | same six; Z 0.14 (CR104) to 0.81 (CR181); level 500.25 | yes |
| Limited fluctuation on lives (1,000/2,000/3,000) | same six | same six | yes |
| Own-experience literal reading | not golden | CR104, 109, 136, 167, 176 | n/a (fork) |
| Limited fluctuation on member months | not golden | CR104, 109, 136, 167, 176 | n/a (fork) |
| Complement = broker survey 548.85 / 561.30 | not golden | adds CR104 / nine employers | n/a (fork) |
| Claims components, 18 employers | per submission | match golden inputs | yes |
| Ask 3 July to September 2026 member months | per submission | exact | yes |
| Ask 4 high-cost members and paid to date | per submission | exact (member_id alone gives wrong counts, e.g. CR176 37 vs 23) | yes |

## Competing answers that survived
1. Expected claims = the employer's own trended experience (the memo's literal text): CR104, CR109, CR136, CR167, CR176. The golden is the credibility-blended six. Nothing shipped closes this fork.
2. Limited-fluctuation credibility on member months gives the own-experience set. On lives it gives the golden six.
3. Credibility complement: the trust's level (golden) against the broker survey (548.85 adds CR104; 561.30 gives nine employers). Nothing shipped rules the survey out as a complement. The metadata calls it a distractor only because "no external benchmark enters".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | judged unzip: 12 files, csv, xlsx, pdf, eligibility 179,535 rows | yes |
| Distractors | 2+ named in metadata, none by file name | 3 named (rebate, roster, broker survey); no file name labels one | yes |
| Distractors unused yet weighty | unused by the solution; a shipped fact rules each out | survey flips CR104 as a complement and the memo only implies "own experience" | partial: survey is not closed by a shipped fact |
| Deliverables | 1 to 3, all in the golden | 1 xlsx, present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | asks 3 and 4 multi-dimensional with unit and rounding in the prompt; ask 2 (chart) is not independently graded | yes |
| Prompt shape and 25+ criteria | identifiable; 25+ | one shape; the criteria count is not verifiable from the shipped folder | not verified |
| Reads as real work product | yes | no LLM tells in the memo or the submission | yes |
| Bundle drift | none | the judged unzip had 12 files, but the current target.zip lists 14 (it still holds crbht_data_dictionary.csv and crbht_extract_manifest_2026-10-07.csv, and metadata.json still lists them). Per the coordinator, the pack was also rebuilt after the thread's unzip with employer names and account managers permuted, then reverted. The judged bundle is therefore not byte-identical to the current zip. | flag |

## Gate G reconciliation
The thread classed the stumping as mechanism statistical_rigor, family analytical_non_defect, with no surface-read dependency and no sole data defect. The design note and card declare an analytical credibility stump (forecast_uncertainty, Buhlmann-Straub). The mechanism matches. The declared distractors (rebate statement, roster, broker survey) are not named as the surface read carrying the task; the surface read is own-experience. No ranking artifact gets the decision wrong. The mismatch is not in classification. The golden's method is not forced by the filed text, and that is the Gate C/E failure.

Gate H: domain: pass (health-plan underwriting with credibility); layers: pass (Layer 1 two lag layouts, overlapping May cells, id reissue, 12/15 stop-loss basis; Layer 2 credibility-weighted expected cost); decisive_step: analytical.

## Stump power (Gate F)
Plausibly strong. The easy route is own experience (CR104, CR109, CR136 wrongly surcharged; CR113, CR118, CR131, CR149 wrongly spared). The stump counts only if credibility is forced, and it is not. A solver following the memo literally is not analytically wrong, so a miss would be an interpretive fork. The credibility step is a textbook actuarial method, which the main thread should weigh against the ladder.

## Findings, ranked
1. Main call and ask 1: the estimand is under-filed (competing_defensible_answer). Own-experience is the literal reading.
2. The credibility complement (trust level against the broker survey) is not closed. The survey flips CR104 and others.
3. target.zip drifts from the judged bundle (14 files against 12, name permutation and revert). The final cut must be re-judged on one stable bundle.
4. Ask 2 (chart) is not independently graded.

## Next action for the author
Run /fix-determinism. File the WHAT in the memo's test: expected 2027 retained claims are the best estimate of the employer's own future cost given how few members its three years rest on, naming no formula. Close the complement (trust level, no external benchmark) by a shipped sentence so the broker survey cannot flip CR104 or CR136. Then rebuild and re-judge once on the final zip.
