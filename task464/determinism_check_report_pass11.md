# determinism-check report, task464, 2026-11-02 (run a12, architecture 12, target.zip md5 5e4ade6bd89db0b2915c9890e54d5a74)

## Verdict
NOT_DETERMINISTIC, confined to ask 5's per-send "clicked within 28 days" counts. The main recommendation and asks 1 to 4 are forced and reproduce.
**Disposition:** FIX_NOW (pin how the 28 days count in ask 5's sentence, or a tolerance; no data or stump change, no rerun of the main call)
**Stumping type:** mechanism: decomposition_attribution (spillover outside the experiment's units), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Golden clicked counts (6,180 / 3,607 / 2,631 / 2,180 / 1,865 / 1,701) reproduce only if "within 28 days of the send" means calendar dates send day through day 27, counting clicks before the 10:00 send and before the restart. Send at its filed 10:00 plus 28x24h gives 6,205 / 3,623 / 2,635 / 2,192 / 1,871 / 1,710; counting only clicks after the restart gives 6,163 / 3,601 / 2,619 / 2,180 / 1,856 / 1,701. The prompt makes restart counts exact and is silent on the clicked counts' precision. Gates C/E fail for ask 5 only: underspecified_objective. Note the design note (fork table row 9) claims "nothing on the edge moves a bin", which holds for the 50,000-click figures but not for the exact person counts of ask 5.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reload 20-22 Oct | dedupe once | 243 exact duplicate rows; deduped months equal Finance xlsx | yes |
| Gain, mailed vs holdout | 111,788 | 111,788 (pooled), 111,796 (per group) | yes, rounds 100,000 |
| Loss, 3 groups, all channels | 255,348 | 255,356; 252,798; 250,155 under other baselines | yes, all round 250,000 |
| Net / 2027 | -143,560 / -311,046 | -143.6k / -311k | yes, -150,000 / -300,000 |
| Restarts per send | 11,383 / 6,758 / 4,848 / 3,910 / 3,451 / 3,150 | identical (13,256 gateway restarts removed, clean cut) | yes |
| Clicked per send | 6,180 ... 1,701 | only under calendar-day window | no under other literal readings |

## Competing answers that survived
- Ask 5 clicked counts: window as calendar days send day to day 27 (golden) against send timestamp +28x24h (6,205 / 3,623 / 2,635 / 2,192 / 1,871 / 1,710) against post-restart clicks only (6,163 / 3,601 / 2,619 / 2,180 / 1,856 / 1,701). No shipped sentence closes it for the exact counts.
- Main call: none. Holdout-only (+242k, keep), email-channel-only (loss 391k) and prior-28/44-day baselines (about -80k, rounds -100k) are eliminated by the plan's "with against without" wording and the data; sign and drop hold under every method.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (csv, xlsx, docx, pdf) | yes |
| Large file | 25,000+ rows | 170k rows (judge) | yes |
| Distractors | 2+ in metadata.json, none labelled in a file name | sponsored_revenue_by_sector_2026.xlsx, alerts_feedback_survey_2026-06.csv; names unlabelled | yes |
| Distractor behaviour | unused, weighs, ruled out by a shipped fact | Finance xlsx reconciles to the deduped warehouse months (the judge used it as a check; the solution does not need it); survey is background | yes, note below |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx); both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | ask 5 clicked counts carry no stated rounding or window rule | no (the finding) |
| Prompt shape / rubric | shape 09 identified, 25+ criteria | shape 09 in metadata; criteria count not checked here (generated rubric, not in folder) | not verified |
| Not LLM-generated / golden realism | yes | judge found no tells; golden has 4 sheets, not re-judged by me | yes (judge) |

## Gate G reconciliation
Judge: decomposition_attribution, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note stump sentence: holdout uplift is correct for the pool; the missed step is the cost to always-on jobseekers at Google, Microsoft and Yahoo. Matches. No distractor is named as the surface read carrying the task (the surface read is the pilot's own holdout, which is correct). Card file not found under ../cards by grep, so stump_class / analyst_test / domain_test not compared directly; the note's Three rules section (task type, domain test, swap, Layer 1) agrees with the judge's Gate H.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Field analysis is email-programme incrementality under interference; the easy route (holdout uplift carried, +242k, keep) is wrong for a strong analyst who read every rule.

## Stump power (Gate F)
Moderate to good. The ladder (note) puts R0 at keep and R1/R2 at -100,000 and -600,000, all outside the golden's bin. The judge flags the textbook route (uplift carried) as the lure; a strong solver who cuts by mailbox group and channel lands the call, so the main thread should weigh whether the ladder keeps one of the top two off it. Ask 5's gateway filter and install-id join are the ask-side difficulty.

## Findings, ranked
1. Ask 5 clicked counts depend on an unfiled window convention (three literal readings differ by up to 25 persons per send).
2. Design note fork row 9 asserts no edge sensitivity; it is true only for the rounded figures.
3. Metadata licence string says "Synthetic ... constructed for this task" (metadata, not a shipped file; hygiene minor).

## Next action for the author
Edit ask 5 in prompt.txt to file the WHAT: count a restarter as clicking if a sponsored click falls on the send date or any of the next 27 calendar days (or state that the clicked counts are to the nearest 50), keep the golden and goldens' sheets as built, extend fork row 9 and checks.py, rebuild twice byte-identical, then re-judge once.
