# determinism-check report, task137, 2026-10-26

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
(Judge thread: one pass, sonnet medium, fresh unzip at /tmp/determinism-check-task137-20261026T142655/target/, verdict at /tmp/determinism-check-task137-20261026T142655/verdict.md.)

## Why
2025-26 GP arrivals at the walk-in clinic (seen 38,386 plus turned away 1,345 = 39,731) understate underlying demand, because practices with their own phlebotomy clinics keep patients in-house in the week after a run-out. The data separates it: lag coefficient about -0.21 overall, about -0.40 in LES-practice arrivals and about -0.03 in the rest. Removing it gives 41.6k to 41.8k, 44.4k to 44.8k grown, and every fitted specification rounds to 45,000 (band 43,750 to 46,250). The naive routes give 42,500 and 40,000.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| GP seen 2025-26 | 38,386 | 38,386 (queue_events CHECKED_IN, GP, UTC to UK date; matches annual report) | Yes |
| GP turned away | 1,345 on 58 days | 1,345 on 58 days (two text-date rows included, 10 and 44) | Yes |
| Underlying demand | 41,714 (coef -0.210) | 41,663 (coef -0.209) | Approximate, 51 visits off, plan unmoved |
| Grown 2 years at 3.5 per cent | 44,685 | 44,630 | Yes, both round to 45,000 |
| Asks 2 and 3, chart | as filed | per verdict.md, reproduced; Cardiology Q1 is 1,685 on visit date against 1,690 on request date | Yes, minor fork on a free ask |

## Competing answers that survived
- Seen plus turned away, 42,500: closed by "underlying demand", a hub that never runs out, and the lag effect (z about -15, only in LES practices). This is the intended wrong route, not a fork.
- Booked GP patients: the annual report says the hub takes "walk-in and booked", but no booked volume ships. The walk-in basis is the only computable one. Minor residual (Gate E).
- Quarter definition (financial quarters assumed) and visit date against request date: affect a few free-ask cells only.
- Chart week bucket unstated; graded on shape.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | Yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, json) | Yes |
| Large file | 25,000 rows or more | 311,893 rows (queue events) | Yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | survey csv, session plan xlsx; neither names itself a distractor; neither answers the graded quantity | Yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png) | Yes |
| Asks | multi-dimensional, unit and rounding stated | plan, 7 specialties by 4 quarters, 4 quarters of days and rates, chart; prompt fixes precision | Yes |
| Prompt shape and 25 or more criteria | identifiable; 25+ | shape recorded as "other"; about 36 graded ask figures plus components; the generated rubric count is not verifiable here | Yes, count unverified |
| Reads as real work product | yes | judge found real-looking artifacts, no authoring disclosures | Yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read no, sole_data_defect no. Design note and card: stump_class analytical; the stump is taking seen plus turned away (39,731, 42,500) as demand when LES practices keep patients in-house after run-outs, recovered only from the lagged-run-out arrival model. These match. The declared distractors (patient survey, hub session plan) are not named as the surface read; the surface read is the pooled count. No finding on distractor load.
Gate H: domain pass, layers pass, decisive_step analytical. The card's analyst_test and domain_test agree: a strong analyst who cleaned and read everything files 42,500. The design note's Three rules lines are consistent with the thread.

## Stump power (Gate F)
Judge: Good, with a caveat that "underlying demand" is a mild cue so some strong runs will find the lag. The scored readers bear this out on the call. Reader A (Sonnet) filed 42,500 on seen plus turned away and hit 8 of 36 ask figures. Reader B (Opus) filed 42,500 on run-out days completed from the arrival profile (39,900 grown) and hit 36 of 36 ask figures. Both missed the call; the ask layer was held by Reader A only at 8 of 36, though Reader B cleared it (the main thread weighs the ask-layer bar, since a 36 of 36 reader sits well above it). The method (a count model on a lagged capacity effect) is a textbook demand-planning route, so a strong solver can take it; the readers did not.

## Findings, ranked
1. Ask layer: Reader B reached 36 of 36 (clinic-code weekday mapping and long-term sickness expansion). This is a rubric-pressure concern for the main thread, not a determinism defect.
2. Critical component 3 (41,714) is specification-sensitive: judge refit gives 41,663. Optional fix: quote it as about 41,700 or state the exact specification. Does not move the plan.
3. Booked GP patients are not quantified anywhere; optional prompt clause that booked patients are planned separately, which needs a rerun.
4. Minor free-ask forks: quarter definition, visit against request date (Cardiology Q1 1,685 against 1,690), chart week bucket.

## Next action for the author
Ship as is, or optionally reword critical component 3 in submission.md as "about 41,700" with the specification stated (no data or golden change); weigh Finding 1 with the scored readers.
