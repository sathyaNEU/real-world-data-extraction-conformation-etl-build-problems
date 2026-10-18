# task190 - determinism judge report

**Order kept: yes.** The pack was worked from scratch and the full derivation was written to
`/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task190_derivation.md`
before `task190_graded_blocks.md` was opened. I reached the committed main call independently
(Metal and metal-bearing wastes, 56.6 per cent against 59.5, 2.9 points, interval 55.4 to 57.8).

**Verdict: NOT_DETERMINISTIC (main recommendation forced; one supplementary figure pair rests on a
convention no shipped file states) + SOLUTION_WRONG (one supplementary figure does not reproduce).**

**Disposition: FIX_NOW.** Two bounded repairs, neither touching the main call, the ladder or any
decision-relevant artifact: (1) pin hours per field day in `bws_2026_design_and_weighting.pdf` s5 (or
restate the 71 hour-recorded visit rows in days), and (2) regenerate the Norte figure in deliverable 3.
If the author counts an edit to a shipped PDF as solver-visible hardening, this becomes SEND_BACK with a
rerun; the analytic surface and every main-call figure stay byte-equivalent either way.

**Gate G classification:** `mechanism: statistical_rigor`, `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`. Every reported number in the pack is FINE: the
register tonnages are correct, the survey arisings are correct, no stakeholder conclusion is overturned.
The difficulty is design-based precision, so no banned-type finding.

**Gate H line:** `domain: pass`, `layers: pass`, `decisive_step: analytical`. The deciding quantity is the
sampling error of a ratio whose denominator is a stratified survey estimate, with the 250-or-more stratum a
complete enumeration that carries 95.8 per cent of metal arisings and contributes zero variance, which is
the core work of an official statistics division; the easy route is to rank the eight streams by point
shortfall, which names Mixed commercial and industrial wastes at 4.9 points (1.45 standard errors, interval
53.0 to 66.2 straddling its 64.5 target) and is wrong.

## Gate table

| gate | call | the number or quotation that decides it |
|---|---|---|
| A | FAIL (SOLUTION_WRONG, one figure) | Deliverable 3, Norte: committed **16.66** usable returns per field day; reproduces only as **538 / 32.54 = 16.53**. 16.66 = 542/32.54, and 542 is the raw row count of outcome "usable return" for EQ-NOR including 4 of the log's 15 byte-identical duplicate rows (same case_ref, same contact_seq, same date). Unique cases are 538, and 542 would put total usable returns at 1,634 against the 1,630 records in `bws_2026_microdata.csv` and the 155+195+520+760 of the design PDF's stratum table. Everything else reproduced exactly: 70,384 t / 124,354 t / 56.6 / 55.4-57.8 / 0.635 SE / 4.57 SE / 1.45 SE / "95.8 per cent" (95.77) / "82,835 legs" / all 32 attainment cells / all 24 pass-through cells / all eight 2025 tonnages / all five municipal rows. |
| B | FAIL (supplementary only) | "field days consumed" by region: 71 rows of `bws_2026_response_log.csv` carry `time_unit = h` (all Alentejo) and **no file in the pack states hours per field day** (grepped all 17 members, every PDF, both xlsx sheets). The committed 10.11 field days and 16.42 returns per day require 8 h; 7.5 h gives 10.78 and 15.40, 7 h gives 11.55 and 14.37, dropping the rows gives no Alentejo visit days. 8 h is the only factor keeping the converted values (0.61 to 0.97 of a day) inside the range the `d` rows occupy (0.60 to 1.00), but that is an inference from the data, not a filed convention. Taxonomy: **external_dependency**; fix location **input_files**. |
| C | PASS on the main call | Metal's upper bound clears its target by 1.66 points under every licensed route: stratified SRSWOR with the finite-population correction **57.84**, the same without the FPC inside the sampled strata **58.03**, stratified delete-one jackknife **57.84** (identical to the FPC estimator to 2 dp), one-sided at 1.645 **57.64**; target 59.5. No other stream reaches 1.45 standard errors from its target. Two routes that do move the answer are both unlicensed and both are named in the derivation: substituting the 2025 release's national-total CV of 3.9 per cent for each stream's own variance hands back Mixed C&I (metal hi95 60.9, mixed hi95 64.16 against 64.5), which the same release forbids ("the statistical stream breakdown is published without them" and the CV is of "the estimated national total"), and the pack's own micro-data shows per-stream CVs of 1.1 to 13.0 per cent; omitting the FPC on the completely enumerated stratum too gives metal hi95 62.57 and **no** established stream, which contradicts `bws_2026_design_and_weighting.pdf` s2 ("every enterprise in it receives a questionnaire... the 2026 round closed with a return from each of them") and answers the prompt with nothing. The variance estimator is further pinned by a shipped figure: the FPC estimator reproduces the release's "coefficient of variation... 3.9 per cent for the 2026 round" exactly (3.915), while dropping the FPC gives 4.091, the release's 2025 number. |
| D | PASS | The split among good answers traces to the analysis, not to a word: "established below its plan target at the 95 per cent level" is defined in `collection_capacity_note_2027.pdf` s3 and no shipped sentence ranks streams by shortfall size (grepped the PDFs for largest/greatest/biggest/rank/most: zero hits). Nothing, read literally, makes the easy answer correct. |
| E | FAIL (supplementary 3 only) | Main ask demands one stream, the points and the module, all pinned. The ask "by region the field days consumed" is missing a needed precision (the hours convention, Gate B above). Two further forks are closed, thinly but closed: "municipalities' reported collections" excludes the five `Associacao de Municipios` rows, and the 27 remaining reporting entities are exactly the 27 `origin_entity` values of the receipts file, which is what makes the committed 118,494 / 115,419 / 3,075 / 2.6 per cent reproduce (taking all 32 entities gives 169,381 / 53,962 / 31.9 per cent); "by region" on the receipts means the waste's origin region, the file's own column, not the facility's (facility-region basis gives Algarve 78.4 and Norte 3.9 per cent). Both would be worth one explicit word in the prompt. |
| F | PASS, strong | Two independent wrong attractors and both are reachable by a careful solver: rank by point shortfall (Mixed C&I, 4.9 points) and borrow the published 3.9 per cent national CV (also Mixed C&I). A third, omitting the census stratum's zero variance, leaves no stream established. Every reported input is correct, so there is nothing to "catch"; the work is the stratified variance of a ratio with an estimated denominator. |
| G | PASS | See the Gate G line above. The register and survey figures are all fine; no misleading surface read carries the task. |
| H | PASS | See the Gate H line above. Layer 1 is genuine, unplanted mess: `waste_movement_legs_2026_h2.csv` renames all eleven columns, the 2026-07-01 waste-code and operation-code reissue runs mid-year, interim R13 storage splits a movement across a parent and a forwarded consignment, 24 municipal return rows are in 100kg, 71 field-log rows are in hours, 15 log rows are exact duplicates, and the 2025 release's published recovered column sits 0.3 to 2.8 per cent below the register recompute. Layer 2 is the design-based interval and the 95 per cent test. |

