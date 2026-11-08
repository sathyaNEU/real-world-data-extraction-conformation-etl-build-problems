# determinism-check report, task156 (architecture 4, pass 2, run r2), 2026-11-08

Target: target.zip sha256 3a6e329bfd5ddc00525353d69521854a356165e4fd26b08b2af66c1a1fccae96. One sonnet/medium thread (run by the main session), order kept: derivation.md was on disk before graded_blocks.md was opened.

## Verdict
DETERMINISTIC (residual margin risk on the two rural spur hubs, NM125 and NM162, and on the onset form)
**Disposition:** APPROVE (no FIX_NOW item)
**Stumping type:** mechanism: forecasting (regime change, onset-threshold hazard on days since power-up), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
All 30 hubs' charges and MWh reproduced exactly from the bundle (0 mismatches; no hub MWh within 0.05 of a rounding line; window edges identical in UTC and Irish time). The 12-hub list is the one the files force once the RC50's monthly cabinet service is seen to power-cycle the HX150s (HX150 Offline blips fall inside PM-RC50 work-order windows at 80 per cent of 743 visits, against 0.7 per cent of 144 at the five hang hubs) and the programme removes the RC50 at the seven standard hubs. The thread's blind first pass listed 5 hubs (own-rate route); it found the coupling only on its appendix pass after opening graded_blocks.md. That is evidence of stump power, and also means the blind derivation differed from the submission on the main call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Charges, 30 hubs (connector_status/sessions, Schedule 6) | per submission 4 | identical | yes (30/30) |
| Energy MWh, 30 hubs | per submission 4 | identical | yes (30/30) |
| Earliest HX150 hang after a power-up | day 76 | 76.4 days (87 of 98 at the five hubs after day 75) | yes |
| Five hang hubs | NM119, 131, 144, 155, 166 | same | yes |
| 12-hub list | golden | P(some unit below 99) 0.96 to 1.00 for the 12 (own simulation, after the coupling was found) | yes, on the appendix pass only |
| Motorway NM104, 112, 127 | above 99 | P 0.10 to 0.17 | yes |
| Spur NM125, NM162 | above 99 | expected per unit 99.15 and 99.33; P 0.41 to 0.48 | yes on expected availability; thin |

