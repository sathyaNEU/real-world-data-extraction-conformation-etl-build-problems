# determinism-check report, task181, 2026-10-11 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules:** domain: pass, layers: pass, decisive_step: analytical

## Why
PR-07 4.2 sends the team to the area with the largest excess of cases with specimens collected 21 September to 4 October 2026 over the complete 2021 to 2025 mean for those dates (4.3). The extract's own `received_utc` shows Inland Pathology, which carried 6 of Griffith's 7 cases, notifying pertussis in weekly Wednesday batches (median 12 days, 76.0% within 14) while the hospital laboratory takes about 2 days (100%). So at 07:00 Griffith's fortnight is far from complete while Wagga Wagga's and Snowy Valleys' are nearly complete. Every nowcast built from the extract's own laboratory delays puts Griffith first (excess 27 to 131, against at most 9.2 for Wagga Wagga). The slide clusters and all ten rows of `pertussis_cases_by_lga.csv` reproduce exactly. The one live fork, counting only the cases notified so far (Wagga Wagga, 7.6 against 5.6), is the task's easy route, not an equally licensed reading: it measures notified cases, not the specimen-dated cases that 4.2 compares with a complete baseline.

## How this pass ran
Pass 1 did not run: its orchestrator was a subagent without the Agent tool, so it could not spawn the thread (`determinism_check_report.md` records it). Pass 1 prepared a clean brief and a bundle copy without opening any intent file. For pass 2 the main thread:
- re-made the bundle copy fresh (`cp -a`, sha256-identical to `task181/target/` on all 11 files);
- checked the brief's system prompt and `prompt.md` sections verbatim against their sources;
- added the other checkouts and the notes folder to the brief's forbidden list by name;
- spawned exactly one judge thread (general-purpose, opus).

The thread read the brief from inside its one allowed directory, used local tools only, and wrote `verdict.md` there (its scripts are in `work/`). The design note, card and `metadata.json` were read only after the thread returned, for the spec gates and the reconciliation below.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CC1: Wagga Wagga cases, specimens 21 Sep to 4 Oct | 9 | 9 | yes |
| CC1: Griffith cases, same window | 7 | 7 | yes |
| CC1: Snowy Valleys cases, same window | 7 | 7 | yes |
| Step 2: other areas in the window | C-G 2; Edward River, Leeton, Narrandera 1 each | the same; Hay, Junee, Murrumbidgee 0 | yes |
| CC2: expected count, Wagga Wagga | 1.4 | 1.4 (2021 to 2025: 0, 0, 1, 3, 3) | yes |
| CC2: expected count, Griffith | 1.4 | 1.4 (0, 0, 0, 5, 2) | yes |
| CC2: expected count, Snowy Valleys | 1.4 | 1.4 (0, 0, 0, 4, 3) | yes |
| CC3: Griffith cases through Inland Pathology | 6 of 7 | 6 of 7 (the 30 Sep case came through the hospital laboratory) | yes |
| CC3: Wagga Wagga and Snowy Valleys through the hospital laboratory | all | 9 of 9, 7 of 7 | yes |
| CC4: Inland Pathology notified within 14 days, specimens Aug 2025 to Jul 2026 | 76% | 76.0% (73/96) on Sydney dates; 77.1% on UTC dates; 60.4% if read as strictly under 14 | yes |
| CC4: hospital laboratory, same measure | 100% | 100% (196/196); longest delay 9 days | yes |
| Step 3: Wagga Wagga leads on the cases notified so far | leads | excess 7.6 against Griffith 5.6 and Snowy Valleys 5.6 | yes |
| Step 5: Griffith's fortnight several times its 7 notified | several times | 29.6 to 132.7 (4.2 to 19 times); base case 44.3 | yes |
| Step 5: Wagga Wagga and Snowy Valleys a little above what is on file | a little above | Wagga Wagga 9.1 to 10.6; Snowy Valleys 7.0 to 8.1 | yes |
| Step 5: Griffith first under per-day and weekly triangles and 6, 12 or 24 months of history | robust | Griffith first in all 33 variants | yes |
| Main recommendation | Griffith | Griffith | yes |
| Slide ask 1: area | Griffith | Griffith | yes |
| Slide ask 2: Banna Avenue Public School | 5 | 5 (the parent notification excluded under 5.1) | yes |
| Slide ask 2: Kooyoo Street Public School | 2 | 2 | yes |
| CSV: Wagga Wagga | 63, 2, 3, 2, 1 | 63, 2, 3, 2, 1 | yes |
| CSV: Griffith | 25, 3, 2, 1, 1 | 25, 3, 2, 1, 1 | yes |
| CSV: Leeton | 11, 0, 1, 0, 1 | 11, 0, 1, 0, 1 | yes |
| CSV: Narrandera | 5, 0, 1, 0, 0 | 5, 0, 1, 0, 0 | yes |
| CSV: Murrumbidgee | 0, 0, 0, 0, 0 | 0, 0, 0, 0, 0 | yes |
| CSV: Hay | 2, 0, 0, 0, 0 | 2, 0, 0, 0, 0 | yes |
| CSV: Edward River | 7, 1, 1, 1, 0 | 7, 1, 1, 1, 0 | yes |
| CSV: Junee | 3, 1, 1, 0, 1 | 3, 1, 1, 0, 1 | yes |
| CSV: Cootamundra-Gundagai | 15, 2, 1, 1, 1 | 15, 2, 1, 1, 1 | yes |
| CSV: Snowy Valleys | 9, 1, 1, 1, 0 | 9, 1, 1, 1, 0 | yes |

