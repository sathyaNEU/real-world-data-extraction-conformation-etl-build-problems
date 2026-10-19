# determinism-check report, task249, 2026-10-19 (pass 2, architecture v4)

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Judge run r4 (one thread, fresh unzip of target.zip sha256 prefix 31ad0d1e, spawned by the main session from the brief because this runtime has no Agent tool). Executed literally, audience_policy_2029.pdf sections 2 to 4 set the estimand (distinct browsers per edition and Berlin month, averaged over Oct to Dec, against the platform's users, note above 25 per cent). The shipped files pin the estimator: the WebKit 7-day cap (analytics_tag_notes.pdf), the meter kept in the same script storage (paywall_and_accounts_notes.pdf), the sign-in register and account origins. On that estimator the split is 8 noted / 4 not, about 3 points either side of the line. Every supplementary figure reproduced exactly. Full thread verdict: /tmp/determinism-check-task249-r4/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reported users per edition, Oct to Dec (RHS 15,558.3; KBR 13,463.7; HOL 6,898.0 ...) | platform_users_by_month_2028.xlsx | web_sessions parquet less 11,399 re-sent rows, bots, 85.214.110.0/24, Berlin months, HKR read as HOL | Yes, every Oct, Nov, Dec cell |
| Overstatement, golden method | 8 noted (RHS, MST, KBR, WBR, GRH, SOW, HOL, LDN at 32.6 to 27.9); 4 not (BST 21.4, FKR 19.8, EIT 18.8, ALH 16.3) | same | Yes, 8 of 12 as golden |
| Print devices 61% WebKit vs 27% other signed-in; 2.04 identifiers per print WebKit device vs 1.25 registered WebKit vs 1.60 registered non-WebKit replay | register + accounts + parquet | direction and levels confirmed | Yes |
| Sold copies Q4 2028, all 12 editions (RHS 7,288 ... FKR 3,667) | circulation, epaper, single_copy_sales, retail_points | exact to the copy, 451 out-of-sequence start dates treated as pre-quarter | Yes |
| Newsletter subscribers at 2028-12-31 23:00 UTC, all 12 (RHS 3,434 ... FKR 984) | contacts, activity_log, group_changes | exact, 71 preference-centre changes and 906 post-midnight add-edition clicks undone newest first, 458 earlier clicks stand | Yes |

## Competing answers that survived
Main call, two variants flip the split and are defensible readings of an unfiled estimator (Gate C candidates). The thread judged each eliminated by shipped facts, with no closed numeric test in a file:
- Sign-in split (register devices for signed-in, replay for signed-out): 4 editions (GRH 22.0, SOW 22.0, LDN 22.4, WBR 22.8 drop). Closed by: the meter shares the capped storage (paywall notes plus tag notes), so signed-out WebKit readers are the weekly and occasional ones; registered WebKit devices carry 1.25 identifiers a month against 1.60 replayed for non-WebKit registered clients.
- Pooled device-only replay (print not held apart): 5 editions (HOL 18.0, KBR 20.0, MST 20.1 drop). Closed by: print subscribers need no meter, are 61% WebKit, and print non-WebKit runs 1.99 against 1.51 signed-out.
Harmless variants (no device-class strata 8/4, lowest noted 27.3; runs within edition 8/4, lowest 28.2) keep the call. A circular runs reference including WebKit clients is not defensible.
Supplementary forks (not blocking): sold copies read 451 start dates (6 Nov to 13 Dec) as not first delivery days, inferred from sub_no order in DATA_DICTIONARY.md and corroborated (122 in-quarter COMBI start same day as Digital Plus access; none flagged before 6 Nov); read literally the figure differs 9 to 60 copies per edition. Newsletter counts need clicks on /newsletter/ausgabe-hinzufuegen read as adding an edition (the URL, and clicked editions always sit in current groups). Both are ask-side data semantics, allowed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 20 | Yes |
| Formats | 3 or more | 5 (md, csv, pdf, xlsx, parquet) | Yes |
| Large file | 25,000 rows or more | web_sessions_2028q4.parquet, 3,012,902 rows | Yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | ad_delivery_2028q4.csv, media_analysis_2028_reach.csv; neither name labels it | Yes |
| Distractors unused yet weighable | each | ad impressions and survey readers per issue, both relevant to a media kit, neither used by any graded figure; neither answers a graded quantity | Yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | Yes |
| Asks multi-dimensional with unit and rounding | each | copies to nearest whole copy, subscribers exact, per edition and quarter or cutoff | Yes |
| Prompt shape and 25 or more criteria | identifiable, 25+ | shape 10 (scorecard of twelve editions plus two per-edition figures); 12 call marks, count, 12 copies, 12 subscribers, chart, note naming editions exceed 25 | Yes (not generated here) |
| Reads as real work product, not LLM generated | none flagged | thread saw memo-style PDFs, no authoring language; golden realism not re-read by this pass | Yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g method_or_model_selection, stump_class analytical, stump_strategy causal_design, no decisive rule filed, no official or validated decoy. Design note: the stump is the conditioning set of the replay (sign-in out, print held apart). Match on all four fields. The declared distractors (ad delivery, survey reach) are not named by the thread as a surface read carrying the task, so no over-load finding. The thread's two flipping routes are the card's analyst_test (4) and the design note's pooled variant (5), the same routes the note names as the easy answers.

Gate H (thread): domain pass, layers pass, decisive_step analytical. Card domain_test and analyst_test agree: the decisive quantity is browsers behind a capped identifier estimated by replay on persistent histories, a swap to hospitals fails, and the 4-edition route is the capable analyst's wrong answer. Design note `## Three rules` agrees (no decoy, not semantics, not rule application). No mismatch.

## Stump power (Gate F)
Thread: both easy routes (sign-in split, 4; pooled replay, 5) are plausible to a strong analyst who read every file; neither is refuted by a stated rule; no memo names the selection effect.
Stage 4 scored readers on this same pack split. One landed the call (8 editions) with a calibration on signed-in WebKit browsers stratified by edition, cookie age and sessions per identifier. One missed (4 editions, the sign-in split). An earlier round's reader using the same calibration pooled across editions filed 9. So the call is reachable but not by default, and the calibration's stratification is where readers diverge: one of two scored readers on this pack was stumped.

## Findings, ranked
1. Residual fork (non-blocking, thread's own risk): the 8/4 call over the 4 and 5 variants rests on a selection argument (meter in the same capped storage) that the files support only through computed facts (1.25 vs 1.60, 1.99 vs 1.51), with no filed numeric test. The thread accepts it as forced. The scored 9 filing shows the calibration route can also move the count, so the golden's closure should stay stated in submission.md's derivation.
2. Ask-side inferred corrections (451 re-dated starts, add-edition clicks): data semantics, permitted for asks, strongly corroborated.
3. Optional, solution only, no rerun: state the 451 re-dated subscription rule and the add-edition click rule explicitly in the write-up as reconstruction steps.

## Next action for the author
Proceed to ship; optionally add the two reconstruction rules from finding 3 to submission.md's solution steps without changing any figure.
