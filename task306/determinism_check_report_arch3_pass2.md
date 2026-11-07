# determinism-check report, task306, 2026-10-31 (pass 2, re-judge after the FIX_NOW)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (one solution-block gap, no pack change)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call is forced by CP-04 s2 and s3 and the shipped YLT, hindcast and experience files. Nine storms within 2 to 23 days of the storm before cost 1.43 to 1.77 times hindcast (aggregate 1.615); the other 34 cost 0.67 to 1.17 (0.976). Costing the YLT at those ratios gives 113 / 94 / 87, release 7, margin 0.70, value 0.1. One pooled ratio gives release about 4.8 and value about -0.3, which flips the call. The pass-1 findings (worth/value wording, cover B reinstatement, ask 7 policy-wide share) are closed: the prompt now says "value", and "our share of each farm policy's sums insured".

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Fast / other ratio | 1.62 / 0.98 | 1.615 / 0.9755 | yes |
| 1-in-200 gross / net A / net A+B | 113 / 94 / 87 | 112.91 / 93.99 / 87.09 | yes |
| Release | 7 | 6.90 | yes |
| Margin | 0.7 | 0.700 | yes |
| Value | 0.1 | 0.13 to 0.14 | yes |
| 2026 recovery / reinstatement premium | 12,015,000 / 1,402,000 | 12,015,394 / 1,401,796 | yes |
| Jan 11-13 home / farm | 13,067,000 / 2,510,000 | 13,066,798 / 2,509,825 | yes |
| Feb 8-9 home / farm | 16,898,000 / 3,541,000 | 16,898,055 / 3,540,717 | yes |
| Feb 15-16 home / farm | 3,943,000 / 931,000 | 3,943,200 / 931,244 | yes |
| Farm SI buildings / contents by county | C 1302.1/618.2, D 1502.4/746.3, S 863.7/396.8, Do 389.0/184.3 | identical | yes |

## Competing answers that survived
1. Undated reopened lines (asks 5 and 6): 379 "/R1" storm lines have no instruction of their own. The golden dates each from its original claim's instructed damage day. Using the line's own loss_date gives recovery 11,881,000, reinstatement premium 1,386,000, and shifts each occurrence cost by tens of thousands. No shipped sentence states the inheritance. Only the write-up is flagged by the judge, but a solver sees only the pack, so this is a real fork on asks 5 and 6 (not the main call) and the closing rule is not in the files. The main thread should decide whether a one-line pin is acceptable in the prompt or the pack.
2. Unmatched register entries: 56 register holdings match nothing; policies absent from the register at 100%. Both conventions reproduce the golden; minor.
3. Dating by instructions rather than loss_date: closed by wording clause 3 ("dated by the day on which the damage was done").

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / 4 | yes |
| Large file | 25,000 rows | home_policies 46,741 | yes |
| Distractors | 2+ named, none in a file name | 3 named in metadata.json; judge also notes the panel email | yes |
| Distractor weighs but unused | yes | flood YLT ruled out by CP-04 s1 | yes |
| Deliverables | 1 to 3 | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding | closing sentence states both | yes |
| Prompt | one paragraph, under 1,000 chars | 993 chars, one paragraph | yes |
| Rubric 25+ | yes | not inspected | not checked |
| Real work product / no LLM tells | yes | judge found none | yes |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read no, sole_data_defect no, which matches the design note (gap-class calibration against the pooled factor, no decoy). No declared distractor is the surface read. Gate H: domain pass, layers pass, decisive_step analytical, agreeing with the note's Three rules and the reflex rung (release 5, value -0.3). The decisive step is a model-calibration choice the data separates, not a field reading or an executed rule.

## Stump power (Gate F)
Good. The pooled ratio, and the season or position-in-year routes (which do not separate the data), file "do not add". The class is found only from the experience file's bimodal ratios against the gap to the storm before. Asks add independent reconstruction devices.

## Findings, ranked
1. Reopened-line dating is an unstated convention. Fix: state in step 6 that a reopened line with no instruction of its own takes its original claim's instructed damage day, and consider whether the pack needs a shipped sentence so the fork is closed for a solver (the judge treats it as a write-up gap).
2. Optional: state in step 7 that policies absent from the coinsurance register are taken at 100%.

## Next action for the author
Add the step 6 sentence (and the optional step 7 one) to submission.md, and decide whether the reopened-line rule needs a shipped statement.
