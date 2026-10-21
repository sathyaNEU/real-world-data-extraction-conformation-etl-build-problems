# leak check, task125

**Verdict: REVIEW.** 12 files read, 56 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: change, measured, decisive, asserted, sentence, population, intakes, estimator, golden, statistics, effect, records, weights, quarters, households, instruction, carried, architecture, controls, application, recruitment, driver, different, release, telephone

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `extract_notes_2026-10-20.md`: 8 of 25 stump-paragraph terms appear (change, population, intakes, statistics, records, controls); read whether the document names the move
- **REVIEW** `field_instruction_FI-2024-03_call_pattern.pdf`: 4 of 25 stump-paragraph terms appear (statistics, instruction, application, telephone); read whether the document names the move
- **REVIEW** `field_instruction_FI-2026-04_first_interview_visits.pdf`: 4 of 25 stump-paragraph terms appear (change, statistics, instruction, telephone); read whether the document names the move
- **REVIEW** `hls_data_dictionary.md`: 4 of 25 stump-paragraph terms appear (intakes, statistics, application, telephone); read whether the document names the move
- **REVIEW** `hls_methods_note_2025.pdf`: 11 of 25 stump-paragraph terms appear (change, population, intakes, statistics, weights, quarters); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read, wave 8 audit of every shipped build (2026-10-20)

The reader held only a fresh unzip of `target.zip` and `prompt.txt`, with the figure names (not values)
from `generator/figures.json`, and was scored by `.claude/skills/leak-check/score_reader.py`.

### Gate F has failed on this build, measured

| block | hit |
|---|---|
| main call | **2 of 2** |
| ask figures | **38 of 53** (71.7 per cent) |

It filed both shares of the rise exactly and the whole five-quarter gap profile with it, including the peak quarter and the fade. It built the decisive construction correctly: apply the cap to the last full quarter collected before the change and re-run the estimation, then remove households only in the waves a capped intake occupies in each target quarter, which is what makes the gap rise and then fade. It listed the wave sets per quarter and confirmed its own pipeline by reproducing the file weights and both published rates.

Asked what sent it there, it quoted the methods note's section 5 verbatim, that the effect of a change is measured by applying it to the last full quarter collected before it and re-running the estimation as in section 4, and section 1 for the overlapping-intake structure that gives the wave logic. That is readability screen test 1 in its strongest form: the pack states the method.

