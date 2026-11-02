# determinism-check report, task464 (architecture 12, target.zip md5 c4f99ad46209a45dff0be4efdb9f7e7a), 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (thread's label; card gate_g says decomposition_attribution), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The filed estimand (jobseeker_email_plan_2027.docx section 5: the business's sponsored clicks with against without the series, 28 days from each of the six pilot sends, 2027 = average pilot send x 13) forces a company-wide count. Read literally it is the pilot-pool gain (+111,788) plus the loss on alerts-on jobseekers at gmail, microsoft and yahoo_aol (-255,348), negative on every defensible baseline. The recommendation, every critical component and every supplementary answer reproduced from the shipped files. One thread, one pass, no retry. Thread verdict: /tmp/determinism-check-task464-a12b/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Mailed vs holdout clicks per jobseeker (six windows) | 0.178 vs 0.034 | 0.178 vs 0.0338 | yes |
| Pilot gain | 111,788 (100,000) | 111,788 | yes |
| Loss, G/M/Y alerts_on, days 0-13, all channels | 255,348 (250,000) | 255,348 | yes |
| Net over pilot | -143,560 (-150,000) | -143,560 | yes |
| 2027 series | -311,046 (-300,000) | -311,046 | yes |
| Restarts per send, scanner passes removed | 11,383 / 6,758 / 4,848 / 3,910 / 3,451 / 3,150 | identical | yes |
| Restarters with a sponsored click, send date +27 days | 6,180 / 3,607 / 2,631 / 2,180 / 1,865 / 1,701 | identical | yes |

## Competing answers that survived
None on the call. Loss baselines tested (own prior fortnight 246,052; with control adjustment 252,811; days 14-27 246,305; ratio from Jan-Apr 2026 257,796; all 2025 to Apr 2026 256,452; non-dip days 255,452) all sit in the 250,000 band and 2027 rounds to -300,000 (net -134,000 to -146,000). A 28-day pre-window (43,602) or 14-day post against 28-day pre (145,142) takes in the previous send's dip: contamination, not a licensed alternative. Full pool instead of mailed arm gives about -284,000, still -300,000. Ask 5 variants (no install-id linking: send 1 6,085; 29-day window: 6,354) move only by not following the filed text. Scanner threshold gap is clean (humans at most 2 links in 10 s, scanner passes 6 to 11), so any threshold 3 to 5 gives the golden.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10+ / 3+ / 25,000+ rows | 12 files, csv, xlsx, docx, pdf (4), 170,352 and 145,905 row files | yes |
| Distractors | 2+ in metadata.json, none named by file name | sponsored_revenue_by_sector_2026.xlsx, alerts_feedback_survey_2026-06.csv; names neutral | yes |
| Distractors unused yet weighable, ruled out by shipped fact | required | month-end sector view cannot give mailbox or window figures; survey is of paused/unsubscribed jobseekers; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both answered in submission | yes |
| Asks multi-dimensional, unit and rounding stated | required | prompt states nearest 100,000 / 50,000 / exact counts; ask 5 is six sends by two counts | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 09 in metadata; prompt 833 characters, one paragraph; the rubric is generated downstream and I could not count criteria from the package | yes on shape, criteria count not verifiable here |
| Not LLM generated, goldens realistic | required | thread found no authoring disclosure; Layer 1 mess reads as operational | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor (spillover onto a population outside the holdout), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Card: gate_g decomposition_attribution, stump_strategy causal_design, layer2_family estimand_identification (interference through a shared sender standing). Design note: the decisive step is a difference in differences of active jobseekers' clicks by mailbox group against unfiltered groups.
The labels differ in name only. Both describe the same step: the holdout cannot see the cost the sends impose on non-experiment recipients, and the analyst must estimate it. Neither is a surface read rejection, a planted defect or a stated rule; the distractors (sector revenue, survey) were not named by the thread as carrying the task. The difference does not change the verdict, the family or the disposition. If the author wants the card and thread to agree, statistical_rigor (estimand and control group) is the nearer description of an interference estimate; decomposition_attribution is defensible since the net effect is split into pool gain and outside loss. Not a send-back finding.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card and design note: same (domain_test and analyst_test present, Three rules block carries No decoy, Not semantics, Not rule application). Match. The thread classed the step analytical because the plan files only the outcome, window and sizing and no method; it did not reach the golden by applying a standard method with no judgment, so no landable-call caveat is needed.

## Stump power (Gate F)
Moderate to good. Easy route is the holdout uplift (+111,788, about +242,000 a year), which says keep. Reaching the golden needs the alerts_on rows split by mailbox group with a baseline not contaminated by the prior send. A strong model reading the Postvane Gmail open drop could find it, so the stump is plausible, not guaranteed. Ask 5 (scanner passes, install-id linking) adds an independent layer. Weighed against the design note's ladder by the main thread.

## Findings, ranked
1. None blocking.
2. Minor: SOLUTION_STEPS step 1 (20-22 October reload, app channel merge) sits outside every graded window; harmless, not load-bearing. Optionally drop or footnote it.
3. Minor: step 6's threshold of 4 is one point in a 3-to-5 gap; any value there gives the same counts. Neither the plan nor the brief states the scanner concept or dedupe rule, both are data-recoverable and do not touch the main call.
4. Label difference between card and thread on mechanism (see Gate G reconciliation); no action required.

## Next action for the author
Ship on this pass; optionally tidy the solution block (step 1 and the threshold note) without touching any figure.
