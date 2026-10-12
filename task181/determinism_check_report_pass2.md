# determinism-check report (pass 2), task181, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (exposure selection on honest data), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the bundle. All 96 ATM-related SMI are level-crossing pairs in one sector, the per-pair loss rate is flat (2.31 to 2.59 per 10,000) while the per-hour rate is not, and Tarvik's 2027 traffic carries 48,545 pairs on 16,414 hours, giving about 72 (72.4 to 72.5). The other seven are 19.0 to 25.6. Residual risk: plan clause 4.2 names no exposure model, but the data separates the hours-based "no sector" read from the pair model. Judge thread: /tmp/determinism-check-task181-781848/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| ATM-related SMI (D or I) | 96 | 96 (71 D + 25 I) | yes |
| Crossing pairs, record | 392,294 | 392,294 | yes |
| Pooled rate per 10,000 pairs | 2.45 | 2.447 | yes |
| Per-sector pair rate | 2.31 to 2.59 | 2.31 (LYS) to 2.59 (LNM) | yes |
| Per-100,000-hour rate, record | 13.8 to 24.2 | 13.8 (TRV) to 24.2 (KRW) | yes |
| Tarvik 2027 pairs / hours | 48,545 / 16,414 | 48,545 / 16,414.0 | yes |
| Tarvik forecast | about 72 | 72.5 / 72.4 | yes |
| Other seven | under 30 | 19.0 to 25.6 | yes |
| ATFM delay per flight (8 sectors) | .53 .41 .43 .16 .29 .55 .27 .10 | identical to 2 dp | yes |
| Solo open hours (8 sectors) | 1532.1 1310.5 735.3 1202.3 771.1 1410.2 971.6 1301.9 | identical to 1 dp | yes |
| ACAS encounters (8 sectors) | 8 9 10 7 4 7 3 2 | identical | yes |

## Competing answers that survived
None. Tested and rejected: "no sector" (hours or entries carry-forward, max about 32; rejected by the loss record), Grendal and Hallin (trend, one extra loss, no filed basis), permissive pair definition (Tarvik 63.5 to 69.6, call unchanged), all-overlap exposure (Tarvik 18.6; rejected by non-flat rate). Only the charted Tarvik value moves with the pair definition.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 15 | yes |
| Formats | 3+ | 6 (csv, json, md, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | fdps parquet 1,693,315 rows; planning csv 308,913 rows | yes |
| Distractors | 2+, none labelled | controller_roster xlsx, met_cb_activity csv, named in metadata.json, neutral file names | yes |
| Distractors relevant, unused | yes | same world, unused by the solution (judge) | yes |
| Deliverables | 1 to 3 | 2 (pptx, csv) | yes |
| Asks multi-dimensional | yes | 8 sectors x 3 measures plus the call and chart | yes |
| Deliverables present | all | both in golden/ | yes |
| Units and rounding stated | yes | delay 2 dp, hours 1 dp, whole encounters; forecast is charted, not rounded | yes |
| Prompt shape, 25+ criteria | yes | shape 01 (per metadata); about 24 graded cells plus the call and components. The count was not generated here, so confirm the 25 floor | yes (floor unconfirmed) |
| Realism | no LLM tells | judge found none; golden realism not independently re-read here | yes |

## Gate G reconciliation
The judge's classification is analytical_non_defect with surface_read_dependency no and sole_data_defect no. It is borderline against single_conceptual_flip (per-hour versus per-pair lens), but pinned by the loss record. The card says stump_class analytical, and its analyst_test names the same trap (hours, traffic-squared or climbing-flight scaling says no sector; only crossing counts put Tarvik over). The design note's mechanism is "gap population (what one unit of exposure is)". These match, and the card's mechanism and stumping_family fields are null. The closeout (14,957 hours, 13.4, 32.0) is a correct trailing report, and metadata lists it among the stated inputs, not as a declared distractor; the judge did not name a declared distractor as the surface read. The risk is the borderline flip reading, since a reviewer may call the lens change a single conceptual flip.

## Stump power (Gate F)
Good. The default hours-based carry-forward reproduces "no sector" and is the trap. The asks carry their own traps: regulation-id reuse, most-penalising regulation, the 14 July 06:00 revision switch, local-time season edges and duplicate ACAS reports.

## Gate H
domain pass, layers pass, decisive_step analytical. Exposure-based incident-rate forecasting is the field's own method; the swap test fails for other domains.

## Findings, ranked
1. Low: clause 4.2 names no exposure model, so there is some reviewer risk on the main call. The judge does not recommend closing it, since a sentence would pre-answer the stump.
2. Low: "levels change order" is strict in the golden. The permissive reading moves the charted Tarvik value to about 64 to 70, with the call unchanged. Stating the strict definition in the write-up would close it.
3. Low: Gate G borderline against single_conceptual_flip, pinned by the all-96-crossings record and the flat per-pair rate.
4. Informational: the config-log remarks that do not match the logged codes read as operational noise, and OM 4.1.2 makes the logged code govern.

## Next action for the author
Ship as is, optionally adding to submission.md one line that "levels change order" is the strict reading and that "about 72" holds to roughly 1.
