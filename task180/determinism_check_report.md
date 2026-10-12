# determinism-check report, task180, 2026-10-12 (pass 1)

## Verdict
DETERMINISTIC, with SOLUTION_WRONG (minor, repairable in the blocks and the golden docx).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Note: one thread (sonnet, medium) judged from judge_brief.md. After it unzipped, `target/well_register.csv` changed (a `former_designation` column replaces the `remarks` column, from the leak reader's realism note). `target.zip` now carries the new column (checked). The MST-Th4a to MST-GT4 mapping survives in that column (MST-GT4 / MST-Th4a, and MST-GT3 / MST-B3). The judge cited a "register remark", so its Ask 1 check ran on the old wording. No graded figure depends on the change. The judge's verdict file is /tmp/determinism-check-task180-20261012073937/verdict.md.

## Why
Pfeilbrunn's catalogue holds its small earthquakes mostly from 23:30 to 05:00 local (442 of 658). Scaled to 24 hours that gives 28.0 per 100,000 m3 against 9.6 on the whole-day record, so Pfeilbrunn is at 223 and 206 in Q1 and Q4 2027 against 120. No other plant exceeds 85 under any reasonable estimator. Both competing answers fail on the files. Carrying located counts forward gives no plant over, and the files refute it through the time-of-day structure. Year-on-year growth gives Lanzenried over, and the files refute it through the LZR4 to LZR5 epoch of 15 July 2025. The call is forced. What does not reproduce is some graded cells: Wendelsried Q4 2027 (46) and critical component 4 in submission.md, and the Pfeilbrunn expected-count cells, which carry a roughly 7 per cent estimator spread. I found a third problem after the thread returned: the golden docx table disagrees with submission.md on Lanzenried (see finding 1).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pfeilbrunn ML>=1.0 within 5 km, night / all | 442 / 658 | 442 / 658 (edge sharp at 23:30 winter, 23:34 summer local) | yes |
| Pfeilbrunn night rate vs whole-day | 28.0 vs 9.6 | 28.04 vs 9.56 | yes |
| Pfeilbrunn 2027 Q1/Q2/Q3/Q4 | 223/70/44/206 | 222.8/70.0/43.6/206.1 | yes |
| Located counts Q4 2025 to Q3 2026 (default path) | PFB 77/62, MOS 92 | matches tls_bulletin_2026Q3 for all five plants | yes |
| Moorstetten 2027 | 85/37/26/81 | same | yes |
| Lanzenried 2027 | 75/32/24/72 (submission.md); 76/33/24/73 (golden docx) | 75/32/24/72 (post-swap rate 10.30 per 100,000 m3) | submission.md yes, golden docx NO |
| Ottenmoos 2027 | 47/22/14/46 | same | yes |
| Wendelsried 2027 | 45/21/15/46 (submission.md); 45/21/15/45 (golden docx) | 45/21/15/45 (45.39 on metered volumes, 45.52 on telemetry) | Q4 in submission.md NO; golden docx yes |
| Critical component 4 | "Wendelsried 46" | 45 | no |
| Annex volumes, 15 cells | as filed in submission.md | all 15 reproduce after shifting the 2026 sheet one month back | yes |
| Annex automatic counts, 15 cells | as filed | all 15 | yes |
| Annex hours under four stations, 15 cells | as filed | all 15 exact | yes |
| Lanzenried LZR5 epoch | 15 July 2025 | inventory epoch; 4 events in the ML 1.0 to 1.2 bin before, 91 after | yes |

The golden annex xlsx matches the submission.md annex cells I read (the first 8 rows).

## Competing answers that survived
1. Pfeilbrunn expected-count cells (supplementary ask 3 of the outlook doc only). The same literal text gives different whole numbers under different rate conventions. The amber call and quarters do not change.

   | Convention | Q1 | Q4 |
   |---|---|---|
   | Night count scaled by time share 24/5.5 (golden) | 223 | 206 |
   | Night count divided by volume injected in the same hours | 238 | 220 |
   | Window 00:00 to 05:00 | 217 | 200 |

   No shipped sentence pins the convention. The golden docx already states that another convention "moves a cell by up to 8 per cent and none across the line". Nothing closes the fork inside the pack, so the cells are only gradable with a tolerance (Gate C, difficulty bar for supplementary answers).
2. Nothing survives on the main call. Every other plant stays under 120 even at its highest 2026 rate (Moorstetten Q1 at 14.3 per 100,000 m3 gives 108). Pfeilbrunn is over under every estimator tried (182 to 238 in Q1 and 206 to 226 in Q4). The margin is thin-but-clean, not fragile.
3. The Q4 2025 volume is inflated by about 40 per cent on the xlsx December 2025 sheet total, because December is filed twice. Telemetry resolves it. It is derivable and unambiguous, so it does not count as a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 7 (csv, pdf, xlsx, parquet, xml, json, md) | yes |
| Large file | 25,000 rows or more | origins 31,267; hourly parquet 197,130 | yes |
| Distractors declared | 2 or more, in metadata.json, none labelled in a name or file | federal_catalogue_2023-2026.csv, groundwater_levels_2025-01_2026-09.csv; no file says it is a distractor | yes |
| Distractors relevant and unused | same world, unused by the solution | the federal catalogue is the same events at ML 2.0 and over; groundwater_levels is the weaker one (same plants, shallow monitoring) | yes, groundwater_levels is weak |
| Distractors ruled out by a shipped fact | any that reproduces a graded quantity is ruled out | the federal catalogue starts at 2.0, which rules it out as a count of ML 1.0 and over; groundwater_levels answers nothing graded | yes |
| Deliverables | 1 to 3 | 2 (amber_outlook_2027.docx, tls_annex_2026.xlsx), both present in golden/ | yes |
| Asks multi-dimensional | not stacked lookups | a 5 x 4 grid of cells plus 45 annex figures (15 each for volume, count, hours) | yes |
| Units and rounding in the asking sentence | stated | cubic metres to the nearest hundred, counts as whole numbers, hours to one decimal | yes |
| Prompt | plain paragraph, under 1,000 characters | 618 characters, question first | yes |
| Prompt shape and criteria floor | shape identifiable, 25 or more criteria | shape 07 (grid of cells); roughly 65 gradable figures plus recommendation blocks | yes, rubric generated downstream, not counted here |
| Realism | not LLM-looking | the thread found no authoring disclosure; the sheet-label shift, refiled December and renamed well read as system mess. The golden memo is dated 14 October 2026 against an as-of date of 12 October 2026 | yes, with the dating nit in finding 4 |

## Gate G reconciliation
The judge classified the task as mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note and the card agree: gate_g `forecasting`, stump_class `analytical`, strategy `other` (detection completeness on a daily noise cycle). No mismatch, so the build reads as one shape from inside and outside.

Two watch items. (a) The judge flagged the Lanzenried year-on-year trap as a borderline sub-trap that leans on rejecting a misleading trend. The design note makes this rung 1, secondary to the decisive rung 3. (b) The bulletin's located counts are the default path's input. They are correct and labelled for the surface network. The judge did not name the bulletin or either declared distractor as the surface read carrying the task. The "forecasting" label rests on the 2027 network change, not on a wrong reported number. A strict reader could still call "the catalogue is incomplete by hour" a flip away from a reported read. The design note's answer is the history-pinned censoring correction, which Gate F endorses as a FINE-numbers shape.

Card inconsistency to fix: the card's `analyst_test` says maximum-curvature completeness is "about ML 0.6 at every plant". The design note and golden say 0.4. The card's `driver_concrete` says the catalogue "still looks complete near ML 0.4". Align the card to 0.4.

## Gate H
The judge's line is `domain: pass, layers: pass, decisive_step: analytical`. The card's `domain_test` and the design note's three rules say the same: the seismologist's completeness-by-hour assessment and the Gutenberg-Richter rate it supports. Swap test: other fields' nouns lose the magnitude-frequency law and the noise-set detection threshold. Layer 1 (UTC against local quarters, the portal's one-month label shift, the renamed well, location-code epochs, multi-origin events) is what the generator's own list also names. The easy route (located counts carried forward) gives no plant over amber; year-on-year growth gives Lanzenried. Consistent with the card's `analyst_test`.

