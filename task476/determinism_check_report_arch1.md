# determinism-check report, task476, 2026-10-20 (pass 1, architecture 1)

## Verdict
DETERMINISTIC, SOLUTION_WRONG (supplementary: days statistic)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: etl_conformance, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: yes

## Reconciliation
Gate H: decisive_step rule_application. Guidelines 3.2 filed the estimand as the rate for the area the 2020 tract covers, and the block relationship file with the block-group table left only execution; stage 4 reader B landed the call and all 140 tract figures on that path. The card's stump_class analytical does not survive the judge's reading, so architecture 1 is spent (build-pipeline: SEND_BACK re-roots). The days finding is real: the prompt asked for the median, the guidelines and the golden the average.

## Thread verdict (verbatim)

# Verdict, task476, run r1

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (supplementary question 2, days column).
- **Disposition:** SEND_BACK. Gate H3 fails (the decisive step is stated-rule execution), and the days statistic conflicts between prompt (median), guidelines 4.2 (average) and the golden (average). Closing that conflict means editing the prompt or the guidelines PDF, so a rerun is required.

## Why
The main call is forced. Literal execution of guidelines 3.1/3.2 gives Dunmore Heights 3 and Kestrel Park 3 qualifying tracts. Linden Row has 2, Calloway Flats 1 and Sorrel Bend 1. The nearest margins are far from the line: the qualifiers' lowest z is 3.04 (tract 402) and the non-qualifiers' highest is 1.06 (tract 404).

The golden's days figures (190, 196, 167, 140, 253) are AVERAGES. The prompt asks for the MEDIAN days. The medians from the shipped files are 80.5, 115, 104, 85 and 108. Guidelines 4.2 says "average", so prompt and guidelines disagree and the golden follows the guidelines against the prompt. Calloway Flats' median of 80.5 also leaves a half-rounding fork against "whole numbers" (80 or 81).

Gate H3 fails because the filed rule ("the rate for the area the 2020 tract covers") plus the shipped block relationship file leaves only execution.

## Evidence (recomputed from target/)
| Item | Result |
|---|---|
| 2019-2023 and 2014-2018 rates, MOEs and z for all 28 tracts | Reproduce to the golden's rounding. The 2014-2018 values for the split tracts are rebuilt from 2010 block groups, e.g. 403.02 = 9.53% (z 4.29), 303.01 = 28.86% (z 0.56), 403.01 = 33.3%. |
| Qualifying tracts per neighborhood | 1, 3, 3, 2, 1, as in the golden. Same under tract-level or block-group 2014-2018 rates for unsplit tracts, and under a ratio-formula MOE. |
| Open housing cases on 31 Dec 2026 (event history; 28 cases closed in 2026 and reopened in 2027 count as closed; residential land use; prior-parcel-ID lookup for 24 older cases) | Properties 24, 25, 31, 27, 21 reproduce. |
| Mean days | 190.2, 196.4, 166.6, 139.7, 252.6, matching the golden's "average". |
| Median days | 80.5, 115, 104, 85, 108. These are what the prompt asks for. |
| Grant dollars and properties (2026 posting, positive checks not reversed, reissues counted, 2026 checks voided in 2027 excluded) | $135,908 / 8, $323,355 / 12, $335,719 / 16, $474,212 / 18, $220,471 / 9 reproduce. |

Surviving forks:
- **Parent-tract route.** Using the 2010 parent tract for 403.02 (19.1%) and 303.01 (17.8%) gives Dunmore Heights + Linden Row, not Kestrel Park. Guidelines 3.2 rules it out, so this is the stump route, not a fork.
- **Days statistic.** Average gives 190/196/167/140/253. Median gives 81 (or 80)/115/104/85/108.
- **Cash-basis grant dollars.** Netting all 2026 rows, including voids of 2025 checks and 2026 checks voided in 2027, gives different dollars (e.g. Sorrel Bend $217,478, Dunmore Heights $359,007). The guidelines do not define "paid". The golden's reading (a voided check was never paid) is the more natural one, but it is not pinned.
- **Tract 404.** A 2.5% sliver of a 2010 block group from tract 405 means 404's boundary differs. The golden uses the whole 404 tract (22.3%). The block-group route gives 18.9%. The qualification result is the same either way (z about 1).

## Files/Hygiene: PASS (no exclusion-level finding)
- **Count and formats:** 14 files in 5 formats: csv (8), xlsx (2), pdf (1), pipe-delimited txt (2), notes txt (1).
- **Realism:** the sources are real-style (ACS tables, Census relationship files, county case, parcel and payment extracts). The one-row-per-case and event files and the register carry realistic noise (re-keyed parcels, mixed date formats, voids).
- **Provenance:** no authoring or benchmark disclosure. The extract notes read as a system README.
- **Temporal coherence:** the extract date of 15 Mar 2027 is after every decisive date.
- **Contamination:** none.

## Stump power
The parent-tract shortcut (Kestrel Park fails at 19.1%, Linden Row passes at 17.8%) is what a capable analyst would plausibly file: Dunmore Heights + Linden Row, and it is wrong. It needs the block relationship file to recover. Stump power is real but procedural. The open-case status trap (the closed_date column versus event history) and the void/reissue handling add ask-level difficulty.

## Stumping type
`mechanism: etl_conformance`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: yes`.
The difficulty is rebuilding the 2014-2018 rate on the 2020 tract geography. On clean data with no boundary change the task would reduce to a routine significance count, so the geography harmonisation carries it.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: rule_application`.
- **Domain:** testing significance of ACS poverty change against margins of error is the field's own analysis.
- **Layer 1:** tract splits and re-keyed parcels. **Layer 2:** the change test across a boundary change.
- **Decisive step:** guidelines 3.2 files the estimand ("the rate for the area the 2020 tract covers") and the formulas, so a strong analyst who read every rule correctly rebuilds from block groups and gets the golden. The parent-tract route breaks the stated rule, not the analysis. H3 is borderline and fails on the test.

## Fix
- **Solution:** regenerate the days column as medians, with a pinned rounding for 80.5.
- **Prompt or input_files:** make "median" and "average" consistent between prompt.txt and guidelines 4.2, and pin "paid" (checks issued and not voided).
- **H3:** re-root so the decisive step is an analysis the filed text does not execute for the solver, for example a validated method choice rather than a stated crosswalk rule.