## Competing answers that survived
- None that lists a different set under the filed estimand. Soft forks, all weighed under (a) to (e) below: the spur hubs under an event reading, and a smooth onset curve.
- Closed in the files: record count against joined charges, tag-first drop (4 to 32 fewer charges a hub), energy from energy_kwh against the register span (0.5 to 2.6 MWh less); Schedule 6.2 and 6.3 and the data separate them.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | pdf, xlsx, csv | yes |
| Large file | 25,000 rows or more | charging_sessions_2026.csv 111,818 rows | yes |
| Distractors | 2 or more, in metadata.json, not in a file name | customer_survey_2026.xlsx, tariff_schedule_2026.pdf; names are neutral | yes |
| Distractors weigh yet unused | relevant, answer a graded quantity arithmetically if any, ruled out by a fact | neither carries an availability figure (design note says so); they are thin as distractors, nothing in them reproduces a graded quantity | soft pass (low weight) |
| Deliverables | 1 to 3, all in golden | 2 (hub_availability_2027.csv, availability_plan_2027.pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | charges (whole) and energy (MWh, one decimal) for 29 hubs, rounding in the prompt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | per-hub flag, charges and energy plus the letter list gives well over 25 | yes |
| Reads as real, not LLM generated | | thread found none; two contractor layouts and clocks, re-keyed ids, re-sent rows | yes (no finding) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card (task156.json): objective forecasting, stump_class analytical, with an analyst_test (strong analyst files 5 hubs, the own-rate route, the 7 standard hubs missed) and a domain_test (hazard on the clock that drives it, regime-dependent maintenance). Design note: mechanism gap time, Layer 2 estimation_fit, decisive step the restart clock plus the programme's removal of the RC50. These match. The declared distractors (survey, tariff) are not named by the thread as a surface read. Gate G clean: no shipped artifact ranks hubs on availability.

Gate H: domain pass, layers pass, decisive_step analytical. Matches the design note's Three rules (No decoy, Not semantics, Not rule application each carried). The thread also classed it analytical on the strength of a coupling no file states, which is consistent with the note's claim that no field records a power-up or a pillar. Stump power note for the main thread: after the coupling is found, the rest (a threshold hazard through a changed regime) is a textbook reliability forecast that a strong solver can land; the stump rests entirely on discovering the coupling, which a medium thread missed blind.

## Stump power (Gate F)
High on the blind evidence: the own-rate, pooled and 2026-carried routes file 5 or 9 hubs, none the golden. Risk is the usual one: a solver who finds the RC50 coupling lands the 12 and banks the call, so the asks must carry the ladder.

## Margins: the thread against the design note and checks.py
- checks.py/note: the closest golden forecast is 0.34 points from 99 (SF4 asserted at 0.2 or more); every true side at least 0.48; 20 of 20 redraws filed the truth's set (closest 0.10, median 0.30); under SF13 the motorway and spur hubs sit at least 99.40, 99.31 and 99.30.
- Thread: NM162 99.33 (agrees with 99.34 closest, 99.31 under the group attendance). NM125 99.15, which is 0.15 to 0.19 lower than the note's floor of about 99.30 for the spur and motorway hubs. The note itself records that day-step members sat up to 0.7 under the simulation before the part-day correction and now agree within about 0.15; the thread's 0.15 gap is of that size, a different simulation convention (callout attendance, mid-day hang onset), not a changed side. NM125 stays above 99 under every point-forecast convention that either side ran; its 0.15 margin is thin and is the single most contestable flag.
- Thread: NM135 at 99.08 (full history) or 98.81 (2024 on) exists only on the own-rate route, which is the rejected route and not on the golden. The note's SF12 window fork covers it.

## Views on (a) to (e)
(a) Clause 4.6 as the hub's expected lowest unit (E[min over units], thread 98.9 to 99.05 at the spurs) against the lowest of each unit's expected availability (SF6, golden). Would list NM125 and NM162 as well (14 hubs), perhaps not the motorway hubs. I do not rank it as a surviving answer: clause 4.6 asks for a forecast of a charge point's availability, and the expectation of a minimum is not a forecast of any charge point; the clause's per-unit wording and Schedule 4's per-charge-point standard (4.1 and the per-charge-point service credit table) fix the unit of account. The note's SF6 asserts only mean against lowest, not E[min], so E[min] is unasserted. Competing, weak: it is the nearest thing to a live fork, and only at two hubs.
(b) The event reading (probability that some unit falls below 99). At P above 0.5 it files the golden's 12 (spurs 0.41 to 0.48 stay out, motorway 0.10 to 0.17 out). Only a threshold under about 0.40 changes the list (adds the spurs; the motorway hubs stay out at 0.17). "Forecasts that ... will fall below" reads as a majority call, so it files the 12; it survives as the same call, not a competing one. A threshold below 0.4 has no support in the text.
(c) Weibull onset. The thread's P of 0.4 to 0.7 for NM104, 112 and 127 and 0.6 to 0.65 for the spurs under it would add up to five hubs under an event reading, but those are probabilities, not the point forecast; the thread did not report expected availability under it. It is ruled out by the data on fit: hazard about 0.3 a year below day 75 and about 14 a year above, with an empty band 68 to 76. The note lists a fitted onset as in the standing family giving the same 12; the thread's numbers do not contradict that on point forecasts, but they are not demonstrated either. Optional hardening, not FIX_NOW: report the point forecast under a fitted Weibull for NM104, 112, 127, 125 and 162 in checks.py as an SF member.
(d) Each unit's own fault rate against the hub's. Ordinary faults sit at roughly 0.4 a unit-year everywhere, so the units' rates differ little; SF16 closes interruptions by the log's dispersion test; NM135 and NM104 move only on the own-rate route, not on the golden. Same call, covered.
(e) Motorway visit gaps (up to 74 days) against the earliest recorded hang at 76.4 days. The gap is 2.4 days under the earliest hang and clear of the empty band; units on those hubs sit above 99 by at least 0.4 in the note. This margin is thin in days but supported by 98 hangs showing a step. It is the same risk as (c): if the onset is read earlier than 74 days the three motorway hubs (and the spurs) cross. It is ruled out by the empty band, not by any file's wording.

## Findings, ranked
1. Spur margin: NM125 at 99.15 (thread) against about 99.30 (note) on expected availability, and P(some unit below 99) 0.41 to 0.48 for both spurs. Thin, not a fork under the filed estimand. Optional: widen by making the 2027 interruption pattern at NM125 and NM162 more decisive (a rebuild that would need a rerun).
2. Weibull and E[min] readings are unasserted in checks.py; both would add the spurs. Optional addition: an SF row for each.
3. The distractors are thin (no availability content). Soft.
4. Blind pass listed 5 hubs: expected for the intended stump, noted so the main thread does not read it as a determinism failure.

## Next action for the author
No fix is needed. If the portal contests the spurs, repair by widening the NM125 and NM162 margin in the generator and rerun the free gates; before then, optionally add the Weibull point forecast and E[min] as asserted SF members in checks.py.