## Stump power (Gate F)
Judged good. The easy routes land on "no plant" or on Lanzenried. A strong solver must bin event times by local hour to find the sharp 23:30 to 05:00 window, then reject the Lanzenried trend through the LZR5 epoch. The judge's caution: a whole-day Gutenberg-Richter extrapolation could reach the right plant and quarters by another method, so the main call is reachable by more than one route. The difficulty rests mostly on the estimator choice plus the volume and epoch hygiene in the three annex asks. No too-easy signal was named; the pack documents no completeness-by-hour defect.

## Findings, ranked
1. The golden docx and submission.md disagree on graded cells. `golden/amber_outlook_2027.docx` Figure 1 table reads Lanzenried 76/33/24/73 and Wendelsried Q4 45. `submission.md` section 4 reads Lanzenried 75/32/24/72 and Wendelsried Q4 46 (and critical component 4 says 46). The docx note says Lanzenried's rate is taken "from August 2025". Submission step 3 says 15 July 2025, and the judge's 75/32/24/72 reproduces from 15 July. Make the docx, the submission and `generator/figures.json` agree, then rebuild. By the judge's recomputation the submission figures for Lanzenried are right and the docx's are one off. For Wendelsried Q4, 45 is right on metered volumes. This breaks the standing rule that a figure shared by two deliverables agrees. The Lanzenried Q1 cell moving to 76 changes nothing about the call.
2. Wendelsried Q4 2027: set to 45 in `submission.md` (Deliverable Answers, outlook ask 3) and set critical component 4 to "Wendelsried 45". Both use the metered volumes the solution step 7 declares.
3. The Pfeilbrunn expected-count cells (and all 2027 cells) are not pinned to a rate convention. Keep the golden docx's sentence on the 8 per cent spread, add the same sentence or a stated convention to `submission.md` step 4, and grade the 2027 cells with a tolerance of about 8 per cent or the nearest 5. Do not file the estimator in the pack. That would make the decisive step rule application.
4. Cosmetic: the golden memo is dated 14 October 2026 against a pack as-of date of 12 October 2026 and a build date of 12 October. Move the memo date to 12 October or later only if the survey would date a memo after its extract date, which it would. Low priority.
5. Card: align `analyst_test` to maximum-curvature ML 0.4 (see Gate G reconciliation).
6. `well_register.csv` changed after the judge unzipped. The graded figures do not depend on the changed column. If the card or design note's Ask 1 text still refers to a "remarks" mapping, update it to the `former_designation` column. The generator's README of the register, if any, should also say so. Re-running the judge is not needed.

## Next action for the author
Reconcile Lanzenried (75/32/24/72 or 76/33/24/73) and Wendelsried Q4 (45) across `generator/figures.json`, `golden/amber_outlook_2027.docx`, `golden/tls_annex_2026.xlsx` and `submission.md` in one generator pass. Set critical component 4 to Wendelsried 45, state the Pfeilbrunn rate convention and its tolerance in `submission.md` step 4, align the card's completeness line to ML 0.4, rebuild twice byte-identically, and re-run `figures_check.py`. No prompt or input-file change is needed, so no model rerun and no re-judge beyond the one the pipeline allows after a FIX_NOW.
