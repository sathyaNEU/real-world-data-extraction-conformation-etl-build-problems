# determinism-check report, task125, pass 2, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: decomposition_attribution (with rotation-panel carry-through), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated judge thread (verdict at /tmp/determinism-check-task125-1791796196/verdict.md) recomputed every graded figure from the rebuilt bundle. The three methods-note additions since pass 1 (visit identity by serial and visit number, section 6 flows, section 7 rounding) closed the forks that sat in the asks. The main call is closed by methods note sections 1, 4 and 5.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Published unemployment Q2 / Q3 2026 | 4.99 / 5.27 (rise 0.27) | 4.9946 / 5.2664 | yes |
| Published employment Q2 / Q3 2026 | 60.01 / 59.36 (-0.65) | 60.0126 / 59.3613 | yes |
| Unemployment gap, 5 quarters | 0.22, 0.37, 0.25, 0.19, 0.07 | 0.2227, 0.3731, 0.2535, 0.1905, 0.0705 | yes |
| Employment gap, 5 quarters | -0.74, -1.37, -1.11, -0.93, -0.63 | -0.7392, -1.3733, -1.1090, -0.9317, -0.6309 | yes |
| Without-cap Q3 rates | 5.04 / 60.10 | 5.0437 / 60.1005 | yes |
| First-interview visits by region | 3,945 / 2,360 / 1,856 / 1,737 / 1,469 / 1,212 | same (after dropping 369 duplicate serial-visit rows) | yes |
| Flow shares | 30.77 / 30.58 / 35.45 / 39.22 / 28.72 / 27.14 | same (72/234 ... 19/70) | yes |
| Weekly hours, thousands | 27,055.5 / 16,009.7 / 12,455.6 / 11,070.1 / 9,858.6 / 8,103.1 | same; hh.mm conversion also reproduces the Q2 release total 85,762.5 | yes |

Nearest rounding margins are 0.0015 (Jan-Mar 2027 unemployment) and 0.0033 (Apr-Jun 2027 employment), clean against raking tolerance.

## Competing answers that survived
None on the main call. Three forks recorded as closed by filed text, residual risk low:
- Flow denominator: all Q2 unemployed would give VEL 24.00 and so on; methods note section 6 ("not interviewed in the second quarter are left out") picks the matched base. The prompt does not say "flow", so a mild reading risk remains.
- Match key: person_no instead of sex plus date of birth gives different counts (VEL 86 vs 72); section 6 says matched person to person and the data separate the candidates.
- Published Q2 rate: release table 5.0 against 4.99 from file weights; two decimals asked.
Alternatives tested and ruled out by the note: no re-rake (0.24, 0.41, 0.29, 0.23, 0.10), all waves capped (0.65), wave-1 only, target-quarter controls (identical to four decimals).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | 6 (csv, json, md, parquet, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | parquet 491,673 rows; call records 182,297 | yes |
| Distractors | 2 or more in metadata.json, not in file names | jobseeker claimants, field staffing json; no file name labels one | yes |
| Distractor weighs but does not answer | unused, relevant, ruled out by a shipped fact | claimant series is flat Q2 to Q3 (about 159.8k to 158.7k), consistent with the cap reading and answers no graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | region x measure asks, rounding stated in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25 or more | shape 02; about 48 golden figures per the leak reader; prompt 997 characters | yes |
| Reads as real, no LLM tell | yes | judge found no authoring leakage; no em dashes in submission.md | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H line: domain pass, layers pass, decisive_step analytical.
Design note and card: stump_class analytical; the default path (wave-1 gap while the cap runs, zero from January 2027) is the same easy route the judge names; decisive step is persistence through the rotation plus re-raking, matching the thread. The declared distractors (claimant series, staffing json) were not named as the surface read. Consistent, no mismatch.
Note for the author, not a determinism finding: the design note's Draw still mentions a youth rate and "three regional measures" while the shipped prompt asks no youth rate and the regional measures are visits, flows and hours. The note is stale there and could be tidied.

## Stump power (Gate F)
Moderate to good by paper. Easy routes (wave-1-only, no re-rake, all waves) each give clearly different gaps. The direction of the call is likely reached by strong models; stump power sits in the five-quarter path to two decimals and the regional asks. Portal is the real measure.

## Findings, ranked
1. None blocking.
2. Low: flow denominator relies on methods note section 6 rather than the prompt's wording.
3. Low: stale youth-rate and shape wording in DESIGN_NOTE.md Draw section.

## Next action for the author
Proceed to SHIP; optionally correct the stale design note lines.
