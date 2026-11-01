# determinism-check report (pass 2), task229, 2026-11-01

Thread: one isolated sonnet/medium judge on a fresh unzip at /tmp/determinism-check-task229-570207/target/. It wrote derivation.md (call, grid, 12 monthly counts, 24 gauging means) before opening graded_blocks.md and reports it kept that order. Spawned by the main session because this runtime has no Agent tool; the brief was written under this contract.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Standard s3.2/s4 grade against the true mean discharge; data plan s1 fixes the published discharge as the issue-2 rating read at the day's mean level; the operating plan fixes the sub-daily hydrograph. The convex rating (b > 1) understates mean flow under peaking, so C104/C105 (Jan-Apr, Jul-Dec) and C112/C113 (from July, continuous in June) fall 14 to 32 per cent short; C107 fails the 1.5 x top-gauged rule in May and June; C124 is damped within 1 per cent. Every block figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Grid (shaded cells) | C104/C105 Jan-Apr, Jul-Dec; C107 May-Jun; C112/C113 Jul-Dec | same | yes |
| Peaking error range | 14 to 32 per cent | C104 -14.8 to -32.3 (Feb to Jul), C105 Feb -14.4 (least), C112 Jul -32.0, C113 Jul -31.0 | yes |
| C124 within 1.0 per cent | 1.0 | -0.5 to -0.95 | yes |
| C107 May, Jun vs 1.5 x 4.21 | 8.65, 9.44 vs 6.315 | same; no other station exceeds | yes |
| Monthly station-days WY2026 | 662 655 695 683 620 696 671 687 672 705 700 686 | same (June 672 with C110/C122 merged; 677 unmerged) | yes |
| Gauging means, 22 stations | C101 -1.2 ... C124 -1.5 | all 22 match to one decimal (C122 merged with C110 -1.99, -2.0); nearest rounding margin 0.02 to 0.03 | yes |

## Competing answers that survived
None changes the committed answer. Residual forks the thread listed:
1. C110/C122 merge (s7 and the register's replaced_by close it; unmerged gives June 677, C110 -2.7, C122 -1.1). The one reading a literal solver could miss.
2. The pre-April-2026 rating is not printed; it is recovered by an exact power-law fit of the daily record's level and discharge pairs (rms 1e-4). No sentence names that route. Using issue 2 for every gauging gives a different set (C117 -1.0 against -3.3).
3. GOES UTC-day labels counted by obs_date, not remapped to local days (month-edge shifts of a few).
4. No attenuation of the pulse is filed down 2.4 km (C105), 3.1 km (C113), 7 km (C124); a 6-hour damping still leaves the grid unchanged.
Optional closing sentence for fork 1 (tie C110's record to C122) would not change the analytic surface.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 12 / 4 (pdf, csv, xlsx, docx) / 39,930 rows | yes |
| Distractors | 2+ named, no file name labels one | flood_frequency_update_2025.pdf, water_quality_grab_samples_2026.csv, field_visits_wy2026.csv named in metadata.json; names do not label them | yes |
| Distractors unused yet weighable, none answers a graded quantity | | thread found none that answers a graded figure; field visits and flood frequency are plausible-looking and unused | yes |
| Deliverables | 1 to 3, all in golden | 2 (png grid, xlsx), both answered | yes |
| Asks multi-dimensional with unit and rounding | | 12 monthly counts (whole numbers), 22 station means (one decimal, per cent) | yes |
| Prompt shape / 25+ rubric criteria | | shape 13 (scenarios and flip point); 23x12 grid cells plus 34 ask figures supply well over 25 | yes |
| Reads as real, not LLM generated | | thread found operational artifacts, coherent dates, no disclosure | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (line 136) and card: forecasting, analytical_non_defect, no, no. Match. The declared distractors (flood frequency, water quality, field visits) are not the surface read; the surface read the thread names is the outlook means taken as published flows, which flags C107 alone, and that is not a declared distractor. Card stump_class analytical agrees.
Gate H (thread): domain pass, layers pass, decisive_step analytical (rating-curve convexity bias under peaking, plus the extrapolation limit; Layer 1 is the GOES/local-day, twin rows, rating change, moved station). Design note `## Three rules` and card domain_test describe the same convexity mechanism. Match.

## Stump power (Gate F)
Moderate to good per the thread. The easy route flags only C107 (five stations wrong) and a second easy route flags C112/C113 from June. The standard and data plan disclose published-versus-true and the operating plan gives the hydrograph, so a strong solver reading all of them can build the sub-daily flow; the work is analytical, not a lookup. The thread does not class the step as a textbook route a solver lands without judgment. The asks add stale-fill rows, old-rating reconstruction and local-day gaugings. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Pre-April-2026 rating recoverable only by fitting the daily record, with no filed route (ask 2); the answer is determinate but a reconstruction, not a stated rule.
2. C110/C122 merge is the one reading that moves June and two means if missed.
3. No attenuation filed downstream; the grid is insensitive to it.
4. Minor: register on_platform_since equals telemetry first_day_new; not exclusion-level.

## Next action for the author
None required; proceed with the ship checks. Optionally add one sentence tying C110's record to C122 for station counts.
