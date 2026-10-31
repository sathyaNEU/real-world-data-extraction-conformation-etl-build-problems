# determinism-check report, task242 (pass 2), 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (verdict at /tmp/determinism-check-task242-pass2/verdict.md) read only the fresh unzip of the 17-file bundle (no README, no data dictionary) and the extracted blocks. Executing the register's SERO-D1 estimand and SOP-EPI-07's M flag word for word gives the golden's six flagged zones (IV, V, VII, VIII, IX, XI). Every defensible smoothing, case-set or dedup variant flags the same six. The reship's changes (describing files removed, assessment number added to SOP-VC-02, whether-form prompt without a zone count) opened no fork: the Breteau zone reads from the premise number and agrees with the ward master on every form.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Panel: 557 sera, 216 patients, 11 bin sensitivities; Sp 0.9867 | as golden | same | yes (ngmc_igm_lot_verification_panel.csv) |
| Line list: 35,166 resident 2027 cases (1,476 non-residents, 7,554 pre-2027 out) | as golden | same | yes |
| Effective Se by zone (0.232 to 0.808) | as golden | same to 3 dp | yes |
| Estimated shares (12 zones) and multiples (3.00, 2.02, 2.71, 3.28, 3.00, 1.85; Puthanpalli 1.29) | as golden | exact | yes |
| Published shares (4,952 tested, 440 reactive) | as golden, bulletin Table 1 | same | yes |
| Breteau index (13,250 houses), 12 zones | 10.6 to 24.8 | exact | yes |
| Household response (2,037 eligible, 1,564 responding), 12 zones | 73.8 to 80.4 | exact | yes |
| Commentary: "a fixed 90-day window flags three" | three | four (Melm, Vell, Chin, Peri) | no (commentary only) |
| Commentary: "kit's 5 to 60 day window" | 0.868 | no source file located | not checked by thread |

## Competing answers that survived
None on the graded figures. Forks that change the flag set (single pooled Se, median/peak/mean day, Sp ignored, 2026 start) are each excluded by filed text: "since 1 January", "misclassification as the laboratory measured it", and an estimand that averages over the infected. A notification-date basis moves one estimate 17 percent (outside the 15 percent tolerance) but flags the same six. A tested-only response rate is excluded by the protocol's "at least one member gave a blood specimen".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 17 / 5 (csv, pdf, xlsx, docx, eml) / 44,196 rows | yes |
| Distractors | 2+ named, none labelled by file name | ncmc_rain_gauges_daily.csv, ncmc_fogging_log_2027.csv in metadata.json; names carry no label | yes |
| Distractors unused yet weighable | yes | carry no serology; relevant vector-control context. They answer no graded quantity, so no arithmetic check applies | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-zone grid, per cent to one decimal, Breteau one decimal | yes |
| Prompt shape and 25+ criteria | shape 07, 25+ | shape 07; design note states well over 25 (not recounted by me) | yes |
| Not LLM generated; goldens real work products | yes | no authoring leakage seen by the thread; golden-realism is a separate gate | yes |

## Gate G reconciliation
The thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, no ranking artifact (Table 1 is the values under review), rain and fogging carry no serology. The card has no mechanism/stumping_family fields to compare. No mismatch. The thread named no declared distractor as the surface read carrying the task, so the distractors are not too load-bearing. The decisive step needs no deleting-wrong-numbers test because no wrong number ships.
Gate H line: domain pass, layers pass, decisive_step analytical. This matches the design note's Three rules (domain test, Layer 1 and Layer 2, decisive step).

## Stump power (Gate F)
Moderate to high per the thread. The easy routes (one pooled panel sensitivity 0.677, 0.708 or 0.868; median day four zones; peak five; mean seven; Sp ignored seven) each land a wrong set, and the single-sensitivity route flags none. The thread did not class the decisive step as the field's standard method reached without judgment, so no landable-call flag is raised. Residual risk the main thread should weigh on the ladder: the median and mean-day summaries are tempting approximations, but they do not reach the golden set.

## Findings, ranked
1. Commentary inconsistency, not graded: submission.md says a fixed 90-day window flags three; the thread's literal 90-day window flags four. The design note (line 234) says three with a particular window definition. Reword or specify the window in the golden's sentence.
2. Commentary: the "kit's 5 to 60 day window" (0.868) was not located in a shipped file by the thread. It is a rejected route, not decisive; confirm it is derivable from the panel or soften the phrase.
3. Notification-date basis moves one estimate 17 percent (outside the 15 percent tolerance) while flagging the same six; the submission claims only tolerance for the listed variants, so no contradiction.

## Next action for the author
Fix the two commentary sentences in submission.md section 1 (the 90-day count and the 5 to 60 day window source), rerun the figures check, then ship. No determinism re-judge is needed since no graded figure moves.
