# determinism-check report, task237, 2026-10-17 (pass r3)

History: r1 (first build) DETERMINISTIC, APPROVE, one optional note (block 4 chart line described a wording-factor marking the prompt never asks for; trimmed). r2 (after realism fixes to ages and version levels) DETERMINISTIC, APPROVE, two cosmetic notes (prompt "send back for retranslation" against the standard's "Rework", now "rework for retranslation"; CSV row order, ungraded). Since r2 the generator added CAPI cases revisited after a break-off inside the module, smoothed ages, redrew long online durations and lowered the Urdu loadings; four CAPI counts and the means changed, the ten decisions did not.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
TAS-4 s.4 to s.6 fix the population (valid completes who answered all twelve items), the scoring, the quantity (share of total-score variance due to differences in connectedness, unrounded) and the bands at 0.70 and 0.80. Executed literally with the wording factor separated, all ten decisions, ten valid-complete counts and ten means reproduce. Every separation of the wording factor the thread tried (bifactor, correlated residuals, method factors on both item sets) gives the same ten decisions; the nearest margin to a band is about 0.045 (Tagalog 0.748, Cantonese 0.649 in the alternative model). Population variants (UTC window, ignored merges, ignored language switch, complete-only status) change counts, but the filed s.4 wording leaves a single reading, so these are closed by the filing, not forks.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Valid completes pa, zh-Hans, yue, tl, ar, es, ur, vi, fa, ko | 542, 606, 489, 450, 569, 622, 478, 512, 490, 573 | same | yes (ncp export, register, ledger; flr long, back-check log) |
| Online total / interviewer total | 3,253 / 2,078 | same | yes |
| Pilot means | 41.76, 39.18, 38.29, 38.36, 39.53, 41.47, 38.46, 39.04, 40.23, 36.89 | same | yes |
| Answered-all-twelve n | 395 to 557 | same | yes |
| Omega hierarchical | bands: pa/es/fa >= 0.80; zh/tl/ar/ko 0.70 to 0.80; yue/ur/vi < 0.70 | 0.855, 0.754, 0.534, 0.748, 0.754, 0.881, 0.591, 0.543, 0.888, 0.752 | yes |
| Alpha, easy route | 0.85 to 0.87 (five versions), Cantonese lower | 0.85 to 0.87; yue 0.755 | yes |
| Single-factor fit | holds in pa, es, ur, fa; fails in six | p .78, .92, .049, .67; p<.001 in the six | yes (Urdu borderline on the absolute test; decision unchanged, omega 0.597 vs 0.591) |

## Competing answers that survived
None. Alpha, single-factor omega and omega total release zh, tl, ar, vi, ko and hold yue, but they count the wording factor as connectedness, against s.6, so they are the intended wrong route. Positive items alone give a different wrong split. The model is not named in the standard, but the data separate the candidates and every defensible separation files the same decisions.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 (judge counted 11) | yes |
| Formats | 3+ | csv, xlsx, pdf, md | yes |
| Large file | 25,000+ rows | flr long, 39,298 rows | yes |
| Distractors | 2+ in metadata.json, none named by file | ncp_paradata, ccs_wave5 results; names do not label them | yes |
| Distractor role | unused, weighs, ruled out by a shipped fact | thread found no new decisive content in either; neither ranks versions | yes |
| Deliverables | 1 to 3, all in golden | 2 (csv, png), both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | ten versions x decision, count, mean; "two decimal places" | yes |
| Prompt shape / rubric | identifiable, 25+ | shape 07, 37 criteria per metadata | yes |
| Reads as real | no LLM tells | README and dictionary plain in-fiction notes | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: field_method, decomposition_attribution-style analytical stump, no planted defect, no certified replay. These agree. Neither declared distractor carries the call. No mismatch.
Gate H: thread domain pass, layers pass, decisive_step analytical; design note's decisive step (bifactor omega hierarchical vs alpha) and Layer 1 list (Eastern vs UTC, merged accounts, back-check, language switches) match. I checked the design note and metadata.json only after the verdict returned.

## Stump power (Gate F)
Strong. After clean data and correct rules, alpha or single-factor omega gets five of ten decisions wrong (Cantonese is held rather than reworked; Urdu stays rework). The thread judged a strong model likely to fall to the alpha route.

## Findings, ranked
1. Post-verdict edit, no re-judge: after the verdict the author reworded the submission to say the wording factor adds nothing in the Punjabi, Spanish, Urdu and Persian versions (one-factor against bifactor test, p 0.37 to 0.71), answering the Urdu p = .049 point. The judge recomputed the single-factor chi-square (Urdu p .049), not that test; the p range is unchecked here. No figure, decision or file under target/ changed (target.zip sha256 038c7375..., figures_check 44 of 44, 114 generator checks and verifier green, per the author). Step 5 of submission.md has the new wording; critical component 1 (line 16) still reads "they share none". Both are consistent with the decisions; align the wording if intended.
2. Urdu single-factor fit sits at p = .049; decision unchanged either way. Not a finding against the call.
3. Judge counted 11 files, bundle has 12; no effect.

## Next action for the author
Make critical component 1 match step 5 ("adds nothing") if that was intended, then ship; no regenerate needed.
