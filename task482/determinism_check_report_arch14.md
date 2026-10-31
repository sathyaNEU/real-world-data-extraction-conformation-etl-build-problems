# determinism-check report, task482, 2026-10-25 (run v14r2, target.zip md5 04486b1a81d00b944db10cafed3d5a1c)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The estimand (final 2026 attribution, capped TCOC per member month, 98 per cent of the 1.052-trended 2025 benchmark) is filed in the Standard and Resolution. The projection method is not filed, but every implementation variant the judge ran gives the same 8 entrants and 5 one-sided practices. Judge thread: one pass, sonnet, medium, isolated to a fresh unzip. Full verdict: /tmp/determinism-check-task482-v14r2/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Mallowcrest threshold | 179.67 | 179.6732 | yes |
| Garrowdale threshold | 454.16 | 454.1614 | yes |
| Members in running stay past cap | 7 (3 + 4) | 7 (PG-183652-03/-04/-05; PG-533674-01..04) | yes |
| Interim-measure entrants | 3 (Ostrelwood, Thornelfield, Jesselford) | same | yes |
| Carried by 2025 run-out alone | 10 under | 10 under | yes |
| Carried plus stays at cap | 8 entrants | 8; ratios 0.905 to 0.961 entrants, 1.049 to 1.057 non-entrants | yes |
| Level-5 shares, all 13 | 18.6 ... 16.5 | exact match | yes |
| Attribution replica | n/a | 100 per cent match, final 2025 (24,835 members) and Oct 2026 runs (21,171) | yes |

## Competing answers that survived
- Interim measure as filed: 3 entrants. Not licensed: it does not project to the final attribution. Closed by the prompt ("projected to the payers' final 2026 attribution").
- Network-wide flat carry factor (0.877): Wexelmoor and Haddelcrest in, Callowglen out. Data separate it: practice factors are stable (split-half r 0.82) and range 0.82 to 0.99; "each practice's ... projected" excludes the flat factor.
- Level-5 shares, literal amount-matcher reading a halved Merrinlake 99215 as level 3: shifts shares 0.2 to 0.8 points (Ostrelwood 17.8, Haddelcrest 17.7, Prestelglen 19.2). Counting at billed level ignoring the Kesselcrest line: 20.3, 20.5, 21.6. The golden is the only reading that classifies every claim uniformly (a halved 99214 at 66.75 matches no level), but the Merrinlake modifier-25 halving is not stated in any shipped file. Residual risk on the asks only, not on the call; the author describes it as the ask's silent device.
- Stay comparator: only a closed 28-day rev-0120 stay (1,571 a day) as ICU comparator breaks the call; judged not a reasonable comparator.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 23 | yes |
| Formats | 3 or more | 5 (csv, txt, xlsx, json, pdf) | yes |
| Large file | 25,000 rows or large DB | KBP claims 159,442 rows; mlh claims 283,414 | yes |
| Distractors in metadata.json | 2 or more, none labelled by file name | 5 named (MA attribution, quality composite, two remittance files, pmh CCF payments); names carry no distractor label | yes |
| Distractors unused yet weighable | yes | judge also found settlement PDF (payer caps 100k/150k/200k vs Standard 250k) and MPI relevant and unused | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png), both in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 13 practices x level-5 share, "per cent to one decimal" | yes |
| Prompt shape, 25 or more criteria | yes | 13 elections + 13 shares + components + chart exceeds 25 (not generated here; counted from graded items) | yes |
| Not LLM-generated / real work product | yes | judge saw no generator text; goldens not opened by me beyond listing | yes (judge basis) |

## Gate G reconciliation
Judge: mechanism forecasting; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Design note: estimation_fit, a censored year; default path (own run-out) enters ten, stays at cap gives eight; nothing planted. Match. No shipped artifact ranks the candidates wrongly; the declared distractors are not named as the surface read carrying the task (the judge named the interim measure and run-out as the easy routes, which are the analyst's own computations, not shipped answers). Gate G: pass.

## Stump power (Gate F)
Good. The decisive discovery (a hospital bills at discharge, so a running stay appears only as daily professional visits and is absent from feeds and from completion factors that exclude claims over USD 100k) is visible but unstated. Easy routes fail (3 and 10 entrants). Risk is that it is hard to find, not that it is guessable. The decisive step is a method call the main thread should weigh with scored readers; it is not a plain textbook method applied mechanically.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the design note's Three rules (domain, Layer 1 mess, Layer 2 censoring, analyst test ending on ten practices).

## Findings, ranked
1. Level-5 asks rest on an unstated Merrinlake modifier-25 payer rule (halving beside a minor procedure, never beside preventive). Data-forced but not filed; shares can shift 0.2 to 0.8 points under the literal amount-match reading. Optional: file the WHAT in the ask ("a claim paid reduced by a payer line to a lower level's rate is paid at that lower level"); do not file the Merrinlake rule. Not blocking.
2. Margin on the call is thin: nearest non-entrants (Wexelmoor 1.049, Haddelcrest 1.053) about 5 per cent over, nearest entrants 5 to 6 per cent under, about 1.5 to 2 standard errors of the carry factor. All variants agree. Not blocking.
3. Minor stale-figure observation: the design note's readability screen lists thresholds 179.75 (Mallowcrest) and 454.47 (Garrowdale), while submission.md and the judge's recompute give 179.67 and 454.16. Submission and bundle agree; the note looks stale. No effect on the verdict.
4. Optional: state in the solution blocks that the stay estimate is robust to comparator and denominator choice (every variant crosses 1.0: Mallowcrest 1.12 to 1.24, Garrowdale 1.13 to 1.15).
5. No cross-batch comparison was made (bundle only).

## Next action for the author
None required to proceed to ship; optionally tighten the level-5 ask wording per finding 1.
