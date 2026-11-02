# determinism-check report (pass 2), task475, 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Scope: target.zip sha256 prefix 5d16182359536da0, fresh unzip at /tmp/determinism-check-task475-p2-144228/target/, one sonnet/medium thread (scratch-only, Bash, no server tools). Verdict file: /tmp/determinism-check-task475-p2-144228/verdict.md. Pass 1 is untouched.

## Why
Every committed figure reproduced from the shipped files: the main call (no county at the 12 per cent cap, Tallis 11.46 per cent, $2,292,000), all 14 counties for returns, shares and allocations, and all 14 values of each re-sited supplementary ask. Policy rev4 (3.1, 4.1, 4.2, 5.1 to 5.3, 6.1), DOR Table 2, the closeout and the data dictionary pin the population, vintage, crosswalk rule, P.O. Box fallback, exclusions, rounding, first-COMPLETED rule and funded-by-grants definition. The re-sited devices (funding codes on the job export; the July 2025 move renumbering jobs) are closed by files: ledger FUND column and closeout definition for Ask A, and the MOVED conversion notes plus invoice service month for Ask B, with the mapping verified by 100 per cent agency and opening-date agreement.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Childless avg credit, first class (DOR Table 2) | $394.88 | 56,022/141,872 = 394.88 | yes |
| With-children avg credit | $4,723.49 | 4,723.487 | yes |
| Fourteen-county returns with children | 54,712.6 | 54,712.6 | yes |
| Tallis returns / share / allocation | 6,270.1 / 11.46% / $2,292,000 | same | yes |
| Other 13 counties, returns, shares, allocations | per submission | match exactly | yes |
| All-credit-returns route, Tallis | 16.54% | 16.54% | yes |
| Statewide-share route, Tallis | 15.46% | not rerun separately (same method) | partial |
| Ask A dwellings, 14 counties | 352,113,135,81,200,212,57,114,129,131,78,176,180,51 | identical | yes |
| Ask B spending, 14 counties | 1,653,025 ... 308,925 | identical; total $10,892,452.88 equals closeout job categories | yes |

## Competing answers that survived
None. Tested and visibly non-golden: funding-code-only for Ask A (349,111,134,78,...); export COMPLETED_DATE (349,109,134,84,...); unmapped job-number join for Ask B (about 20 to 24 per cent agency agreement). Minor note: the implicit mapping of DOR's first three classes to IRS AGI_STUB 1 is exact (same under-$25,000 range) and the derived childless average reproduces the table.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt | yes |
| Large file | 25,000 rows or more | status history 28,588 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | TY2022 IRS extract, county-to-ZIP relationship xlsx; neither named as a distractor in a file name | yes |
| Distractor quality | unused, weighable, ruled out by a shipped fact | TY2022 gives a different answer, ruled out by policy 3.1 (latest published year); county-to-ZIP direction ruled out by the policy's ZIP-to-county sharing. (The judge also listed the data dictionary as a distractor; it is not declared, and that is not a defect.) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 14-county grids, units and rounding in the prompt | yes |
| Prompt shape, 25+ criteria | identifiable, 25 or more | per-county grids for counts, shares, allocations, dwellings, spending (70+ gradable figures) | yes |
| Reads as real | clean | judge found no authoring language; dictionary mildly over-explanatory | yes |

## Gate G reconciliation
Thread: mechanism etl_conformance / method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; stump sentence is the statewide share of claimants with children applied to every county, which caps Tallis at 12 per cent; nothing planted. Match. Neither declared distractor is named as the surface read carrying the task; the competing routes found (statewide share, all credit returns) are method choices, not shipped wrong rankings. Gate G: pass, no shipped artifact ranks candidates wrongly.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card and note's Three rules: no decoy, not semantics, not rule application, analyst_test on clean truth (statewide share caps Tallis). Match.

## Stump power (Gate F)
Judge rates it good: the uniform statewide share or all credit returns put Tallis over the cap; only the per-ZIP decomposition from each ZIP's own credit amount leaves it at 11.46 per cent. Note for the main thread: with the two statewide averages filed in DOR Table 2, the per-ZIP split is a two-equation solve a strong solver can reach, so the call is a textbook route (stumping 1.3); weigh against the scored readers' result. The re-sited Ask A/B devices (tract versus entered county, funding-code gaps, job renumbering at the move) are where the thread expects a strong model to slip in at least one county.

## Findings, ranked
1. None blocking.
2. Minor: Ask A relies on the closeout definition and ledger FUND column to derive that the previous system kept one funding code per job; the sentence is not verbatim in the dictionary. Derivable, not a fork.
3. Minor: statewide-share 15.46 per cent route not separately rerun by the thread.

## Next action for the author
Proceed to ship; no repair needed.
