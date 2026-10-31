# determinism-check report, task245, pass 3, 2026-10-31

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (informative missingness, rebuild of lost days), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (fresh unzip of target.zip 7987c653 at /tmp/determinism-check-task245-20261031172746/target/, blocks inlined, judge system prompt verbatim) executed the prompt and AQ-QP-04 s5.1 and s5.2 literally. Every graded value reproduced. The call (TBT1, TH3, TBT4 noted; nine not) held under every wind-aware rebuild tried (4 to 36 sectors, with or without speed and rain, other backgrounds, a multiplicative variant). Section 5.1 files the estimand and 5.2 the note rule; the data separate the rebuilds (valid means on terminal-wind days 54 to 82 against about 20 elsewhere, so the lost days are informatively missing). Daily means never sit on 50, so threshold and rounding forks are empty. Source: /tmp/determinism-check-task245-20261031172746/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Valid-day exceedances TBT1/TH3/TBT4 | 22/17/19 | 22/17/19 | yes |
| Lost / valid days of the three | 229 / 866 | 229 / 866 | yes |
| Terminal-wind days, lost / valid | 103 / 72 | 103 / 72 | yes |
| Mean valid-day PM10 on those days | 53.9/82.1/63.0 | 53.9/82.1/63.0 | yes |
| Whole-year TBT1/TH3/TBT4 | 57/51/51 | 56/51/51 | yes (inside 39-61, 45-58, 44-56) |
| Other nine, whole-year | 14,16,14,30,30,24,15,11,2 | 14,16,13,30,30,24,15,11,2 | yes (TBT5 13 inside 8-16) |
| NO2 annual means (six) | 19.0, 29.0, 26.3, 19.4, 15.5, 23.7 | 19.008, 29.012, 26.302, 19.384, 15.514, 23.716 | yes |
| Deposition (five gauges) | 69, 61, 60, 59, 46 | 68.8, 60.8, 59.8, 59.3, 46.3 | yes |
| Background medians on wind days | 19.9/22.2/21.0 | 19.6/21.5/21.1 | narrative only, not graded (hourly vs daily median) |

## Competing answers that survived
None. Scaling by data capture (notes TH5 37.8 and TH6 41.9), background-only fill (26/20/24) and interpolation (31/24/28) are contradicted by the shipped valid-day wind evidence. The lab's 0.0731 m2 on Frisbee periods gives 51/46/44/45/35, closed by plan s3 and the service log.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 11 / 4 (csv, xlsx, pdf, eml) / 166,776 rows | yes |
| Distractors | 2+ in metadata.json, none labelled in a file name | asr2027_table_a3_no2_2026.pdf, background_maps_2027_thornmouth_extract.csv; names neutral | yes |
| Distractor unused yet relevant; none answers a graded quantity | yes | judge: neither counts PM10 days; both weigh | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12-station, 6-station, 5-gauge grids; unit and rounding in the prompt | yes |
| Prompt shape / 25+ criteria | shape identified, 25+ | shape 10 in metadata; design note says well over 25 (not recomputed) | yes (author-stated) |
| Reads as real, not LLM generated | yes | judge: no authoring language, operational-looking artifacts; golden realism not independently re-read | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card stump_class analytical; stump sentence (scale by capture or 90.4th percentile notes TH5 and TH6; network fill or interpolation leaves the three at 31 or under) matches the thread's tested fills (26/20/24, 31/24/28, scaling 37.8/41.9). The declared distractors are not named as carrying the task. No mismatch.

## Gate H (three rules)
Thread: domain pass, layers pass, decisive_step analytical. Design note and card: decisive step is rebuilding lost hours from background plus each station's wind-sector increment (pollution rose), analyst_test and domain_test as the thread describes. The thread reached the golden by applying that rebuild with a judgment the data had to settle (informative missingness), not a bare standard method. Consistent.

## Stump power (Gate F)
Good. The easy routes file two wrong notes or none; a careful solver can reach the call by testing whether outages track terminal wind, and one that skips the missingness test fails. The main thread weighs this against the design note's ladder.

## Findings, ranked
1. None blocking.
2. Minor: TBT5 whole-year 13 against golden 14 (inside range); narrative wind-day background medians differ slightly (not graded).

## Next action for the author
Proceed to ship (stage 5) on the final cut; no repair and no rerun.