## Figures I could not reproduce

| committed figure | what I got | cause |
|---|---|---|
| Deliverable 3, Norte: 16.66 usable returns per field day | **16.53** (538 / 32.54) | 542 counts 4 byte-identical duplicate log rows; unique cases are 538 and the micro-data holds 1,630 returns, not 1,634. Norte field days (32.54) are unaffected because the committed method already counts a visit once per `visit_ref`, which is duplicate-immune. |
| Deliverable 3, Alentejo: 10.11 field days and 16.42 returns per field day | 10.11 / 16.42 at 8 h to the day, **10.78 / 15.40** at 7.5 h, **11.55 / 14.37** at 7 h | No shipped file states hours per field day (Gate B). |

Everything else reproduced to the stated rounding, including every main-call figure.

## Also worth the author's attention (not gate failures)

- **The 2025 calibration does not tie exactly.** Deliverable 4 reproduces from the register (metal 67,709 t), but `waste_statistics_2025_release.pdf` Table 1 publishes 67,376 t for the same stream and says recovered tonnage "is taken from the National Waste Movement Register". The gaps are +333 / +345 / +333 / +239 / +217 / +143 / +79 / +47 t and I could not reconcile them under any basis I tried (confirmation-date cutoffs, receipt-date basis, dropping superseded producer permits, facility-licence filters). A solver who answers deliverable 4 from the published column is 0.5 per cent off on every stream, and one who treats the table as a calibration target will hunt for an adjustment that does not exist. The table is still load-bearing in a good way: it is what pins R1 as a recovery operation (mixed C&I and wood recover only through R1, so excluding it would publish zero against 89,404 and 19,026) and what rules out a first-op-only read (metal 47,768 against 67,376).
- Hygiene: **PASS**. 17 files, three formats (12 csv, 4 pdf, 1 xlsx), largest file 80,104 rows, no README or how-generated artifact, no synthetic or benchmark disclosure, no authoring language, no tool banner, dates coherent (register extract 2027-01-31, survey 2027-01-16, council letter 2027-01-14, answer due 28 February), distractors (`hazardous_export_notifications_2026.csv`, `carrier_permit_vehicle_log_2026.csv`) relevant but unused. Nothing exclusion-level.

## Fix

**input_files** for the determinism failure and **solution** for the reproduction failure:
1. Add one sentence to `bws_2026_design_and_weighting.pdf` s5 stating the hours-to-field-day convention the
   division books visits at (eight hours to the field day, which is the only factor consistent with the
   `d` rows' own range), or convert the 71 `h` rows to days in `bws_2026_response_log.csv` and drop the
   `time_unit` column's second value.
2. Restate Norte's usable returns per field day as **16.53** in the golden and in `figures.json`, computed
   on distinct cases after the log's exact-duplicate rows are dropped, so the five regions sum to the 1,630
   records of the micro-data.
3. Optional, cheap, and it removes the last two thin spots: one word in the prompt for the municipal
   reconciliation ("the municipalities' own returns" and "by the region the waste arose in"), and either
   reconcile the 2025 release's recovered column to the register or widen the gap so it cannot be mistaken
   for the answer to deliverable 4.
