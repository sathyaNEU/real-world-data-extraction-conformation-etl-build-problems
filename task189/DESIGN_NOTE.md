# task189 design note

Araglen Regional Water Authority, MCPA compliance in the 2025/26 reporting year: how many of the
district's water bodies the annual return states as non-compliant.

## Draw

| Axis | Value |
|---|---|
| Card | `.claude/skills/fingerprint/cards/task189.json`, filed and committed with this note |
| Domain, task type | Physical & Environmental Sciences, `environmental-monitoring-exceedance` |
| Objective | Anomaly Detection & Diagnostics (an apparent exceedance separated from a measurement artifact) |
| Shape | 10, scorecard: each water body's check against the standard |
| Decision | a count committed to the National Water Quality Office in the return due 30 November 2026 |
| Gate G | `signal_vs_noise_or_hold`; decisive generator G16 method selection, then G17, G2 |
| Strategy | `other`: the mean of a left-censored sample whose reporting limits differ by laboratory |
| Layer 2 | `estimation_fit`, own pattern `left-censored-results-with-several-reporting-limits` |
| As-of date | 16 November 2026 (the authority's extract date; the return is due 30 November 2026) |
| Guard | WARN only. `overuse.org_family` government_agency in 28 builds: the unit that files a river basin district's statutory return is a public authority and no other org family is honest here. `test.same_puzzle_older` and `test.same_driver_older` differentiated against task70 and task260 in the card. |

**Data-native sentence.** MCPA is sprayed on rush-infested pasture in a six-week window, so in this
district's record the herbicide is quantified in a handful of spring and summer samples and is below
the laboratory's reporting limit in most of the rest, and because the authority's own framework
laboratory reports to 0.01 ug/L while the catchment partnership's laboratory reports to 0.05 ug/L,
over half the standard, the share of a water body's year that is known only as a bound depends on
which laboratory holds its sample points.

**Sources read.** `analytical_tasks/02_anomaly_detection/AD12_regulator-return-attack-campaign-unit.md`
(seed): the decision shape only, one count committed to a regulator at a date where monitoring fires
at a finer unit than the return counts; its own architecture, a method pinned by reproducing two
published returns, is a certified replay and is not used. `guard.py mechanisms --objective
anomaly-detection`: 21 spent drivers, none on censored measurement; the nearest, task180, turns on
events never recorded at all because the detection threshold moves with a daily noise cycle, where
here every result is present and carries its own upper bound. `references/client/two-layer-task-design.md`:
Layer 2 family `estimation_fit`, censoring and truncation.

## Default path

1. Read `lims_results_export_2025_2026.csv`, keep `determinand_code = MCPA`.
2. Keep `sample_type = FIELD` (drop the blanks, field duplicates, laboratory duplicates and spikes,
   all named in the data dictionary) and keep the approved version of every result, dropping the
   provisional rows the approved ones supersede.
3. Convert the results reported in ng/L to ug/L using the `units` column.
4. Join each `lab_client_point_code` to the authority's `sample_point_code` through
   `sample_point_crosswalk.csv`, then to its water body through `monitoring_programme_2025_26.xlsx`,
   taking the water body code in force in the reporting year from `water_body_register.csv`.
5. Keep the samples whose sample date falls in the reporting year, 1 April 2025 to 31 March 2026.
6. For each result carrying the `<` qualifier, substitute half the value in `reporting_limit_ug_l`.
7. Average the results per water body and compare each average with the 0.08 ug/L annual average
   standard in `surface_water_quality_regulations_2019.pdf`, clause 7.2.
8. Count the water bodies whose average exceeds the standard and write that count into the return.

**Ends on:** 7 non-compliant water bodies (Ballynure, Cloonfad, Derryvore, Glasheen, Kilcrohane,
Owenbeg and Tirneevin Stream).
**Golden:** 4 non-compliant water bodies (Cloonfad, Glasheen, Kilcrohane and Owenbeg).

## Stump sentence

The default path substitutes half the reporting limit for every result reported below it, the
default in practice, and files **7 non-compliant water bodies**; three of those seven
(Ballynure, Derryvore and Tirneevin Stream) are over the standard only because most of their
samples went to the laboratory whose reporting limit is 0.05 ug/L, so half of it, 0.025 ug/L, is
written into their year where the authority's own laboratory shows the concentration at those
points to be nearer 0.004 ug/L.

## Tried and rejected

- Shrinkage of each water body's mean before the threshold comparison (the small-sample selection
  reading): `guard.py nearest` measured the driver at 0.12 against task253 v3, which already builds
  "how many units have a latent level below a fixed line, seen only through averages of small and
  unequal samples". Dropped at the draw.
- A flow-weighted against time-weighted annual mean as the decisive step: the weighting is a reading
  of "annual average" and would be a semantic fork on the main call, so clause 7.2 files the
  arithmetic mean of the compliance results and the uneven sampling interval becomes ask-layer mess.
- The seed's own architecture (the return's method must reproduce the two previously published
  returns): a certified replay, banned by the 10/10 rules and by `guard.py` as a validated decoy; no
  previous return ships in the pack at all.
