# determinism-check report, task231, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (etl_conformance for the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (one pass, sonnet, medium, scratch path only) executed the standard (section 4.2) and the register notes literally. The scope rule is filed: a firm that ceased on or before the frame date is out of scope whether or not the register shows it. The unseen ceased share is estimable from settled rounds, since the register's registration lag has a median of about 455 days. The call is unchanged for any share between about 13.9% and 22.7%. Every defensible estimate (15.3% filed, 14.9 to 15.7% across window and drop-rule variants, age-standardised 15.35%, region-specific shares) sits inside that band. Only censored shortcuts (all rounds 11.8 to 12.1%, last two years 7.5 to 7.8%, contact-centre CEAS only, no adjustment) fall outside, and the files expose each as an error.

Pack-version note: the judge worked on a copy made before the final rebuild. The rebuild applied the leak reader's realism fixes (December main closes moved to 23 December, manifest issue dates and owners, questionnaire sections). The call and all graded ask figures are unchanged. The settled-round counts moved from 7,493 of 48,920 to 7,494 of 48,978 (still 15.3%). I did not rerun the judge (one thread only). The independent verifier and figures_check pass on the current pack, and the rebuild moved the share by under 0.01 points, far inside the band.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Invited / returned by main close | 8,604 / 4,610 | 8,604 / 4,610 (17 repeat returns) | yes |
| Register-closed by 1 Sep | 24 | 24 | yes |
| Non-returners with no closure | 3,970 | 3,970 | yes |
| Settled-round share | 15.3% (now 7,494 of 48,978) | 7,493 / 48,920 = 15.32% on the pre-rebuild copy | yes (rebuilt counts differ by 1 and 58, same share; verifier passes) |
| Region rates at 15.3% | Capital and Harbour red; Islands and W Uplands amber; others green | Capital 48.7, Harbour 52.7, Islands 55.5, W Uplands 55.4, Border 58.7, others 60.4 to 61.4 | yes |
| Rejected route: register as it stands | five regions red | Capital, Harbour, Islands, Border, W Uplands red; others amber | yes |
| Rejected routes 12.1% / 7.8% | Islands and W Uplands red | Islands 54.6 / 53.4, W Uplands 54.5 / 53.3 | yes |
| Ask 3 firms reached (12 regions) | 454 ... 242 | all match | yes |
| Ask 3 calls placed (12 regions) | 1,359 ... 743 | all match (total 9,682; 10,071 without dedupe) | yes |
| Ask 4 June late returns and shares (12 regions) | 104/18.9% ... 47/10.8% | all match | yes |
| Ask 5 recruited / returned (9 groups) | 34/30 ... 107/99 | all match (returned only with returns restricted to 2026Q1 on) | yes |

## Competing answers that survived
None on the main call. Flip thresholds: Islands below 13.5%, Western Uplands below 13.8%, Border below 12.9%, Harbour above 22.7%, Capital above 34%. The filed 15.3% is inside every one.

Residual thinness (not an open fork): Islands and Western Uplands sit 0.4 to 0.5 points above 55%. A single-round share such as 2021Q1 (13.7%) would put Western Uplands at 54.96. The pooled estimate has a standard error under 0.2 points, and every pooled or standardised variant stays above the flip points.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | yes |
| Large file | 25,000 rows or more | outcomes 210,800 rows; call log 148,136 rows | yes |
| Distractors | 2 or more in metadata, none labelled by file name | BCS_regional_balances_2026_06.xlsx and BCS_questionnaire_2026.pdf named; no file name labels one | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh; none answers a graded quantity | the judge found neither needed; neither ranks the regions on the decision question; bcs_region_review_2023.csv is mapping material and not a distractor | yes |
| Deliverables | 1 to 3, each in the golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12-region and 9-group cuts; counts and shares to one decimal place stated in the prompt | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 10 (scorecard); design note counts 21 on the main side before 66 ask figures | yes |
| Reads as real | no LLM tells, goldens realistic | judge found no authoring language; the leak reader's realism fixes were applied after the judge's copy | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
The card has stump_class analytical, stump_strategy maturity_censoring, decisive_rule_filed false, official_decoy false and gate_g forecasting. The design note's decisive step is estimating the eligibility of unresolved non-respondents from settled earlier rounds.
These match. The thread did not name either declared distractor as the surface read carrying the task. Its rejected routes (register as it stands, pooled all-round share, last two years, call-centre resolved mix) are the card's analyst_test routes, and it reproduced their wrong answers (five-region extension; four-region extension with Border amber). The card's gate_g label "forecasting" is the note's label for the nowcast of eventual closures. The thread's finer label describes the same mechanism, so there is no mismatch.

Gate H: domain pass, layers pass, decisive_step analytical. The card's domain_test (AAPOR's e for unresolved eligibility, estimated from settled register closures) and the note's Three rules agree. The standard names the scope issue, so the work is estimating its size, which is analysis and not rule application.

## Stump power (Gate F)
The decisive trap is right-censoring of the register's closures. The two easy routes both file wrong answers: trust the register, or pool all earlier rounds. The standard states the scope rule openly, so a solver who notices it and then pools all rounds is the realistic failure. The asks add independent silent devices (duplicate call records, code 71, six-digit company numbers and old region codes, phone return timing, panel_id reuse, Rev 2.1 mapping, duplicate firm rows). A strong model has to model the lag and not just read the rule. The judge rated this likely not too easy. The portal remains the only stump evidence.

## Findings, ranked
1. None blocking.
2. Thin margin on Islands and Western Uplands (0.4 to 0.5 points above 55% at 15.3%). Clean under all pooled variants, but a single-round share is a possible dispute.
3. Optional wording for grading: the slide's bar heights depend on the 84.7% in-scope basis, and the answer list gives only colours, thresholds and title. State the basis and a tolerance if bar heights are graded.
4. Minor temporal nit, not decisive: the register notes say the extract holds records "at the end of 25 September 2026", while the manifest stamps extraction at 21:47Z that day. This was seen on the pre-rebuild copy and the manifest was revised afterward, so check it is still consistent.
5. The judge saw the pre-rebuild pack, so the realism edits were never read by it.

## Next action for the author
Proceed to ship step 5 with no repair. Optionally record the 84.7% basis and tolerance for the slide's bar heights.
