# determinism-check report, task267, 2026-10-17 (pass 3)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (verification-bias correction, design-weighted sensitivity), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: isolated, from /tmp/determinism-check-task267-1792260553/judge_brief.md, over a fresh unzip of target.zip. It returned /tmp/determinism-check-task267-1792260553/verdict.md. The thread ran from the brief because this runtime has no Agent tool.

## Why
Protocol 6.2 and 6.3 file the estimand (every adult screened, first screening, at least 85 of 100 with undiagnosed diabetes, then fewest referred). The evaluation draw (OGTT to all referred by the 2026 rule, a random fifth of the rest) forces group weighting. Literal execution gives A57G120 at 90% and 36.3%. A55 qualifies (93%) but refers 49.3%; A57 (80%) and R26A60 (79%) fail; SC5 refers 35.9% but finds 62%. The pass 2 FIX_NOW (credit memo grain) is closed: each memo line attaches through applies_to to the line it reverses, and the prompt's "tests done that month" puts the credit with its test. 246 of 246 resolve. The memo's own date would give different months (March 15,015.00, November 46,508.00), and the shipped text excludes it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First screenings | 37,269 | 37,269 (149 repeated encounter_id dropped) | yes |
| Complete OGTT / diabetes | 10,715 / 1,117 | same (matches close-out) | yes |
| Weights | n/a | not-referred 29,792/4,665 = 6.386; RULE 7,477/6,050 = 1.236 | yes |
| Sensitivity % (A60, R26A60, A57, SC5, A57G120, A55) | 51, 79, 80, 62, 90, 93 | 51.1, 78.9, 80.2, 61.8, 90.0, 93.0 | yes |
| Referred % of screened | 8.4, 24.9, 28.2, 35.9, 36.3, 49.3 | same | yes |
| Cartridges A01-A12 | 3486, 2686, 2966, 4216, 3735, 3535, 3692, 3864, 2588, 3449, 3071, 2960 (40,248) | same, all twelve | yes |
| Monthly net billed Mar-Nov, total / adults screened | 415,800.00 / 409,255.00 | all nine months exact | yes |

## Competing answers that survived
None that changes a committed answer.
- Unweighted reading (tested only): R26A60 94.5%, A57G120 93.6%, A57 82.8%. Picks R26A60 at 24.9%. This is the declared easy route, wrong under 6.2, not a reading fork.
- Finer post-strata: A57G120 stays 90.0 to 90.2, A57 80.2. Full HbA1c x glucose x score strata move A57 to 80.6 and R26A60 to 77.8. The call holds. A57's whole percent could read 81 only under that elaborate model (residual risk, low).
- December billing (17,748.50 / 17,055.50): "each month of the season" is March to November (2 Mar to 20 Nov in the notes, nine months in the close-out). A December row would be extra, not a conflict.
- Six-digit program IDs: the zero-pad is forced by the 7-digit format, 0 collisions.
- 93 accessions billed twice and never credited: kept, per "billed, net of its credits".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | csv, txt, xlsx, pdf | yes |
| Large file | 25,000 rows or more | encounters 38,154; run log 49,144 | yes |
| Distractors | 2 or more in metadata.json, none labelled in file names | participant_feedback_2026.csv, orlenby_chronic_disease_profile_2024.xlsx | yes |
| Distractors unused yet weighable, none answering a graded quantity | required | neither gives a rule's sensitivity; the close-out counts people and answers its own question correctly | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, docx), both present | yes |
| Asks multi-dimensional, unit and rounding stated | required | six rules x 2 shares, 12 analyzers, 9 months x 2 amounts; rounding in the prompt | yes |
| Prompt shape and 25 or more criteria | required | shape 10 scorecard; about 12 rule figures + 12 + 18 + call + components, above 25 (estimated; the generated rubric is not shipped here) | yes |
| Prompt | one paragraph, under 1,000 characters | 956 characters | yes |
| Reads as real work product, not LLM-generated | required | judge found no authoring language; hygiene PASS | yes |
| License records | recorded | not checkable by the thread; author's pre-ship check | not verified |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, estimation_fit (weighting a partially verified sample), card gate_g method_or_model_selection, decisive step the inverse-OGTT-rate weighting by 2026 group. These match: the verification-bias correction. The declared distractors (feedback cards, 2024 profile) were not named as the surface read carrying the task. The thread's analyst-test route (94% among the tested, R26A60 at 24.9%) matches the card's analyst_test word for word. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. This agrees with the note's Three rules and the card's domain_test. The Layer 1 mess (UTC copies, six-digit IDs, loaners, credit-memo months) drives the asks and not the call.

## Stump power (Gate F)
Strong for the call. The tested-only figures are arithmetically correct and the easy analyst files R26A60. Protocol 6.2 ("counting every adult screened, whether or not they had the test") points at the estimand without giving the method. The asks' Layer 1 devices are harder than the call.

## Findings, ranked
1. None blocking.
2. Low: A57 reads 80.2 under group weighting; an elaborate full-strata model gives 81. The design note records every weighting agreeing at the whole percent for the tested weightings.
3. Low: "each month of the season" leaves December implicit (March to November is supported by the notes and the close-out).
4. Note: the pass 2 credit memo fork is closed by "tests done that month" plus applies_to. The thread found the filed text sufficient.

## Next action for the author
Proceed to stage 5 ship; no generator change. Optionally confirm the license records in metadata.json, which the thread could not see.
