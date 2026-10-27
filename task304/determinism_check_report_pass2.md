# determinism-check report, task304, pass 2, 2026-10-27

Zip: target.zip sha256 57a875af8fc619d4b8e1ad5bf1de4042dbb7b9f52849dd0c73e0976a88c1215d. Judge thread: one pass, verdict at /tmp/determinism-check-task304-1793082100/verdict.md (spawned by the coordinator because this runtime has no Agent tool). Earlier report determinism_check_report.md (zip 5194480e) is untouched.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The files force First-time buyer 2019-21. Every term-aware variant of the 2027 first-entry forecast gives it 8.0 to 9.7 possessions avoided (rounds to 10). High LTV 2022-24 is next at 3.2 to 4.9 ("fewer than 5"). High LTV leads only when the term-increase state is dropped, which the shipped history refutes (hazard about 1% a month from month 8 after an extension against 0.15% for never-extended accounts). All workbook and critical-component figures reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Orders made or varied (FTB, HLTV, SO) | 34, 71, 9 | 34, 71, 9 | yes |
| Suspended on terms | 27, 56, 9 | 27, 56, 9 | yes |
| Open claims 30 Sep 2026 | 17, 43, 2 | 17, 43, 2 | yes |
| Possessions sold | 20, 24, 4 | 20, 24, 4 | yes |
| Sold at a loss | 7, 24, 2 | 7, 24, 2 | yes |
| Average loss | 4,500; 33,300; 3,300 | 4,495; 33,327; 3,314 | yes (rounded) |
| CC1 term raised 2026 | 7,129 of 16,455; median 10 yrs; 10% vs 26% | same (9.9 yrs, 9.8%, 25.9%) | yes |
| CC2 2024 raised | 347; 4 within eight month ends; 81 later | same | yes |
| Planning rates | 4.5, 7.4, 1.9, 10.7 | 4.50, 7.39, 1.94, 10.65 | yes |
| Avoided 2027 | FTB 10; others under 5 | FTB 8.7 as specified (8.0 to 9.7 across variants); HLTV 4.5 (3.2 to 4.9); SO 0.6; BTL 1.2 | yes |

## Competing answers that survived
None on the main call. High LTV first needs the term state dropped or the payment rise read as the risk (refuted by the history). Pooling books makes BTL next best at 3.7, not a defensible method. Ask forks, all pinned by data or policy but undocumented as such: resent order lines (K8HD9926 gives HLTV open 44 if not dropped), debt summed over register loan parts (one row gives FTB 5 losses at 3,458), book taken from the history, average over all sold including nil losses (loss-making-only would be 12,842). The judge ruled each inferable; they sit on the asks, which are free of the rule.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 13 files; csv, parquet, pdf, xlsx; history 4,260,553 rows | yes |
| Distractors named, none labelled in a file name | 2+ | metadata names house price index, contact centre volumes, board risk appetite, rate card (4); none in a name | yes |
| Distractors unused, weigh, ruled out | yes | unused by the solution; none reproduces a graded quantity; judge found no hand-over | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/; no format family required | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-book multi-cut asks; unit and rounding in the prompt (nearest ten, nearest hundred pounds) | yes |
| Prompt shape, rubric 25+ criteria | yes | shape identifiable (book choice plus caseload and loss tables); the rubric count is not checkable from the folder, author reports precut 52/0/0 | yes, on the author's precut |
| Not LLM generated, goldens real work products | yes | judge found no authoring leakage; golden realism not re-read here | yes (judge) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, analyst_test is the roll-rate chain on book, current arrears and payment rise that files High LTV first and misses the term-extended first-time buyers; design note stump sentence is the same trap. These match. The declared distractors (house price index, contact centre volumes, board risk statement, rate card) are not named as the surface read; the thread names the trailing-arrears roll-rate chain, not a distractor. Gate H: thread domain pass, layers pass, decisive_step analytical; design note Three rules (collections arrears-entry hazard with forbearance as a state, Layer 1 resent months and dash-variant codes, Layer 2 hazard by months since concession) agree. Minor drift: the design note and card give the easy-route figures as FTB 2.9 / HLTV 4.5 (card 9.0 for the golden), while the judge's own chain gives FTB about 2.1 on the trap and 8.7 on the golden. Both put High LTV first on the trap and FTB first with the term state, so it is not a mismatch.

## Stump power (Gate F)
Plausible stump. The trailing numbers are correct and a strong analyst's roll-rate chain files High LTV (about 4.5) over FTB (about 2). Only a months-since-extension state, recognising the 2026 cohort has not yet reached its risk window and validated on the earlier 2024 cohort, flips it. The judge classes this analytical (forecast with a censored lag). The method is a textbook organ, so the blind readers' result should weigh it; no solver or scored reader runs on this build under the STOP block.

## Findings, ranked
1. Thin boundary: High LTV unrounded sits 0.1 to 0.7 under the "5" line in every variant (3.2 to 4.9); no variant crossed. Its nearest-ten value is 0, so "fewer than 5" is consistent but close. Optional wording: "0 at the nearest ten (about 4 to 5 unrounded)".
2. Ask conventions (resent order lines, loan-part debt summing, book from history) are inferable but not written in any shipped file. Optional: record as Layer-1 mess in metadata.json.
3. litigation_open_claims_2023-01_to_2026-09.csv starts at 2022-02-12, so the name understates its span. Not stump-affecting.
4. The judge called the pilot report a distractor, but metadata lists it as a context artifact. Not a defect.

## Next action for the author
No repair is needed. Proceed with the ship steps for zip 57a875af. Optionally add the two wording and metadata notes above, which do not touch the cut pack.
