# determinism-check report, task179, 2026-10-28

## Verdict
NOT_DETERMINISTIC (external_dependency), confined to the enrolment-days supplementary answer. The main call (500) is forced and reproduces. No SOLUTION_WRONG on the main call; the January enrolment-days cell does not reproduce.
**Disposition:** FIX_NOW (differs from the thread's SEND_BACK; reasoning below). One re-judge after the fix.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Judge thread (verdict at /tmp/determinism-check-task179-1793162456/verdict.md) found that the 500 forecast reproduces (my-feature logistic 498.4, stratified 481.6, recency-aware 513 to 522.7; caseload-only route about 400 to 414), and that 7,688 / 5,676 / 30.6% vs 4.5% reproduce. The zones (143, all months) reproduce. Enrolment days reproduce for Feb and Jun to Dec; Mar to May only under one reading of a same-day SUSPEND/RESUME; January is 6,247 against golden 6,256.

Disposition reasoning. The judge prompt's taxonomy: FIX_NOW = every defect repairable in-house with no model rerun (solution regeneration or rewording, a config or data-dictionary pin that only fixes what the correct count IS), analytic surface solvers work against unchanged. SEND_BACK = regenerating behavioural or ledger data, closing a fork in the story itself, widening a decisive margin, or hardening that changes what solvers see; it also says NOT_DETERMINISTIC is only "normally" SEND_BACK. Here: (a) the main call is forced and Gates G and H pass, so the decisive step and the forecast surface are untouched; (b) the offset/DST fork is closed by one sentence in Schedule C or the Keswick header (a pin that fixes what the correct count is, golden already uses Chicago-style DST); (c) the same-day ordering fork is closed by one sentence in C.4, again matching the golden's reading; (d) January is a solution-block correction or a stated rule. None regenerates data or changes the main-call analytic surface, so this is FIX_NOW, not a SEND_BACK of the architecture. Conditions that would convert it to SEND_BACK: the January 9-day gap needs changed device-event or jail data to close, or the pins would hand a solver something on the forecast. A re-judge is required after the fix because Schedule C text changes what solvers read.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Caseload 31 Dec 2026 | 7,688 | 7,688 | yes |
| Category V new-arrest bookings 2018-2026 | 5,676 | 5,676 | yes |
| Victims on caseload 2026 / 2025 | 531 / 209 | 534 / 207 (report date), 532 / 211 (occurred) | approx; match key and date field unpinned, forecast unaffected |
| Next-year Cat V rate, victims vs rest | 30.6% / 4.5% | 30.6% / 4.46% | yes |
| Model without victims | 413.8 | 408.7 | approx |
| Model with victims | 494.4 | 498.4 (481.6 to 522.7 across estimators) | yes, rounds to 500 |
| Enrolment days Feb, Jun-Dec | golden | match (Chicago DST) | yes |
| Enrolment days Mar-May | golden | match only if client 9146983's same-day suspend/resume is a sub-day suspension | conditional |
| Enrolment days Jan | 6,256 | 6,247 | NO (total 75,749 vs 75,758) |
| Zones by month (143) | golden | match exactly | yes |

## Competing answers that survived
1. Merrow offset/DST unstated: fixed UTC-6 moves April -1, Aug +1, Oct +1; fixed UTC-5 moves Feb +1. Shipped rule needed: UTC offset and DST rule for Merrow time (Schedule C or Keswick header). Open.
2. Client 9146983, SUSPEND and RESUME both effective 2026-03-20, RESUME logged first: effective-date-then-logged-time order leaves suspension open to the 14 May END, removing 53 days (Mar -11, Apr -30, May -12). Golden takes the sub-day reading. Open; C.4 does not pin within-day order.
3. January days 6,247 vs 6,256: rule behind the golden not found (client 8684742 C.3 treatment is one candidate, 15 days). Open.
4. Forecast margin: valid estimators 481.6 to 522.7, inside the 475 to 525 band but thin at both ends (watch item, not a fork).
5. Victim match key and date field: shifts 531 by a few; forecast unaffected (minor).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 12 / 4 (csv, xlsx, pdf, json) / HPD about 154,600 rows | yes |
| Distractors in metadata, none labelled by file name | 2+ | program_referrals csv, merrow_recidivism_brief pdf; names neutral | yes |
| Distractors unused yet weighable; none answers a graded quantity | yes | brief is statewide any-offense rearrest by MRAS level; referrals flag leaves call at 492.7 per note | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (docx, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12 monthly days + 12 monthly zones + forecast, whole numbers / nearest 50 stated | yes |
| Prompt shape, rubric 25+ criteria | yes | forecast + 24 monthly cells + components gives 25+ gradable items; rubric itself not shipped, not verifiable here | yes (by count) |
| Not LLM-generated, goldens business-real | yes | package reads as system extracts; judge found no authoring language; golden realism not re-read by me | yes (judge hygiene PASS) |

## Gate G reconciliation
Thread: forecasting, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: mechanism is linking police victim records to the caseload as a leading indicator (victimization overlap), consistent with the thread. The declared distractors (programme referrals, statewide brief) were not named by the thread as the surface read carrying the task; the thread named the caseload-only risk model (about 400 to 414) as the easy route, matching the note's 400 default. No mismatch. Gate G passes.
Gate H: domain pass, layers pass, decisive_step analytical. Design note's Three rules lines (No decoy, Not semantics, Not rule application) agree: the note's easy route is 400, the call is 500 only after matching two agencies' records of one person, and no filed rule says victims are higher risk.

## Stump power (Gate F)
Strong on the main call: caseload-only base rate or risk model gives about 400 to 414; 500 needs the fuzzy join of HPD victims to the caseload, validating the lift on past year ends and noticing the 2026 victim surge (about 2.5x usual). The decisive step is a research-grade covariate link, not the field's textbook route, so it is not a landable standard method. Watch the 475/525 margin on valid estimators. The enrolment-days asks add work but are currently exposed to the three forks above.

## Findings, ranked
1. Merrow UTC offset and DST rule absent from the package (Gate B); changes 1 day in several monthly cells under fixed-offset readings.
2. Same-day SUSPEND/RESUME order for client 9146983 unpinned; moves Mar/Apr/May by 11/30/12 days.
3. January enrolment days 6,247 vs golden 6,256, rule not found (Gate A).
4. Forecast margin thin at both ends of valid estimators (optional).
5. Victim match key and date field unpinned (minor, forecast unaffected).

## Next action for the author
Add to Schedule C (C.2 and C.4) one sentence stating Merrow time's UTC offset and DST rule and one stating that within an effective date a suspend and resume are taken in event order (or the sub-day suspension rule), then show the rule that yields January 6,256 or correct it to the literal figure in both goldens and submission.md; rebuild twice byte-identical and re-judge once.
