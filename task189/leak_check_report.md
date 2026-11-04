# leak check, task189

**Verdict: REVIEW.** 14 files read, 11 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: method, sample, clause, asserted, average, standard, authority, decisive, programme, points, kilcrohane, laboratory, sentence, non-detects, limits, sensitive, comparison, dictionary, schedule, reading, window, estimate, estimator, censored, qualifier

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `kilgarron_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move
- **REVIEW** `laboratory_method_schedule.pdf`: 7 of 25 stump-paragraph terms appear (method, sample, authority, laboratory, dictionary, schedule); read whether the document names the move
- **REVIEW** `lims_field_dictionary.pdf`: 7 of 25 stump-paragraph terms appear (method, sample, authority, programme, laboratory, dictionary); read whether the document names the move
- **REVIEW** `surface_water_quality_regulations_2019.pdf`: 9 of 25 stump-paragraph terms appear (method, sample, average, standard, authority, programme); read whether the document names the move
- **REVIEW** `tirneevin_quarterly_report_2025q3.pdf`: 3 of 25 stump-paragraph terms appear (sample, authority, laboratory); read whether the document names the move

## 6 ranking artifacts (INFO 2)
- **INFO** `abstraction_point_register.csv`: names 6 of 7 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `monitoring_point_crosswalk.csv`: names 7 of 7 answer-set candidates; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

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
| main call | **landed in prose (the key was left unanswered)** |
| ask figures | **see below** (n/a per cent) |

It filed four non-compliant water bodies in its prose, which is the committed call, and named them. It left the `call` key itself unanswered, so the scorer has nothing to compare; the prose is the evidence here and it is unambiguous.

It built the decisive construction: of the compliance samples a majority are below the reporting limit, one laboratory reports to twice the standard and the other to a twentieth of it, so the average turns on how the non-detects are valued, and it valued each at the mean of the same water body's own results from the sensitive laboratory. It rejected the limit, half the limit, zero and a fitted distribution, and reported which water bodies flip under each, including the one that falls just under if non-detects go to zero.

**A filed clause sent it there and it quoted the clause**, that the authority shall put the sample's own concentration at the figure the results it holds support and shall not report any property of a fitted distribution. It then said that nothing told it which imputation to use and it inferred that from which water bodies have both laboratories' points. So the clause rules out the alternatives and the data picks the survivor, which is close to a forced method.

```
== call figures ==
HIT  below_limit_total                  golden 276                        reader 276

== ask figures ==
HIT  a1_sampling.Aghavannagh.below_limit golden 18                         reader 18
HIT  a1_sampling.Aghavannagh.samples    golden 23                         reader 23
HIT  a1_sampling.Ballynure.below_limit  golden 35                         reader 35
HIT  a1_sampling.Ballynure.samples      golden 47                         reader 47
HIT  a1_sampling.Carrowbeg.below_limit  golden 18                         reader 18
HIT  a1_sampling.Carrowbeg.samples      golden 30                         reader 30
HIT  a1_sampling.Cloonfad.below_limit   golden 11                         reader 11
HIT  a1_sampling.Cloonfad.samples       golden 36                         reader 36
HIT  a1_sampling.Derryvore.below_limit  golden 25                         reader 25
HIT  a1_sampling.Derryvore.samples      golden 35                         reader 35
HIT  a1_sampling.Drominagh.below_limit  golden 31                         reader 31
HIT  a1_sampling.Drominagh.samples      golden 36                         reader 36
HIT  a1_sampling.Glasheen.below_limit   golden 19                         reader 19
HIT  a1_sampling.Glasheen.samples       golden 36                         reader 36
HIT  a1_sampling.Kilcrohane.below_limit golden 5                          reader 5
HIT  a1_sampling.Kilcrohane.samples     golden 24                         reader 24
HIT  a1_sampling.Knockanure.below_limit golden 28                         reader 28
HIT  a1_sampling.Knockanure.samples     golden 35                         reader 35
HIT  a1_sampling.Lisheenaguile.below_limit golden 16                         reader 16
HIT  a1_sampling.Lisheenaguile.samples  golden 24                         reader 24
HIT  a1_sampling.Moneycashen.below_limit golden 19                         reader 19
HIT  a1_sampling.Moneycashen.samples    golden 24                         reader 24
HIT  a1_sampling.Owenbeg.below_limit    golden 31                         reader 31
HIT  a1_sampling.Owenbeg.samples        golden 47                         reader 47
HIT  a1_sampling.Tirneevin Stream.below_limit golden 20                         reader 20
HIT  a1_sampling.Tirneevin Stream.samples golden 30                         reader 30
HIT  a2_nitrate.Ballynure Borehole 1.at_or_above_trigger golden 14                         reader 14
HIT  a2_nitrate.Ballynure Borehole 1.max_no3_mgl golden 50.7                       reader 50.7
HIT  a2_nitrate.Cloonfad Spring Chamber.at_or_above_trigger golden 0                          reader 0
HIT  a2_nitrate.Cloonfad Spring Chamber.max_no3_mgl golden 35.5                       reader 35.5
HIT  a2_nitrate.Gortaleen Borehole.at_or_above_trigger golden 25                         reader 25
HIT  a2_nitrate.Gortaleen Borehole.max_no3_mgl golden 65.9                       reader 65.9
HIT  a2_nitrate.Moneycashen Intake.at_or_above_trigger golden 0                          reader 0
HIT  a2_nitrate.Moneycashen Intake.max_no3_mgl golden 28.5                       reader 28.5
HIT  a2_nitrate.Rathvilly Borehole 2.at_or_above_trigger golden 3                          reader 3
HIT  a2_nitrate.Rathvilly Borehole 2.max_no3_mgl golden 41.3                       reader 41.3
HIT  a2_nitrate.Sheskin Shallow Well.at_or_above_trigger golden 19                         reader 19
HIT  a2_nitrate.Sheskin Shallow Well.max_no3_mgl golden 60.1                       reader 60.1
HIT  a3_quarter.export                  golden 242                        reader 242
HIT  a3_quarter.one_only                golden 18                         reader 18
HIT  a3_quarter.reports                 golden 250                        reader 250
HIT  compliance_samples_total           golden 427                        reader 427
HIT  nitrate_trigger_mgl_no3            golden 37.5                       reader 37.5
miss non_compliant                      golden ["Cloonfad", "Glasheen", " reader 4
HIT  programme_points                   golden 37                         reader 37
HIT  reporting_limit_legacy_ugl         golden 0.1                        reader 0.1
HIT  reporting_limit_sensitive_ugl      golden 0.005                      reader 0.005
HIT  standard_ugl                       golden 0.05                       reader 0.05
HIT  water_bodies_assessed              golden 13                         reader 13

READ AS A COUNT, so these misses are not sound: the reader answered the size of a set where
the golden holds its members, and the size is right. Read the reader's prose before scoring
the call, and rename the key or ask for the members next time.
     non_compliant                      golden ["Cloonfad", "Glasheen", "Kilc reader 4

call figures   1 of 1 hit
ask figures    48 of 49 hit (98.0 per cent)

FAIL  the reader landed the call. Gate F has failed and the architecture is spent:
      a ladder is not repaired by hardening, and an ask is not repaired by re-wording.
```