The thread also checked:
- Every infant is at least 17 days from the six-month boundary; the closest is 163 days.
- Four maternal doses fail 6.3 cleanly: two came 10 and 11 days before the birth, and two belong to 2024 pregnancies.
- The week-35 report reconciles exactly to the line list and the influenza file.

## Competing answers that survived
None. The thread tested seven forks; each closes on a shipped fact:
1. **Cases notified so far against all specimen-dated cases** (Wagga Wagga against Griffith). This is the trap, not a licensed reading:
   - 4.2 and 4.3 count the same specimen-dated quantity, and 4.3's baseline is complete;
   - the 07:00 extract is a point-in-time cut, with no Inland Pathology Griffith specimens from 23 to 28 September yet on file;
   - 4.1 asks only that the call come from the extract, which the nowcast does.
2. **Lag-matched baseline** (Wagga Wagga 7.8 against 6.4). It rewrites 4.3.
3. **Delays borrowed from the influenza file** (Wagga Wagga). Rejected: influenza is a different condition and a different pipeline (six receipt days a week, mean 1.9 days), while the line list carries pertussis's own route delays (336 of 356 Inland Pathology receipts on a Wednesday).
4. **Nowcast design choices.** All 33 variants give Griffith, and so does an artificially conservative one (8.93 against 7.91).
5. **Window boundary** (UTC day or including the extract day). Nothing changes.
6. **Clusters.** Counting the parent, the Canal Road single episode and the roster matches each change nothing. The slide inherits fork 1 only through the area.
7. **Quarterly table.** Every alternative (notifications, not cases; the wrong episode date; 2727 to Snowy Valleys; string MRNs; dropping "that pregnancy" or the 14 days) misreads an explicit clause.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in the pack | 10 or more | 11 | yes |
| Distinct formats | 3 or more | 6 (pdf, txt, parquet, csv, md, xlsx) | yes |
| Large file | 25,000 rows or more | `respiratory_admissions_2019-2026.csv` 29,036 rows; `antenatal_vaccinations_2019-2026.parquet` 35,724 rows | yes |
| Declared distractors | 2 or more, none labelled as such | `influenza_notifications_2026.csv`, `cd_weekly_report_2026_wk35.pdf`; neither name nor content labels them | yes |
| Distractors unused yet relevant | each | Influenza: the same laboratories and the same receipt clock, tempting as a delay source. Week-35 report: the same unit, the same areas, pertussis counts by area | yes |
| A distractor that answers a graded quantity is ruled out by a shipped fact | each | Week-35 report: counts notifications by week received ("notifications counted in the week the unit received them"), while 3.3 and 3.5 define cases by episode and first specimen. Influenza: answers nothing graded by itself; borrowing its delays is fork 3, closed by the line list's own pertussis receipt times | yes |
| Deliverables | 1 to 3 | 2 (`response_team_brief.pptx`, `pertussis_cases_by_lga.csv`) | yes |
| Golden deliverables present | all named | both in `golden/` | yes |
| Asks multi-dimensional | yes | area plus clusters dependent on the call; ten areas by five linked measures (episodes, infants, admissions linkage, maternal vaccination linkage) | yes |
| Units and rounding stated | every ask | all asks are counts of cases | yes |
| Prompt shape and the 25-criteria floor | identifiable, 25 or more | shape 17; 1 area, 2 schools with counts, 50 table values | yes |
| Realism | no LLM tells, goldens read as work products | minor tells only (finding 1) | yes, with a note |

