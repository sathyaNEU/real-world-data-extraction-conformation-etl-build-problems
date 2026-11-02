# determinism-check report, task247, pass 3, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose sonnet/medium judge, scratch /tmp/determinism-check-task247-pass3/ (target.zip md5 a84fab8e0c0491b4930ac9cf942b8dc4). Source: its verdict.md.

## Why
The main call (nine sites at Alert Level 2: PB06, PB07, PB09 to PB15) follows from the filed estimand (season maximum on the reprocessed record, 84-day DHW of HotSpots at or above 1.0, thresholds 4 and 8). The 2018 to 2026 back-test separates the candidate estimators, so one survives. Declared levels come straight from the bulletins workbook. All 16 logger-hours figures reproduced to the hour. The site of every deployment and the log's clock are each fixed to one reading by the shipped data. The clock also has a filed header (eml -0500); the pre-August-2025 pin map is fixed by the data only, with no filed sentence.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| NRT minus reprocessed, observed days 2018-2026 | 0.06 | 0.0595 | yes |
| Refill RMSE / hot-day bias | 0.065 / -0.001 | 0.0648 / -0.0009 (n=1,174) | yes |
| Flag-mean-corrected RMSE / hot-day bias | 0.142 / -0.263 | 0.1425 / -0.2633 | yes |
| Raw NRT hot-day bias | -0.270 | -0.270 | yes |
| Declared levels, 16 sites | filed list | bulletins 1 to 27, highest level in 1 Jun-31 Oct | yes, 16 of 16 |
| Season max DHW, 16 sites | 3,5,2,6,5,9,11,7,10,12,13,10,12,9,11,6 | 3.105, 4.944, 2.041, 6.072, 5.024, 8.851, 11.061, 6.961, 10.001, 11.977, 12.994, 9.902, 12.251, 9.012, 11.020, 5.961 | yes, 16 of 16 (none within 0.05 of 4 or 8) |
| Logger hours PB01 to PB16 | 3584, 2783, 3333, 4678, 4074, 2859, 4412, 3188, 2565, 4338, 3743, 4350, 3413, 3862, 3757, 3683 | identical, all 16 | yes, 16 of 16 |
Source fields: NRT extract (latest issue, flag by version), reprocessed CSV, climatology CSV, watch_sites_register.csv (mmm_c), bulletins xlsx, logger_log, logger_pin_register, logger_readings (windows deployed to retrieved, serial match, June-October 2024-2026, temperature at or above mmm_c in whole hundredths; ties 34 to 96 per site).

## Competing answers that survived
Logger hours, site of each deployment. Reading A: apply logger_pin_register.csv to every deployment; this moves 15 of 16 sites (PB01 -419, PB02 -255, PB03 +111, PB04 -503, PB05 +55, PB06 +318, PB07 +49, PB08 +524, PB09 +186, PB10 +470, PB11 +99, PB12 +9, PB13 +424, PB14 -778, PB15 -89, PB16 -218). Reading B (golden): register tags from the four trips beginning 18 August 2025; for the five earlier trips the site is the stop's place in the identical north-to-south route. The judge refutes A with the data: optimal assignment of logger daily means to pixel SST gives 16 of 16 pins at the golden site on the early trips (0 of 16 at the register's), 16 of 16 at the register's site from August 2025; B fits 37 of 48 early deployments better (0.15 vs 0.21 C); a reverse route fits worse (0.216). The judge does not count A as a fork, but it states this is "the one place where a literal reader and the golden differ": no filed sentence says the early tags differed. The `checked` column (12 to 15 April 2027) dates the register only as of April 2027, so the early map is a reconstruction.
Logger hours, clock. Marked UTC times read as local would add exactly +5 hours to each of the 16 figures. Refuted by the eml -0500 header and by the warm out-of-water jump in the readings landing five hours after the converted time. The April 2026 UTC marks fall outside the season windows.
Main call. Estimator forks tried (0.0595 vs 0.06; interpolating anomaly vs SST) change no level and no rounded value (PB16 5.79 vs 5.96, both 6). The uncorrected-anomaly refill is refuted by the back-test.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, pdf, xlsx, eml) | yes |
| Large file | 25,000 rows or more | 425,836 (logger readings) | yes |
| Distractors | 2 or more in metadata.json, none named by file name | 4 listed (kd490 monthly, port tide gauge, 2023 slates, 2023 protocol); none labelled in a file name | yes |
| Distractors unused yet weighable | yes | judge: present, no site heat-stress figure from them | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states DHW nearest whole number, hours whole numbers | yes |
| Prompt shape and 25+ rubric criteria | identifiable, 25 or more | shape 01 recorded in metadata; rubric criteria count not computed by me (rubric is portal-generated); 16 sites x 3 + 16 hours + list, count, chart gives ample surface | not verified, likely |
| Reads as real, not LLM generated | yes | judge: no authoring disclosure or benchmark language; goldens not separately read by me | judge pass |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and pipeline stump: NRT corrected by the flag-mean differences files three Level 2 sites (PB07, PB09, PB10); refilling gaps from the observed days either side files nine. Same stump, same numbers (the judge's critical components 1 to 3 reproduce it). The judge does not name the declared distractors as the surface read, and none carries the call. No mismatch. Note: the design note's `## Three rules` carries No decoy, Not semantics and Not rule application lines (lines 137 to 154).

## Stump power (Gate F)
Good. The easy routes (NRT as issued, or NRT less the flag-mean difference) understate the unobserved warm days and file the wrong level at six to seven sites and a list of 3 to 5; a solver who cleaned the flag recoding and re-issues still files the wrong list unless it back-tests a refill. The judge classes the decisive step analytical, and this is not the textbook-method case: the judge reached the refill by the filed back-test, not by applying a standard method. The logger ask adds a second reconstruction (re-tagged early pins and a mixed clock) on which a solver who trusts the register scores wrong at 15 of 16 sites.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: version-dependent flag recoding, re-issues, kelvin, UTC against local clock, re-tagged pins. Layer 2: back-testing the refill against the reprocessed record. The pin and clock devices sit only on the asks, which are free of the rule.

## Findings, ranked
1. Residual, non-blocking: the pre-August-2025 pin-to-site map is determinate from the logger temperatures but has no filed sentence behind it. The `checked` column fixes only the April 2027 tags. A literal reader files reading A; the judge treats the files as refuting A. If the portal reads this as an open fork, it lands on the logger-hours ask only (asks are not bound by the semantics rule), and the main call and the 16 DHW figures are untouched.
2. Pass 2's two unfiled conventions are closed: the clock by the UTC marks plus the eml -0500 header and the readings' jump; the site by the data only.
3. Rubric criteria count not checked by me.

## Next action for the author
Ship as is. Optionally, if you want the early pin map closed in words, file it in a file solvers see (a change to what solvers read, so it needs a rebuild and a fresh re-check); otherwise no step.
