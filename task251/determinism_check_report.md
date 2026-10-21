# determinism-check report, task251, 2026-10-21

Two isolated passes, one thread each (Sonnet, medium). Pass 1 judged target.zip 41198eaa. The pack was then re-cut (the power-failure ask's device was re-sited; the visits cells and power-failure cells changed, the main call and components did not) and pass 2 judged target.zip 20f316fe. Pass 2 is the confirming pass and governs. The final pack is target.zip 6283c112 (see Hygiene follow-up).

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (calibration transfer beyond the validated range, estimated from paired-station natural experiments), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Both threads rebuilt the sensitivity, the queue loss and the TCX-2 cold miss independently from the bundle and arrived at exactly the 7 flagged stations: R02-01, R04-03, R06-01, R08-05, R14-01, R25-01 and R29-03. The gaps around the line are wide. Pass 2: flagged stations sit at -7.03 to -9.32 per cent, the largest unflagged error is -3.51 per cent (R18-01). Pass 1 agreed (flagged -7.2 or worse, next -3.7). Every decisive fact is in a shipped file: controller model in the register and its Code history, temperature in weather_daily, sensitivity in the Northline workbook, pairing in the network file, the estimand in TDP-03 section 5. The maintenance tables reproduce cell for cell in both passes (on their respective packs).

## Recomputation ledger (pass 2, pack 20f316fe)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Stations flagged | 7 (list above) | same 7; R02-01 -7.28, R04-03 -8.06, R06-01 -7.25, R08-05 -7.03, R14-01 -8.64, R25-01 -9.32, R29-03 -7.21 | Yes |
| Listed stations beyond 6 per cent | all 7 | minimum 7.03 | Yes |
| Other 23 within 4.5 per cent | max 4.5 | max 3.51 (R18-01), then R11-01 -2.98 | Yes |
| Max occupancy, any filmed hour | 8.2 | 8.18 (R18-01 NB, 2027-08-18 17:00), hourly csv occupancy | Yes |
| Min filmed-day mean temperature | 13 | 13.3 (R22-02, 2027-08-23), weather_daily Mean Temp | Yes |
| Cold miss, TCX-2 against TCX-4, free flow | none above about 2 degrees, about 1 in 10 at -10 | ratio 0.99 (0 to 2), 0.999 (2 to 4), 0.90 (-10 to -8), 0.88 (-12 to -10), 0.86 (below -14), same on all 3 mixed bridges | Yes |
| TCX-4 miss | none | free-flow ratio 0.995 to 0.998 in all bands; occupancy per vehicle winter/summer 0.99 (TCX-4), 1.13 (TCX-2) | Yes |
| Queue loss | none in free flow, nearly 1 in 5 at 40 per cent | 0.8 per cent at or below 8, 4.4 at 28 to 30, 17.2 at 38 to 40, 19.0 at 40 to 42, 26.5 at 46 to 48 | Yes |
| Visits Ashby Q1 to Q4 | 2, 20, 7, 15 | 2, 20, 7, 15 | Yes |
| Visits Kessel | 9, 20, 6, 14 | 9, 20, 6, 14 | Yes |
| Visits Marlow | 3, 11, 9, 11 | 3, 11, 9, 11 | Yes |
| Power failures Ashby | 8, 15, 9, 8 | 8, 15, 9, 8 | Yes |
| Power failures Kessel | 20, 15, 9, 12 | 20, 15, 9, 12 | Yes |
| Power failures Marlow | 10, 7, 7, 10 | 10, 7, 7, 10 | Yes |
| Quoted alternative lists | queue alone (5), cold alone (4), summer validation (2) | queue-only R04-03 -5.76, R08-05 -5.26, R25-01 -7.04; cold-only R04-03 -5.76, R06-01 -7.25, R14-01 -5.65, R25-01 -9.32 with R08-05 -3.92, R02-01 -3.65, R29-03 -4.71 inside; validation-only R14-01 -5.65, R25-01 -7.04 | Yes |

Also confirmed in pass 2: hourly file is a full panel (60 duplicated local hours, all the 7 Nov fall-back hour, none duplicated in UTC); the 30 stations merge R08-01/05 and R19-01/03, and treating them as split does not change the list; validation loops equal the hourly file on all 1,440 filmed hours; filmed days are all weekdays in July and August. Pass 1 ledger on its own pack agreed on the list, margins, 8.18 and 13.3 limits, curves, and its own (older) visits and power cells.

## Competing answers that survived
None on the main call. Tested and rejected by shipped evidence: the summer-validation list (2 stations; the filmed conditions exclude both effects), queue-only (5), cold-only (4), raw loop counts with no sensitivity (shifts every station by about -2.4 per cent), and queue-loss shape between 8 and 25 per cent occupancy (zero or linear ramp moves no station by more than 0.01 points).

Residual forks, none touching the call (both passes concur):
1. Sensitivity carried across a controller swap (R08-05, R19-03): licensed by TDP-03 section 2, moves no flag.
2. Visits (asks 2 and 3): a literal count of booked labour days gives 24 more station-days. The 24 are all "Controller reset" orders at TCX-4 stations with no door event that local day and 0.25 to 0.75 booked hours; the 13 on-site resets, which have door events, booked 0.75 to 4.0 hours. Forced by the data but an inference no file states. Residual risk on asks only.
3. Power failures at TCX-2 stations: a break holding two LOST/OK pairs counts 2 (COMMS_OK means a poll succeeded; neighbouring TCX-4s on the same feeder log the same pairs as MAINS_FAIL). Licensed by the data, an inference.
4. Quarter by local date against UTC date: two Ashby failures fall in Q3 locally and Q4 by UTC date. The hourly record and TDP-03 are local, so local is natural.
5. Decimals for per-station errors are not pinned in the prompt. Per-station errors are not graded figures (the licensed family spreads them); the graded answers are the list, the marks and the maintenance cells.

## Spec gates
Taken from the judge's Files/Hygiene read (pass 2); I did not separately re-audit the rubric count or prompt shape here.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | Yes |
| Formats | 3 or more | 5 (csv, xlsx, pdf, md, eml) | Yes |
| Large file | 25,000 rows or more | hourly csv 525,338 rows (events csv 1,929) | Yes |
| Distractors | 2 or more, unused, relevant | collisions_regional_roads_2027.xlsx, regional_roads_pavement_condition_2026.xlsx (unused by the solution) | Yes (metadata.json naming not checked by me) |
| Deliverables | 1 to 3 | 2 (xlsx, png) | Yes |
| Asks unit and rounding | stated | per-cent errors left at "per cent" with no decimals, declined as ungraded | Noted |
| Reads as LLM generated | none | no benchmark, synthetic or tool language found; in-fiction authors; coherent dates | Yes |
| Rubric 25 or more criteria | 25 | not assessed by the thread | Open for the main thread |

## Gate G reconciliation (as pass 2 states it)
mechanism: method_or_model_selection; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. The validation figures are accurate for the conditions they cover; the difficulty is that their domain (occupancy at most 8.2 per cent, mean temperature at least 13 degrees) does not cover the year, and the two unvalidated losses must be identified from the five bridge pairs. On perfectly clean data the task would still stump. The declared distractors are not the surface read carrying the task. I did not read the design note or card for a field-by-field comparison; the main thread holds that reconciliation.

**Gate H line:** domain: pass, layers: pass, decisive_step: analytical.
Domain: detector sensitivity transfer, occupancy-dependent undercount and a temperature-dependent controller miss are what traffic data engineering estimates; the swap test fails to preserve them under another field's nouns. Layer 1: renumbered stations, UTC offsets and DST fall-back, missing weather day, year-2000 COLD_START timestamps, repeated events, remote resets booked as labour. Layer 2: pairing bridge stations with shared flow, isolating the cold miss on the 3 mixed-generation bridges, then the queue loss with the cold miss taken out, and applying both hourly. Easy route: apply the validation sensitivity as the year's error, which files 2 stations and clears 5 of the 7.

## Stump power (Gate F)
Strong (pass 2); Good (pass 1). Taking the contractor's validation as each station's accuracy flags only R14-01 and R25-01. Correcting one mechanism gives 5 or 4 stations. Only the two-mechanism model gives 7. Three failure levels are plausible for a frontier model: stop at the validation; find the queue effect but not the cold miss; apply a correction on the wrong denominator or hours. Margins are clean, so a failure is not noise. Caution for the main thread: both effects are discoverable with ordinary pairwise-ratio plots and the standard defines the estimand but not the method, so a strong solver who cleans the data may land the call; the blind readers' result should weigh this.

## Findings, ranked
1. None blocking. Visits rule (fork 2) and the power-failure double-trip reading (fork 3) are the residual inference risks, on asks only.
2. Hygiene: TDP-03 revision 4's change cell was clipped ("maintenance figures by dist"). Fixed after pass 2 in the generator by wrapping the table's cells; the text is unchanged and no figure moved. The final pack is target.zip 6283c112 (generator checks 0 failed, verify 0, two byte-identical builds, figures_check 14 of 14, precut 51 of 51). The fix is cosmetic and was not re-judged.
3. Optional prompt precision for the chart's per-cent errors (decimals) was declined, as per-station errors are not graded.

## Next action for the author
Ship target.zip 6283c112; no re-judge is needed.
