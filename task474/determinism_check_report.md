# determinism-check report, task474, 2026-10-20

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged against the verdict as written (/tmp/determinism-check-task474-r1/verdict.md, one thread, no retry). The pack was regenerated after the thread ran (the two ask devices re-sited, the overstated critical component removed; main call and designated set unchanged). That regeneration was not re-judged and not re-verified here; the forced-outage fork below is recorded as the thread found it.

## Why
Rule 2.2 defines the rate as the NOx the unit emitted in all its operating hours, so the blank-NOx hours (about 6 percent of operating hours, 44 percent of first-hour-after-start hours) must be estimated. Measured NOx is 273, 182 and 97 lb in hours 1, 2 and 3 after a start against about 6 lb steady, so a load fill cannot represent start hours. Filling from the same unit's measured hours at the same hour after a start gives 7 of 9 units at or above 0.170, with clear margins (lowest designated 0.183, highest non-designated 0.101). Robust to the cutoff (2 to 8 hours), a constant steady-level fill and season-only against year-long hour-after-start means.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Season MWh and operating hours, 9 units (e.g. AF-1, CB-1) | 162,546 / 1,027; 116,713 / 732 | same, all 9 | yes (dahs_hourly_export_2026.csv, GLOAD_MW, OP_TIME) |
| Designated set under the hours-since-start fill | 7 (AF-1, AF-2, CB-1, DF-1, DF-3, SR-1, SR-2) | same 7; rates .188 .228 .259 .101 .183 .099 .188 .187 .186 | yes |
| Fuel cost, 9 units and total | $32,743,332 | same to the dollar; every hour finds an invoice; ignoring DST gives other dollars (AF-2 $3,152,253) so agreement Section 1 pins it | yes |
| Forced outage hours (union of overlapping events) | 1,283 total | union reproduces; "latest report supersedes" gives 1,262 | yes under the literal union; fork open in the thread's reading |
| Critical component 2, load fill designates 3 (AF-2, CB-1, SR-1) | 3 | model-dependent (linear/quadratic on the full year gives the 3; 10 MW-bin mean puts AF-1 at 0.1713; cubic 0.1682; fit on hours after 3 gives AF-2, SR-1) | no (component since removed from the block) |

## Competing answers that survived
- Forced-outage overlaps: union of hours (golden) against "latest report supersedes" (1,262 total, e.g. AF-1 60 against 63). Supplementary figures only. Coordinator reports rule 3.2 "the later report stands" now closes it in the regenerated pack; unverified by me. If so, the filed rule reads supersede and the golden's 1,283 union no longer matches; the regenerated submission must be checked against the rule as filed.
- Fleet-pooled hour-after-start means drop DF-1 to 0.151: weak fork, the data show units differ and the design note's SF7 closes it as same-unit.
- Measured-only fill (2 designated: AF-2, SR-1): not the quantity rule 2.2 names, not a literal reading.
- None of these changes the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, txt) | yes |
| Large file | 25,000 rows or more | dahs_hourly_export_2026.csv, 90,792 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | ambient_ozone_daily_2026.csv, nox_allowance_holdings_2026.xlsx named; file names do not label them; the maintenance tickets file is a further noise file | yes |
| Distractors relevant, unused, none answers a graded quantity | yes | ambient ozone and allowance holdings weigh as air quality and compliance position, neither yields a unit rate; thread found none carrying the call | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | xlsx grid of 9 units x 5 figures with whole MWh, whole hours, nearest dollar; PDF names set and chart | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 07 grid; 9 units x 5 figures plus call, count, designations and chart comfortably exceeds 25 (generated rubric not inspected) | yes (inferred) |
| Not LLM-generated, goldens real work product | yes | thread saw no authoring leakage; golden realism not re-read here | yes (thread) |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 estimation_fit, mechanism method_or_model_selection, decisive step filling by hours since start, no decoy, no planted defect. Match. The declared distractors (ambient ozone, allowance holdings) are not named by the thread as the surface read; the surface read is the load fill, which is the declared default path (AF-2, CB-1, SR-1). Design note's "Ends on" reproduces as 3 units under a linear/quadratic load fit; the thread shows it is model-dependent for AF-1, but every variant under-designates.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note Three rules agree: Layer 1 clock bases, blanks, re-reported GADS events; Layer 2 a CEMS missing-data substitution respecting start-up behaviour. No mismatch.

## Stump power (Gate F)
Good per the thread: the easy routes (drop blanks, scale by measured share, load fill) give 2 or 3 units against 7, and the start-hour profile is in the data's own measured hours. Caution for the main thread: hours-since-start conditioning is the standard CEMS missing-data idea and a strong solver may reach it by validating a fill against measured start hours; the decisive step required judgment the data settles, so it is not rule application, but blind-reader results should weigh the 1.3 stumping figure.

## Findings, ranked
1. Forced-outage overlap convention (supplementary only): union against supersede. Coordinator reports the regenerated pack files "the later report stands"; confirm the regenerated golden uses it (the thread's 1,262 total, not 1,283).
2. Critical component 2 overstated (removed by regeneration, nothing further).
3. Fleet-pooled start-hour fill moves DF-1 to 0.151; weak, closed by SF7.

## Next action for the author
Confirm the regenerated submission.md and golden forced-outage hours follow rule 3.2 "the later report stands" (supersede, about 1,262 total) and that the removed component leaves the block consistent; then proceed to ship, no re-judge needed for the main call.
