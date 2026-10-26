# determinism-check report, task270, 2026-10-26 (round 1, pack md5 37e03fa7e6a4094e0b53333e118d8a53)

## Verdict
NOT_DETERMINISTIC
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Standard 2.2 and 2.3 file "the change's effect on the candidate" and "on six-month retention" and an effect as the difference a change makes to a metric's mean. Executed word for word on the scorecards (treatment mean less control mean) the correlations are first purchase 0.29, sessions 0.39, active days 0.23, items saved 0.10, push opens 0.09: the literal winner is sessions, not the golden's first purchase. The golden (0.54, 0.31, 0.14, 0.02, -0.09) holds only under a shared-sampling-error correction (mean covariance and variances taken out, covariance from the holdout's user-level correlations) that no shipped file states. A covariance-only correction gives 0.36, 0.19, 0.09, 0.01, -0.06, so the two-decimal figures are estimator-specific. Second fork: the forecast figure's unit (weekly total repeated on each day, against a daily figure) is stated nowhere; read per day, users per arm are about 7 times larger. Minor: the cohort refresh rule (latest row replaces earlier; otherwise H2 is 1.73 pp not 1.69 pp), the 2.80 multiplier (exact z gives the same three decimals), and the closing cutoff (winner stable).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Population | 399 experiments, 489 changes | 399, 489 | Yes |
| Correlations | 0.54 / 0.31 / 0.14 / 0.02 / -0.09 | 0.536 / 0.312 / 0.137 / 0.024 / -0.093 under the unfiled correction; literal 0.29 / 0.39 / 0.10 / 0.09 / 0.23 | Only under the unfiled method |
| Calendar users per arm (all 7), MDEs | OB-27-001 24,786 etc. | same under weekly-total reading; 173,501 per day reading | Yes, one reading |
| 2025 holdout read | H1, H2 rows | same with latest-refresh rule | Yes, with an unfiled rule |

## Competing answers that survived
1. Raw against shared-noise-corrected effects: sessions (0.39) against first purchase (0.54); also 0.54 against 0.36 for first purchase across licensed estimators. Closing rule: none shipped.
2. Forecast unit: weekly total against daily figure; users per arm 24,786 against about 173,501.
3. Minor: cohort refresh replacement; 2.80 against 2.8016 (same result); closing cutoff.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 13 files, 5 formats (csv, yaml, pdf, txt, xlsx), holdout 31,584 rows | Yes |
| Distractors | 2+ in metadata, none named by file name | app_store_ratings_2024_2026.csv, acquisition_spend_2026.xlsx; unused, per judge | Yes |
| Distractors relevant enough to weigh, ruled out by a shipped fact | yes | Not tested in round 1 (judge reports them unused) | Not verified |
| Deliverables | 1 to 3 | 2 (pptx, xlsx) | Yes |
| Asks stating unit and rounding | yes | Prompt states rounding and units | Yes |
| Rubric 25+ criteria, prompt shape | yes | Shape 01 per design note; count not generated yet | Not verified |
| Reads as real work product | yes | Judge saw no leakage or generated-looking text | Yes |

## Gate G reconciliation
Judge: Gate G not raised; no shipped artifact ranks the candidates wrongly; declared distractors are unused and are not the surface read. The surface read is the analyst's own raw correlation (sessions), which is the design note's default path. Judge mechanism (errors-in-variables / shared-sampling-covariance correction) matches the design note's stump (sampling covariance of two effects on the same users, taken out). Match on mechanism, family and Gate H. The mismatch is on determinism only: the note says the standard files the estimand and not the method, but the shipped wording does not file that the correlation is between true effects.

Gate H: domain pass (surrogate or proxy-metric validation), layers pass, decisive_step analytical. Agrees with the note's Three rules, with the caveat that the stump is credited only after the estimand is filed.

## Stump power (Gate F)
Strong if the estimand is closed: the raw route picks sessions, a strong model stopping at raw correlation is stumped. As filed, the failures would be a fork, not a clean analytical error. The corrected method is the field's standard trial-level surrogacy approach; whether a strong solver reaches it is for the scored readers.

## Findings, ranked
1. Estimand unfiled: raw effects against true effects net of shared sampling error (Gates C, E; underspecified_objective).
2. Estimator-specific two-decimal figures (0.54 against 0.36).
3. Forecast unit unfiled.
4. Cohort refresh rule unfiled.

## Next action for the author
File the WHAT in standard 2.3 (the correlation between the changes' effects themselves, net of the sampling error their two measures share), the forecast's weekly unit and the cohort refresh rule, then recut and re-judge once; test that the winner and two-decimal figures hold across licensed estimators.
