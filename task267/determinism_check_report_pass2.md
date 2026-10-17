# determinism-check report, task267, pass 2, 2026-10-17

## Verdict
NOT_DETERMINISTIC (supplementary ask 3 only, the credit memo amounts; the main call and asks 1 and 2 are forced and reproduce). SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW. The fork sits under Gates C and E (underspecified_objective, prompt_ambiguity), which fail as fixable findings per determinism-check section 6. Gates G and H pass, so there is no SEND_BACK. The thread itself wrote SEND_BACK because closing the fork changes shipped files or graded figures; I classify by the gate table. This was the one licensed re-judge, so no third judge pass runs before the author closes the fork.
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The 246 credit memo lines in thessler_invoice_lines_2026.csv carry printed amounts of -38.50 (x52), -77.00 (x86), -115.50 (x72) and -154.00 (x36), each applied to a single 38.50 invoice line (I re-counted these). The golden nets each credit "at the amount of the invoice line it applies to", which overrides the printed amount. The prompt says only "net of its credits", and no shipped document speaks of capping or replacing a credit (the extract notes only say the file holds invoices and credit memos; the protocol never mentions credits). Read literally, the printed amounts apply, and all nine months move in both figures. Under the printed reading, March is 14,206.50 and 13,706.00 against the golden 14,630.00 and 14,129.50, and November net is 46,970.00 against 47,509.00. The judge also finds the golden reading is the only coherent one, because a printed memo line otherwise credits more than the line it reverses. That is an inference, and the real reviewer reads the literal text. The design note records this grain as deliberately unfiled (device D6) and at round 1 kept it unfiled; this pass shows the literal reading cannot close it. The 18 dollar figures of ask 3 are therefore an open fork.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adults first screened (screening_encounters_2026.csv) | 37,269 | 37,269 | yes |
| Complete OGTT matched on 7-digit ID (ogtt_results_2026.txt) | 10,715 | 10,715 | yes |
| Sensitivity, whole percent, A60 / R26A60 / A57 / SC5 / A57G120 / A55 | 51 / 79 / 80 / 62 / 90 / 93 | 51.13 / 78.88 / 80.20 / 61.83 / 90.03 / 92.98 | yes |
| Referral share, A60 / R26A60 / A57 / SC5 / A57G120 / A55 | 8.4 / 24.9 / 28.2 / 35.9 / 36.3 / 49.3 | 8.44 / 24.86 / 28.21 / 35.92 / 36.28 / 49.27 | yes |
| Cartridges per analyzer A01 to A12 (gq200_run_log_2026.csv, register, error codes pdf) | 40,248 in all, per-analyzer as in submission | identical | yes |
| Monthly net billed and adult-screened part, March to November | golden pairs, $415,800.00 and $409,255.00 | identical only under credits at the invoice line amount; the printed-amount reading gives different values (convention B) | yes under the golden convention, no under the literal one |

## Competing answers that survived
- **Credit amount (thessler_invoice_lines_2026.csv, amount_usd and applies_to).** Answer 1 (golden): each credit line at the amount of the invoice line it applies to, giving $14,630.00 / $14,129.50 for March and $415,800.00 net in all. Answer 2 (literal): each credit at its printed amount, giving $14,206.50 / $13,706.00 for March, and all nine months differ. No shipped rule closes it. This is the only surviving fork, and it touches ask 3 only.

## Spec gates
Checked by me against the fresh unzip.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, txt, xlsx, pdf) | yes |
| Large file | 25,000 or more rows | gq200_run_log_2026.csv 49,144; screening_encounters_2026.csv 38,154 | yes |
| Distractors named, none labelled by file name | 2 or more | metadata.json names participant_feedback_2026.csv and orlenby_chronic_disease_profile_2024.xlsx; neither file name says "distractor" | yes |
| Distractors unused yet weighty, and ruled out by a shipped fact if they answer a graded quantity | as stated | the judge found the feedback and the 2024 profile unused; I did not independently test whether either reproduces a graded figure | accepted on the judge's read |
| Deliverables | 1 to 3, all in the golden | 2, both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | as stated | 6 rules x 2 shares, 12 analyzers, 9 months x 2 amounts; the prompt states the roundings | yes |
| Rubric reach | 25 or more criteria | 42 gradable figures in asks plus the call | yes |
| Prompt shape, no LLM tells | as stated | judge found nothing generated; the shape is a multi-part review | yes |

## Gate G reconciliation
The thread reports mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no and sole_data_defect no. The card's stump_class is analytical. Its analyst_test (complete-case sensitivity gives the 2026 rule or HbA1c 6.0 at 94%, 24.9% referred) matches the judge's complete-case route exactly (94.4% there, against the weighted 79%). Its domain_test (diagnostic accuracy under partial verification with inverse-probability weighting) matches the judge's Gate H line. The design note's fork table has no row for the credit grain; the credit device is filed as an ask device (D6), so there is no mismatch on the main call. Neither declared distractor carries the call. Gate G: pass, statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no.

Gate H: pass. domain: pass, layers: pass, decisive_step: analytical (verification-bias correction through the one-in-five draw).

## Stump power (Gate F)
Strong. The easy complete-case route files R26A60 at 94% and 24.9% referred, the wrong call. Only the weighting yields A57G120 at 90%. The asks add a second hold, but the credit fork means ask 3 cannot be graded cleanly until it is closed.

## Findings, ranked
1. Credit memo grain unfiled for ask 3 (Gates C and E, underspecified_objective). The literal reading of "net of its credits" nets the printed amounts, not the golden's invoice-line amounts. All 18 dollar figures are affected.
2. Distractor weight was not independently tested by me (low).

## Next action for the author
Close the ask 3 fork in the generator in one step, keeping the call and asks 1 and 2 frozen. Either make each credit memo line's amount equal to the invoice line it applies to, so that the printed and golden readings agree, or add a billing-office note saying credits are applied at the line amount. Alternatively, re-key the golden to the printed amounts. Then rebuild, confirm the rebuild is byte-identical, and rerun figures_check.py. The design note says a filed sentence would hand over the D6 device, so equalising the amounts is the cleaner route, but that changes the device and the ask 3 stump; the author decides.
