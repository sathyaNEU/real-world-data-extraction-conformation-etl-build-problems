# determinism-check report, task191 (architecture 4), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one minor ask-reading note below, no fix required)
**Stumping type:** mechanism: statistical_rigor (informative right-censoring, age-conditioned expectation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread (tuning_2027_thread.eml) files the estimand: alerts by run business date, duplicates out, XB-HRJ read with XB-HRJ2, open alerts counted "by how they will end", floor 3 per cent. The judge thread reproduced the main call and every supplementary answer from the bundle. CRY-OFF, CSH-VEL, DRM-REA and PRF-DEV stay under 3 per cent on every reading (even with every open alert a SAR: 2.83, 2.45, 2.10, 1.90). RMF-P2P, MUL-INF and MER-RND fall under 3 on the decided-only and naive rates (2.72/2.36/2.74 decided) and clear it once the open alerts are read at the age-conditioned SAR share (4.50, 4.46, 4.62). Verdict file: /tmp/determinism-check-task191-1793486766/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| In-window alerts, DUP out | (n/a) | 55,238 (157 DUP, run TMR-20260310-02) | yes |
| Open alerts RMF-P2P / MUL-INF / MER-RND | 91 / 127 / 82 | 91 / 127 / 82 | yes |
| Adjusted rate RMF-P2P / MUL-INF / MER-RND | 4.5 to 4.6 | 4.50 / 4.46 / 4.62 | yes |
| Adjusted rate CRY-OFF / CSH-VEL / DRM-REA / PRF-DEV | under 3 | 2.17 / 2.15 / 1.84 / 1.50 | yes |
| Investigations by quarter, 14 x 4 | golden | all cells match | yes |
| SARs by month Jan-Oct 2026, initial / continuing | golden | all ten months match | yes |

## Competing answers that survived
- Residual (minor): taking only the in-window alerts 330+ days old as the whole-year estimate gives MUL-INF 2.72 (RMF-P2P 3.73, MER-RND 3.89). Unconditional small-sample shortcut (about 25 SARs) that ignores "by how they will end" and cannot cover the oldest open ages. Treated as a method error, not a licensed reading.
- Ask 4 quarter basis (my own check, below): alert business-date quarter against case opened-date quarter differ for 574 of 10,337 cases. The prompt says investigations "opened" in each quarter, so the literal reading is the opened date. Not an open fork, but the one reading where a solver's different count would be defensible only by ignoring the word "opened".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 10 / 5 (csv, json, xlsx, pdf, eml) | yes |
| Large file | 25,000+ rows | alerts 74,360; customers 40,074 | yes |
| Distractors | 2+ named, none in file names | customer_risk_tiers_2026-10.csv, investigations_capacity_2027.xlsx, qa_case_sampling_2026.csv; none carries a conversion | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both in golden/ | yes |
| Asks unit and rounding | stated | "whole numbers", per cent for chart | yes |
| Prompt | one paragraph, under 1,000 chars, no count | 627 chars, no count | yes |
| Rubric 25+ criteria; no LLM tell | | not generated here; prompt shape is a scorecard over 14 scenarios plus 14x4 and 10x2 cells, which supports 25+ | not checked directly |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read no, sole_data_defect no. Design note (read after the thread returned): informative_censoring, decisive step the age-conditioned read of undecided alerts, no decoy, distractors carry no conversion. The thread names no distractor as the surface read. Match. The easy route (decided share, or open projected at it) files seven scenarios, which is the note's declared default path; no shipped artifact ranks the scenarios wrongly.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the note's Three rules. The thread does not class the step analytical merely because it is the field standard: the golden needs a method choice the data separate (decided, naive and conditional readings give different calls). Stump power is strong on paper (wide margins, one specific wrong answer); the portal measures it.

Leak reader's three ask readings:
1. SAR month, UTC against Eastern: the judge tested it, counts identical (filings are 12:00 to 22:00 UTC). Not a fork.
2. Quarter by alert business date or case opened date: the prompt says investigations opened, so opened date (Eastern) is literal. Judge found Eastern against UTC gives zero differences. My check shows the alert-date basis would move 574 cases, so the opened-date wording is what closes it. Optional hardening: confirm the design note's fork table has a row for it.
3. Calendar against fiscal quarters: the twelve months to 30 September are the window; no shipped file defines a fiscal calendar, and the labels 2025 Q4 to 2026 Q3 are calendar quarters that coincide with it. Per-cell counts do not depend on the label. Not a fork.

## Stump power (Gate F)
Strong on paper. Easy route files seven scenarios; correct call is four. Margins: CRY-OFF 2.17 and PRF-DEV 1.50 against 3; RMF-P2P 4.50, MUL-INF 4.46, MER-RND 4.62. The WHAT is filed and the HOW is open, so it is not rule application.

## Findings, ranked
1. Minor: ask 4 quarter basis resolves only on the word "opened" (574 cases differ under the alert-date basis). Ensure fork table row exists.
2. Minor: the 330+ day in-window cohort shortcut leaves MUL-INF at 2.72; a method error, not a fork.

## Next action for the author
None required. Proceed to ship; optionally confirm the quarter-basis row in the design note's fork table.
