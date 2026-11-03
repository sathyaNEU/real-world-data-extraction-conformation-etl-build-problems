# determinism-check report (pass 2), task307, 2026-11-03

Reworked bundle: 15 files (adds protection_log_2016_2026.csv, 1,058 rows; planning note and unit_register reissued); prompt now also asks for trips. Judge thread r2, one pass, scratch /tmp/determinism-check-task307-r2/.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (with forecasting on a regime change), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the shipped files. The call is forced by one pitting rate of 0.24 cm2 per restricted-band hour (30 to under 58 per cent of rating, unit_register.xlsx Driftsområder), holding in all seven inspection pairs that start on or after 2016 while pitting per running hour spans 0.012 to 0.143. Carried at each unit's 2026 band hours (planning note 2.4), Nesvik G1 passes 2,400 cm2 in 2027 and spares 4,650 MWh per NOK million against Sørdal G1 at 3,820, gap 830. No Gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Band rate (cm2/band hour) | 0.24 | R-205 0.23996; R-207 0.23989 and 0.23996; R-301 0.24006; R-302 0.24014; R-410 0.24007; R-501 0.23996 | yes |
| Last-inspection pitting | 1,260 / 650 / 910 / 570 / 0 / 1,050 / 1,350 | same after rounding (blade+band totals, after repair) | yes |
| Pitting at 31 Dec 2026 | 1,650 / 1,250 / 1,990 / 880 / 890 / 2,250 / 1,790 | 1,650.4 / 1,248.1 / 1,989.8 / 882.5 / 889.4 / 2,250.2 / 1,790.8 | yes |
| Pass years | SDL-G1 2029, SDL-G3 2031, NSV-G1 2027, others none | same (SDL-G1 end-2028 2,392.0) | yes |
| Outage MWh | 55,800 / 14,100 / 67,000 | 55,833 / 14,127 / 67,020 | yes |
| MWh per NOK million (excl. VAT) | 3,820 / 990 / 4,650 | 3,824 / 995 / 4,654 | yes |
| Gap | 830 | 829.9 | yes |
| Generation since 2016 (MWh) | 4,542,200 / 4,464,600 / 2,427,200 / 2,710,000 / 557,900 / 2,900,000 / 3,370,200 | identical at 100 MWh | yes |
| Starts | 427 / 423 / 433 / 501 / 6,738 / 383 / 400 | zero-to-generation plus resynchronised breaker trips; ties to every pair in unit_counter_readings.csv (zero-to-generation alone does not tie) | yes |
| Trips | 22 / 16 / 23 / 20 / 15 / 26 / 18 | own generator-breaker trips plus station line-breaker trips in an hour the unit generated; same under hour-beginning or hour-ending stamps | yes |
| Clock | Norwegian local vs UTC | 63,264 rows match local time on every row incl. 7 skips and 7 repeats; 72-hour overlap identical | yes |
| Tag remap | per maintenance log | switch at local midnight 2016-08-01 (OSD), 2017-06-12 (SDL), 2017-07-24 (NSV); tag-map reading gives e.g. SDL-G3 838,500 | yes |

## Competing answers that survived
None. Pooled per-running-hour (about 0.0123, peaker excluded) files NSV-G2 (2030, 6,147 per NOK million), which fails the peaker's pairs; pooled with the peaker passes almost every unit in 2027; latest or oldest-inspection pitting points at OSD units or NSV-G2, none passing under the filed rule. Boundary inclusion moves pitting by about 1 cm2 (at most 6 hours on a bound), no rounded figure. Refurbishment-window downtime is not mentioned, so a literal reading counts none. Variant rates and boundaries keep SDL-G1 at 2029 (thin 8 cm2 margin at end-2028, but it follows from the filed 2026-duty rule).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | 4 (csv, xlsx, docx, pdf) | yes |
| Large file | 25,000+ rows | historian 63,264 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (day-ahead prices, reserve contracts, reservoir inflow) | yes |
| Distractors unused yet weighty | none answers a graded quantity | none enters the arithmetic; the reserve contracts explain the duty step and the duty is read from the units' own output | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-unit tables; rounding and units in the prompt sentence | yes |
| Prompt shape, 25+ criteria | | shape 01 ranked list with one pick; 7 units x 6 cells, pick/runner-up/gap, 7 x 3 ask cells, chart parts, well over 25 | yes |
| Not LLM-generated | | judge: no authoring or provenance leaks, realistic Norwegian layer-1 mess; goldens not re-read by me for realism | yes |

## Gate G reconciliation
Judge: mechanism method_or_model_selection (with forecasting), analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy `other` (wear in one output band), family `estimand_identification`, `stump_class: analytical`; forecasting named as the honest mechanism. Consistent in class and defect posture (the mechanism label differs in wording only, both mean the exposure-variable selection then projection). The judge named the easy route NSV-G2 at 6,147, matching the design note's default path (the pass 1 judge had said SDL-G3). No declared distractor is the surface read carrying the task. Gate G: pass.

Gate H (judge): domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules and the card's analyst_test and domain_test.

## Stump power (Gate F)
Good per judge. The field's reflex (pitting per running hour, or calendar rate) files NSV-G2 or an OSD unit; the band-hour exposure must be found by calibrating across all inspection pairs, with the FCR-N reserve duty since 2022 pushing SDL-G1 and NSV-G1 into the band and the peaker's tenfold running-hour rate as the cross-check. Not a landable textbook route. Caveat for the main thread: unit_register.xlsx's Driftsområder names the 30 to 58 per cent band.

## Findings, ranked
1. No blocking finding. DETERMINISTIC, APPROVE.
2. Cosmetic: outage_planning_note_2027.docx last-modified metadata is 2026-12-09 while it states condition at 31 December 2026 and the quote is dated 6 Nov 2026. No analytic effect; consider aligning the docx modified date.
3. Note: SDL-G1 passes in 2029 with an 8 cm2 margin at end-2028 (2,392.0 vs 2,400); every rate and boundary variant tried keeps the year, and the figure per NOK million would not change even if the year moved within the window.
4. Note: starts and trips (asks) hinge on definitions on the production report page (resynchronised breaker trips count as starts; line-breaker trips count against units generating in that hour). The judge found them forced and tied to unit_counter_readings.csv; not the call.
5. Note: the judge listed the production report among the distractors; metadata.json names three others and the report carries the ask definitions, so this is a judge labelling slip, not a spec issue.

## Next action for the author
Record the pass 2 verdict (DETERMINISTIC, APPROVE) and this report path in pipeline.json's judge block and continue to the ship gates; optionally align the docx modified date.
