# determinism-check report, task239, 2027-10-17 (run date 2026-10-17)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (sonnet, medium) read only a fresh unzip of target.zip and the extracted blocks. Executing WI-SV-03 sections 3 to 5, the dashboard methodology and the data dictionary word for word reproduces every committed answer. The standard's 4.1 files the team level as the score a member is expected to give, so the factor is fitted to latent team levels (between-team covariance less pooled within-team covariance): TC01 to TC10 load 0.80 or more, TC11 and TC12 under 0.25, ten items stay. A factor on observed team means keeps eight; a person-level factor keeps none.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Returns that count | 11,482 | 11,482 | yes |
| Reported teams / returns used | 1,016 / 8,323 | 1,016 / 8,323 | yes |
| Personal link count/outside/more unanswered/used | 7,793/1,156/929/5,708 | same | yes |
| Site tablet | 1,975/314/215/1,446 | same | yes |
| Paper form | 1,714/290/255/1,169 | same | yes |
| TC01 to TC12 answers/favourable | per submission | all 12 same | yes |
| Six divisions, teams/returns | 228/1,821; 149/1,309; 103/781; 148/1,140; 245/2,060; 143/1,212 | same | yes |
| Loadings TC01-10 >= 0.80, TC11-12 < 0.25 | bands | 0.885 to 0.936; -0.02 | yes |
| Observed-means factor keeps 8 (TC09/10 about 0.58) | stated in rationale | 8 | yes |
| "Correcting means for unreliability gives TC09/TC10 withdrawn" | stated in rationale | judge's noise-correcting estimators all keep 10 | NOT reproduced (see findings) |

## Competing answers that survived
None moves the decision. Counts-level forks (below) are the residue:
1. Reused codes of five split teams (DO-111, DO-154, EN-229, HO-228, HO-829): golden reads personal links as September codes, tablets before the 13 September reload and paper as July codes. Data confirm the timing but no document states it. Alternative reads move asks 2 and 4 (tablet-as-itself: 1,017 teams, 298 tablets outside, 1,461 used; personal-via-map: 1,012 teams, 1,180 outside, 5,684 used).
2. 14 teams with division_since exactly 2027-09-01: golden counts them in the new division (methodology defers only moves "after"); other reading gives Delivery 237/2,005, Corporate 151/1,267. Wording favours the golden.
3. "Loadings to two decimal places": golden commits bands only; two-decimal values differ by unbiased estimator (TC01 0.91 or 0.88). Decisions identical.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 15 / 5 (csv, pdf, docx, xlsx, md) / 219,652 rows | yes |
| Distractors in metadata.json, none in a file name | 2+ | staff_in_post and sv26_dashboard_items named; names do not label them | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | give percent favourable or headcount only, tie to nothing graded | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | channel x 4 counts, item x 2, division x 2; loadings 2 dp stated; counts are integers | yes |
| Prompt shape, rubric 25+ | yes | shape 10; design note puts criteria at 63 | yes |
| Reads as real, not LLM generated | yes | judge found nothing exclusion-level; synthetic team names tolerable | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; the easy path (one factor on team means) lands on eight items, golden ten from between-team covariance net of pooled within. Match. The declared distractors (staff in post, 2026 items) are not the surface read carrying the task. Gate G: PASS.

## Stump power (Gate F)
Good. The routine routes (observed-means factor, 8 kept; person-level factor, 0 kept) are wrong; only a measurement-error-corrected team-level factor gives 10. Section 4.1 hints but does not name the method. Supplementary counts add attrition risk through the channel, code and time rules.

Gate H: domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test (a strong analyst who reads every rule right still files eight).

## Findings, ranked
1. (Rationale vs recomputation, low) The Final Recommendation says correcting team means "for their unreliability" gives ten items with TC09/TC10 withdrawn, and the card's analyst_test says the same route still withdraws the practice items. The judge's mean-team-size-corrected estimator instead keeps ten (TC09 0.84, TC10 0.81, TC11 0.07). Unless the author's disattenuation is a specific variant, the sentence misdescribes a wrong route. Decision unaffected, but fix the sentence or show the variant so a reviewer who tries a correction is not told it fails.
2. (Inference risk, low) Reused-code placement is not stated in any document; asks 2 and 4 carry a small inference risk. Optional fix: one sentence in a shipped document that the tablets' pre-13 September list and the paper packs' printed codes are the July list and invitations were loaded in September.
3. (Low) Boundary-date moves (14 teams on exactly 1 September) rest on "after" wording only.
4. (Low) Golden commits bands, not two-decimal loadings, against a prompt asking two decimals. Record values under the stated estimator or treat bands as the grading form.

## Next action for the author
Reconcile finding 1 (edit the rationale sentence or document the disattenuation variant); optionally add the one clarifying sentence for finding 2. No rerun of the judge is needed.