```
== call figures ==
HIT  cap_share_of_rise_points           golden "0.22"                     reader 0.22
HIT  labour_market_share_of_rise_points golden "0.05"                     reader 0.05

== ask figures ==
HIT  cap_share_of_employment_change_points golden "-0.74"                    reader -0.74
HIT  change_employment_rate_points      golden "-0.65"                    reader -0.65
HIT  employment_fall_points             golden "0.65"                     reader 0.65
HIT  employment_rate_2026Q3_without_cap golden "60.10"                    reader 60.1
HIT  employment_rate_below_six_visit_rate_points.Apr-Jun 2027 golden "0.93"                     reader 0.93
HIT  employment_rate_below_six_visit_rate_points.Jan-Mar 2027 golden "1.11"                     reader 1.11
HIT  employment_rate_below_six_visit_rate_points.Jul-Sep 2026 golden "0.74"                     reader 0.74
HIT  employment_rate_below_six_visit_rate_points.Jul-Sep 2027 golden "0.63"                     reader 0.63
HIT  employment_rate_below_six_visit_rate_points.Oct-Dec 2026 golden "1.37"                     reader 1.37
HIT  employment_rate_gap_points.Apr-Jun 2027 golden "-0.93"                    reader -0.93
HIT  employment_rate_gap_points.Jan-Mar 2027 golden "-1.11"                    reader -1.11
HIT  employment_rate_gap_points.Jul-Sep 2026 golden "-0.74"                    reader -0.74
HIT  employment_rate_gap_points.Jul-Sep 2027 golden "-0.63"                    reader -0.63
HIT  employment_rate_gap_points.Oct-Dec 2026 golden "-1.37"                    reader -1.37
HIT  first_interview_visits_2026Q3_intake.Carrowdene golden 2360                       reader 2360
HIT  first_interview_visits_2026Q3_intake.Dunmarrow golden 1212                       reader 1212
HIT  first_interview_visits_2026Q3_intake.Haskvale golden 1737                       reader 1737
HIT  first_interview_visits_2026Q3_intake.Pellard golden 1856                       reader 1856
HIT  first_interview_visits_2026Q3_intake.Tirrin golden 1469                       reader 1469
HIT  first_interview_visits_2026Q3_intake.Velmouth golden 3945                       reader 3945
miss gap_tolerance_points.employment    golden "0.15"                     reader 0.03
miss gap_tolerance_points.unemployment  golden "0.05"                     reader 0.03
HIT  labour_market_share_of_employment_change_points golden "0.09"                     reader 0.09
HIT  published_employment_rate_2026Q2   golden "60.01"                    reader 60.01
HIT  published_employment_rate_2026Q3   golden "59.36"                    reader 59.36
HIT  published_unemployment_rate_2026Q2 golden "4.99"                     reader 4.99
HIT  published_unemployment_rate_2026Q3 golden "5.27"                     reader 5.27
HIT  rise_unemployment_rate_points      golden "0.27"                     reader 0.27
miss template_quarter                   golden "Apr-Jun 2026"             reader "2026Q2"
miss total_weekly_hours_thousand.Carrowdene golden "16009.7"                  reader 15954.9
miss total_weekly_hours_thousand.Dunmarrow golden "8103.1"                   reader 8075.3
miss total_weekly_hours_thousand.Haskvale golden "11070.1"                  reader 11032.1
miss total_weekly_hours_thousand.Pellard golden "12455.6"                  reader 12411.9
miss total_weekly_hours_thousand.Tirrin golden "9858.6"                   reader 9825.4
miss total_weekly_hours_thousand.Velmouth golden "27055.5"                  reader 26963.2
miss unemployed_to_employed_counts.Carrowdene golden [37, 121]                  reader 37
miss unemployed_to_employed_counts.Dunmarrow golden [19, 70]                   reader 19
miss unemployed_to_employed_counts.Haskvale golden [40, 102]                  reader 40
miss unemployed_to_employed_counts.Pellard golden [39, 110]                  reader 39
miss unemployed_to_employed_counts.Tirrin golden [27, 94]                   reader 27
miss unemployed_to_employed_counts.Velmouth golden [72, 234]                  reader 72
HIT  unemployed_to_employed_share_pct.Carrowdene golden "30.58"                    reader 30.58
HIT  unemployed_to_employed_share_pct.Dunmarrow golden "27.14"                    reader 27.14
HIT  unemployed_to_employed_share_pct.Haskvale golden "39.22"                    reader 39.22
HIT  unemployed_to_employed_share_pct.Pellard golden "35.45"                    reader 35.45
HIT  unemployed_to_employed_share_pct.Tirrin golden "28.72"                    reader 28.72
HIT  unemployed_to_employed_share_pct.Velmouth golden "30.77"                    reader 30.77
HIT  unemployment_rate_2026Q3_without_cap golden "5.04"                     reader 5.04
HIT  unemployment_rate_gap_points.Apr-Jun 2027 golden "0.19"                     reader 0.19
HIT  unemployment_rate_gap_points.Jan-Mar 2027 golden "0.25"                     reader 0.25
HIT  unemployment_rate_gap_points.Jul-Sep 2026 golden "0.22"                     reader 0.22
HIT  unemployment_rate_gap_points.Jul-Sep 2027 golden "0.07"                     reader 0.07
HIT  unemployment_rate_gap_points.Oct-Dec 2026 golden "0.37"                     reader 0.37

call figures   2 of 2 hit
ask figures    38 of 53 hit (71.7 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```

**The repair:** the methods note states the decisive method in its own words, so executing it is rule application rather than analysis. Re-root at stage 1: that section goes, and the reason to re-run on the pre-change quarter has to come from the data's structure.
