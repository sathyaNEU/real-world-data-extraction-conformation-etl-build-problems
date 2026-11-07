# determinism-check report, task306, 2026-10-31 (architecture 3, target.zip sha256 9e435efb...e3be8 after the PDF-wrap rebuild)

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (the solution blocks disagree on the word "worth")
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Costing storms by incurred over hindcast by gap class (within 24 days of the storm before: 1.62; others 0.98) gives 113 / 94 / 87, release 7, margin 0.7. One pooled ratio (1.06) gives 94 / 76 / 71, release 5, and rejects the cover. The call and all capital figures hold under every reasonable variant (gap cut 24 to 70, sums/mean/median). Defect: FINAL_RECOMMENDATION and step 8 state the worth as 0.8 (12% of the release, 0.1 "added"), while Deliverable ask 4 and the xlsx description state 0.1. The prompt's "its worth to us a year" and CP-04 s3 license both.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Close / other ratio | 1.62 / 0.98 | 1.615 / 0.9755 | yes |
| 1-in-200 gross / net A / net A+B | 113 / 94 / 87 | 113.31 / 94.37 / 87.47 | yes |
| Release | 7 | 6.90 | yes |
| Margin | 0.7 | 0.697 | yes |
| Worth net of margin | 0.1 | 0.131 (capped); 0.162 if the one-reinstatement cap is ignored (prints 0.2) | yes, with cap |
| 2026 occurrences home/farm | 13,067,000/2,510,000; 16,898,000/3,541,000; 3,943,000/931,000 | within 1k of each | yes |
| Expiring recovery / RP | 12,015,000 / 1,402,000 | 12,015,394 / 1,401,796 | yes |
| Farm SI by county (£m) | C 1302.1/618.2, D 1502.4/746.3, S 863.7/396.8, Do 389.0/184.3 | 1302.06/618.16, 1502.44/746.26, 863.67/396.77, 388.98/184.27 | yes |

## Competing answers that survived
1. "Worth": 0.8 (12% of release) or 0.1 (net of margin). Prompt and CP-04 s3 permit both; the blocks split. Closing sentence needed in the prompt.
2. Ask 7 coinsurance share applied to whole policy (golden) or only the matched holding (Cornwall 1420.1/671.3, Devon 1628.9/815.9, Somerset 955.6/437.3, Dorset 449.6/212.1). No file states the policy-wide reading. Minor, pinnable.
3. One-reinstatement aggregate cap on cover B: ignoring it prints worth 0.2. The wording says one full reinstatement, so the cap is literal; the working should state it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / 4 (csv, xlsx, pdf, eml) | yes |
| Large file | 25,000 rows | home_policies 46,741 rows | yes |
| Distractors | 2+ named, none labelled in a file name | 3 named in metadata.json (flood YLT, panel security, home policies); no file name labels one | yes |
| Distractor weighs but is unused | yes | flood YLT excluded by CP-04 s1 (flood under CP-05); home policies and panel security unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | closing sentence states unit and rounding for each | yes |
| Prompt | one paragraph, under 1,000 chars | 983 chars | yes |
| Rubric 25+ criteria; prompt shape | identifiable | shape "other"; the rubric is generated and was not inspected here | not checked |
| Reads as real work product | yes | judge found no authoring disclosure; golden realism not re-read | yes (judge) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: stump is the pooled model-adjustment factor against the gap-class split; no decoy, declared distractors are unrelated to the call. Match. The thread names no declared distractor as the surface read. Gate H: domain pass, layers pass, decisive_step analytical, agreeing with the note's Three rules. The thread's reflex (one pooled ratio, 94/76/71, do not add) equals the note's rung 1 (release 5, worth minus 0.3), so no mismatch.

## Stump power (Gate F)
Good on paper. The pooled ratio is the field's standard model adjustment factor and files the wrong call. The right route needs a join across two files with no shared ID and testing the right covariate (gap to the previous storm, not season or rank). The thread flags that it depends on the solver testing that covariate; the main thread weighs this against the note's ladder (rank and season routes are refuted by quiet-season later storms). Asks carry independent devices.

## Findings, ranked
1. "Worth" inconsistency: the Final Recommendation and step 8 give 0.8, ask 4 and the xlsx give 0.1. Fix: align the blocks to "worth 0.1, being 12% of the release (0.8) less the margin (0.7)" and pin the prompt as "its net worth to us a year, after the margin". The design note already treats worth as 0.1.
2. Cover B one-reinstatement cap is not stated in the working; ignoring it prints 0.2. Fix: state the cap in step 4 or 5 and in the xlsx.
3. Ask 7 policy-wide coinsurance share is unpinned. Fix: phrase it "our share of each farm policy's sums insured".

## Next action for the author
Edit the Final Recommendation, step 8 and prompt.txt as in finding 1 (with finding 2 and 3 pins), rebuild and re-verify, then re-judge once. The prompt change is a pin only; no data or ladder change.