## Gate G reconciliation
| Field | Judge (from outside) | Card and design note (from inside) | Match |
|---|---|---|---|
| Gate G mechanism | forecasting | `gate_g: forecasting` | yes |
| Stumping family | analytical_non_defect; no surface read, no sole data defect | `stump_class: analytical` | yes |
| Domain | pass: delay-adjusted excess over a five-year seasonal baseline is surveillance epidemiology's own nowcasting and aberration detection | `domain_test`: an epidemiological nowcast from each reporting route's own delay distribution; the noun swap breaks it | yes |
| Layers | Layer 1 messy data (episodes, UTC across daylight saving, split postcodes, MRN and Medicare formats, free-text schools); Layer 2 the laboratory-specific right-truncation nowcast | `layer2_family: field_method`, pattern `epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/2`; `layer1` names the episode rule, split postcodes, UTC times, the register linkage | yes |
| The easy route | count the cases on the extract, giving Wagga Wagga (or pool delays across conditions) | `analyst_test`: the cases notified so far, or a nowcast on one pooled delay, give Wagga Wagga | yes |

The build reads the same from outside as from inside. The thread did not name a declared distractor as the surface read carrying the task.

## Stump power (Gate F)
Likely adequate. The 07:00 count is the natural move given 4.1 and the prompt's "settles it off this morning's line-list extract". Only a solver who measures each laboratory's lag sees that most of Griffith's Inland Pathology fortnight is not yet notified, and the influenza file catches solvers who pool delays across conditions. No file documents the lag, so nothing disarms the trap in advance. Both in-house solver rounds on this architecture (rounds 2 and 3) missed in exactly this way, with no word on reporting delay. The residual risk is a wrong-reason split: a run that measures the lag and still cites 4.1 for Wagga Wagga would be interpretive rather than analytical.

## Findings, ranked
1. **Minor hygiene.** Two small tells in the workbooks: `postcode_lga_concordance.xlsx` and `school_rosters_term3_2026.xlsx` store inline strings although their docProps name Microsoft Excel, and the nine roster sheets share an identical header block. Optional fix in the generator's workbook writer (shared strings; per-school header variation); no graded figure moves.
2. **Residual Gate C and F risk, no action now.** A reading of 4.1 ("from the line-list extract run at 07:00") as fixing the count to the cases on file. The judge ruled it the trap, not a licensed reading. Its optional pin ("PR-07 counts a case on its specimen date, however late the laboratory notifies it") would cost stump power and need a rerun, so it is held unless live runs split for that reason.
3. **Process, not a task181 finding.** A subagent cannot spawn the judge thread in this setup. The main thread spawns it from a brief the orchestration prepares (pass 1's no-run record).

## Next action for the author
Ship task181 at stage 8 once the stage-5 guard BLOCK (`ban.strategy` maturity_censoring against task134) is settled by the author's decision.
